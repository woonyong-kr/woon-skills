---
name: cache
description: cache-aside·read-through·write-through·write-behind, key·TTL, invalidation, stampede, stale data, negative caching과 tenant 격리를 설계·진단·검증할 때 사용한다.
---

# Cache

cache는 성능 복사본이지 암묵적인 두 번째 정본이 아니다.

1. source of truth, 허용 stale age, read/write ratio, cardinality와 miss 비용을 측정한다.
2. [캐시 정합성 기준](references/consistency.md)으로 pattern, key version, invalidation, TTL·eviction과 stampede 방어를 정한다.
3. correctness를 cache hit에 의존하지 않게 하고 miss·eviction·cache outage에서도 원본 계약을 보존한다.
4. DB commit과 invalidation의 crash window는 `$tx`, tenant key 격리는 `$tenant`, 용량과 hot key는 `$capacity`를 함께 적용한다.

TTL 숫자를 관행으로 복사하지 않는다. 결과에는 stale contract, key namespace, mutation 순서, failure mode, hit·miss·age·eviction metric과 cold/warm/concurrent 검증을 포함한다.
