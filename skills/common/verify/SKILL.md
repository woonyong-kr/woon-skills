---
name: verify
description: 구현·문서·설정 변경이 실제 요구를 만족하는지 테스트, 빌드, 정적 검사, 동작 확인으로 검증하고 근거와 한계를 보고할 때 사용한다.
---

# Verify

요구사항을 관찰 가능한 acceptance criteria로 바꾼다. 위험에 비례해 다음 계층을 좁은 것부터 실행한다.

1. 변경 파일 format과 lint
2. type/schema/config validation
3. 직접 관련 unit test와 regression test
4. 통합·빌드·CLI smoke test
5. UI는 실제 render, interaction, responsive state
6. 배포는 live artifact identity와 health

테스트가 통과해도 실행하지 않은 E2E·production을 추정하지 않는다. 실패는 명령, exit code, 재현 조건, 영향 범위로 보고한다. 현재 실행 결과만 증거로 쓴다.
