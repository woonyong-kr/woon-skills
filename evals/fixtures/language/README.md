# Language convention fixture

`verify.sh`는 TypeScript, Java, Python, C, C++, C#의 최소 모듈을 실제 compiler/type checker로 검증하고 언어별 소유 경계를 정적으로 확인한다.

- public type과 함수 위치
- import/include self-containment
- C pointer length·output contract와 internal linkage
- C++ private invariant와 value semantics
- C# nullable·async와 private field naming
- Python mutable default·실행 guard

이 fixture는 문법·type·link와 선택된 구조 계약을 검증하지만 framework reflection, serializer, ABI 호환, sanitizer, multi-platform compiler와 production 동작을 증명하지 않는다. 실제 프로젝트에서는 저장소 formatter·analyzer·test와 target matrix를 추가한다.
