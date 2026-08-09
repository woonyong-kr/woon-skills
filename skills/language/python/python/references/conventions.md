# Python 규약

## 적용 순서

지원 Python version, `pyproject.toml`, formatter, linter, type checker와 기존 public import를 먼저 읽는다. Black/Ruff/Pyink 같은 자동 도구와 이 문서의 줄 길이가 다르면 도구를 따르고 수동 정렬하지 않는다.

## module 순서와 import

1. module docstring
2. `from __future__ import annotations`
3. standard library, third-party, repository package import
4. module constant와 schema/type alias
5. public enum·dataclass·Protocol/ABC
6. public function·class
7. module-private helper
8. executable guard

import는 한 줄에 한 module을 기본으로 하고 full package path를 사용한다. strict Google mode는 symbol보다 module을 import하고 `from package import module` 형태를 사용한다. type checker 전용 import 등 예외는 tool과 runtime cycle을 확인한다. 상대 import나 `sys.path` 변경으로 실행 위치에 따라 다른 module을 읽게 하지 않는다.

## 함수와 class 위치

module-level function은 state가 없고 module이 policy를 소유할 때 쓴다. 단지 숨기기 위해 nested function/class를 만들지 말고 `_private_helper`로 둔다. closure가 local value를 실제로 캡처할 때만 중첩한다.

관련 class와 top-level function은 같은 module에 둘 수 있으며 Java처럼 파일당 class 하나를 강제하지 않는다. 긴 함수는 줄 수만으로 분리하지 않지만 약 40줄을 넘고 책임·indent·local state가 늘면 의미 단위 분리를 검토한다.

mutable object를 default argument로 두지 않는다. `None` sentinel이나 immutable default를 사용하고 함수 안에서 새 값을 만든다. property는 값처럼 읽어도 되는 작고 예측 가능한 동작에만 쓰며 I/O나 큰 비용을 숨기지 않는다.

## 이름과 visibility

- module·package·function·method·variable·parameter: `lower_snake_case`
- class·exception·Protocol·public type alias: `PascalCase`
- constant: `UPPER_SNAKE_CASE`
- internal symbol: leading `_`; double-leading name mangling은 기본 privacy 도구로 쓰지 않음

`.py` module 이름에 dash를 쓰지 않는다. 이름의 길이는 scope에 비례하며 익숙하지 않은 축약과 type을 반복하는 Hungarian 이름을 피한다.

## 오류·resource·type

- built-in exception이 의미를 충분히 표현하면 재사용하고 custom exception은 `Error`로 끝낸다.
- `assert`를 외부 입력 검증이나 필수 runtime invariant에 쓰지 않는다.
- broad `except Exception`은 process boundary, cleanup, batch isolation처럼 정책이 있을 때만 쓰고 원인을 기록하거나 `raise ... from error`로 보존한다.
- file, socket, lock, transaction은 context manager로 닫는다. import 시 network·filesystem mutation 같은 숨은 실행을 만들지 않는다.
- public API와 오류가 잦거나 모호한 collection에는 type을 적는다. `Any`는 untyped boundary에서 좁히고 내부로 확산하지 않는다.
- 실행 파일은 `main()`과 `if __name__ == "__main__":` guard를 사용한다.

## 문서와 검증

public module·class·function은 사용자가 알아야 할 목적, parameter 의미, return, side effect와 예외를 docstring으로 설명한다. 구현을 그대로 낭독하지 않는다. format → lint → type check → pytest를 실행하고 public import와 executable entrypoint를 함께 확인한다.

이 문서는 [Google Python Style Guide](https://github.com/google/styleguide/blob/1809c769de31ba388c755ad15dd057a9ba8531fd/pyguide.md)를 참고해 Woon의 formatter 우선·public compatibility·domain ownership 기준으로 재작성했다.
