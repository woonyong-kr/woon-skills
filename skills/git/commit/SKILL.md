---
name: commit
description: Git 커밋을 만들거나 영어 Conventional Commits 메시지를 작성·검토·분리할 때 사용한다. 브랜치 전략, merge, rebase, history 복구는 별도 소유 스킬을 쓴다.
---

# Commit

Woon의 새 커밋은 `type(scope): imperative English subject`를 사용한다. Google의 [CL 설명 원칙](https://google.github.io/eng-practices/review/developer/cl-descriptions.html)과 [release-please](https://github.com/googleapis/release-please)가 지원하는 Conventional Commits 형식을 결합한 공통 기준이다. Conventional Commits를 Google이 만든 규약이라고 설명하지 않는다. 이전 한국어 제목·scope 금지 규칙은 대체하며 과거 커밋은 재작성하지 않는다. 외부 프로젝트에 기여할 때는 그 프로젝트의 명시적 규칙을 확인한다.

1. `git status --short`, `git diff`, 필요하면 `git diff --staged`로 실제 변경을 확인한다.
2. 사용자 변경과 이번 작업을 분리하고, 한 커밋에는 함께 되돌릴 변경만 넣는다.
3. `feat|fix|refactor|docs|test|chore|style|perf|build|ci|revert` 중 결과를 가장 정확히 나타내는 type을 고른다.
4. scope는 실제 변경한 모듈·영역을 짧게 쓰고, 제목은 `preserve`, `remove`, `add` 같은 영어 명령형으로 구체적 결과를 한 줄에 적는다. 끝에 마침표를 붙이지 않는다.
5. 제목만으로 이유·migration·주요 제약이 드러나지 않을 때만 빈 줄 뒤 짧은 영어 본문을 추가한다. 실제 변경·검증 사실만 쓰고 미실행 테스트·배포·성능을 완료로 표현하지 않는다. 호환성을 깨는 변경은 `!`와 필요한 영어 `BREAKING CHANGE:` 설명으로 표시한다.
6. 검증은 `repo://core/standards/code.yaml`, 폴더 역할은 `repo://core/standards/repository-layout.yaml`, README는 `repo://core/standards/documentation.yaml`을 따른다. 규칙을 이 스킬에 복제하지 않는다. 실제 검증 결과와 staged diff를 확인한 뒤 요청 범위의 파일만 commit한다. 메시지 작성 요청을 commit·push·amend·force push 권한으로 확대하지 않는다.

메시지만 요청받으면 복사 가능한 영어 후보 하나를 먼저 준다. 예시와 다른 Git 작업의 소유권은 [참고](references/git-workflow.md)를 필요할 때만 읽는다.
