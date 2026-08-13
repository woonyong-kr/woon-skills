---
name: novel-handoff
description: 소설의 현재 맥락을 다른 AI로 이어갈 때 사용한다. 기본 local-full 또는 외부용 de-identified 모드로 정본·연표·인물 상태·미해결을 구분한 붙여넣기용 인계 프롬프트를 만든다.
---

# Novel Handoff

1. 기본값은 `local-full`이다. 외부 AI·공유 환경이면 반드시 `de-identified derived context`로 전환하고, 경계가 불명확하면 외부용으로 간주한다.
2. 단일 inventory/catalog로 범위를 고르고 필요한 파일만 읽기 전용으로 확인한다. 기본 범위는 현재 입구·작업 문서·불변 원본이며, 이전 이관본·Git 이력 보존본은 복구 또는 판본 비교가 필요한 경우에만 명시적으로 연다. 원문은 수정·복제하지 않고 revision과 빠진 자료를 기록한다.
3. 사건을 선형 연표에 놓고 `사실·해석·허구·감정·결정·미해결`을 섞지 않는다. 실존 인물의 의도·감정은 직접 근거가 없으면 사실로 쓰지 않는다.
4. 인계 계약의 역할별로 정보를 한 번씩만 넣어 붙여넣기용 prompt를 만든다.
5. 기본 출력은 핵심 packet 하나로 제한한다. 실제 tokenizer가 있으면 1,200 token, 없으면 `3,600자 이하 추정`을 목표로 하고, 넘는 증거는 중복 없는 선택형 부록으로 분리한다. 분량 때문에 미해결·금지 조건·출처 경계를 버리지 않는다.
6. 외부용에는 식별자·원문·media·정확한 날짜·재식별 단서를 넣지 않는다. `local-full`도 private/local-only와 최소 범위를 지킨다.
7. 프롬프트를 만들어 보여 주는 것까지만 수행한다. 외부 MCP를 쓰지 않고 요청 없이 저장·전송·정본 병합·commit·publish하지 않는다.

packet 필드와 누락·토큰 판정은 [인계 계약](references/handoff-contract.md)을 읽는다. 정본 반영은 `$novel-merge`, 일반 회고는 `$insight`, 지식 저장은 `$archive`, 관계도는 `$diagram`이 소유한다. 단일 원본은 `repo://skills/skills/novel/novel-handoff`다.
