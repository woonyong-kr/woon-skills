---
name: job
description: background job, scheduler, worker, batch, durable workflow의 claim·lease·heartbeat, retry, checkpoint, cancellation, duplicate, partial failure와 운영 재처리를 설계·검증할 때 사용한다.
---

# Job

process lifetime과 업무 workflow lifetime을 분리해 restart 뒤에도 안전하게 이어지게 한다.

1. job identity, input snapshot, 상태 machine, terminal outcome과 owner를 정의한다.
2. [Job 실행 기준](references/execution.md)으로 durable enqueue, claim·lease·fencing, checkpoint, retry·DLQ와 cancellation을 정한다.
3. job effect와 상태 commit은 `$tx`, queue delivery는 `$event`, concurrency·backpressure는 `$capacity`를 함께 적용한다.
4. 변경한 claim·effect·checkpoint·cancel 경계가 영향을 받는 worker kill, lease expiry, duplicate delivery·restart 조건을 골라 재시작 뒤 상태와 업무 효과를 검증한다.

in-memory scheduler와 `sleep`만으로 durable workflow를 주장하지 않는다. 결과에는 상태 전이, 재시작·재처리 계약, progress·age metric과 운영 명령의 안전 경계를 포함한다.
