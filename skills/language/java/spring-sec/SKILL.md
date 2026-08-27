---
name: spring-sec
description: Spring Security의 authentication·authorization, SecurityFilterChain, method/object-level 권한, CSRF·CORS와 권한 negative test를 설계·검토할 때 사용한다. 권한 검증은 spring-test가 아니라 이 skill이 소유한다.
---

# Spring Security

보호할 resource, principal, permission, trust boundary를 먼저 정의한다. route matcher는 구체적인 rule부터 두고 default deny를 선호한다. authentication과 authorization을 분리하며 UI 숨김을 권한 검증으로 간주하지 않는다.

session/cookie면 CSRF, browser cross-origin이면 CORS의 정확한 origin·method·credential을 검토한다. JWT signature뿐 아니라 issuer, audience, expiry, key rotation을 확인한다. secret/token을 log나 test fixture에 넣지 않는다.

anonymous, wrong role, expired credential, object-level access를 포함한 negative test를 작성한다.
`@WebMvcTest` slice나 Spring context wiring 자체가 별도 검증 대상일 때만 `$spring-test`를 함께 쓴다.
