# 인증·인가 기준

## OAuth·OIDC flow

- browser·native public client는 Authorization Code + PKCE를 사용하고 implicit grant를 사용하지 않는다.
- redirect URI는 exact match allowlist로 검증하고 open redirect를 차단한다.
- `state`로 authorization response CSRF를 방어하고 OIDC `nonce`로 ID token replay를 확인한다.
- resource owner password grant를 새 설계에 사용하지 않는다.
- service-to-service는 workload identity 또는 제한된 client credential을 사용하고 사람 token을 재사용하지 않는다.

## Token 검증과 저장

- signature와 허용 algorithm뿐 아니라 issuer, audience, expiry, not-before와 key rotation을 검증한다.
- ID token을 API access token으로 사용하지 않는다.
- access token은 짧게, refresh token은 rotation·reuse detection과 revocation 경로를 둔다.
- browser session cookie는 `Secure`, `HttpOnly`, 적절한 `SameSite`, rotation과 CSRF 방어를 갖춘다.
- token을 URL, log, localStorage 기본값, source와 fixture에 노출하지 않는다.
- introspection·JWKS 장애의 fail-open/fail-closed 정책과 cache age를 명시한다.

## Authorization

- route 접근 뒤 object-level authorization을 별도로 확인한다.
- principal, tenant, resource owner, action, scope와 resource state를 policy input으로 둔다.
- default deny와 최소 권한을 적용하고 admin bypass를 한곳에서 감사한다.
- service가 downstream에 호출자를 위임할지 자기 identity로 호출할지 명시한다.
- cache된 permission의 stale/revocation window를 검증한다.

## Negative test

- missing·expired·wrong issuer·wrong audience·revoked token
- redirect 변조, code replay와 refresh token reuse
- 다른 tenant·다른 owner의 같은 resource ID
- role은 맞지만 scope·state가 틀린 요청
- logout·권한 회수 직후 cache와 active session
- key rotation 중 old/new key와 unknown `kid`

실제 identity provider metadata와 표준 version을 확인하지 않은 설정은 `unverified`로 남긴다.
