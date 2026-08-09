---
name: archive
description: 현재 AI 대화를 중복 없는 하나의 canonical 학습 문서로 정제해 private woon-knowledge에 저장하거나 기존 문서에 병합할 때 사용한다.
---

# Archive

먼저 `$knowledge` 방식으로 2~3개 안정적인 keyword를 검색하고 후보 문서 전체와 revision을 읽는다. index missing이면 `woon_knowledge_reindex` MCP를 호출하고 동일 검색을 한 번 재시도한다. `woon knowledge index` CLI와 default vault fallback은 금지한다. 제목 유사도가 아니라 같은 질문에 답하는지로 identity를 판단한다.

대화 순서, 반복 질문, 사과, 상태 narration을 제거하고 검증된 사실·결정·예제·한계를 기존 section에 통합한다. MCP body에는 YAML frontmatter와 H1을 넣지 않는다. `prerequisites`, `next_concepts`, `related`에는 검색·조회로 확인한 slash-separated canonical ID(`domain/slug`)만 넣는다. 제목·표시 이름·검색 keyword를 넣지 말고 ID를 확인하지 못한 관계는 빈 배열로 보낸다. 새 문서는 `expected_revision` 없이, 기존 문서는 조회한 revision을 넣어 `woon_knowledge_archive_conversation`을 호출한다. conflict가 나면 다시 읽고 병합하며 force overwrite하지 않는다.

저장 뒤 `woon_knowledge_audit`을 실행한다. private 정본이며 별도 요청 없이 commit, push, publish하지 않는다. 입력 계약은 [MCP contract](references/mcp-contract.md)를 필요할 때만 읽는다. 이 스킬은 `repo://skills/skills/knowledge/archive`의 단일 원본이며 knowledge 저장소에 복사하지 않는다.

대화가 학습 설명을 포함하면 `woon resolve repo://skills/standards/learning-content-quality.md`로 내부 표준을 읽는다. 문제·실행 근거·인과·개념·한계를 재배열하되 대화에 없던 실행 결과를 만들지 않는다.
