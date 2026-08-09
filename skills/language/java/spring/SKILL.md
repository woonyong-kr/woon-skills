---
name: spring
description: Spring Boot component, configuration, controller, service, transaction, dependency injection과 module 경계를 설계·검토할 때 사용한다.
---

# Spring

framework stereotype보다 business owner와 transaction boundary를 먼저 정한다. constructor injection과 immutable dependency를 기본으로 하되 repository convention을 따른다.

controller는 transport parsing·validation·response mapping을, application service는 use-case orchestration과 transaction을, domain은 framework-independent rule을 맡는다. `@Transactional`은 실제 consistency boundary에 두며 self-invocation과 lazy access를 검토한다. 모든 class를 `public` 또는 `@Service`로 만들지 않는다.

config property는 typed validation을 사용하고 secret default를 commit하지 않는다. Spring context를 띄우기 전 pure unit test가 가능한 policy는 분리한다.
