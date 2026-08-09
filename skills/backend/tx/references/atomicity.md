# 원자성 기준

## 목차

- 불변식과 commit point
- local transaction
- isolation과 동시성
- 여러 system의 일관성
- crash window

## 불변식과 commit point

각 write path에 다음을 명시한다.

| 항목 | 결정 |
| --- | --- |
| invariant | commit된 상태에서 항상 참이어야 하는 식 |
| owner | invariant를 결정하는 use case·aggregate |
| resources | 함께 원자적으로 바뀌는 실제 저장 자원 |
| commit point | caller가 성공으로 간주할 수 있는 순간 |
| unknown | 성공 여부를 알 수 없는 구간과 조회 방법 |
| recovery | retry, compensation, reconciliation 또는 수동 복구 |

ACID는 같은 transaction manager가 지배하는 resource 안에서만 주장한다. DB transaction과 HTTP·email·object storage·다른 DB·broker publish는 기본적으로 하나의 원자적 commit이 아니다.

## local transaction

- transaction boundary를 한 업무 command의 consistency boundary와 맞춘다.
- helper·repository가 임의로 commit하지 않게 한다.
- constraint, unique index, foreign key와 check를 마지막 방어선으로 둔다. 사전 조회만으로 동시성 invariant를 보장하지 않는다.
- transaction callback 전체가 재실행될 수 있으므로 callback 안의 외부 side effect를 제거하거나 멱등화한다.
- commit 실패 전의 반환값과 읽은 값을 외부 성공으로 노출하지 않는다.
- remote I/O 동안 row lock과 connection을 잡지 않는다. 필요하면 lock duration과 pool 고갈을 부하 시험으로 입증한다.

## isolation과 동시성

- `READ COMMITTED`: statement마다 snapshot이 달라질 수 있음을 전제로 lost update·write skew를 별도 방어한다.
- `REPEATABLE READ`·snapshot isolation: 안정된 snapshot이 모든 업무 invariant를 직렬화하지는 않는다.
- `SERIALIZABLE`: 성공한 transaction의 serial order를 보장하지만 serialization failure를 whole-transaction retry해야 한다.
- optimistic concurrency는 version compare와 상태 전이를 한 conditional write로 수행하고 영향 row 수가 1인지 확인한다.
- pessimistic lock은 모든 경쟁 writer가 같은 lock protocol을 사용할 때만 효과가 있다.
- distributed lease는 만료 뒤 늦은 writer를 막지 못한다. correctness가 필요하면 monotonic fencing token을 downstream write에서 검증한다.
- deadlock은 global lock order, 짧은 scope와 bounded whole-transaction retry로 다룬다.

read→판단→write가 하나의 원자적 compare 없이 분리되면 TOCTOU bug로 취급한다.

## 여러 system의 일관성

- DB state와 publish 의도를 함께 보존해야 하면 같은 DB transaction에 outbox row를 쓴다.
- relay는 publish 후 mark 전에 crash할 수 있으므로 duplicate publish를 정상으로 가정한다.
- consumer는 message ID·consumer scope의 inbox 기록과 업무 mutation을 같은 local transaction에 둔다.
- 여러 service의 업무 흐름은 durable state machine으로 상태, 허용 전이, retry와 compensation을 기록한다.
- compensation은 rollback이 아니다. 실패할 수 있는 새 업무 operation이며 멱등성·재시도·감사가 필요하다.
- 되돌릴 수 없는 effect는 실행 전에 예약·확인 단계, 실행 뒤 조회·reconciliation과 운영 escalation을 둔다.

2PC는 모든 participant와 운영 환경이 지원하고 blocking·coordinator failure·latency 비용을 수용할 때만 선택한다.

## crash window

최소 다음 지점에서 process kill·exception·timeout을 주입한다.

1. idempotency claim 전
2. claim 뒤 업무 mutation 전
3. mutation 뒤 idempotency result 저장 전
4. local commit 직전
5. commit 직후 response 전
6. outbox 읽기 뒤 publish 전
7. publish 뒤 sent mark 전
8. consumer effect 뒤 offset·ack 전

각 지점에서 commit된 invariant, replay 결과, duplicate 수, orphan·stuck 상태와 복구 시간을 확인한다.
