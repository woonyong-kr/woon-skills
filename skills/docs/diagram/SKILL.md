---
name: diagram
description: Markdown Mermaid로 architecture·flow·sequence·state·class·ER을 설계·검토하거나 Obsidian JSON Canvas와 정본·light·dark 경계를 판단할 때 사용한다.
---

# Diagram

그림이 답할 질문을 한 문장으로 먼저 정하고 유형 하나를 고른다: 흐름 `flowchart`, 호출 순서 `sequenceDiagram`, 상태 `stateDiagram-v2`, 타입 `classDiagram`, cardinality `erDiagram`.

overview는 9 nodes 이내, node는 한 동작·상태, sibling label은 같은 문법으로 유지한다. source identifier를 정확히 쓰고 inheritance, runtime call, DB relation을 한 그림에 섞지 않는다. 색을 hard-code하지 말고 위치·선·label로 의미를 전달한다.

완료 전에 [diagram checklist](references/diagram-checklist.md)로 source 대조, branch 구분, light/dark render, clipping을 확인한다. 다른 저장소는 이 스킬을 복사하지 말고 `repo://skills/skills/docs/diagram`을 참조한다.

학습용 code·memory·exception 흐름에서는 AI raster image를 만들지 않는다. `woon resolve repo://skills/standards/learning-content-quality.md`의 diagram gate를 적용해 실제 identifier, 의미 있는 공간 구획, 번호가 붙은 arrow, diagram 뒤의 관찰 설명으로 같은 정보 품질을 만든다.

Obsidian `.canvas`를 요청해도 검증된 Markdown Mermaid를 삭제하거나 색만으로 필수 의미를 표현하지 않는다. Canvas는 같은 identifier·단계를 유지하고 Obsidian·공개 renderer를 별도 검증한 보조물로만 둔다. 세부 계약은 `woon resolve repo://skills/standards/obsidian-compatibility.md`를 읽는다.
