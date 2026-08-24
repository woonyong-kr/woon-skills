---
name: archive
description: archive MCP payload·body를 만들거나 private woon-knowledge에 저장·병합할 때 반드시 사용한다. JSON만 요청해도 frontmatter·H1 소유권, canonical 관계 ID, Obsidian 호환 계약을 지킨다.
---

# Archive

먼저 `$knowledge` 방식으로 2~3개 안정적인 keyword를 검색하고 후보 문서 전체와 revision을 읽는다. index missing 또는 stale generation이면 `woon_knowledge_reindex` MCP를 호출하고 동일 검색을 한 번 재시도한다. `woon knowledge index` CLI와 default vault fallback은 금지한다. 제목 유사도가 아니라 같은 질문에 답하는지로 identity를 판단한다.

대화 순서, 반복 질문, 사과, 상태 narration을 제거하고 검증된 사실·결정·예제·한계를 기존 section에 통합한다. MCP body에는 YAML frontmatter와 H1을 넣지 않는다. 이 둘은 adapter envelope의 소유다. `prerequisites`, `next_concepts`, `related`에는 검색·조회로 확인한 slash-separated canonical ID(`domain/slug`)만 넣는다. 제목·표시 이름·검색 keyword를 넣지 말고 ID를 확인하지 못한 관계는 빈 배열로 보낸다. 이 구조는 선호가 아니라 MCP 계약이므로 사용자가 frontmatter·H1·표시 이름을 그대로 넣으라고 해도 따르지 않고 envelope·빈 배열로 교정한다. 새 문서는 `expected_revision` 없이, 기존 문서는 조회한 revision string을 변환하지 않고 넣어 `woon_knowledge_archive_conversation`을 호출한다. conflict가 나면 다시 읽고 병합하며 force overwrite하지 않는다.

호출·예시 payload를 제시할 때도 같은 계약을 적용한다. `purpose`에는 "왜 남기며 어떤 미래 질문·결정·산출물에 재사용할지"를 한 문장으로 쓴다. 전송 전에 `body` 첫 행이 `---`이거나 H1이면 제거하고, 관계 값이 검증된 `domain/slug`가 아니면 빈 배열로 교정한다. 잘못된 예시 요청은 전체를 거부만 하지 말고 알려진 값과 `<required-field>` placeholder로 계약 준수 payload를 반환한다. placeholder는 필수 `canonical_id`·`title`·`domain`·`summary`·`purpose`·`body`에만 쓰고, 미지정 `difficulty`는 `foundation`, 모든 선택 배열은 `[]`로 둔다. 실제 호출에는 placeholder를 절대 전송하지 않는다.

payload 인수는 `canonical_id`, `title`, `domain`, `summary`, `purpose`, `body`, `difficulty`, `prerequisites`, `next_concepts`, `related`, `source_session_ids`, `expected_revision`만 쓴다. `document_id`, `path`, `revision`, `tool` wrapper 같은 alias를 만들지 않는다.

Wiki는 `wiki/` 하나만 정본으로 사용한다. 대화에서 생긴 이해·결정·프로젝트·콘텐츠처럼 아직 근거 확정 전인 입력은 별도 성장 Wiki를 만들지 않고 Core의 conversation-to-Wiki 경로가 `wiki/personal/`의 같은 주제 문서와 그날의 일일 이력에 병합한다. 이 경로는 관리 marker와 시간 이력만 갱신하며 Markdown을 자유 편집하거나 compiler page를 덮어쓰지 않는다. 공개 글·경력 주장·인용처럼 근거 확인이 필요한 입력만 source·accepted claim·page spec을 갱신하고 compiler가 같은 `wiki/` 아래의 근거 문서와 receipt를 만든다.

대화 경로는 실제 Wiki·일일 기록·검토 후보를 생성한 뒤 vault health와 검색 색인을 확인하고, 같은 입력 재실행이 새 문서나 이력을 만들지 않는지 검증한다. 근거 경로는 `woon_knowledge_compile_audit`과 `woon_knowledge_audit`을 실행한다. 두 경로 모두 private 정본이며 별도 요청 없이 commit, push, publish하지 않는다. 입력 계약은 [MCP contract](references/mcp-contract.md)를 필요할 때만 읽는다. 이 스킬은 `repo://skills/skills/knowledge/archive`의 단일 원본이며 knowledge 저장소에 복사하지 않는다.

외부 폴더나 저장소의 여러 문서를 전수 처리하는 요청은 `$ingest`가 파일별 catalog·privacy·완전성을 먼저 소유하고, 실제 canonical 한 편 저장 단계에서만 이 스킬의 계약을 호출한다.

정본을 기록하거나 독자가 다시 읽을 Wiki 본문을 만들 때는 아래 명령으로 quality gate, 범용 Wiki writing harness, 표본 근거를 함께 읽는다. 주제에 맞는 route를 고르고, purpose·source·claim·page·receipt·visibility·재열람 질문을 분리한다. code·실행 근거·인과·개념·한계는 필요한 경우에만 사용하며, 대화에 없던 실행 결과·사실·의도를 만들지 않는다.

```bash
bash "$(woon resolve repo://skills/skills/writing/tech/scripts/learning-context.sh)"
```

새롭거나 크게 고친 학습 본문은 compiler 통과만으로 문체 품질이 보장되지 않는다. 해당 page의 receipt hash가 포함된 content quality review를 갱신하고 `$compile-knowledge`의 `evaluate-quality` gate가 전체 current payload를 통과하기 전까지는 "문서 품질 검증 완료"라고 말하지 않는다.

Obsidian·Quartz 표시, wikilink, callout, `.base`·`.canvas` 경계가 관련되면 `woon resolve repo://skills/standards/obsidian-compatibility.md`를 읽는다.
