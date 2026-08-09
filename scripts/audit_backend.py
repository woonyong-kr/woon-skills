#!/usr/bin/env python3
"""Validate backend skill ownership, routing, behavior and profile wiring."""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

BACKEND_SKILLS = {
    "auth",
    "cache",
    "capacity",
    "domain",
    "event",
    "job",
    "observe",
    "privacy",
    "protocol",
    "resilience",
    "storage",
    "tenant",
    "tx",
}
TX_CASES = {
    "tx-nested-retry-amplification",
    "tx-outbox-relay-crash",
    "tx-remote-effect-local-failure",
    "tx-response-loss-replay",
    "tx-stale-lease-worker",
    "tx-write-skew",
}
MACHINE_PATH = re.compile(r"/Users/|/home/[^/]+|[A-Za-z]:\\\\Users\\\\")


def load_mapping(path: Path) -> Mapping[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, Mapping) else {}


def audit_backend(root: Path) -> list[str]:
    errors: list[str] = []
    behavior_path = root / "evals" / "behavior" / "backend-deep.yaml"
    routing_path = root / "evals" / "routing" / "engineering.yaml"
    effects_path = root / "conflicts" / "effects.yaml"
    eval_profile_path = root / "profiles" / "eval.yaml"

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

    missing_tx = TX_CASES.difference(case_ids)
    if missing_tx:
        errors.append(f"{behavior_path}: missing tx cases {sorted(missing_tx)}")

    routing = load_mapping(routing_path)
    routing_cases = routing.get("cases", [])
    routed = {
        case.get("expect_primary")
        for case in routing_cases
        if isinstance(case, Mapping)
    }
    missing_routing = BACKEND_SKILLS.difference(routed)
    if missing_routing:
        errors.append(
            f"{routing_path}: missing primary routing {sorted(missing_routing)}"
        )

    effects_text = effects_path.read_text(encoding="utf-8")
    eval_profile_text = eval_profile_path.read_text(encoding="utf-8")
    for name in sorted(BACKEND_SKILLS):
        skill_files = list((root / "skills").glob(f"**/{name}/SKILL.md"))
        if len(skill_files) != 1:
            errors.append(f"skills: backend owner {name!r} must resolve exactly once")
            continue
        relative = skill_files[0].parent.relative_to(root).as_posix()
        if f"  {relative}:" not in effects_text:
            errors.append(f"{effects_path}: missing {relative}")
        if f"  - {relative}" not in eval_profile_text:
            errors.append(f"{eval_profile_path}: missing {relative}")
        for file in skill_files[0].parent.rglob("*"):
            if file.is_file():
                text = file.read_text(encoding="utf-8")
                if "[TODO" in text or "TODO:" in text:
                    errors.append(f"{file}: placeholder remains")
                if MACHINE_PATH.search(text):
                    errors.append(f"{file}: machine-local path is forbidden")

    tx_text = (root / "skills" / "backend" / "tx" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    for reference in ("atomicity.md", "idempotency.md", "verification.md"):
        if f"references/{reference}" not in tx_text:
            errors.append(f"skills/backend/tx/SKILL.md: missing {reference} routing")

    for owner in (
        root / "skills" / "architecture" / "hexagonal" / "SKILL.md",
        root / "skills" / "backend" / "api" / "SKILL.md",
    ):
        if "$tx" not in owner.read_text(encoding="utf-8"):
            errors.append(f"{owner}: must route transaction details to $tx")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = audit_backend(root)
    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1
    print(f"backend_skills={len(BACKEND_SKILLS)} routing=ok behavior=ok ownership=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
