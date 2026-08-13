# 공개 승격 계약

## 해결하는 실패

private 정본은 사실·증거·불확실성·내부 문맥을 최대한 보존한다. public 글은 독자와 목적에 맞게 선별해야 한다. 둘을 그대로 연결하면 다음 문제가 생긴다.

- private path·session ID·개인정보·회사 내부 자료가 노출된다.
- 같은 숫자와 소유권이 블로그·포트폴리오·이력서마다 달라진다.
- 기술 설명이 포트폴리오를 덮거나 성과 문구가 블로그의 설명력을 훼손한다.
- 초안 요청이 파일 반영·push·deploy 권한으로 확대된다.

이 스킬은 원문을 공개하는 도구가 아니라, 한 근거 집합을 목적별 public claim으로 승격하는 review queue다.

## Claim ledger

candidate 전에 표 또는 동등한 구조로 다음을 확정한다.

| field | 규칙 |
|---|---|
| claim_id | candidate 사이에서 같은 사실을 식별하는 안정 ID |
| statement | 공개 가능한 최소 사실. source 문장을 그대로 복사하지 않는다 |
| evidence | canonical_id와 revision, 필요하면 public code·test·asset |
| verification | current-verified, historical, inferred, unresolved 중 하나 |
| ownership | personal, team, post-project-personal 중 하나 |
| metric_context | 수치의 환경·입력·횟수·측정법. 없으면 숫자를 성과로 쓰지 않는다 |
| rights | public-approved, private, unknown 중 하나 |
| destinations | blog, portfolio 또는 둘 다 |

입력에 ownership이 없으면 `unresolved`, rights가 없으면 `unknown`이다. 작성 요청, source 보유, verification 상태나 인접 claim의 ownership으로 이 값을 추론하지 않는다. 예를 들어 개인 행동 claim 뒤의 수치 claim은 별도 ownership 근거가 없으면 `unresolved`다. `private`, `unknown`, `unresolved` claim은 공개 candidate 본문에서 제외하고 영수증에 이유를 남긴다. 본문이 전부 보류돼도 private field를 제거한 ledger의 최소 사실·verification·ownership·metric context·rights·destination은 유지한다. historical 기록은 현재 사실처럼 쓰지 않는다. 팀 성과는 개인 성과로 바꾸지 않는다.

private field는 ledger와 영수증 어디에도 raw value를 다시 쓰지 않는다. `private identifier 1건`, `이메일 1건`, `내부 경로 1건`처럼 유형과 건수만 기록한다. 가림 처리나 제외 설명도 원문 재출력 권한이 아니다.

## 승인 상태

1. `candidate`: 대화 안에서 검토할 글과 영수증만 만든다. 파일 write 없음.
2. `approved-for-source-write`: 사용자가 방금 본 candidate, destination과 포함 범위를 명시해 승인했다. 해당 `woon-site/content` source만 쓸 수 있다.
3. `validated`: 저장소의 required check와 실제 route/render를 확인했다. 이는 commit·push·deploy 승인이 아니다.
4. `published`: 별도 commit·push·deploy 요청과 live artifact 검증까지 끝난 상태다.

`좋아`, `진행해`, `알겠어`, `써 줘`, 과거 대화의 포괄 승인은 2단계로 바꾸지 않는다. 승격 승인은 다른 candidate나 destination에 재사용하지 않는다.

## 승격 영수증

candidate 끝에 다음을 짧게 붙인다.

```text
승격 상태: candidate — 승인 대기
근거: <canonical_id>@<revision> (<current-verified|historical>)
대상: <blog|portfolio|both>
포함 claim: <claim_id 목록>
제외·보류: <privacy, rights, ownership, evidence 사유>
예정 source: 승인 전 미정
권한 경계: file write 없음 · commit/push/deploy 별도 승인
```

승인 뒤에는 예정 source를 실제 상대 경로로 바꾸고 실행한 검증과 미실행 계층을 기록한다. machine-local 절대 경로는 영수증에 넣지 않는다.

## Public source 경계

- blog: `repo://site/content/posts/<slug>.md`
- portfolio: `repo://site/content/work/<slug>.md`
- portfolio 목록 선택: 사용자가 해당 항목을 명시적으로 선택했을 때만 `portfolio: true`
- 상단 고정: 사용자가 한 항목을 명시적으로 고정했을 때만 `portfolioPinned: true`

generated source와 deployment output은 직접 수정하지 않는다. 승인된 source write 뒤 대상 저장소가 선언한 `claims`, `images`, `build`, route/render 검증을 실행한다.
