#!/usr/bin/env python3
"""
skill-syncer: skills 저장소 -> Claude/Codex 스킬 디렉토리 동기화

SOURCE_DIR 결정 우선순위:
  1. --source 인자
  2. 환경변수 SKILL_SOURCE_DIR
  3. 환경변수 CLAUDE_SKILL_SOURCE_DIR (레거시 호환)
  4. 이 스크립트 위치(scripts/) 기준 상위 2단계(skills 루트) 자동 사용
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
from pathlib import Path

_script_based_dir = Path(__file__).resolve().parents[2]
SOURCE_DIR = Path(
    os.environ.get("SKILL_SOURCE_DIR")
    or os.environ.get("CLAUDE_SKILL_SOURCE_DIR")
    or _script_based_dir
)
CLAUDE_SKILLS_PLUGIN_ROOT = Path(
    os.environ.get(
        "CLAUDE_SKILLS_PLUGIN_ROOT",
        str(Path.home() / "Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"),
    )
)
CODEX_SKILLS_DIR = Path(
    os.environ.get("CODEX_SKILLS_DIR", str(Path.home() / ".codex" / "skills"))
)
IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def find_claude_target_skills_dir() -> Path | None:
    """현재 활성 Claude 세션의 skills 디렉토리를 동적으로 탐색한다."""
    if not CLAUDE_SKILLS_PLUGIN_ROOT.exists():
        return None

    candidates = []

    for plugin_id_dir in CLAUDE_SKILLS_PLUGIN_ROOT.iterdir():
        if not plugin_id_dir.is_dir():
            continue
        for session_id_dir in plugin_id_dir.iterdir():
            if not session_id_dir.is_dir():
                continue
            skills_dir = session_id_dir / "skills"
            if skills_dir.exists() and skills_dir.is_dir():
                mtime = max(
                    f.stat().st_mtime
                    for f in skills_dir.rglob("*")
                    if f.is_file()
                ) if any(skills_dir.rglob("*")) else skills_dir.stat().st_mtime
                candidates.append((mtime, skills_dir))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]


def iter_skill_files(skill_dir: Path):
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(skill_dir).parts
        if "__pycache__" in rel_parts or path.name == ".DS_Store" or path.suffix == ".pyc":
            continue
        yield path


def build_signature(skill_dir: Path) -> tuple[tuple[str, str], ...]:
    """스킬 디렉토리의 실제 파일 내용을 기준으로 비교용 서명을 만든다."""
    signature = []
    for path in iter_skill_files(skill_dir):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        signature.append((path.relative_to(skill_dir).as_posix(), digest))
    return tuple(signature)


def replace_tree(src: Path, dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=IGNORE_PATTERNS)


def sync_skill(skill_src: Path, target_dir: Path) -> str:
    """단일 스킬 폴더를 target_dir에 복사하고 상태를 반환한다."""
    dest = target_dir / skill_src.name

    if not dest.exists():
        shutil.copytree(skill_src, dest, ignore=IGNORE_PATTERNS)
        return "added"
    if build_signature(skill_src) != build_signature(dest):
        replace_tree(skill_src, dest)
        return "updated"
    return "skipped"


def collect_skill_dirs(source_dir: Path) -> list[Path]:
    return sorted(
        d for d in source_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").exists()
    )


def resolve_targets(target: str) -> tuple[list[tuple[str, Path]], list[str]]:
    resolved = []
    warnings = []

    if target in ("claude", "all"):
        claude_target = find_claude_target_skills_dir()
        if claude_target:
            resolved.append(("claude", claude_target))
        else:
            warnings.append(
                "[경고] Claude 스킬 디렉토리를 찾지 못했습니다. "
                f"확인 경로: {CLAUDE_SKILLS_PLUGIN_ROOT}"
            )

    if target in ("codex", "all"):
        CODEX_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        resolved.append(("codex", CODEX_SKILLS_DIR))

    return resolved, warnings


def sync_target(target_name: str, target_dir: Path, skill_dirs: list[Path]) -> dict[str, list[str]]:
    added, updated, skipped = [], [], []

    for skill_dir in skill_dirs:
        status = sync_skill(skill_dir, target_dir)
        if status == "added":
            added.append(skill_dir.name)
        elif status == "updated":
            updated.append(skill_dir.name)
        else:
            skipped.append(skill_dir.name)

    print(f"[완료] {target_name} 동기화")
    print(f"  대상:       {target_dir}")
    if added:
        print(f"  추가됨     : {', '.join(added)}")
    if updated:
        print(f"  업데이트됨 : {', '.join(updated)}")
    if skipped:
        print(f"  변경 없음  : {', '.join(skipped)}")
    print()

    return {"added": added, "updated": updated, "skipped": skipped}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Claude/Codex 스킬 디렉토리 동기화")
    parser.add_argument("--target", choices=["claude", "codex", "all"], default="all")
    parser.add_argument("--source", default="")
    return parser.parse_args()


def main():
    args = parse_args()
    source_dir = Path(args.source or SOURCE_DIR).expanduser().resolve()

    if not source_dir.exists():
        print(f"[오류] 소스 디렉토리를 찾을 수 없습니다: {source_dir}")
        raise SystemExit(1)

    skill_dirs = collect_skill_dirs(source_dir)
    if not skill_dirs:
        print("[경고] 소스 디렉토리에 SKILL.md를 가진 스킬 폴더가 없습니다.")
        return

    targets, warnings = resolve_targets(args.target)
    if not targets:
        for warning in warnings:
            print(warning)
        raise SystemExit(1)

    print(f"소스:  {source_dir}")
    print(f"대상:  {', '.join(name for name, _ in targets)}")
    print()

    reports = []
    for target_name, target_dir in targets:
        reports.append(sync_target(target_name, target_dir, skill_dirs))

    for warning in warnings:
        print(warning)

    if any(report["added"] for report in reports):
        print("[안내] 새로 추가된 스킬은 도구에 따라 다음 세션부터 인식될 수 있습니다.")
    if any(report["updated"] for report in reports):
        print("[안내] 기존 스킬 업데이트는 현재 세션에서 바로 반영될 수 있습니다.")


if __name__ == "__main__":
    main()
