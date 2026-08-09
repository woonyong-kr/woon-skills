---
name: domain
description: Domain-Driven Design의 bounded context, 공통 언어, entity·value object·aggregate, invariant와 domain event를 설계·검토할 때 사용한다. 서비스·transaction 경계가 업무 규칙과 어긋날 때도 사용한다.
---

# Domain

업무 규칙과 용어를 코드 구조보다 먼저 확정한다.

1. actor, command, outcome, invariant와 실패 조건을 실제 업무 문장으로 적는다.
2. 같은 용어가 같은 뜻을 갖는 범위로 bounded context를 나누고 context 간 번역 책임을 정한다.
3. identity가 필요하면 entity, 값 자체가 의미이면 immutable value object를 선택한다.
4. 한 transaction에서 즉시 지켜야 하는 invariant만 aggregate boundary 안에 둔다. 다른 aggregate는 ID로 참조한다.
5. aggregate root만 외부 mutation entry로 두고 생성 시점부터 invariant를 만족시킨다.
6. context·aggregate·event를 판단할 때 [도메인 모델 기준](references/model.md)을 읽는다.
7. 실제 원자성·동시성·멱등성은 `$tx`, port·adapter는 `$hexagonal`, 저장소 mapping은 해당 data skill에 맡긴다.

결과에는 context map, aggregate별 invariant·command·event, 즉시 일관성과 지연 수렴의 경계, 미확정 업무 질문을 구분한다. CRUD 화면, DB table 또는 조직도만 보고 aggregate·service를 만들지 않는다.
