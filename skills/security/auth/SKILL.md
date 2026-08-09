---
name: auth
description: OAuth 2.0·OIDC, session·cookie, token, service identity와 authentication·authorization lifecycle을 framework 독립적으로 설계할 때 사용한다. Spring Security 설정만에는 사용하지 않는다.
---

# Auth

authentication, token transport와 resource authorization을 서로 다른 결정으로 다룬다.

1. actor, client type, trust boundary, protected resource와 권한 결정을 정의한다.
2. [인증·인가 기준](references/flows.md)으로 flow, redirect, PKCE, issuer·audience, token storage·rotation·revocation을 설계한다.
3. 모든 object access에서 tenant·owner·role·scope·state를 함께 검증한다.
4. framework 설정은 `$spring-sec` 등 해당 skill, 일반 위협 검토는 `$security`, tenant 격리는 `$tenant`에 맡긴다.

UI 숨김, gateway 인증 또는 JWT signature만으로 authorization을 증명하지 않는다. 결과에는 trust boundary, flow, credential lifetime, deny-by-default policy와 negative test를 포함한다.
