---
name: refactor
description: 외부 동작을 유지하면서 구조, 이름, 함수·클래스 경계, 중복 또는 dependency direction을 개선해 달라는 요청에 사용한다.
---

# Refactor

먼저 보존할 동작과 테스트를 적는다. 테스트가 없으면 현재 동작을 포착하는 characterization test 또는 최소 재현을 만든다.

1. smell이 아니라 실제 변경 이유와 책임 경계를 찾는다.
2. rename, extract, move, dependency inversion을 한 종류씩 작게 수행한다.
3. 공개 import, API, serialization, database schema 호환성을 확인한다.
4. 시각적 일관성만을 위해 새 type, layer, `Manager`/`Service`를 만들지 않는다.
5. 각 단계 뒤 좁은 테스트를 실행하고 마지막에 전체 관련 검증을 실행한다.

동작 변경이 필요해지면 refactor와 기능 변경을 분리해 사용자에게 알린다.
