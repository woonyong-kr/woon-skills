#!/usr/bin/env python3
"""Validate the Markdown-frontmatter graph consumed by Markdown Mindmap."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
MAP_BLOCK = re.compile(r"```mindmap\n(.*?)\n```", re.DOTALL)
LEVEL = re.compile(
    r"^\s*-\s*id:\s*(?P<id>[\w-]+).*?\n"
    r"(?P<body>.*?)(?=^\s*-\s*id:|^edges:|\Z)",
    re.MULTILINE | re.DOTALL,
)
EDGE = re.compile(
    r"^\s*-\s*\{\s*from:\s*(?P<from>[\w-]+),\s*to:\s*(?P<to>[\w-]+),\s*via:\s*(?P<via>[\w-]+)\s*}\s*$",
    re.MULTILINE,
)
FROM = re.compile(r"^\s*from:\s*(?P<path>\S+)\s*$", re.MULTILINE)
ROLE = re.compile(r"mindmap_role:\s*(?P<role>[\w-]+)")
FIELD = re.compile(r"^(?P<key>[\w-]+):\s*(?P<value>.+?)\s*$", re.MULTILINE)
WIKILINK = re.compile(r"\[\[(?P<target>[^\]|#]+)")


@dataclass(frozen=True)
class Note:
    path: Path
    fields: dict[str, str]


def frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        return {}
    return {
        field.group("key"): field.group("value").strip().strip('"\'')
        for field in FIELD.finditer(match.group(1))
    }


def map_levels(block: str) -> dict[str, tuple[Path, str]]:
    levels: dict[str, tuple[Path, str]] = {}
    for match in LEVEL.finditer(block):
        source = FROM.search(match.group("body"))
        role = ROLE.search(match.group("body"))
        if source is None or role is None:
            raise ValueError(f"level {match.group('id')} needs from and mindmap_role")
        levels[match.group("id")] = (Path(source.group("path")), role.group("role"))
    if not levels:
        raise ValueError("mindmap block has no levels")
    return levels


def all_notes(vault: Path, folders: set[Path]) -> list[Note]:
    notes: list[Note] = []
    for folder in folders:
        absolute = vault / folder
        if not absolute.is_dir():
            raise ValueError(f"mindmap folder does not exist: {folder}")
        for path in sorted(absolute.rglob("*.md")):
            notes.append(Note(path.relative_to(vault), frontmatter(path)))
    return notes


def resolve_parent(raw: str, notes: list[Note]) -> Path | None:
    match = WIKILINK.search(raw)
    if match is None:
        return None
    target = match.group("target").strip()
    candidates = [note.path for note in notes if note.path.with_suffix("").as_posix() == target]
    candidates.extend(note.path for note in notes if note.path.stem == target)
    unique = list(dict.fromkeys(candidates))
    return unique[0] if len(unique) == 1 else None


def validate(vault: Path, map_path: Path) -> list[str]:
    text = (vault / map_path).read_text(encoding="utf-8")
    blocks = MAP_BLOCK.findall(text)
    if len(blocks) != 1:
        return [f"{map_path}: expected exactly one mindmap fenced block"]
    try:
        levels = map_levels(blocks[0])
    except ValueError as error:
        return [f"{map_path}: {error}"]
    notes = all_notes(vault, {folder for folder, _ in levels.values()})
    selected: dict[str, list[Note]] = {
        level: [note for note in notes if note.fields.get("mindmap_role") == role]
        for level, (_, role) in levels.items()
    }
    errors: list[str] = []
    for level, matching in selected.items():
        if not matching:
            errors.append(f"{map_path}: level {level} selects no Markdown note")
    selected_paths = {note.path for matching in selected.values() for note in matching}
    seen_ids: dict[str, Path] = {}
    for note in (note for note in notes if note.path in selected_paths):
        identifier = note.fields.get("mindmap_id", "")
        if not identifier:
            errors.append(f"{note.path}: missing mindmap_id")
        elif identifier in seen_ids:
            errors.append(f"duplicate mindmap_id {identifier}: {seen_ids[identifier]} and {note.path}")
        else:
            seen_ids[identifier] = note.path
    for edge in EDGE.finditer(blocks[0]):
        from_level = edge.group("from")
        to_level = edge.group("to")
        via = edge.group("via")
        if from_level not in selected or to_level not in selected:
            errors.append(f"{map_path}: edge references an unknown level")
            continue
        if via != "parent":
            errors.append(f"{map_path}: only parent frontmatter edges are allowed")
            continue
        parents = {note.path for note in selected[from_level]}
        for child in selected[to_level]:
            raw_parent = child.fields.get("parent", "")
            parent = resolve_parent(raw_parent, notes)
            if parent not in parents:
                errors.append(
                    f"{child.path}: parent {raw_parent or '(missing)'} does not resolve to {from_level}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    args = parser.parse_args()
    try:
        errors = validate(args.vault.resolve(), args.map)
    except (OSError, ValueError) as error:
        print(f"Markdown Mindmap validation failed: {error}", file=sys.stderr)
        return 1
    if errors:
        print("Markdown Mindmap validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Markdown Mindmap validation passed: {args.map}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
