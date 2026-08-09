"""
gh_pr.py: PR 관련 작업

사용법:
  python3 gh_pr.py list [--state open|closed|merged|all]
  python3 gh_pr.py get <number>
  python3 gh_pr.py create --title "feat: 제목" [--base main] [--body "..."] [--draft]
  python3 gh_pr.py merge <number> [--method squash|rebase|merge]
  python3 gh_pr.py close <number>
  python3 gh_pr.py comment <number> --body "내용"
  python3 gh_pr.py review-requested
"""

import argparse
import sys
from common import err, gh, info, load_config, ok, require_repo, rows


REVIEW_DECISION_KO = {
    "APPROVED": "승인됨",
    "CHANGES_REQUESTED": "변경 요청",
    "REVIEW_REQUIRED": "리뷰 대기",
    "": "리뷰 없음",
}


def list_prs(owner: str, repo: str, state: str = "open"):
    data = gh("pr", "list",
              "--repo", f"{owner}/{repo}",
              "--state", state,
              "--json", "number,title,state,reviewDecision,headRefName,author",
              "--limit", "30")
    if not data:
        info("해당하는 PR이 없습니다.")
        return
    items = []
    for pr in data:
        decision = REVIEW_DECISION_KO.get(pr.get("reviewDecision") or "", "")
        items.append(f"#{pr['number']:<4} {pr['title']:<50} ({decision})")
    rows(f"PR 목록 ({state})", items)


def get_pr(owner: str, repo: str, number: int):
    data = gh("pr", "view", str(number),
              "--repo", f"{owner}/{repo}",
              "--json", "number,title,state,body,reviewDecision,headRefName,baseRefName,author")
    print(f"#{data['number']} {data['title']}")
    print(f"  브랜치: {data['headRefName']} → {data['baseRefName']}")
    print(f"  상태:   {data['state']} / {REVIEW_DECISION_KO.get(data.get('reviewDecision') or '', '')}")
    if data.get("body"):
        print()
        print(data["body"])


def create_pr(owner: str, repo: str, title: str, base: str = "main",
              body: str = "", draft: bool = False):
    args = ["pr", "create",
            "--repo", f"{owner}/{repo}",
            "--title", title,
            "--base", base]
    if body:
        args += ["--body", body]
    else:
        args += ["--body", _default_pr_body()]
    if draft:
        args.append("--draft")
    result = gh(*args)
    ok(f"PR 생성됨: {title}")
    if isinstance(result, str) and result.startswith("http"):
        info(result)

def merge_pr(owner: str, repo: str, number: int, method: str = "squash"):
    gh("pr", "merge", str(number),
       "--repo", f"{owner}/{repo}",
       f"--{method}")
    ok(f"PR #{number} 머지됨 ({method})")


def close_pr(owner: str, repo: str, number: int):
    gh("pr", "close", str(number), "--repo", f"{owner}/{repo}")
    ok(f"PR #{number} 닫힘")


def comment_pr(owner: str, repo: str, number: int, body: str):
    gh("pr", "comment", str(number),
       "--repo", f"{owner}/{repo}",
       "--body", body)
    ok(f"PR #{number}에 코멘트 작성됨")


def review_requested(owner: str, repo: str):
    """내가 리뷰 요청받은 PR 목록을 조회한다."""
    data = gh("pr", "list",
              "--repo", f"{owner}/{repo}",
              "--search", "review-requested:@me",
              "--json", "number,title,author,reviewDecision",
              "--limit", "20")
    if not data:
        info("리뷰 요청받은 PR이 없습니다.")
        return
    items = [f"#{pr['number']:<4} {pr['title']:<50} (by {pr['author']['login']})"
             for pr in data]
    rows("리뷰 요청받은 PR", items)


def _default_pr_body() -> str:
    """conventions/pr.md에서 본문 템플릿을 추출한다."""
    from common import load_convention
    conv = load_convention("pr")
    # 템플릿 마크다운 블록 추출
    lines = conv.splitlines()
    in_block = False
    template_lines = []
    for line in lines:
        if line.strip() == "```markdown" and not in_block:
            in_block = True
            continue
        if line.strip() == "```" and in_block:
            break
        if in_block:
            template_lines.append(line)
    return "\n".join(template_lines) if template_lines else ""


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PR 관련 작업")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list")
    p_list.add_argument("--state", default="open",
                        choices=["open", "closed", "merged", "all"])

    p_get = sub.add_parser("get")
    p_get.add_argument("number", type=int)

    p_create = sub.add_parser("create")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--base", default="main")
    p_create.add_argument("--body", default="")
    p_create.add_argument("--draft", action="store_true")

    p_merge = sub.add_parser("merge")
    p_merge.add_argument("number", type=int)
    p_merge.add_argument("--method", default="squash",
                         choices=["squash", "rebase", "merge"])

    p_close = sub.add_parser("close")
    p_close.add_argument("number", type=int)

    p_comment = sub.add_parser("comment")
    p_comment.add_argument("number", type=int)
    p_comment.add_argument("--body", required=True)

    sub.add_parser("review-requested")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    config = load_config()
    owner, repo = require_repo(config)

    if args.cmd == "list":
        list_prs(owner, repo, args.state)
    elif args.cmd == "get":
        get_pr(owner, repo, args.number)
    elif args.cmd == "create":
        create_pr(owner, repo, args.title, args.base, args.body, args.draft)
    elif args.cmd == "merge":
        merge_pr(owner, repo, args.number, args.method)
    elif args.cmd == "close":
        close_pr(owner, repo, args.number)
    elif args.cmd == "comment":
        comment_pr(owner, repo, args.number, args.body)
    elif args.cmd == "review-requested":
        review_requested(owner, repo)


if __name__ == "__main__":
    main()
