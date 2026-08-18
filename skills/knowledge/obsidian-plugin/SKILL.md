---
name: obsidian-plugin
description: Woon Obsidian Vault의 Community Plugin 설치 상태를 확인하고, 사용자가 승인한 plugin을 공식 release에서 검증·설치·활성화·제거할 때 사용한다.
---

# Obsidian Plugin

Obsidian plugin은 UI 조작이나 임의 폴더 복사로 관리하지 않는다. `$obsidian-plugin`은 Core의 receipt 기반 adapter만 사용한다.

```bash
woon knowledge obsidian-plugin status --vault <vault>
woon knowledge obsidian-plugin install --plugin <approved-id> --vault <vault>
woon knowledge obsidian-plugin remove-detected-mindmaps --vault <vault>
woon knowledge obsidian-plugin configure-simple-calendar --vault <vault>
woon knowledge obsidian-plugin retire --plugin notion-bases --vault <vault>
```

`status`는 설치 manifest, version, 활성 config, 설정 파일과 `mindmap` 판정을 read-only로 반환한다. 설치는 allowlist의 공식 GitHub release API와 release asset SHA-256을 확인하고, manifest `id`가 요청 ID와 같을 때만 stage → backup → atomic replace → `community-plugins.json` 갱신 → 재조회 순서로 진행한다. receipt와 backup은 Vault의 Git 제외 `.local/woon-knowledge/obsidian-plugins/`에 남긴다.

설치 전에는 먼저 `status`로 대상 ID와 기존 mindmap plugin을 확정한다. 삭제는 `remove-detected-mindmaps`만 사용해 설치 manifest가 실제 mindmap인 plugin만 backup으로 옮긴다. Obsidian 기본 Canvas, Excalidraw, 비 mindmap plugin, 그리고 이름만 비슷한 폴더는 제거하지 않는다.

Community plugin 설정상 활성화와 현재 실행 중인 Obsidian의 runtime load는 다르다. adapter는 저장하지 않은 문서를 잃을 수 있는 앱 재시작이나 UI 자동화를 하지 않는다. 설치 뒤 Obsidian을 안전하게 reload한 다음 `status` receipt와 실제 plugin 화면으로 rendered 동작을 확인한다.

Apple Calendar 화면은 Core가 배포·영수증으로 설치하는 `woon-simple-calendar`만 사용한다. 설정 전 `woon calendar refresh`로 Core가 `inbox/calendar/events/*.md`의 일정 행과 `inbox/calendar/apple-calendar.md`의 월간 dashboard를 함께 만들 수 있는지 확인한다. 일정 행에는 `Date`, 고정된 `Category`, user-confirmed 인물 링크만 남으며, Simple Calendar는 이를 날짜별 두 줄 카드와 저채도 분류 채움색으로 표시한다. 카드는 움직이지 않고 hover·keyboard focus에서만 같은 분류의 채움색이 진해지며, 긴 제목의 전체 내용은 tooltip과 클릭한 읽기 전용 Markdown에서 확인한다. 시간, 장소, 메모, 참석자, URL, 원본 event ID는 화면과 Markdown에 넣지 않는다. 동명이 식별자는 `inbox/review/calendar-person-identity-review.md`에만 후보로 남기고 자동 링크하지 않는다.

Simple Calendar의 JavaScript·CSS·manifest 정본은 `woonyong-kr/simple-calendar`의 공식 GitHub release이고, Core adapter는 release의 manifest ID와 asset SHA-256을 검증한 runtime 사본만 Vault에 설치한다. 왼쪽 ribbon의 `Apple Calendar 열기` 아이콘과 같은 이름의 명령 팔레트 명령은 같은 읽기 전용 dashboard를 연다. calendar block은 문서 작업 영역 전체를 채우며, card 클릭은 대응 Markdown을 열 뿐 생성·끌어놓기·inline edit·외부 동기화는 지원하지 않는다. 일정 변경은 Apple Calendar에서만 한다. 이전 `notion-bases`는 새 dashboard·plugin manifest·receipt와 실제 렌더링을 검증한 뒤 `retire --plugin notion-bases`로만 local backup에 옮긴다.

현재 승인된 plugin ID와 공식 release 출처는 [approved plugins](references/approved-plugins.md)에 둔다. 새 plugin은 사용자 승인, Community Plugin 등록 확인, 공식 repository와 manifest ID 일치, release asset hash 검증 규칙을 먼저 추가한 뒤에만 allowlist에 넣는다.
