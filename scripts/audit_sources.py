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
    "adopt-as-test",
    "evaluate-no-change",
    "merge-into-skill-system",
    "reject",
    "reject-active-skill",
    "retain-existing",
    "retain-split-owners",
}
REQUIRED_SKILL_FIELDS = ("name", "purpose", "overlap", "decision", "reason")


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


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

    for review_path in sorted(reviews_path.glob("*.yaml")):
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
    skill_count = sum(len(load_mapping(path).get("skills", [])) for path in reviews)
    print(f"source_reviews={len(reviews)} reviewed_skills={skill_count} catalog=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
