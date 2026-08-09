# Java design reference

## Package and folder design

Gradle/Maven 표준 layout이 있으면 `src/main/java`, `src/test/java`를 유지한다. package는 lowercase dot segments이며 보통 reverse domain 뒤에 bounded context와 feature를 둔다.

예: `com.example.billing.invoice` 안에서 domain model, use case, port가 응집되고 framework adapter는 `...invoice.adapter.persistence`처럼 dependency direction을 드러낸다. 기존 저장소가 layer-first 구조면 요청 없이 전면 이동하지 않는다.

- domain rule: Spring/JPA/HTTP import 없이 domain owner에 둔다.
- application orchestration: use case와 transaction boundary
- inbound adapter: controller, message listener, CLI
- outbound adapter: repository implementation, client, filesystem
- configuration: wiring과 framework bean

`common`, `util`, `manager`, `service` package를 dumping ground로 쓰지 않는다. 공유 코드는 동일한 meaning과 change reason이 증명될 때만 둔다.

## Files and top-level types

public top-level class/interface/record/enum은 같은 이름의 파일 하나에 둔다. private implementation detail은 enclosing type의 nested private type이 읽기 쉬울 때만 둔다. 여러 package가 알아야 하는 type을 convenience 때문에 nested로 숨기지 않는다.

DTO는 transport boundary schema, entity는 persistence model, domain type은 business invariant를 표현한다. 이름만 다른 동일 구조를 모든 layer에 기계적으로 복제하지 않는다. 분리 이유가 serialization, lifecycle, ownership, security 중 무엇인지 명시한다.

## Naming

- class/record/interface/enum/annotation: `PascalCase`
- method/field/local/parameter: `lowerCamelCase`
- constant: `UPPER_SNAKE_CASE`
- package: lowercase, underscore 없음
- boolean: `isActive`, `hasPermission`, `canRetry`, `shouldPublish`
- collection: plural; map은 `usersById`
- unit: `timeoutSeconds`, `sizeBytes`

interface에 습관적으로 `I` prefix를 붙이지 않는다. 구현명 `DefaultX`, `XImpl`보다 실제 strategy나 adapter 의미를 쓴다. `Manager`, `Helper`, `Processor`는 책임이 설명되지 않으면 피한다.

## Member order and placement

repository formatter/Checkstyle가 절대 우선이다. 규칙이 없으면 탐색이 쉬운 순서를 쓴다.

1. static constants
2. static factory methods
3. instance fields
4. constructors
5. public API
6. package-private extension/test seam
7. private helpers
8. nested types

모든 public method를 위로 올리는 기계적 정렬보다 호출 흐름과 책임 응집을 유지한다. field는 가능하면 `private final`, constructor injection을 사용하되 framework requirement를 따른다.

method는 state invariant를 다루는 owner type에 둔다. 여러 entity를 조정하거나 I/O transaction을 여는 동작은 application service/use case에 둔다. getter에 network/DB I/O를 숨기지 않는다.

## Class, record, enum, interface

class:
- mutable lifecycle, identity, encapsulated invariant 또는 framework contract가 있음

record:
- immutable value carrier이고 record component가 공개 contract가 되어도 됨
- ORM proxy, mutable lifecycle, hidden derived field가 필요하면 신중히 선택

enum:
- 닫힌 finite set이며 새 값 추가가 모든 consumer에 의미가 있음
- 외부 공급자 문자열 전체를 무조건 enum으로 만들지 않음

interface:
- consumer가 필요한 behavior contract
- 두 구현을 만들기 위한 형식적 layer가 아니라 실제 boundary
- interface와 implementation을 같은 package에 자동으로 쌍으로 만들지 않음

abstract class는 shared state/lifecycle과 template contract가 동시에 있을 때만 쓴다. composition으로 충분하면 inheritance를 피한다. sealed hierarchy는 domain의 닫힌 variant가 실제로 보장될 때 사용한다.

## Visibility

기본은 가장 좁은 visibility다.

- `private`: type 내부 구현
- package-private: 같은 feature/package 협력과 test seam
- `protected`: 의도된 subclass extension contract가 있을 때만
- `public`: 다른 package가 의존해야 하는 stable API

test 편의를 위해 production member를 public으로 넓히지 않는다. package placement나 observable behavior test를 검토한다.

## Methods and errors

method name은 verb 또는 query를 나타낸다: `calculateTotal`, `findInvoice`, `isExpired`. `get`은 값 반환인지 I/O 조회인지 애매하면 domain verb로 구분한다.

parameter가 많다고 무조건 builder를 만들지 않는다. 입력이 stable command/value concept인지 먼저 판단한다. `Optional`은 return absence 표현에 주로 쓰고 field/parameter 사용은 repository convention을 따른다. `null` contract는 annotation과 validation 정책으로 일관되게 처리한다.

domain exception은 business failure를, adapter exception은 기술 failure를 표현한다. boundary에서 cause를 보존해 의미 있는 exception으로 변환한다. catch 후 log하고 다시 같은 exception을 던져 duplicate log를 만들지 않는다.

## Consistency repair

1. current public API와 package consumers를 찾는다.
2. characterization test 또는 compiler boundary를 확보한다.
3. type/method 하나씩 move 또는 rename한다.
4. package-private/public 변화와 serialization/reflection/JPA 영향을 확인한다.
5. formatter, compile, static analysis, unit/integration test를 실행한다.
