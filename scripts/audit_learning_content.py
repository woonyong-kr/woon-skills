#!/usr/bin/env python3
"""Validate the learning-content quality and behavior contracts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def non_empty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def audit_learning_content(root: Path) -> list[str]:
    errors: list[str] = []
    standard_path = root / "standards/learning-content-quality.md"
    compile_skill_path = root / "skills/knowledge/compile-knowledge/SKILL.md"
    kotlin_plan_skill_path = root / "skills/learning/kotlin-in-action-14-days/SKILL.md"
    quality_path = root / "evals/quality/learning-content.yaml"
    behavior_path = root / "evals/behavior/learning-content.yaml"
    result_paths = sorted((root / "evals/results").glob("learning-content-*.yaml"))
    if not quality_path.exists():
        return [f"{quality_path}: missing"]
    if not behavior_path.exists():
        return [f"{behavior_path}: missing"]
    if not result_paths:
        return [f"{root / 'evals/results'}: learning-content result is missing"]

    for path in (standard_path, compile_skill_path, kotlin_plan_skill_path):
        if not path.exists():
            errors.append(f"{path}: missing")
    if standard_path.exists():
        standard_text = standard_path.read_text(encoding="utf-8")
        for required in (
            "원문에 없는 인출·전이 문제",
            "선형 이동은 Map과 `prerequisites`·`next_concepts` metadata가 소유한다",
            "모든 원문 code를 verbatim으로 exact-once 보존한다",
            "fragment·dependency·intentional-error·placeholder",
            "synthetic wrapper·대체 code는 만들지 않는다",
        ):
            if required not in standard_text:
                errors.append(f"{standard_path}: missing book source-only rule: {required}")
        if "자료를 닫고 푸는 인출·전이 문제와 원문 목차의 바로 인접한 이전·다음 링크를 둔다" in standard_text:
            errors.append(f"{standard_path}: legacy book workflow injection rule remains")
        for legacy in (
            "faithful static+harness",
            "같은 static-exception harness",
            "각 원문 예제는 독자가 개별 실행할 수 있는 고유 block을 가져야 한다",
            "같은 leaf의 source-faithful runnable harness",
        ):
            if legacy in standard_text:
                errors.append(f"{standard_path}: legacy runnable contract remains: {legacy}")
    if compile_skill_path.exists():
        compile_text = compile_skill_path.read_text(encoding="utf-8")
        if "`source-landed`와 `translated` leaf authored body에는 원문에 없는" not in compile_text:
            errors.append(f"{compile_skill_path}: missing source-only book leaf rule")
        for required in (
            "exact-once 배정하고 verbatim으로 보존한다",
            "fragment|dependency|intentional-error|placeholder",
            "synthetic wrapper·harness나 대체 code",
        ):
            if required not in compile_text:
                errors.append(f"{compile_skill_path}: missing static-only rule: {required}")
        if "실행 전 예측·실제 output·원인·한 가지 변형·Reset 가능 상태를 함께 검증한다" in compile_text:
            errors.append(f"{compile_skill_path}: legacy runnable prose injection rule remains")
    if kotlin_plan_skill_path.exists():
        kotlin_plan_text = kotlin_plan_skill_path.read_text(encoding="utf-8")
        if "personal/projects/kotlin-in-action-14-days" not in kotlin_plan_text:
            errors.append(f"{kotlin_plan_skill_path}: project progress owner is missing")
        if "책 leaf에 `직접 확인하기`" not in kotlin_plan_text:
            errors.append(f"{kotlin_plan_skill_path}: book canonical write prohibition is missing")

    quality = load_mapping(quality_path)
    if quality.get("version") != 1:
        errors.append(f"{quality_path}: version must be 1")
    standard = quality.get("standard")
    prefix = "repo://skills/"
    if not isinstance(standard, str) or not standard.startswith(prefix):
        errors.append(f"{quality_path}: standard must use repo://skills/")
    elif not (root / standard.removeprefix(prefix)).exists():
        errors.append(f"{quality_path}: standard target does not exist")

    contract_targets: dict[str, Path] = {}
    for field, expected_name in (
        ("writing_harness", "learning-writing-harness.md"),
        ("style_corpus", "learning-style-corpus.yaml"),
    ):
        value = quality.get(field)
        if not isinstance(value, str) or not value.startswith(prefix):
            errors.append(f"{quality_path}: {field} must use repo://skills/")
            continue
        target = root / value.removeprefix(prefix)
        if not target.exists() or target.name != expected_name:
            errors.append(f"{quality_path}: {field} target does not exist")
        else:
            contract_targets[field] = target

    harness_path = contract_targets.get("writing_harness")
    if harness_path is not None:
        harness = harness_path.read_text(encoding="utf-8")
        required_sections = (
            "## Canonical lifecycle",
            "## Claim unit contract",
            "## Input contract",
            "## Adaptive route selection",
            "## Writing state machine",
            "## Korean prose renderer",
            "## Block contracts",
            "## LLM execution protocol",
            "## Reject rules",
            "## Final reader check",
        )
        for heading in required_sections:
            if heading not in harness:
                errors.append(f"{harness_path}: missing {heading}")

    learning_context_uri = "repo://skills/skills/writing/tech/scripts/learning-context.sh"
    for integration_path in (
        root / "skills/knowledge/archive/SKILL.md",
        root / "skills/knowledge/ingest/SKILL.md",
    ):
        if not integration_path.exists():
            errors.append(f"{integration_path}: missing Wiki writing integration")
        elif learning_context_uri not in integration_path.read_text(encoding="utf-8"):
            errors.append(
                f"{integration_path}: missing learning-context integration"
            )

    corpus_path = contract_targets.get("style_corpus")
    if corpus_path is not None:
        corpus = load_mapping(corpus_path)
        if corpus.get("version") != 2:
            errors.append(f"{corpus_path}: version must be 2")
        collections = corpus.get("collections")
        if not isinstance(collections, list) or len(collections) < 2:
            errors.append(f"{corpus_path}: requires two or more source collections")
        else:
            for position, collection in enumerate(collections, start=1):
                if not isinstance(collection, dict):
                    errors.append(f"{corpus_path}: collection {position} must be a mapping")
                    continue
                digest = collection.get("sha256")
                if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                    errors.append(f"{corpus_path}: collection {position} has invalid sha256")
                if not isinstance(collection.get("document_count"), int) or collection[
                    "document_count"
                ] < 1:
                    errors.append(
                        f"{corpus_path}: collection {position} has invalid document_count"
                    )
                if not isinstance(collection.get("page_count"), int) or collection[
                    "page_count"
                ] < 1:
                    errors.append(f"{corpus_path}: collection {position} has invalid page_count")
                if not isinstance(collection.get("role"), str) or not collection["role"].strip():
                    errors.append(f"{corpus_path}: collection {position} requires role")
        samples = corpus.get("samples")
        if not isinstance(samples, list) or len(samples) < 4:
            errors.append(f"{corpus_path}: requires four or more samples")
        else:
            seen_sample_ids: set[str] = set()
            for position, sample in enumerate(samples, start=1):
                if not isinstance(sample, dict):
                    errors.append(f"{corpus_path}: sample {position} must be a mapping")
                    continue
                sample_id = sample.get("id")
                digest = sample.get("sha256")
                pages = sample.get("reviewed_pages")
                role = sample.get("role")
                if (
                    not isinstance(sample_id, str)
                    or not sample_id
                    or sample_id in seen_sample_ids
                ):
                    errors.append(f"{corpus_path}: sample {position} has invalid id")
                else:
                    seen_sample_ids.add(sample_id)
                if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                    errors.append(f"{corpus_path}: sample {position} has invalid sha256")
                if (
                    not isinstance(pages, list)
                    or not pages
                    or any(not isinstance(page, int) or page < 1 for page in pages)
                ):
                    errors.append(f"{corpus_path}: sample {position} has invalid reviewed_pages")
                if not isinstance(role, str) or not role.strip():
                    errors.append(f"{corpus_path}: sample {position} requires role")
        if not non_empty_strings(corpus.get("observations")):
            errors.append(f"{corpus_path}: observations must not be empty")

    samples = quality.get("source_sampling")
    if not isinstance(samples, list) or len(samples) < 4:
        errors.append(f"{quality_path}: source_sampling requires four or more samples")
    else:
        for position, sample in enumerate(samples, start=1):
            if not isinstance(sample, dict) or not isinstance(
                sample.get("document"), str
            ):
                errors.append(f"{quality_path}: sample {position} requires document")
                continue
            pages = sample.get("pages")
            if (
                not isinstance(pages, list)
                or not pages
                or any(not isinstance(page, int) or page < 1 for page in pages)
            ):
                errors.append(f"{quality_path}: sample {position} has invalid pages")

    execution = quality.get("execution")
    if not isinstance(execution, dict):
        errors.append(f"{quality_path}: execution contract is missing")
    else:
        if execution.get("executors") != ["codex", "claude"]:
            errors.append(f"{quality_path}: executors must be codex then claude")
        if not isinstance(execution.get("trials"), int) or execution["trials"] < 3:
            errors.append(f"{quality_path}: trials must be at least 3")
        if execution.get("blind_compare") is not True:
            errors.append(f"{quality_path}: blind_compare must be true")
        if execution.get("held_out_required") is not True:
            errors.append(f"{quality_path}: held_out_required must be true")

    rubric = quality.get("rubric")
    if (
        not isinstance(rubric, dict)
        or not rubric
        or any(not isinstance(score, int) or score < 1 for score in rubric.values())
    ):
        errors.append(f"{quality_path}: rubric requires positive integer weights")
        rubric_names: set[str] = set()
        maximum = 0
    else:
        rubric_names = {name for name in rubric if isinstance(name, str)}
        maximum = sum(rubric.values())
    minimum = quality.get("minimum_score")
    if not isinstance(minimum, int) or minimum < 1 or minimum > maximum:
        errors.append(f"{quality_path}: minimum_score exceeds rubric bounds")

    hard_fail_value = quality.get("hard_fail")
    if not non_empty_strings(hard_fail_value):
        errors.append(f"{quality_path}: hard_fail requires non-empty identifiers")
        hard_fails: set[str] = set()
    else:
        hard_fails = set(hard_fail_value)
        if len(hard_fails) != len(hard_fail_value):
            errors.append(f"{quality_path}: hard_fail identifiers must be unique")

    cases = quality.get("cases")
    if not isinstance(cases, list) or len(cases) < 8:
        errors.append(f"{quality_path}: quality cases require eight or more cases")
    else:
        seen: set[str] = set()
        for position, case in enumerate(cases, start=1):
            if not isinstance(case, dict):
                errors.append(f"{quality_path}: case {position} must be a mapping")
                continue
            identifier = case.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in seen:
                errors.append(
                    f"{quality_path}: case {position} has invalid or duplicate id"
                )
            else:
                seen.add(identifier)
            required = case.get("require")
            if not non_empty_strings(required) or not set(required).issubset(
                rubric_names
            ):
                errors.append(
                    f"{quality_path}: case {position} has unknown rubric requirement"
                )
            forbidden = case.get("forbid", [])
            if forbidden and (
                not non_empty_strings(forbidden)
                or not set(forbidden).issubset(hard_fails)
            ):
                errors.append(
                    f"{quality_path}: case {position} has unknown hard-fail rule"
                )

    behavior = load_mapping(behavior_path)
    if behavior.get("version") != 1 or behavior.get("profile") != "publishing":
        errors.append(f"{behavior_path}: requires version 1 and publishing profile")
    behavior_cases = behavior.get("cases")
    if not isinstance(behavior_cases, list) or len(behavior_cases) < 8:
        errors.append(f"{behavior_path}: behavior cases require eight or more cases")
    else:
        seen = set()
        for position, case in enumerate(behavior_cases, start=1):
            if not isinstance(case, dict):
                errors.append(f"{behavior_path}: case {position} must be a mapping")
                continue
            identifier = case.get("id")
            required = case.get("require")
            forbidden = case.get("forbid")
            if not isinstance(identifier, str) or not identifier or identifier in seen:
                errors.append(
                    f"{behavior_path}: case {position} has invalid or duplicate id"
                )
            else:
                seen.add(identifier)
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                errors.append(f"{behavior_path}: case {position} requires prompt")
            if not non_empty_strings(required) or not non_empty_strings(forbidden):
                errors.append(
                    f"{behavior_path}: case {position} requires require and forbid"
                )
            elif set(required).intersection(forbidden):
                errors.append(
                    f"{behavior_path}: case {position} overlaps require and forbid"
                )
        required_behavior_cases = {
            "archive-envelope-stays-owned",
            "fixed-template-is-not-quality",
            "record-preserves-provenance-and-uncertainty",
            "decision-keeps-reversal-condition",
            "record-route-never-invents-execution",
            "general-diagram-keeps-stable-entities",
            "book-source-phase-does-not-invent-learning-workflow",
        }
        missing_behavior_cases = required_behavior_cases - seen
        if missing_behavior_cases:
            errors.append(
                f"{behavior_path}: missing required cases "
                + ", ".join(sorted(missing_behavior_cases))
            )

    result_path = result_paths[-1]
    result = load_mapping(result_path)
    if result.get("version") != 1 or result.get("held_out_case") != "exception-flow":
        errors.append(
            f"{result_path}: requires version 1 and exception-flow held-out case"
        )
    scoring = result.get("scoring")
    maximum = scoring.get("maximum") if isinstance(scoring, dict) else None
    expected_maximum = sum(rubric.values()) if isinstance(rubric, dict) else 18
    if maximum != expected_maximum:
        errors.append(f"{result_path}: scoring maximum must match the quality rubric")
    executors = result.get("executors")
    if not isinstance(executors, dict) or set(executors) != {"codex", "claude"}:
        errors.append(f"{result_path}: requires codex and claude results")
    else:
        for executor_name in ("codex", "claude"):
            executor = executors.get(executor_name)
            candidate = (
                executor.get("candidate") if isinstance(executor, dict) else None
            )
            if not isinstance(candidate, dict):
                errors.append(f"{result_path}: {executor_name} candidate is missing")
                continue
            trials = candidate.get("trials")
            scores = candidate.get("scores")
            if (
                not isinstance(trials, int)
                or trials < 3
                or candidate.get("passed") != trials
                or not isinstance(scores, list)
                or len(scores) != trials
                or any(score != maximum for score in scores)
            ):
                errors.append(
                    f"{result_path}: {executor_name} candidate requires three full-score passes"
                )
    hardening = result.get("usability_hardening")
    if not isinstance(hardening, dict):
        errors.append(f"{result_path}: usability hardening evidence is missing")
    else:
        status = hardening.get("status")
        codex_hardening = hardening.get("codex")
        claude_hardening = hardening.get("claude")
        if not isinstance(codex_hardening, dict) or (
            codex_hardening.get("trials") != 3
            or codex_hardening.get("passed") != 3
            or codex_hardening.get("scores") != [maximum, maximum, maximum]
        ):
            errors.append(f"{result_path}: hardening Codex requires three full passes")
        if not isinstance(claude_hardening, dict):
            errors.append(f"{result_path}: hardening Claude evidence is missing")
        else:
            requested = claude_hardening.get("requested_trials")
            completed = claude_hardening.get("completed_trials")
            passed = claude_hardening.get("passed")
            scores = claude_hardening.get("scores")
            valid_completed = (
                requested == 3
                and isinstance(completed, int)
                and 1 <= completed <= requested
                and passed == completed
                and isinstance(scores, list)
                and len(scores) == completed
                and all(score == maximum for score in scores)
            )
            if not valid_completed:
                errors.append(
                    f"{result_path}: hardening Claude evidence is inconsistent"
                )
            elif status == "complete" and completed != requested:
                errors.append(
                    f"{result_path}: completed hardening requires three Claude passes"
                )
            elif status == "blocked_by_external_rate_limit":
                if claude_hardening.get(
                    "blocked_trials"
                ) != requested - completed or not isinstance(
                    claude_hardening.get("reset_at"), str
                ):
                    errors.append(
                        f"{result_path}: blocked hardening requires reset evidence"
                    )
            elif status != "complete":
                errors.append(f"{result_path}: unknown usability hardening status")
    optimization = result.get("context_optimization")
    rejected = optimization.get("rejected") if isinstance(optimization, dict) else None
    if not isinstance(rejected, list) or len(rejected) < 2:
        errors.append(
            f"{result_path}: context optimization requires rejected reductions"
        )
    routing = result.get("routing")
    if (
        not isinstance(routing, dict)
        or routing.get("cases", 0) < 61
        or routing.get("repeat", 0) < 3
    ):
        errors.append(f"{result_path}: routing requires all cases repeated three times")
    else:
        for executor_name in ("codex", "claude"):
            executor = routing.get(executor_name)
            if (
                not isinstance(executor, dict)
                or executor.get("primary_recall", 0) < 0.95
                or executor.get("forbidden_selections") != 0
                or executor.get("agreement", 0) < 0.90
            ):
                errors.append(
                    f"{result_path}: {executor_name} routing threshold failed"
                )
    limitations = result.get("limitations")
    if not non_empty_strings(limitations):
        errors.append(f"{result_path}: limitations must be recorded")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = audit_learning_content(root)
    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1
    print("learning-content quality=ok behavior=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
