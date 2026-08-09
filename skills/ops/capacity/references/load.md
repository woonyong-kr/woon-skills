# 용량과 backpressure 기준

## Workload model

- 평균·peak·burst arrival rate와 시간대 변화를 분리한다.
- service time은 평균뿐 아니라 p50·p95·p99와 timeout을 측정한다.
- read/write 비율, payload, fan-out, tenant skew와 hot key를 기록한다.
- CPU, memory, connection, thread, file descriptor, queue와 downstream quota를 모두 후보 병목으로 둔다.

Little's Law `L = λW`는 안정된 구간의 추정에만 쓰고 unbounded queue·burst·retry storm을 가리지 않는다.

## Bounded resources

- queue와 executor는 명시적 상한을 두고 overflow에서 reject·defer·shed할 우선순위를 정한다.
- connection pool 크기는 DB capacity, transaction duration과 application replica 수를 함께 계산한다.
- worker 수를 늘리기 전에 downstream concurrency와 lock contention을 측정한다.
- batch는 throughput, memory, transaction time, partial failure와 retry 단위를 함께 비교한다.
- rate limit은 principal·tenant·operation별 공정성과 burst allowance를 정의한다.
- producer가 consumer보다 빠르면 pull, credit, token 또는 bounded blocking으로 backpressure를 전파한다.

## Overload와 recovery

- optional work를 먼저 shed하고 critical path의 예산을 보호한다.
- queue 대기 시간이 남은 deadline을 넘으면 실행 전에 거부한다.
- autoscaling signal은 이미 늦은 CPU만 보지 말고 queue age·concurrency·throughput도 검토한다.
- scale-out이 DB·broker·third-party bottleneck을 악화시키지 않는지 확인한다.
- 부하 제거 뒤 backlog와 retry가 recovery를 다시 무너뜨리지 않게 drain rate를 제한한다.

## 검증

- step·spike·soak·stress와 dependency slowdown을 분리해 실행한다.
- coordinated omission을 피하고 client-side end-to-end latency를 측정한다.
- queue depth·age, utilization, saturation, rejected work와 downstream calls를 기록한다.
- tenant 하나의 burst가 다른 tenant SLO에 미치는 영향을 측정한다.
- 한계 초과에서 무한 대기·OOM 대신 계약된 rejection/degradation이 발생하는지 확인한다.
