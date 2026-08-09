---
name: audit
description: 스킬 catalog의 규격, metadata, 중복, source·license, reference, profile·effect·routing 연결과 안전 위반을 정적으로 검사할 때 사용한다.
---

# Audit

변경 스킬을 먼저 검사하고 release 전 전체 catalog를 검사한다. 결정적 검사를 의미 평가보다 우선한다.

1. Agent Skills 규격과 Woon의 `name`·directory·description 제약을 검사한다.
2. `agents/openai.yaml`의 display name, 한국어 설명과 `$skill`을 포함한 기본 요청을 검사한다.
3. 깨진 link, 한 단계 reference, 중복 name·description·본문, TODO와 stale 경로를 검사한다.
4. source URL·확인 commit·license·채택 방식과 vendor 불변성을 검사한다.
5. effect·conflict·profile·profile-resolution·routing·behavior 연결을 검사한다.
6. secret, 개인 절대 경로, raw private prompt, generated file 직접 편집과 무단 외부 효과를 검사한다.
7. 결과를 `error`, `warning`, `advisory`로 나누고 파일·필드·수정 조건을 제시한다.

전체 항목과 등급은 [검사 계약](references/checks.md)을 읽는다. 정적 통과는 효과 검증이 아니다. 행동은 `$comply`, 토큰은 `$budget`, 자연어 선택은 routing eval로 별도 확인한다.
