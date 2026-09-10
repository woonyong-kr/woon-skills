#!/usr/bin/env python3
"""Read-only Korean prose review hints; never rewrite or classify authorship.

Pattern ideas adapted from hjongc/humanizer-kr (MIT); see ../LICENSE.
Markdown masking is conservative. A person must review meaning and false positives.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PATTERNS = {
    "translationese-connectors": r"또한|더 나아가|이를 통해|궁극적으로|전반적으로|이러한 점에서",
    "inflated-praise": r"혁신적인|획기적인|차별화된|탁월한|완벽한|압도적인|차원이 다른",
    "nominalization": r"측면에서|기반으로|중심으로|(?:효율성|생산성|편의성) 향상을 위한|것입니다",
    "passive-chain": r"제공됩니다|진행됩니다|확인됩니다|구성됩니다|처리됩니다",
    "vague-authority": r"많은 전문가|업계에서는|여러 연구에 따르면|대부분의 사람들은|일각에서는",
    "chatbot-artifact": r"물론입니다|좋은 질문입니다|아래와 같이 정리|도움이 되었으면|정확히 보셨습니다",
    "honorific-padding": r"사용자님께서는|확인하시어|참고 부탁드립니다|진행 부탁드립니다|이용에 참고하여 주시기 바랍니다",
    "generic-positive-conclusion": r"앞으로의 행보가 기대|더 나은 미래를 만들어|지속적인 성장이 기대|좋은 결과를 기대할 수",
    "hedging-stack": r"할 수 있을 것으로 (?:보|예상)|영향을 줄 수 있을 것으로",
    "heading-warmup": r"살펴보겠습니다|알아보겠습니다|다음과 같습니다",
    "bold-label-list": r"(?m)^\s*[-*]\s+\*\*[^*\n]{1,30}[:：]\*\*",
    "fake-candid-opener": r"솔직히 말하면|한마디로 말하면|정리하자면",
    "change-anchored-doc": r"새롭게 추가된|개선되었습니다|변경되었습니다|추가되었습니다",
    "weak-reader-action": r"필요한 조치를 진행|이용에 참고",
}


def blank(text: str) -> str:
    """Preserve offsets and line numbers while hiding protected spans."""
    return re.sub(r"[^\n\r]", " ", text)


def prose_only(text: str) -> str:
    lines = text.splitlines(keepends=True)
    masked: list[str] = []
    frontmatter = bool(lines and lines[0].strip() == "---")
    fence: str | None = None
    math_end: str | None = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if frontmatter:
            masked.append(blank(line))
            if index and stripped in {"---", "..."}:
                frontmatter = False
        elif fence:
            masked.append(blank(line))
            if re.fullmatch(r"\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                fence = None
        elif marker:
            fence = marker.group(1)
            masked.append(blank(line))
        elif math_end:
            masked.append(blank(line))
            if math_end in line:
                math_end = None
        elif stripped.startswith(("$$", r"\[")):
            start, end = ("$$", "$$") if stripped.startswith("$$") else (r"\[", r"\]")
            math_end = None if end in stripped[len(start):] else end
            masked.append(blank(line))
        elif re.match(r"^\s*>|^(?: {4}|\t)|^\s{0,3}\[[^]]+\]:", line):
            masked.append(blank(line))
        else:
            masked.append(line)
    prose = "".join(masked)
    for pattern in (
        r"<!--[\s\S]*?(?:-->|\Z)",
        r"(?<!`)(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)",
        r"(?<!\\)\$[^$\n]+(?<!\\)\$",
        r"\\\([\s\S]*?\\\)",
        r"!?\[\[[^\]\n]+\]\]",
        r"!\[[^\]\n]*\]\([^\n]*?\)",
        r"<https?://[^>\n]+>|https?://[^\s<>]+",
    ):
        prose = re.sub(pattern, lambda match: blank(match.group()), prose)
    # Keep ordinary link labels visible, but do not inspect destinations.
    prose = re.sub(r"(\[[^\]\n]*\])\([^\n]*?\)", lambda match: match.group(1) + blank(match.group()[len(match.group(1)):]), prose)
    return prose


def audit(text: str) -> list[dict[str, str | int]]:
    prose = prose_only(text)
    findings: list[dict[str, str | int]] = []
    for code, pattern in PATTERNS.items():
        for match in re.finditer(pattern, prose):
            findings.append({"code": code, "line": prose.count("\n", 0, match.start()) + 1, "match": match.group()})
    return sorted(findings, key=lambda item: (int(item["line"]), str(item["code"])))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="UTF-8 files; omit to read stdin")
    parser.add_argument("--json", action="store_true", help="Print review candidates as JSON")
    args = parser.parse_args()
    try:
        inputs = [(str(path), path.read_text(encoding="utf-8")) for path in args.paths] if args.paths else [("stdin", sys.stdin.read())]
    except (OSError, UnicodeError) as error:
        parser.exit(2, f"Cannot read input: {error}\n")
    results = [{"path": path, "findings": audit(text)} for path, text in inputs]
    if args.json:
        print(json.dumps({"advisory_only": True, "files": results}, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result['path']}: {len(result['findings'])} review candidates")
            for finding in result["findings"]:
                print(f"  {finding['line']}: [{finding['code']}] {finding['match']}")
        print("검토 후보이며 자동 판정이 아닙니다. 의미와 문맥을 직접 확인하세요.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
