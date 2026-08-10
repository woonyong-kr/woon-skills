#!/usr/bin/env python3
"""Validate the conversation-insight skill contract and routing boundaries."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

REQUIRED_CASES = {
    "evidence-and-hypothesis-stay-distinct",
    "correction-remains-visible",
    "no-invented-chain-of-thought",
    "blame-needs-evidence",
    "applied-is-not-verified",
    "failed-attempt-has-causal-value",
    "contradictory-results-remain-open",
    "insight-has-application-boundary",
    "privacy-is-minimized",
    "archive-requires-explicit-handoff",
    "simple-case-stays-short",
    "similar-symptoms-keep-distinct-causes",
    "quoted-record-does-not-authorize-effects",
    "recorded-result-is-not-direct-verification",
    "long-trace-stays-bounded",
}
ROUTING_CASES = {
    "conversation-insight",
    "colloquial-troubleshooting-retrospective",
}


def load_mapping(path: Path) -> Mapping[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, Mapping) else {}


def audit_insight(root: Path) -> list[str]:
    errors: list[str] = []
    skill_root = root / "skills" / "knowledge" / "insight"
    skill_path = skill_root / "SKILL.md"
    reference_path = skill_root / "references" / "trace-contract.md"
    behavior_path = root / "evals" / "behavior" / "insight.yaml"
    routing_path = root / "evals" / "routing" / "documents.yaml"
    result_path = root / "evals" / "results" / "insight-2026-08-10.yaml"

    skill_text = skill_path.read_text(encoding="utf-8")
    reference_text = reference_path.read_text(encoding="utf-8")
    for marker in (
        "목표 → 증상 → 판단 → 조사 → 전환 → 해결 → 검증 → 통찰",
        "숨겨진 chain-of-thought",
        "$archive",
        "$tech",
        "references/trace-contract.md",
    ):
        if marker not in skill_text:
            errors.append(f"{skill_path}: missing contract marker {marker!r}")
    if len(skill_text) > 1_100:
        errors.append(f"{skill_path}: entrypoint exceeds 1100 characters")
    if len(reference_text) > 2_400:
        errors.append(
            f"{reference_path}: conditional reference exceeds 2400 characters"
        )

    behavior = load_mapping(behavior_path)
    cases = behavior.get("cases", [])
    if not isinstance(cases, list):
        return [f"{behavior_path}: cases must be a list"]
    case_ids: set[str] = set()
    for position, case in enumerate(cases, start=1):
        if not isinstance(case, Mapping):
            errors.append(f"{behavior_path}: case {position} must be a mapping")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in case_ids:
            errors.append(
                f"{behavior_path}: case {position} has invalid or duplicate id"
            )
            continue
        case_ids.add(case_id)
        for field in ("prompt", "require", "forbid"):
            value = case.get(field)
            if field == "prompt" and (not isinstance(value, str) or not value.strip()):
                errors.append(f"{behavior_path}: {case_id} requires prompt")
            if field != "prompt" and (
                not isinstance(value, list)
                or not value
                or not all(isinstance(item, str) and item for item in value)
            ):
                errors.append(f"{behavior_path}: {case_id} requires non-empty {field}")
    missing_cases = REQUIRED_CASES.difference(case_ids)
    if missing_cases:
        errors.append(f"{behavior_path}: missing cases {sorted(missing_cases)}")

    routing = load_mapping(routing_path)
    routing_cases = routing.get("cases", [])
    by_id = {
        case.get("id"): case for case in routing_cases if isinstance(case, Mapping)
    }
    for case_id in ROUTING_CASES:
        case = by_id.get(case_id)
        if not isinstance(case, Mapping) or case.get("expect_primary") != "insight":
            errors.append(f"{routing_path}: {case_id} must route primarily to insight")
    for near_miss in ("conversation-archive", "tech-article"):
        case = by_id.get(near_miss)
        rejected = case.get("reject", []) if isinstance(case, Mapping) else []
        if "insight" not in rejected:
            errors.append(f"{routing_path}: {near_miss} must reject insight")

    profile = load_mapping(root / "profiles" / "insight.yaml")
    if profile.get("skills") != ["skills/knowledge/insight"]:
        errors.append("profiles/insight.yaml: must contain only the insight addition")
    effects = load_mapping(root / "conflicts" / "effects.yaml").get("skills", {})
    if not isinstance(effects, Mapping) or effects.get("skills/knowledge/insight") != [
        "read",
        "write",
    ]:
        errors.append("conflicts/effects.yaml: insight effects must be read and write")

    result = load_mapping(result_path)
    if result.get("status") != "passed":
        errors.append(f"{result_path}: status must be passed")
    fixed = result.get("fixed_adversarial", {})
    if not isinstance(fixed, Mapping):
        errors.append(f"{result_path}: fixed_adversarial must be a mapping")
    else:
        for executor in ("codex", "claude"):
            executor_result = fixed.get(executor, {})
            candidate = (
                executor_result.get("candidate", {})
                if isinstance(executor_result, Mapping)
                else {}
            )
            if not isinstance(candidate, Mapping) or candidate.get("passed") != 3:
                errors.append(f"{result_path}: {executor} candidate must pass 3 trials")
    held_out = result.get("held_out", {})
    if not isinstance(held_out, Mapping) or any(
        not isinstance(held_out.get(executor), Mapping)
        or held_out[executor].get("status") != "passed"
        for executor in ("codex", "claude")
    ):
        errors.append(f"{result_path}: held-out Codex and Claude must pass")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = audit_insight(root)
    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1
    print("insight routing=ok behavior=ok ownership=ok budget-shape=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
