# Port와 Adapter 경계 기준

이 문서는 interface, port와 adapter를 만들거나 제거할 때 사용하는 언어 중립 기준이다. transaction, retry, idempotency와 오류 변환 정책은 별도 effect 기준이 소유하고, contract·integration test의 상세 방법은 별도 test 기준이 소유한다.

## 목차

- 핵심 구분
- 결정 순서
- 경계 수준 선택
- Port 생성 조건
- Port 소유권
- Inbound와 outbound
- Contract 설계
- Adapter 책임
- 경계 타입과 변환
- Wiring과 배치
- 기존 코드 정리
- 금지 패턴
- 결정 결과와 완료 점검

## 핵심 구분

| 개념 | 의미 | 반드시 코드 타입인가 |
| --- | --- | --- |
| application core | 업무 정책과 use case가 있는 내부 | 아님 |
| port | 내부와 외부가 나누는 목적 있는 대화 또는 capability | 아님 |
| interface | 언어가 제공하는 추상 계약 선언 | port를 표현할 수 있지만 같은 개념은 아님 |
| adapter | 외부 기술·protocol과 port 계약을 서로 변환하는 구현 | 보통 코드 module·class·function |
| wrapper | 다른 API를 감싸 호출 형태를 바꾸거나 사용을 제한하는 얇은 구현 | port나 adapter일 수도, 아닐 수도 있음 |
| facade | 여러 내부 기능을 하나의 단순한 진입점으로 제공 | 외부 기술 경계를 뜻하지 않음 |
| gateway | 외부 subsystem을 domain capability로 표현한 outbound 경계 | port 이름이나 adapter 역할로 사용 가능 |
| repository | aggregate·domain object의 저장과 조회를 표현하는 outbound 경계 | 모든 table·CRUD에 적용하지 않음 |

port가 존재해도 별도의 `interface` 선언이 필요하지 않을 수 있다. 함수 signature, protocol, structural type 또는 module API로 충분하면 가장 작은 표현을 사용한다. 반대로 이름이 `Adapter`나 `Repository`라고 해서 실제 port가 생기는 것은 아니다.

## 결정 순서

다음 순서를 건너뛰고 폴더나 interface부터 만들지 않는다.

1. use case가 보장할 업무 결과와 실패를 한 문장으로 적는다.
2. 대화에 참여하는 actor·system과 누가 상호작용을 시작하는지 적는다.
3. core가 외부에 요구하거나 외부에 제공하는 capability를 기술 이름 없이 적는다.
4. 현재 core로 새는 framework·ORM·SDK·protocol 타입을 찾는다.
5. 경계가 없을 때 함께 바뀌는 코드와 독립적으로 바뀌어야 하는 코드를 구분한다.
6. `직접 사용`, `adapter만`, `명시적 port + adapter` 중 가장 작은 수준을 선택한다.
7. port가 필요하면 실제 consumer와 최소 contract를 정한다.
8. adapter의 변환 책임과 composition 위치를 정한다.
9. 공개 import, 직렬화, reflection, DI와 저장된 데이터 호환성을 확인한다.
10. import graph와 경계별 test로 결정이 실제로 지켜지는지 확인한다.

결정 근거로 `테스트하기 쉽다`, `느슨하게 결합된다`, `확장 가능하다`만 쓰지 않는다. 어떤 consumer, 기술 누출, 변경 축, 대체 구현 또는 실패 계약 때문에 경계가 필요한지 적는다.

## 경계 수준 선택

### 직접 사용

다음을 모두 만족하면 별도 port와 adapter 없이 concrete dependency를 직접 사용할 수 있다.

- 업무 정책이 아니라 application edge 또는 composition code에서만 사용한다.
- 외부 타입이 domain과 use case contract로 퍼지지 않는다.
- 변환, 오류 의미 변경, lifecycle 조정과 protocol 격리가 필요 없다.
- 변경 시 함께 수정할 호출자가 좁고 같은 소유자 안에 있다.
- 대체 구현이나 isolated core test가 현재 요구되지 않는다.
- 같은 application edge에서 configuration으로 library 하나를 고를 뿐, 공통 내부 표현이나 독립 contract가 필요하지 않다.

직접 사용은 기본값이 아니라 확인된 작은 경계의 선택이다. 외부 dependency가 core 여러 곳으로 확산되면 다시 판단한다.

### Adapter만

다음과 같으면 기술 격리를 위한 concrete adapter·module·function을 만들되 별도 interface 선언은 생략할 수 있다.

- 외부 SDK·ORM·protocol 형식을 내부 값으로 변환해야 한다.
- 호출자가 하나이거나 같은 feature 안에서 함께 변경된다.
- 언어의 함수 signature나 structural contract만으로 사용 형태가 충분히 명확하다.
- 대체 구현을 runtime에 선택하거나 여러 consumer가 공유하는 독립 contract가 없다.

configuration 분기나 library method 전달만으로 adapter라고 부르지 않는다. 호출자가 의존하는 안정된 내부 입력·출력·오류 의미가 있고, 각 기술 구현이 그 계약으로 실제 변환할 때 adapter가 된다. 그런 변환이 없으면 edge의 직접 사용이나 작은 private function으로 유지한다.

application이 concrete adapter를 직접 의존하면 완전한 dependency inversion은 아니다. 그 trade-off가 작은 코드와 낮은 변경 위험보다 큰지 확인한다.

### 명시적 Port와 Adapter

core가 외부 기술과 독립적으로 capability를 요구하거나 제공하고, 그 계약을 별도 검증·구현·교체해야 하면 명시적 port를 둔다. adapter는 port를 구현하고 외부 기술에 의존한다.

구현체 수만으로 결정하지 않는다. 구현체 하나여도 기술 누출과 독립 변경 경계가 실제라면 port가 필요할 수 있고, 구현체가 여러 개여도 core가 그 차이를 소비하지 않으면 하나의 interface로 묶을 이유가 없을 수 있다.

## Port 생성 조건

다음 질문 중 첫 번째와 나머지 하나 이상에 `예`일 때 port 후보가 된다.

1. core가 이 capability를 업무 또는 use case 언어로 요구하거나 외부에 제공하는가?
2. 외부 SDK·ORM·framework·protocol 타입을 core contract에서 제거해야 하는가?
3. 현재 둘 이상의 실제 adapter가 같은 consumer contract를 만족해야 하는가?
4. test adapter나 fake가 단순 mock 편의를 넘어 core를 외부 장치 없이 실행하게 하는가?
5. dependency가 core와 다른 변경 주기, 배포, 장애, 보안 또는 lifecycle 경계를 가지는가?
6. 같은 capability를 HTTP·CLI·message·batch처럼 둘 이상의 driving adapter가 호출하는가?
7. contract test를 여러 구현에 동일하게 적용해야 하는가?

다음 이유만으로는 port를 만들지 않는다.

- 모든 dependency에는 interface가 있어야 한다는 관례
- 미래에 구현체가 늘어날 수 있다는 추측
- mock framework로 대체하기 편하다는 이유만 있음
- class 이름에 `Service`, `Repository`, `Client`가 붙어 있음
- 외부 library의 method를 그대로 한 번 전달함
- 폴더 대칭이나 architecture diagram을 완성하려는 목적
- 구현체 둘의 method 모양이 우연히 비슷함

test seam은 실제로 중요한 판단 근거지만 production contract를 test double의 편의에 맞추지 않는다. 먼저 consumer가 필요로 하는 capability를 정하고 fake가 그 계약을 따르게 한다.

## Port 소유권

port는 구현체가 아니라 가장 안쪽의 실제 consumer가 소유한다.

- inbound port: 외부 actor가 호출하는 application use case 계약이며 application이 소유한다.
- outbound port: use case가 외부에 요구하는 capability이며 보통 application consumer가 소유한다.
- domain port: domain policy 자체가 외부 capability를 업무 개념으로 요구하고 application orchestration으로 분리할 수 없을 때만 domain이 소유한다.
- shared port: 여러 consumer가 동일한 의미와 변경 이유를 실제로 공유할 때만 공통 core 위치에 둔다.

adapter, database module 또는 SDK package가 port를 소유하지 않는다. 구현체가 필요한 method를 contract에 추가하지 말고, consumer의 사용 사례가 추가될 때 contract를 변경한다.

하나의 큰 port를 여러 consumer가 일부씩 사용하면 consumer별 capability로 분리한다. 단, 같은 업무 대화를 인위적으로 method 하나씩 쪼개 수십 개의 port를 만들지 않는다. 다음이 같으면 하나의 port로 유지할 수 있다.

- consumer와 사용 목적
- 변경 이유
- lifecycle과 실패 의미
- 구현 및 contract test 대상

## Inbound와 Outbound

inbound·outbound는 data가 들어오고 나가는 방향이 아니라 누가 대화를 시작하고 제어하는지로 구분한다.

- inbound: 사용자, HTTP client, CLI, scheduler, queue consumer가 application을 깨운다.
- outbound: application이 database, remote API, filesystem, publisher, clock 같은 외부 capability를 호출한다.

HTTP response가 밖으로 나가도 HTTP controller는 inbound adapter다. Webhook payload가 application 안으로 들어와도 application이 먼저 subscription이나 callback을 요청하고 protocol lifecycle을 소유한다면 전체 대화의 제어 방향을 추가로 확인한다.

하나의 외부 system이 use case에 따라 inbound와 outbound 역할을 모두 할 수 있다. system 이름만으로 한쪽에 고정하지 않는다.

## Contract 설계

port contract는 기술 기능 목록이 아니라 consumer가 수행하려는 대화를 표현한다.

1. 이름은 SQL, HTTP, Kafka, Stripe 같은 기술보다 업무 capability를 우선한다.
2. method는 확인된 use case가 실제로 호출하는 것만 포함한다.
3. 입력·출력은 domain 또는 application이 소유하는 값으로 표현한다.
4. ORM entity, database row, HTTP request/response, SDK result와 framework context를 노출하지 않는다.
5. 단건·복수, 부재, 순서, pagination과 mutation 의미를 명시한다.
6. 동기·비동기, cancellation과 streaming을 구현 세부로 숨기지 않는다.
7. 호출이 write, remote I/O 또는 외부 공개를 일으키면 계약에서 확인 가능해야 한다.
8. 오류, timeout, retry, idempotency와 transaction 의미는 effect 기준으로 확정한다.
9. 구현체별 선택 기능을 base port에 optional method로 누적하지 않는다.
10. generic CRUD interface를 기본으로 만들지 않는다. use case가 요구하는 capability를 표현한다.

예시:

- `DatabasePort.executeSql(query)`보다 `OrderRepository.findPendingOrders(cutoff)`
- `PaymentClient.call(payload)`보다 `PaymentAuthorizer.authorize(payment)`
- `StorageService.save(data)`보다 실제 소비 의미에 맞는 `DocumentArchive.archive(document)`

단, domain-specific method가 adapter 안에 query policy와 업무 규칙을 중복시키지 않게 한다. 무엇을 조회할지는 consumer가 정하고, SQL·protocol로 어떻게 실행할지는 adapter가 정한다.

## Adapter 책임

inbound adapter는 다음을 담당한다.

- protocol·framework 입력 읽기
- 형식 parsing과 transport-level validation
- 인증 결과와 request context를 application 입력으로 변환
- inbound port 호출
- application 결과와 오류를 protocol response·exit code·ack로 변환

outbound adapter는 다음을 담당한다.

- application 값을 SDK·ORM·protocol 입력으로 변환
- 외부 호출 실행
- 외부 결과를 application 값으로 복원
- 기술 오류를 분류 가능한 내부 실패로 변환
- 기술별 timeout, connection과 resource 사용을 effect·lifecycle 정책에 맞게 적용

adapter는 다음을 소유하지 않는다.

- 여러 use case의 업무 순서
- domain invariant와 가격·권한·상태 전이 정책
- 다른 adapter를 직접 호출하는 workflow
- consumer가 요청하지 않은 generic capability
- 외부 row·payload를 그대로 반환해 core에 mapping 책임 전가

여러 adapter의 호출 순서와 성공 조건은 use case가 소유한다. adapter가 다른 adapter를 호출해야 한다면 실제로 하나의 외부 subsystem을 캡슐화하는 내부 구현인지, application workflow가 잘못 내려간 것인지 확인한다.

## 경계 타입과 변환

필드가 같다는 이유만으로 transport DTO, command, domain value와 persistence row를 하나로 공유하지 않는다. 반대로 계층마다 동일한 type을 기계적으로 복사하지도 않는다.

다음 중 하나가 다르면 경계 타입을 분리한다.

- 허용 입력과 validation
- 보안·노출 가능한 field
- nullable·default·단위와 시간대
- identity와 lifecycle
- 직렬화·versioning
- 오류와 부분 값 허용 여부
- 소유자와 변경 주기

차이가 없고 같은 소유자와 계약을 공유하면 내부 type을 재사용할 수 있다. 변환 함수는 adapter 가까이에 두고, domain type이 외부 형식을 해석하게 하지 않는다.

## Wiring과 배치

concrete adapter 선택과 생성은 composition root에서 수행한다.

- core는 service locator, global container와 runtime registry를 직접 조회하지 않는다.
- adapter는 필요한 client·connection·configuration을 명시적으로 받는다.
- singleton, request, job과 tenant scope는 실제 resource lifecycle에 맞춘다.
- container가 생성한 resource의 종료 책임과 수동 생성한 resource의 종료 책임을 섞지 않는다.
- test는 production composition을 몰래 바꾸지 말고 명시적인 test composition을 사용한다.

폴더는 architecture 그림을 복제하기 위해 만들지 않는다. 저장소의 강제 구조가 없으면 feature 안에서 실제 port·adapter 수와 접근 경계를 기준으로 평평하게 시작한다. 동일 책임의 파일이 늘거나 package/module 경계가 필요할 때 `ports/`, `adapters/`, `inbound/`, `outbound/`를 분리한다.

언어별 interface 표현, visibility, 파일명과 package 규칙은 해당 언어 스킬이 소유한다.

## 기존 코드 정리

기존 시스템에 경계를 도입할 때 한 vertical slice씩 이동한다.

1. 현재 public behavior와 외부 dependency 호출을 characterization test로 고정한다.
2. controller·service·domain에 섞인 외부 타입과 effect를 표시한다.
3. consumer가 실제로 사용하는 최소 capability를 추출한다.
4. 기존 integration을 새 adapter 뒤로 옮기되 동작을 함께 바꾸지 않는다.
5. composition root에서 새 경계를 연결한다.
6. core unit test와 adapter integration test를 각각 실행한다.
7. 기존 facade·wrapper·alias가 필요하면 제거 조건과 consumer migration을 기록한다.
8. 한 slice가 검증된 뒤 다음 slice로 이동한다.

full rewrite, 전체 package 이동과 기술 교체를 한 변경에 결합하지 않는다. port 추출과 behavior 변경이 함께 필요하면 단계와 증거를 분리한다.

## 금지 패턴

- 모든 class에 대응 interface 만들기
- 실제 consumer 없이 `I...`, `...Port`, `...Adapter` 접미사만 추가하기
- ORM repository method 전체를 application port에 복사하기
- 하나의 `CommonPort`, `BaseRepository`, `IntegrationService`에 unrelated capability 누적하기
- adapter가 use case나 다른 adapter의 workflow를 조정하기
- domain이 framework annotation, SDK client, database row와 transport DTO를 import하기
- application이 concrete adapter를 직접 생성하기
- service locator와 전역 singleton으로 dependency를 숨기기
- fake 동작만 확인하고 실제 adapter가 같은 contract라고 가정하기
- test 편의만 위해 production contract 넓히기
- 작은 feature에 파일 하나씩인 대칭형 `domain/application/ports/adapters` tree 만들기
- `interface가 있으니 decoupled`라고 주장하고 import graph를 확인하지 않기

## 결정 결과와 완료 점검

경계 설계 결과는 다음 형식으로 제시한다.

```text
use case:
actor와 제어 방향:
외부 capability:
선택한 경계 수준: 직접 사용 | adapter만 | port + adapter
port owner와 contract:
adapter와 기술 dependency:
변환할 경계 타입:
composition과 lifecycle:
보존할 공개 계약:
정적 검증:
runtime·integration 검증:
미검증 위험:
```

완료 전에 확인한다.

- port마다 실제 consumer와 목적 있는 대화를 말할 수 있다.
- named interface마다 별도 선언이 필요한 이유가 있다.
- 구현체 수가 아니라 consumer contract와 변경 경계로 결정했다.
- core import graph에 framework·ORM·SDK·protocol 구현이 없다.
- adapter가 업무 workflow와 domain invariant를 소유하지 않는다.
- adapter contract에 외부 타입과 구현 전용 method가 새지 않는다.
- composition root 밖에서 concrete adapter를 선택하거나 생성하지 않는다.
- folder와 접미사가 아니라 compile-time dependency 방향으로 경계를 확인했다.
- fake·mock뿐 아니라 실제 adapter 검증 필요 범위를 적었다.
- migration wrapper와 호환 alias에는 제거 조건이 있다.
- 실행하지 않은 integration·E2E·production 검증을 통과로 표현하지 않았다.
