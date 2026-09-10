---
name: verify
description: 구현·문서·설정 변경이 실제 요구를 만족하는지 테스트, 빌드, 정적 검사, 동작 확인으로 검증하고 근거와 한계를 보고할 때 사용한다.
---

# Verify

요구사항을 관찰 가능한 acceptance criteria로 바꾼다. 다음 중 변경 영향·위험에 필요한 계층만 선택한다. 모든 계층을 고정 순서로 실행하는 목록이 아니다.

1. 변경 파일 format과 lint
2. type/schema/config validation
3. 직접 관련 unit test와 regression test
4. 통합·빌드·CLI smoke test
5. UI는 실제 render, interaction, responsive state
6. 배포는 live artifact identity와 health

테스트가 통과해도 실행하지 않은 E2E·production을 추정하지 않는다. 실패는 명령, exit code, 재현 조건, 영향 범위로 보고한다. 입력 revision·환경·도구가 같은 기존 통과 근거는 재사용하고, 달라진 조건에 해당하는 검증만 다시 수행한다.
