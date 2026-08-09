---
name: audit
description: 스킬 catalog의 frontmatter, 구조, 중복, source·license, stale reference, trigger 품질과 전체 일관성을 정적 검토할 때 사용한다.
---

# Audit

changed skills부터 빠르게 검사하고 release 전 전체 catalog를 검사한다.

1. `name`과 directory 일치, description 길이·구체성, TODO 잔존
2. link/resource 존재와 한 단계 progressive disclosure
3. duplicated trigger, contradictory procedure, unsafe side effect
4. source URL, commit, license, update policy
5. profile budget, conflict/effect declaration, global name uniqueness
6. absolute local path, secret, 개인 token 포함 여부

정적 통과는 효과 검증이 아니다. 행동은 `$comply`, token은 `$budget`, natural routing은 semantic eval로 별도 확인한다.
