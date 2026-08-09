"""
gh_release.py: 릴리즈 관련 작업

사용법:
  python3 gh_release.py list
  python3 gh_release.py create <tag> --title "v1.2.0" [--notes "..."] [--draft]
  python3 gh_release.py notes <tag>
"""

import argparse
import sys
from common import gh, info, load_config, ok, require_repo, rows, load_convention


TYPE_TO_SECTION = {
    "feat":     "기능 추가",
    "fix":      "버그 수정",
    "perf":     "개선",
    "refactor": "개선",
    "docs":     "기타",
    "chore":    "기타",
    "build":    "기타",
    "ci":       "기타",
    "style":    "기타",
    "test":     "기타",
}

SECTION_ORDER = ["기능 추가", "버그 수정", "개선", "기타"]


def list_releases(owner: str, repo: str):
    data = gh("release", "list",
              "--repo", f"{owner}/{repo}",
              "--json", "tagName,name,isDraft,isPrerelease,createdAt",
              "--limit", "10")
    if not data:
        info("릴리즈가 없습니다.")
        return
    items = []
    for r in data:
        flags = []
        if r.get("isDraft"):
            flags.append("draft")
        if r.get("isPrerelease"):
            flags.append("pre")
        flag_str = f" ({', '.join(flags)})" if flags else ""
        items.append(f"{r['tagName']:<12} {r.get('name', '')}{flag_str}")
    rows("릴리즈 목록", items)


def generate_notes(owner: str, repo: str, tag: str) -> str:
    """이전 태그 이후 커밋에서 릴리즈 노트를 생성한다."""
    # 직전 태그 찾기
    releases = gh("release", "list",
                  "--repo", f"{owner}/{repo}",
                  "--json", "tagName",
                  "--limit", "5")
    prev_tag = releases[0]["tagName"] if releases else ""

    # 커밋 목록 가져오기
    range_ref = f"{prev_tag}..HEAD" if prev_tag else "HEAD"
    commits_raw = gh("log", "--oneline", "--no-merges", range_ref)

    if isinstance(commits_raw, str) and commits_raw:
        commit_lines = commits_raw.strip().splitlines()
    else:
        return "변경 내용이 없습니다."

    # 타입별 분류
    sections: dict[str, list[str]] = {s: [] for s in SECTION_ORDER}
    for line in commit_lines:
        parts = line.split(" ", 1)
        if len(parts) < 2:
            continue
        subject = parts[1]
        commit_type = subject.split(":")[0].strip().lower() if ":" in subject else ""
        section = TYPE_TO_SECTION.get(commit_type, "기타")
        # PR 번호 추출
        pr_num = ""
        if "(#" in subject:
            pr_num = " " + subject[subject.rfind("(#"):]
            subject = subject[:subject.rfind("(#")].strip()
        title = subject.split(":", 1)[-1].strip() if ":" in subject else subject
        sections[section].append(f"- {title}{pr_num}")

    # 노트 조합
    lines = ["## 변경 내용", ""]
    for section in SECTION_ORDER:
        if sections[section]:
            lines.append(f"### {section}")
            lines.extend(sections[section])
            lines.append("")

    return "\n".join(lines).strip()


def create_release(owner: str, repo: str, tag: str, title: str,
                   notes: str = "", draft: bool = False):
    if not notes:
        notes = generate_notes(owner, repo, tag)

    args = ["release", "create", tag,
            "--repo", f"{owner}/{repo}",
            "--title", title,
            "--notes", notes]
    if draft:
        args.append("--draft")

    gh(*args)
    ok(f"릴리즈 생성됨: {title} ({tag})")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="릴리즈 관련 작업")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list")

    p_create = sub.add_parser("create")
    p_create.add_argument("tag")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--notes", default="")
    p_create.add_argument("--draft", action="store_true")

    p_notes = sub.add_parser("notes")
    p_notes.add_argument("tag")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    config = load_config()
    owner, repo = require_repo(config)

    if args.cmd == "list":
        list_releases(owner, repo)
    elif args.cmd == "create":
        create_release(owner, repo, args.tag, args.title, args.notes, args.draft)
    elif args.cmd == "notes":
        notes = generate_notes(owner, repo, args.tag)
        print(notes)


if __name__ == "__main__":
    main()
