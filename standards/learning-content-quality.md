# Learning content quality

## Purpose

기술 학습 문서의 텍스트와 Mermaid가 김영한 Java 강의 자료에서 확인한 설명의 인과성, 단계성, 가독성에 가까워지도록 하는 내부 품질 표준이다. 원본 표현이나 그림을 복제하지 않고 교육 구조만 적용한다.

대표 표본은 Java 입문의 메서드와 실전 Java 중급의 불변 객체, 예외 처리, 중첩 클래스 자료다. 모든 문서가 같은 목차를 가져야 한다는 뜻은 아니다.

## Text progression

독자가 새 개념이 왜 필요한지 경험한 다음 이름을 배우게 한다.

1. 구체적인 목표 또는 실패 상황을 짧게 제시한다.
2. 최소 실행 코드와 실제 결과로 현재 상태를 고정한다.
3. 중복, unexpected mutation, control flow, lifecycle 같은 문제를 한 번에 하나 드러낸다.
4. 문제를 설명할 필요가 생긴 시점에 개념과 용어를 정의한다.
5. 값, reference, call, state가 이동하는 순서를 실제 identifier로 추적한다.
6. 일반 규칙과 적용되지 않는 경계를 분리한다.
7. 개선 코드를 제시하고 이전 코드와 달라진 이유를 연결한다.
8. 작은 연습 또는 counterexample로 독자가 규칙을 적용하게 한다.
9. 마지막에 판단 기준만 요약하고 다음 개념과 연결한다.

짧은 참고 문서에는 필요한 단계만 사용한다. 분량을 채우기 위해 역사, 일반론, 비유를 추가하지 않는다.

## Concept grounding

목차를 쓰기 전에 독자가 이미 안다고 가정할 **선행 개념**과 문서 안에서 새로 설명할 개념을 구분한다. 선행 개념은 대상 독자에게 실제로 기대할 수 있는 것만 둔다. 작성 중에는 공개할 필요 없는 짧은 장부로 각 section의 `requires`와 `introduces`를 추적한다.

- section은 앞에서 소개했거나 선행 개념으로 선언한 개념만 사용한다.
- 산출물 첫 문장은 독자가 관찰할 구체적인 목표나 실패다. 요청문이 제시한 미정의 기술 문장을 그대로 인용해 시작하지 않는다.
- 새 용어는 먼저 구체적인 문제나 관찰을 보여 준 뒤, 그 관찰을 부를 이름으로 도입한다. 용어집을 서두에 덤프하지 않는다.
- 새 내용을 추가할 때 문서 끝을 기본 위치로 삼지 않는다. 필요한 선행 개념이 모두 소개된 뒤이면서, 그 내용을 처음 요구하는 section보다 앞선 가장 이른 위치에 넣는다.
- 개념 의존성이 순환하면 순서를 그대로 복제하지 않는다. 실행 가능한 최소 사례나 관찰 가능한 현상으로 한 개념의 전제를 끊고, 나머지를 그 위에 선형으로 쌓는다.
- 기술 용어뿐 아니라 이름 없는 아이디어도 선행성 검사 대상이다. `aliasing`, `defensive copy`처럼 새 용어를 쓰면 같은 section에서 관찰 가능한 의미와 필요를 연결한다.
- 사용자가 특정 순서를 요구해도 아직 설명하지 않은 개념에 의존하게 만드는 순서는 그대로 따르지 않는다. 재배치 이유와 보존한 요구를 짧게 밝힌다.

완성 후 첫 등장부터 역방향으로 검사한다. 각 개념의 첫 사용 지점에서 독자가 그 의미를 이미 알 수 없다면, 설명을 앞당기거나 의존하는 문장을 뒤로 옮긴다.

## Paragraph and code quality

- section 하나는 질문 하나에 답한다.
- 결론이나 현재 관찰을 section 첫 문장에 둔다.
- prose, code, output, diagram에서 class·method·variable 이름을 동일하게 유지한다.
- code 전에는 볼 이유를, code 뒤에는 관찰할 결과를 설명한다.
- 실행 결과와 예상 결과를 구분한다.
- 한 단계에서 바뀌는 조건을 최소화해 원인과 결과를 추적할 수 있게 한다.
- 초급 설명은 용어를 제거하지 말고 처음 등장할 때 정의한다.
- 중급 설명은 단순화를 명시하고 실제 failure mode와 한계를 남긴다.
- 근거 없는 단정, 장식적 수사, AI narration을 제거한다.

## Diagram quality

그림은 이미지 장식이 아니라 상태와 관계의 실행 가능한 설명이다. 기본 출력은 Markdown Mermaid다.

- 그림 하나는 질문 하나만 답한다.
- overview는 9 nodes 이내로 제한하고 상세 단계는 여러 diagram으로 나눈다.
- 실제 code identifier와 value를 사용한다.
- before/after, stack/heap, caller/callee처럼 공간 구획에 의미를 준다.
- 순서가 중요하면 arrow에 번호를 붙이고 prose도 같은 번호로 해설한다.
- 값 복사와 reference 공유, 정상 흐름과 exception 흐름처럼 혼동되는 선은 label과 line style로 구분한다.
- failure는 decorative icon이나 color만으로 표시하지 말고 text label과 path로 표현한다.
- light/dark mode에서 읽히도록 hard-coded fill과 text color를 피한다.
- diagram 앞에는 질문, 뒤에는 독자가 읽어야 할 2~5개 관찰을 둔다.
- source와 대조하고 Mermaid render에서 clipping, crossing, contrast를 확인한다.

AI raster image로 code, memory, sequence를 설명하지 않는다. 실제 screenshot, 측정 chart, 물리적 대상처럼 Mermaid가 사실을 보존하지 못하는 자료만 별도 image를 사용한다.

## Acceptance gate

- 첫 20% 안에 독자가 해결할 구체적 문제를 이해한다.
- 새 개념은 그 필요가 드러난 뒤 정의된다.
- 모든 section의 개념 의존성이 선행 개념 또는 앞선 section에서 충족되며, 순환 의존이 없다.
- 추가한 내용은 문서 끝이 아니라 의존성상 가장 이른 유효 위치에 놓인다.
- 중요한 claim은 code, output, source 또는 diagram에서 확인된다.
- diagram 없이 prose만으로도 핵심 사실이 남고, diagram은 관계 이해를 실제로 줄여 준다.
- code와 diagram identifier가 source와 일치한다.
- summary는 본문에 없던 주장을 추가하지 않는다.
- 초급 독자가 따라갈 수 있고 숙련 독자가 잘못된 단순화를 발견하지 않는다.
