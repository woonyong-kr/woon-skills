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
5. 모든 Map은 `# 페이지 제목 → ## 주제 키워드 → - [[직접 하위 링크]]`로 보여 준다. 주제 키워드를 일반 불릿이나 wrapper link로 만들지 않고 H2로 둔다. 같은 화면에는 직접 하위 링크만 평평한 불릿으로 표시하며 손자 이하를 펼치지 않는다. `navigation_groups`가 H2 주제와 direct child 순서를 소유한다. 한 페이지에서는 장르·목적·관계·진행 단계 중 하나의 분류 축만 사용하고, 포함 관계가 겹치는 label은 대표 label 하나로 합친다. 모든 direct child는 정확히 한 그룹에 있어야 하고 그룹당 링크가 20개를 넘으면 안 된다. 전체 subtree·최신 목록·summary·상태·개수는 펼치지 않는다.
   책 Map의 화면 계약은 더 엄격하다. 각 Map은 `# 페이지 제목 → ## 주제 키워드 → - [[직접 하위 학습 페이지]]`로 렌더링한다. 책 root에서는 부·부록이 H2이고 그 아래 장·부록 링크가 평평한 불릿으로 온다. 장 Map에서는 의미 있는 절·주제 키워드가 H2이고 그 아래 세부 학습 페이지 링크가 평평한 불릿으로 온다. H2 주제 키워드는 별도 wrapper page나 링크가 아니며, `N장`·`부록 A`처럼 H1을 줄여 반복하지 않고 같은 화면에 그보다 깊은 후손을 펼치지 않는다. 하위 절이 없는 Summary 같은 terminal section도 독립 leaf 링크로 두며 Map authored body는 비운다. 기존 Map의 원문 설명·예제·그림은 삭제하지 않고 가장 가까운 leaf로 provenance와 함께 이동한다. 정본 계층은 보통 `책 → 장 → 세부 학습 페이지`의 2~4단계로 제한하고, 탐색만 위한 빈 절 wrapper를 만들지 않는다. 원문에 더 깊은 구조가 있어도 독립 페이지가 꼭 필요하지 않다면 가장 가까운 leaf의 heading과 coverage locator로 보존하며, 정보량과 재탐색 필요가 명확할 때만 더 깊은 예외를 허용한다.
6. `aliases`는 같은 정체성의 다른 이름, `related_to`는 비교·원인·사례·사용 같은 횡단 관계다. 둘 다 기본 부모를 대신하지 않는다.
7. 순서는 탐색 의미다. root는 `개념 → 책 → 리소스 → 프로젝트 → 커리어 → 인물 → 생활` 순서를 사용하고, 기술 개념은 가까운 선수·응용 주제를 붙인다. 그룹 안에서는 선수 개념·작업 흐름·가나다순·날짜순 중 하나를 일관되게 적용한다. `navigation_groups`가 있으면 group과 `children` 배열이 사람 화면과 AI 문맥의 순서를 함께 소유하고, `sequence`는 평탄 인덱스 예외와 단일 child의 fallback만 소유한다. 파일명 자동 정렬에 맡기지 않는다.

## 페이지와 엔티티

- 탐색 페이지는 `H1 제목 → H2 주제 키워드 → direct child 링크 불릿`만 읽는다. `navigation_groups`는 표시 순서일 뿐 새 정체성이나 두 번째 parent를 만들지 않는다. 모든 entity 첫 화면은 같은 Map 형식과 필요한 날짜별 이력을 함께 보여 주며, 설명과 판단 근거는 명확한 내부 section 또는 도착한 상세 topic·detail에서 읽는다.
- 책은 `책` 페이지에서 `- 장르 텍스트` 아래의 한국 번역판 책 제목 wikilink를 바로 연다. 영문 원제는 alias와 source metadata에 남긴다. 정본 parent tree는 `Wiki → 책 → 장르 키워드 → 책 제목`을 유지한다. 책 페이지는 검증한 판본의 실제 부·장 링크만, 장은 실제 절 링크만, 절은 실제 세부 절 링크만 소유한다. 같은 페이지 anchor, 임의의 요약 계층, 소개용 자식, `키워드:`·`영역: Area N`을 목차처럼 만들지 않는다.
- 학습 책 첫 화면은 검증한 판본의 `부 → 장` 목차만 보여 준다. 장 화면은 실제 `절`, 절 화면은 실제 `세부 절`만 보여 주며 한 화면이 두 단계 이상을 펼치지 않는다. 탐색 모양을 위해 빈 하위 문서나 `학습 자료`, `체크포인트`, `다시 열었을 때` 같은 가짜 자식을 만들지 않는다.
- 책 계층에는 `2주·1달·5달` 중요도 색인을 두지 않는다. 1·2차 책 leaf는 원문의 설명·도판·code만 소유하고 선형 이동은 Map과 관계 metadata가 소유한다. 실제 대화에서 확인된 오개념·실행·결과·인출·전이는 4차 `understanding-enriched`에서만 기존 문맥에 자연스럽게 병합하며 반복 workflow section을 만들지 않는다. 재사용 가능한 일반 개념은 개념 Wiki에 병합하되 책 절을 대체하거나 같은 본문을 복제하지 않는다.
- 책 절의 원문 기반 설명은 대화 보강보다 먼저 존재하는 기준층이다. 이후 학습 대화에서 드러난 오개념·질문·실행 결과는 해당 절의 보강 section에 출처와 시점을 남겨 병합하되, 기준층의 주장·예제·목차를 삭제하거나 대화 내용으로 바꾸지 않는다. 서로 충돌하면 원문, 현재 공식 문서, 사용자 관찰을 분리하고 어느 하나를 조용히 덮어쓰지 않는다.
- 책 leaf와 일반 개념은 별도 parent tree와 canonical identity를 유지한다. 책 밖의 질문·새 근거·현재 버전은 개념 문서를 성장시키고, 책의 특정 판본 설명은 책 leaf에 남는다. 둘은 `related_to`와 검증된 본문 wikilink로 연결하되 같은 설명을 복제하거나 한쪽을 다른 쪽의 child로 만들지 않는다.
- 책 tree의 판본·목차·번역·실행 예제 안착을 먼저 완료하고, 개념 tree 연결 확장은 별도 hash 기반 증분 실행으로 처리한다. 개념 연결을 위해 책 장을 다시 생성하거나 전체 개념 corpus를 매 장마다 재검색하지 않으며, 개념 연결 미실행은 source-covered 책 장의 완료를 막지 않는다.
- `콘텐츠` subtree와 Facet은 만들지 않는다. 강의·글·영상에서 얻은 의미는 기존 주제 Wiki에 흡수하고, 외부 원자료와 PDF·이미지·전사는 `Wiki → 리소스 → 분야 텍스트 → 원자료 링크`로만 색인한다. 같은 출처·대상·용도라는 이유로 중간 bundle 문서를 만들지 않는다.
- 책이 아닌 외부 자료의 의미 부모나 `resource_keyword`를 확정할 수 없으면 중간 콘텐츠 카드를 만들지 않고 Review로 보낸다. Novel·민감 자료는 일반 리소스 Graph에 중복 노출하지 않는다.
- 프로젝트 entity는 목표·완료 조건, 요구사항, 설계, 결정, 구현, 검증, 결과, 남은 문제를 subtree와 본문으로 관리한다.
- 인물 hub의 직접 child는 사람 이름의 person entity뿐이다. 인물 entity는 관계·프로젝트·결정·대화·자료를 주제 wikilink로 묶고 사건은 같은 페이지의 `이력`에 날짜순으로 누적한다. 날짜만을 위한 별도 히스토리 문서를 만들지 않는다. 사람 이름과 특정 분석 제목을 별도 인물처럼 병렬로 두지 않는다. 이름 한 번의 언급으로 entity를 만들지 않는다.
- 질문과 답변은 관련 키워드 본문에 둔다. 질문 자체가 계속 갱신되는 독립 정체성일 때만 detail child로 분리한다.

## 파생 화면 경계

- `maps/`에는 `.canvas`와 plugin profile 같은 화면 상태만 둘 수 있다. Markdown Map, 별도 키워드 목록, 독립 시작 노트를 만들지 않는다.
- Global Graph는 `graph/overview` tag가 있는 root·hub·entity만 보여 준다. leaf는 현재 페이지의 subtree, Local Graph, Linked Graph에서 연다.
- `.base`, Canvas, Linked Graph는 Wiki metadata와 실존 wikilink를 읽는다. 화면에만 존재하는 제목·답변·관계·순서를 만들지 않는다.
- 한 문서의 code·실행·상태 관계를 설명하는 canonical 시각화는 `$diagram`의 Markdown Mermaid다.

### Graph 색상 계약

Global Graph, Local Graph, Linked Graph는 서로 다른 탐색 범위를 보여 주더라도 같은 metadata가 같은 색을 가져야 한다. 제목·폴더명·본문 단어를 추측해 색을 정하지 않고 다음 우선순위로 판정한다.

1. `type: calendar-event`, `entity_kind: event|schedule`, `facets: 일정|캘린더`는 **일정 · amber/orange**다.
2. `entity_kind: person` 또는 `facets: 인물`은 **인물 · pink**다.
3. `entity_kind: project` 또는 `facets: 프로젝트`는 **프로젝트 · blue**다.
4. `entity_kind: book`은 **책 · purple**, `entity_kind: resource`는 **리소스 · cyan**이다.
5. 위 의미 범주가 없고 `node_kind: topic|detail`인 node는 **개념·하위 항목 · green**이다.
6. `node_kind: root|hub`는 **탐색 허브 · teal**, 그 밖의 entity와 판정 불가 node는 **neutral gray**다.

색은 관계 종류나 상태를 대신하지 않으며 node dot에만 적용한다. 제목은 host text color를 유지한다. Global Graph는 위 색상과 무관하게 `graph/overview` tag가 있는 대표 node만 보여 주며, 일정이라는 이유만으로 전체 Calendar event를 Global Graph에 펼치지 않는다. Local Graph는 현재 문서의 실제 연결, Linked Graph는 현재 Markdown의 실제 outgoing link와 일시적 preview에 같은 판정 함수를 적용한다. 새 entity kind를 추가할 때는 세 화면의 query·parser·legend를 함께 갱신하고, light/dark theme에서 네 핵심 범주인 인물·개념·프로젝트·일정을 서로 구별할 수 있는지 확인한다.

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
3. root의 직접 child 링크, hub의 직접 링크·작은 분류·명시적 `navigation_groups` 2단 불릿, topic·entity의 child·latest 링크가 실제 metadata와 일치하며 hub에 최신 subtree를 펼치거나 설명·날짜·개수를 반복하지 않는다. 명시적 평탄 인덱스 예외를 제외한 모든 다중 child 페이지는 한 축의 `navigation_groups`를 가진다.
4. `콘텐츠` 분류가 없고 책 화면은 장르 텍스트→한국 번역판 책 링크→검증한 판본의 부·장·절 선형 목차로 이어지며, 리소스는 분야 텍스트→원자료 링크이고 프로젝트·인물 entity는 각각 project·topic-timeline 계약을 충족한다.
5. Canvas target과 edge가 실존 Wiki 관계와 일치하고 수동 배치를 보존한다.
6. Obsidian에서 root tree, entity tree, latest, Global Graph, Local Graph를 실제로 확인한다. UI 확인 전에는 정적 검증 완료로만 보고한다.
