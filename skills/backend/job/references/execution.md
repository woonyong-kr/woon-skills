# Job 실행 기준

## Durable lifecycle

```text
queued -> claimed -> running -> succeeded
                    |       -> failed-terminal
                    |       -> retry-wait -> queued
                    |       -> cancelling -> cancelled
                    -> unknown/reconcile
```

- enqueue acknowledgement 전에 durable record가 존재해야 한다.
- job ID와 business intent ID를 구분하고 같은 intent 중복 enqueue를 멱등화한다.
- input은 실행 시 다시 조회할지 immutable snapshot을 저장할지 업무 의미로 정한다.
- status update와 business effect의 transaction·reconciliation 경계를 명시한다.

## Claim·lease·checkpoint

- atomic conditional claim으로 한 active owner를 고르고 lease owner·expiry·attempt를 저장한다.
- heartbeat 지연과 clock assumption을 명시한다.
- lease 만료 뒤 늦은 worker write에는 monotonic fencing token을 검증한다.
- checkpoint는 재실행 가능한 최소 단위 뒤에 원자적으로 저장한다.
- chunk를 작게 하는 것과 external rate·transaction overhead를 workload로 비교한다.

## Retry·cancel·operation

- failure를 transient, permanent, poison, cancelled, unknown으로 분류한다.
- retry는 bounded attempt뿐 아니라 elapsed deadline과 backoff·jitter를 가진다.
- cancellation은 cooperative하고 이미 commit된 effect를 자동 rollback하지 않는다.
- manual retry·skip·cancel·state correction은 authorization, dry-run, expected version과 audit을 갖춘다.
- deploy shutdown은 새 claim 중지→in-flight checkpoint/lease handoff→resource close 순으로 수행한다.

## 검증

- claim 직후, effect 직후, checkpoint 직전·직후 worker kill
- lease 만료와 old worker 재개
- 같은 job·intent duplicate delivery
- retry 중 deploy와 schema version 변경
- partial batch 실패와 resume
- cancellation과 terminal commit 경쟁
- poison job이 partition·queue를 막는 상황

완료 수뿐 아니라 queue age, run age, attempt, lease expiry, stuck state, duplicate suppression과 reconciliation latency를 관측한다.
