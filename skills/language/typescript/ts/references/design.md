# TypeScript 설계 기준

## 모듈과 파일 배치

- import 가능한 코드는 저장소가 정한 source root에 두고 테스트는 기존 co-location 또는 별도 test 구조를 따른다.
- 업무 규칙은 framework와 I/O를 모르는 기능 모듈, 흐름 조정은 use case, HTTP·CLI·message는 입력 경계, database·remote API·filesystem은 adapter에 둔다.
- `utils.ts`, `helpers.ts`, `common.ts`를 기본 목적지로 사용하지 않는다.
- `index.ts`는 안정된 public surface만 명시적으로 export한다. feature 전체를 wildcard로 재수출하거나 내부 모듈을 숨겨 circular dependency를 만들지 않는다.
- public top-level type과 함수가 독립된 변경 이유를 가지면 파일을 분리하고, 작은 private helper는 소유 모듈에 둔다.

## 선언 순서

저장소 규칙이 없으면 다음 순서를 사용한다.

1. side-effect import
2. 외부 value import와 `import type`
3. 내부 value import와 `import type`
4. module constant
5. public type·interface·enum
6. public function·class
7. private helper

public surface를 먼저 읽을 수 있게 하고 private helper는 소유 동작 가까이에 묶는다.

## 표기 규칙

- file·folder: `kebab-case`
- type·interface·class·enum: `PascalCase`
- function·method·property·variable·parameter: `lowerCamelCase`
- 환경 변수와 실제 전역 상수: `UPPER_SNAKE_CASE`
- private class field: `private` 또는 `#` 중 저장소 기준 하나를 사용
- boolean: `is`, `has`, `can`, `should`
- collection: 복수형, map은 `usersById`처럼 key를 표시
- unit: `timeoutSeconds`, `sizeBytes`

interface에 `I` 접두사를 붙이지 않는다. 이름의 단어 선택과 금지 어휘는 `$naming`이 소유한다.

## type과 interface

- `interface`: 확장 가능한 object contract와 class implementation 경계
- `type`: union, intersection, mapped·conditional type, tuple과 function signature
- 같은 object shape를 표현하려고 type과 interface를 중복 정의하지 않는다.
- 외부 입력은 `unknown`으로 받고 schema 또는 type guard로 좁힌다. `any`는 untyped boundary에서만 격리하고 내부로 반환하지 않는다.
- 상태 변형이 닫힌 집합이면 공통 판별 필드를 가진 discriminated union을 사용하고 exhaustive check를 둔다.
- 단순 상수 집합은 runtime enum이 필요한지 확인하고, 아니면 `as const` object와 union을 검토한다.
- 읽기 전용 계약에는 `readonly`를 사용하되 외부 mutable collection을 type assertion만으로 불변이라고 속이지 않는다.
- `as`와 non-null assertion은 runtime 검증이 아니므로 입력 검증 대용으로 사용하지 않는다.

## 함수와 클래스

- 상태가 필요 없는 동작은 module function을 우선한다.
- class는 identity, invariant, lifecycle, dependency bundle 또는 framework contract가 있을 때 사용한다.
- 긴 parameter list를 습관적으로 options object로 바꾸지 않는다. 입력이 하나의 안정된 개념일 때만 object로 묶는다.
- callback과 closure는 포착한 상태와 실행 시점이 명확할 때 사용한다.
- public function은 반환 type을 명시하고 외부 경계의 generic type argument를 생략하지 않는다.
- overload는 구현 하나가 실제로 구분 가능한 호출 계약 여러 개를 제공할 때만 사용한다.

## async와 오류

- async function은 `Async` 접미사보다 도메인 행동을 이름으로 사용하고 `Promise<Result>` 계약을 명시한다.
- 독립 작업이고 전체 실패가 허용될 때만 `Promise.all`을 사용한다.
- 부분 성공이 계약이면 작업별 결과 또는 `Promise.allSettled`를 사용하고 실패 처리 정책을 명시한다.
- floating Promise를 남기지 않는다. 의도적으로 분리 실행하면 오류 관찰 방법을 둔다.
- `catch`한 값은 `unknown`으로 취급하고 좁힌다.
- 원래 오류를 `cause`로 보존하고 의미를 아는 경계에서 domain 또는 adapter 오류로 변환한다.
- 예상 가능한 domain failure와 programmer error를 같은 빈 값으로 바꾸지 않는다.

## 일관성 복구

1. `tsconfig.json`, package exports, path alias와 모든 import 사용처를 기록한다.
2. public type·function과 runtime side effect를 테스트로 고정한다.
3. 공개 이름만 바꾸고 signature와 runtime contract가 같으면 명시적 export alias를 사용한다. parameter·return·오류 계약이 다르면 wrapper로 변환 지점을 드러낸다.
4. 모듈 하나를 이동하거나 이름을 바꾼다.
5. type-only와 runtime import, circular dependency와 package export를 확인한다.
6. 저장소 scripts의 format, lint, type check, test와 build를 실행한다.
7. 다음 책임 단위로 진행한다.
