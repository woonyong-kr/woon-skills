# C# 규약

## file, namespace와 using

file·folder는 `PascalCase`, core public type과 file 이름을 맞추고 한 파일에 core type 하나를 둔다. partial/generated/framework type은 예외다. file-scoped와 block namespace 중 repository 방식 하나를 사용한다.

`using`은 namespace 밖 file top에 두고 `System` group을 먼저, 나머지를 alphabetical order로 둔다. global/implicit using은 project 전체에서 실제로 공유하는 namespace만 포함한다. 긴 generic type을 숨기기 위한 alias보다 의미 있는 named type을 만든다.

## modifier와 member 순서

strict Google modifier 순서는 다음이다.

`public protected internal private new abstract virtual override sealed static readonly extern unsafe volatile async`

repository analyzer가 없으면 member를 다음 kind로 묶는다.

1. nested type·enum·delegate·event
2. static·const·readonly field
3. instance field·property
4. constructor·finalizer
5. method

각 group 안에서는 `public` → `internal` → `protected internal` → `protected` → `private` 순서로 둔다. interface implementation은 관련 member를 함께 둔다. overload는 연속 배치하고 private helper는 owner method와의 탐색성을 해치지 않는 범위에서 method group 뒤에 둔다.

## 이름

- namespace·type·method·public property·enum: `PascalCase`
- interface: `I` + `PascalCase`
- local·parameter: `camelCase`
- private/protected/internal field와 property: `_camelCase`
- generic type parameter: `T` 또는 `TResult`
- async method: `LoadAsync`; predicate: `IsValid`, `HasAccess`

strict Google mode는 `const`, `static`, `readonly` 여부와 무관하게 private field를 `_camelCase`로 유지한다. acronym은 `MyRpc`, `HttpClient`처럼 한 단어로 취급한다. Woon 공통 어휘와 금지 단어는 `$naming`이 소유한다.

## 표현과 collection

단순 read-only property는 expression body를 허용하되 복잡한 method 전체를 짧아 보이게 압축하지 않는다. non-trivial lambda나 재사용 lambda는 named method로 뺀다. LINQ chain이 여러 단계의 side effect·enumeration을 숨기면 imperative code나 named query로 분리한다.

literal boolean·숫자 argument의 의미가 보이지 않으면 named argument, enum, named constant 또는 options type을 사용한다. `out`은 try-pattern이나 다중 return 계약이 명확할 때만 쓰고 일반 return/value tuple/named result와 비교한다. public API의 복잡한 tuple은 named type을 우선한다.

## format와 변경

`.editorconfig`와 formatter가 절대 우선이다. strict Google mode는 2-space indent, 100-column, K&R brace와 optional block에도 brace를 사용한다. 현대 .NET 기본 formatter와 다르면 한 project 안에 섞지 않고 선택을 config로 고정한다. 기능 변경과 대규모 formatting은 분리한다.

이 문서는 [Google C# Style Guide](https://github.com/google/styleguide/blob/1809c769de31ba388c755ad15dd057a9ba8531fd/csharp-style.md)의 naming·organization·collection 규칙을 현재 .NET 저장소에 조건부 적용하도록 재작성했다.
