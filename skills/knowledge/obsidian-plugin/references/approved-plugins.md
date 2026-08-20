# Approved Obsidian plugins

| ID | Community Plugin | Official release repository | Intended role |
| --- | --- | --- | --- |
| `light-mindmap` | Light Mindmap | `ninglg/light-mindmap` | 한 Markdown 문서의 heading을 학습·리허설·발표용 mindmap으로 렌더 |
| `markdown-mindmap` | Markdown Mindmap | `kikocastro/markdown-mindmap` | frontmatter 관계를 읽어 여러 Markdown 문서를 프로젝트·키워드·질문 지도로 렌더 |
| `woon-simple-calendar` | Simple Calendar | `woonyong-kr/simple-calendar` official release | Core가 만든 local Markdown 일정을 읽기 전용 월간 카드 화면으로 표시하고 ribbon·명령 팔레트에서 dashboard를 연다 |

## Local development allowlist

| ID | Source repository | Boundary |
| --- | --- | --- |
| `context-graph` | `woonyong-kr/context-tree` | 사용자가 명시적으로 승인한 수동 개발 검증에서만 `install-local-build`로 설치한다. 공식 release·Community Plugin 승인으로 간주하지 않는다. |

두 mindmap plugin은 Markdown 원본을 읽는다. `light-mindmap`의 node 편집은 heading을 바꾸므로 source diff와 link를 재검증해야 하고, `markdown-mindmap`은 map block의 folder·`parent` relation을 다시 읽어 card를 그린다.

`woon-simple-calendar`는 `inbox/calendar/events/`의 Core 생성 Markdown만 읽는다. Core는 각 일정에 `Date`와 고정된 `Category`를 생성하고, `inbox/calendar/apple-calendar.md`에 month-only dashboard를 만든다. 이 파일 계열은 하나의 재생성 가능한 local-only projection이며, EventKit ID·장소·메모·참석자·URL·설명은 넣지 않는다. calendar block은 문서 작업 영역 전체를 사용한다. 카드에는 시간이 없고 제목은 두 줄까지 보이며, 전체 제목은 hover tooltip으로 확인한다. plugin의 신규 note 생성·drag·inline edit·외부 계정·CalDAV·원격 동기화는 지원하지 않으며 Core 파일 권한과 renderer 계약으로 차단한다. `notion-bases`와 `full-calendar-remastered`는 새 설치 대상이 아니라 migration backup 대상이다.
