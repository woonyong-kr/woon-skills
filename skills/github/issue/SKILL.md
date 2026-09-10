---
name: issue
description: GitHub Issue를 검색·작성·수정하거나 연결된 GitHub Projects의 일정 필드와 필요한 권한을 공식 gh CLI로 관리할 때 사용한다. 일반 캘린더 일정과 PR은 해당 소유 스킬이 맡는다.
---

# Issue

중복 issue와 repository template을 먼저 확인한다. 제목은 재현 가능한 문제나 원하는 결과를 쓰고, 본문에는 현재 동작, 기대 동작, 재현 절차, 환경, 근거, acceptance criteria를 둔다.

label, assignee, milestone은 실제 저장소 값을 조회해 사용한다. 추정 원인을 사실처럼 쓰지 않는다. issue 생성·comment·close는 사용자 요청 범위 안에서만 수행하고 생성된 URL과 상태를 확인한다.

Projects 일정·권한 작업은 [공식 gh Projects 절차](references/projects.md)를 따른다. 현재 승인된 계정·Project·Issue·필드만 변경하고, 기존 item 재사용과 변경 전후 재조회로 중복과 불확실한 재시도를 막는다. OAuth grant의 권한은 `$safety`에서 확인하며 읽기 전용 준비는 계속한다.
