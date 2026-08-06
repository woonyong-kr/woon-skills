#!/usr/bin/env python3
"""Resolve the running Docker container that mounts a host workspace and run commands in it."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Match:
    container_id: str
    container_name: str
    image: str
    host_source: str
    container_dest: str
    container_workdir: str


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        stderr = proc.stderr.strip() or proc.stdout.strip() or "command failed"
        raise RuntimeError(f"{' '.join(cmd)}: {stderr}")
    return proc.stdout


def running_containers() -> list[tuple[str, str, str]]:
    output = run(
        [
            "docker",
            "ps",
            "--format",
            "{{.ID}}\t{{.Names}}\t{{.Image}}",
        ]
    )
    containers = []
    for line in output.splitlines():
        if not line.strip():
            continue
        container_id, name, image = line.split("\t", 2)
        containers.append((container_id, name, image))
    return containers


def inspect_mounts(container_ids: Iterable[str]) -> list[dict]:
    ids = list(container_ids)
    if not ids:
        return []
    output = run(["docker", "inspect", *ids])
    return json.loads(output)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def find_best_match(workdir: Path) -> Match:
    containers = running_containers()
    inspected = inspect_mounts(container_id for container_id, _, _ in containers)

    best: Match | None = None
    best_len = -1

    for data in inspected:
        container_id = data["Id"][:12]
        name = data["Name"].lstrip("/")
        image = data["Config"]["Image"]
        for mount in data.get("Mounts", []):
            source = mount.get("Source")
            dest = mount.get("Destination")
            mount_type = mount.get("Type")
            if mount_type != "bind" or not source or not dest:
                continue

            source_path = Path(source).resolve()
            if not is_relative_to(workdir, source_path):
                continue

            rel = workdir.relative_to(source_path)
            container_workdir = Path(dest) / rel
            match = Match(
                container_id=container_id,
                container_name=name,
                image=image,
                host_source=str(source_path),
                container_dest=dest,
                container_workdir=str(container_workdir),
            )

            score = len(str(source_path))
            if score > best_len:
                best = match
                best_len = score

    if best is None:
        raise RuntimeError(
            f"no running Docker container has a bind mount covering host path: {workdir}"
        )
    return best


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Find the running Docker container that mounts a host workspace and "
            "run commands inside the corresponding container directory."
        )
    )
    parser.add_argument(
        "--workdir",
        default=os.getcwd(),
        help="Host workspace path to match. Defaults to the current directory.",
    )
    parser.add_argument(
        "--print-match",
        action="store_true",
        help="Print the chosen container match and exit.",
    )
    parser.add_argument(
        "--shell",
        help="Run a shell command in the container using sh -lc.",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to execute after '--'. Example: -- make test",
    )
    return parser.parse_args()


def format_match(match: Match) -> str:
    return (
        f"container={match.container_name} ({match.container_id})\n"
        f"image={match.image}\n"
        f"host_source={match.host_source}\n"
        f"container_dest={match.container_dest}\n"
        f"container_workdir={match.container_workdir}"
    )


def main() -> int:
    args = parse_args()
    workdir = Path(args.workdir).expanduser().resolve()

    try:
        match = find_best_match(workdir)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.print_match:
        print(format_match(match))
        return 0

    if args.shell and args.command:
        print("error: use either --shell or '-- command ...', not both", file=sys.stderr)
        return 2

    if args.shell:
        cmd = [
            "docker",
            "exec",
            match.container_name,
            "sh",
            "-lc",
            f"cd {sh_quote(match.container_workdir)} && {args.shell}",
        ]
        return subprocess.run(cmd).returncode

    command = args.command
    if command and command[0] == "--":
        command = command[1:]

    if not command:
        print(format_match(match))
        return 0

    cmd = [
        "docker",
        "exec",
        "-w",
        match.container_workdir,
        match.container_name,
        *command,
    ]
    return subprocess.run(cmd).returncode


def sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


if __name__ == "__main__":
    sys.exit(main())
