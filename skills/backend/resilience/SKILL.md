---
name: resilience
description: 분산 호출의 timeout, deadline, retry, backoff·jitter, circuit breaker, bulkhead, load shedding, fallback, cancellation과 partial failure를 설계·검증할 때 사용한다.
---

# Resilience

실패를 없앤다고 가정하지 말고 failure mode별로 제한·격리·복구한다.

1. dependency별 latency·availability SLO, failure 분류, 전체 deadline과 결과 불명 가능성을 적는다.
2. [분산 실패 기준](references/failures.md)으로 timeout·retry owner·breaker·bulkhead·fallback을 선택한다.
3. write retry와 unknown result는 `$tx`, queue와 처리량은 `$capacity`, 관측 지표는 `$observe`에 맡긴다.
4. 수정한 deadline·retry·격리·fallback이 영향을 받는 slow dependency·partial outage·retry storm·recovery 조건을 골라 제한과 복구 계약을 검증한다.

모든 오류를 retry하거나 stale fallback으로 숨기지 않는다. 결과에는 failure assumption, budget, 격리 단위, degraded contract, recovery trigger와 실행한 장애 증거를 포함한다.
