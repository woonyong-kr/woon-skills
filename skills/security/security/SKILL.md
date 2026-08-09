---
name: security
description: 코드·설정·dependency의 auth, injection, secret, access control, supply chain과 threat를 보안 관점에서 검토·수정할 때 사용한다.
---

# Security

asset, actor, trust boundary와 공격 surface를 먼저 정한다. finding은 exploitable path, prerequisite, impact, evidence, remediation으로 쓴다.

input validation과 output encoding, SQL/command/path injection, SSRF, object-level authorization, secret exposure, insecure default, dependency provenance를 확인한다. scanner 결과는 source와 runtime reachability를 검증해 false positive와 구분한다.

secret 값은 출력하지 않고 `[REDACTED_SECRET]`로 표시한다. exploit이나 destructive test는 승인된 scope와 안전한 fixture에서만 수행한다. 수정 후 positive뿐 아니라 negative security test를 실행한다.
