# C# 설계 기준

## project와 type 경계

SDK, target frameworks, nullable와 implicit using, analyzer severity, dependency injection·serialization framework를 먼저 확인한다. folder와 namespace는 project convention을 따르되 기술 layer만 깊게 중첩하지 않고 feature ownership을 드러낸다.

- class: identity, mutable lifecycle, encapsulated invariant 또는 framework contract
- record/class: value-like data와 명시적 immutable contract
- readonly record struct/struct: 작고 복사 비용과 value semantics가 검증된 값
- interface: consumer가 필요한 stable behavior boundary; 구현 하나마다 기계적으로 만들지 않음

constructor는 유효한 object를 만들고 async I/O나 복구가 필요한 작업은 factory/use case로 분리한다. required member와 object initializer로 invariant를 우회하지 않게 한다.

## member와 visibility

compile되는 가장 좁은 visibility를 사용한다. `protected`는 subclass extension contract, `internal`은 assembly boundary, `public`은 외부 stable API일 때만 쓴다. test 편의를 위해 production member를 넓히지 않고 `InternalsVisibleTo`도 최소 assembly에만 적용한다.

property는 값처럼 읽을 수 있는 작고 예측 가능한 동작에 사용한다. network/database I/O, 큰 계산과 상태 전이를 getter에 숨기지 않는다. public mutable field보다 property와 method로 invariant를 보호한다.

## nullable, collection과 오류

- nullable reference type을 켜고 `!`는 runtime 검증 대용으로 쓰지 않는다.
- empty와 missing이 다른 계약이면 `null`, empty collection, option/result를 구분한다.
- input은 필요한 가장 좁은 read-only interface를 받고, return collection의 ownership과 mutation 가능성을 드러낸다.
- iterator가 한 번 실행되는지 재열거 가능한지 문서와 type으로 구분한다. 즉시 `ToList()`로 materialize해 lazy 이점을 없애지 않는다.
- caller가 복구할 수 있는 failure는 의미 있는 exception 또는 result로 표현하고 low-level cause를 `InnerException`으로 보존한다.
- `IDisposable`/`IAsyncDisposable` resource는 `using`/`await using`으로 닫고 finalizer에 의존하지 않는다.

## async와 cancellation

Task-returning non-event method는 repository convention이 없으면 `Async` suffix를 쓴다. `async void`는 event handler 외에 쓰지 않는다. `CancellationToken`은 호출 chain에서 전달하고 임의로 새 token이나 `CancellationToken.None`으로 끊지 않는다. fire-and-forget은 failure 관찰과 owner lifetime이 있을 때만 허용한다.

library code의 `ConfigureAwait` 정책은 target framework와 repository 기준을 따른다. sync-over-async (`.Result`, `.Wait()`)로 deadlock과 thread starvation을 만들지 않는다.

## 검증

`dotnet format --verify-no-changes`, `dotnet build` analyzer·nullable warning, unit/integration test를 target framework별로 실행한다. reflection, serializer, DI container와 source generator가 constructor·member visibility·name 변경에 의존하는지 확인한다.

이 문서는 [Google C# Style Guide](https://github.com/google/styleguide/blob/1809c769de31ba388c755ad15dd057a9ba8531fd/csharp-style.md)를 참고하되 오래된 language-version 선택은 현재 SDK·analyzer 계약으로 대체했다.
