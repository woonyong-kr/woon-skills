# LLM·Agent 층별 진단 기준

## 관찰 경계

| 층 | 보존할 증거 | 대표 실패 |
| --- | --- | --- |
| system·policy | 최종 조립 순서, source, version, digest | 충돌, 중복, 오래된 규칙 |
| session history | 포함·제외된 turn과 truncation | 잘못된 과거 상태 재주입 |
| retrieval·memory | query, 후보, score, provenance, 상태 | 정정 전 사실, scope 누출 |
| model inference | provider, model, sampling, raw request·response | direct 기준본과 차이 |
| tool selection | 허용 toolset, 선택 이유, schema | prompt-only 강제, 잘못된 routing |
| tool execution | validated args, 실제 result, exit·error | 호출 생략, 허위 성공 |
| output validation | parse·schema·semantic 결과 | 형식 통과 후 의미 오류 |
| retry·repair | trigger, attempt, 비용, before·after | 숨은 재호출, 의미 변조 |
| renderer·transport | raw·rendered diff, link target | Markdown·JSON·링크 손상 |
| persistence·cache | key, version, TTL, invalidation | 과거 artifact를 현재 증거로 사용 |

하나의 `trace_id`로 위 증거를 연결하되 secret, private payload와 불필요한 전문은 저장하지 않는다. 민감 정보는 redaction하고 원문 보존이 불가능하면 digest와 승인된 보관 위치를 기록한다.

## 대조 순서

1. 사용자에게 보인 실패를 입력·model·tool fixture와 함께 replay한다.
2. wrapper를 우회한 direct inference를 같은 조건으로 실행한다.
3. 층을 하나씩 추가해 최초로 결과가 달라지는 지점을 찾는다.
4. 한 원인만 바꿔 고정 실패와 held-out 변형을 반복한다.
5. 정확성, tool 실행, repair 횟수, latency와 token을 기준본과 비교한다.

direct inference도 실패하면 model·prompt·task contract를 조사한다. direct는 통과하고 application만 실패하면 모델 교체보다 최초 변조 층을 먼저 수정한다.

## 필수 불변 조건

- 필수 tool은 실행 기록과 후조건 없이는 완료로 판정되지 않는다.
- schema의 required·type·enum·additional properties와 권한 범위는 실행 전에 검증한다.
- repair가 최종 JSON을 만들었어도 최초 통과율과 의미 변경률을 따로 보고한다.
- user correction은 이전 memory를 `superseded` 또는 `disputed`로 비활성화하며 이력을 지우지 않는다.
- similarity 단독으로 정본을 선택하지 않고 scope·검증·최신성·정정 관계를 함께 본다.
- renderer 결과만 저장해 model 원문과 변환 과정을 잃지 않는다.
- 관측하지 못한 층은 정상이라고 추정하지 않고 미검증으로 표시한다.

## 보고 형식

```text
증상과 재현 입력:
direct model 기준본:
최초 변조 층:
메커니즘과 근거:
영향과 심각도:
가장 작은 code-first 수정:
고정 회귀와 held-out 검증:
latency·token·repair 변화:
미검증 층과 남은 위험:
```

심각도는 실제 영향과 도달 가능한 경로로 정한다. 관측 가능한 근거 없이 “모델이 나빠졌다”, “memory가 오염됐다” 또는 “prompt가 약하다”고 단정하지 않는다.
