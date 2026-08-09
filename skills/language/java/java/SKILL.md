---
name: java
description: Java package·파일 구조, class·interface·record·enum·method·field 위치, naming, visibility, exception을 일관되게 설계·정리할 때 사용한다.
---

# Java

JDK version, build tool, formatter/Checkstyle, package structure와 주변 type을 먼저 읽는다. repository 규칙이 없을 때만 이 기본값을 적용한다.

1. package는 layer 이름보다 domain responsibility와 dependency direction을 드러낸다.
2. top-level public type은 파일 하나에 하나만 둔다.
3. interface는 실제 대체 구현이나 외부 boundary가 있을 때 consumer가 필요한 최소 method로 만든다.
4. visibility는 compile되는 가장 좁은 수준을 쓴다. 습관적으로 `public`을 붙이지 않는다.
5. member order는 repository formatter를 따르고 관련 field·constructor·method를 가까이 둔다.
6. checked/unchecked exception은 caller의 recovery contract로 결정한다.
7. formatter, compiler, static analysis와 test를 실행한다.

상세 파일 배치와 naming, class/interface/method 기준은 필요할 때 [Java design](references/design.md)을 읽는다.
