---
name: hexagonal
description: Hexagonal·Clean Architecture의 port·adapter 경계를 설계·검토할 때 사용한다. interface 추출, transaction·retry·idempotency, 오류·lifecycle, contract·integration test와 migration에도 사용한다.
---

# Hexagonal

business policy가 framework, database, network에 직접 의존하거나 경계의 책임·효과·검증 방법이 불명확할 때 적용한다.

## 작업 순서

1. 변경할 use case, 보존할 공개 동작, 외부 actor·system과 강제된 저장소 규칙을 확인한다.
2. interface·port·adapter·DTO·composition·폴더 경계를 판단하거나 migration할 때 [references/boundaries.md](references/boundaries.md)를 읽는다.
3. transaction·retry·timeout·idempotency·오류·동시성·lifecycle을 판단할 때 [references/effects.md](references/effects.md)를 읽는다.
4. fake·contract·integration·composition·architecture test 또는 migration 검증을 설계할 때 [references/testing.md](references/testing.md)를 읽는다.
5. 파일 위치·이름·공통 코드 품질은 `$quality`, 언어 표현은 해당 `$java`, `$python`, `$ts` 규칙을 함께 적용한다.
6. 선택한 경계 수준, port owner, contract, adapter, effect, composition, 검증과 미검증 위험을 구분해 보고한다.

port는 consumer가 소유하는 최소 contract다. 구현체 수나 폴더 대칭만으로 interface를 만들지 않는다. dependency direction은 이름이나 diagram이 아니라 import graph, contract와 실제 adapter test로 확인한다.
