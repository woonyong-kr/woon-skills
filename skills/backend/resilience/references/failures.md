# 분산 실패 기준

## Deadline과 cancellation

- caller의 end-to-end deadline에서 queue·connection·request·recovery 시간을 배분한다.
- 하위 timeout은 남은 deadline보다 짧게 두고 deadline을 전파한다.
- connect, read, idle과 operation timeout의 의미를 분리한다.
- cancellation은 가능한 하위 작업에 전달하되 이미 발생한 remote effect의 rollback으로 간주하지 않는다.

## Retry

- retry owner는 logical intent와 전체 budget을 아는 한 계층만 맡는다.
- validation, auth, business conflict와 permanent failure는 같은 입력으로 retry하지 않는다.
- transient failure만 bounded exponential backoff와 jitter로 retry한다.
- `Retry-After`와 server throttle을 존중하고 attempt·elapsed·final outcome을 관측한다.
- retry budget·token bucket으로 outage 중 증폭을 제한한다.

## 격리와 과부하

- circuit breaker는 dependency failure를 빠르게 드러내는 장치이며 correctness를 보장하지 않는다.
- half-open probe 수와 recovery 조건을 명시한다.
- bulkhead는 tenant, dependency, workload priority 같은 실제 blast radius 단위로 pool·semaphore·queue를 분리한다.
- queue는 반드시 bounded로 두고 overflow에서 reject, shed, defer 중 계약을 정한다.
- critical dependency와 optional enrichment를 분리한다.

## Fallback

- stale data의 최대 age, source, privacy·authorization과 사용자 표시를 정한다.
- empty success, 오래된 권한, 잘못된 가격처럼 의미를 바꾸는 fallback을 금지한다.
- fallback이 primary recovery를 가리거나 SLO를 거짓으로 높이지 않게 별도 metric을 둔다.
- write fallback은 새로운 source of truth를 만들 수 있으므로 명시적 reconciliation 없이는 사용하지 않는다.

## 검증

- latency distribution의 p50뿐 아니라 p95·p99와 deadline 초과를 측정한다.
- dependency 100% failure, 부분 failure, slow response, connection reset과 recovery를 주입한다.
- retry 포함 실제 downstream call 수와 queue depth를 측정한다.
- 한 tenant·dependency 장애가 다른 workload로 전파되지 않는지 확인한다.
- breaker open·half-open·close 전이와 restart 후 상태를 확인한다.
- fallback 결과가 contract와 보안 경계를 보존하는지 negative test를 실행한다.
