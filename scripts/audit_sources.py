#!/usr/bin/env python3
"""Validate pinned upstream reviews against the source catalog."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

COMMIT = re.compile(r"^[0-9a-f]{40}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REVIEW_DECISIONS = {
    "adopt-as-new-skill",
    "adopt-as-test",
    "evaluate-no-change",
    "merge-into-skill-system",
    "reject",
    "reject-active-skill",
    "retain-existing",
    "retain-split-owners",
}
REQUIRED_SKILL_FIELDS = ("name", "purpose", "overlap", "decision", "reason")
REQUIRED_GROUP_FIELDS = ("id", "purpose", "overlap", "decision", "reason")
SUPPLY_CHAIN_FIELDS = (
    "source_files_reviewed",
    "scripts_reviewed",
    "dependency_files_reviewed",
    "effects",
    "network",
    "writes",
    "shell",
    "installation",
)


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def reviewed_skill_names(review: dict[str, Any]) -> list[str]:
    """Return the canonical reviewed names for either supported review shape."""
    inventory = review.get("inventory")
    if isinstance(inventory, list):
        return [name for name in inventory if isinstance(name, str)]
    skills = review.get("skills")
    if not isinstance(skills, list):
        return []
    return [
        item["name"]
        for item in skills
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    ]


def audit_grouped_review(review_path: Path, review: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    inventory = review.get("inventory")
    groups = review.get("groups")
    if not isinstance(inventory, list):
        return [f"{review_path}: inventory must be a list"]
    if not isinstance(groups, list):
        return [f"{review_path}: groups must be a list"]

    inventory_names: set[str] = set()
    for position, name in enumerate(inventory, start=1):
        if not isinstance(name, str) or not name.strip():
            errors.append(
                f"{review_path}: inventory {position} must be a non-empty string"
            )
            continue
        if name in inventory_names:
            errors.append(f"{review_path}: duplicate inventory skill {name!r}")
        inventory_names.add(name)

    covered: set[str] = set()
    group_ids: set[str] = set()
    for position, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            errors.append(f"{review_path}: group {position} must be a mapping")
            continue
        for field in REQUIRED_GROUP_FIELDS:
            if not isinstance(group.get(field), str) or not group[field].strip():
                errors.append(f"{review_path}: group {position} missing {field}")
        group_id = group.get("id")
        if isinstance(group_id, str):
            if group_id in group_ids:
                errors.append(f"{review_path}: duplicate group {group_id!r}")
            group_ids.add(group_id)
        decision = group.get("decision")
        if decision not in REVIEW_DECISIONS:
            errors.append(f"{review_path}: unsupported decision {decision!r}")

        members = group.get("skills")
        if not isinstance(members, list) or not members:
            errors.append(
                f"{review_path}: group {position} skills must be a non-empty list"
            )
            continue
        for member in members:
            if not isinstance(member, str) or not member.strip():
                errors.append(f"{review_path}: group {position} has invalid skill name")
                continue
            if member not in inventory_names:
                errors.append(
                    f"{review_path}: group skill {member!r} is outside inventory"
                )
            if member in covered:
                errors.append(
                    f"{review_path}: skill {member!r} appears in multiple groups"
                )
            covered.add(member)

    uncovered = sorted(inventory_names - covered)
    if uncovered:
        errors.append(
            f"{review_path}: inventory skills are uncovered: {', '.join(uncovered)}"
        )
    return errors


def audit_sources(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "sources" / "catalog.yaml"
    reviews_path = root / "sources" / "reviews"
    if not catalog_path.exists():
        return ["sources/catalog.yaml: missing"]

    catalog = load_mapping(catalog_path)
    repositories = catalog.get("repositories", [])
    if not isinstance(repositories, list):
        return ["sources/catalog.yaml: repositories must be a list"]

    indexed: dict[str, dict[str, Any]] = {}
    for item in repositories:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append("sources/catalog.yaml: repository requires string id")
            continue
        source_id = item["id"]
        if source_id in indexed:
            errors.append(f"sources/catalog.yaml: duplicate repository {source_id!r}")
        indexed[source_id] = item

    review_paths = sorted(reviews_path.glob("*.yaml"))
    review_ids = {path.stem for path in review_paths}
    required_reviews = {
        source_id
        for source_id, item in indexed.items()
        if item.get("review_required") is True
    }
    missing_reviews = sorted(required_reviews - review_ids)
    if missing_reviews:
        errors.append(
            "sources/catalog.yaml: required reviews are missing: "
            + ", ".join(missing_reviews)
        )

    for source_id in sorted(required_reviews):
        catalog_item = indexed[source_id]
        improves = catalog_item.get("improves")
        if not isinstance(improves, list) or not improves:
            errors.append(
                f"sources/catalog.yaml: required review {source_id!r} needs improves"
            )
            continue
        for target in improves:
            if not isinstance(target, str) or not target.strip():
                errors.append(
                    f"sources/catalog.yaml: {source_id!r} has invalid improves target"
                )
            elif not (root / target).exists():
                errors.append(
                    f"sources/catalog.yaml: {source_id!r} improves target "
                    f"does not exist: {target}"
                )

    for review_path in review_paths:
        review = load_mapping(review_path)
        source_id = review_path.stem
        catalog_item = indexed.get(source_id)
        if catalog_item is None:
            errors.append(f"{review_path}: source is missing from catalog")
            continue

        for field in (
            "repository",
            "upstream",
            "checked_commit",
            "checked_version",
            "license",
            "decision",
        ):
            if not isinstance(review.get(field), str) or not review[field].strip():
                errors.append(f"{review_path}: missing string {field}")
        evidence = review.get("evidence")
        if not isinstance(evidence, dict) or not evidence:
            errors.append(f"{review_path}: evidence must be a non-empty mapping")
        if catalog_item.get("supply_chain_required") is True:
            supply_chain = review.get("supply_chain")
            if not isinstance(supply_chain, dict):
                errors.append(f"{review_path}: supply_chain must be a mapping")
            else:
                for field in SUPPLY_CHAIN_FIELDS:
                    value = supply_chain.get(field)
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"{review_path}: supply_chain missing {field}")

        commit = review.get("checked_commit", "")
        if not isinstance(commit, str) or COMMIT.fullmatch(commit) is None:
            errors.append(f"{review_path}: checked_commit must be 40 lowercase hex")
        checked_at = review.get("checked_at", "")
        checked_at_text = (
            checked_at.isoformat() if isinstance(checked_at, date) else checked_at
        )
        if (
            not isinstance(checked_at_text, str)
            or DATE.fullmatch(checked_at_text) is None
        ):
            errors.append(f"{review_path}: checked_at must use YYYY-MM-DD")
        for field in ("upstream", "checked_commit", "checked_version", "license"):
            if review.get(field) != catalog_item.get(field):
                errors.append(f"{review_path}: {field} differs from source catalog")

        grouped = "inventory" in review or "groups" in review
        if grouped and "skills" in review:
            errors.append(
                f"{review_path}: use either skills or inventory/groups, not both"
            )
            continue
        if grouped:
            errors.extend(audit_grouped_review(review_path, review))
            reviewed = reviewed_skill_names(review)
            scope = review.get("scope", {})
            declared = scope.get("skill_files") if isinstance(scope, dict) else None
            if declared != len(reviewed):
                errors.append(
                    f"{review_path}: scope.skill_files={declared!r}, reviewed={len(reviewed)}"
                )
            continue

        skills = review.get("skills", [])
        if not isinstance(skills, list):
            errors.append(f"{review_path}: skills must be a list")
            continue
        scope = review.get("scope", {})
        declared = scope.get("skill_files") if isinstance(scope, dict) else None
        if declared != len(skills):
            errors.append(
                f"{review_path}: scope.skill_files={declared!r}, reviewed={len(skills)}"
            )

        names: set[str] = set()
        for position, skill in enumerate(skills, start=1):
            if not isinstance(skill, dict):
                errors.append(f"{review_path}: skill {position} must be a mapping")
                continue
            for field in REQUIRED_SKILL_FIELDS:
                if not isinstance(skill.get(field), str) or not skill[field].strip():
                    errors.append(f"{review_path}: skill {position} missing {field}")
            name = skill.get("name")
            if isinstance(name, str):
                if name in names:
                    errors.append(f"{review_path}: duplicate skill {name!r}")
                names.add(name)
            decision = skill.get("decision")
            if decision not in REVIEW_DECISIONS:
                errors.append(f"{review_path}: unsupported decision {decision!r}")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = audit_sources(root)
    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1
    reviews = sorted((root / "sources" / "reviews").glob("*.yaml"))
    skill_count = sum(len(reviewed_skill_names(load_mapping(path))) for path in reviews)
    print(f"source_reviews={len(reviews)} reviewed_skills={skill_count} catalog=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
