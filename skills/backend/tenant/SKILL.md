---
name: tenant
description: multi-tenant backend의 tenant identity, data·cache·queue·compute 격리, authorization, quota, noisy neighbor, shard·region 배치와 tenant migration을 설계·검증할 때 사용한다.
---

# Tenant

tenant를 선택 가능한 request parameter가 아니라 신뢰 경계를 통과해 전파되는 security context로 다룬다.

1. tenant identity의 authoritative source와 user↔tenant membership을 정한다.
2. [테넌트 격리 기준](references/isolation.md)으로 shared·pooled·silo model을 component별로 선택한다.
3. DB query, cache key, message, job, log와 object storage 전 경로에 tenant context가 유지되는지 검증한다.
4. 인증은 `$auth`, object access는 `$security`, capacity fairness는 `$capacity`, privacy는 `$privacy`를 함께 적용한다.

UI·hostname·client가 보낸 tenant ID만 신뢰하지 않는다. 결과에는 isolation matrix, blast radius, quota, migration, negative test와 미검증 infrastructure 경계를 포함한다.
