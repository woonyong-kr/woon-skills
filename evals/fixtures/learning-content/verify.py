#!/usr/bin/env python3
"""Validate the executable learning-content fixture and extract Mermaid blocks."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

FENCE = re.compile(r"```(?P<language>[a-zA-Z0-9_-]+)\n(?P<body>.*?)\n```", re.DOTALL)
HEADING = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+)$", re.MULTILINE)
FORBIDDEN_MERMAID = re.compile(r"\b(style|classDef|themeVariables)\b|#[0-9a-fA-F]{3,8}")
NUMBERED_ARROW = re.compile(
    r"(?:->>|-->>|-->|-\.->|--x|-x).*?(?:\b\d+(?:[:.)]|(?=\s|[\"'|]))|[①-⑳])"
)


def fenced_blocks(markdown: str, language: str) -> list[str]:
    return [
        match.group("body")
        for match in FENCE.finditer(markdown)
        if match.group("language") == language
    ]


def validate_obsidian_index(markdown: str) -> list[str]:
    errors: list[str] = []
    headings = [
        (len(match.group("marks")), match.group("title"))
        for match in HEADING.finditer(markdown)
    ]
    if headings != [(1, "학습 문서 검증")]:
        errors.append("Obsidian index requires exactly one canonical H1")
    if markdown.startswith("---\n"):
        errors.append(
            "standalone Obsidian index must not duplicate archive frontmatter"
        )
    if "> [!note]" not in markdown:
        errors.append("Obsidian index requires a note callout")
    if "[[immutable-address|불변 주소 학습 문서 열기]]" not in markdown:
        errors.append("Obsidian index requires the canonical aliased wikilink")
    return errors


def validate_markdown(markdown: str, source: str, actual_output: str) -> list[str]:
    errors: list[str] = []
    headings = [
        (len(match.group("marks")), match.group("title"))
        for match in HEADING.finditer(markdown)
    ]
    if not headings or headings[0][0] != 1:
        errors.append("standalone fixture requires one leading H1")
    if sum(1 for level, _ in headings if level == 1) != 1:
        errors.append("standalone fixture requires exactly one H1")
    for current, following in zip(headings, headings[1:]):
        if following[0] > current[0] + 1:
            errors.append("heading levels must not be skipped")

    first_paragraph = next(
        (
            line
            for line in markdown.splitlines()[1:]
            if line and not line.startswith("#")
        ),
        "",
    )
    observes_unintended_change = re.search(
        r"둘 다 .+바뀝니다", first_paragraph
    ) is not None or ("회원 A" in first_paragraph and "바뀝니다" in first_paragraph)
    if not observes_unintended_change:
        errors.append("first paragraph must state the observable failure")

    java_blocks = fenced_blocks(markdown, "java")
    if java_blocks != [source.rstrip()]:
        errors.append("Java block must exactly match AddressLesson.java")

    text_blocks = fenced_blocks(markdown, "text")
    if text_blocks != [actual_output.rstrip()]:
        errors.append("documented output must exactly match the Java execution")

    diagrams = fenced_blocks(markdown, "mermaid")
    if len(diagrams) != 2:
        errors.append("fixture requires exactly two focused Mermaid diagrams")
    required_identifiers = {
        "memberA",
        "memberB",
        "sharedAddress",
        "addressA",
        "addressB",
        "moveTo",
    }
    combined = "\n".join(diagrams)
    missing = sorted(
        identifier for identifier in required_identifiers if identifier not in combined
    )
    if missing:
        errors.append(f"Mermaid is missing source identifiers: {', '.join(missing)}")
    for position, diagram in enumerate(diagrams, start=1):
        if FORBIDDEN_MERMAID.search(diagram):
            errors.append(f"Mermaid {position} hard-codes color or style")
        if len(NUMBERED_ARROW.findall(diagram)) < 3:
            errors.append(f"Mermaid {position} requires at least three numbered arrows")

    if markdown.index("공유 참조라고 합니다") < markdown.index("실제 실행 결과"):
        errors.append("shared-reference term must follow the observed result")
    if markdown.index("불변 객체라고 합니다") < markdown.index(
        "왜 회원 A까지 바뀌는가"
    ):
        errors.append("immutable-object term must follow the causal explanation")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("actual_output", type=Path)
    parser.add_argument("mermaid_output", type=Path)
    args = parser.parse_args()

    markdown_path = args.fixture / "immutable-address.md"
    obsidian_index_path = args.fixture / "obsidian-index.md"
    source_path = args.fixture / "AddressLesson.java"
    markdown = markdown_path.read_text(encoding="utf-8")
    source = source_path.read_text(encoding="utf-8")
    actual_output = args.actual_output.read_text(encoding="utf-8")
    errors = validate_markdown(markdown, source, actual_output)
    errors.extend(
        validate_obsidian_index(obsidian_index_path.read_text(encoding="utf-8"))
    )
    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1

    args.mermaid_output.mkdir(parents=True, exist_ok=True)
    for position, diagram in enumerate(fenced_blocks(markdown, "mermaid"), start=1):
        (args.mermaid_output / f"diagram-{position}.mmd").write_text(
            diagram + "\n", encoding="utf-8"
        )
    print("learning document: headings, code, output and Mermaid semantics passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
