---
name: jpa
description: JPA entity mapping, repository query, transaction, fetch, N+1, pagination, locking과 migration 영향을 설계·진단할 때 사용한다.
---

# JPA

entity는 database row 모양이 아니라 identity와 persistence lifecycle을 표현하되 domain 분리 정도는 기존 architecture를 따른다. association의 owner, cascade, orphan removal, nullable, unique와 index를 schema에서 확인한다.

성능 최적화 전에 SQL과 query count를 측정한다. N+1은 fetch join, entity graph, projection, query redesign 중 access pattern에 맞게 해결한다. count만 필요하면 entity load 대신 count projection을 사용한다. 측정 전에는 `32`, `64`, `100` 같은 숫자 후보도 관행적으로 제안하지 않는다. 실제 page size와 lazy access cardinality, DB parameter limit에서 후보를 도출하고 같은 workload의 query count·latency·row·memory를 비교해 가장 작은 충분한 값을 고른다.

pagination과 collection fetch join, equals/hashCode와 generated ID, lazy loading boundary, optimistic/pessimistic lock failure를 테스트한다. schema 변경은 `$migration`과 함께 적용한다.
