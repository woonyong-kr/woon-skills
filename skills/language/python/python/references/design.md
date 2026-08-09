# Python design reference

## Package and file placement

`src/<package>/` layout을 쓰는 저장소는 importable code를 `src`에, test를 `tests`에 둔다. 이미 flat layout이면 요청 없이 바꾸지 않는다.

- domain policy: framework와 I/O를 모르는 domain module
- use-case orchestration: application/service module
- database, HTTP, filesystem, vendor SDK: adapter/infrastructure module
- CLI, HTTP handler, consumer: boundary module
- shared helper: 두 개 이상의 caller가 같은 의미와 change reason을 공유할 때만

`utils.py`, `helpers.py`, `common.py`를 기본 목적지로 쓰지 않는다. 의미가 `parse_duration`이면 duration parser를 소유한 module에 둔다. 한 파일이 여러 independent reason으로 자주 바뀌거나 탐색이 어려울 때만 분리한다.

## Module declaration order

repository formatter/import sorter가 우선이다. 별도 규칙이 없으면 다음 순서를 쓴다.

1. module docstring
2. `from __future__ import annotations`
3. standard library, third-party, local imports
4. module constants
5. public type aliases, enum, dataclass
6. public Protocol/ABC
7. public functions and classes
8. private helpers
9. executable guard

호출 순서에 맞춰 helper를 위아래로 반복 배치하지 않는다. public surface를 먼저 읽을 수 있게 하고 private helper는 owner 가까이 묶는다.

## Naming

- module/package/function/variable: `lower_snake_case`
- class/exception/protocol: `PascalCase`
- constant: `UPPER_SNAKE_CASE`
- private implementation: leading `_`
- boolean: `is_healthy`, `has_access`, `should_retry`
- collection: 복수형 `users`; mapping은 의미를 드러내는 `users_by_id`
- unit: `timeout_seconds`, `size_bytes`
- async function은 `async_` prefix보다 domain verb를 유지

`data`, `info`, `value`, `object`, `thing`, `manager`, `processor`처럼 책임을 숨기는 이름을 피한다. 기존 public API rename은 caller와 compatibility를 먼저 확인한다.

## Functions

함수 이름은 `load_registry`, `validate_profile`, `render_report`처럼 observable result를 나타내는 verb로 시작한다. predicate는 `is/has/can/should`를 쓴다.

module-level function:
- object state가 필요 없고 domain operation이 명확함
- dependency를 parameter로 받음
- 여러 class가 공유해도 동일 owner가 있음

instance method:
- object invariant/state를 사용하거나 변경함
- lifecycle과 함께 움직임

`@staticmethod`은 namespace 역할만 하면 module function을 우선한다. closure는 짧은 local policy와 캡처가 의미를 명확히 할 때만 쓴다. 긴 parameter list는 무조건 dataclass로 바꾸지 말고 입력이 하나의 stable concept인지 확인한다.

guard clause로 invalid path를 먼저 끝내고 main path의 indentation을 얕게 유지한다. hidden I/O를 pure-looking helper 뒤에 감추지 않는다.

## Classes and interfaces

class는 identity, invariant, lifecycle, polymorphic behavior 중 하나가 있을 때 쓴다. immutable record면 `@dataclass(frozen=True, slots=True)`가 적합한지 검토한다. dict가 external schema boundary면 TypedDict/model을 고려하되 repository의 validation library를 따른다.

`Protocol`은 consumer가 필요한 최소 surface를 소유한다. 구현 class 전체를 복제하지 않는다. runtime check가 필요하지 않으면 `@runtime_checkable`을 붙이지 않는다. 구현이 하나뿐이고 교체·test seam이 없으면 Protocol을 만들지 않는다.

inheritance보다 composition을 우선하되 framework contract는 따른다. mixin은 독립된 작은 behavior와 명확한 method contract가 있을 때만 쓴다.

## Types and errors

public boundary와 ambiguous collection에는 type을 명시한다. `Any`는 untyped 외부 boundary에서 좁히고 내부로 퍼뜨리지 않는다. `cast`는 runtime conversion이 아니므로 검증 대용으로 쓰지 않는다.

exception은 caller가 구별해 처리해야 하는 failure meaning으로 나눈다. low-level cause는 `raise DomainError(...) from error`로 보존한다. invalid external input은 write 전에 거부한다. broad `except Exception`은 cleanup, boundary translation, batch isolation처럼 명확한 정책이 있을 때만 사용하고 삼키지 않는다.

## Consistency repair

잘못 배치된 기존 코드를 정리할 때 한 번에 구조를 재설계하지 않는다.

1. 현재 public import와 test를 기록한다.
2. 책임이 명확한 단위 하나를 move/rename한다.
3. compatibility import가 필요한지 판단한다.
4. caller와 tests를 수정한다.
5. formatter, lint, type check, test를 실행한다.
6. 다음 단위로 진행한다.
