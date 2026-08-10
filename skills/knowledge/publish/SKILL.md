---
name: publish
description: private woon-knowledge의 승인된 문서를 공개 WIKI·사이트용 산출물로 선별·변환·검증해 발행할 때 사용한다. 내부 저장에는 사용하지 않는다.
---

# Publish

private source와 public output을 분리한다. `publish:true` 같은 metadata는 repository 공개 권한이 아니다.

`써 줘`, `정리해 줘`, `후보를 보여 줘`는 대화 안의 candidate 작성 권한뿐이다. 정확한 candidate와 공개 범위를 보여 준 뒤 사용자가 그 산출물의 반영을 승인해야 public source를 쓸 수 있다.

1. 승인 전에는 source ID·revision, 포함·제외 claim, 개인정보·권리 판단, 미확인 사항을 공개 승격 영수증으로 제시하고 멈춘다.
2. 승인 뒤에도 secret, 개인정보, 회사 내부 자료, 비공개 link, source session ID를 다시 검사한다.
3. 승인된 public source만 deterministic하게 쓰고 build·rendered link·navigation을 검증한다.
4. repository visibility, target branch와 destination을 확인하되 private repository 자체를 public으로 바꾸지 않는다.
5. commit, push와 deploy는 반영 승인에 포함되지 않는다. 각각 명시적으로 요청된 범위만 수행하고 live artifact identity를 확인한다.

블로그와 포트폴리오처럼 같은 근거를 서로 다른 독자용으로 승격할 때는 `$site-promotion`이 candidate와 claim 일관성을 먼저 소유한다.

Obsidian용 private 정본을 Quartz·WIKI로 변환하거나 wikilink를 검사할 때는 `woon resolve repo://skills/standards/obsidian-compatibility.md`를 읽어 형식 호환성과 공개 경계를 함께 검증한다.
