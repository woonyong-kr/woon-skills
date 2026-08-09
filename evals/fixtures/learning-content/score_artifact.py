#!/usr/bin/env python3
"""Score one learning Markdown artifact with deterministic executable checks."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

VERIFY_PATH = Path(__file__).with_name("verify.py")
VERIFY_SPEC = importlib.util.spec_from_file_location(
    "learning_content_verify_shared", VERIFY_PATH
)
assert VERIFY_SPEC is not None and VERIFY_SPEC.loader is not None
VERIFY_MODULE = importlib.util.module_from_spec(VERIFY_SPEC)
sys.modules[VERIFY_SPEC.name] = VERIFY_MODULE
VERIFY_SPEC.loader.exec_module(VERIFY_MODULE)
FORBIDDEN_MERMAID = VERIFY_MODULE.FORBIDDEN_MERMAID
HEADING = VERIFY_MODULE.HEADING
NUMBERED_ARROW = VERIFY_MODULE.NUMBERED_ARROW
fenced_blocks = VERIFY_MODULE.fenced_blocks
DIAGRAM_VERIFIER = (
    Path(__file__).resolve().parents[3]
    / "skills/docs/diagram/scripts/verify-mermaid.sh"
)
GRADER_VERSION = "deterministic-v5"

WEIGHTS = {
    "problem_before_definition": 2,
    "runnable_example_and_output": 2,
    "causal_walkthrough": 2,
    "terminology_and_boundaries": 2,
    "concept_grounding_and_order": 2,
    "source_matched_identifiers": 2,
    "diagram_question_and_numbered_flow": 2,
    "readability_and_theme": 2,
    "practice_or_counterexample": 1,
    "concise_summary": 1,
}


def concept_mentions(markdown: str, concept_term: str) -> list[re.Match[str]]:
    if concept_term == "검사 예외":
        pattern = r"검사 예외|checked exception"
    elif concept_term == "예외 전파":
        pattern = (
            r"예외\s*전파|예외(?:가|는|를|의)?[^\n.!?]{0,40}"
            r"(?:전파|전달|호출한 쪽으로[^\n.!?]{0,20}올라)"
        )
    else:
        pattern = re.escape(concept_term)
    return list(re.finditer(pattern, markdown, re.IGNORECASE))


def is_console_command_block(language: str, body: str) -> bool:
    if language != "console":
        return False
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    command = re.compile(
        r"^(?:\$\s*)?(?:javac|java|mvn|gradle|\./gradlew|python\d*|node|npm|pnpm|yarn|cargo|go|dotnet)\b"
    )
    return bool(lines) and all(command.search(line) for line in lines)


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)


def outputs_after_first_java(markdown: str) -> tuple[str, int, bool]:
    pairs = java_output_pairs(markdown)
    if not pairs:
        return "", -1, False
    _, output, position, evidence_before = pairs[0]
    return output, position, evidence_before


def java_output_pairs(markdown: str) -> list[tuple[str, str, int, bool]]:
    blocks = list(VERIFY_MODULE.FENCE.finditer(markdown))
    pairs: list[tuple[str, str, int, bool]] = []
    for java_index, java_block in enumerate(blocks):
        if java_block.group("language") != "java":
            continue
        output_blocks = []
        for block in blocks[java_index + 1 :]:
            if block.group("language") in {"java", "mermaid"}:
                break
            if block.group("language") in {
                "text",
                "console",
            } and not is_console_command_block(
                block.group("language"), block.group("body")
            ):
                output_blocks.append(block)
        if not output_blocks:
            continue
        evidence_before = True
        previous_end = java_block.end()
        for output_block in output_blocks:
            evidence_region = markdown[previous_end : output_block.start()]
            evidence_before = evidence_before and (
                re.search(
                    r"실제(?:로|\s+compile|\s+컴파일|\s+실행|\s*·|[^.\n]{0,60}(?:컴파일|compile|실행|결과|확인))|직접|검증한 결과|실행 결과|예상(?:한|되는|\s+실행|\s*값|\s+결과)|결과를 예상|미실행",
                    evidence_region,
                )
                is not None
            )
            previous_end = output_block.end()
        pairs.append(
            (
                java_block.group("body"),
                "\n".join(block.group("body") for block in output_blocks),
                output_blocks[0].start(),
                evidence_before,
            )
        )
    return pairs


def diagram_snapshot_mismatches(markdown: str) -> list[str]:
    latest_java = ""
    mismatches: list[str] = []
    for block in VERIFY_MODULE.FENCE.finditer(markdown):
        language = block.group("language")
        body = block.group("body")
        if language == "java":
            latest_java = body
            continue
        if language != "mermaid":
            continue
        if re.search(r"\bcatch\s*\(", body) and not re.search(
            r"\bcatch\s*\(", latest_java
        ):
            mismatches.append("diagram introduces catch absent from preceding Java")
        if re.search(r"\bthrow\b", body) and not re.search(r"\bthrow\b", latest_java):
            mismatches.append("diagram introduces throw absent from preceding Java")
    return mismatches


def score_artifact(
    markdown: str,
    identifiers: tuple[str, ...],
    concept_term: str,
) -> dict[str, object]:
    scores = {name: 0 for name in WEIGHTS}
    evidence: dict[str, object] = {}
    hard_fail: list[str] = []
    headings = [
        (len(match.group("marks")), match.group("title"))
        for match in HEADING.finditer(markdown)
    ]
    first_h2 = next((title for level, title in headings if level == 2), "")
    first_fifth = markdown[: max(1, len(markdown) // 5)]
    prose_lines = [
        line
        for line in markdown.splitlines()[1:]
        if line and not line.startswith(("#", "```"))
    ]
    first_paragraph = prose_lines[0] if prose_lines else ""
    early_observable_failure = (
        re.search(r"실패|오류|예외|종료|출력|전파|바뀌|예상과 달리", first_paragraph)
        is not None
        and "```java" in first_fifth
    )
    if (
        re.search(r"문제|실행|동작|결과|예외|변경|실패|오류|확인", first_h2)
        or early_observable_failure
    ):
        scores["problem_before_definition"] = 2

    java_blocks = fenced_blocks(markdown, "java")
    output_pairs = java_output_pairs(markdown)
    documented_output, output_position, output_evidence_before = (
        (output_pairs[0][1], output_pairs[0][2], all(pair[3] for pair in output_pairs))
        if output_pairs
        else ("", -1, False)
    )
    if java_blocks and not output_pairs:
        hard_fail.append("missing_typed_output_evidence")
    elif output_pairs and not output_evidence_before:
        hard_fail.append("output_evidence_state_not_before_result")
    compile_ok = False
    run_returncode: int | None = None
    output_matches = False
    compile_detail = "missing Java block"
    executed_java_block: int | None = None
    with tempfile.TemporaryDirectory(prefix="woon-learning-score-") as temporary:
        work = Path(temporary)
        for pair_index, (executable_java, pair_output, _, _) in enumerate(
            output_pairs, start=1
        ):
            class_match = re.search(
                r"public\s+class\s+([A-Za-z_$][\w$]*)", executable_java
            ) or re.search(
                r"class\s+([A-Za-z_$][\w$]*)[^{}]*\{\s*public\s+static\s+void\s+main",
                executable_java,
                re.DOTALL,
            )
            if class_match is not None:
                class_name = class_match.group(1)
                pair_work = work / f"pair-{pair_index}"
                pair_work.mkdir()
                source = pair_work / f"{class_name}.java"
                source.write_text(executable_java + "\n", encoding="utf-8")
                compiled = run(["javac", "-encoding", "UTF-8", source.name], pair_work)
                compile_ok = compiled.returncode == 0
                compile_detail = compiled.stderr.strip()
                if compile_ok:
                    executed = run(
                        ["java", "-cp", str(pair_work), class_name], pair_work
                    )
                    run_returncode = executed.returncode
                    compile_detail = executed.stderr.strip()
                    observed_output = (executed.stdout + executed.stderr).strip()
                    output_matches = observed_output == pair_output.strip()
                    if output_matches:
                        executed_java_block = pair_index
                        break
        if compile_ok and output_matches:
            scores["runnable_example_and_output"] = 2
        elif compile_ok and output_pairs:
            hard_fail.append("invented_execution_result")

        diagrams = fenced_blocks(markdown, "mermaid")
        rendered = bool(diagrams)
        for position, diagram in enumerate(diagrams, start=1):
            source = work / f"diagram-{position}.mmd"
            source.write_text(diagram + "\n", encoding="utf-8")
            output_dir = work / "rendered"
            completed = run([str(DIAGRAM_VERIFIER), str(source), str(output_dir)], work)
            default_output = output_dir / f"diagram-{position}-default.svg"
            dark_output = output_dir / f"diagram-{position}-dark.svg"
            rendered = (
                rendered
                and completed.returncode == 0
                and default_output.exists()
                and default_output.stat().st_size > 0
                and dark_output.exists()
                and dark_output.stat().st_size > 0
            )

    diagrams = fenced_blocks(markdown, "mermaid")
    combined_diagrams = "\n".join(diagrams)
    snapshot_mismatches = diagram_snapshot_mismatches(markdown)
    if snapshot_mismatches:
        hard_fail.append("code_diagram_snapshot_mismatch")
    arrow_count = len(NUMBERED_ARROW.findall(combined_diagrams))
    numbered_explanations = len(
        re.findall(r"^\s*(?:\d+\.\s+|[-*]\s+[①-⑳])", markdown, re.MULTILINE)
    )
    if arrow_count >= 3 and numbered_explanations >= 3:
        scores["causal_walkthrough"] = 2

    boundary_heading = any(
        level == 2 and re.search(r"경계|한계|주의|어디에서.+처리|처리해야", title)
        for level, title in headings
    )
    mentions = concept_mentions(markdown, concept_term)
    if boundary_heading and mentions:
        scores["terminology_and_boundaries"] = 2

    concept_positions = [
        match.start() for match in mentions if match.start() > output_position
    ]
    concept_position = min(concept_positions) if concept_positions else -1
    if output_position >= 0 and concept_position > output_position:
        scores["concept_grounding_and_order"] = 2

    missing_code = [
        identifier
        for identifier in identifiers
        if identifier not in "\n".join(java_blocks)
    ]
    missing_diagram = [
        identifier for identifier in identifiers if identifier not in combined_diagrams
    ]
    if not missing_code and not missing_diagram:
        scores["source_matched_identifiers"] = 2
    else:
        hard_fail.append("code_diagram_identifier_mismatch")

    question_before_diagram = True
    for match in re.finditer(r"```mermaid", markdown):
        context = markdown[max(0, match.start() - 400) : match.start()]
        explicit_question = (
            "?" in context
            or "답합니다" in context
            or re.search(
                r"다음 그림은[^.\n]*(?:어디|왜|어떻게)[^.\n]*(?:보여|설명)",
                context,
            )
            is not None
        )
        question_before_diagram = question_before_diagram and explicit_question
    if diagrams and question_before_diagram and arrow_count >= 3:
        scores["diagram_question_and_numbered_flow"] = 2

    heading_valid = (
        bool(headings)
        and headings[0][0] == 1
        and sum(1 for level, _ in headings if level == 1) == 1
    )
    heading_valid = heading_valid and all(
        following[0] <= current[0] + 1
        for current, following in zip(headings, headings[1:])
    )
    if heading_valid and rendered:
        scores["readability_and_theme"] = 2

    if any(re.search(r"연습|확인할 문제|반례", title) for _, title in headings):
        scores["practice_or_counterexample"] = 1
    if any(re.search(r"정리|요약", title) for _, title in headings):
        scores["concise_summary"] = 1

    if any(FORBIDDEN_MERMAID.search(diagram) for diagram in diagrams):
        hard_fail.append("diagram_meaning_depends_only_on_color")
    if re.search(
        r"!\[[^]]*\]\([^)]*\.(?:png|jpe?g|webp)(?:\?[^)]*)?\)", markdown, re.IGNORECASE
    ):
        hard_fail.append("decorative_ai_image_used_for_code_or_memory_flow")

    total = sum(scores.values())
    evidence.update(
        {
            "compile_ok": compile_ok,
            "run_returncode": run_returncode,
            "output_matches": output_matches,
            "output_evidence_before": output_evidence_before,
            "java_output_pairs": len(output_pairs),
            "executed_java_block": executed_java_block,
            "compile_detail": compile_detail,
            "mermaid_blocks": len(diagrams),
            "numbered_arrows": arrow_count,
            "themes_rendered": rendered,
            "missing_code_identifiers": missing_code,
            "missing_diagram_identifiers": missing_diagram,
            "diagram_snapshot_mismatches": snapshot_mismatches,
        }
    )
    unique_hard_fail = sorted(set(hard_fail))
    return {
        "grader_version": GRADER_VERSION,
        "score": total,
        "maximum": sum(WEIGHTS.values()),
        "passed": total >= 15 and not unique_hard_fail,
        "scores": scores,
        "hard_fail": unique_hard_fail,
        "evidence": evidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--identifier", action="append", required=True)
    parser.add_argument("--concept-term", required=True)
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()
    result = score_artifact(
        args.artifact.read_text(encoding="utf-8"),
        tuple(args.identifier),
        args.concept_term,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.require_pass and not result["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
