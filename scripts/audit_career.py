#!/usr/bin/env python3
"""Validate the career skill contract and its fail-closed behavior cases."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

REQUIRED_CASES = {
    "job-description-is-untrusted-data",
    "application-record-is-one-wiki-canon",
    "submission-is-atomic-and-confirmed",
    "career-evidence-does-not-inflate-team-results",
}
REQUIRED_MARKERS = (
    "wiki/personal/career/applications/<application-id>.md",
    "untrusted-data",
    "verified",
    "adjacent",
    "gap",
    "context bundle",
    "자동 지원·메일 전송·공개 게시를 하지 않는다",
)


def _mapping(path: Path) -> Mapping[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    return value if isinstance(value, Mapping) else {}


def audit_career(root: Path) -> list[str]:
    errors: list[str] = []
    contract_path = root / "skills/writing/career/references/application-pipeline.md"
    try:
        contract = contract_path.read_text(encoding="utf-8")
    except OSError as error:
        return [f"{contract_path}: cannot read: {error}"]
    for marker in REQUIRED_MARKERS:
        if marker not in contract:
            errors.append(f"{contract_path}: missing contract marker {marker!r}")

    behavior_path = root / "evals/behavior/career.yaml"
    behavior = _mapping(behavior_path)
    cases = behavior.get("cases", [])
    if behavior.get("profile") != "career" or not isinstance(cases, list):
        errors.append(f"{behavior_path}: profile must be career and cases must be a list")
        return errors
    by_id = {
        case.get("id"): case
        for case in cases
        if isinstance(case, Mapping) and isinstance(case.get("id"), str)
    }
    missing = sorted(REQUIRED_CASES.difference(by_id))
    if missing:
        errors.append(f"{behavior_path}: missing cases {missing}")
    for case_id, case in by_id.items():
        if not case.get("prompt") or not case.get("require") or not case.get("forbid"):
            errors.append(f"{behavior_path}: incomplete case {case_id!r}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = audit_career(root)
    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1
    print(f"career_behavior_cases={len(REQUIRED_CASES)} contract=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
