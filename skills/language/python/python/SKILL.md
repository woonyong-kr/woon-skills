---
name: python
description: Python 파일·package 구조, class·Protocol·function 위치, naming, typing, exception, public API를 일관되게 설계·정리할 때 사용한다.
---

# Python

저장소의 Python version, `pyproject.toml`, formatter, type checker, test layout과 주변 module을 먼저 읽는다. 공통 변경 규율은 `$quality`를 함께 적용한다.

1. 새 파일 전에 기존 owner module과 import direction을 찾는다.
2. package는 기술 유형이 아니라 domain responsibility로 나눈다.
3. function은 사용하는 곳이 아니라 policy/data를 소유한 module에 둔다.
4. `Protocol`이나 ABC는 실제 대체 구현·외부 boundary·isolated test seam이 있을 때만 만든다.
5. public import path를 바꾸면 compatibility export 또는 migration을 검토한다.
6. visual consistency만을 위해 새 `InvoiceId` 같은 wrapper type이나 layer를 만들지 않는다.
7. repository의 lint, type check, pytest를 실행한다.

파일 배치, 선언 순서, naming, class/interface/function 기준은 관련 작업에서만 [Python design](references/design.md)을 읽는다.
