---
name: tx
description: transaction, isolation, lock, idempotency, atomic write, retry, outbox·inbox, saga, compensation과 unknown result를 설계·검증할 때 사용한다. 중복 결제·이중 처리·부분 commit 같은 정합성 버그에도 사용한다.
---

# Transaction

원자성의 범위를 annotation이나 함수가 아니라 실제 commit 가능한 resource로 증명한다.

1. 업무 의도, 성공 관찰 시점, 반드시 함께 commit할 state와 별도 system effect를 목록화한다.
2. local transaction·isolation·lock·constraint를 정할 때 [원자성 기준](references/atomicity.md)을 읽는다.
3. retry 가능한 command·timeout·duplicate가 있으면 [멱등성 기준](references/idempotency.md)을 읽는다.
4. 여러 resource, broker, remote API가 있으면 local atomicity와 eventual convergence를 분리하고 outbox·inbox·workflow·compensation·reconciliation 중 필요한 최소 mechanism을 선택한다.
5. 구현 전 [검증 행렬](references/verification.md)에서 해당 failure point를 고르고 정상 경로뿐 아니라 commit 전후 crash, response loss, duplicate와 concurrency를 재현한다.
6. API 표면은 `$api`, event delivery는 `$event`, framework transaction 문법은 해당 언어 skill에 맡긴다.

다음은 허용하지 않는다.

- local rollback이 이미 성공한 remote effect를 취소한다고 주장하기
- idempotency key를 adapter나 매 retry마다 새로 만들기
- key 기록과 업무 mutation을 서로 다른 local commit으로 저장하기
- SDK·adapter·service·job retry를 중첩하기
- timeout·cancellation을 remote 실패의 증거로 처리하기
- `exactly once`를 적용 범위와 failure assumption 없이 주장하기

결과에는 invariant, transaction owner·resource·isolation, idempotency scope·key·fingerprint·state·retention, retry owner·budget, unknown-result recovery, fault-injection 증거와 미검증 범위를 포함한다.
