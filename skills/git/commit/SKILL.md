---
name: commit
description: Git 커밋을 만들거나 커밋 메시지를 작성·검토·분리할 때 사용한다. 브랜치 전략, merge, rebase, history 복구는 각각 별도 스킬을 쓴다.
---

# Commit

저장소의 명시적 convention이 있으면 우선한다. 없으면 `<type>: <한국어 제목>`을 사용하며 scope와 마침표는 쓰지 않는다.

1. `git status --short`, `git diff`, 필요하면 `git diff --staged`로 실제 변경을 확인한다.
2. 사용자 변경과 이번 작업을 분리하고, 한 커밋에는 함께 되돌릴 변경만 넣는다.
3. `feat|fix|refactor|docs|test|chore|style|perf|build|ci|revert` 중 결과를 가장 정확히 나타내는 type을 고른다.
4. 제목은 모호한 `수정·작업·변경·업데이트` 대신 관찰 가능한 결과를 쓴다.
5. 이유, migration, 넓은 영향이 불명확할 때만 한국어 본문을 추가한다.
6. 검증 결과를 확인한 뒤 명시한 파일만 stage하고 commit한다. 요청 없이 push하지 않는다.

메시지만 요청받으면 복사 가능한 한 개의 후보를 먼저 준다. 상세 기준과 예시는 [Git workflow](references/git-workflow.md)를 필요할 때만 읽는다.
