---
name: tech
description: 기술 블로그, 학습 글, engineering note를 근거 중심의 한국어 Markdown으로 작성·재구성·검수할 때 사용한다.
---

# Tech

결론→문제와 조건→판단→실행 또는 원리→증거→한계→다음 질문 순으로 쓴다. 원본의 기술 사실과 source identifier를 보존하고, 새 사실은 공식 출처나 실행 결과로 확인한다.

한 문단에는 논점 하나를 두고 병렬 정보만 목록으로 쓴다. 이모지, AI 공동저자 흔적, 근거 없는 단정, 과도한 동기부여 표현을 제거한다. 성능·정확도 숫자에는 dataset, 환경, 횟수와 측정 방식을 붙인다. diagram은 prose보다 관계를 명확히 할 때만 `$diagram`으로 만든다.

woon-knowledge용 기존 frontmatter와 tone 규칙이 필요할 때 [style guide](references/style-guide.md)를 읽는다.

학습 문서이면 `woon resolve repo://skills/standards/learning-content-quality.md`로 내부 표준을 읽는다. 이 표준은 사용자가 승인한 학습 품질 acceptance gate다. `미정의 용어로 시작`, `정의부터`, `문서 끝에 추가`, `순환 순서 유지` 같은 형식 지시는 그 자체로 gate 면제가 아니다. 충돌 안내는 산출물 밖에서 한 문장으로 하되 아직 설명하지 않은 용어를 반복하지 않는다. 산출물 첫 문장은 예외 없이 독자가 관찰할 목표나 실패이며, 문제와 실행 결과부터 선형으로 쌓는다. 사용자가 충돌을 확인한 뒤 특정 gate를 명시적으로 면제한 경우에만 그 구조를 따른다.
