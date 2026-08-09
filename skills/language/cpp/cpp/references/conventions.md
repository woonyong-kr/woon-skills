# C++ 규약

## include와 declaration

include 순서는 관련 header → C system → C++ standard library → third-party → project header이며 non-empty group 사이에 한 줄을 둔다. group 내부는 정렬한다. generated build나 platform 조건이 요구하는 예외는 작은 범위에 격리한다.

class는 비어 있지 않은 section만 `public` → `protected` → `private` 순서로 둔다. 각 section 안에서는 다음을 기본으로 한다.

1. type alias·enum·nested type·friend type
2. struct의 public data member
3. static constant
4. factory
5. constructor·assignment
6. destructor
7. member function
8. remaining data member

같은 역할의 overload는 연속 배치한다. 큰 method definition을 class body에 넣지 않는다. `.cc` definition 순서는 header declaration 순서 또는 호출 흐름 중 하나를 선택해 유지하고 public API 이름을 찾기 어렵게 흩뜨리지 않는다.

## 이름

strict Google 기본값은 다음과 같다. 기존 repository formatter/naming이 다르면 섞지 않는다.

- file: lowercase, project가 허용한 `_` 또는 `-`; 규칙이 없으면 `_`; source `.cc`, header `.h`
- type·concept·type template parameter: `PascalCase`
- function: `PascalCase`; accessor/mutator는 field처럼 `snake_case` 허용
- variable·parameter·namespace: `snake_case`
- class data member: `snake_case_`; struct data member: `snake_case`
- constant·enumerator: `kPascalCase`
- macro: project prefix를 포함한 `UPPER_SNAKE_CASE`

acronym은 `StartRpc`처럼 한 단어로 처리한다. 공개 scope가 넓을수록 구체적인 이름을 쓰고 type을 반복하는 Hungarian notation을 쓰지 않는다.

## function과 format

return type과 function name은 가능한 한 같은 줄, opening parenthesis는 name과 같은 줄, opening brace는 마지막 signature 줄 끝에 둔다. parameter가 wrap되면 정렬하거나 4-space continuation을 사용한다. parameter name은 declaration에도 적되 override처럼 의미가 명백한 unused parameter만 생략한다.

Google strict mode는 2-space indent와 80-column 일반 한계를 사용한다. 그러나 `.clang-format`이 있으면 formatter가 정본이며 수동 vertical alignment를 만들지 않는다. namespace body는 별도 indent를 두지 않고 preprocessor directive는 block indent와 독립시킨다.

## comments와 변경

header declaration은 caller가 알아야 할 ownership, lifetime, thread-safety, side effect와 failure를 설명한다. `.cc` definition은 구현 선택의 이유를 설명하고 declaration 문서를 반복하지 않는다. 기존 비준수 파일 전체를 기능 변경에 섞어 reformat하지 않는다.

이 문서는 [Google C++ Style Guide](https://github.com/google/styleguide/blob/1809c769de31ba388c755ad15dd057a9ba8531fd/cppguide.html)의 include, declaration order, access, naming과 formatting 규칙을 조건부 strict mode로 정규화했다.
