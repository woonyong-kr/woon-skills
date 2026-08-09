---
name: adr
description: Architecture Decision Record를 새로 작성하거나 대안·trade-off·결정 상태·후속 결과를 갱신할 때 사용한다.
---

# ADR

한 ADR에는 되돌리기 어려운 결정 하나만 담는다.

- Title: 결정 내용을 중립적으로 표현
- Status: proposed, accepted, superseded, deprecated
- Context: 제약과 해결할 문제
- Decision: 선택과 적용 범위
- Alternatives: 실제 검토한 대안과 기각 이유
- Consequences: 이점, 비용, failure mode, 운영 영향
- Verification: 결정이 유효한지 확인할 지표와 테스트

코드와 설정에서 확인되지 않은 배경을 만들지 않는다. 기존 결정을 바꾸면 원문을 덮어쓰지 말고 새 ADR에서 supersede 관계를 기록한다.
