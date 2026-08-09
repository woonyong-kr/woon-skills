---
name: comply
description: 스킬 지침이 실제 agent 행동에서 일관되게 지켜지는지 positive·boundary·negative scenario와 반복 실행으로 평가할 때 사용한다.
---

# Comply

스킬별 핵심 규칙을 observable behavior로 바꾼다. happy path뿐 아니라 충돌 규칙, 잘못된 사용자 입력, 위험한 요청, 도구 실패를 포함한다.

각 case는 prompt, fixture, 기대 행동, 금지 행동, 증거를 가진다. 최소 3회 반복해 outcome과 rationale agreement를 확인한다. keyword 포함만으로 통과시키지 말고 실제 file placement, command, external write 여부를 검사한다.

실패하면 description 문제인지 본문 절차 문제인지 분리해 가장 작은 부분만 고치고 같은 case와 adjacent boundary case를 재실행한다.
