---
name: github-issue-manager
description: >
  GitHub 이슈에 결과 요약 댓글을 남기고, 로컬 코드/문서 경로를 GitHub 링크로 연결하고,
  이슈 상태와 GitHub Project 상태(Todo, In Progress, Done)를 함께 관리합니다.
  이슈 완료 처리, 진행중 변경, 관련 문서 링크 연결, 결과 요약 댓글 작성, 내부 소스코드
  경로 링크 생성, 이슈 자동 정리 작업이 필요할 때 사용합니다. "이슈 상태 바꿔줘",
  "이슈에 결과 정리 댓글 달아줘", "문서 링크를 이슈에 연결해줘", "진행중/완료 처리해줘",
  "이슈 자동 정리해줘" 같은 요청에서 트리거합니다.
---

# GitHub Issue Manager

`gh` CLI 기반으로 GitHub 이슈 댓글, 링크, 상태를 정리하는 스킬이다.

이 스킬의 목적은 두 가지다.

1. 이슈 댓글을 "작업했다" 톤이 아니라 결과 요약 톤으로 남긴다.
2. 댓글 작성과 상태 변경을 GitHub connector가 아니라 로컬 `gh`로 처리해서 `with ChatGPT Codex Connector` 표시를 피한다.

## 언제 쓰는가

- 이슈에 결과 요약 댓글을 달아야 할 때
- 로컬 문서나 소스 파일 경로를 GitHub 링크로 바꿔 이슈에 연결해야 할 때
- 이슈를 `Todo`, `In Progress`, `Done`으로 옮겨야 할 때
- 완료된 이슈를 닫거나, 다시 열어야 할 때
- 작업 결과와 링크, 상태 변경을 한 번에 처리해야 할 때

## 기본 원칙

- 댓글은 "문서 만들어두었습니다", "정리해두었습니다" 같은 보고체보다 결과 요약 중심으로 쓴다.
- 댓글 첫 문장은 결과가 무엇인지 바로 말한다.
- 작업 과정 설명보다 이슈 기준으로 무엇이 정리되었는지, 무엇이 반영되었는지를 적는다.
- 링크는 가능한 한 GitHub blob URL로 남긴다.
- 댓글 작성은 반드시 로컬 `gh` 또는 이 스킬의 스크립트로 처리한다.
- GitHub connector/MCP 코멘트 도구는 사용하지 않는다. 댓글에 via-app 표시가 남기 때문이다.

## 댓글 작성 순서

1. 이슈 제목과 현재 상태를 확인한다.
2. 연결할 로컬 파일과 실제 반영 내용을 확인한다.
3. 결과 요약 2~4줄을 먼저 쓴다.
4. 필요한 경우 핵심 포인트를 2~3개 bullet로 짧게 적는다.
5. 마지막에 `관련 링크` 섹션으로 문서나 코드 링크를 붙인다.

댓글 스타일 예시는 [references/comment-style.md](references/comment-style.md)에 정리되어 있다.

## 빠른 사용법

### 1. 로컬 경로를 GitHub 링크로 만들기

```bash
python3 /Users/woonyong/workspace/skills/github-issue-manager/scripts/issue_manager.py link docs/goal.md
python3 /Users/woonyong/workspace/skills/github-issue-manager/scripts/issue_manager.py link src/main.c:42
```

### 2. 결과 요약 댓글 달기

```bash
python3 /Users/woonyong/workspace/skills/github-issue-manager/scripts/issue_manager.py comment 4 \
  --body-file /tmp/comment.md
```

### 3. Project 상태만 바꾸기

```bash
python3 /Users/woonyong/workspace/skills/github-issue-manager/scripts/issue_manager.py status 4 \
  --project-status done
```

### 4. 댓글 + 링크 + 상태를 한 번에 처리하기

```bash
python3 /Users/woonyong/workspace/skills/github-issue-manager/scripts/issue_manager.py sync 4 \
  --body-file /tmp/comment.md \
  --link docs/checklist.md \
  --project-status done
```

완료와 동시에 이슈를 닫고 싶으면 `--close-when-done`을 추가한다.

## 실무적으로 권장하는 흐름

### 결과 요약 댓글

- 첫 줄에 완료 결과를 쓴다.
- 다음 줄에는 이슈 기준으로 무엇이 반영되었는지 적는다.
- 링크는 마지막에 모은다.

### 상태 변경

- 아직 작업 중이면 `In Progress`
- 결과가 반영됐고 검토만 남았으면 팀 기준에 맞춰 `Done` 또는 그대로 유지
- 정말 끝난 이슈만 닫는다

### 링크 연결

- 문서는 `docs/...`
- 소스는 실제 수정한 `.c`, `.h`, `README.md`
- 필요하면 `:12` 또는 `:12:30` 형식으로 줄 번호까지 붙인다

## 주의할 점

- 현재 git 저장소의 `origin` remote 기준으로 저장소를 찾는다.
- 링크는 기본적으로 원격 기본 브랜치 기준으로 생성한다.
- 절대경로를 넘겨도 저장소 내부 파일이면 자동으로 상대경로로 바꾼다.
- 이슈가 여러 Project에 들어가 있으면 기본적으로 첫 번째 Project를 사용한다.
- 특정 Project만 바꾸려면 `--project-title`을 넣는다.

## 관련 스크립트

- `scripts/issue_manager.py`: 댓글, 링크, 상태 변경 진입점
- `scripts/common.py`: `gh` 래핑, 저장소 감지, GitHub Project 상태 변경 공통 함수

## 추천 요청 예시

- `$github-issue-manager로 이슈 4번에 결과 요약 댓글 달고 docs/checklist.md 링크 연결한 뒤 Done으로 바꿔줘`
- `$github-issue-manager로 이슈 12번을 진행중으로 바꾸고 관련 코드 링크도 같이 정리해줘`
- `$github-issue-manager로 이슈 8번 댓글을 결과 요약형으로 다시 써줘`
