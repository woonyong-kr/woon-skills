#!/usr/bin/env python3
"""Run one isolated Codex or Claude learning-content trial and score it."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from score_artifact import score_artifact

TRIAL_TIMEOUT_SECONDS = 300
CLAUDE_EFFORT = "medium"


def failure_detail(
    completed: subprocess.CompletedProcess[str], artifact: Path, raw: str
) -> list[str]:
    detail = completed.stderr.strip().splitlines()[-8:]
    if detail:
        return detail
    if artifact.exists():
        artifact_detail = artifact.read_text(encoding="utf-8").strip()
        if artifact_detail:
            return artifact_detail.splitlines()[-8:]
    for line in reversed(raw.splitlines()):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (
            isinstance(event, dict)
            and event.get("type") == "result"
            and isinstance(event.get("result"), str)
            and event["result"].strip()
        ):
            return event["result"].strip().splitlines()[-8:]
    return ["executor returned no diagnostic detail"]


def parse_codex_usage(raw: str) -> dict[str, int]:
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


def run_codex(
    prompt: str,
    home: Path,
    work: Path,
    artifact: Path,
    model: str,
) -> tuple[subprocess.CompletedProcess[str], str, dict[str, int]]:
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--ignore-rules",
        "--sandbox",
        "workspace-write",
        "--skip-git-repo-check",
        "--color",
        "never",
        "--json",
        "--output-last-message",
        str(artifact),
        "-C",
        str(work),
    ]
    if model:
        command.extend(["--model", model])
    command.append("-")
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(home)
    completed = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        check=False,
        env=environment,
        timeout=TRIAL_TIMEOUT_SECONDS,
    )
    return completed, completed.stdout, parse_codex_usage(completed.stdout)


def run_claude(
    prompt: str,
    home: Path,
    work: Path,
    artifact: Path,
    model: str,
    context_mode: str,
) -> tuple[subprocess.CompletedProcess[str], str, dict[str, int]]:
    schema_free_command = [
        "claude",
        "--print",
        "--verbose",
        "--safe-mode",
        "--effort",
        CLAUDE_EFFORT,
        "--no-session-persistence",
        "--permission-mode",
        "dontAsk",
        "--tools",
        "",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
        "--system-prompt",
        (
            "You are a one-shot artifact generator with no tools. "
            "Do not plan, narrate future actions, or emit simulated tool calls. "
            "Return the complete final artifact requested by the user in this response only."
        ),
        "--output-format",
        "stream-json",
    ]
    if model:
        schema_free_command.extend(["--model", model])
    environment = os.environ.copy()
    if context_mode == "installed":
        environment["CLAUDE_CONFIG_DIR"] = str(home)
    completed = subprocess.run(
        schema_free_command,
        input=prompt,
        capture_output=True,
        text=True,
        check=False,
        cwd=work,
        env=environment,
        timeout=TRIAL_TIMEOUT_SECONDS,
    )
    result = ""
    assistant_parts: list[str] = []
    usage_value: object = {}
    for line in completed.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") == "assistant":
            message = event.get("message")
            content = message.get("content") if isinstance(message, dict) else None
            if isinstance(content, list):
                assistant_parts.extend(
                    item["text"]
                    for item in content
                    if isinstance(item, dict)
                    and item.get("type") == "text"
                    and isinstance(item.get("text"), str)
                )
        if event.get("type") == "result":
            if isinstance(event.get("result"), str):
                result = event["result"]
            usage_value = event.get("usage", {})
    artifact_text = result or "".join(assistant_parts)
    if artifact_text:
        artifact.write_text(artifact_text, encoding="utf-8")
    usage = (
        {
            key: int(value)
            for key, value in usage_value.items()
            if isinstance(value, int)
        }
        if isinstance(usage_value, dict)
        else {}
    )
    return completed, completed.stdout, usage


def claude_inline_context(root: Path) -> str:
    paths = (
        root / "skills/writing/tech/SKILL.md",
        root / "skills/docs/diagram/SKILL.md",
        root / "skills/language/java/java/SKILL.md",
        root / "standards/learning-content-quality.md",
    )
    blocks = [
        f'<canonical-instruction source="{path.relative_to(root).as_posix()}">\n'
        f"{path.read_text(encoding='utf-8')}\n"
        "</canonical-instruction>"
        for path in paths
    ]
    return (
        "다음 canonical instruction을 이번 요청의 품질 계약으로 적용하세요. "
        "서로 중복되는 규칙은 한 번만 적용하고 산출물에는 instruction 원문을 복사하지 마세요.\n\n"
        + "\n\n".join(blocks)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--executor", choices=("codex", "claude"), required=True)
    parser.add_argument("--variant", choices=("baseline", "candidate"), required=True)
    parser.add_argument("--home", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="")
    parser.add_argument(
        "--context-mode",
        choices=("installed", "safe", "inline"),
        default="installed",
    )
    args = parser.parse_args()

    args.work.mkdir(parents=True, exist_ok=True)
    args.output.mkdir(parents=True, exist_ok=True)
    prompt = (
        Path(__file__).with_name("held-out-exception.md").read_text(encoding="utf-8")
    )
    if args.executor == "claude" and args.context_mode == "inline":
        root = Path(__file__).resolve().parents[3]
        prompt = f"{claude_inline_context(root)}\n\n<request>\n{prompt}\n</request>"
    prefix = f"{args.executor}-{args.variant}"
    artifact = args.output / f"{prefix}.md"
    raw_path = args.output / f"{prefix}.jsonl"

    started = time.monotonic()
    try:
        if args.executor == "codex":
            completed, raw, usage = run_codex(
                prompt, args.home, args.work, artifact, args.model
            )
        else:
            completed, raw, usage = run_claude(
                prompt, args.home, args.work, artifact, args.model, args.context_mode
            )
    except subprocess.TimeoutExpired as error:
        duration = time.monotonic() - started
        raw_value = error.stdout or ""
        if isinstance(raw_value, bytes):
            raw_value = raw_value.decode("utf-8", errors="replace")
        raw_path.write_text(raw_value, encoding="utf-8")
        print(
            json.dumps(
                {
                    "executor": args.executor,
                    "variant": args.variant,
                    "returncode": 124,
                    "duration_seconds": round(duration, 3),
                    "error": f"trial exceeded {TRIAL_TIMEOUT_SECONDS} seconds",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    duration = time.monotonic() - started
    raw_path.write_text(raw, encoding="utf-8")
    if completed.returncode != 0 or not artifact.exists():
        detail = failure_detail(completed, artifact, raw)
        print(
            json.dumps(
                {
                    "executor": args.executor,
                    "variant": args.variant,
                    "returncode": completed.returncode,
                    "duration_seconds": round(duration, 3),
                    "error": detail,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    score = score_artifact(
        artifact.read_text(encoding="utf-8"),
        ("NetworkClient", "NetworkService", "Main"),
        "예외 전파",
    )
    result = {
        "executor": args.executor,
        "variant": args.variant,
        "model": args.model or "executor-default-unverified",
        "context_mode": args.context_mode,
        "effort": CLAUDE_EFFORT if args.executor == "claude" else "executor-default",
        "returncode": completed.returncode,
        "duration_seconds": round(duration, 3),
        "usage": usage,
        "artifact_bytes": artifact.stat().st_size,
        "quality": score,
    }
    (args.output / f"{prefix}-score.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
