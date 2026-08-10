---
name: diagram
description: Markdown Mermaid로 architecture·flow·sequence·state·class·ER을 설계·검토하거나 Obsidian JSON Canvas와 정본·light·dark 경계를 판단할 때 사용한다.
---

# Diagram

그림이 답할 질문을 한 문장으로 먼저 정하고 유형 하나를 고른다: 흐름 `flowchart`, 호출 순서 `sequenceDiagram`, 상태 `stateDiagram-v2`, 타입 `classDiagram`, cardinality `erDiagram`. 산출물에서는 Mermaid fence 직전의 비어 있지 않은 문장을 실제 identifier가 포함되고 `?` 또는 `하는가.`로 끝나는 질문으로 쓰며, fence 뒤에는 같은 번호를 사용하는 관찰 2~5개를 둔다.

overview는 9 nodes 이내, node는 한 동작·상태, sibling label은 같은 문법으로 유지한다. source identifier를 정확히 쓰고 inheritance, runtime call, DB relation을 한 그림에 섞지 않는다. 색을 hard-code하지 말고 위치·선·label로 의미를 전달한다.

Obsidian의 640px split pane에 3개 participant를 놓는 `sequenceDiagram`은 자연 폭을 620px 이하로 설계해 20px 여유를 남긴다. 첫 줄에 `%%{init: {"sequence": {"actorMargin": 24, "width": 112}}}%%`를 사용하고 participant에는 class·variable identifier만 쓴다. type·signature는 prose로 옮기며 arrow label은 번호를 포함해 한글 16자 이내로 줄인다. 4개 이상이면 한 그림을 억지로 축소하지 말고 질문별로 나눈다. 가로 `flowchart LR`이 620px를 넘으면 `TD`로 바꾼다. 최종 acceptance는 640px 이하이며 620px는 생성 안전 목표다.

독립 diagram 작성·검토는 완료 전에 [diagram checklist](references/diagram-checklist.md)로 source 대조, branch 구분, light/dark render, clipping을 확인한다. 학습 문서에서는 아래 learning-content 표준이 같은 gate를 소유하므로 checklist를 중복해서 읽지 않는다. 다른 저장소는 이 스킬을 복사하지 말고 `repo://skills/skills/docs/diagram`을 참조한다.

Mermaid CLI가 repository에 고정되어 있지 않으면 이미 존재하는 `scripts/verify-mermaid.sh <source.mmd> <output-dir>`를 바로 한 번 호출한다. script 파일을 `find`·`rg`·`ls`로 다시 찾지 않는다. 이 script는 설치된 `mmdc` 또는 npm cache의 고정 version으로 default·dark SVG를 만든다. exit `2`이면 새 package를 설치하거나 같은 명령을 반복하지 말고 render를 미검증으로 남긴다. source 작성, 두 theme render와 파일 확인을 여러 tool turn으로 쪼개지 않는다.

학습용 code·memory·exception 흐름에서는 AI raster image를 만들지 않는다. `woon resolve repo://skills/standards/learning-content-quality.md`의 diagram gate를 적용해 실제 identifier, 의미 있는 공간 구획, 번호가 붙은 arrow, diagram 뒤의 관찰 설명으로 같은 정보 품질을 만든다. 단, PDF·웹·문서에 실제 UI·측정 chart·강의 도판 같은 설명력 높은 source figure가 있으면 Mermaid로 다시 그려 버리지 않는다. 원본 asset의 보존·권리·privacy·본문 매핑은 `repo://skills/skills/knowledge/ingest/references/source-assets.md`를 따른다.

Obsidian `.canvas`를 요청해도 검증된 Markdown Mermaid를 삭제하거나 색만으로 필수 의미를 표현하지 않는다. Canvas는 같은 identifier·단계를 유지하고 Obsidian·공개 renderer를 별도 검증한 보조물로만 둔다. 세부 계약은 `woon resolve repo://skills/standards/obsidian-compatibility.md`를 읽는다.
