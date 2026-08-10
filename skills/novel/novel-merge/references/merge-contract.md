# 소설 대화 병합 계약

다른 AI와의 대화가 길거나 정본과 충돌하고, 단순 수정으로 identity를 판단하기 어려울 때만 읽는다.

## 입력 원장

novel 전체는 `private/local-only`다. 원본·파생본·분석·일기·계획은 복사하지 않고 하나의 inventory/catalog가 다음 필드를 소유한다.

| catalog 필드 | 규칙 |
|---|---|
| `path` | repository-relative 또는 local resolver ID; 머신 절대 경로 금지 |
| `kind` | original, derived, analysis, diary, plan, media, transcript 등 한 종류 |
| `short_abstract` | 파일을 열지 않고 내용·범위를 판단할 수 있는 비식별 1~3문장 |
| `provenance` | parent ID와 source ID; 원본이면 parent 없음 |
| `privacy` | 항상 private/local-only; public 승격 금지 |
| `status` | active, superseded, held, missing 등 현재 상태 |
| `timeline_range` | 정확한 날짜를 재노출하지 않는 내부 범위 표현 |
| `related_ids` | event·character·document ID; 제목 복제 금지 |

같은 path/content identity의 catalog 행을 두 개 만들지 않는다. media와 transcript는 서로 다른 kind지만 provenance로 연결하며 원본을 embedding하거나 catalog에 복사하지 않는다.

각 claim에 다음을 둔다.

| 필드 | 규칙 |
|---|---|
| `claim_id` | 이번 입력 안에서만 안정적인 ID |
| `source_locator` | 대화·파일·구간을 찾을 수 있는 비민감 locator |
| `class` | `사실`, `해석`, `허구`, `감정`, `결정`, `일정`, `미해결` 중 하나 |
| `event_id` | 확인한 기존 사건 ID 또는 신규 후보 ID; 추측으로 연결하지 않음 |
| `disposition` | `추가`, `병합`, `중복`, `충돌`, `보류`, `기각` 중 하나 |
| `reason` | identity, 근거, 충돌 또는 보류 이유 한 문장 |

입력의 모든 의미 단위가 정확히 한 행에 대응해야 한다. 인사·반복·도구 narration은 묶어 `기각`할 수 있지만 누락시키지 않는다.

## 사건 identity와 선형 연표

두 기록이 같은 사건인지 `행위·참여자·시간 범위·장소 범위·관찰 가능한 결과`로 판단한다. 표현이나 제목만 같으면 부족하고, 관찰 결과가 양립하지 않으면 별도 사건 또는 충돌이다. 기존 `event_id`를 우선하며 새 ID는 새로운 사건일 때만 만든다.

연표는 사건 ID를 한 번만 소유한다. 인물 문서·장면·해석은 연표를 복사하지 않고 사건 ID를 참조한다. 회상과 서술 순서는 별도 속성으로 두고 실제 사건 순서를 바꾸지 않는다.

문서는 길이·글자 수·고정 heading 때문에 나누지 않는다. 독립 질문, 독립 수정·재사용 책임 또는 선행 맥락 경계가 달라질 때만 분리한다. 같은 전제와 사건을 다시 설명해야 한다면 기존 정본에 병합하고 overview는 상세를 복사하지 않고 ID로 연결한다. summary는 사건 재서술이 아니라 채택·보류·반증 판단 기준만 소유한다.

## 병합 규칙

- `사실`: 원문이나 정본 근거가 있을 때만 갱신한다. 후속 교정은 이전 값을 삭제하지 않고 revision lineage로 대체 관계를 남긴다.
- `해석`: 근거 사건과 반증 조건을 둔다. 경쟁 해석은 하나를 사실로 승격하지 않는다.
- `허구`: 작가가 채택한 설정·장면과 AI 제안 후보를 분리한다.
- `감정`: 허구 인물의 정본 상태와 실존 인물에 대한 관찰·진술·추정을 분리한다.
- `결정`: 결정 주체, 시점, 선택한 안과 폐기·보류한 안을 기록한다.
- `일정`: 계획한 작업·만남과 이미 발생한 사건을 분리하고, 예정이 바뀌어도 과거 사건을 고치지 않는다.
- `미해결`: 답을 만들지 않고 필요한 증거와 다음 판단 조건을 기록한다.

원문은 append-only evidence이며 정정도 원문을 고치지 않는다. 정본 변경은 `before hash → claim disposition → catalog update → after hash → 검사 결과`로 추적한다. write 중 hash가 달라지면 병합을 멈추고 최신 정본에서 identity를 다시 판단한다. 외부 MCP나 외부 AI는 병합 경로에 포함하지 않는다.

## 완료 검사

1. 입력 claim 수와 disposition 원장 수가 일치한다.
2. 같은 사건 ID가 연표에 한 번만 존재한다.
3. 모든 정본 추가가 source locator 또는 명시적 작가 결정에 연결된다.
4. 충돌과 대안 해석이 삭제되지 않았고 반증 조건이 있다.
5. 실존 인물의 private 원문과 재식별 정보가 공개 영역에 새지 않는다.
6. 원문 hash는 변경 전과 같다.
7. 모든 자료 유형이 단일 catalog에 한 번만 있으며 필수 필드가 채워졌다.
8. 공개 repo 또는 외부 도구로 실명·원문·사진·음성·전사·정확한 날짜가 나가지 않았다.

하나라도 확인하지 못하면 `부분 반영` 또는 `미검증`으로 보고하고 완료라고 쓰지 않는다.
