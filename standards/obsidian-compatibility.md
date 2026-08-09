# Obsidian compatibility

## Purpose

Woon 지식 문서를 Obsidian에서 읽고 연결할 수 있게 하되, private canonical 소유권과 Quartz 공개 경계를 바꾸지 않는다. 이 문서는 Obsidian 전체 문법이 아니라 Woon이 확정한 교차 규칙이다.

## Ownership layers

- archive MCP의 구조화 인수는 `canonical_id`, `title`, `domain`, `summary`, `difficulty`, 관계 ID, `source_session_ids`, `expected_revision`을 소유한다. `aliases`·`publish`·`access`·`status`는 archive 인수가 아니다.
- filesystem adapter가 구조화 인수에서 YAML frontmatter와 H1을 생성하고 `status: Canonical`, `publish: false`, `access: local-only`를 고정한다. MCP `body`에는 이 영역을 반복하지 않고 H2 이하의 본문만 넣는다. 사용자가 중복을 지시해도 MCP 계약을 우선한다.
- Markdown 본문은 검증된 설명·코드·관찰·한계를 소유한다. metadata를 본문으로 복제해 두 개의 정본을 만들지 않는다.

## Links and visibility

- 내부 지식 링크는 검색·조회로 실존을 확인한 canonical ID만 `[[domain/slug|표시명]]`으로 쓴다. 제목만 아는 경우 plain text로 두고 relation 배열은 비운다.
- 외부 URL은 `[표시명](https://...)` 형식을 쓴다. Obsidian 전용 block reference는 외부 렌더러에서 검증하지 못하면 필수 정보에 사용하지 않는다.
- public 문서는 private source의 경로·wikilink·session ID를 포함하지 않는다. `publish: true`는 콘텐츠 선별 metadata일 뿐 repository 공개나 source 노출 승인이 아니다.

## Portable body

- CommonMark heading, list, table, fenced code를 기본으로 한다. callout은 `> [!note]` 계열만 선택적으로 쓰고, 접힌 callout 안에만 필수 사실을 숨기지 않는다.
- archive MCP body는 H2 이하로 시작하고 adapter가 frontmatter와 H1을 만든다. 독립 Markdown은 대상 저장소 계약에 따라 H1을 한 번 사용할 수 있지만 archive body 형식을 그대로 복제하지 않는다.
- heading hierarchy를 목차의 정본으로 삼는다. 수동 목차와 heading을 각각 편집하지 않으며, 목차 link는 Obsidian·Quartz에서 같은 anchor가 열리는 것을 확인한 경우에만 생성한다.
- code·memory·call·exception 흐름의 canonical 시각화는 Markdown 안의 Mermaid다. JSON Canvas는 같은 identifier와 단계를 유지하는 local 보조물일 뿐 Mermaid를 대체하지 않는다.
- `.base`는 local 조회 view이며 원문이나 공개 학습 문서의 정본이 아니다. `.canvas`·`.base`를 만들 때는 YAML·JSON 구문과 참조 대상을 별도로 검증한다.
- 색은 보조 신호다. 경로·상태·예외은 text label과 line style로도 구분한다.

## Acceptance

1. `woon_knowledge_audit`으로 metadata, duplicate, broken·ambiguous link, private/public 위반을 검사한다.
2. Obsidian Reading view와 light·dark mode에서 heading, wikilink, callout, Mermaid 대비와 clipping을 확인한다.
3. 공개 대상은 Quartz build 후 링크·Mermaid·navigation과 private 정보 불포함을 rendered output에서 확인한다.
4. 표시를 확인하지 못한 층은 통과로 보고하지 않고 미검증으로 남긴다.
