"""
gh_issue.py: 이슈 관련 작업

사용법:
  python3 gh_issue.py list [--state open|closed|all] [--label bug]
  python3 gh_issue.py get <number>
  python3 gh_issue.py create --title "[bug] 설명" [--body "..."] [--label bug]
  python3 gh_issue.py close <number>
  python3 gh_issue.py comment <number> --body "내용"
"""

import argparse
import sys
from common import err, gh, info, load_config, ok, require_repo, rows, load_convention

TITLE_TAG_TO_LABEL = {
    "bug": "bug",
    "feat": "enhancement",
    "docs": "documentation",
    "question": "question",
    "chore": "maintenance",
}


def list_issues(owner: str, repo: str, state: str = "open", label: str = ""):
    args = ["issue", "list",
            "--repo", f"{owner}/{repo}",
            "--state", state,
            "--json", "number,title,state,labels,assignees",
            "--limit", "30"]
    if label:
        args += ["--label", label]
    data = gh(*args)
    if not data:
        info("해당하는 이슈가 없습니다.")
        return
    items = []
    for issue in data:
        labels = ", ".join(l["name"] for l in issue.get("labels", []))
        label_str = f" [{labels}]" if labels else ""
        items.append(f"#{issue['number']:<4} {issue['title']}{label_str}")
    rows(f"이슈 목록 ({state})", items)


def get_issue(owner: str, repo: str, number: int):
    data = gh("issue", "view", str(number),
              "--repo", f"{owner}/{repo}",
              "--json", "number,title,state,body,labels,assignees,comments")
    labels = ", ".join(l["name"] for l in data.get("labels", []))
    print(f"#{data['number']} {data['title']}")
    print(f"  상태:  {data['state']}")
    if labels:
        print(f"  라벨:  {labels}")
    if data.get("body"):
        print()
        print(data["body"])


def create_issue(owner: str, repo: str, title: str,
                 body: str = "", label: str = ""):
    # 제목 태그에서 라벨 자동 감지
    detected_label = label
    if not detected_label:
        for tag, mapped in TITLE_TAG_TO_LABEL.items():
            if title.lower().startswith(f"[{tag}]"):
                detected_label = mapped
                break

    # 본문이 없으면 이슈 타입에 맞는 템플릿 사용
    if not body:
        body = _default_issue_body(title)

    args = ["issue", "create",
            "--repo", f"{owner}/{repo}",
            "--title", title,
            "--body", body]
    if detected_label:
        args += ["--label", detected_label]

    gh(*args)
    ok(f"이슈 생성됨: {title}")


def close_issue(owner: str, repo: str, number: int):
    gh("issue", "close", str(number), "--repo", f"{owner}/{repo}")
    ok(f"이슈 #{number} 닫힘")


def comment_issue(owner: str, repo: str, number: int, body: str):
    gh("issue", "comment", str(number),
       "--repo", f"{owner}/{repo}",
       "--body", body)
    ok(f"이슈 #{number}에 코멘트 작성됨")


def _default_issue_body(title: str) -> str:
    """제목 태그를 보고 알맞은 템플릿을 반환한다."""
    conv = load_convention("issue")
    lines = conv.splitlines()

    tag = ""
    if title.lower().startswith("[bug]"):
        tag = "bug"
    elif title.lower().startswith("[feat]"):
        tag = "feat"
    else:
        tag = "other"

    # 템플릿 블록 탐색
    target_header = f"## 본문 템플릿: {tag}"
    if tag == "other":
        target_header = "## 본문 템플릿: question / docs / chore"

    in_block = False
    template_lines = []
    found = False
    for line in lines:
        if line.strip() == target_header:
            found = True
            continue
        if found and line.strip().startswith("```markdown"):
            in_block = True
            continue
        if found and in_block and line.strip() == "```":
            break
        if found and in_block:
            template_lines.append(line)

    return "\n".join(template_lines) if template_lines else ""


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="이슈 관련 작업")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list")
    p_list.add_argument("--state", default="open",
                        choices=["open", "closed", "all"])
    p_list.add_argument("--label", default="")

    p_get = sub.add_parser("get")
    p_get.add_argument("number", type=int)

    p_create = sub.add_parser("create")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--body", default="")
    p_create.add_argument("--label", default="")

    p_close = sub.add_parser("close")
    p_close.add_argument("number", type=int)

    p_comment = sub.add_parser("comment")
    p_comment.add_argument("number", type=int)
    p_comment.add_argument("--body", required=True)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    config = load_config()
    owner, repo = require_repo(config)

    if args.cmd == "list":
        list_issues(owner, repo, args.state, args.label)
    elif args.cmd == "get":
        get_issue(owner, repo, args.number)
    elif args.cmd == "create":
        create_issue(owner, repo, args.title, args.body, args.label)
    elif args.cmd == "close":
        close_issue(owner, repo, args.number)
    elif args.cmd == "comment":
        comment_issue(owner, repo, args.number, args.body)


if __name__ == "__main__":
    main()
