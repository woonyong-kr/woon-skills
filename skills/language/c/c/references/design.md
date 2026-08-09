# C 설계 기준

## dialect와 경계

`-std`, compiler extension, target OS·CPU, endian, word size와 ABI를 먼저 기록한다. C11 프로젝트에 C23 syntax를 섞거나 embedded/freestanding code에 hosted library를 가정하지 않는다. 외부 binary·protocol·FFI 경계는 width, alignment, byte order와 ownership을 명시한다.

## header와 source 소유권

public header는 consumer가 단독 include해도 compile되어야 한다. 필요한 type을 직접 include하고 transitive include에 기대지 않는다. 공개할 항목만 둔다.

1. include guard 또는 저장소가 정한 `#pragma once`
2. 필요한 system/project include
3. public macro·constant·enum
4. opaque 또는 공개 struct type
5. public function declaration

구현 세부 struct, static data와 helper는 `.c`에 둔다. ABI에서 struct layout을 공개할 이유가 없으면 forward-declared opaque type과 constructor/destructor 또는 caller-owned API를 사용한다. header의 `static` 함수와 object definition은 복제 비용·주소 identity를 이해한 경우에만 둔다.

## 함수 위치와 linkage

public function은 header에 declaration, 한 source에 definition을 둔다. translation unit 전용 function/data는 `static`으로 internal linkage를 명시한다. 함수 순서는 formatter가 정하지 않으면 다음 중 하나를 module 전체에서 고정한다.

- 작은 module: public entry point 뒤에 호출 흐름 순서로 static helper
- prototype 최소화가 중요한 module: static helper를 첫 사용 전에 정의하고 public entry point를 뒤에 배치

두 방식을 한 파일에서 섞지 않는다. forward declaration은 mutual recursion, public entry-first 탐색, compiler attribute처럼 이유가 있을 때만 둔다. parameter가 없는 함수는 `f(void)`로 선언한다.

## data와 ownership

- public API는 `const` input, mutable in/out, nullable pointer를 구분한다.
- buffer는 pointer와 element count를 함께 받고 byte count인지 element count인지 이름에 표시한다.
- 소유권 이전은 함수명·문서·type 중 하나에 숨기지 말고 allocation/free pair와 allocator compatibility를 명시한다.
- return pointer의 owner와 lifetime, borrowed view가 가리키는 object의 수명을 적는다.
- struct는 관련 data invariant를 묶는다. 의미 없는 `void *context`는 callback boundary에서만 쓰고 type contract를 문서화한다.
- integer 변환, signed/unsigned 비교, overflow, array bound, string terminator와 object lifetime을 검증한다.

## 오류와 cleanup

module마다 error convention 하나를 선택한다: status enum/int + out value, nullable result + separate error, 또는 result struct. predicate boolean과 error code를 같은 반환값에서 혼용하지 않는다. caller가 구분할 failure를 조용한 default로 바꾸지 않는다.

여러 resource를 얻는 함수는 역순 cleanup을 한 경로에서 보장한다. `goto cleanup`은 중복 해제 방지와 단일 cleanup에 유리할 때 허용하되 초기화되지 않은 resource를 해제하지 않게 상태를 명시한다. `errno`는 실패 직후에만 읽고 보존이 필요하면 다른 호출 전에 복사한다.

## 검증

target compiler의 높은 warning을 error로 실행하고 가능한 경우 static analyzer, AddressSanitizer, UndefinedBehaviorSanitizer, thread/memory sanitizer, fuzz와 boundary test를 적용한다. sanitizer 성공은 다른 target ABI와 production 최적화 동작을 대신하지 않는다.

Google은 독립 C style guide를 제공하지 않는다. C 안전 계약은 [SEI CERT C](https://wiki.sei.cmu.edu/confluence/display/c/Introduction), 형식 선택 참고는 [GNU C standards](https://www.gnu.org/prep/standards/html_node/Writing-C.html)와 실제 저장소 formatter를 사용하며 이를 Google C 규칙으로 표시하지 않는다.
