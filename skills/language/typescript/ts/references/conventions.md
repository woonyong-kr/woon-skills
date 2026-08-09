# TypeScript 규약

## 적용 순서

1. `tsconfig.json`, formatter, linter, package export와 같은 저장소의 실행 가능한 규칙
2. 같은 역할의 기존 파일에서 반복되는 규칙
3. 이 문서의 Woon 기본값
4. Google 소유 저장소이거나 사용자가 명시한 경우에만 strict Google 차이

서로 다른 규칙을 한 폴더에 섞지 않는다. 예를 들어 기존 파일이 `kebab-case`이면 Google의 `snake_case`를 새 파일 하나에만 적용하지 않는다. 대규모 표기 변경은 기능 변경과 분리한다.

## 파일과 import

- Woon 기본 file·folder 이름은 `kebab-case`다. strict Google mode는 `.ts` source file에 `snake_case`를 사용한다.
- side-effect import는 의도가 드러나는 위치에 따로 두고, value와 type을 구분한다. type-only symbol은 `import type` 또는 inline `type` modifier를 사용한다.
- 외부 package, workspace package, 동일 feature의 상대 import 순서를 repository sorter 하나로 고정한다. alias는 `tsconfig`와 runtime bundler가 모두 해석할 때만 쓴다.
- wildcard barrel export를 만들지 않는다. public surface는 명시적으로 export하고 mutable binding을 export하지 않는다.
- namespace 역할만 하는 static class 대신 module의 function·constant를 export한다. TypeScript `namespace`는 기존 declaration merge나 외부 계약이 요구하지 않으면 만들지 않는다.

## 선언과 함수 위치

formatter가 별도 순서를 강제하지 않으면 다음 순서를 쓴다.

1. side-effect import
2. 외부 value/type import
3. 내부 value/type import
4. module constant와 schema
5. public type·interface·enum
6. public function·class
7. module-private helper

named top-level function은 선언식 `function parseInvoice()`를 기본으로 하고 callback은 arrow function을 쓴다. local helper는 한 caller의 흐름을 설명하면 가까이 두되, 여러 export가 공유하면 이름 있는 module-private function으로 올린다. class field arrow function은 instance별 identity가 실제로 필요할 때만 쓴다.

## class와 visibility

- class는 invariant·identity·lifecycle이 있을 때만 쓴다. 단순 grouping을 위해 만들지 않는다.
- public API, constructor, protected extension point, private implementation을 읽기 쉬운 묶음으로 유지한다. 저장소가 정한 member-order lint가 있으면 그것이 우선이다.
- strict Google mode는 TypeScript `private`을 쓰고 `#private` identifier를 쓰지 않는다. Woon 기본은 저장소가 선택한 한 방식만 일관되게 쓴다.
- constructor에서 overridable method나 외부 I/O를 호출하지 않는다. field initializer와 constructor parameter property가 같은 상태를 이중 소유하지 않게 한다.

## 이름

- type·interface·class·enum·decorator·type parameter: `PascalCase`
- function·method·property·variable·parameter·module alias: `lowerCamelCase`
- process 전체에서 고정된 global constant: `CONSTANT_CASE`
- boolean: `is`, `has`, `can`, `should`; collection은 복수형; unit은 이름에 명시

interface에 `I` prefix를 붙이지 않는다. acronym도 한 단어처럼 `HttpUrl`, `loadRpc`로 적는다. `_` prefix/suffix와 `$`는 framework 계약이 아니면 쓰지 않는다. 구체적인 단어 선택과 사용자 선호 어휘는 `$naming`이 소유한다.

## type과 runtime 안전

- object contract는 `interface`, union·tuple·mapped/conditional type은 `type`을 기본으로 하되 같은 shape를 중복 선언하지 않는다.
- 외부 입력은 `unknown`에서 runtime validation으로 좁힌다. `as`, non-null assertion, double assertion은 검증이 아니며 불변식 근거를 남긴다.
- optional property와 `| undefined`를 의미 없이 함께 쓰지 않는다. absent와 present-but-undefined를 구분해야 할 때만 둘을 나눈다.
- 단순 type에는 `T[]`, 복합 union/object element에는 `Array<T>`를 사용해 괄호 모호성을 피한다.
- `===`/`!==`를 기본으로 한다. `eval`, `Function(string)`, builtin prototype 수정, `const enum`, primitive wrapper instance를 쓰지 않는다.
- `@ts-ignore`나 `@ts-nocheck`로 오류를 숨기지 않는다. 테스트의 의도된 type error도 가능하면 typed fixture로 좁힌다.

## 주석과 검증

JSDoc은 public 사용자가 알아야 할 계약, 일반 주석은 구현 이유를 설명한다. TypeScript가 이미 표현한 type을 `@param`·`@return`에 반복하지 않는다. format → lint/conformance → typecheck → unit/integration test → build를 저장소 script로 실행한다.

이 문서는 [Google TypeScript Style Guide](https://github.com/google/styleguide/blob/1809c769de31ba388c755ad15dd057a9ba8531fd/tsguide.html)를 참고해 Woon의 저장소 우선·점진 변경·runtime 검증 기준으로 재작성했다. Google guide도 외부 환경에는 그대로 맞지 않을 수 있음을 명시한다.
