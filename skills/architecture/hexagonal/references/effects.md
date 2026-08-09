# 경계 효과와 소유권

이 문서는 port와 adapter를 지나는 효과를 빠짐없이 찾고 해당 전문 스킬로 연결한다. transaction·retry·message·capacity의 상세 규칙을 복제하지 않는다.

## 효과 목록

| 효과 | 반드시 정할 내용 | 상세 소유자 |
| --- | --- | --- |
| local·remote write | 성공 관찰 시점, commit resource, unknown result | `$tx` |
| duplicate·retry | 업무 intent, key, owner, 전체 budget | `$tx`, `$resilience` |
| message·event | delivery, ordering, ack, replay | `$event` |
| background work | durable state, lease, checkpoint, cancel | `$job` |
| timeout·fallback | deadline, partial failure, degraded contract | `$resilience` |
| concurrency·queue | in-flight, backpressure, overload | `$capacity` |
| cache | source of truth, stale age, invalidation | `$cache` |
| tenant·credential | scope, isolation, authorization | `$tenant`, `$auth` |
| telemetry·audit | logical operation, attempt, privacy | `$observe`, `$privacy` |
| resource | create, share, close, shutdown | 이 문서 |

단순 read도 network, lazy loading, cache refresh와 credential rotation이 있으면 효과로 기록한다. effect를 숨기기 위해 port를 만들지 않는다.

## 오류 변환

- adapter는 vendor exception·status·driver code를 core가 판단 가능한 `invalid`, `conflict`, `transient`, `timeout`, `permanent`, `cancelled`, `unknown-result`로 변환한다.
- core는 업무 의미를 알 때만 기술 실패를 업무 실패로 바꾼다.
- inbound adapter는 내부 오류를 HTTP status, RPC status, CLI exit 또는 nack으로 변환한다.
- 원래 cause, operation, retryability와 correlation을 보존한다.
- 같은 실패를 layer마다 반복 log하지 않고 복구·대응 owner가 한 번 기록한다.
- secret, credential, raw query와 개인 payload를 오류·log에 포함하지 않는다.

vendor 오류 문자열 parsing은 adapter 한곳에 격리하고 contract test로 고정한다. catch-all로 빈 값이나 성공을 반환하지 않는다.

## Resource lifecycle

- thread-safe client, connection pool과 immutable config는 application scope로 공유할 수 있다.
- request, transaction, job과 tenant credential·mutable state는 해당 scope 밖으로 내보내지 않는다.
- singleton adapter에 request·tenant state를 저장하지 않는다.
- resource 생성과 close·dispose owner를 composition root에서 정한다.
- lazy initialization은 동시 첫 요청과 실패 후 재시도를 검증한다.
- shutdown은 새 작업 수락 중지→in-flight 처리·checkpoint→flush→resource 종료 순으로 수행한다.

## 완료 점검

- 각 side effect가 한 owner와 전문 스킬에 연결됐다.
- port contract에 SDK·ORM·transport type이 새지 않는다.
- adapter가 workflow·업무 성공 조건을 소유하지 않는다.
- 오류 변환과 log owner가 한곳이다.
- singleton에 request·tenant mutable state가 없다.
- 실행하지 않은 transaction·failure·production 검증을 통과로 표현하지 않았다.
