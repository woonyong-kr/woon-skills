# 관측 계약

## Signal 역할

- metric: rate, distribution, saturation과 SLO를 bounded cardinality로 집계한다.
- trace: 한 logical flow의 service·queue·DB dependency와 critical path를 연결한다.
- log: 특정 사건의 진단 context와 분류된 원인을 구조화한다.
- audit: 누가 어떤 권한으로 어떤 업무 state를 바꿨는지 tamper-evident하게 기록한다.

같은 정보를 세 signal에 그대로 복사하지 않는다. trace ID는 correlation이고 idempotency key·user identity가 아니다.

## 공통 필드

- service, operation, outcome, error class, duration
- trace/span correlation과 deployment version
- tenant·user는 raw 값 대신 승인된 pseudonymous identifier
- logical operation ID와 attempt number
- async message ID, consumer group과 processing outcome

payload, token, credential, full query와 개인정보는 기본적으로 기록하지 않는다. high-cardinality ID를 metric label로 넣지 않는다.

## SLI·SLO

- availability는 server 2xx 비율만이 아니라 valid request의 유효한 업무 결과로 정의한다.
- latency는 성공·실패·async accepted를 구분하고 percentile과 측정 지점을 명시한다.
- async flow는 end-to-end age, backlog와 deadline 내 완료 비율을 본다.
- correctness·duplicate·stale result 같은 data SLI를 infrastructure health와 분리한다.
- SLO window, 포함·제외 조건, data source와 missing telemetry 처리를 고정한다.

## Alert와 검증

- symptom 기반 multi-window burn-rate를 우선하고 원인 metric은 진단에 쓴다.
- alert마다 owner, severity, runbook, silence·escalation과 복구 조건을 둔다.
- instrumentation 실패가 service 성공으로 집계되지 않게 한다.
- trace sampling이 오류·느린 요청과 rare unknown result를 잃지 않는지 확인한다.
- dependency timeout, retry, queue redelivery와 partial outage를 주입해 signal이 실제 원인과 사용자 영향을 드러내는지 검증한다.
