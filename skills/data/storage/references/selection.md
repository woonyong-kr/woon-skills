# 저장소 선택 기준

## 요구사항

- point read, range scan, join, full-text, graph traversal, append, blob 중 주요 access pattern을 순위화한다.
- per-key·per-aggregate·global ordering과 read-your-writes·monotonic read 필요를 구분한다.
- RPO·RTO, durability acknowledgement와 replica lag 허용을 수치로 정한다.
- 예상 cardinality, item size, growth, hot partition과 tenant skew를 측정한다.
- backup, restore, schema evolution, region·compliance와 운영 역량을 포함한다.

## 선택 원칙

- relational: constraint, transaction, join과 ad-hoc query가 핵심이면 우선 검토한다.
- document: aggregate 단위 read/write와 schema variation이 크되 cross-document invariant가 적을 때 검토한다.
- key-value: stable key의 low-latency access가 중심이고 secondary query가 제한적일 때 검토한다.
- wide-column: partition·sort key가 명확한 대규모 sparse workload에 사용한다.
- search engine: ranking·inverted index용 projection으로 두고 업무 정본으로 만들지 않는다.
- object storage: large immutable blob과 lifecycle에 사용하고 metadata transaction 경계를 별도 설계한다.

## Partition·replication

- partition key가 cardinality, distribution과 query를 동시에 만족하는지 실제 histogram으로 확인한다.
- cross-partition query·transaction 비용과 re-sharding 경로를 설계한다.
- replica read의 staleness와 failover 뒤 consistency를 API 계약에 반영한다.
- write acknowledgement가 memory, leader disk, quorum 중 어디까지 durable한지 확인한다.
- backup 존재가 restore 성공을 뜻하지 않으므로 point-in-time restore와 checksum을 정기 검증한다.

## 복사본과 검증

- canonical change에 version·event ID를 부여해 projection lag와 gap을 찾는다.
- index·search·analytics는 canonical source에서 재구축 가능해야 한다.
- dual write로 복사본을 동기화하지 말고 durable change stream/outbox와 idempotent projector를 사용한다.
- representative data volume에서 latency, throughput, cost, hot partition, failover와 restore를 측정한다.
