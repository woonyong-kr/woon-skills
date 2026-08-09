# 캐시 정합성 기준

## Pattern 선택

- cache-aside: application이 miss load와 invalidation을 소유한다. 단순하지만 DB commit 뒤 invalidation 유실 창을 다룬다.
- read-through: cache loader 계약과 원본 오류·timeout 전파를 검증한다.
- write-through: cache 성공이 source of truth commit을 의미하는지 실제 구현을 확인한다.
- write-behind: data loss window, ordering, durable queue와 reconciliation을 명시하지 않으면 사용하지 않는다.
- refresh-ahead: stale 허용과 예측 가능한 hot key에만 적용하고 실패 시 age 상한을 지킨다.

## Key와 invalidation

- key에 tenant, resource identity, projection/schema version과 authorization-sensitive variant를 포함한다.
- raw query string·locale·permission처럼 결과를 바꾸는 차원을 빠뜨리지 않는다.
- mutation은 source of truth commit 뒤 invalidation하거나 versioned key로 stale overwrite를 차단한다.
- out-of-order invalidation에는 version·sequence를 사용한다.
- list·aggregate cache는 한 entity 변경이 어떤 key를 무효화하는지 dependency를 관리한다.
- negative cache는 not-found와 transient error를 구분하고 짧고 측정된 TTL만 둔다.

## TTL·eviction·stampede

- TTL은 업무 stale tolerance, update frequency와 recovery 목표에서 도출한다.
- 같은 TTL 동시 만료를 막기 위해 bounded jitter를 사용한다.
- single-flight·request coalescing은 key별 in-flight를 하나로 줄이되 leader 실패와 wait timeout을 처리한다.
- stale-while-revalidate는 최대 stale age와 사용자 표시를 정한다.
- distributed lock만으로 correctness를 주장하지 않는다. lease 만료 뒤 stale writer에는 fencing/version 검증이 필요하다.
- eviction policy와 memory ceiling에서 required state가 사라져도 correctness가 유지돼야 한다.

## 검증

- cold miss, warm hit, eviction과 cache 전체 장애
- DB commit 직후 process kill과 invalidation redelivery
- 동시 N개 miss와 loader call 수
- old refresh가 new value 뒤에 도착하는 reorder
- tenant·permission이 다른 같은 resource key
- hot key, memory pressure, TTL 동시 만료

hit ratio만 보지 말고 p95 latency, origin load, stale age, invalidation lag, evictions와 incorrect-hit 수를 함께 측정한다.
