# 경계 효과와 실패 정책

이 문서는 port와 adapter를 지나는 transaction, retry, timeout, idempotency, 동시성, 오류, lifecycle과 관측 계약을 정의한다. 경계 자체의 생성 기준은 `boundaries.md`, 검증 방법은 `testing.md`가 소유한다.

## 목차

- 효과 목록부터 작성하기
- Transaction 소유권
- 여러 시스템의 일관성
- Retry 정책
- Idempotency 계약
- Timeout과 cancellation
- 동시성, 순서와 중복
- 오류 분류와 변환
- 부분 성공과 복구
- Resource lifecycle
- 보안과 관측
- 결정 결과와 완료 점검

## 효과 목록부터 작성하기

구현 전에 use case가 일으키거나 관찰하는 효과를 표로 작성한다.

| 항목 | 반드시 정할 내용 |
| --- | --- |
| 읽기·쓰기 | local memory, DB, filesystem, remote API, message publish 여부 |
| 성공 | caller가 관찰하는 결과와 완료 시점 |
| 실패 | 업무 실패, 기술 실패, timeout과 결과 불명 상태 |
| 원자성 | 함께 성공해야 하는 변경과 독립적으로 복구할 변경 |
| 재시도 | 재시도 주체, 조건, 최대 시도·시간과 backoff |
| 중복 | 같은 업무 의도를 식별하는 key와 replay 결과 |
| 순서 | 입력·처리·발행 순서 보장과 허용 가능한 역전 |
| 수명 | client, connection, transaction, request와 tenant scope |
| 관측 | correlation ID, metric, log와 audit의 소유 경계 |

단순 read처럼 보이더라도 network 호출, cache 갱신, lazy loading과 credential refresh가 있으면 숨은 효과로 기록한다. 이름만 보고 pure operation으로 가정하지 않는다.

## Transaction 소유권

use case는 어떤 업무 변경이 함께 성공해야 하는지 결정한다. adapter는 자신이 소유한 저장소나 broker에서 그 결정을 실행하는 기술 mechanism을 제공한다.

- core contract에는 ORM session, JDBC connection, database transaction object를 노출하지 않는다.
- application이 transaction annotation이나 unit-of-work abstraction을 사용할 때도 업무 원자성의 시작·종료가 한 use case와 일치하는지 확인한다.
- adapter 내부 helper가 임의로 commit해 상위 use case의 원자성을 깨지 않게 한다.
- read-only transaction, isolation level, lock과 optimistic version은 실제 consistency 요구에서 정한다.
- remote network 대기 동안 DB transaction과 row lock을 유지하지 않는다. 불가피하면 lock 시간, timeout과 장애 시나리오를 측정해 근거를 남긴다.
- transaction callback 안에서 재시도될 수 있는 code는 외부 write를 중복 실행하지 않아야 한다.

`transactional`이라는 이름이나 annotation만으로 원자성이 증명되지 않는다. 실제 resource, commit boundary, rollback 대상과 외부 효과를 확인한다.

## 여러 시스템의 일관성

일반 DB transaction 하나로 DB, payment API, email, object storage와 message broker를 모두 원자적으로 만들 수 있다고 가정하지 않는다.

1. 먼저 업무상 반드시 동시 성공해야 하는 state와 나중에 수렴해도 되는 state를 구분한다.
2. local state와 event 발행을 함께 보존해야 하면 transactional outbox를 검토한다.
3. message 중복 수신이 가능하면 inbox 또는 처리 기록과 idempotent consumer를 검토한다.
4. 여러 단계의 업무 흐름은 상태 machine, saga 또는 명시적 workflow로 표현한다.
5. 이미 발생한 외부 효과를 되돌려야 하면 실제 가능한 compensation을 정의한다.
6. 되돌릴 수 없는 효과는 retry보다 reconciliation과 운영 개입 경로를 먼저 설계한다.

outbox, saga와 compensation은 기본 장식이 아니다. 장애 창, 처리량, 지연 허용, 복구 책임과 운영 복잡성이 요구할 때만 선택한다.

## Retry 정책

retry는 실패를 숨기는 기능이 아니라 일시적 실패를 제한된 예산 안에서 다시 시도하는 정책이다.

- 기본 retry owner는 최초 업무 의도, idempotency key와 전체 deadline을 아는 application caller 또는 job runner다. 이때 adapter와 SDK의 자동 retry는 끈다.
- provider 특화 retry를 adapter에 명시적으로 위임할 수는 있다. 이 경우 application은 다시 시도하지 않고 adapter는 실제 attempt 수, elapsed budget과 최종 분류를 반환·관측 가능하게 해야 한다.
- 어느 선택이든 한 요청 경로의 retry owner는 하나다. SDK, adapter, use case와 job runner의 중첩 retry를 허용하지 않는다.
- connection reset, rate limit, 명시적 unavailable처럼 분류된 transient failure만 재시도한다.
- validation, authorization, business conflict와 permanent failure는 같은 입력으로 재시도하지 않는다.
- write는 idempotent contract가 있거나 중복 효과를 검출·복구할 수 있을 때만 자동 재시도한다.
- 최대 시도 횟수뿐 아니라 전체 elapsed-time budget과 호출별 timeout을 함께 정한다.
- bounded exponential backoff와 jitter를 사용하고 서버가 제공한 `Retry-After`를 존중한다.
- queue나 batch에서는 retry가 뒤의 item, partition ordering과 처리량에 주는 영향을 정한다.
- retry exhausted를 원래 cause와 별개의 모호한 오류로 덮지 않는다.

timeout 뒤에는 요청이 전달되지 않았을 수도, 처리 중일 수도, 성공했지만 response만 유실됐을 수도 있다. write 결과가 불명확하면 같은 key로 조회하거나 reconciliation한 뒤 다음 행동을 정한다.

## Idempotency 계약

idempotency는 같은 업무 의도를 여러 번 전달해도 새로운 효과가 반복되지 않는 계약이다.

- key는 adapter가 매 시도마다 새로 만들지 않고 최초 업무 의도를 아는 caller가 생성한다.
- 같은 업무 의도의 retry는 같은 key를 사용하고, 새로운 업무 의도는 새로운 key를 사용한다.
- 같은 key와 다른 canonical payload가 오면 conflict로 거부한다.
- key, payload fingerprint, 처리 상태와 replay할 결과를 업무 mutation과 가능한 한 원자적으로 저장한다.
- `processing`, `succeeded`, `failed`, `unknown` 같은 상태와 각 상태에서 caller가 받을 응답을 정한다.
- key retention과 만료 뒤 replay 의미를 정한다. 보존 기간을 무한으로 가정하지 않는다.
- idempotency가 순서, authorization, 사용 한도나 동시성 문제까지 해결한다고 가정하지 않는다.

자연 key를 쓸지 별도 idempotency key를 쓸지는 충돌 범위와 업무 의도 수명으로 결정한다. hash만 저장할 때는 canonicalization과 collision 위험을 문서화한다.

## Timeout과 cancellation

- 모든 외부 I/O에는 유한한 connect·read·operation timeout 또는 inherited deadline을 둔다.
- 하위 adapter에는 남은 전체 예산보다 긴 timeout을 주지 않는다.
- connect timeout, response timeout과 전체 use-case deadline을 같은 숫자로 뭉개지 않는다.
- cancellation signal은 가능한 하위 호출에 전달하고 resource를 정리한다.
- caller cancellation은 remote side effect가 취소됐다는 증거가 아니다.
- timeout 기본값은 SDK 우연한 값에 맡기지 않고 latency 자료, 사용자 SLO와 upstream budget에서 정한다.

timeout을 줄여 빠르게 실패하는 것과 성공률·중복 위험·부하를 함께 측정한다. 검증 없이 임의의 고정값을 복사하지 않는다.

## 동시성, 순서와 중복

- 최대 in-flight 수, queue 크기와 backpressure 정책을 명시한다.
- 결과가 입력 순서를 보존해야 하는지, 완료 순서여도 되는지 구분한다.
- 첫 실패 시 전체 실패, 부분 성공, best effort 중 기존 contract를 유지한다.
- at-least-once delivery에서는 duplicate와 redelivery를 정상 입력으로 다룬다.
- concurrent write에는 optimistic version, compare-and-set, unique constraint 또는 필요한 lock을 사용한다.
- conflict가 발생했을 때 자동 retry, caller conflict, merge 중 하나를 업무 의미로 정한다.
- unordered collection이나 병렬 scheduler에 의존하는 test 결과를 안정된 계약으로 오해하지 않는다.

병렬화는 효과 의미를 바꿀 수 있다. 독립성이 증명되지 않은 호출을 속도만을 위해 동시에 실행하지 않는다.

## 오류 분류와 변환

내부 실패는 caller가 다음 행동을 결정할 수 있을 만큼만 구체적으로 분류한다.

| 분류 | 예 | 일반적인 caller 행동 |
| --- | --- | --- |
| invalid | 입력 형식·필수 값 오류 | 입력 수정 |
| unauthorized·forbidden | 인증·권한 실패 | 인증 또는 권한 처리 |
| not-found | 계약상 필요한 대상 부재 | 종료 또는 업무별 대안 |
| conflict | version, 중복, 상태 전이 충돌 | 갱신·재조회·사용자 판단 |
| transient | 일시적 network·overload | 예산 안 retry |
| timeout | deadline 초과 | 결과 상태 확인 후 판단 |
| permanent | 지원하지 않는 요청·영구 remote 거부 | retry 없이 수정·중단 |
| cancelled | caller 또는 상위 deadline 취소 | 하위 정리 후 전파 |
| unknown-result | write 성공 여부 불명 | 조회·reconciliation |

- adapter는 vendor exception, status code와 driver error를 내부 분류로 변환한다.
- core는 업무 의미를 알고 있을 때만 기술 실패를 업무 실패로 바꾼다.
- inbound adapter는 내부 오류를 HTTP response, CLI exit code, nack 같은 protocol 결과로 변환한다.
- 원래 cause, operation, retryability와 correlation 정보를 보존한다.
- secret, credential, query parameter와 개인 payload를 public message나 log에 노출하지 않는다.
- 같은 실패를 모든 layer에서 반복 기록하지 않는다. 복구·대응 결정을 소유한 경계에서 한 번 기록한다.
- catch-all로 빈 값, 성공 또는 generic internal error를 반환하지 않는다.

외부 오류 문자열을 parse해 업무 로직을 만들지 않는다. 안정된 code나 type이 없으면 adapter 한곳에 격리하고 contract test로 고정한다.

## 부분 성공과 복구

batch와 multi-step workflow는 `성공/실패` Boolean만으로 충분하지 않을 수 있다.

- item별 결과, 전체 상태와 재실행 가능한 범위를 정의한다.
- 이미 성공한 item을 다시 실행할지 건너뛸지 정한다.
- compensation 실패와 reconciliation 대기 상태를 정상 상태 machine에 포함한다.
- 사용자에게 성공으로 응답하는 시점과 실제 후속 처리가 끝나는 시점을 구분한다.
- dead-letter queue, retry queue와 운영 재처리에는 소유자, 보존 기간과 audit trail을 둔다.
- 수동 복구가 필요하면 안전한 조회, 재시도, 중단과 상태 교정 절차를 제공한다.

부분 성공을 새로 허용하면 API contract, UI 표현, metric과 호출자 로직이 바뀐다. 성능 최적화로 몰래 도입하지 않는다.

## Resource lifecycle

- client, connection pool과 thread-safe immutable configuration은 application scope로 공유할 수 있다.
- request, transaction, job과 tenant별 credential·state는 해당 scope 밖으로 누출하지 않는다.
- singleton adapter에 mutable request context나 tenant state를 저장하지 않는다.
- resource 생성 위치와 close·dispose 책임을 composition root에서 정한다.
- lazy initialization은 첫 요청 latency와 동시 초기화 실패를 검증한다.
- shutdown은 새 작업 수락 중지, in-flight 처리, flush와 resource 종료 순서를 갖는다.

resource scope가 명확하지 않으면 편의를 위해 global singleton으로 만들지 않는다.

## 보안과 관측

- credential은 port method argument와 domain value로 널리 전달하지 않고 보안 경계에서 주입·조회한다.
- 최소 권한, tenant 격리와 outbound destination allowlist를 adapter 설정에 적용한다.
- correlation·trace ID는 흐름을 잇되 업무 idempotency key와 같은 것으로 취급하지 않는다.
- metric은 attempt와 logical operation, success와 unknown result를 구분한다.
- log에는 operation, adapter, latency, retry count와 분류된 오류를 남기되 payload·secret은 redaction한다.
- audit은 누가 어떤 업무 상태를 바꿨는지 기록하며 debug log를 audit log로 대신하지 않는다.

관측 code가 dependency direction을 뒤집거나 domain을 특정 telemetry SDK에 결합시키지 않게 adapter 또는 composition 경계에 둔다.

## 결정 결과와 완료 점검

효과 설계 결과는 다음 형식으로 제시한다.

```text
use case와 외부 효과:
transaction owner와 범위:
여러 시스템 consistency:
retry owner, 조건과 전체 예산:
idempotency key, 상태와 retention:
timeout과 cancellation:
동시성, 순서와 duplicate:
오류 분류와 변환 경계:
부분 성공·compensation·reconciliation:
resource scope와 종료 책임:
관측과 보안:
검증 증거:
미검증 위험:
```

완료 전에 확인한다.

- 각 write의 성공 시점과 결과 불명 상태를 설명할 수 있다.
- transaction scope가 실제 resource와 일치한다.
- remote call을 local transaction처럼 표현하지 않았다.
- retry owner가 하나이고 중첩 retry의 총 시도 수를 계산했다.
- write retry에는 같은 업무 의도를 보존하는 idempotency 계약이 있다.
- timeout과 cancellation 뒤 side effect 상태를 추측하지 않는다.
- concurrency limit, ordering, duplicate와 conflict 정책이 있다.
- vendor 오류가 core나 public contract로 직접 새지 않는다.
- cause를 보존하고 같은 실패를 중복 기록하지 않는다.
- singleton에 request·tenant mutable state가 없다.
- secret 없는 log·metric·audit로 복구 상태를 판단할 수 있다.
- 실행하지 않은 failure injection과 production 복구를 검증했다고 표현하지 않았다.
