# 멱등성 기준

## 목차

- 업무 의도와 key
- atomic claim과 replay
- 상태 machine
- retry와 unknown result
- retention과 보안

## 업무 의도와 key

- 최초 업무 의도를 아는 caller가 key를 생성하고 모든 같은-intent retry에 재사용한다.
- scope는 최소 `tenant/caller + operation + key`로 분리한다.
- 동일 parameter hash를 key로 대체하지 않는다. 같은 내용의 독립 주문·결제는 별도 의도일 수 있다.
- 같은 key의 canonical payload fingerprint가 다르면 `conflict`로 거부한다.
- canonicalization에 포함·제외할 field, Unicode·decimal·timestamp 표현을 고정한다.

## atomic claim과 replay

idempotency record와 local 업무 mutation을 가능한 한 같은 transaction에 둔다.

```text
absent --atomic claim--> processing --atomic mutation/result--> succeeded
                                  \--classified failure--> failed
                                  \--uncertain external effect--> unknown
```

- `succeeded`: 원래 status·stable response reference를 의미상 동일하게 replay한다.
- `processing`: 같은 worker가 진행 중인지 lease/fencing으로 판별하고 무한 대기하지 않는다.
- `failed`: 입력 수정이 필요한 permanent failure와 다시 시도 가능한 transient failure를 분리한다.
- `unknown`: 새 effect를 만들지 말고 provider 조회·correlation·reconciliation으로 귀결한다.
- duplicate request가 첫 요청과 경쟁해도 effect는 최대 한 번만 시작돼야 한다.

response 전체에 secret·시간 가변 header를 그대로 저장하지 않는다. 안정된 결과 ID와 필요한 public body만 보존한다.

## 상태 machine

- 상태 전이는 conditional update와 version/fencing token으로 보호한다.
- owner lease 만료만으로 이전 worker의 write가 안전해지지 않는다. downstream이 fencing token을 거부할 수 있어야 한다.
- process restart 뒤 `processing`을 조회해 resume·reconcile·fail 중 하나로 결정한다.
- terminal 상태를 임의로 되돌리지 않는다. 새 intent는 새 key와 새 record로 시작한다.
- authorization은 최초 요청뿐 아니라 replay 시 현재 caller가 결과를 볼 권한이 있는지 확인한다.

## retry와 unknown result

- 한 logical operation의 retry owner는 하나다.
- 총 attempt 수는 계층별 곱으로 계산해 중첩 retry를 탐지한다.
- write retry는 같은 key, 같은 canonical payload와 bounded deadline을 사용한다.
- timeout, broken connection과 caller cancellation은 effect 미발생 증거가 아니다.
- provider가 key 조회를 지원하면 먼저 조회하고, 없으면 업무별 reconciliation key를 저장한다.
- 새로운 key로 재호출하는 것은 기존 intent가 종결됐다는 증거 뒤에만 허용한다.

## retention과 보안

- retention은 client retry window, queue redelivery, 법적 보존과 storage 비용으로 정한다.
- 만료 후 같은 key가 새 intent인지 거부 대상인지 API contract에 명시한다.
- tenant가 다른 같은 key는 충돌하지 않되 scope 누락으로 data가 섞이지 않게 unique constraint를 검증한다.
- key를 인증 수단으로 쓰지 않고 로그에는 필요 시 hash·redaction을 적용한다.
- metric은 logical operation, physical attempt, replay, conflict, unknown과 reconciliation age를 구분한다.
