---
name: registry
description: woon-skills에 새 스킬을 등록·분류·병합·vendor 고정·profile 연결하거나 짧은 이름과 natural-language trigger를 설계할 때 사용한다.
---

# Registry

`woon-skills`가 canonical이다. 먼저 기존 catalog와 installed fallback에서 같은 trigger·procedure·side effect를 검색한다.

- 위치: `skills/<domain>/<short-name>/SKILL.md`
- 이름: global unique, 보통 한 단어, 사용자가 자연스럽게 부를 가장 짧은 명사·동사
- description: 무엇을 하는지와 언제 쓰는지를 180자 이내로 구체화
- 본문: 실행 절차와 decision gate만 유지
- 상세 규칙: 실제로 필요할 때만 여는 한 단계 `references/`
- 분리: trigger나 side effect가 독립될 때
- 병합: 같은 요청에서 항상 함께 필요하고 owner·effect가 같을 때
- vendor: 내용 수정 없이 commit lock; 유용한 부분은 출처를 기록해 Woon skill로 재작성

등록 후 source lock, effects, profile, profile-resolution eval, semantic routing case를 함께 갱신한다. `$audit`, `$comply`, `$budget`을 통과하기 전 기본 profile에 넣지 않는다.
