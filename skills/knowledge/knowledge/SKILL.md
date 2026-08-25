---
name: knowledge
description: private woon-knowledge에서 정본 문서를 검색·조회·감사·이력 확인·복구하거나 지식 중복과 연결 품질을 진단할 때 사용한다.
---

# Knowledge

`woon-knowledge`를 private canonical source로 유지한다. MCP는 상시 로드하지 않고 지식 작업에서만 on-demand로 사용한다.

- 찾기: 안정적인 한국어·technical keyword로 `woon_knowledge_search`. 결과를 고를 때 `canonical_id`·title·aliases·keywords·중심 질문을 함께 보고, 선택한 leaf의 ancestor path·직접 child·최근 이력·필요한 evidence를 context bundle로 읽는다.
- compiler receipt 또는 source-schema stale: `woon_knowledge_compile`을 호출하고 동일 검색을 한 번 재시도한다. index generation만 stale이면 `woon_knowledge_reindex` MCP를 호출한 뒤 동일 검색을 한 번 재시도한다. `woon knowledge index` CLI나 경로를 생략한 default vault fallback은 사용하지 않는다.
- canonical 결과: 선택한 `canonical_id`를 `woon_knowledge_get`으로 전체 조회.
- read-only corpus 결과: 반환된 `document_id`와 `chunk_id`를 `woon_knowledge_read_excerpt`로 필요한 문맥만 조회. corpus 원본을 canonical로 가장하거나 수정하지 않는다.
- 다른 산출물의 근거로 넘길 때는 `canonical_id`·revision·source type·현재 재검증 여부를 함께 기록한다. 검색 결과를 공개 문장으로 바로 바꾸거나 오래된 기록을 현재 사실로 승격하지 않는다.
- 품질: source provenance와 receipt는 `woon_knowledge_compile_audit`, link·metadata·duplicate 문제는 `woon_knowledge_audit`.
- 답변·인용: 별도 LLM이 만든 답변은 generator run ID, claim 단위, `document_id`·`chunk_id`·revision·원문 quote를 payload로 남긴 뒤, 명시한 vault·cases·answers 경로로 `woon knowledge evaluate-answers`를 실행한다. 기계 검증은 quote와 현재 excerpt의 일치만 증명하며, claim별 semantic judgment가 없으면 전체 통과로 말하지 않는다.
- 이력: `woon_knowledge_history`로 revision과 Git evidence 확인.
- 복구: 사용자가 revision을 선택하고 승인한 뒤 `woon_knowledge_restore`.

대화를 같은 주제의 Wiki와 일일 이력에 병합하는 일은 `$archive`, 외부 corpus 전수 수집은 `$ingest`, 근거 문서의 source·claim·page spec 갱신은 `$compile-knowledge`, 키워드 tree와 Graph 파생 화면은 `$knowledge-navigation`이 맡는다. 성장·검증·탐색 상태를 이유로 두 번째 Wiki나 Markdown Map을 만들지 않는다. 직접 `wiki/` overwrite, receipt 수정, 별도 vector DB 정본, CLI를 통한 default production vault 변경, 자동 commit/push를 만들지 않는다. 이 스킬의 단일 원본은 `repo://skills/skills/knowledge/knowledge`이며 다른 저장소에 복사하지 않는다.
