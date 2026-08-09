---
name: ts
description: TypeScript 코드의 모듈·파일 배치, type/interface, 함수·클래스, async 오류와 언어별 표기 규칙을 설계하거나 일관되게 정리할 때 사용한다. JavaScript 전용 작업에는 사용하지 않는다.
---

# TypeScript

저장소의 `tsconfig.json`, package scripts, formatter, linter와 같은 역할의 기존 모듈을 먼저 확인한다. 공통 배치 판단에는 `$quality`, 이름의 의미와 사용자 어휘에는 `$naming`을 함께 적용한다. TypeScript 구조에는 [설계 기준](references/design.md), import·선언 순서·표기에는 [규약](references/conventions.md)을 필요한 경우에만 읽는다.

1. 실행 환경과 module system, strictness, path alias와 public export를 확인한다.
2. 변경할 모듈의 책임과 runtime 경계를 정한다.
3. type, interface, class, function과 discriminated union 중 가장 좁은 표현을 선택한다.
4. `unknown`을 경계에서 좁히고 `any`가 내부로 퍼지지 않게 한다.
5. I/O와 async 실패를 이름과 반환 계약에서 숨기지 않는다.
6. public import와 runtime behavior를 보존하며 한 모듈씩 이동하거나 이름을 바꾼다.
7. 저장소에 실제로 있는 format→lint→type check→test→build 순으로 검증한다.

완료 전에 새 barrel export와 circular dependency가 없는지, type-only import가 runtime import로 남지 않았는지, 처리하지 않은 Promise와 조용한 fallback이 없는지 확인한다.
