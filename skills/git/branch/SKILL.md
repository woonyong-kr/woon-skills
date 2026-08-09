---
name: branch
description: Git 브랜치를 만들고 이름을 정하거나 GitHub Flow, trunk-based, GitFlow, merge와 rebase 전략을 판단할 때 사용한다.
---

# Branch

저장소의 protected branch, CI, release 방식, feature flag, 협업자를 먼저 확인한다.

- 기본은 `main`에서 짧은 `feat/<slug>` 또는 `fix/<slug>` 브랜치를 만든다.
- 공유·push된 branch는 rebase로 history를 바꾸지 않는다.
- merge 방식은 저장소 정책을 따르며, 확실하지 않으면 PR의 허용 방식부터 확인한다.
- 여러 버전 유지와 release train이 실제로 없으면 GitFlow를 도입하지 않는다.
- branch 생성·전환 전 dirty state와 base SHA를 기록한다.

branch 삭제나 강제 갱신은 `$safety`를 함께 적용한다.
