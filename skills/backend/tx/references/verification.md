# Transaction 검증 행렬

## 결정적 검증

| 위험 | 주입·경쟁 | 반드시 확인할 불변식 |
| --- | --- | --- |
| local partial commit | mutation 사이 exception | 전부 commit 또는 전부 rollback |
| response loss | commit 직후 connection drop | 같은 key replay가 effect를 늘리지 않음 |
| payload conflict | 같은 key, 다른 payload | mutation 없이 conflict |
| duplicate race | 같은 key 동시 N개 | logical effect 1개, 동일 terminal result |
| lost update | 같은 version 동시 write | 하나만 성공하거나 serializable retry |
| write skew | 서로 다른 row를 읽고 write | 업무 invariant 보존 또는 한 transaction abort |
| serialization failure | commit conflict | transaction 전체를 처음부터 재실행 |
| relay crash | publish 뒤 sent mark 전 kill | duplicate 허용, consumer effect 1개 |
| consumer crash | effect 뒤 ack 전 kill | redelivery 뒤 effect 1개 |
| stale worker | lease 만료 뒤 이전 worker 재개 | 낮은 fencing token write 거부 |
| remote unknown | provider success 뒤 timeout | 새 effect 없이 조회·reconcile |
| retry amplification | 여러 계층 transient failure | 단일 owner와 총 budget 준수 |

## 테스트 계층

1. pure state-machine test로 모든 허용·금지 전이를 검사한다.
2. 실제 DB integration test로 constraint, isolation과 rollback을 검사한다.
3. 두 개 이상의 실제 connection·thread/process로 race를 만든다.
4. commit·publish·ack 전후에 kill point를 넣고 restart한다.
5. proxy/fake server로 response loss, timeout, duplicate와 reorder를 주입한다.
6. outbox backlog, stuck processing, unknown age와 reconciliation metric을 확인한다.

sleep에 기대지 말고 barrier, latch, advisory lock 또는 deterministic hook으로 순서를 제어한다. mock repository만으로 DB 원자성·isolation을 증명하지 않는다.

## mutation proof

검증기가 실제 버그를 잡는지 최소 mutant를 실행한다.

- key를 retry마다 변경
- key record와 mutation commit 분리
- payload fingerprint 비교 제거
- conditional version 조건 제거
- publish와 DB write를 순차 dual write로 변경
- consumer inbox를 effect와 다른 transaction에 저장
- SDK retry를 켜서 service retry와 중첩
- timeout을 failure로 확정

각 mutant가 예상한 invariant violation으로 실패하고 원본만 통과해야 한다. 실행하지 않은 실제 DB·broker·production 장애는 `unverified`로 보고한다.
