from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def ok(msg: str) -> None:
    print(f"[완료] {msg}")


def info(msg: str) -> None:
    print(f"[안내] {msg}")


def warn(msg: str) -> None:
    print(f"[경고] {msg}")


def err(msg: str) -> None:
    print(f"[오류] {msg}", file=sys.stderr)


def run(cmd: list[str], *, check: bool = True, input_text: str | None = None) -> str:
    result = subprocess.run(
        cmd,
        text=True,
        input=input_text,
        capture_output=True,
    )
    if check and result.returncode != 0:
        err(result.stderr.strip() or "명령 실행 실패")
        sys.exit(1)
    return result.stdout.strip()


def gh(*args: str, input_text: str | None = None) -> dict | list | str:
    output = run(["gh", *args], input_text=input_text)
    if not output:
        return ""
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return output


def load_config() -> dict[str, str]:
    config: dict[str, str] = {}

    env_files = [
        Path.home() / ".config" / "skills" / "github.env",
        Path.home() / ".config" / "claude-skill" / "github.env",
    ]
    for env_file in env_files:
        if not env_file.exists():
            continue
        for raw in env_file.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()

    for key in ("GITHUB_DEFAULT_OWNER", "GITHUB_DEFAULT_REPO"):
        if os.environ.get(key):
            config[key] = os.environ[key]

    owner, repo = detect_remote()
    if owner and repo:
        config.setdefault("GITHUB_DEFAULT_OWNER", owner)
        config.setdefault("GITHUB_DEFAULT_REPO", repo)

    return config


def detect_remote() -> tuple[str | None, str | None]:
    canonical = detect_repo_with_gh()
    if canonical != (None, None):
        return canonical

    try:
        url = run(["git", "remote", "get-url", "origin"])
    except SystemExit:
        return None, None

    if "github.com" not in url:
        return None, None
    path = url.split("github.com")[-1].lstrip("/:").removesuffix(".git")
    parts = path.split("/")
    if len(parts) != 2:
        return None, None
    return canonicalize_repo(parts[0], parts[1])


def detect_repo_with_gh() -> tuple[str | None, str | None]:
    try:
        data = gh("repo", "view", "--json", "owner,name")
    except SystemExit:
        return None, None

    if not isinstance(data, dict):
        return None, None

    owner = data.get("owner", {}).get("login")
    repo = data.get("name")
    if owner and repo:
        return owner, repo
    return None, None


def canonicalize_repo(owner: str, repo: str) -> tuple[str, str]:
    try:
        data = gh("repo", "view", f"{owner}/{repo}", "--json", "owner,name")
    except SystemExit:
        return owner, repo

    if isinstance(data, dict):
        current_owner = data.get("owner", {}).get("login") or owner
        current_repo = data.get("name") or repo
        return current_owner, current_repo
    return owner, repo


def require_repo() -> tuple[str, str]:
    config = load_config()
    owner = config.get("GITHUB_DEFAULT_OWNER")
    repo = config.get("GITHUB_DEFAULT_REPO")
    if not owner or not repo:
        err("저장소를 찾지 못했습니다. git remote 또는 ~/.config/skills/github.env를 확인하세요.")
        sys.exit(1)
    return owner, repo


def repo_root() -> Path:
    return Path(run(["git", "rev-parse", "--show-toplevel"])).resolve()


def default_branch(owner: str, repo: str) -> str:
    output = gh("repo", "view", f"{owner}/{repo}", "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name")
    if isinstance(output, str) and output.strip():
        return output.strip()
    branch = run(["git", "branch", "--show-current"], check=False).strip()
    return branch or "main"


def close_issue(owner: str, repo: str, number: int) -> None:
    run(["gh", "issue", "close", str(number), "--repo", f"{owner}/{repo}"])
    ok(f"이슈 #{number} 닫음")


def reopen_issue(owner: str, repo: str, number: int) -> None:
    run(["gh", "issue", "reopen", str(number), "--repo", f"{owner}/{repo}"])
    ok(f"이슈 #{number} 다시 엶")


def fetch_issue_project_items(owner: str, repo: str, number: int) -> list[dict]:
    query = """
    query($owner:String!, $repo:String!, $number:Int!) {
      repository(owner:$owner, name:$repo) {
        issue(number:$number) {
          projectItems(first:20) {
            nodes {
              id
              project { id title }
              fieldValueByName(name:"Status") {
                __typename
                ... on ProjectV2ItemFieldSingleSelectValue {
                  name
                  optionId
                  field {
                    ... on ProjectV2SingleSelectField {
                      id
                      name
                      options { id name }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """.strip()
    data = gh(
        "api",
        "graphql",
        "-f",
        f"query={query}",
        "-F",
        f"owner={owner}",
        "-F",
        f"repo={repo}",
        "-F",
        f"number={number}",
    )
    return data["data"]["repository"]["issue"]["projectItems"]["nodes"]


def normalize_project_status(status: str) -> str:
    key = status.strip().lower().replace("_", "-").replace(" ", "")
    mapping = {
        "todo": "Todo",
        "to-do": "Todo",
        "할일": "Todo",
        "대기": "Todo",
        "in-progress": "In Progress",
        "inprogress": "In Progress",
        "진행중": "In Progress",
        "done": "Done",
        "완료": "Done",
        "finish": "Done",
        "finished": "Done",
    }
    return mapping.get(key, status)


def update_project_status(
    owner: str,
    repo: str,
    number: int,
    project_status: str,
    project_title: str = "",
) -> None:
    items = fetch_issue_project_items(owner, repo, number)
    if not items:
        warn(f"이슈 #{number}는 연결된 GitHub Project가 없습니다.")
        return

    target = None
    if project_title:
        for item in items:
            if item["project"]["title"] == project_title:
                target = item
                break
    else:
        target = items[0]

    if not target:
        warn(f"Project '{project_title}'를 찾지 못했습니다.")
        return

    field_value = target.get("fieldValueByName")
    if not field_value:
        warn("Status 필드를 찾지 못했습니다.")
        return

    wanted = normalize_project_status(project_status)
    options = field_value["field"]["options"]
    option = next((opt for opt in options if opt["name"].lower() == wanted.lower()), None)
    if not option:
        warn(f"Status 옵션 '{project_status}'를 찾지 못했습니다.")
        return

    mutation = """
    mutation($projectId:ID!, $itemId:ID!, $fieldId:ID!, $optionId:String!) {
      updateProjectV2ItemFieldValue(
        input: {
          projectId: $projectId
          itemId: $itemId
          fieldId: $fieldId
          value: { singleSelectOptionId: $optionId }
        }
      ) {
        projectV2Item { id }
      }
    }
    """.strip()

    gh(
        "api",
        "graphql",
        "-f",
        f"query={mutation}",
        "-F",
        f"projectId={target['project']['id']}",
        "-F",
        f"itemId={target['id']}",
        "-F",
        f"fieldId={field_value['field']['id']}",
        "-F",
        f"optionId={option['id']}",
    )
    ok(f"이슈 #{number} Project 상태를 '{option['name']}'로 변경")
