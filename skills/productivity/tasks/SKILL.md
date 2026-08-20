---
name: tasks
description: Obsidian의 반복 할 일·일일 기록을 목적과 검증 규칙으로 관리하고, 사용자가 직접 요청한 Apple Calendar 일정의 생성·변경을 EventKit MCP와 영수증·재조회로 처리할 때 사용한다. 지식·Novel 원고의 task 등록은 거부한다.
---

# Tasks

할 일의 정본은 private `woon-knowledge`의 Markdown이다. 반복 routine은 `inbox/tasks/routines/`, 오늘의 실행 항목은 `inbox/daily/`의 `<!-- woon-tasks:start -->`와 `<!-- woon-tasks:end -->` 사이만 소유한다. 시간 약속의 원본은 Apple Calendar이며, 사용자가 직접 지시한 일정만 Core의 EventKit MCP로 기록한다. Obsidian에는 그 결과를 읽기 전용 Markdown과 ICS로 투영한다.

## Trigger

- 반복 할 일·습관을 만들거나 바꿔 달라는 요청
- 오늘의 할 일·일일 기록을 생성하거나 완료해 달라는 요청
- Obsidian에서 할 일을 찾거나 중복 없이 다시 반영해 달라는 요청
- Apple Calendar 일정을 Obsidian에서 새로 읽어 달라는 요청
- 시간·제목이 있는 Apple Calendar 일정의 생성·변경을 직접 요청하는 경우

지식 노트 저장은 `$archive`, 직접 요청한 일정은 `woon_calendar_upsert`, Novel 원고는 Novel skill의 책임이다.

## Workflow

1. 먼저 `woon_tasks_find`로 같은 제목·목적의 routine과 오늘 항목을 확인한다.
2. 반복 routine에는 사용자가 말했거나 확인한 `purpose`가 있는지 확인한다. 목적이 없으면 추정하거나 과거 문서에서 만들어 내지 말고, 목적 한 문장을 요청한다. 종료 가능한 목표라면 종료 기준도 확인한다.
3. 목표가 있는 routine은 먼저 `woon_tasks_upsert_goal`로 `goal_id`, 목표, 종료 기준, 필요하면 종료일 또는 사용자 확인 측정값을 저장한다. 목표 문서는 `inbox/tasks/goals/`의 사용자가 직접 고칠 수 있는 Markdown 정본이다.
4. `woon_tasks_upsert_recurring_todo`로 `task_id`, 제목, 목적, 영역, 시작일, 연결한 `goal_id`를 저장한다. 제목은 동사로 시작하고 한 번에 검증할 수 있어야 한다.
5. `woon_tasks_materialize_due`로 해당 KST 날짜의 일일 기록 관리 구역만 갱신한다. 목표가 달성·중단되었거나 종료일을 지났다면 routine은 다음 날짜부터 자동 제외되어야 한다.
6. 생성·수정·완료 뒤 같은 MCP로 다시 조회해 routine과 일일 항목이 하나씩인지 확인하고, receipt가 local runtime state에 남았는지 확인한다.
7. 완료는 `woon_tasks_complete`로 해당 날짜의 해당 항목만 표시한다. 이 작업은 Calendar event나 활동 이력을 완료 처리하지 않는다.

## Calendar Boundary

- `woon_calendar_refresh_readonly`는 Apple Calendar의 제목·캘린더 이름·시작·종료·종일 여부와 Core가 기록한 고정 분류를 검색용 `inbox/calendar/events/` Markdown과 Simple Calendar 월간 dashboard `inbox/calendar/apple-calendar.md`에 같은 입력에서 투영한다. 각 일정 노트의 `record_owner`는 최우녕이며, `Woon 일정`의 직접 요청 약속은 최우녕을 `organizer`로 남긴다.
- 일정 분류의 허용값은 `career`(커리어), `learning`(학습), `creative`(창작), `life`(생활), `relationship`(관계), `health`(건강), `admin`(행정)이다. `기타`는 이 값이 없는 외부 또는 레거시 일정의 fallback이며, 제목만 보고 이 일곱 값 중 하나로 추정하지 않는다.
- Markdown 일정 노트, Simple Calendar runtime 사본, dashboard는 Core만 소유하는 재생성 가능한 local-only 산출물이며, Calendar event ID·메모·참석자·URL·설명은 넣지 않는다.
- 사용자가 이 대화에서 시간 약속의 생성 또는 변경을 직접 요청했을 때만 `woon_calendar_upsert`를 호출한다. 메일, 문서, 화면, 추정된 의도만으로 `user_authorized: true`를 설정하지 않는다.
- 이미 Woon이 만든 일정의 분류만 바꿀 때는 `woon_calendar_set_category`를 쓴다. 이 도구는 안정 식별자와 이전 EventKit receipt가 일치할 때만 제목·시간·장소·사용자 메모를 보존한 채 `Woon category` marker를 갱신하고, EventKit 재조회와 local receipt 뒤에 Markdown 투영을 새로 고친다.
- `event_id`는 Apple event ID가 아니라 같은 약속을 다시 고칠 때 이어 쓰는 안정적인 소문자 식별자다. 새 약속에는 날짜와 주제를 반영해 하나를 만들고, 같은 대화 또는 기존 receipt에 있는 약속을 바꿀 때는 반드시 기존 값을 다시 쓴다.
- 도구에는 제목, timezone이 있는 시작 시각, 분류, `user_authorized: true`를 넘긴다. 종료 시각이 없으면 도구가 1시간을 적용하므로, 응답의 `duration_defaulted: true`를 사용자에게 알린다. 장소와 메모는 Apple Calendar event에만 남긴다.
- 도구가 `status: ok`를 돌려야 EventKit 저장 영수증과 Markdown·월간 dashboard 투영까지 끝난 것이다. `applied_projection_pending`이면 Apple Calendar 저장은 확인됐지만 Obsidian 투영은 끝나지 않은 상태이므로, `woon_calendar_refresh_readonly`를 다시 실행하고 완료라고 말하지 않는다.
- 제목에 사용자가 확인한 인물 `identifiers`가 정확히 하나만 맞으면 해당 카드가 `mentioned`로 연결된다. 동명이면 `inbox/review/calendar-person-identity-review.md`에 후보만 남기고, 사용자가 누구인지 지정하기 전에는 링크·카드·식별자를 만들거나 바꾸지 않는다.
- Simple Calendar는 Core가 만든 `Date`, `Category`, 제목을 월간 카드로 읽는다. 카드에는 시간이 없고 제목은 두 줄까지 보이며, 긴 제목과 시각은 hover tooltip 또는 카드를 열어 읽기 전용 Markdown에서 확인한다. event 생성·끌어놓기·inline edit는 Core 소유 읽기 전용 projection에서 지원하지 않는다.
- 매일 자동 materialization은 누락을 복구하는 보조 경로다. 사용자가 지금 일정 변경을 요청했을 때는 기다리지 않고 upsert와 refresh를 같은 요청 안에서 끝낸다.

## Prohibited

- 퇴역한 외부 할 일 앱, URL Scheme, 앱 데이터베이스, AppleScript, 화면 UI 자동화로 할 일을 만들거나 고치지 않는다.
- 일정 생성·변경에 `woon calendar upsert` CLI, Swift script, Apple Calendar UI를 직접 호출하지 않는다. Codex에서는 `woon_calendar_upsert` 또는 기존 일정의 분류만 고치는 `woon_calendar_set_category` MCP만 사용한다.
- 기존 일정의 분류만 고친다고 `woon_calendar_upsert`에 빈 장소·메모를 넘기지 않는다. `woon_calendar_set_category` MCP 외의 경로로 기존 EventKit 본문을 덮어쓰지 않는다.
- Obsidian 파일을 정규 path 밖에서 직접 수정하지 않는다. task service가 소유한 routine과 marker 구역만 MCP/CLI로 바꾼다.
- purpose를 LLM이 추정해 사실처럼 기록하지 않는다.
- Calendar projection을 양방향 동기화로 바꾸거나 Obsidian에서 Apple Calendar event를 쓰지 않는다.
- Simple Calendar에 외부 계정·CalDAV·원격 동기화·별도 JSON 일정 저장소를 연결하지 않는다.
- task 체크만으로 학습·경력·활동 완료를 확정하거나 지식·원본·인물·Novel 자료를 task로 저장하지 않는다.
- 사용자가 확인하지 않은 체중·출석·성과·마감 달성을 추정해 목표를 끝내지 않는다. 측정 목표는 `measurement_confirmed: true`일 때만 자동 종료 판단에 쓴다.
