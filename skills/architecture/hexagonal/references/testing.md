# 경계 검증 기준

이 문서는 Hexagonal Architecture가 폴더 이름이 아니라 실제 dependency, contract와 runtime behavior로 지켜지는지 검증한다. 경계 생성 기준은 `boundaries.md`, transaction·retry·idempotency 같은 효과 계약은 `effects.md`가 소유한다.

## 목차

- 검증 대상부터 분리하기
- Domain unit test
- Use-case unit test
- Port contract test
- Outbound adapter integration test
- Inbound adapter test
- Composition과 lifecycle test
- Architecture 정적 검사
- Fake와 mock의 한계
- 실패, 시간과 동시성 검증
- Migration 검증
- 실행 환경과 결정성
- 완료 증거와 점검

## 검증 대상부터 분리하기

각 test가 무엇을 증명하고 무엇을 증명하지 않는지 먼저 정한다.

| 검증 층 | 주로 증명하는 것 | 증명하지 않는 것 |
| --- | --- | --- |
| domain unit | invariant, 계산, 상태 전이 | DB·network·serialization |
| use-case unit | orchestration, port 호출, 업무 실패 | 실제 adapter 계약 준수 |
| port contract | 모든 adapter가 공유해야 할 observable behavior | 특정 infra의 운영 성능 |
| adapter integration | driver·SDK·schema·mapping·기술 오류 | 전체 wiring과 사용자 흐름 |
| inbound adapter | parsing, auth context, protocol mapping | 실제 outbound infra |
| composition smoke | concrete wiring, config, scope와 시작 | 장시간 운영·production 상태 |
| end-to-end | 배포된 경로의 대표 사용자 흐름 | 모든 실패 조합과 내부 분기 |

test 개수나 coverage 비율만으로 경계 품질을 판단하지 않는다. 중요한 contract, 실패와 실제 integration이 빠졌는지 확인한다.

## Domain unit test

- framework, database, network, clock과 random을 직접 호출하지 않고 빠르게 실행한다.
- invariant의 정상·경계·거부 사례를 검증한다.
- 상태 전이는 이전 상태, 입력, 새 상태와 발생한 domain event를 함께 확인한다.
- 값 객체의 equality, 단위, rounding, timezone과 validation을 실제 업무 규칙으로 고정한다.
- 순수 계산은 같은 입력에 같은 결과를 내는지 확인한다.
- 구현의 private method 호출 순서보다 public behavior를 검증한다.

domain test가 외부 container, application context 또는 ORM bootstrap을 요구하면 dependency가 안쪽으로 샜는지 조사한다.

## Use-case unit test

use-case test는 consumer 관점의 작은 fake나 spy port로 orchestration을 검증한다.

- 성공 경로에서 필요한 capability, 입력과 호출 순서를 확인한다.
- business rejection, not-found, conflict와 외부 실패가 계약대로 전파·변환되는지 확인한다.
- 실패 전에 수행돼야 할 validation과 실패 뒤 실행되지 않아야 할 write를 확인한다.
- transaction boundary와 여러 port의 업무 순서를 확인하되 ORM API 자체를 mock하지 않는다.
- retry, idempotency와 compensation은 `effects.md`에서 정한 owner의 behavior로 검증한다.
- 불필요한 interaction assertion으로 내부 구현 순서를 고정하지 않는다.

fake가 쉽게 만들어진다는 이유로 production port를 넓히지 않는다. consumer가 실제로 요구하는 contract만 사용한다.

## Port contract test

port contract suite는 port consumer가 소유하며 같은 contract를 주장하는 모든 adapter에 반복 적용한다.

contract에 따라 다음을 포함한다.

- 정상 입력과 결과의 의미
- 단건·복수와 부재 표현
- 중복, cardinality와 uniqueness
- 정렬·pagination·cursor와 안정된 순서
- mutation 뒤 읽기와 visibility 시점
- precision, null, default, 단위와 timezone
- validation, conflict, not-found, transient, timeout과 unknown-result 분류
- idempotency key replay와 payload mismatch
- concurrency/version conflict
- cancellation과 resource cleanup

공통 suite에 adapter 생성 factory와 cleanup hook만 주입한다. 구현별 세부 assertion은 별도 integration test에 둔다.

contract suite를 in-memory fake에도 적용하면 fake의 의미 차이를 조기에 찾을 수 있다. 다만 fake가 통과해도 실제 DB·SDK adapter가 통과했다는 뜻은 아니다.

## Outbound adapter integration test

실제 adapter는 가능한 한 실제 driver와 대표 infrastructure에서 검증한다.

- 지원하는 database, broker, filesystem 또는 provider sandbox의 명시된 version을 사용한다.
- schema와 migration을 production과 같은 경로로 적용한다.
- serialization, mapping, nullable, precision, timezone, encoding과 pagination을 확인한다.
- unique constraint, transaction rollback, isolation과 concurrent update를 확인한다.
- SDK status·exception을 내부 오류로 변환하는 사례를 확인한다.
- timeout, rate limit, disconnect, partial response와 duplicate를 failure injection으로 검증한다.
- test data와 resource를 사례별로 격리하고 성공·실패 뒤 결정적으로 정리한다.
- production credential과 production destination을 사용하지 않는다.

외부 provider sandbox가 실제 운영과 다른 제한을 가지면 그 차이를 미검증 위험으로 기록한다. mock HTTP server 결과를 provider integration 통과로 표현하지 않는다.

## Inbound adapter test

- protocol 입력을 application command·query로 정확히 변환하는지 확인한다.
- 형식 오류는 use case 호출 전에 거부하고 write가 발생하지 않게 한다.
- 인증 결과, tenant, locale, deadline과 correlation context 전달을 확인한다.
- application result와 오류를 status, response, exit code, ack·nack으로 변환하는지 확인한다.
- public schema, field 이름, compatibility와 versioning을 검증한다.
- framework serialization과 content type, encoding을 실제 runtime으로 확인한다.

controller test에서 domain policy를 다시 구현하지 않는다. inbound adapter는 protocol 경계만 검증하고 업무 결과는 use-case test가 소유한다.

## Composition과 lifecycle test

composition smoke test는 production과 같은 wiring code로 application을 시작하고 최소 대표 경로를 호출한다.

- 필요한 port마다 concrete adapter가 정확히 하나 선택되는지 확인한다.
- 잘못된 config와 누락된 credential이 시작 시 명확히 실패하는지 확인한다.
- singleton, request, transaction, job과 tenant scope가 의도대로 분리되는지 확인한다.
- resource가 한 번 생성되고 소유한 경계에서 종료되는지 확인한다.
- shutdown 중 새 작업 차단, in-flight 처리와 flush 순서를 확인한다.
- test replacement가 production composition을 암묵적으로 변경하지 않는지 확인한다.

DI container가 graph를 만들었다는 사실만으로 lifecycle과 thread safety가 검증되지는 않는다. 병렬 request나 tenant fixture로 scope 누출을 확인한다.

## Architecture 정적 검사

import와 build dependency 규칙을 자동 검사한다.

- domain은 application, adapter, framework, ORM과 SDK를 import하지 않는다.
- application은 concrete outbound adapter와 inbound framework를 import하지 않는다.
- adapter는 자신이 구현하는 consumer-owned port를 향해 의존한다.
- composition root만 concrete adapter를 선택·생성한다.
- package/module cycle이 없다.
- forbidden annotation, generated client와 persistence type이 core public contract에 없다.

언어별 package visibility, module graph와 architecture-test 도구는 해당 언어 규칙으로 구현한다. 단순 directory 문자열 검사만 쓰지 말고 실제 compiler/import graph와 함께 확인한다.

## Fake와 mock의 한계

좋은 fake는 contract의 observable behavior를 단순하게 구현한다. 실제 기술을 흉내 내는 별도 제품이 되면 안 된다.

- fake는 absence, duplicate, ordering, conflict와 mutation 의미를 실제 contract와 맞춘다.
- fake의 dictionary나 list 동작을 DB의 transaction, collation, null과 isolation 의미로 가정하지 않는다.
- mock은 caller가 중요한 interaction을 지키는지 확인할 때만 사용한다.
- 모든 method 호출 횟수와 내부 순서를 assertion해 refactor를 막지 않는다.
- SDK·ORM chain을 깊게 mock하지 말고 adapter를 실제 integration으로 검증한다.
- clock, random과 ID generator는 명시적으로 제어해 결정성을 확보한다.

fake와 실제 adapter가 다른 결과를 내면 test를 완화하지 말고 먼저 port contract가 모호한지, fake가 틀렸는지, adapter bug인지 분류한다.

## 실패, 시간과 동시성 검증

- transient failure가 정한 횟수·시간 안에서만 재시도되는지 확인한다.
- permanent와 business failure가 자동 재시도되지 않는지 확인한다.
- 중첩 retry가 없는지 logical operation당 실제 attempt 수를 센다.
- 같은 idempotency key replay가 effect를 반복하지 않고 같은 결과를 주는지 확인한다.
- 같은 key와 다른 payload가 conflict인지 확인한다.
- timeout 뒤 성공 여부 불명 상태와 reconciliation 경로를 확인한다.
- cancellation이 하위로 전달되고 resource가 정리되는지 확인한다.
- max in-flight, backpressure, 입력 순서와 첫 오류·부분 성공 정책을 확인한다.
- optimistic conflict와 duplicate delivery를 병렬 fixture로 반복한다.

시간 test는 실제 장시간 sleep보다 fake clock, controllable server와 bounded deadline을 사용한다. 실제 timeout integration은 별도로 소수 유지한다.

## Migration 검증

기존 code에 port와 adapter를 도입할 때 behavior 변경과 구조 변경을 분리한다.

1. 기존 public behavior와 external calls를 characterization test로 고정한다.
2. 한 vertical slice의 old path와 new path에 같은 fixture를 적용한다.
3. 필요한 경우 shadow read, dual-run 또는 recorded replay로 결과 차이를 비교한다.
4. serialization, DB data, event와 public import compatibility를 확인한다.
5. traffic 전환 기준, rollback 조건과 관측 metric을 정한다.
6. wrapper, alias와 feature flag의 제거 조건과 consumer migration을 기록한다.
7. 한 slice의 parity와 운영 관찰을 확인한 뒤 다음 slice로 이동한다.

dual-write는 새로운 consistency 문제를 만든다. 명시적 idempotency, reconciliation과 rollback 없이 안전한 migration으로 가정하지 않는다.

## 실행 환경과 결정성

- dependency와 runtime version을 manifest·lockfile로 고정한다.
- test는 실행 순서, 이전 process와 local credential에 의존하지 않는다.
- 임시 port, directory, database와 namespace를 충돌 없이 할당한다.
- random seed와 시간은 재현 가능하게 기록하거나 제어한다.
- flaky test는 단순 rerun으로 숨기지 않고 race, 외부 의존과 cleanup 원인을 분류한다.
- CI에서 실행되지 않는 slow·sandbox test는 별도 command와 책임자를 문서화한다.
- production에 write하지 않는 guard를 endpoint, account와 credential 수준에서 둔다.

fixture 자체가 application architecture를 위한 거대한 framework가 되지 않게 한다. 반복되는 실제 setup만 작은 helper로 추출한다.

## 완료 증거와 점검

검증 결과는 다음 형식으로 보고한다.

```text
검증한 contract:
domain·use-case unit:
공통 port contract suite와 적용 adapter:
실제 adapter integration 환경:
inbound protocol:
composition·lifecycle:
architecture import graph:
failure·retry·idempotency·concurrency:
migration parity·rollback:
실행 명령과 결과:
미실행 환경과 잔여 위험:
```

완료 전에 확인한다.

- 각 test가 증명하는 층과 증명하지 않는 층을 구분했다.
- core test가 framework와 external infrastructure 없이 실행된다.
- 모든 실제 adapter가 consumer-owned contract suite를 통과한다.
- fake 통과를 실제 adapter 증거로 대신하지 않는다.
- schema, SDK, serialization과 기술 오류를 실제 integration에서 확인했다.
- production composition과 resource scope를 smoke test했다.
- import graph와 cycle을 compiler·정적 검사로 확인했다.
- transaction, retry, timeout, idempotency와 duplicate의 실패 사례가 있다.
- migration은 representative fixture와 rollback 기준을 갖는다.
- test가 production account나 data에 write하지 않는다.
- flaky rerun과 임의 coverage 수치로 누락된 계약을 숨기지 않는다.
- 실행하지 않은 E2E·provider sandbox·production 관찰을 통과로 표현하지 않았다.
