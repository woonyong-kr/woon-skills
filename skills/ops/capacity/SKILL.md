---
name: capacity
description: backend의 traffic model, concurrency, queue, connection pool, rate limit, backpressure, load shedding, batch size와 scaling limit을 설계·측정·검증할 때 사용한다.
---

# Capacity

평균 처리량이 아니라 burst, tail latency와 bounded resource에서 안전한 한계를 찾는다.

1. arrival rate, service time distribution, concurrency, payload, tenant skew와 downstream quota를 측정한다.
2. [용량 기준](references/load.md)으로 queue·pool·limit·backpressure와 overload contract를 정한다.
3. retry·timeout은 `$resilience`, hot cache는 `$cache`, SLI는 `$observe`를 함께 적용한다.
4. steady, burst, soak, dependency slowdown과 recovery를 같은 workload model로 검증한다.

임의의 thread·connection·batch 숫자를 제안하지 않는다. 결과에는 가정, bottleneck, safe operating limit, rejection 정책, p50·p95·p99와 saturation·recovery 증거를 포함한다.
