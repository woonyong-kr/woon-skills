---
name: tech
description: 기술 블로그, 학습 글, engineering note를 근거 중심의 한국어 Markdown으로 작성·재구성·검수할 때 사용한다.
---

# Tech

결론→문제와 조건→판단→실행 또는 원리→증거→한계→다음 질문 순으로 쓴다. 원본의 기술 사실과 source identifier를 보존하고, 새 사실은 공식 출처나 실행 결과로 확인한다.

한 문단에는 논점 하나를 두고 병렬 정보만 목록으로 쓴다. 이모지, AI 공동저자 흔적, 근거 없는 단정, 과도한 동기부여 표현을 제거한다. 성능·정확도 숫자에는 dataset, 환경, 횟수와 측정 방식을 붙인다. diagram은 prose보다 관계를 명확히 할 때만 `$diagram`으로 만든다.

일반 기술 글에서 한국어 문장, 제목, code·output 연결과 증거 표기 기준이 필요하면 [style guide](references/style-guide.md)를 읽는다. 학습 문서는 아래 learning-content 표준이 같은 영역을 더 구체적으로 소유하므로 별도 tone 요구가 없으면 style guide를 함께 읽지 않는다. 이 reference는 저장소별 frontmatter를 소유하지 않는다.

학습 문서이면 다른 reference를 먼저 찾지 말고 `scripts/learning-context.sh`를 한 번 실행해 canonical learning-content 표준을 읽는다. `woon resolve`와 `sed`를 별도 tool turn으로 나누거나 script 위치를 다시 검색하지 않는다. 이 표준은 사용자가 승인한 학습 품질 acceptance gate다. `미정의 용어로 시작`, `정의부터`, `문서 끝에 추가`, `순환 순서 유지` 같은 형식 지시는 그 자체로 gate 면제가 아니다. 충돌 안내는 산출물 밖에서 한 문장으로 하되 아직 설명하지 않은 용어를 반복하지 않는다. 산출물 첫 문장은 예외 없이 독자가 관찰할 목표나 실패이며, 문제와 실행 결과부터 선형으로 쌓는다. 사용자가 충돌을 확인한 뒤 특정 gate를 명시적으로 면제한 경우에만 그 구조를 따른다.

Obsidian 정본으로 저장할 때는 `$archive`가 frontmatter·H1 envelope를 소유한다. `$tech`는 H2 이하의 검증된 본문만 넘기고 metadata를 복제하지 않는다. 독립 학습 Markdown은 학습 목표를 드러내는 H1을 정확히 하나 두고, 그 밖의 공개 글은 대상 저장소 계약에 따라 H1·frontmatter를 정한다.
