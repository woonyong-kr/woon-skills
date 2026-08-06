#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from common import (
    close_issue,
    default_branch,
    err,
    gh,
    info,
    ok,
    repo_root,
    reopen_issue,
    require_repo,
    update_project_status,
)


PATH_SPEC_RE = re.compile(r"^(?P<path>.+?)(?::(?P<start>\d+)(?::(?P<end>\d+))?)?$")


def parse_path_spec(raw: str) -> tuple[str, int | None, int | None]:
    match = PATH_SPEC_RE.match(raw)
    if not match:
        return raw, None, None
    path = match.group("path")
    start = match.group("start")
    end = match.group("end")
    return path, int(start) if start else None, int(end) if end else None


def resolve_repo_relative(path_text: str) -> Path:
    root = repo_root()
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    else:
        path = path.resolve()
    try:
        return path.relative_to(root)
    except ValueError:
        err(f"저장소 바깥 파일은 링크할 수 없습니다: {path}")
        sys.exit(1)


def build_blob_url(owner: str, repo: str, ref: str, raw_spec: str) -> str:
    path_text, start, end = parse_path_spec(raw_spec)
    rel = resolve_repo_relative(path_text)
    url = f"https://github.com/{owner}/{repo}/blob/{ref}/{rel.as_posix()}"
    if start and end:
        url += f"#L{start}-L{end}"
    elif start:
        url += f"#L{start}"
    return url


def render_links(owner: str, repo: str, ref: str, specs: list[str]) -> list[str]:
    lines: list[str] = []
    for spec in specs:
        path_text, start, end = parse_path_spec(spec)
        rel = resolve_repo_relative(path_text)
        label = rel.as_posix()
        if start and end:
            label = f"{label}:{start}-{end}"
        elif start:
            label = f"{label}:{start}"
        url = build_blob_url(owner, repo, ref, spec)
        lines.append(f"- {label}: {url}")
    return lines


def read_body(body: str, body_file: str) -> str:
    if body_file:
        return Path(body_file).read_text().strip()
    return body.strip()


def append_links(body: str, links: list[str]) -> str:
    if not links:
        return body
    if body:
        return f"{body}\n\n관련 링크\n" + "\n".join(links)
    return "관련 링크\n" + "\n".join(links)


def create_or_update_comment(owner: str, repo: str, issue: int, body: str, comment_id: int | None) -> None:
    if comment_id:
        gh(
            "api",
            f"repos/{owner}/{repo}/issues/comments/{comment_id}",
            "-X",
            "PATCH",
            "-f",
            f"body={body}",
        )
        ok(f"댓글 #{comment_id} 수정")
        return

    gh(
        "issue",
        "comment",
        str(issue),
        "--repo",
        f"{owner}/{repo}",
        "--body",
        body,
    )
    ok(f"이슈 #{issue}에 댓글 작성")


def apply_issue_state(owner: str, repo: str, issue: int, state: str | None) -> None:
    if not state:
        return
    normalized = state.strip().lower()
    if normalized in {"open", "opened", "reopen", "reopened"}:
        reopen_issue(owner, repo, issue)
    elif normalized in {"closed", "close", "done", "완료"}:
        close_issue(owner, repo, issue)
    else:
        err(f"지원하지 않는 이슈 상태입니다: {state}")
        sys.exit(1)


def cmd_link(args: argparse.Namespace) -> None:
    owner, repo = require_repo()
    ref = args.ref or default_branch(owner, repo)
    lines = render_links(owner, repo, ref, args.paths)
    if args.markdown:
        print("\n".join(lines))
        return
    for line in lines:
        print(line.split(": ", 1)[1])


def cmd_comment(args: argparse.Namespace) -> None:
    owner, repo = require_repo()
    ref = args.ref or default_branch(owner, repo)
    body = read_body(args.body, args.body_file)
    if not body and not args.link:
        err("댓글 본문이 비어 있습니다.")
        sys.exit(1)
    body = append_links(body, render_links(owner, repo, ref, args.link))
    if args.dry_run:
        print(body)
        return
    create_or_update_comment(owner, repo, args.issue, body, args.edit_comment_id)


def cmd_status(args: argparse.Namespace) -> None:
    owner, repo = require_repo()
    if args.dry_run:
        info("dry-run이라 상태 변경은 하지 않았습니다.")
        return
    if args.project_status:
        update_project_status(owner, repo, args.issue, args.project_status, args.project_title)
    apply_issue_state(owner, repo, args.issue, args.issue_state)


def cmd_sync(args: argparse.Namespace) -> None:
    owner, repo = require_repo()
    ref = args.ref or default_branch(owner, repo)
    body = read_body(args.body, args.body_file)
    if not body and not args.link and not args.project_status and not args.issue_state:
        err("처리할 내용이 없습니다.")
        sys.exit(1)

    if body or args.link:
        body = append_links(body, render_links(owner, repo, ref, args.link))
        if args.dry_run:
            print(body)
        else:
            create_or_update_comment(owner, repo, args.issue, body, args.edit_comment_id)

    if args.dry_run:
        info("dry-run이라 실제 변경은 하지 않았습니다.")
        return

    if args.project_status:
        update_project_status(owner, repo, args.issue, args.project_status, args.project_title)

    issue_state = args.issue_state
    normalized_project_status = (args.project_status or "").strip().lower().replace("_", "-")
    if not issue_state and args.close_when_done and normalized_project_status in {"done", "완료"}:
        issue_state = "closed"

    apply_issue_state(owner, repo, args.issue, issue_state)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GitHub 이슈 댓글/링크/상태 관리")
    sub = parser.add_subparsers(dest="cmd")

    p_link = sub.add_parser("link")
    p_link.add_argument("paths", nargs="+")
    p_link.add_argument("--ref", default="")
    p_link.add_argument("--markdown", action="store_true")
    p_link.set_defaults(func=cmd_link)

    p_comment = sub.add_parser("comment")
    p_comment.add_argument("issue", type=int)
    p_comment.add_argument("--body", default="")
    p_comment.add_argument("--body-file", default="")
    p_comment.add_argument("--link", action="append", default=[])
    p_comment.add_argument("--ref", default="")
    p_comment.add_argument("--edit-comment-id", type=int)
    p_comment.add_argument("--dry-run", action="store_true")
    p_comment.set_defaults(func=cmd_comment)

    p_status = sub.add_parser("status")
    p_status.add_argument("issue", type=int)
    p_status.add_argument("--project-status", default="")
    p_status.add_argument("--project-title", default="")
    p_status.add_argument("--issue-state", default="")
    p_status.add_argument("--dry-run", action="store_true")
    p_status.set_defaults(func=cmd_status)

    p_sync = sub.add_parser("sync")
    p_sync.add_argument("issue", type=int)
    p_sync.add_argument("--body", default="")
    p_sync.add_argument("--body-file", default="")
    p_sync.add_argument("--link", action="append", default=[])
    p_sync.add_argument("--ref", default="")
    p_sync.add_argument("--edit-comment-id", type=int)
    p_sync.add_argument("--project-status", default="")
    p_sync.add_argument("--project-title", default="")
    p_sync.add_argument("--issue-state", default="")
    p_sync.add_argument("--close-when-done", action="store_true")
    p_sync.add_argument("--dry-run", action="store_true")
    p_sync.set_defaults(func=cmd_sync)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
