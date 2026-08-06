"""
gh_actions.py: GitHub Actions / CI 관련 작업

사용법:
  python3 gh_actions.py list [--limit 10]
  python3 gh_actions.py status <run-id>
  python3 gh_actions.py rerun <run-id>
  python3 gh_actions.py trigger <workflow> [--ref main]
  python3 gh_actions.py failed
"""

import argparse
import sys
from common import gh, info, load_config, ok, require_repo, rows, warn

STATUS_KO = {
    "completed": "완료",
    "in_progress": "진행 중",
    "queued": "대기 중",
    "waiting": "대기 중",
}

CONCLUSION_KO = {
    "success": "성공",
    "failure": "실패",
    "cancelled": "취소",
    "skipped": "건너뜀",
    "timed_out": "시간 초과",
    "neutral": "중립",
}


def list_runs(owner: str, repo: str, limit: int = 10):
    data = gh("run", "list",
              "--repo", f"{owner}/{repo}",
              "--json", "databaseId,displayTitle,status,conclusion,createdAt,headBranch",
              "--limit", str(limit))
    if not data:
        info("실행 기록이 없습니다.")
        return
    items = []
    for run in data:
        status = STATUS_KO.get(run["status"], run["status"])
        conclusion = CONCLUSION_KO.get(run.get("conclusion") or "", "")
        state = f"{status} / {conclusion}" if conclusion else status
        items.append(f"{run['databaseId']:<12} {run['displayTitle']:<45} [{state}] ({run['headBranch']})")
    rows(f"워크플로우 실행 목록 (최근 {limit}개)", items)


def get_status(owner: str, repo: str, run_id: int):
    data = gh("run", "view", str(run_id),
              "--repo", f"{owner}/{repo}",
              "--json", "databaseId,displayTitle,status,conclusion,jobs,url")
    status = STATUS_KO.get(data["status"], data["status"])
    conclusion = CONCLUSION_KO.get(data.get("conclusion") or "", "")
    print(f"{data['displayTitle']}")
    print(f"  상태: {status}" + (f" / {conclusion}" if conclusion else ""))
    if data.get("jobs"):
        print()
        print("  Job 목록:")
        for job in data["jobs"]:
            job_status = CONCLUSION_KO.get(job.get("conclusion") or "", STATUS_KO.get(job.get("status", ""), ""))
            print(f"    - {job['name']:<40} [{job_status}]")
    if data.get("url"):
        print(f"\n  {data['url']}")


def rerun_workflow(owner: str, repo: str, run_id: int):
    gh("run", "rerun", str(run_id), "--repo", f"{owner}/{repo}")
    ok(f"워크플로우 #{run_id} 재실행 요청됨")


def trigger_workflow(owner: str, repo: str, workflow: str, ref: str = "main"):
    gh("workflow", "run", workflow,
       "--repo", f"{owner}/{repo}",
       "--ref", ref)
    ok(f"워크플로우 '{workflow}' 트리거됨 (ref: {ref})")


def list_failed(owner: str, repo: str):
    """최근 실패한 워크플로우만 조회한다."""
    data = gh("run", "list",
              "--repo", f"{owner}/{repo}",
              "--status", "failure",
              "--json", "databaseId,displayTitle,createdAt,headBranch",
              "--limit", "10")
    if not data:
        info("최근 실패한 워크플로우가 없습니다.")
        return
    items = [f"{r['databaseId']:<12} {r['displayTitle']:<45} ({r['headBranch']})"
             for r in data]
    rows("실패한 워크플로우", items)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="GitHub Actions 관련 작업")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list")
    p_list.add_argument("--limit", type=int, default=10)

    p_status = sub.add_parser("status")
    p_status.add_argument("run_id", type=int)

    p_rerun = sub.add_parser("rerun")
    p_rerun.add_argument("run_id", type=int)

    p_trigger = sub.add_parser("trigger")
    p_trigger.add_argument("workflow")
    p_trigger.add_argument("--ref", default="main")

    sub.add_parser("failed")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    config = load_config()
    owner, repo = require_repo(config)

    if args.cmd == "list":
        list_runs(owner, repo, args.limit)
    elif args.cmd == "status":
        get_status(owner, repo, args.run_id)
    elif args.cmd == "rerun":
        rerun_workflow(owner, repo, args.run_id)
    elif args.cmd == "trigger":
        trigger_workflow(owner, repo, args.workflow, args.ref)
    elif args.cmd == "failed":
        list_failed(owner, repo)


if __name__ == "__main__":
    main()
