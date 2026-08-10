#!/usr/bin/env python3
"""Run deterministic structural checks for the Woon skill catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path

from audit_backend import audit_backend
from audit_insight import audit_insight
from audit_learning_content import audit_learning_content
from audit_sources import audit_sources
from build_catalog import FRONTMATTER, build, render, scalar_fields

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
INTERFACE_FIELD = re.compile(
    r'^  (?P<key>display_name|short_description|default_prompt): (?P<value>".*")$',
    re.MULTILINE,
)


def interface_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in INTERFACE_FIELD.finditer(text):
        fields[match.group("key")] = json.loads(match.group("value"))
    return fields


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    names: set[str] = set()
    skill_files = sorted((root / "skills").rglob("SKILL.md"))

    for skill_file in skill_files:
        text = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if match is None:
            errors.append(f"{skill_file}: missing frontmatter")
            continue
        fields = scalar_fields(text)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not NAME.fullmatch(name) or len(name) > 64:
            errors.append(f"{skill_file}: invalid name {name!r}")
        if name != skill_file.parent.name:
            errors.append(f"{skill_file}: directory and name differ")
        if name in names:
            errors.append(f"{skill_file}: duplicate name {name!r}")
        names.add(name)
        if not description or len(description) > 1024:
            errors.append(f"{skill_file}: invalid description length")

        agent_file = skill_file.parent / "agents" / "openai.yaml"
        if not agent_file.exists():
            errors.append(f"{skill_file.parent}: missing agents/openai.yaml")
        else:
            interface = interface_fields(agent_file.read_text(encoding="utf-8"))
            missing = {
                "display_name",
                "short_description",
                "default_prompt",
            }.difference(interface)
            if missing:
                errors.append(f"{agent_file}: missing quoted fields {sorted(missing)}")
            short = interface.get("short_description", "")
            if short and not 25 <= len(short) <= 64:
                errors.append(f"{agent_file}: short_description must be 25..64 chars")
            prompt = interface.get("default_prompt", "")
            if prompt and f"${name}" not in prompt:
                errors.append(f"{agent_file}: default_prompt must contain ${name}")

        for raw_link in LINK.findall(text):
            target = raw_link.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            linked = (skill_file.parent / target).resolve()
            if not linked.exists():
                errors.append(f"{skill_file}: broken link {raw_link!r}")

    output = root / "catalog.json"
    expected = render(build(root))
    if not output.exists() or output.read_text(encoding="utf-8") != expected:
        errors.append("catalog.json: stale generated catalog")

    eval_profile = (root / "profiles" / "eval.yaml").read_text(encoding="utf-8")
    if not re.search(r"^installable:\s*false\s*$", eval_profile, re.MULTILINE):
        errors.append("profiles/eval.yaml: installable must be false")

    errors.extend(audit_sources(root))
    errors.extend(audit_learning_content(root))
    errors.extend(audit_backend(root))
    errors.extend(audit_insight(root))

    if errors:
        print("\n".join(f"error: {error}" for error in errors))
        return 1
    source_reviews = len(list((root / "sources" / "reviews").glob("*.yaml")))
    print(
        f"skills={len(skill_files)} metadata=ok links=ok catalog=ok "
        f"source_reviews={source_reviews}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
