---
name: postgres
description: PostgreSQL query, index, EXPLAIN, transaction, lock, vacuum, connection과 schema 성능을 진단·최적화할 때 사용한다.
---

# Postgres

실제 PostgreSQL version, schema, statistics와 representative parameters를 확인한다. `EXPLAIN (ANALYZE, BUFFERS)`는 안전한 환경과 query에만 실행하고 estimated/actual row 차이, scan, sort, buffer, lock을 읽는다.

index는 query predicate·join·order와 write cost로 판단하며 무작정 추가하지 않는다. transaction scope, isolation, deadlock order, connection pool과 long-running query를 함께 본다. config 값과 batch size는 workload 측정 없이 임의 숫자를 제안하지 않는다.

변경 전후 같은 dataset과 query로 비교하고 migration 영향은 `$migration`으로 관리한다.
