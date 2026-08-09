"""
common.py: 설정 로드 / 출력 포맷 / gh CLI 래핑 공통 유틸
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


# ─── 설정 ────────────────────────────────────────────────────────────────────

def load_config() -> dict:
    """
    설정 우선순위:
      1. 환경변수
      2. ~/.config/skills/github.env
      3. ~/.config/claude-skill/github.env (레거시 호환)
      4. 현재 디렉토리의 git remote URL 자동 감지
    """
    config = {}

    env_files = [
        Path.home() / ".config" / "claude-skill" / "github.env",
        Path.home() / ".config" / "skills" / "github.env",
    ]
    for env_file in env_files:
        if not env_file.exists():
            continue
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                config[key.strip()] = value.strip()

    for key in ("GITHUB_DEFAULT_OWNER", "GITHUB_DEFAULT_REPO", "GITHUB_TOKEN"):
        if key in os.environ:
            config[key] = os.environ[key]

    if "GITHUB_DEFAULT_OWNER" not in config or "GITHUB_DEFAULT_REPO" not in config:
        remote = _detect_remote()
        if remote:
            config.setdefault("GITHUB_DEFAULT_OWNER", remote[0])
            config.setdefault("GITHUB_DEFAULT_REPO", remote[1])

    return config


def _detect_remote() -> tuple[str, str] | None:
    """현재 git 저장소의 origin remote에서 owner/repo를 추출한다."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        # https://github.com/owner/repo.git 또는 git@github.com:owner/repo.git
        if "github.com" in url:
            path = url.split("github.com")[-1].lstrip("/:").removesuffix(".git")
            parts = path.split("/")
            if len(parts) == 2:
                return parts[0], parts[1]
    except subprocess.CalledProcessError:
        pass
    return None


def require_repo(config: dict) -> tuple[str, str]:
    """owner/repo를 반환한다. 없으면 오류 출력 후 종료."""
    owner = config.get("GITHUB_DEFAULT_OWNER")
    repo = config.get("GITHUB_DEFAULT_REPO")
    if not owner or not repo:
        err("저장소를 찾을 수 없습니다. ~/.config/skills/github.env에 "
            "GITHUB_DEFAULT_OWNER와 GITHUB_DEFAULT_REPO를 설정하거나 "
            "(레거시: ~/.config/claude-skill/github.env) "
            "git 저장소 내에서 실행하세요.")
        sys.exit(1)
    return owner, repo


# ─── 출력 포맷 ────────────────────────────────────────────────────────────────

def ok(msg: str):
    print(f"[완료] {msg}")

def err(msg: str):
    print(f"[오류] {msg}", file=sys.stderr)

def info(msg: str):
    print(f"[안내] {msg}")

def warn(msg: str):
    print(f"[경고] {msg}")

def rows(title: str, items: list[str]):
    print(f"[목록] {title}")
    for item in items:
        print(f"  {item}")


# ─── gh CLI 래핑 ─────────────────────────────────────────────────────────────

def gh(*args, input_text: str | None = None) -> dict | list | str:
    """
    gh CLI를 실행하고 JSON 결과를 반환한다.
    JSON이 아닌 경우 문자열을 반환한다.
    오류 발생 시 err() 출력 후 sys.exit(1).
    """
    cmd = ["gh"] + list(args)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            input=input_text,
        )
        if result.returncode != 0:
            err(result.stderr.strip() or f"gh 명령 실패: {' '.join(cmd)}")
            sys.exit(1)
        output = result.stdout.strip()
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return output
    except FileNotFoundError:
        err("gh CLI가 설치되어 있지 않습니다. https://cli.github.com 에서 설치하세요.")
        sys.exit(1)


def gh_silent(*args) -> bool:
    """성공 여부만 반환한다. 오류 메시지를 직접 처리할 때 사용한다."""
    cmd = ["gh"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


# ─── 컨벤션 로더 ──────────────────────────────────────────────────────────────

def load_convention(name: str) -> str:
    """conventions/<name>.md 파일을 읽어 반환한다."""
    base = Path(__file__).resolve().parent.parent / "conventions"
    path = base / f"{name}.md"
    if not path.exists():
        warn(f"컨벤션 파일을 찾을 수 없습니다: {path}")
        return ""
    return path.read_text()
