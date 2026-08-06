---
name: github
description: >
  GitHub 저장소 작업을 수행합니다. PR, 이슈, CI/CD, 릴리즈, 알림, README 업데이트를
  모두 처리합니다. conventions/ 디렉토리의 규칙을 읽고 적용해서 사용자가 직접 쓴 것과
  동일한 문체와 형식으로 출력합니다. AI 생성 표식, 이모지, 영문 마케팅 문체는 절대 사용하지 않습니다.

  트리거 예시:
  PR — "PR 만들어줘", "PR 목록 보여줘", "PR 머지해줘", "리뷰 요청받은 PR 보여줘",
       "PR에 코멘트 달아줘", "PR 닫아줘", "PR 상태 확인해줘"
  이슈 — "이슈 만들어줘", "버그 이슈 등록해줘", "이슈 목록 보여줘", "이슈 닫아줘"
  CI — "CI 상태 확인해줘", "빌드 실패 확인해줘", "워크플로우 재실행해줘",
       "Actions 목록 보여줘", "워크플로우 트리거해줘"
  릴리즈 — "릴리즈 만들어줘", "릴리즈 노트 작성해줘", "태그 릴리즈해줘"
  알림 — "알림 확인해줘", "GitHub 알림 보여줘", "알림 읽음 처리해줘"
  README — "README 업데이트해줘", "README 변경사항 반영해줘"
---

# GitHub 스킬

GitHub 저장소의 PR, 이슈, CI/CD, 릴리즈, 알림, README를 터미널에서 관리합니다.

## 스크립트 위치

모든 스크립트는 `scripts/` 디렉토리에 있습니다.
실행 전 `cd` 없이 절대 경로나 스크립트 기준 경로로 실행합니다.

```
scripts/
├── common.py        공통 유틸 (직접 실행 불가)
├── gh_pr.py         PR
├── gh_issue.py      이슈
├── gh_actions.py    CI/CD
├── gh_release.py    릴리즈
├── gh_notify.py     알림
└── gh_readme.py     README 업데이트
```

## 컨벤션 규칙

생성 전 반드시 아래 파일을 읽고 규칙을 적용합니다.

- `conventions/style.md` — 어투, 금지 항목 (모든 작업에 공통 적용)
- `conventions/pr.md` — PR 제목/본문 템플릿, 라벨 매핑
- `conventions/issue.md` — 이슈 제목/본문 템플릿
- `conventions/release.md` — 릴리즈 노트 템플릿, 버전 규칙
- `conventions/readme.md` — README 섹션 구조, 자동 업데이트 트리거

## 실행 규칙

- 저장소 정보는 `common.load_config()`가 자동 감지합니다
- 명시적으로 지정하려면 `--repo owner/repo` 인자를 사용합니다
- 출력 포맷: `[완료]` `[오류]` `[안내]` `[경고]` `[목록]`

## PR

```bash
# 목록
python3 scripts/gh_pr.py list [--state open|closed|merged|all]

# 단건 조회
python3 scripts/gh_pr.py get <number>

# 생성 (본문은 conventions/pr.md 템플릿 자동 적용)
python3 scripts/gh_pr.py create --title "feat: 제목" [--base main] [--draft]

# 머지
python3 scripts/gh_pr.py merge <number> [--method squash|rebase|merge]

# 닫기
python3 scripts/gh_pr.py close <number>

# 코멘트
python3 scripts/gh_pr.py comment <number> --body "내용"

# 리뷰 요청받은 PR
python3 scripts/gh_pr.py review-requested
```

## 이슈

```bash
# 목록
python3 scripts/gh_issue.py list [--state open|closed|all] [--label bug]

# 단건 조회
python3 scripts/gh_issue.py get <number>

# 생성 (제목 태그로 라벨 자동 매핑, 본문 템플릿 자동 적용)
python3 scripts/gh_issue.py create --title "[bug] 설명"

# 닫기
python3 scripts/gh_issue.py close <number>

# 코멘트
python3 scripts/gh_issue.py comment <number> --body "내용"
```

## CI/CD

```bash
# 최근 실행 목록
python3 scripts/gh_actions.py list [--limit 10]

# 특정 실행 상태
python3 scripts/gh_actions.py status <run-id>

# 재실행
python3 scripts/gh_actions.py rerun <run-id>

# 워크플로우 트리거
python3 scripts/gh_actions.py trigger <workflow-name> [--ref main]

# 실패한 것만 조회
python3 scripts/gh_actions.py failed
```

## 릴리즈

```bash
# 목록
python3 scripts/gh_release.py list

# 노트 미리보기 (커밋 기반 자동 생성)
python3 scripts/gh_release.py notes <tag>

# 생성
python3 scripts/gh_release.py create <tag> --title "v1.2.0" [--draft]
```

## 알림

```bash
# 미확인 알림 목록
python3 scripts/gh_notify.py list

# 모두 읽음 처리
python3 scripts/gh_notify.py mark-read
```

## README 업데이트

```bash
# 변경된 섹션 미리보기
python3 scripts/gh_readme.py preview

# 자동 업데이트 (변경 감지된 섹션만)
python3 scripts/gh_readme.py update

# 특정 섹션만
python3 scripts/gh_readme.py update --section env|usage|features
```

## 설정

`~/.config/skills/github.env` 파일로 기본 저장소를 설정합니다.

```bash
GITHUB_DEFAULT_OWNER=woonyong-kr
GITHUB_DEFAULT_REPO=my-repo
```

git 저장소 내에서 실행하면 remote URL에서 자동 감지합니다.

레거시 경로 `~/.config/claude-skill/github.env`도 계속 읽지만 새 설정은 `~/.config/skills/github.env`를 사용합니다.
