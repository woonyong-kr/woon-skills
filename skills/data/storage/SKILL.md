---
name: storage
description: relational·document·key-value·wide-column·search·object storage를 access pattern, consistency, durability, partitioning, query와 운영 비용으로 선택·설계·검토할 때 사용한다.
---

# Storage

저장소 이름보다 데이터 권한, access pattern과 요구 guarantee를 먼저 고정한다.

1. entity size·cardinality, read/write/query, ordering, consistency, durability, retention과 growth를 측정한다.
2. [저장소 선택 기준](references/selection.md)으로 primary source, index·projection, partition key, replication과 failure semantics를 정한다.
3. 한 사실의 canonical owner를 하나로 두고 search·cache·analytics 복사본에는 rebuild·lag·reconciliation 계약을 둔다.
4. local transaction은 `$tx`, PostgreSQL tuning은 `$postgres`, cache는 `$cache`, migration은 `$migration`에 맡긴다.

polyglot persistence를 목적 없이 도입하지 않는다. 결과에는 요구 guarantee, 선택·거절 근거, data lifecycle, recovery와 대표 workload 검증을 포함한다.
