# Approved Obsidian plugins

| ID | Community Plugin | Official release repository | Intended role |
| --- | --- | --- | --- |
| `light-mindmap` | Light Mindmap | `ninglg/light-mindmap` | 한 Markdown 문서의 heading을 학습·리허설·발표용 mindmap으로 렌더 |
| `markdown-mindmap` | Markdown Mindmap | `kikocastro/markdown-mindmap` | frontmatter 관계를 읽어 여러 Markdown 문서를 프로젝트·키워드·질문 지도로 렌더 |
| `link-calendar` | Link Calendar Navigator | `woonyong-kr/link-calendar` | 날짜가 있는 Markdown을 월간 보기와 날짜별 정본 링크로 탐색한다. Woon source만 Core 설정으로 읽기 전용이다 |
| `linked-graph` | Linked Graph Navigator | `woonyong-kr/linked-graph` | 현재 Markdown의 outgoing 1-hop을 기본 그래프와 목차로 탐색하고, hover·focus 동안만 실제 outgoing 2-hop을 미리 보며 지식이나 UI 상태를 저장하지 않는다 |
| `runnable-code-blocks` | Runnable Code Blocks | `woonyong-kr/runnable-code-blocks` | 21개 `run-<language>` fence를 browser 또는 named remote provider에서 명시적인 Run으로만 실행한다 |

## Local development allowlist

| ID | Source repository | Boundary |
| --- | --- | --- |
| `linked-graph` | `woonyong-kr/linked-graph` | exact `1.5.0` read-only current-note force graph build만 `install-local-build`와 receipt로 검증한다. edge-to-edge viewport와 unclamped ephemeral world, density-responsive spacing, bounds-based fit, pan·zoom, drag-reheated shared simulation, movable root, canonical parent navigation, dot-above-title-below labels, no static group captions, dot-only hover emphasis, no false root action outline, hover·focus·touch outgoing 2-hop preview, direct 120개·preview 48개 상한과 전체 Outline fallback, measured collision, metadata dot colour, neutral text, Obsidian `--graph-line` 기반 1px solid direct edges와 1px dashed preview edges를 실제 Obsidian에서 확인한다. `context-graph`는 이 설치가 검증된 뒤 backup retirement한다. |
| `link-calendar` | `woonyong-kr/link-calendar` | CI·release asset attestation을 통과한 exact `3.2.0` source build를 `install-local-build`와 receipt로 검증한다. 신규 source read-only 기본값, 낙관적 날짜 충돌 차단, 1회 Undo, 안전한 속성명과 source별 날짜 상태를 확인한다. 구형 `context-calendar`는 이 설치가 검증된 뒤 backup retirement한다. |
| `runnable-code-blocks` | `woonyong-kr/runnable-code-blocks` | exact `0.2.4` local build만 `install-local-build`와 receipt로 검증한다. 21개 `run-<language>` fence는 명시적인 Run에서만 실행하며 원격 우선·browser 우선·원격 끄기 설정과 결과 불명 시 중복 실행 차단을 확인한다. 프로젝트 소유 실행 서버·자동 실행·코드 저장·filesystem 접근·child process·runtime 자동 설치·PATH 변경은 허용하지 않고, named third-party provider로 source가 전송될 수 있음을 표시한다. DartPad는 compile API로 source를 전송하고 반환된 JavaScript는 CSS class로 숨긴 임시 sandboxed frame에서 실행한다. Obsidian reload 뒤 전체 언어 목록, 실제 provider 환경, 100 source lines + numbered trailing lines, IntelliJ Darcula syntax palette, compact 편집·Run·conditional Reset·Output을 직접 확인한다. |

두 mindmap plugin은 Markdown 원본을 읽는다. `light-mindmap`의 node 편집은 heading을 바꾸므로 source diff와 link를 재검증해야 하고, `markdown-mindmap`은 map block의 folder·`parent` relation을 다시 읽어 card를 그린다.

`link-calendar`는 독립 사용 시 여러 folder profile, folder 안의 optional tag filter, 날짜·시간·하루 종일·제목·분류 mapping과 writable source를 지원한다. Tag만으로 Vault 전체를 색인하지 않는다. Woon의 `inbox/calendar/events/` profile만 `editable: false`로 고정한다. Obsidian reload 뒤 `ribbon`, `month-view`, `event-marker`, `daily-agenda`, `direct-note-link`, `readonly-blocked`를 모두 직접 확인하고 `attest-link-calendar-runtime`으로 남긴 operator attestation이 현재 asset·settings·dashboard hash와 일치해야 교체를 완료한 것으로 본다. 구형 `context-calendar`, `woon-simple-calendar`, `notion-bases`, `full-calendar-remastered`는 새 설치 대상이 아니라 이 검증 후 migration backup 대상이다.
