# 도메인 모델 기준

## 목차

- 증거부터 모델링하기
- bounded context
- entity와 value object
- aggregate와 invariant
- service와 event
- 검증

## 증거부터 모델링하기

요구사항에서 다음 표를 먼저 채운다.

| 항목 | 질문 |
| --- | --- |
| 용어 | actor마다 같은 단어를 같은 뜻으로 쓰는가 |
| command | 누가 어떤 의도로 상태를 바꾸는가 |
| invariant | 어떤 상태 조합은 절대 commit되면 안 되는가 |
| observation | 성공을 누가 언제 관찰하는가 |
| time | 즉시 지켜야 하는가, 나중에 수렴해도 되는가 |
| authority | 이 사실을 결정하는 system·context는 어디인가 |

명사에서 class를 바로 만들지 않는다. 실제 decision과 lifecycle이 없는 객체는 data carrier일 수 있다.

## bounded context

- 한 context 안에서는 용어, identity, rule과 source of truth가 일관돼야 한다.
- 다른 context가 같은 이름을 다르게 쓰면 type과 API를 분리하고 명시적으로 번역한다.
- context boundary는 team 수나 deployment 수가 아니라 model 변화 이유와 업무 권한으로 정한다.
- shared kernel은 공동 변경 비용과 release 결합을 감수할 때만 사용한다.
- 외부·legacy model은 anti-corruption adapter에서 번역하고 core에 외부 enum·status를 퍼뜨리지 않는다.

## entity와 value object

- 시간이 지나도 추적할 identity가 필요할 때만 entity로 만든다.
- 값이 같으면 교환 가능한 개념은 value object로 만들고 생성 시 유효성을 검증한다.
- value object는 immutable로 두고 변경은 새 값을 반환한다.
- primitive string·number가 통화, 기간, tenant ID, 상태 같은 규칙을 가리면 의미 type을 사용한다.
- identity equality와 field equality를 섞지 않는다.

## aggregate와 invariant

- aggregate는 graph 묶음이 아니라 transaction consistency boundary다.
- root는 invariant를 깨는 중간 상태를 외부에 노출하지 않는다.
- 한 command가 항상 함께 잠그고 갱신해야 하는 최소 객체만 포함한다.
- 다른 aggregate는 object reference 대신 stable ID로 참조한다.
- aggregate가 무한히 커지면 contention, load와 transaction 비용을 측정하고 invariant를 재검토한다.
- 여러 aggregate를 한 transaction에 넣기 전 정말 즉시 일관성이 필요한지 확인한다. 지연 수렴이 가능하면 event·workflow와 reconciliation을 설계한다.
- validation은 입력 형식, domain invariant, cross-aggregate policy를 구분한다.

## service와 event

- 한 entity·value object에 자연스럽게 속하지 않는 stateless domain rule만 domain service로 둔다.
- workflow, transaction, port 호출과 retry는 application service가 소유한다.
- domain event는 이미 발생한 업무 사실을 과거형으로 표현하고 aggregate commit 전 임의로 publish하지 않는다.
- integration event는 외부 consumer용 schema·version·privacy 계약을 별도로 가진다.
- event가 command를 위장하거나 모든 field snapshot을 유출하지 않게 한다.

## 검증

- aggregate unit test: 각 command가 invariant를 보존하고 불가능한 전이를 거부하는지 확인한다.
- state transition test: 같은 시작 상태와 command가 결정적 결과를 내는지 확인한다.
- concurrency test: 실제 transaction에서 동시에 들어온 command가 invariant를 깨지 않는지 확인한다.
- contract test: context 번역이 외부 model 변화와 오류를 격리하는지 확인한다.
- example mapping: 실제 업무 사례와 반례를 domain expert가 검토한다.

repository·ORM test만 통과했다고 domain model이 맞다고 판단하지 않는다. 업무 사실이 불명확하면 추측한 invariant를 확정하지 않고 질문으로 남긴다.
