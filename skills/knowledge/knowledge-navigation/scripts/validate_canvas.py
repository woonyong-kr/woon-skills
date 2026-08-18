#!/usr/bin/env python3
"""Validate Woon's Markdown-backed JSON Canvas navigation views."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")
BLOCK = re.compile(r"\^([A-Za-z0-9_-]+)\s*$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(errors, f"{path}: JSON을 읽을 수 없습니다: {error}")
        return None
    if not isinstance(payload, dict):
        fail(errors, f"{path}: 최상위 값은 object여야 합니다.")
        return None
    return payload


def resolve_markdown(vault: Path, relative: str, errors: list[str], owner: str) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(errors, f"{owner}: vault 상대 Markdown 경로만 허용합니다: {relative}")
        return None
    resolved = (vault / candidate).resolve()
    try:
        resolved.relative_to(vault)
    except ValueError:
        fail(errors, f"{owner}: vault 밖 경로를 가리킵니다: {relative}")
        return None
    if resolved.suffix != ".md" or not resolved.is_file():
        fail(errors, f"{owner}: 존재하는 .md 파일을 가리켜야 합니다: {relative}")
        return None
    return resolved


def resolve_canvas(vault: Path, relative: str, errors: list[str]) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(errors, f"canvas: vault 상대 .canvas 경로만 허용합니다: {relative}")
        return None
    resolved = (vault / candidate).resolve()
    try:
        resolved.relative_to(vault)
    except ValueError:
        fail(errors, f"canvas: vault 밖 경로를 가리킵니다: {relative}")
        return None
    if resolved.suffix != ".canvas" or not resolved.is_file():
        fail(errors, f"canvas: 존재하는 vault 상대 .canvas 파일을 지정해야 합니다: {relative}")
        return None
    return resolved


def normalize_wikilink_target(target: str) -> str:
    file_part, marker, subpath = target.partition("#")
    normalized_file = file_part if file_part.endswith(".md") else f"{file_part}.md"
    return normalized_file + (marker + subpath if marker else "")


def subpath_exists(markdown: Path, subpath: str) -> bool:
    target = subpath[1:].strip()
    lines = markdown.read_text(encoding="utf-8").splitlines()
    if target.startswith("^"):
        block_id = target[1:]
        return any(match and match.group(1) == block_id for match in (BLOCK.search(line) for line in lines))
    return any(match and match.group(1).strip() == target for match in (HEADING.match(line) for line in lines))


def require_int(node: dict[str, Any], field: str, errors: list[str], node_id: str) -> None:
    value = node.get(field)
    if not isinstance(value, int) or isinstance(value, bool):
        fail(errors, f"node {node_id}: {field}은 정수여야 합니다.")


def canvas_targets(payload: dict[str, Any], vault: Path, errors: list[str], origin: Path) -> tuple[dict[str, dict[str, Any]], set[str]]:
    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        fail(errors, f"{origin}: nodes와 edges는 배열이어야 합니다.")
        return {}, set()

    node_by_id: dict[str, dict[str, Any]] = {}
    targets: set[str] = set()
    for node in nodes:
        if not isinstance(node, dict):
            fail(errors, f"{origin}: object가 아닌 node가 있습니다.")
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            fail(errors, f"{origin}: node id가 비어 있습니다.")
            continue
        if node_id in node_by_id:
            fail(errors, f"{origin}: 중복 node id입니다: {node_id}")
            continue
        node_by_id[node_id] = node
        if node.get("type") != "file":
            fail(errors, f"node {node_id}: file node만 허용합니다.")
            continue
        for field in ("x", "y", "width", "height"):
            require_int(node, field, errors, node_id)
        file_path = node.get("file")
        if not isinstance(file_path, str) or not file_path:
            fail(errors, f"node {node_id}: file 경로가 필요합니다.")
            continue
        markdown = resolve_markdown(vault, file_path, errors, f"node {node_id}")
        subpath = node.get("subpath")
        if subpath is not None:
            if not isinstance(subpath, str) or not subpath.startswith("#"):
                fail(errors, f"node {node_id}: subpath는 # heading 또는 #^block-id여야 합니다.")
            elif markdown is not None and not subpath_exists(markdown, subpath):
                fail(errors, f"node {node_id}: 대상 heading/block이 없습니다: {file_path}{subpath}")
        targets.add(f"{file_path}{subpath or ''}")

    edge_ids: set[str] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            fail(errors, f"{origin}: object가 아닌 edge가 있습니다.")
            continue
        edge_id = edge.get("id")
        if not isinstance(edge_id, str) or not edge_id:
            fail(errors, f"{origin}: edge id가 비어 있습니다.")
        elif edge_id in edge_ids:
            fail(errors, f"{origin}: 중복 edge id입니다: {edge_id}")
        else:
            edge_ids.add(edge_id)
        if "label" in edge:
            fail(errors, f"edge {edge_id}: Canvas에만 지식을 남기지 않도록 label은 허용하지 않습니다.")
        for field in ("fromNode", "toNode"):
            if edge.get(field) not in node_by_id:
                fail(errors, f"edge {edge_id}: 존재하지 않는 {field}입니다: {edge.get(field)}")
    return node_by_id, targets


def manual_subset(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    nodes = {node["id"]: node for node in payload.get("nodes", []) if isinstance(node, dict) and isinstance(node.get("id"), str) and node["id"].startswith("manual-")}
    manual_ids = set(nodes)
    edges = [edge for edge in payload.get("edges", []) if isinstance(edge, dict) and (edge.get("fromNode") in manual_ids or edge.get("toNode") in manual_ids)]
    return nodes, sorted(edges, key=lambda edge: str(edge.get("id")))


def validate_manual_preservation(previous: dict[str, Any], current: dict[str, Any], errors: list[str]) -> None:
    before_nodes, before_edges = manual_subset(previous)
    after_nodes, after_edges = manual_subset(current)
    if before_nodes != after_nodes:
        fail(errors, "manual- node의 위치·크기·대상·속성이 바뀌었습니다. 수동 배치를 보존해야 합니다.")
    if before_edges != after_edges:
        fail(errors, "manual- node에 연결된 edge가 바뀌었습니다. 수동 연결을 보존해야 합니다.")


def canvas_section_targets(markdown: Path, errors: list[str]) -> set[str]:
    content = markdown.read_text(encoding="utf-8")
    section = re.search(r"^## Canvas 노드\s*$([\s\S]*?)(?=^##\s|\Z)", content, re.MULTILINE)
    if section is None:
        fail(errors, f"{markdown}: '## Canvas 노드' section이 필요합니다.")
        return set()
    targets = {normalize_wikilink_target(match.group(1).strip()) for match in WIKILINK.finditer(section.group(1))}
    if not targets:
        fail(errors, f"{markdown}: Canvas 노드 section에 wikilink가 없습니다.")
    return targets


def duplicate_keywords(markdown: Path, errors: list[str]) -> None:
    content = markdown.read_text(encoding="utf-8")
    frontmatter = re.match(r"^---\s*$([\s\S]*?)^---\s*$", content, re.MULTILINE)
    if frontmatter is None:
        fail(errors, f"{markdown}: keywords가 있는 YAML frontmatter가 필요합니다.")
        return
    lines = frontmatter.group(1).splitlines()
    values: list[str] = []
    in_keywords = False
    for line in lines:
        if line.startswith("keywords:"):
            in_keywords = True
            continue
        if in_keywords and re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*", line):
            break
        if in_keywords:
            match = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if match:
                values.append(match.group(1).strip("'\" ").casefold())
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(errors, f"{markdown}: 중복 keyword입니다: {', '.join(duplicates)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--canvas", required=True)
    parser.add_argument("--map", dest="map_path")
    parser.add_argument("--previous")
    args = parser.parse_args()

    errors: list[str] = []
    vault = args.vault.resolve()
    canvas_path = resolve_canvas(vault, args.canvas, errors)
    if canvas_path is None:
        return 1
    payload = load_json(canvas_path, errors)
    current_targets: set[str] = set()
    if payload is not None:
        _, current_targets = canvas_targets(payload, vault, errors, canvas_path)

    if args.previous:
        previous_path = (vault / args.previous).resolve()
        previous = load_json(previous_path, errors) if previous_path.is_file() else None
        if previous is None:
            fail(errors, f"previous: 읽을 수 있는 이전 Canvas가 필요합니다: {args.previous}")
        elif payload is not None:
            validate_manual_preservation(previous, payload, errors)

    if args.map_path:
        map_path = resolve_markdown(vault, args.map_path, errors, "map")
        if map_path is not None:
            duplicate_keywords(map_path, errors)
            if canvas_section_targets(map_path, errors) != current_targets:
                fail(errors, "map의 Canvas 노드 wikilink와 Canvas file/subpath 대상이 일치하지 않습니다.")

    if errors:
        print("Canvas validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Canvas validation passed: {args.canvas} ({len(current_targets)} Markdown node targets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
