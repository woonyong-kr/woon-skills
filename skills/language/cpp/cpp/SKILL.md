---
name: cpp
description: C++ header·source, class·struct·access, ownership, 함수·include·naming 규칙을 설계·검토할 때 사용한다. C에는 사용하지 않는다.
---

# C++

target standard, compiler, build graph, `.clang-format`, static analyzer, exception·RTTI 정책과 같은 component를 먼저 읽는다. 공통 책임 배치는 `$quality`, 어휘는 `$naming`을 함께 적용한다.

1. public API·ABI와 ownership/lifetime을 먼저 고정한다.
2. self-contained header와 Include What You Use를 지키고 transitive include에 기대지 않는다.
3. value semantics를 우선하고 동적 소유권은 `std::unique_ptr`, 공유가 계약일 때만 `std::shared_ptr`로 표현한다.
4. class는 invariant를 캡슐화하고 단순 data aggregate는 struct를 사용한다.
5. access·declaration·definition 위치와 naming을 module 전체에서 일관되게 정리한다.
6. format, compile warning, static analysis, sanitizer와 test를 실제 standard로 실행한다.

type·ownership·API 경계는 [설계 기준](references/design.md), include·member 순서·표기는 [규약](references/conventions.md)을 필요한 경우에만 읽는다.
