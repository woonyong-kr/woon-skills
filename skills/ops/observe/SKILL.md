---
name: observe
description: backend의 structured log, metric, distributed trace, correlation, audit signal, SLI·SLO, alert와 dashboard를 설계·검토할 때 사용한다. 부분 실패·재시도·비동기 흐름을 운영에서 추적할 때도 사용한다.
---

# Observe

수집 가능한 모든 신호가 아니라 사용자가 겪는 결과와 운영 결정을 관측한다.

1. 사용자 outcome과 correctness·availability·latency·durability SLI를 정의한다.
2. [관측 계약](references/signals.md)으로 log·metric·trace의 역할, cardinality, privacy와 async context propagation을 정한다.
3. logical operation과 physical attempt, success와 accepted·pending·unknown을 구분한다.
4. alert는 SLO 영향과 즉시 가능한 대응이 있을 때만 page로 만든다.

debug log를 audit log로 대신하지 않는다. 결과에는 signal schema, SLI 계산식·window, trace boundary, alert condition·runbook과 failure injection에서 관측된 증거를 포함한다.
