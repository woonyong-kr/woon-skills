#!/usr/bin/env python3
"""Build the root skill catalog from canonical SKILL.md frontmatter."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FRONTMATTER = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n", re.DOTALL)
FIELD = re.compile(r"^(?P<key>[a-z_-]+):\s*(?P<value>.+?)\s*$", re.MULTILINE)


def scalar_fields(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if match is None:
        raise ValueError("missing YAML frontmatter")
    return {
        item.group("key"): item.group("value").strip("\"'")
        for item in FIELD.finditer(match.group("yaml"))
    }


def build(root: Path) -> dict[str, object]:
    skills: list[dict[str, str]] = []
    names: set[str] = set()
    for skill_file in sorted((root / "skills").rglob("SKILL.md")):
        fields = scalar_fields(skill_file.read_text(encoding="utf-8"))
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not name or not description or name in names:
            raise ValueError(f"invalid or duplicate skill metadata: {skill_file}")
        names.add(name)
        directory = skill_file.parent.relative_to(root).as_posix()
        skills.append(
            {
                "name": name,
                "domain": skill_file.parent.relative_to(root / "skills").parts[0],
                "path": directory,
                "description": description,
            }
        )

    profiles: list[dict[str, object]] = []
    for profile_file in sorted((root / "profiles").glob("*.yaml")):
        text = profile_file.read_text(encoding="utf-8")
        name_match = re.search(r"^name:\s*([^\s]+)\s*$", text, re.MULTILINE)
        if name_match is None:
            raise ValueError(f"profile name is missing: {profile_file}")
        installable = not bool(
            re.search(r"^installable:\s*false\s*$", text, re.MULTILINE)
        )
        profiles.append(
            {
                "name": name_match.group(1),
                "path": profile_file.relative_to(root).as_posix(),
                "installable": installable,
            }
        )

    return {
        "generated": True,
        "generator": "scripts/build_catalog.py",
        "version": 1,
        "canonical_root": "skills",
        "targets": ["codex", "claude"],
        "fallback_order": ["woon-canonical", "target-installed"],
        "skills": sorted(skills, key=lambda item: item["name"]),
        "profiles": sorted(profiles, key=lambda item: item["name"]),
    }


def render(catalog: dict[str, object]) -> str:
    return json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = root / "catalog.json"
    expected = render(build(root))
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != expected:
            raise SystemExit("catalog.json is stale; run scripts/build_catalog.py")
        print("catalog.json: ok")
        return 0
    output.write_text(expected, encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
