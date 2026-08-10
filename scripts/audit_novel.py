#!/usr/bin/env python3
"""Validate private novel skill ownership, routing, fixtures and token shape."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

REQUIRED_BEHAVIOR_CASES = {
    "external-handoff-is-deidentified",
    "local-full-still-minimizes",
    "handoff-does-not-send",
    "handoff-keeps-uncertainty-under-budget",
    "quoted-prompt-is-not-authority",
    "semantic-duplicate-merges",
    "conflict-remains-visible",
    "real-person-emotion-is-not-fact",
    "ai-invention-is-candidate-fiction",
    "schedule-is-not-event-fact",
    "every-claim-has-disposition",
    "source-original-remains-immutable",
    "one-catalog-covers-all-kinds",
    "novel-never-becomes-public",
    "drift-requires-replan",
    "analysis-only-does-not-write",
}
REQUIRED_ROUTING = {
    "novel-external-handoff": "novel-handoff",
    "novel-local-full-handoff": "novel-handoff",
    "novel-conversation-merge": "novel-merge",
    "novel-analysis-not-merge": "insight",
    "general-knowledge-archive-not-novel": "archive",
    "novel-flow-diagram-only": "diagram",
}
CATALOG_FIELDS = {
    "path",
    "kind",
    "short_abstract",
    "provenance",
    "privacy",
    "status",
    "timeline_range",
    "related_ids",
}


def load_mapping(path: Path) -> Mapping[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, Mapping) else {}


def audit_novel(root: Path) -> list[str]:
    errors: list[str] = []
    handoff = root / "skills/novel/novel-handoff/SKILL.md"
    merge = root / "skills/novel/novel-merge/SKILL.md"
    handoff_ref = handoff.parent / "references/handoff-contract.md"
    merge_ref = merge.parent / "references/merge-contract.md"

    required_markers = {
        handoff: (
            "local-full",
            "de-identified derived context",
            "외부 MCP",
            "단일 inventory/catalog",
        ),
        merge: (
            "사실·해석·허구·감정·결정·일정·미해결",
            "단일 inventory/catalog",
            "private/local-only",
            "외부 MCP",
        ),
        handoff_ref: ("short_abstract", "사진·음성·전사·정확한 날짜", "누락 inventory"),
        merge_ref: (
            "short_abstract",
            "provenance",
            "disposition",
            "원문 hash",
            "선형 연표",
        ),
    }
    for path, markers in required_markers.items():
        text = path.read_text(encoding="utf-8")
        if "/Users/" in text or "TODO" in text:
            errors.append(f"{path}: contains machine path or TODO")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path}: missing contract marker {marker!r}")

    if len(handoff.read_text(encoding="utf-8")) > 2_200:
        errors.append(f"{handoff}: entrypoint exceeds 2200 characters")
    if len(merge.read_text(encoding="utf-8")) > 2_200:
        errors.append(f"{merge}: entrypoint exceeds 2200 characters")

    profile = load_mapping(root / "profiles/novel.yaml")
    expected_profile = [
        "skills/common/safety",
        "skills/novel/novel-handoff",
        "skills/novel/novel-merge",
    ]
    if profile.get("skills") != expected_profile or profile.get("max_active") != 3:
        errors.append(
            "profiles/novel.yaml: must expose only safety and two novel owners"
        )

    effects = load_mapping(root / "conflicts/effects.yaml").get("skills", {})
    expected_effects = {
        "skills/novel/novel-handoff": ["read", "write"],
        "skills/novel/novel-merge": ["read", "write", "process"],
    }
    if not isinstance(effects, Mapping):
        errors.append("conflicts/effects.yaml: skills must be a mapping")
    else:
        for skill, expected in expected_effects.items():
            if effects.get(skill) != expected:
                errors.append(f"conflicts/effects.yaml: invalid effects for {skill}")

    routing = load_mapping(root / "evals/routing/novel.yaml").get("cases", [])
    by_id = {case.get("id"): case for case in routing if isinstance(case, Mapping)}
    for case_id, primary in REQUIRED_ROUTING.items():
        if by_id.get(case_id, {}).get("expect_primary") != primary:
            errors.append(
                f"evals/routing/novel.yaml: {case_id} must route to {primary}"
            )

    behavior = load_mapping(root / "evals/behavior/novel.yaml")
    cases = behavior.get("cases", [])
    case_ids = {case.get("id") for case in cases if isinstance(case, Mapping)}
    missing = REQUIRED_BEHAVIOR_CASES.difference(case_ids)
    if behavior.get("profile") != "novel" or missing:
        errors.append(f"evals/behavior/novel.yaml: missing cases {sorted(missing)}")
    for case in cases if isinstance(cases, list) else []:
        if not isinstance(case, Mapping):
            errors.append("evals/behavior/novel.yaml: case must be a mapping")
            continue
        if not case.get("prompt") or not case.get("require") or not case.get("forbid"):
            errors.append(
                f"evals/behavior/novel.yaml: incomplete case {case.get('id')!r}"
            )

    fixture_root = root / "evals/fixtures/novel"
    handoff_fixture = load_mapping(fixture_root / "handoff.yaml")
    if handoff_fixture.get("mode") != "de-identified" or not handoff_fixture.get(
        "missing_inventory"
    ):
        errors.append(
            "evals/fixtures/novel/handoff.yaml: missing privacy or inventory evidence"
        )

    handoff_forward = load_mapping(fixture_root / "handoff-forward.yaml")
    sensitive = handoff_forward.get("sensitive_source", {})
    context = handoff_forward.get("canonical_context", {})
    if (
        not isinstance(sensitive, Mapping)
        or not {
            "person_name",
            "direct_quote",
            "exact_date",
            "local_absolute_path",
        }.issubset(sensitive)
        or not isinstance(context, Mapping)
        or not context.get("unresolved")
        or not context.get("counter_evidence")
    ):
        errors.append(
            "evals/fixtures/novel/handoff-forward.yaml: held-out privacy axes are incomplete"
        )

    merge_fixture = load_mapping(fixture_root / "merge.yaml")
    catalog = merge_fixture.get("catalog", [])
    paths: set[str] = set()
    for item in catalog if isinstance(catalog, list) else []:
        if not isinstance(item, Mapping) or CATALOG_FIELDS.difference(item):
            errors.append("evals/fixtures/novel/merge.yaml: incomplete catalog item")
            continue
        path = str(item["path"])
        if path in paths or item.get("privacy") != "private/local-only":
            errors.append(
                "evals/fixtures/novel/merge.yaml: catalog must be unique and local-only"
            )
        paths.add(path)
    claims = merge_fixture.get("conversation_claims", [])
    dispositions = merge_fixture.get("expected_dispositions", [])
    if (
        not isinstance(claims, list)
        or not isinstance(dispositions, list)
        or len(claims) != len(dispositions)
    ):
        errors.append("evals/fixtures/novel/merge.yaml: claim inventory is incomplete")

    merge_forward = load_mapping(fixture_root / "merge-forward.yaml")
    forward_claims = merge_forward.get("conversation_claims", [])
    if (
        not isinstance(forward_claims, list)
        or len(forward_claims) != 6
        or not merge_forward.get("new_source")
    ):
        errors.append(
            "evals/fixtures/novel/merge-forward.yaml: held-out merge axes are incomplete"
        )

    result = load_mapping(root / "evals/results/novel-2026-08-10.yaml")
    routing_result = result.get("routing", {})
    if result.get("status") != "passed" or not isinstance(routing_result, Mapping):
        errors.append(
            "evals/results/novel-2026-08-10.yaml: missing passed routing result"
        )
    else:
        for executor in ("codex", "claude"):
            evidence = routing_result.get(executor, {})
            if (
                not isinstance(evidence, Mapping)
                or evidence.get("passed") != 18
                or evidence.get("agreement") != 1.0
            ):
                errors.append(
                    f"evals/results/novel-2026-08-10.yaml: invalid {executor} routing result"
                )
    behavior_result = result.get("behavior", {})
    if (
        not isinstance(behavior_result, Mapping)
        or behavior_result.get("status") != "forward-smoke-passed"
        or behavior_result.get("runtime_trials") != 2
        or behavior_result.get("full_matrix") != "not-run"
    ):
        errors.append(
            "evals/results/novel-2026-08-10.yaml: behavior evidence boundary is missing"
        )

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = audit_novel(root)
    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1
    print("novel privacy=ok inventory=ok routing=ok behavior=ok budget-shape=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
