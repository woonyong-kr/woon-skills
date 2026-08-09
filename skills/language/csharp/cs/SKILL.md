---
name: cs
description: C# namespace·file, class·interface·record·member 순서, visibility, async·nullable 규칙을 설계·검토할 때 사용한다.
---

# C#

target .NET SDK, `LangVersion`, nullable, analyzer, `.editorconfig`, formatter와 solution 구조를 먼저 읽는다. 공통 책임 배치는 `$quality`, 어휘는 `$naming`을 함께 적용한다.

1. namespace·project와 feature ownership을 정하고 core type과 file 이름을 맞춘다.
2. class·record·struct·interface 중 identity, value, mutation과 boundary에 맞는 표현을 선택한다.
3. visibility를 좁게 두고 constructor가 유효한 object를 만들게 한다.
4. nullable, async, cancellation, collection ownership과 exception 계약을 public API에 드러낸다.
5. `using`, member와 modifier 순서를 repository analyzer 또는 한 기본값으로 고정한다.
6. format, analyzer, nullable compile과 test를 target framework 전체에서 실행한다.

type·API·오류 경계는 [설계 기준](references/design.md), file·member 순서·표기는 [규약](references/conventions.md)을 필요한 경우에만 읽는다.
