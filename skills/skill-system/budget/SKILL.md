---
name: budget
description: skill·agent·MCP·rule·profile의 문맥 비용을 기준본과 측정하고 routing·행동 품질을 유지하며 토큰 증가나 절감안을 판단할 때 사용한다.
---

# Budget

추정량과 실제 사용량을 섞지 않는다.

1. 대상 profile, Codex·Claude 실행기, model, tokenizer와 승인본 commit을 기록한다.
2. 항상 노출되는 metadata, 활성화된 본문, 실제 읽은 reference, system·rule·tool schema가 포함된 실행량을 분리한다.
3. 실행기가 제공한 input·cached·output 사용량을 우선하고, tokenizer나 문자 추정은 방법과 오차를 표시한다.
4. 비용 비교가 필요하면 승인본과 후보본을 같은 요청·profile·도구에서 측정한다. 반복 표본이 충분할 때만 p50·p95·증감률과 변동을 보고한다.
5. metadata·본문·동시 활성 skill·MCP toolset 순으로 큰 비용부터 줄인다. 상세 규칙은 조건부 reference로 옮긴다.
6. 확인된 routing·행동 회귀는 토큰 절감으로 상쇄하지 않는다. 불변조건·명확한 입력 계약에 필요한 길이는 보존하고, 실제 품질 향상은 비교 근거가 있을 때만 주장한다.

비교 기준과 검토 임계치는 [측정 계약](references/measurement.md)을 읽는다. 병합·분리와 profile 승격은 `$registry`, 정적 위반은 `$audit`이 소유한다.
