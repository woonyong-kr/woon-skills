# Korean Wiki writing harness

## Purpose

이 문서는 Vault Wiki를 만드는 실행 계약이다. 코드, 기술, 조사, 결정, 사건, 절차, 학습 기록처럼 무엇을 기록하더라도 주제와 독자에 맞는 경로를 고르면서, 독자가 매번 자연스럽게 따라 읽고 다시 찾을 수 있게 하는 것이 목표다. 모든 문서를 같은 목차나 같은 말투로 보이게 하려는 계약은 아니다.

자연스러운 경험은 다음 순서가 독자에게 납득되는 상태다.

1. 지금 무엇을 보거나 해 보려는지 안다.
2. 현재 자료·상태·사건·코드에서 무엇이 일어나는지 안다.
3. 왜 그 결과가 문제이거나 중요한지 안다.
4. 필요한 용어와 구조가 그 장면을 어떻게 설명하는지 안다.
5. 비슷한 다음 상황에서 무엇을 확인할지 안다.

이 다섯 경험은 항상 필요하지만, 각 경험이 별도 section이나 같은 문장 수를 가져야 한다는 뜻은 아니다. 작성 과정은 `learning-content-quality.md`의 검증 gate와 `learning-style-corpus.yaml`의 교체 가능한 표본 근거를 함께 사용한다.

## Canonical lifecycle

Wiki는 읽기 좋은 글 하나로 끝나지 않는다. 자동 기록과 재열람이 같은 정본을 바라보도록 아래 lifecycle을 유지한다.

1. `capture`: 원본, 실행 결과, 관찰, 결정, 대화, 외부 자료를 원형과 공개 범위가 보존되게 받는다.
2. `source`: 무엇을 근거로 삼는지, 생성 시각·범위·제한이 무엇인지 기록한다.
3. `claim`: source가 직접 뒷받침하는 사실, 해석, 미결정을 분리한다.
4. `page`: 독자가 다시 찾을 질문에 맞춰 claim을 자연스러운 한국어 Wiki로 렌더링한다.
5. `receipt`: 어느 source·claim·page spec에서 이 페이지가 생성됐는지 남긴다.
6. `revisit`: 검색과 재열람에 필요한 title, purpose, exact term, section, source scope를 정본에 보존하고, 독자는 현재 답과 근거까지 되돌아갈 수 있어야 한다.

새 기록은 `purpose` 없이 정본에 저장하지 않는다. purpose는 작성 당시의 의도를 추정해 덧쓰는 필드가 아니라, 지금 왜 남기는지와 미래에 어떤 질문에 재사용할지를 적는 필드다. 민감하거나 local-only인 기록은 일반 Wiki, MCP, 공개 그래프 경로에 자동 편입하지 않고 별도의 privacy contract를 따른다.

## Claim unit contract

`claim`은 한 페이지 전체나 한 번의 대화 전체가 아니라, 나중에 source와 함께 다시 확인할 수 있는 한 가지 사실, 해석, 결정 또는 미결정이다. `statement`에는 그 단위를 한 문장으로 적고, `markdown`에는 그 질문을 설명하는 하나의 의미 덩어리만 둔다. 하나의 claim이 다른 장면, 다른 행위자, 다른 근거, 다른 시점으로 넘어가면 claim도 나눈다.

source-body legacy page는 원문을 보존하는 동안 예외로 둘 수 있지만, 새로 편집하거나 갱신하는 페이지는 claim을 section 단위로 나누고 각 claim의 `source_ids`를 실제 근거로만 좁힌다. 페이지는 claim을 이어 독자용 흐름을 만들고, receipt는 그 순서와 source를 다시 만들 수 있어야 한다. 이 구분은 자연스러운 본문을 잘게 잘라 검색용 사본으로 만들라는 뜻이 아니라, 설명의 의미 덩어리와 provenance의 검증 단위를 맞추라는 뜻이다.

## Input contract

본문을 쓰기 전에 아래 장부를 만든다. 이 장부는 독자에게 공개하지 않아도 되지만, 비어 있는 필드는 문장으로 추정하지 않는다.

```yaml
learning_brief:
  central_question: 독자가 이 문서를 읽고 답할 한 가지 질문
  reader:
    already_knows: [이미 사용할 수 있는 개념과 도구]
    must_decide_or_do: 읽은 뒤 판단하거나 구현할 일
  evidence:
    source_records: [원본, URL, 실행 결과, 결정 기록, 관찰 기록]
    facts: [source가 직접 뒷받침하는 사실]
    interpretations: [사실과 구분한 현재 해석]
    code_snapshot: 현재 설명할 source revision 또는 없음
    runtime_status: actual | expected | static-only | source-only | not-applicable
  scene:
    observable: 독자가 먼저 볼 코드, 값, 명령, 오류, 원문 장면 또는 판단이 나온 상황
    expectation: 이 장면에서 처음에는 무엇을 예상하는가
    tension: 예상과 실제가 갈라지는 지점 또는 해결해야 할 일
  boundaries:
    in_scope: 이번 문서가 끝까지 설명할 범위
    later: 지금은 이름만 남기거나 다음 문서로 넘길 범위
  canonical:
    purpose: 미래에 어떤 질문에 다시 쓸 문서인가
    exact_terms: [바꾸면 안 되는 identifier, 인명, 문서 이름, 제품명 또는 전문 용어]
    visibility: private | local-only | internal | publishable
    revisit_questions: [나중에 이 문서를 다시 열 질문]
```

`central_question`, `observable`, `evidence.source_records`, `canonical.purpose`, `canonical.visibility` 중 하나라도 비어 있으면 최종 본문을 만들지 않는다. source가 부족하면 그 사실을 단정하는 문장 대신 필요한 source를 요청하거나, 확인 가능한 범위만 남긴다. 해석은 사실 문장처럼 렌더링하지 않는다.

## Adaptive route selection

문서는 아래 route 중 하나를 시작점으로 고른다. route는 표면 목차가 아니라 독자가 처음 건너야 할 이해의 간격을 뜻한다. 여러 route를 섞을 수 있지만, 필요 없는 단계를 채우지 않는다.

| 독자가 건너야 할 간격 | 시작 route | 이어서 필요한 단계 |
| --- | --- | --- |
| 같은 작업이 반복되거나 코드가 읽기 어렵다 | `repeat-to-structure` | 반복 장면 → 비용 → 분리 코드 → 다시 읽기 |
| 한 값의 변경이 다른 곳을 바꾼다 | `expected-to-actual` | 예상 → 실제 결과 → 값·참조 추적 → 해결 비교 |
| 호출 순서, 자원, 예외처럼 중간 단계가 중요하다 | `flow-to-cause` | 정상 흐름 → 실패 삽입 → 끊긴 지점 → 복구 또는 전파 |
| 메모리, 수명, 권한처럼 보이지 않는 상태를 다룬다 | `visible-to-hidden` | 관찰 가능한 장면 → 보이지 않는 상태 가설 → 상태 그림 → 근거로 역검증 |
| 두 기술이 비슷해 보여 구분이 어렵다 | `same-question-contrast` | 같은 질문 → 기준 하나 → A 결과 → B 결과 → 선택 경계 |
| 명령·도구·절차 자체가 목표다 | `goal-to-workflow` | 완료 상태 → 최소 명령 → 출력 판정 → 실패 시 다음 확인 |
| 사건, 회의, 대화, 관찰을 다시 찾아야 한다 | `record-to-meaning` | 시간·원본 → 확인한 사실 → 현재 해석 → 미결정 → 재열람 질문 |
| 여러 자료를 읽고 하나의 판단을 남긴다 | `source-to-decision` | 질문 → 자료별 사실 → 충돌·한계 → 선택한 판단 → 되돌릴 조건 |
| 개념은 알지만 현실에서 언제 쓰는지 모른다 | `concept-to-application` | 익숙한 상황 → 개념 모델 → 적용 사례 → 적용하지 않는 경계 |
| 짧은 참고가 목적이다 | `answer-with-anchor` | 직접 답 → 가장 작은 근거 → 적용 경계 → 관련 질문 |

어느 route라도 `정의부터`, `목차 채우기`, `용어 나열`로 시작하지 않는다. 반대로 독자가 이미 겪은 장면을 길게 연기하지도 않는다. `reader.already_knows`와 `scene.observable`에 맞춰 가장 짧은 경로를 고른다.

## Writing state machine

LLM은 아래 상태를 순서대로 검토하고, 선택한 route에 필요한 상태만 본문으로 렌더링한다. 상태 이름은 내부 제어용이며 heading으로 그대로 출력하지 않는다.

| 상태 | 들어오는 정보 | 본문에서 하는 일 | 다음 상태로 넘어갈 조건 | 금지 |
| --- | --- | --- | --- | --- |
| `anchor` | central question, reader goal | 독자가 실제로 볼 장면, source, 현재 상태, 판단 또는 완료 목표를 잡는다 | 독자가 무엇을 확인할지 한 문장으로 알 수 있다 | 추상 정의, 역사로 시작 |
| `baseline` | code, source, value, event, command, normal output | 현재 상태를 최소한으로 보여 준다 | 대상과 기대 결과가 고정됐다 | 이후 개선·해석과 현재 상태를 섞기 |
| `tension` | expectation, actual, cost, conflict | 예상과 실제의 차이 또는 기록해야 할 이유를 드러낸다 | 독자가 다음 설명이 왜 필요한지 안다 | 근거 없는 위기감, 수사 질문 연속 |
| `trace` | source snapshot, event sequence, evidence | 값·참조·호출·자원·사실·결정 중 필요한 하나를 실제 이름으로 따라간다 | 원인이 추측이 아니라 근거 경로로 보인다 | source 전체를 문장으로 다시 읽기 |
| `name` | observed mechanism | 이미 본 현상에 짧은 이름을 붙인다 | 용어가 장면 하나와 연결됐다 | 용어집, 약어만 먼저 제시 |
| `change` | alternative action, interpretation, or code | 해결·개선·선택을 제시한다 | 이전 장면과 비교 가능한 변경점이 있다 | 새 행동이나 코드를 정답처럼 던지기 |
| `verify` | same input, source, output, comparison | 같은 기준으로 변화·사실·결정이 맞는지 보인다 | 무엇이 그대로이고 무엇이 달라졌는지 말할 수 있다 | 실행하지 않은 값을 실제 결과라고 쓰기 |
| `boundary` | scope, exception, trade-off, uncertainty | 이 설명이 적용되지 않는 조건과 지금 생략할 깊이를 밝힌다 | 과장된 일반화가 제거됐다 | 예외 목록을 본문보다 길게 만들기 |
| `transfer` | reader goal, revisit question | 다음 코드·자료·결정에서 다시 쓸 확인 질문을 남긴다 | 독자가 한 가지 행동이나 판단을 할 수 있다 | 본문 전체를 다시 요약하기 |

`anchor → baseline → tension → trace → name → change → verify → boundary → transfer`는 가장 긴 route의 예시일 뿐이다. 예를 들어 짧은 참고는 `anchor → trace → boundary → transfer`만 사용하고, 비교 문서는 `anchor → baseline(A/B) → tension → trace → boundary`를 쓴다.

## Korean prose renderer

### 설명자의 위치

- 설명자는 독자와 같은 자료와 장면을 보는 사람처럼 쓴다. 실제로 함께 확인할 때는 “먼저 확인해보자”, “순서대로 따라가 보자”, “여기서 한 번 멈춰 보자”를 쓸 수 있다.
- 이 표현은 사고를 전환하는 지점에만 한 번 쓴다. 매 문단을 “이제”, “자”, “핵심은”으로 열어 진행을 흉내 내지 않는다.
- 독자가 아직 몰라도 되는 깊이는 숨기지 말고, “지금은 이 범위까지만 이해하면 충분하다”처럼 현재의 학습 경계를 말한다. 다만 미룬 사실을 현재 결론의 근거로 쓰지 않는다.

### 문장과 문단

- 한 문단은 독자가 수행하는 생각 하나를 끝낸다. 장면을 보고, 결과를 보고, 이유를 이해하는 흐름은 보통 두세 문장이지만 문장 수를 목표로 세지 않는다.
- 같은 주체·같은 시점·직접 인과는 한 문장에 둔다. 예를 들어 “`b`가 가리키는 객체를 바꾸면 `a`도 같은 객체를 보고 있으므로 `a`의 출력도 함께 달라진다.”처럼 관찰과 이유가 한 호흡일 때가 그렇다.
- 독자가 장면을 본 뒤 판단해야 하거나, 행위자·시간·증거가 바뀌면 문장을 나눈다. “`b`만 바꿨다고 생각했다. 그런데 실행 결과에서는 `a`도 바뀌었다.”처럼 예상과 실제를 분리할 때가 그렇다.
- `-고`, `-며`, 쉼표로 원인·대조·조건을 감추지 않는다. 대등한 사실은 `-고`, 인과는 `그래서`·`-므로`, 대조는 `하지만`·`반면`, 조건은 `이때`·`-면`으로 드러낸다.
- 주어는 기계적으로 반복하지 않지만, 책임 주체가 바뀌면 다시 쓴다. `사용자`, `브라우저`, `TLS`, `CA`처럼 누가 선택·검증·변경하는지 되짚지 않게 한다.
- "정책적 의미를 부여한다", "신뢰를 수행한다"처럼 명사를 겹치지 않는다. "PintOS가 `struct thread`에 tid와 상태를 기록해 실행 단위로 다룬다"처럼 주체·동작·대상을 쓴다.

### 용어와 코드

- 먼저 장면을 보여 주고, 그 장면을 부를 필요가 생겼을 때 용어를 도입한다. “이처럼 한 곳의 변경이 다른 곳에 예상 밖으로 영향을 주는 일을 사이드 이펙트라고 한다.”처럼 이미 본 결과에 이름을 붙인다.
- 기술 용어, API, code identifier, 고유한 사건·문서 이름은 원문 표기를 유지한다. 처음 한 번은 쉬운 한국어 역할을 붙이고, 이후에는 같은 이름을 쓴다.
- code, 인용, 표, timeline, diagram 전에는 지금 이 근거가 답할 질문을 한 문장으로 적고, 뒤에는 독자가 실제로 확인할 값·순서·사실·대조 하나를 짚는다. 근거 전체를 문장으로 줄줄이 번역하지 않는다.
- 실제 output·관찰·인용이면 근거 상태를 표시하고, 예상 결과·해석이면 그 성격을 같은 위치에 표시한다. 실행 결과의 정확한 형식은 quality gate를 따른다.

## Block contracts

필요한 block만 사용한다. block의 순서는 route가 결정하고, 같은 block을 한 문서에서 반복할 때는 새 질문이나 새 source snapshot이 있어야 한다.

| block | 최소 입력 | 독자에게 남겨야 할 것 | 작성 확인 |
| --- | --- | --- | --- |
| 장면 | concrete code/value/failure/goal | 지금 확인할 대상 | 첫 문장만 읽어도 무엇을 보는지 안다 |
| 근거 | source snapshot, record, code, quote, table, timeline | 장면 또는 판단을 확인할 최소 근거 | 근거 밖의 설명과 identifier·범위가 같다 |
| 결과 | runtime status, observation, output, decision | 예상·실제 차이 또는 완료 판정 | 결과의 증거·해석 상태가 바로 위에 있다 |
| 추적 | one causal or evidential path | 값·호출·상태·사실·결정 중 하나의 이동 | 한 block에 두 개 이상 경로를 섞지 않는다 |
| 용어 | observed mechanism | 이미 본 장면의 짧은 이름 | 용어가 장면보다 먼저 나오지 않는다 |
| 그림 | a specific question | prose만으로 어려운 관계 | source snapshot과 방향·이름이 같다 |
| 비교 | common question | 선택 기준 하나 | 표가 설명을 대신하지 않는다 |
| 경계 | non-goal or exception | 이번 결론의 적용 범위 | 새 핵심 개념을 갑자기 도입하지 않는다 |
| 적용 | nearby next task | 다음 행동 또는 진단 질문 | 정답 암기가 아니라 확인 행동이다 |

## LLM execution protocol

LLM은 최종 Markdown을 바로 쓰지 않는다. 아래 산출물을 내부에서 만든 뒤, 각 gate를 통과할 때만 다음 단계로 이동한다.

```yaml
writer_state:
  1_plan:
    output: learning_brief + selected_route + candidate_sections
    gate: central_question, evidence, observable, boundary가 비어 있지 않다
  2_trace:
    output: source identifier별 값·호출·상태 변화와 근거
    gate: 설명할 경로가 source snapshot 또는 명시한 예상에 연결된다
  3_outline:
    output: section별 독자 질문, 사용하는 state, 필요한 block
    gate: 고정 목차가 아니라 route에 필요한 section만 남았다
  4_draft:
    output: 한국어 본문, 필요한 근거 block, diagram
    gate: 새 용어는 먼저 관찰됐고 각 근거 block의 역할이 다르다
  5_reader_pass:
    output: 문단 연결, 주어, 연결어, 중복을 고친 본문
    gate: 소리 내어 읽어도 주체·원인·대상이 흐려지지 않는다
  6_evidence_pass:
    output: source, runtime status, identifier, scope를 대조한 기록
    gate: quality gate의 hard fail이 없다
  7_archive_pass:
    output: source, claim, page spec, receipt와 visibility를 대조한 기록
    gate: purpose와 재열람 질문이 남고, 사실·해석·미결정·공개 범위가 섞이지 않는다
```

`1_plan`에서 route를 고른 이유와 `3_outline`에서 생략한 state를 기록한다. 이 기록은 receipt나 작성 로그에는 남길 수 있지만, 독자용 본문에 기계적인 단계 목록으로 노출하지 않는다.

## Reject rules

아래 결과는 자연스러운 학습 문서가 아니라는 신호다.

- 모든 문서에 같은 10개 heading을 만들거나, 정한 글자 수를 채우려고 빈 section을 만든다.
- 첫 문장이 용어 정의, 사전식 설명, 역사, "핵심은" 같은 결론 표어다.
- 한 줄 문단을 연속해 놓고 설명의 호흡을 잃는다.
- code, 인용, 표, output, diagram이 같은 말을 반복하거나 서로 다른 source snapshot을 설명한다.
- 문제를 만들기 위해 사실보다 큰 실패를 꾸미거나, 실행하지 않은 output을 실제라고 쓴다.
- 독자가 이미 아는 내용을 길게 되풀이하거나, 아직 모르는 심화 개념을 결론의 전제로 쓴다.
- 어려운 용어를 모두 한국어로 바꿔 정확한 identifier를 잃거나, 반대로 영어 용어만 나열해 역할을 숨긴다.
- 기록의 사실, 현재 해석, 반대 근거, 미결정을 한 문장 안에서 같은 확실성으로 섞는다.
- purpose 없이 새 지식을 저장하거나, visibility를 확인하지 않고 private 기록을 일반 검색 경로에 넣는다.

## Final reader check

완성 직전에 작성자는 각 문서에 맞는 질문만 골라 확인한다.

1. 첫 문단에서 독자가 보고 있는 자료·값·사건·상황을 상상할 수 있는가?
2. 정의를 읽기 전에 왜 이 설명이 필요한지 알 수 있는가?
3. 결과가 예상과 다르면, 그 차이가 문서 중간에 실제로 드러나는가?
4. 용어를 빼도 관찰과 원인이 남고, 용어를 넣으면 더 정확해지는가?
5. code, 인용, 표, output, diagram이 각각 다른 질문에 답하는가?
6. 사실, 해석, 미결정, 공개 범위가 구분되어 있는가?
7. 마지막 문장이 다음 행동·판단·재열람 질문을 남기며, 앞 문단을 슬로건처럼 반복하지 않는가?
8. 이 문서만의 route를 골랐는가, 아니면 고정 목차를 채웠는가?
