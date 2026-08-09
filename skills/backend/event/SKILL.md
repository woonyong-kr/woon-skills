---
name: event
description: message broker, domain·integration event, outbox·inbox, at-least-once delivery, duplicate, ordering, partition, consumer retry·DLQ와 schema evolution을 설계·검토할 때 사용한다.
---

# Event

delivery 횟수의 홍보 문구보다 end-to-end 업무 효과를 정의한다.

1. producer, owner, consumer, event identity, ordering key와 성공·ack 시점을 정한다.
2. [전달 계약](references/delivery.md)으로 duplicate, reorder, delay, poison message와 schema 변화의 동작을 확정한다.
3. DB write와 publish 원자성, inbox와 consumer mutation은 `$tx`를 함께 적용한다.
4. event에 필요한 최소 공개 사실만 담고 consumer별 command를 generic event에 섞지 않는다.
5. broker·client의 실제 guarantee와 설정을 version-matched 공식 문서·integration test로 확인한다.

`exactly once`를 broker 내부 범위에서 end-to-end side effect까지 확대하지 않는다. 결과에는 delivery assumption, ordering·partition, dedup scope·retention, retry·DLQ·replay, schema compatibility와 운영 metric을 포함한다.
