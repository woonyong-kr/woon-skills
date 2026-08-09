"""
gh_readme.py: README 자동 업데이트

사용법:
  python3 gh_readme.py update [--section usage|env|features|all]
  python3 gh_readme.py preview
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from common import info, load_config, load_convention, ok, warn


README_PATH = Path("README.md")

SECTION_TRIGGERS = {
    "usage":    ["scripts/"],
    "env":      [".env.example"],
    "features": ["SKILL.md"],
}

SECTION_HEADERS_KO = {
    "usage":    "사용법",
    "env":      "환경 설정",
    "features": "주요 기능",
}


def detect_changed_sections() -> list[str]:
    """git diff로 변경된 파일을 감지하고 업데이트가 필요한 섹션을 반환한다."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True
        )
        changed = result.stdout.strip().splitlines()
    except Exception:
        return []

    sections = []
    for section, triggers in SECTION_TRIGGERS.items():
        if any(any(t in f for f in changed) for t in triggers):
            sections.append(section)
    return sections


def read_readme() -> str:
    if not README_PATH.exists():
        return ""
    return README_PATH.read_text()


def update_section(content: str, section: str, new_body: str) -> str:
    """README에서 특정 섹션의 본문만 교체한다. 구조는 유지한다."""
    header = SECTION_HEADERS_KO.get(section, section)
    pattern = rf"(## {re.escape(header)}\n)(.*?)(?=\n## |\Z)"
    replacement = rf"\g<1>{new_body}\n"
    updated = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if updated == content:
        warn(f"'{header}' 섹션을 찾지 못했습니다. README에 '## {header}' 헤더가 있는지 확인하세요.")
    return updated


def generate_section_content(section: str) -> str:
    """섹션 유형에 따라 새 본문을 생성한다."""
    if section == "env":
        env_example = Path(".env.example")
        if env_example.exists():
            return f"```bash\n{env_example.read_text().strip()}\n```"
        return ""
    if section == "usage":
        # scripts/ 하위 파일 목록 기반으로 사용법 섹션 생성 안내만 제공
        # 실제 내용은 도구가 scripts/ 코드를 읽고 채워야 함
        info("사용법 섹션은 scripts/ 코드를 분석해서 직접 작성해야 합니다.")
        return ""
    return ""


def preview():
    """변경이 필요한 섹션을 출력한다."""
    sections = detect_changed_sections()
    if not sections:
        info("변경 감지된 섹션이 없습니다.")
        return
    for s in sections:
        header = SECTION_HEADERS_KO.get(s, s)
        print(f"  업데이트 필요: ## {header}")


def update(section_filter: str = "all"):
    if not README_PATH.exists():
        warn("README.md가 없습니다.")
        return

    if section_filter == "all":
        sections = detect_changed_sections()
        if not sections:
            info("변경 감지된 섹션이 없습니다.")
            return
    else:
        sections = [section_filter]

    content = read_readme()
    updated_sections = []

    for section in sections:
        new_body = generate_section_content(section)
        if not new_body:
            continue
        content = update_section(content, section, new_body)
        updated_sections.append(SECTION_HEADERS_KO.get(section, section))

    if updated_sections:
        README_PATH.write_text(content)
        ok(f"README 업데이트됨: {', '.join(updated_sections)}")
    else:
        info("자동으로 업데이트할 수 있는 섹션이 없습니다. 직접 작성이 필요합니다.")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="README 자동 업데이트")
    sub = parser.add_subparsers(dest="cmd")

    p_update = sub.add_parser("update")
    p_update.add_argument("--section", default="all",
                          choices=["all", "usage", "env", "features"])

    sub.add_parser("preview")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    load_config()

    if args.cmd == "update":
        update(args.section)
    elif args.cmd == "preview":
        preview()


if __name__ == "__main__":
    main()
