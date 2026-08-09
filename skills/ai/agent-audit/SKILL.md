---
name: agent-audit
description: LLM·agent application의 prompt, context, memory, retrieval, tool, repair·retry, renderer와 persistence 층에서 정확도 저하·숨은 호출·출력 변조의 원인을 진단할 때 사용한다.
---

# Agent Audit

모델이나 persona를 바꾸기 전에 wrapper가 입력·행동·출력을 어떻게 바꾸는지 증명한다.

1. 같은 입력과 model 설정으로 direct model 기준본과 실제 application replay를 비교한다.
2. 조립된 context의 출처·순서·digest, model 원문, tool 요청·결과, validation 실패, retry·repair, renderer 전후와 최종 응답을 하나의 trace로 연결한다. secret과 private payload는 redaction한다.
3. 필수 tool·권한·인자·후조건은 prompt가 아니라 schema와 실행 코드에서 강제한다.
4. structured output은 parse→schema→업무 의미 순으로 검증한다. deterministic repair만 먼저 적용하고 LLM 재호출은 새 inference로 기록하며 횟수·비용·변경 내용을 숨기지 않는다.
5. memory는 assistant 주장을 자동 정본화하지 않는다. provenance·scope·검증 상태·정정 관계·만료를 보존하고 사용자 정정과 현재 원문을 우선한다.
6. renderer와 transport는 원문을 보존하고 변환 diff를 남긴다. 링크·JSON·Markdown의 의미를 조용히 바꾸지 않는다.
7. finding은 증상→변조 층→메커니즘→근거→재현→가장 작은 code-first 수정 순으로 제시한다.

prompt 강화만으로 숨은 repair, memory 오염, tool 강제 실패와 renderer 변조를 해결했다고 판정하지 않는다. 층별 진단이나 보고 형식이 필요할 때만 [진단 기준](references/layers.md)을 읽는다.
