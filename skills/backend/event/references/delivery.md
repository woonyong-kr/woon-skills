# Event 전달 계약

## Event identity와 schema

- event ID는 발행 시 한 번 생성하고 redelivery에 유지한다.
- aggregate·stream ID와 monotonic sequence 또는 version으로 gap·reorder를 판별한다.
- 발생 시각과 처리 시각을 구분하고 wall clock만으로 순서를 보장하지 않는다.
- schema에는 type, version, producer contract와 privacy classification을 둔다.
- additive 변경도 consumer가 unknown field를 허용하는지 contract test로 확인한다.
- 삭제·의미 변경은 migration window, dual read/write 또는 새 event type으로 관리한다.

## Producer

- domain commit과 integration event 변환 시점을 분리한다.
- DB state와 publish 의도가 함께 남아야 하면 `$tx`의 outbox 계약을 사용한다.
- relay claim, publish, sent mark는 crash 가능 지점을 갖는다. duplicate publish를 허용하고 idempotent consumer로 귀결한다.
- ordering이 필요하면 같은 업무 stream이 같은 partition/order key를 사용하도록 검증한다.
- producer retry가 broker client retry와 중첩되지 않게 한다.

## Consumer

- ack·offset commit은 업무 mutation이 durable해진 뒤 수행한다.
- message ID와 consumer identity의 inbox record를 업무 mutation과 같은 local transaction에 둔다.
- duplicate는 성공 replay 또는 no-op으로 처리하고 error log 폭주를 만들지 않는다.
- stale sequence는 정책에 따라 무시·보관·reconcile하고 gap은 관측한다.
- retry 가능한 transient failure와 poison/permanent failure를 분리한다.
- DLQ는 무덤이 아니다. owner, 원인, 보존, redrive 조건, schema version과 감사 trail을 둔다.

## 검증

- 같은 message N회 전달
- 순서 역전과 sequence gap
- consumer effect 뒤 ack 전 crash
- relay publish 뒤 mark 전 crash
- consumer 두 개의 같은 partition 경쟁
- schema 구·신 version 혼합
- DLQ redrive 중 재중복
- backlog 증가, lag와 retry storm

검증 결과는 broker 수신 횟수와 business effect 횟수를 별도로 기록한다.
