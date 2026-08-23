# Approved Obsidian plugins

| ID | Community Plugin | Official release repository | Intended role |
| --- | --- | --- | --- |
| `light-mindmap` | Light Mindmap | `ninglg/light-mindmap` | 한 Markdown 문서의 heading을 학습·리허설·발표용 mindmap으로 렌더 |
| `markdown-mindmap` | Markdown Mindmap | `kikocastro/markdown-mindmap` | frontmatter 관계를 읽어 여러 Markdown 문서를 프로젝트·키워드·질문 지도로 렌더 |
| `context-calendar` | Context Calendar | `woonyong-kr/simple-calendar` | 날짜가 있는 일반 Markdown을 월간·Agenda·Context로 탐색한다. Woon source만 Core 설정으로 읽기 전용이다 |

## Local development allowlist

| ID | Source repository | Boundary |
| --- | --- | --- |
| `context-graph` | `woonyong-kr/context-tree` | 사용자가 명시적으로 승인한 수동 개발 검증에서만 `install-local-build`로 설치한다. 공식 release·Community Plugin 승인으로 간주하지 않는다. |
| `context-calendar` | `woonyong-kr/simple-calendar` | 자동 심사를 통과한 exact `2.0.2` source build를 receipt로 검증할 때만 사용한다. |

두 mindmap plugin은 Markdown 원본을 읽는다. `light-mindmap`의 node 편집은 heading을 바꾸므로 source diff와 link를 재검증해야 하고, `markdown-mindmap`은 map block의 folder·`parent` relation을 다시 읽어 card를 그린다.

`context-calendar`는 독립 사용 시 여러 folder profile, folder 안의 optional tag filter, 사용자 정의 property mapping과 writable source를 지원한다. Tag만으로 Vault 전체를 색인하지 않는다. Woon의 `inbox/calendar/events/` profile만 `editable: false`로 고정하며, Core는 `Date`, `Category`, 확인된 인물·관련 문서 링크를 생성한다. EventKit ID·장소·메모·참석자·URL은 projection에 넣지 않는다. Obsidian reload 뒤 `ribbon`, `month-view`, `event-card`, `context-links`, `readonly-blocked`를 모두 직접 확인하고 `attest-context-calendar-runtime`으로 남긴 operator attestation이 현재 asset·settings·dashboard hash와 일치해야 교체를 완료한 것으로 본다. 구형 `woon-simple-calendar`, `notion-bases`, `full-calendar-remastered`는 새 설치 대상이 아니라 이 검증 후 migration backup 대상이다.
