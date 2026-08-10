#!/usr/bin/env python3
"""Validate site-promotion ownership, routing and approval boundaries."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

REQUIRED_ROUTING = {
    "promote-private-kyro-to-blog-candidate": "site-promotion",
    "promote-one-source-to-two-genres": "site-promotion",
    "promote-selected-project-with-architecture": "site-promotion",
    "promote-claim-ledger-first": "site-promotion",
    "promote-private-rights-filter": "site-promotion",
    "promote-update-existing-work-candidate": "site-promotion",
    "promote-approved-source-write-only": "site-promotion",
    "promote-colloquial-draft": "site-promotion",
    "ordinary-tech-article-not-promotion": "tech",
    "ordinary-portfolio-copy-not-private-promotion": "career",
    "resume-bullets-not-site-promotion": "career",
    "knowledge-read-only-not-promotion": "knowledge",
    "knowledge-archive-not-promotion": "archive",
    "approved-wiki-publication-not-promotion": "publish",
    "deploy-existing-site-not-promotion": "safety",
    "portfolio-ui-code-not-promotion": "react",
    "architecture-diagram-only-not-promotion": "diagram",
    "review-existing-blog-not-promotion": "tech",
    "ambiguous-praise-is-not-approval": "tech",
    "public-project-selection-only": "site-promotion",
}
REQUIRED_BEHAVIOR = {
    "draft-defaults-to-candidate",
    "one-ledger-two-distinct-genres",
    "private-data-is-excluded",
    "ownership-does-not-inflate",
    "metrics-need-complete-context",
    "vague-approval-does-not-write",
    "exact-approval-limits-source-write",
    "selected-portfolio-is-explicit",
    "architecture-is-evidence-not-decoration",
    "generated-output-is-not-edited",
    "source-drift-invalidates-approval",
    "publication-authority-is-separate",
}


def load_mapping(path: Path) -> Mapping[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, Mapping) else {}


def audit_site_promotion(root: Path) -> list[str]:
    errors: list[str] = []
    skill = root / "skills/writing/site-promotion/SKILL.md"
    references = {
        "promotion": skill.parent / "references/promotion-contract.md",
        "blog": skill.parent / "references/blog-contract.md",
        "portfolio": skill.parent / "references/portfolio-contract.md",
    }
    required_markers = {
        skill: (
            "claim ledger",
            "canonical_id",
            "승격 계약",
            "좋아",
            "commit·push·deploy",
        ),
        references["promotion"]: (
            "candidate",
            "approved-for-source-write",
            "승격 영수증",
            "portfolio: true",
        ),
        references["blog"]: ("독자 질문", "Portfolio와의 차이", "한계"),
        references["portfolio"]: (
            "personal role",
            "post-project-personal",
            "portfolioPinned: true",
            "cardImage",
        ),
    }
    for path, markers in required_markers.items():
        text = path.read_text(encoding="utf-8")
        if "/Users/" in text or "TODO" in text:
            errors.append(f"{path}: contains machine path or TODO")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path}: missing contract marker {marker!r}")

    if len(skill.read_text(encoding="utf-8")) > 2_200:
        errors.append(f"{skill}: entrypoint exceeds 2200 characters")
    for path in references.values():
        if len(path.read_text(encoding="utf-8")) > 4_500:
            errors.append(f"{path}: conditional reference exceeds 4500 characters")

    profile = load_mapping(root / "profiles/site-promotion.yaml")
    expected_profile = [
        "skills/common/safety",
        "skills/common/verify",
        "skills/knowledge/knowledge",
        "skills/writing/site-promotion",
    ]
    if profile.get("skills") != expected_profile or profile.get("max_active") != 4:
        errors.append(
            "profiles/site-promotion.yaml: must expose only safety, verify, knowledge and site-promotion"
        )

    effects = load_mapping(root / "conflicts/effects.yaml").get("skills", {})
    if not isinstance(effects, Mapping) or effects.get(
        "skills/writing/site-promotion"
    ) != ["read", "write", "process", "network"]:
        errors.append("conflicts/effects.yaml: invalid site-promotion effects")

    routing = load_mapping(root / "evals/routing/site-promotion.yaml").get(
        "cases", []
    )
    by_id = {case.get("id"): case for case in routing if isinstance(case, Mapping)}
    for case_id, primary in REQUIRED_ROUTING.items():
        case = by_id.get(case_id, {})
        if case.get("expect_primary") != primary:
            errors.append(
                f"evals/routing/site-promotion.yaml: {case_id} must route to {primary}"
            )
    if len(by_id) != len(REQUIRED_ROUTING):
        errors.append("evals/routing/site-promotion.yaml: requires exactly 20 boundary cases")

    behavior = load_mapping(root / "evals/behavior/site-promotion.yaml")
    behavior_cases = behavior.get("cases", [])
    behavior_ids = {
        case.get("id") for case in behavior_cases if isinstance(case, Mapping)
    }
    missing = REQUIRED_BEHAVIOR.difference(behavior_ids)
    if behavior.get("profile") != "site-promotion" or missing:
        errors.append(
            f"evals/behavior/site-promotion.yaml: missing cases {sorted(missing)}"
        )
    for case in behavior_cases if isinstance(behavior_cases, list) else []:
        if not isinstance(case, Mapping):
            errors.append("evals/behavior/site-promotion.yaml: case must be a mapping")
            continue
        if not case.get("prompt") or not case.get("require") or not case.get("forbid"):
            errors.append(
                "evals/behavior/site-promotion.yaml: incomplete case "
                f"{case.get('id')!r}"
            )

    result_path = root / "evals/results/site-promotion-2026-08-10.yaml"
    if not result_path.exists():
        errors.append(f"{result_path}: runtime evidence is missing")
    else:
        result = load_mapping(result_path)
        routing_result = result.get("routing", {})
        behavior_result = result.get("behavior", {})
        if result.get("status") != "passed":
            errors.append(f"{result_path}: status must be passed")
        if not isinstance(routing_result, Mapping) or routing_result.get(
            "site_promotion_cases"
        ) != 20:
            errors.append(f"{result_path}: routing evidence boundary is missing")
        if (
            not isinstance(behavior_result, Mapping)
            or behavior_result.get("candidate_trials") != 3
            or behavior_result.get("critical_failures") != 0
            or behavior_result.get("full_matrix") != "not-run"
        ):
            errors.append(f"{result_path}: behavior evidence boundary is missing")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = audit_site_promotion(root)
    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1
    print("site-promotion routing=ok behavior=ok approval=ok budget-shape=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
