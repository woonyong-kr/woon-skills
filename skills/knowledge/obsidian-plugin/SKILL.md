---
name: obsidian-plugin
description: Woon Obsidian Vault의 Community Plugin 상태를 확인하고, 승인된 공식 release나 사용자 소유 local development build를 receipt·backup·hash로 검증해 설치·활성화·제거할 때 사용한다.
---

# Obsidian Plugin

Obsidian plugin은 UI 조작이나 임의 폴더 복사로 관리하지 않는다. `$obsidian-plugin`은 Core의 receipt 기반 adapter만 사용한다.

```bash
woon knowledge obsidian-plugin status --vault <vault>
woon knowledge obsidian-plugin install --plugin <approved-id> --vault <vault>
woon knowledge obsidian-plugin install-local-build --plugin <approved-development-id> \
  --source-dir <built-plugin-directory> --version <exact-version> --vault <vault>
woon knowledge obsidian-plugin remove-detected-mindmaps --vault <vault>
woon knowledge obsidian-plugin configure-link-calendar --vault <vault>
woon knowledge obsidian-plugin attest-link-calendar-runtime \
  --attested-check ribbon --attested-check month-view --attested-check event-card \
  --attested-check daily-agenda --attested-check direct-note-link \
  --attested-check readonly-blocked --vault <vault>
woon knowledge obsidian-plugin retire --plugin notion-bases --vault <vault>
```

`status`는 설치 manifest, version, 활성 config, 설정 파일과 `mindmap` 판정을 read-only로 반환한다. 설치는 allowlist의 공식 GitHub release API와 release asset SHA-256을 확인하고, manifest `id`가 요청 ID와 같을 때만 stage → backup → atomic replace → `community-plugins.json` 갱신 → 재조회 순서로 진행한다. receipt와 backup은 Vault의 Git 제외 `.local/woon-knowledge/obsidian-plugins/`에 남긴다.

Community Plugin 등록 전에 사용자가 소유한 plugin을 실제 Vault에서 검증해야 할 때는 임의 폴더 복사 대신 `install-local-build`만 사용한다. 사용자가 현재 작업에서 교체를 명시적으로 승인했고 [approved plugins](references/approved-plugins.md)의 development allowlist에 있는 ID에 한해, `main.js`·`manifest.json`·`styles.css`의 일반 파일 여부, manifest ID, 정확한 version과 SHA-256을 확인한다. 기존 설정 파일은 변경 없이 보존하고 stage → backup → atomic replace → 활성 config 재조회를 거친다. 실패하면 runtime·설정·활성 config를 모두 기존 상태로 복원한다. 이 경로는 로컬 개발 검증일 뿐 공식 release나 Community Plugin 승인을 대체하지 않으며 자동화에서 임의로 호출하지 않는다.

설치 전에는 먼저 `status`로 대상 ID와 기존 mindmap plugin을 확정한다. 삭제는 `remove-detected-mindmaps`만 사용해 설치 manifest가 실제 mindmap인 plugin만 backup으로 옮긴다. Obsidian 기본 Canvas, Excalidraw, 비 mindmap plugin, 그리고 이름만 비슷한 폴더는 제거하지 않는다.

Community plugin 설정상 활성화와 현재 실행 중인 Obsidian의 runtime load는 다르다. adapter는 저장하지 않은 문서를 잃을 수 있는 앱 재시작이나 UI 자동화를 하지 않는다. 설치 뒤 Obsidian을 안전하게 reload한 다음 `status` receipt와 실제 plugin 화면으로 rendered 동작을 확인한다.

`linked-graph`는 현재 Markdown의 resolved outgoing wikilink만 작성 순서로 읽는 오른쪽 사이드바다. Markdown·Canvas·Map·관계·레이아웃·설정 파일을 쓰지 않는다. exact `1.0.1` local build와 receipt가 확인된 뒤에만 구형 `context-graph`를 `retire`로 backup 이동한다. 편집기의 fold 상태는 공개 API로 읽지 않고, 펼치기·검색은 세션 UI 상태로만 둔다.

Apple Calendar projection은 독립 공개 plugin인 `link-calendar`의 한 read-only source profile로만 연결한다. 설정 전 `woon calendar refresh`로 Core가 `inbox/calendar/events/*.md`와 `inbox/calendar/apple-calendar.md`를 함께 재생성할 수 있는지 확인한 뒤, 검증된 local build를 `install-local-build`로 설치하고 `configure-link-calendar`로 `woon-apple-calendar` profile을 upsert한다. 이 profile은 `editable: false`이며 다른 사용자 profile과 plugin 설정을 보존한다.

`link-calendar` 정본은 `woonyong-kr/link-calendar` 저장소다. 공개 plugin 자체는 어떤 Vault·Calendar 공급자·분류 이름도 가정하지 않고 folder/tag/property mapping을 설정으로 받는다. Woon Core는 `Date`·`End Date`·`Start Date`·`All Day`·`title`·`Category`를 연결한다. plugin은 월간 보기와 선택 날짜의 시간·정본 링크만 파생하며 본문 미리보기·backlink·인물·프로젝트·관련 문서·레이아웃을 별도 저장하거나 표시하지 않는다. 원본 event ID·장소·메모·참석자·URL은 Woon projection에 넣지 않는다.

구형 `context-calendar`와 `woon-simple-calendar`는 새 plugin의 exact version·asset hash·활성 config·read-only profile·dashboard·configure receipt가 모두 검증된 뒤에만 각각 `retire`로 backup 이동한다. 설치 파일 존재만으로 완료하지 않고 Obsidian reload 뒤 ribbon, 월간 화면, 일정 카드, 날짜별 일정, 정본 문서 링크, read-only 차단을 실제 UI에서 확인한 다음 `attest-link-calendar-runtime`으로 전체 checklist를 기록한다. 이 operator attestation은 현재 asset·settings·dashboard hash에 묶이므로 어느 하나라도 바뀌면 화면을 다시 확인해야 한다.

현재 승인된 plugin ID와 공식 release 출처는 [approved plugins](references/approved-plugins.md)에 둔다. 새 plugin은 사용자 승인, Community Plugin 등록 확인, 공식 repository와 manifest ID 일치, release asset hash 검증 규칙을 먼저 추가한 뒤에만 allowlist에 넣는다.
