"""
gh_notify.py: GitHub 알림 관련 작업

사용법:
  python3 gh_notify.py list
  python3 gh_notify.py mark-read
"""

import argparse
import sys
from common import gh, info, load_config, ok, rows


def list_notifications():
    data = gh("api", "notifications", "--paginate")
    if not isinstance(data, list) or not data:
        info("미확인 알림이 없습니다.")
        return
    items = []
    for n in data[:20]:
        repo = n.get("repository", {}).get("full_name", "")
        subject = n.get("subject", {})
        ntype = subject.get("type", "")
        title = subject.get("title", "")
        items.append(f"{repo:<35} [{ntype}] {title}")
    rows(f"미확인 알림 ({len(data)}개)", items)


def mark_read():
    gh("api", "notifications", "--method", "PUT", "-f", "read=true")
    ok("모든 알림을 읽음으로 표시했습니다.")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="알림 관련 작업")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("list")
    sub.add_parser("mark-read")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    load_config()  # 설정 초기화

    if args.cmd == "list":
        list_notifications()
    elif args.cmd == "mark-read":
        mark_read()


if __name__ == "__main__":
    main()
