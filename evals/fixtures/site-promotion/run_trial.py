#!/usr/bin/env python3
"""Run one fresh Codex site-promotion baseline or candidate trial."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

from score_artifact import score


def candidate_context(root: Path) -> str:
    paths = (
        root / "skills/writing/site-promotion/SKILL.md",
        root / "skills/writing/site-promotion/references/promotion-contract.md",
        root / "skills/writing/site-promotion/references/blog-contract.md",
        root / "skills/writing/site-promotion/references/portfolio-contract.md",
    )
    blocks = [
        f'<canonical-instruction source="{path.relative_to(root).as_posix()}">\n'
        f"{path.read_text(encoding='utf-8')}\n"
        "</canonical-instruction>"
        for path in paths
    ]
    return (
        "다음 canonical instruction을 적용하되 지시 원문을 산출물에 복사하지 마세요. "
        "도구를 사용하거나 파일을 수정하지 말고 이번 응답에 완성된 후보만 반환하세요.\n\n"
        + "\n\n".join(blocks)
    )


def parse_usage(raw: str) -> dict[str, int]:
    usage: dict[str, int] = {}
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed" and isinstance(
            event.get("usage"), dict
        ):
            usage = {
                key: int(value)
                for key, value in event["usage"].items()
                if isinstance(value, int)
            }
    return usage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("baseline", "candidate"), required=True)
    parser.add_argument("--trial", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[3]
    request = Path(__file__).with_name("held-out.md").read_text(encoding="utf-8")
    prompt = request
    if args.variant == "candidate":
        prompt = f"{candidate_context(root)}\n\n<request>\n{request}\n</request>"

    args.output.mkdir(parents=True, exist_ok=True)
    artifact = args.output / f"{args.variant}-{args.trial}.md"
    raw_path = args.output / f"{args.variant}-{args.trial}.jsonl"
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--ignore-rules",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        "--color",
        "never",
        "--json",
        "--output-last-message",
        str(artifact),
        "-C",
        str(args.output),
    ]
    if args.model:
        command.extend(["--model", args.model])
    command.append("-")
    started = time.monotonic()
    completed = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        check=False,
        timeout=300,
    )
    duration = round(time.monotonic() - started, 3)
    raw_path.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0 or not artifact.exists():
        print(
            json.dumps(
                {
                    "variant": args.variant,
                    "trial": args.trial,
                    "returncode": completed.returncode,
                    "duration_seconds": duration,
                    "error": completed.stderr.strip().splitlines()[-8:],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    quality = score(artifact.read_text(encoding="utf-8"))
    result = {
        "variant": args.variant,
        "trial": args.trial,
        "model": args.model or "executor-default-unverified",
        "returncode": completed.returncode,
        "duration_seconds": duration,
        "usage": parse_usage(completed.stdout),
        "artifact_bytes": artifact.stat().st_size,
        "quality": quality,
    }
    (args.output / f"{args.variant}-{args.trial}-score.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
