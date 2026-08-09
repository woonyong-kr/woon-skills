# Java 규약

## 적용 순서

JDK·Gradle/Maven, formatter, Checkstyle/Error Prone, module/package 규칙을 먼저 읽는다. 실행 가능한 저장소 규칙이 없을 때 이 문서를 기본값으로 쓴다. 기능 수정과 무관한 전면 reformat·rename은 별도 변경으로 분리한다.

## source file과 import

한 `.java` 파일에는 같은 이름의 top-level type 하나만 둔다. UTF-8을 사용하고 package declaration은 줄바꿈하지 않는다.

import는 wildcard와 module import를 쓰지 않고 한 줄에 하나씩 적는다. static import와 non-static import를 각각 ASCII 순으로 정렬하고 두 block 사이에 한 줄만 둔다. static import로 nested class를 가져오지 않는다. formatter가 다른 자동 순서를 강제하면 formatter를 따른다.

## class 내용과 method 위치

class 내용은 고정된 공개/비공개 정렬보다 읽는 흐름과 책임을 우선한다. 다만 다음 계약은 유지한다.

- 같은 이름의 constructor·method overload는 중간에 다른 member를 끼우지 않고 연속 배치한다.
- field, constructor/factory, public behavior, package-private seam, private helper를 논리적 section으로 묶는다.
- private helper는 사용하는 public behavior 가까이에 두되 overload 묶음을 깨지 않는다.
- nested type은 enclosing type의 구현 세부일 때만 둔다. package 밖의 consumer가 알아야 하면 top-level 파일로 분리한다.

Google strict formatting은 2-space block indent, 100-column limit, K&R brace와 one statement per line을 쓴다. 저장소 formatter가 있으면 수동 정렬이나 column 맞춤을 하지 않는다.

## modifier와 visibility

modifier 순서는 다음을 기본으로 한다.

`public protected private abstract default static final sealed non-sealed transient volatile synchronized native strictfp`

annotation은 modifier 앞에 둔다. visibility는 compiler가 허용하는 가장 좁은 수준을 사용한다. `protected`는 의도된 subclass extension point, `public`은 package 밖의 stable contract일 때만 쓴다. test 편의로 production member를 넓히지 않는다.

## 이름

- package/module: lowercase dot segments
- class·interface·record·enum·annotation: `PascalCase`
- method·field·parameter·local: `lowerCamelCase`
- 실제 constant: `UPPER_SNAKE_CASE`
- type variable: `T`, `R` 또는 `RequestT`처럼 역할이 보이는 이름

acronym을 한 단어처럼 `HttpServer`, `XmlParser`로 적는다. interface에 `I` prefix를 붙이지 않는다. 구현에는 `Impl`, `Default`, `Manager`보다 strategy·adapter 의미를 사용한다.

## 언어 안전과 문서

- `@Override` 가능한 declaration에는 항상 붙인다.
- caught exception은 복구·변환·기록·rethrow 중 하나를 수행하며 빈 catch로 버리지 않는다.
- static member는 instance가 아니라 declaring class로 한정한다.
- finalizer를 사용하지 않고 resource는 `try-with-resources`와 명시적 lifecycle로 닫는다.
- public/protected API에는 caller가 알아야 할 invariant, side effect, nullability, exception을 Javadoc으로 적는다. type signature를 문장으로 반복하지 않는다.

format → compile → static analysis → unit/integration test를 실행하고 reflection, serialization, annotation processor, JPA proxy가 member move나 visibility 변경에 의존하는지 확인한다.

이 문서는 [Google Java Style Guide](https://github.com/google/styleguide/blob/1809c769de31ba388c755ad15dd057a9ba8531fd/javaguide.html)를 참고해 Woon의 domain ownership·좁은 visibility·점진 변경 기준으로 재작성했다.
