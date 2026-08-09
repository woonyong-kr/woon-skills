# C 규약

## 파일과 include

- public header: `<module>.h`; implementation: `<module>.c`; internal header는 실제로 여러 source가 공유할 때만 만든다.
- source는 대응 header를 가장 먼저 include해 self-contained 여부를 드러낸다. 이후 C standard/system, third-party, project header를 blank line으로 나누고 각 group을 정렬한다.
- header 이름은 표준 library와 충돌하지 않게 구체적으로 짓는다. include guard는 project·path를 포함한 `PROJECT_PATH_FILE_H_`처럼 충돌을 피한다.
- conditional include와 platform branch는 작은 adapter/header로 격리한다.

## 선언 순서

저장소 규칙이 없으면 header는 public constant/type/function 순서, source는 include → private macro/constant → private type → static data → 필요한 prototype → function definition 순서로 둔다. 여러 variable을 한 declaration에 묶지 않고 선언과 초기화를 가능한 좁은 scope에 둔다.

## 이름

- file·function·variable·parameter·struct/enum tag: `lower_snake_case`
- macro와 compile-time constant: `UPPER_SNAKE_CASE`
- public symbol: `invoice_parse`, `invoice_error`처럼 module prefix
- predicate: `is_`, `has_`, `can_`; collection count: `_count`; bytes: `_bytes`

type 정보를 반복하는 Hungarian prefix를 쓰지 않는다. portable public type에 구현 예약 이름, leading double underscore, underscore+uppercase를 만들지 않는다. `_t` suffix는 POSIX namespace와 충돌할 수 있으므로 public Woon type 기본값으로 쓰지 않는다.

## 함수와 전처리기

function declaration에는 parameter name을 포함하고 declaration·definition signature를 한 source에서 검증한다. input을 먼저, output/in-out을 뒤에 둔다. 출력 하나면 return value를 우선하되 오류를 함께 반환해야 하면 명시적 status 계약을 쓴다.

function-like macro보다 `static inline` 또는 ordinary function을 우선한다. 불가피한 macro는 argument를 한 번만 평가하고 모든 parameter·전체 식을 괄호로 보호한다. 여러 문장 macro를 새로 만들지 않으며 기존 호환 macro는 `do { ... } while (0)`과 side-effect 검사를 적용한다.

## format와 확인

brace·indent·line length는 repository `.clang-format`이나 formatter를 따른다. Linux kernel의 8-space tab, GNU의 function layout 같은 project-specific 형식을 일반 C 기본값으로 섞지 않는다. Woon greenfield default는 2-space indent, K&R brace, one statement per line이지만 formatter config를 함께 커밋해 사람의 기억에 의존하지 않는다.

최소 검증 예시는 target에 맞춰 조정한다.

```bash
clang -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Werror module.c test.c
```

이 문서는 Google 독립 C guide가 없다는 [google/styleguide 목록](https://github.com/google/styleguide/tree/1809c769de31ba388c755ad15dd057a9ba8531fd)과 C 전용 1차 출처를 분리해 작성했다.
