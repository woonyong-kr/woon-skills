---
name: spring-test
description: Spring Boot slice·integration test, MockMvc/WebTestClient, Testcontainers와 context failure를 작성·진단할 때 사용한다. SecurityFilterChain·object-level 권한 검증만이면 spring-sec를 사용한다.
---

# Spring Test

검증할 boundary에 맞춰 가장 작은 test를 선택한다: pure unit, `@WebMvcTest`, repository slice, full `@SpringBootTest`. 편의 때문에 모든 test에서 full context를 띄우지 않는다.

HTTP test는 status뿐 아니라 validation, serialization, auth와 error contract를 확인한다. database integration은 실제 dialect 차이가 중요할 때 Testcontainers를 쓰고 test data lifecycle을 격리한다. `@MockBean` 남용으로 wiring 문제를 가리지 않는다.

context cache, profile, dynamic property와 migration 상태를 확인하고 flaky sleep 대신 observable condition을 기다린다.
