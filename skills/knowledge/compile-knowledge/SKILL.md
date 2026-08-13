---
name: compile-knowledge
description: private woon-knowledge의 LLM Wiki source·claim·page spec·receipt를 추가·수정·감사·컴파일할 때 사용한다. catalog/llm-wiki 변경이나 receipt 불일치·stale 검색 복구에 사용한다.
---

# Compile Knowledge

`wiki/`는 compiler 산출물이다. source, accepted claim, page spec만 편집하고 Markdown 출력·receipt를 직접 고치지 않는다.

1. 먼저 `$knowledge`로 기존 canonical 문서와 관계 ID를 확인한다. 대화 한 건을 정본에 저장하는 일은 `$archive`, 외부 corpus 전수 수집은 `$ingest`에 넘긴다.
2. 변경할 `catalog/llm-wiki/sources.yaml`, `claims.yaml`, `pages.yaml`을 읽고 [compiler contract](references/compiler-contract.md)의 필수 필드와 privacy 규칙을 적용한다. 원본은 덮어쓰지 않으며 locator에 머신 절대 경로·secret·private 원문을 넣지 않는다.
3. source는 원문 hash와 보존 본문, claim은 해당 source ID와 채택 근거, page spec은 한 output path와 source/claim 집합을 가진다. public page에는 public provenance만 연결한다. 미확인 주장·충돌은 `review-queue.yaml`에 남기고 accepted claim으로 만들지 않는다.
4. `woon_knowledge_compile`을 호출한다. 직접 Markdown 변경 또는 receipt 오류가 있으면 source/claim/page spec을 고친 뒤 다시 컴파일한다. `--force`는 compiler 변경 또는 receipt 전체 재생성이 필요한 경우에만 쓴다.
5. `woon_knowledge_compile_audit`과 `woon_knowledge_audit`을 모두 통과시킨다. source 변경 뒤 search가 stale이면 compile이 먼저이고 reindex는 그 다음이다. compiler 입력·출력·index가 모두 current인지 확인한 뒤에만 완료를 말한다.

컴파일 실패 시 output 파일을 수동 복구하지 않는다. Git diff로 source catalog 변경을 검토하고 필요한 입력만 되돌린 후 재컴파일한다. 자동 commit, push, publish는 하지 않는다.
