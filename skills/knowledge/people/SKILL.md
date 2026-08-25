---
name: people
description: Vault 문서의 소유자, 자료 저자·제공자, 발표자, 회의 참석자·협업자를 인물 카드와 역할로 연결하고 사람 기준으로 다시 찾을 때 사용한다. 이름만 언급된 자료나 Novel·민감 인물은 이 skill로 일반 지도에 넣지 않는다.
---

# People

`config/person-schema.json`과 [인물과 자료 연결 규칙](repo://knowledge/docs/person-knowledge-schema.md)을 먼저 읽는다. 이 skill은 연락처나 인물 소개를 만들지 않고, 한 사람이 관련된 문서와 역할을 다시 찾을 수 있게 연결하는 절차다.

## 작업 순서

1. `woon_people_find`로 같은 인물 카드를 먼저 찾는다. 이름이 비슷하다는 사실만으로 카드를 합치지 않는다.
2. 문서의 `record_owner`와 원자료의 `author`, `source-provider`, `speaker`, 회의의 `participant`, `organizer`를 분리한다. 별도 지시가 없는 Vault 기록의 소유자는 최우녕이다.
3. 이미 확인된 카드가 있으면 `woon_people_link_document`에 문서 상대 경로, 역할, 문서 안에서 확인한 근거를 함께 보낸다. 호출 뒤 `woon_people_documents`로 같은 문서가 정확히 한 번 연결됐는지 재조회한다.
4. 사용자가 "이 표기는 이 사람"이라고 직접 확인한 경우에만 `woon_people_set_identity_identifiers`로 `value`, 필요한 `context_terms`, 한 줄 근거를 기록한다. 새 general 한국어 실명 카드는 전체 이름과 성 제외 이름을 기본 식별자로 기록한다. 일반 `aliases`나 이름 유사도는 식별자로 쓰지 않는다.
5. 카드가 없으면 명시 요청 또는 서로 다른 자료에서 확인된 반복 관계가 있는지 확인한다. 둘 중 하나가 없으면 `attributions`에 이름·역할·근거만 남기고 카드를 만들지 않는다.
6. 카드 생성이 정당하면 `woon_people_upsert_card`에 `explicit-request` 또는 `repeated-evidence`를 명시한다. 목적은 "왜 이 사람 기준으로 문서를 다시 찾아야 하는가"로 한 문장만 쓴다.

## 문서별 선택

- 일반 source·회의·일일 기록·brain 후보: 이 skill의 local MCP로 역할 연결이 가능하다.
- compiler가 소유한 `wiki/`: 생성 Markdown을 직접 고치지 않는다. `$compile-knowledge`로 source·claim·page spec을 갱신하고 compiler receipt까지 확인한다.
- 이름은 있으나 카드 생성 근거가 없는 자료: `attributions`만 사용한다.
- Novel 원문, `wiki/private/_sources/**`, 실제 인물의 창작·민감 자료: 일반 인물 지도·검색으로 옮기지 않는다. 원문은 Wiki 내부 source 경계에 두고 확인된 작품·인물 관계만 기존 `wiki/private/**` 정본 아래에 연결한다.
- 자동 수집 메일·대화 후보: 사람 이름이나 관계를 추정해 카드·링크를 만들지 않는다. 후보 검토 뒤 명시된 사실만 이 skill으로 연결할 수 있다.
- Calendar 제목: Core가 `identifiers`의 정확한 표기만 local-only 일정 노트에 연결한다. `Woon 일정`에서 직접 만든 일정은 최우녕을 `organizer`로 연결한다. 같은 식별자가 여러 카드에 있으면 `inbox/review/calendar-person-identity-review.md`에 후보만 남기고 자동 연결하지 않으며, 사용자가 지정한 뒤에만 맥락 단어를 포함한 식별자를 갱신한다.
- Novel private history: 원문을 읽어 이름을 추정하지 않는다. `wiki/private/_sources/novel/work/work-catalog.yaml`과 `wiki/private/_sources/novel/work/people/person-link-ledger.yaml`은 source 입력 장부이며, 검증된 작품→인물·인물→작품 관계의 정본은 기존 `wiki/private/**` 작품·사람 subtree에 한 번만 기록한다. `inbox/private-person-history/**`나 source dashboard를 만들지 않는다. 원문 전체는 복사하지 않고 source locator·hash·확인 근거만 둔다. `review_candidates`가 있을 때만 Review를 만들고 승인 전에는 관계를 승격하지 않는다.

## 완료 기준

- 사람 카드가 생겼다면 작은 관계 대시보드만 있고, 추정한 신상·관계 설명은 없다.
- 연결 문서에는 `people`과 `person_roles`가 함께 있으며 role과 evidence가 빠지지 않는다.
- 사람 기준 재조회 결과에는 의도적으로 연결한 문서만 나온다.
- 기본 `people-index`와 전역 Graph에 Novel·민감 인물 카드가 나타나지 않는다.
- `novel-local-only` 카드의 직접 확인된 식별자는 local-only Calendar 노트에만 쓸 수 있고, 이 예외가 일반 지도·검색으로 번지지 않는다.
- private history 검증은 작품 catalog와 explicit relation ledger를 반복 실행해도 새 dashboard·링크·이력을 만들지 않으며, Novel 원문이나 전역 Graph를 바꾸지 않는다. 사람용 관계 갱신은 Wiki projection 한 경로만 소유한다.
- Calendar는 Novel 작품·관계·원문을 event나 task로 가져오지 않고, 사용자 확인 식별자의 local-only 사람 연결만 허용한다.

이 skill은 `repo://skills/skills/knowledge/people`의 단일 원본이며, Vault에는 사용 문서만 둔다.
