---
name: knowledge-navigation
description: LLM Wiki, 학습 노트, 면접 문답을 키워드에서 질문·답변·후속 질문으로 연결하고 Markdown 정본과 Obsidian JSON Canvas 보조 지도를 함께 만들거나 검증할 때 사용한다. 지식 지도, Canvas, 문서 간 탐색, 질문 노트 구조화, 고아 문서·중복 키워드 점검 요청에 적용한다.
---

# Knowledge Navigation

`$knowledge-navigation`은 여러 Markdown 문서 사이를 탐색하는 방법을 정한다. 답과 근거는 Markdown에 남기고, `.canvas`는 그 Markdown 파일이나 특정 heading/block을 여는 보조 뷰로만 만든다. Canvas 카드·edge label·group에만 존재하는 지식은 만들지 않는다.

먼저 `$knowledge`로 기존 정본과 동일 질문을 찾는다. LLM Wiki의 읽는 페이지는 compiler 산출물인 `wiki/`이므로 직접 고치지 않는다. 새 지식은 `$archive` 또는 `$compile-knowledge`의 source·claim·page spec 경로로 넣고, 이 skill은 그 문서로 가는 질문·키워드 지도만 소유한다.

## 도구 선택

- 프로젝트 → 키워드 → 질문처럼 여러 Markdown 문서를 계층으로 탐색해야 하면 Markdown Mindmap을 주 도구로 쓴다.
- 특정 문서·heading 사이의 제한된 공간 배치를 보고 싶으면 이 skill과 JSON Canvas를 보조 뷰로 쓴다.
- 한 Markdown 문서의 heading 흐름을 빠르게 복습·발표·면접 리허설해야 하면 Light Mindmap을 쓴다. 이는 여러 문서를 독립 노드로 탐색하는 도구가 아니다.
- 코드·실행·상태 관계를 설명해야 하면 `$diagram`의 Markdown Mermaid가 정본이다. Canvas와 Light Mindmap은 Mermaid를 대체하지 않는다.

## Markdown 정본 계약

1. 지도 Markdown에 `keywords`, `canvas_view`, `canvas_sync`를 기록하고, `## Canvas 노드` 아래에 Canvas에 놓을 문서/heading 링크를 정확한 vault 상대 wikilink로 적는다.
2. 질문은 `질문 → 답변 → 근거 → 후속 질문`을 Markdown에 쓴다. 짧은 답이라도 근거 문서 또는 확인 상태를 남기며, 답이 없는 질문은 `미확인`으로 둔다.
3. 같은 키워드는 같은 지도 안에서 한 번만 대표로 둔다. 동의어는 새 노드가 아니라 대표 문서의 alias 또는 본문 표기로 연결한다.
4. 답이 LLM Wiki를 바꾸면 source·claim·page spec을 갱신하고 compiler를 실행한다. 지도는 compiler가 만든 Markdown으로 연결하지만, compiler output을 직접 편집하지 않는다.

## Markdown Mindmap 계약

Markdown Mindmap은 Markdown 파일과 frontmatter 관계만 읽어 지도 block을 다시 그린다. 프로젝트·키워드·질문·후속 질문은 각각 실제 `.md` 파일이고, 카드의 답변은 질문 문서의 `## 짧은 답변`, `## 상세 근거`, `## 후속 질문`에 둔다.

1. node 문서에는 `mindmap_role`, 안정적인 `mindmap_id`, 부모 문서를 가리키는 `parent: "[[...]]"`를 둔다. 관계를 map block이나 plugin 설정에 중복 저장하지 않는다.
2. map host에는 `mindmap` fenced block만 두고, level은 폴더와 `mindmap_role`로 고른다. edge의 `via`는 child의 `parent`여야 한다.
3. 새 질문을 추가할 때는 질문 Markdown과 `parent`만 만들고 map host에서 Refresh한다. 별도 node 데이터·Canvas text card·복사한 답변을 만들지 않는다.
4. 후속 질문은 질문 본문의 wikilink와 별도 follow-up map으로 연결한다. 한 map에 모든 깊이를 추가해 무한한 나무를 만들지 않는다.
5. plugin card를 눌러 여는 rendered note가 답변의 유일한 본문이다. map에는 제목·선·필터만 둔다.

공식 plugin이 설치되지 않았으면 `$obsidian-plugin`의 Core adapter로 정확한 plugin ID를 확인한다. map block을 쓰는 문서는 Reading view 또는 Live Preview에서 renderer를 확인하고, Refresh 뒤 새 문서가 실제 card로 보이는지 재확인한다.

정적 관계 검사는 아래 명령으로 실행한다. 이는 map block의 level·role·`parent`와 `mindmap_id`만 검사하며, rendered card 검증을 대신하지 않는다.

```bash
python3 "$(woon resolve repo://skills/skills/knowledge/knowledge-navigation/scripts/validate_markdown_mindmap.py)" \
  --vault <vault> \
  --map <vault-relative-map.md>
```

## Canvas 계약

1. `.canvas`에는 `file` node와 node 사이 edge만 둔다. `text`, `link`, `group` node와 edge `label`은 금지한다.
2. 각 node의 `file`은 vault 안의 기존 `.md`이고, `subpath`를 쓸 때는 실제 `# heading` 또는 `#^block-id`여야 한다. 절대 경로, Canvas 자체, 이미지, 외부 URL은 넣지 않는다.
3. Canvas에서 읽어야 하는 제목·질문·답은 대응 Markdown heading 또는 block에 있다. Canvas의 위치·크기·선은 탐색 순서만 보조한다.
4. 신규 Canvas는 `auto-` ID만 AI가 소유한다. `manual-` ID와 그 node에 닿는 edge는 사용자의 배치이므로 재생성 전에 이전 파일과 비교해 달라지면 멈추고 계획만 보고한다. 접두어가 없는 기존 Canvas는 전부 수동 배치로 취급한다.
5. 대량 변경 전에는 대상 Markdown, 현재 Canvas, 생성 범위, 보존할 `manual-` 범위를 표로 제시한다. 동의 없이 전체 Vault를 재배치하거나 모든 문서를 Canvas에 넣지 않는다.

생성 뒤에는 아래 검사를 실행한다. `--previous`는 재생성일 때만 준다.

```bash
python3 "$(woon resolve repo://skills/skills/knowledge/knowledge-navigation/scripts/validate_canvas.py)" \
  --vault <vault> \
  --canvas <vault-relative-map.canvas> \
  --map <vault-relative-map.md>
```

재생성일 때만 `--previous <previous-canvas>`를 추가한다.

## Light Mindmap 분기

Light Mindmap은 `type: mindmap` Markdown의 H1~H6 heading을 한 문서 안에서 렌더한다. 다음에만 사용한다.

- 긴 한 문서의 학습 순서·면접 답변·발표 개요를 연습할 때
- heading 하나가 개념 하나이고, heading에 둔 wikilink를 클릭해 보충 문서로 이동하게 할 때

다음에는 사용하지 않는다.

- 여러 독립 문서를 모두 node로 배치하는 탐색 지도
- compiler가 소유하는 `wiki/` 출력의 frontmatter를 바꾸는 일
- Mermaid의 코드·실행·상태 관계를 꾸미기 위한 대체 그림

AI는 Light Mindmap 문서에서 `type`, `mindmap-layout`, `mindmap-theme`, `mindmap-line`, `mindmap-node` frontmatter와 근거가 있는 heading만 바꾼다. 시각 균형을 맞추려고 heading·사실·질문을 새로 만들지 않으며, Canvas·diagram·이미지를 삽입하지 않는다. 플러그인의 node 직접 편집은 Markdown heading을 수정하므로, 수정 뒤 source view diff와 link 검증을 다시 실행한다.

표시 검증은 plugin이 설치·활성화된 Obsidian에서 source view, light theme, dark theme로 같은 문서를 열어 heading 누락·클리핑·wikilink 이동을 확인하는 것이다. 설치되지 않았거나 UI adapter가 없으면 정적 계약 검사까지만 통과로 기록하고 rendered 검증은 미완료로 남긴다.

## 완료 기준

1. Markdown의 `## Canvas 노드`와 Canvas node 대상이 일치한다.
2. JSON Canvas 구문, Markdown target, heading/block target, duplicate keyword, manual placement 보존 검사가 통과한다.
3. 새 지식이 compiler 범위면 `$compile-knowledge`의 compile·audit도 통과한다.
4. Canvas는 Obsidian에서, Light Mindmap은 light/dark에서 실제로 열리는 것을 별도로 확인한다. 이 중 UI 표시를 확인하지 못한 것은 완료가 아니라 정적 검증 완료다.
