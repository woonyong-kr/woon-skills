---
name: c
description: C header·source 배치, 함수·struct·pointer ownership, 전처리기와 오류 계약을 설계·검토할 때 사용한다. C++에는 사용하지 않는다.
---

# C

target C dialect, compiler, platform ABI, build flags, formatter와 sanitizer를 먼저 확인한다. 공통 책임 배치는 `$quality`, 어휘는 `$naming`을 함께 적용한다.

1. public declaration과 ABI는 self-contained header, 구현은 대응하는 source가 소유한다.
2. translation unit 내부 symbol은 `static`으로 제한하고 public symbol은 module prefix를 사용한다.
3. pointer마다 nullability, length, mutability, ownership과 lifetime을 계약으로 드러낸다.
4. allocation·resource 획득과 해제 owner를 하나로 정하고 부분 초기화 실패 경로를 검증한다.
5. macro보다 typed function·enum·constant를 우선하고 여러 문장 macro를 새로 만들지 않는다.
6. compiler warning, static analysis, sanitizer와 test를 실제 target dialect로 실행한다.

파일·함수·struct 경계는 [설계 기준](references/design.md), include·선언 순서·표기는 [규약](references/conventions.md)을 필요한 경우에만 읽는다.
