# 테스트 설계 기준

## 목차

- 테스트가 소유하는 계약
- 기대값과 입력
- test double
- 경계와 실패
- 비동기·시간·동시성
- 배치와 이름
- mutation 확인

## 테스트가 소유하는 계약

테스트 본문을 쓰기 전에 다음 질문에 한 문장으로 답한다.

> production 코드의 어떤 현실적인 잘못이 이 테스트를 실패시켜야 하는가?

답이 “source text가 바뀜”, “private method 이름이 바뀜”, “상수가 바뀜”뿐이면 구현 감지기다. public 결과, 상태 전이, 외부 경계에 보낸 값, 오류 또는 부수 효과를 검증한다. framework 자체가 이미 보장하는 동작이 아니라 우리 코드가 framework와 맺은 경계를 검사한다.

한 테스트는 하나의 관찰 가능한 행동을 소유한다. 서로 다른 원인으로 실패하는 정상·오류·경계 흐름은 분리하되, 하나의 원자적 transaction처럼 함께 보장해야 하는 불변 조건은 같은 scenario에서 검증한다.

## 기대값과 입력

- 기대값은 literal 또는 사람이 검토한 fixture로 만든다.
- production builder, parser, formatter나 같은 공식을 기대값 계산에 재사용하지 않는다.
- 표 기반 테스트는 입력과 독립적인 `expected`를 각 행에 명시한다.
- 현재 출력물을 그대로 snapshot으로 승인하지 않는다. snapshot은 안정된 구조의 의도한 변경을 사람이 검토했을 때만 쓴다.
- 정상값뿐 아니라 빈 값, 0, 최댓값, 경계 직전·정확한 경계·직후, malformed, unauthorized와 중복 요청을 포함한다.

## Test double

실제 동작을 먼저 실행해 느리거나 외부인 경계를 확인한 뒤 그 지점만 fake·stub·mock으로 바꾼다.

- mock 호출 자체를 최종 결과처럼 검증하지 않는다.
- argument, 횟수와 순서가 계약이면 구체적으로 검증한다.
- response double은 실제 필수 field와 오류 형태를 빠뜨리지 않는다.
- mock 때문에 실제 상태 기록·validation·cleanup이 사라지면 한 단계 아래 외부 I/O를 대신한다.
- setup이 assertion보다 복잡하거나 실제 component의 메서드를 계속 누락하면 integration test로 전환한다.
- 테스트 전용 cleanup은 production class가 아니라 test utility가 소유한다.

## 경계와 실패

오류 test는 예외 종류뿐 아니라 원인 보존, 부분 상태 미발생과 외부 효과 횟수를 확인한다. retry·idempotency·transaction은 다음을 분리한다.

1. 재시도 가능한 실패와 즉시 실패
2. 최대 시도 횟수
3. 같은 idempotency key 또는 중복 효과 방지
4. 마지막 cause 보존
5. 중간 write의 rollback 또는 보상

## 비동기·시간·동시성

임의 `sleep`으로 완료 시점을 추측하지 않는다. event, state, count나 파일 존재처럼 관찰할 조건을 기다리고 전체 timeout에는 실패 이유를 넣는다. debounce·TTL처럼 시간 자체가 계약일 때만 clock을 제어하거나 근거 있는 시간을 사용한다.

동시성 test는 같은 실행을 반복하는 것으로 끝내지 않는다. barrier나 controllable fake로 문제 순서를 만들고, 동시 실행 한도, 결과 순서, 중복 효과와 첫 오류 정책을 각각 검증한다.

## 배치와 이름

- production 코드와 같은 기능·public behavior를 기준으로 test를 가까이 둔다.
- 구현 계층 폴더를 기계적으로 복제하지 않는다.
- 이름은 `조건_행동_기대결과`가 드러나게 쓰되 framework 관례를 따른다.
- 공통 fixture는 두 곳 이상에서 같은 의미로 쓰이고 함께 변경될 때만 추출한다.

## Mutation 확인

완료 전에 현실적인 결함을 하나씩 가정한다.

- 잘못된 분기 또는 상수
- argument나 호출 순서 변경
- validation·상태 변경·외부 효과 누락
- 빈 결과 또는 조용한 fallback
- unauthorized·malformed 입력 허용

각 결함을 잡는 테스트를 지목한다. 고위험 변경이나 뒤늦게 작성한 회귀 테스트는 안전한 임시 mutation 또는 수정 전 revision으로 실제 실패를 확인하고 원상복구한 뒤 다시 통과시킨다.
