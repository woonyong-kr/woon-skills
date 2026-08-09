# C++ 설계 기준

## API와 파일 경계

project의 C++ standard와 ABI, exception·RTTI·module 정책을 먼저 확인한다. public header는 단독 compile 가능해야 하며 필요한 declaration을 직접 include한다. template, concept, 짧고 안정된 inline 외의 non-trivial definition은 `.cc`에 둔다. forward declaration은 include cost보다 incomplete-type·ownership·ABI 위험이 작은 경우에만 사용한다.

관련 `.cc`는 자기 header를 첫 include로 두어 누락 dependency를 즉시 드러낸다. public API에 implementation-only third-party type을 노출하지 않는다. PImpl은 compile boundary나 ABI 안정성이 실제 요구일 때만 사용한다.

## class, struct와 member

- class: invariant와 encapsulation이 핵심이며 data member는 constant 예외 외에 private
- struct: 서로 독립적으로 접근 가능한 passive data aggregate
- constructor: 완전한 invariant를 만들되 virtual call, 숨은 I/O와 실패 복구가 어려운 큰 작업을 하지 않음
- factory: construction failure, subtype 선택, ownership transfer를 return type으로 표현해야 할 때 사용

copy/move/destructor는 Rule of Zero를 우선한다. custom resource owner가 필요하면 copy 가능 여부와 move 후 상태를 명시한다. inheritance는 substitutable public interface 또는 framework contract일 때만 쓰고 implementation reuse만을 위해 선택하지 않는다.

## 함수와 parameter

결과는 return value를 우선한다. non-optional input은 value 또는 `const&`, non-optional output/in-out은 reference, optional pointer-like input/output은 pointer나 `std::optional`로 nullability를 드러낸다. input parameter를 output보다 앞에 둔다.

raw pointer/reference는 기본적으로 non-owning view다. ownership transfer는 `std::unique_ptr`; 실제 공동 수명일 때만 `std::shared_ptr`를 사용한다. `shared_ptr`를 lifetime 불확실성을 숨기는 기본값으로 쓰지 않는다. span/string_view 같은 view는 source보다 오래 살아남지 않게 한다.

overload는 caller에게 같은 개념의 명확한 계약을 제공할 때만 쓰고 default argument가 virtual dispatch나 source/binary compatibility를 흐리면 쓰지 않는다. boolean parameter가 호출 지점에서 의미를 숨기면 enum 또는 options value type을 사용한다.

## 언어 기능과 실패

- `nullptr`을 쓰고 C-style cast 대신 가장 좁은 C++ cast를 사용한다.
- `auto`는 type이 initializer에서 명확하거나 반복을 줄일 때 쓰고 ownership·numeric width를 숨기지 않는다.
- `const`, `constexpr`, `constinit`은 의미에 맞게 사용하며 강제 cast로 const를 제거하지 않는다.
- signed/unsigned 변환, narrowing, lifetime, iterator invalidation과 data race를 검증한다.
- exception 정책은 저장소와 ABI를 따른다. exception을 쓰면 basic/strong/no-throw guarantee와 destructor behavior를 정하고, 쓰지 않으면 status/result를 일관되게 전파한다.
- coroutine/module/template metaprogramming은 compile·debug·tooling 비용보다 계약 이점이 클 때만 도입한다.

## 검증

format → target standard compile → warning/static analysis → unit/integration test → Address/Undefined/Thread sanitizer와 필요한 benchmark를 실행한다. header self-containment, ODR, symbol visibility와 ABI 변화를 별도로 확인한다.

이 문서는 [Google C++ Style Guide](https://github.com/google/styleguide/blob/1809c769de31ba388c755ad15dd057a9ba8531fd/cppguide.html)를 Woon의 repository-first·ownership·점진 변경 기준으로 재작성했다.
