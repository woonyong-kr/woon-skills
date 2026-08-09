---
name: registry
description: woon-skills에서 스킬을 검색·등록·분류·병합·퇴역하고 짧은 이름, source, effect, profile과 Codex·Claude routing을 연결할 때 사용한다.
---

# Registry

`woon-skills`가 canonical이다. `woon resolve repo://skills/catalog.json`으로 root catalog를 찾고 Woon 스킬을 먼저 검색한다. 없을 때만 Codex·Claude의 installed fallback과 vendor를 조사한다.

1. primary trigger, near-miss, owner, effect와 금지 행동을 정의한다.
2. trigger·owner·effect가 모두 같으면 병합하고 하나라도 독립이면 분리한다.
3. routing이 유지되는 가장 짧은 global unique 이름을 고른다. installed 이름과 충돌하면 더 구체화한다.
4. `skills/<domain>/<name>/SKILL.md`, `agents/openai.yaml`과 필요한 한 단계 reference만 만든다.
5. source·derivation, effect·conflict, 최소 profile, profile-resolution, routing과 behavior 사례를 연결한다.
6. root catalog를 재생성하고 `$audit → $budget → $comply`를 통과시킨다.
7. 사용자 승인 뒤 기본 profile에 승격한다. 평가 전용 profile은 Codex·Claude에 설치하지 않는다.

등록·병합·이름 변경·퇴역의 상세 절차는 [등록 계약](references/registration.md)을 읽는다. 퇴역은 먼저 profile과 참조를 이동하고 `archive/`에 보존하며 unmanaged 설치 폴더를 삭제하지 않는다.
