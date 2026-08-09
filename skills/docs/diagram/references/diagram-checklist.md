# 다이어그램 검사표

- Mermaid fence 바로 앞에 그림이 답할 질문을 실제 identifier가 포함된 질문형 문장으로 한 개만 명시한다.
- 관계에 맞는 Mermaid 유형을 사용하고 inheritance·runtime call·DB relation을 한 그림에 섞지 않는다.
- overview는 9 nodes 이하, node 하나는 한 동작이나 상태, label은 세 줄 이하로 둔다.
- source의 class·method·variable·value identifier를 그대로 사용한다.
- 순서가 의미라면 arrow label에 `1.`부터 번호를 붙이고 뒤의 설명도 같은 번호를 사용한다.
- 정상·오류, 값 복사·reference 공유는 text label과 line style로 구분한다.
- hard-coded fill·text color와 red/green만의 의미를 사용하지 않는다.
- 선행 조건은 의존 단계보다 먼저 나타나며 crossing line과 잘린 text가 없다.
- Markdown 안의 Mermaid source를 정본으로 유지하고 생성된 SVG·PNG를 정본으로 삼지 않는다.
- default·dark theme로 실제 render해 syntax, contrast, clipping과 label 가독성을 확인한다.
- Obsidian split pane처럼 폭이 좁은 대상은 목표 pane 폭을 정하고 SVG natural `viewBox` width와 실제 Reading view를 함께 확인한다. 학습 문서 fixture의 기준은 640 CSS px다.
- 640px의 3-participant sequence는 자연 폭 620px 이하를 생성 목표로 둔다. `actorMargin: 24`, `width: 112` init, 짧은 identifier와 한글 16자 이내 arrow label을 적용한다. participant가 더 많으면 diagram을 나누고 620px를 넘는 가로 flowchart는 `TD`를 우선한다. acceptance 상한 640px와 생성 목표 620px를 혼동하지 않는다.
- repository가 고정한 Mermaid tool과 version을 우선한다. 없으면 bundled `scripts/verify-mermaid.sh`를 사용하고 unversioned package나 mutable latest를 호출하지 않는다.
- bundled verifier의 exit `2`는 renderer unavailable이다. package 설치와 network 재시도를 하지 않고 미검증 범위를 보고한다.
- 두 theme의 command exit와 생성물 크기를 verifier 한 번으로 확인한다. 한 theme가 중단됐는데 다른 theme까지 검증됐다고 보고하지 않는다.
