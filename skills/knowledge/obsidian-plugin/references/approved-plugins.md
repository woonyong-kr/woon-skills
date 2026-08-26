# Approved Obsidian plugins

| ID | Community Plugin | Official release repository | Intended role |
| --- | --- | --- | --- |
| `light-mindmap` | Light Mindmap | `ninglg/light-mindmap` | 한 Markdown 문서의 heading을 학습·리허설·발표용 mindmap으로 렌더 |
| `markdown-mindmap` | Markdown Mindmap | `kikocastro/markdown-mindmap` | frontmatter 관계를 읽어 여러 Markdown 문서를 프로젝트·키워드·질문 지도로 렌더 |
| `link-calendar` | Link Calendar | `woonyong-kr/link-calendar` | 날짜가 있는 Markdown을 월간 보기와 날짜별 정본 링크로 탐색한다. Woon source만 Core 설정으로 읽기 전용이다 |
| `linked-graph` | Linked Graph | `woonyong-kr/linked-graph` | 현재 Markdown에 작성된 outgoing link 순서만 오른쪽 사이드바에서 탐색하며 지식이나 UI 상태를 저장하지 않는다 |

## Local development allowlist

| ID | Source repository | Boundary |
| --- | --- | --- |
| `linked-graph` | `woonyong-kr/linked-graph` | exact `1.1.0` read-only current-note build만 `install-local-build`와 receipt로 검증한다. `context-graph`는 이 설치가 검증된 뒤 backup retirement한다. |
| `link-calendar` | `woonyong-kr/link-calendar` | CI·release asset attestation을 통과한 exact `3.1.1` source build를 `install-local-build`와 receipt로 검증한다. 구형 `context-calendar`는 이 설치가 검증된 뒤 backup retirement한다. |

두 mindmap plugin은 Markdown 원본을 읽는다. `light-mindmap`의 node 편집은 heading을 바꾸므로 source diff와 link를 재검증해야 하고, `markdown-mindmap`은 map block의 folder·`parent` relation을 다시 읽어 card를 그린다.

`link-calendar`는 독립 사용 시 여러 folder profile, folder 안의 optional tag filter, 날짜·시간·하루 종일·제목·분류 mapping과 writable source를 지원한다. Tag만으로 Vault 전체를 색인하지 않는다. Woon의 `inbox/calendar/events/` profile만 `editable: false`로 고정한다. Obsidian reload 뒤 `ribbon`, `month-view`, `event-marker`, `daily-agenda`, `direct-note-link`, `readonly-blocked`를 모두 직접 확인하고 `attest-link-calendar-runtime`으로 남긴 operator attestation이 현재 asset·settings·dashboard hash와 일치해야 교체를 완료한 것으로 본다. 구형 `context-calendar`, `woon-simple-calendar`, `notion-bases`, `full-calendar-remastered`는 새 설치 대상이 아니라 이 검증 후 migration backup 대상이다.
