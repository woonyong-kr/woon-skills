---
name: knowledge-navigation
description: Woon Wiki의 단일 계층형 키워드 트리, 하위 문서 색인, 엔티티별 성장 구조와 Obsidian Graph·Canvas 파생 화면을 설계·검증할 때 사용한다. 고아 문서, 중복 키워드, 별도 Map, 모호한 부모를 진단하는 요청에 적용한다.
---

# Knowledge Navigation

`$knowledge-navigation`은 `woon-knowledge/docs/wiki-information-architecture.md`를 실행하는 절차다. 사람이 읽고 AI가 검색하는 지식·질문·탐색 순서의 정본은 `wiki/**/*.md`뿐이다. 먼저 `$knowledge`로 기존 정체성을 찾고, 실제 기록은 `$archive` 또는 `$compile-knowledge`로 반영한다.

## 단일 트리 계약

1. `wiki/README.md`만 root다. 모든 활성 Wiki 문서는 root에서 `parent` 하나를 따라 도달해야 한다.
2. 부모는 폴더가 아니라 의미로 선택한다. `parent_topics`, `parent_moc`, `map_role`, `mindmap_role`로 병렬 계층을 만들지 않는다.
3. `canonical_id`, title, aliases, keywords, 중심 질문을 함께 대조한다. 같은 질문이면 기존 문서의 section을 갱신하고, 독립된 중심 질문·고유 근거 또는 이력·둘 이상의 재사용 맥락 중 하나가 있을 때만 새 child를 만든다.
4. 새 child는 `parent`, 대표 `keywords`, `central_question`, 생성 이유를 확정할 수 있을 때만 만든다. 부모가 모호하면 root에 임시로 붙이지 않고 Review로 보낸다.
5. root는 직접 하위 키워드 wikilink만 보여 준다. hub의 작은 순수 분류 child는 일반 텍스트 불릿으로 두고 그 직접 child wikilink를 한 단계 들여써 평탄화한다. 프로젝트·인물처럼 direct child 자체가 실체인 hub는 `navigation_groups`에 주제 label과 direct child `canonical_id`를 명시해 같은 2단 불릿으로 보여 준다. 한 hub에서는 장르·목적·관계·진행 단계 중 하나의 분류 축만 사용하고, 포함 관계가 겹치는 label은 대표 label 하나로 합친다. 모든 direct child는 정확히 한 그룹에 있어야 하고 그룹당 링크가 20개를 넘으면 안 된다. 전체 subtree·최신 목록·summary·상태·개수는 펼치지 않는다. topic·entity의 하단 색인만 직접 하위 키워드와 필요한 최신 관련 문서의 wikilink를 보여 준다.
6. `aliases`는 같은 정체성의 다른 이름, `related_to`는 비교·원인·사례·사용 같은 횡단 관계다. 둘 다 기본 부모를 대신하지 않는다.
7. 순서는 탐색 의미다. root는 `개념 → 책 → 리소스 → 프로젝트 → 커리어 → 인물 → 생활` 순서를 사용하고, 기술 개념은 가까운 선수·응용 주제를 붙인다. 그룹 안에서는 선수 개념·작업 흐름·가나다순·날짜순 중 하나를 일관되게 적용한다. `sequence`와 `navigation_groups` 배열 순서를 명시하며 파일명 자동 정렬에 맡기지 않는다.

## 페이지와 엔티티

- 탐색 페이지는 직접 링크 또는 `분류 텍스트 → child 링크` 2단 불릿만 읽는다. `navigation_groups`는 표시 순서일 뿐 새 정체성이나 두 번째 parent를 만들지 않는다. 모든 entity 첫 화면도 주제 키워드 wikilink와 별도 히스토리를 우선하며, 설명과 판단 근거는 도착한 상세 topic·detail에서 읽는다.
- 책은 `책` 페이지에서 `- 장르 텍스트` 아래의 책 제목 wikilink를 바로 연다. 정본 parent tree는 `Wiki → 책 → 장르 키워드 → 책 제목`을 유지하며, 책 페이지는 목차 anchor와 장별 개념·정리 wikilink만 소유하고 소개문·`키워드:`·`영역: Area N`을 반복하지 않는다.
- `콘텐츠` subtree와 Facet은 만들지 않는다. 강의·글·영상에서 얻은 의미는 기존 주제 Wiki에 흡수하고, 외부 원자료와 PDF·이미지·전사는 `Wiki → 리소스 → 분야 hub → 같은 출처·대상·용도의 bundle topic`에서 링크로만 색인한다. 리소스 첫 화면은 `분야 텍스트 → bundle 링크`를 보여 주고 자료가 하나뿐인 분야만 원자료 링크를 바로 보여 준다.
- 책이 아닌 외부 자료의 의미 부모나 `resource_keyword`를 확정할 수 없으면 중간 콘텐츠 카드를 만들지 않고 Review로 보낸다. Novel·민감 자료는 일반 리소스 Graph에 중복 노출하지 않는다.
- 프로젝트 entity는 목표·완료 조건, 요구사항, 설계, 결정, 구현, 검증, 결과, 남은 문제를 subtree와 본문으로 관리한다.
- 인물 hub의 직접 child는 사람 이름의 person entity뿐이다. 인물 entity는 관계·프로젝트·결정·대화·자료를 주제 wikilink로 묶고 사건은 별도 히스토리에 날짜순으로 누적한다. 사람 이름과 특정 분석 제목을 별도 인물처럼 병렬로 두지 않는다. 이름 한 번의 언급으로 entity를 만들지 않는다.
- 질문과 답변은 관련 키워드 본문에 둔다. 질문 자체가 계속 갱신되는 독립 정체성일 때만 detail child로 분리한다.

## 파생 화면 경계

- `maps/`에는 `.canvas`와 plugin profile 같은 화면 상태만 둘 수 있다. Markdown Map, 별도 키워드 목록, 독립 시작 노트를 만들지 않는다.
- Global Graph는 `graph/overview` tag가 있는 root·hub·entity만 보여 준다. leaf는 현재 페이지의 subtree, Local Graph, Linked Graph에서 연다.
- `.base`, Canvas, Linked Graph는 Wiki metadata와 실존 wikilink를 읽는다. 화면에만 존재하는 제목·답변·관계·순서를 만들지 않는다.
- 한 문서의 code·실행·상태 관계를 설명하는 canonical 시각화는 `$diagram`의 Markdown Mermaid다.

## Canvas 계약

1. `.canvas`에는 기존 Wiki Markdown을 가리키는 `file` node와 node 사이 edge만 둔다. `text`, `link`, `group` node와 edge label은 지식 정본으로 사용하지 않는다.
2. node `file`은 vault 안의 실존 `.md`다. `subpath`는 실제 heading 또는 block이어야 한다.
3. Canvas edge는 실제 `parent`, `related_to`, 본문 wikilink 중 하나를 투영한다. 좌표·색·edge가 Markdown 관계를 대신하지 않는다.
4. `auto-` ID만 AI가 재생성한다. `manual-` ID와 그 node에 닿는 edge, 접두어 없는 기존 배치는 사용자 소유로 보존한다.
5. 대량 변경 전후에 대상 Markdown, Canvas, 자동 생성 범위, 보존할 수동 범위를 비교한다.

```bash
python3 "$(woon resolve repo://skills/skills/knowledge/knowledge-navigation/scripts/validate_canvas.py)" \
  --vault <vault> \
  --canvas <vault-relative-map.canvas>
```

## 완료 기준

1. root에서 모든 활성 Wiki가 `parent`로 도달하고 cycle·고아 문서가 없다.
2. title·aliases·keywords·중심 질문 기준의 의미상 중복과 병렬 Markdown Map이 없다.
3. root의 직접 child 링크, hub의 직접 링크·작은 분류·명시적 `navigation_groups` 2단 불릿, topic·entity의 child·latest 링크가 실제 metadata와 일치하며 hub에 최신 subtree를 펼치거나 설명·날짜·개수를 반복하지 않는다.
4. `콘텐츠` 분류가 없고 책 화면은 장르 텍스트→책 링크→목차 링크, 리소스는 분야 텍스트→중복 없는 bundle 링크→원자료 링크이며, 프로젝트·인물 entity는 각각 project·topic-timeline 계약을 충족한다.
5. Canvas target과 edge가 실존 Wiki 관계와 일치하고 수동 배치를 보존한다.
6. Obsidian에서 root tree, entity tree, latest, Global Graph, Local Graph를 실제로 확인한다. UI 확인 전에는 정적 검증 완료로만 보고한다.
