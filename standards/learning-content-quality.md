# Learning content quality gate

## Purpose

Vault Wiki의 사실성, 증거, source·claim·page·receipt 관계, code·diagram 일치, Obsidian 표시를 검사하는 내부 품질 gate다. 문서를 어떤 순서와 문체로 쓸지는 `learning-writing-harness.md`가 소유하며, 두 표준은 항상 함께 적용한다.

문체와 구성의 근거는 `learning-style-corpus.yaml`이 소유한다. 표본은 교체하거나 추가할 수 있으므로 이 파일에는 강사, 강의, 교재, 세부 목차를 고정하지 않는다.

승인된 표본 분석에서 얻은 문체·전개 원칙은 재사용하되, 특정 문장·코드·그림은 복제하지 않는다.

## Document map

작성 전에 산출물 밖의 짧은 장부를 만든다.

- `audience`: 독자가 이미 알고 있거나 할 수 있는 일
- `goal`: 문서 끝에서 독자가 판단, 설명, 실행 또는 다시 찾을 수 있어야 하는 일
- `requires`: 문서 밖에서 이미 알고 있다고 가정하는 배경
- `introduces`: 각 section이 처음 설명하거나 판단에 쓰는 사실·개념·결정
- `evidence`: source, 실제 관찰·실행 결과, code, 인용, 표, timeline 또는 diagram 중 claim을 확인할 근거

제목과 heading hierarchy가 목차의 정본이다. 개념 의존 순서가 확정된 뒤 heading을 배치하고, 수동 목차는 대상 renderer의 anchor를 실제 확인할 수 있을 때만 생성한다. 정본 heading과 별개인 손편집 목차를 유지하지 않는다.

독립 Wiki 문서는 독자가 다시 찾을 질문이나 목표를 드러내는 H1을 정확히 하나 둔다. `$archive`에 전달하는 본문은 archive가 frontmatter와 H1을 소유하므로 H2부터 시작한다. 두 경우 모두 heading level을 건너뛰지 않는다.

## One canonical chapter, three responsibilities

Vault Wiki는 LLM의 정본, 혼자 읽는 자료, 동료에게 설명하는 자료를 위해 각각 다른 문체의 사본을 만들지 않는다. 하나의 정본 장을 두고, 각 책임을 아래처럼 분리한다. 이렇게 해야 설명을 고친 뒤 검색용 요약이나 설명용 사본이 먼저 낡는 일을 막을 수 있다.

- **정본과 검색**은 `source`, `claim`, `page`, `receipt`, `purpose`, 정확한 identifier, 동의어, H1/H2 hierarchy가 맡는다. 출처, 사실의 범위, 검색 필터와 재생성 경로는 이 계층에서 명시한다.
- **독자 본문**은 한국어 독자가 흐름을 따라 읽을 수 있는 설명을 맡는다. 자연스러운 문장을 키워드 목록이나 claim 조각으로 바꾸지 않고, section 하나가 하나의 의미 덩어리로 검색되게 heading과 문단 경계를 쓴다.
- **설명 기능**은 본문 안의 질문, 관찰 가능한 예제·근거, 상태 변화, 적용 질문이 맡는다. 같은 내용을 발표 대본과 요약본으로 중복하지 않고, 동료가 필요한 section에서 읽기를 멈추거나 이어 갈 수 있게 한다.

LLM이 문맥을 찾기 좋게 만드는 핵심은 어색하게 짧은 문장이 아니라, 안정적인 제목 구조와 정확한 용어, 의미가 닫힌 문단, 정본 메타데이터다. 본문에서는 독자의 이해를 우선하고, 검색에 필요한 압축과 출처 추적 정보는 정본 계층에서 보완한다.

compiler가 검증한 일반 교과 개념의 출처는 `source → claim → page → receipt`가 소유한다. 같은 출처를 본문 문장마다 반복하지 않으며, inline citation이 없다는 이유만으로 근거 경계 실패로 판정하지 않는다. 본문은 일반 설명·구현 예시·특정 버전의 실제 실행·측정 결과를 서로 혼동하지 않아야 한다. `> 확인 범위:`가 있으면 그 문장을 적용 경계의 우선 근거로 사용하고, 본문이 그 경계를 직접 모순할 때만 실패로 판정한다.

품질 검토의 실패는 선택한 현재 Markdown anchor가 결함을 직접 입증할 때만 유효하다. 자연스러운 완전한 문장을 막연히 부족하다고 평가하거나, 일반 교과 설명을 inline citation 부재만으로 탈락시키는 판정은 오탐이다. 명확한 결함을 현재 문장에서 입증하지 못하면 통과시킨다.

## Gate scope

- 문서마다 같은 heading, 문장 수, code block 수, diagram 수를 강제하지 않는다.
- 어떤 작성 경로를 골랐더라도 독자가 관찰한 장면, 이유, 기술적 근거, 적용 경계 사이의 연결을 따라갈 수 있어야 한다.
- 짧은 참고 문서는 필요한 단계만 사용한다. 분량을 채우기 위해 역사, 일반론, 비유를 추가하지 않는다.
- `node_kind: root|hub|entity`인 탐색 페이지는 설명 장이 아니라 키워드 hyperlink surface다. H1과 직접 하위 키워드 링크만으로 판정하며, 본문 prose·근거 section·요약을 추가하라고 요구하지 않는다. 정보·판단·이력 품질은 링크된 detail·information·history 문서에서 검사한다.
- `private/novel/**/source-*`와 `private/novel/people/*` 같은 source/relation projection은 내부 원본 또는 정본 인물로 가는 링크가 목적이다. 링크의 정확성·privacy·단일 소유권을 검사하고 설명 분량을 늘리지 않는다.

## Concept grounding

목차를 쓰기 전에 독자가 이미 안다고 가정할 **선행 개념**과 문서 안에서 새로 설명할 개념을 구분한다. 선행 개념은 대상 독자에게 실제로 기대할 수 있는 것만 둔다. 작성 중에는 공개할 필요 없는 짧은 장부로 각 section의 `requires`와 `introduces`를 추적한다.

- section은 앞에서 소개했거나 선행 개념으로 선언한 개념만 사용한다.
- 산출물 첫 문장은 선택한 route에 맞는 구체적인 목표, source, 현재 상태, 판단 장면 또는 실패다. 요청문이 제시한 미정의 기술 문장을 그대로 인용해 시작하지 않고, 코드 실행이 없는 기록·결정 문서에 가상의 실패를 만들지 않는다.
- 새 용어는 먼저 구체적인 문제나 관찰을 보여 준 뒤, 그 관찰을 부를 이름으로 도입한다. 용어집을 서두에 덤프하지 않는다.
- 새 내용을 추가할 때 문서 끝을 기본 위치로 삼지 않는다. 필요한 선행 개념이 모두 소개된 뒤이면서, 그 내용을 처음 요구하는 section보다 앞선 가장 이른 위치에 넣는다.
- 개념 의존성이 순환하면 순서를 그대로 복제하지 않는다. 실행 가능한 최소 사례나 관찰 가능한 현상으로 한 개념의 전제를 끊고, 나머지를 그 위에 선형으로 쌓는다.
- 기술 용어뿐 아니라 이름 없는 아이디어도 선행성 검사 대상이다. `aliasing`, `defensive copy`처럼 새 용어를 쓰면 같은 section에서 관찰 가능한 의미와 필요를 연결한다.
- 사용자가 특정 순서를 요구해도 아직 설명하지 않은 개념에 의존하게 만드는 순서는 그대로 따르지 않는다. 재배치 이유와 보존한 요구를 짧게 밝힌다.

완성 후 첫 등장부터 역방향으로 검사한다. 각 개념의 첫 사용 지점에서 독자가 그 의미를 이미 알 수 없다면, 설명을 앞당기거나 의존하는 문장을 뒤로 옮긴다.

## Paragraph and evidence quality

아래의 code, output, Mermaid 세부 규칙은 해당 근거를 실제로 쓰는 문서에만 적용한다. 사건 기록, 조사, 결정, 절차처럼 코드가 없는 Wiki도 source·사실·해석·범위·재열람 경로의 같은 정본 계약을 따른다.

- section 하나는 질문 하나에 답한다.
- 결론이나 현재 관찰을 section 첫 문장에 둔다.
- prose, code, output, diagram, timeline에서 class·method·variable·entity 이름을 동일하게 유지한다.
- 첫 실행 예제, 그 output과 바로 뒤 diagram은 같은 source snapshot을 설명한다. 아직 제시하지 않은 개선 코드의 branch·catch·state를 현재 그림에 미리 넣지 않는다.
- code, 인용, 표, timeline, diagram 전에는 볼 이유를, 뒤에는 관찰할 결과를 설명한다.
- output fence에는 `text` 또는 `console` language를 붙인다. 문서 안의 **모든 output fence 각각**의 바로 위 한 줄은 `검증 상태: 실제 compile·run 결과` 또는 `검증 상태: 미실행 예상 결과` 중 정확히 하나다. 첫 output에만 표시하거나 code 앞·fence 뒤에서 대신 설명하지 않는다. stdout과 stderr를 나누면 각 channel 이름을 같은 줄에 덧붙인다.
- shell command는 `bash` 또는 command-only `console` fence에, stdout·stderr는 별도 output fence에 둔다. output fence에 `$ javac`, `$ java` 같은 prompt를 섞지 않는다. 완전한 source가 아닌 부분 snippet·method 교체안에는 독립 compile·run 결과를 붙이지 않는다. 결과가 필요하면 완전한 source를 다시 제시하거나 앞의 실행 가능한 source에 적용할 diff임을 명시하고 전체 source로 검증한다.
- 한 단계에서 바뀌는 조건을 최소화해 원인과 결과를 추적할 수 있게 한다.
- 초급 설명은 용어를 제거하지 말고 처음 등장할 때 정의한다.
- 중급 설명은 단순화를 명시하고 실제 failure mode와 한계를 남긴다.
- 근거 없는 단정, 장식적 수사, AI narration을 제거한다.

## Visual rhythm

- heading 직후에는 그 section이 답할 질문이나 결론을 둔다.
- code·output·diagram을 연속해서 던지지 말고 각각 앞뒤에 관찰 목적과 결과를 연결한다.
- 한 code block은 한 변화만 보여 주고, 긴 전체 코드는 실행 가능한 source와 연결한 뒤 핵심 부분만 설명한다.
- output은 code와 다른 fence로 분리하고 실제 실행 여부를 표시한다.
- 같은 종류의 주의·한계는 같은 callout 또는 문장 형식을 사용한다. 색과 아이콘만으로 의미를 전달하지 않는다.
- 문단, 목록, code와 diagram 사이에 충분한 여백을 두되 의미 없는 빈 section이나 장식용 표를 만들지 않는다.

## Diagram quality

그림은 이미지 장식이 아니라 상태와 관계의 실행 가능한 설명이다. 기본 출력은 Markdown Mermaid다.

- 그림 하나는 질문 하나만 답한다.
- overview는 9 nodes 이내로 제한하고 상세 단계는 여러 diagram으로 나눈다.
- 코드·실행 흐름은 실제 identifier와 value를 사용하고, 조사·결정·일반 구조는 source에 있는 안정적인 역할·행위자·개념 이름을 사용한다.
- before/after, stack/heap, caller/callee처럼 공간 구획에 의미를 준다.
- 순서가 중요하면 arrow에 번호를 붙이고 prose도 같은 번호로 해설한다.
- 값 복사와 reference 공유, 정상 흐름과 exception 흐름처럼 혼동되는 선은 label과 line style로 구분한다.
- failure는 decorative icon이나 color만으로 표시하지 말고 text label과 path로 표현한다.
- light/dark mode에서 읽히도록 hard-coded fill과 text color를 피한다.
- diagram 앞에는 질문, 뒤에는 독자가 읽어야 할 2~5개 관찰을 둔다.
- source와 대조하고 Mermaid render에서 clipping, crossing, contrast를 확인한다.
- Obsidian에서 볼 문서는 640 CSS px split pane에서도 핵심 label과 arrow가 가로 스크롤 없이 읽혀야 한다. diagram 자연 폭은 20px 안전 여유를 둔 620px 이하로 설계하고 최종 acceptance만 640px로 판정한다.
- 3-participant `sequenceDiagram`은 Mermaid fence 첫 줄에 `%%{init: {"sequence": {"actorMargin": 24, "width": 112}}}%%`를 정확히 둔다. participant에는 실제 짧은 identifier만 두고 arrow label은 번호를 포함해 한글 16자 이내로 줄이며 type·signature와 긴 설명은 prose로 옮긴다.
- before/after를 한 그림에 함께 놓으면 두 snapshot과 바뀐 지점을 명시적으로 구획한다. 그렇지 않으면 현재 code snapshot과 개선 snapshot을 별도 그림으로 나눈다.

AI raster image로 code, memory, sequence를 설명하지 않는다. 실제 screenshot, 측정 chart, 물리적 대상, 강의·PDF의 원본 figure처럼 Mermaid가 사실을 보존하지 못하는 자료는 source image를 유지한다. source image의 hash·caption·출처·page·권리·공개 범위를 기록하고, 같은 bytes는 한 canonical asset만 참조한다. code·state Mermaid와 source image가 서로 다른 질문에 답할 때만 함께 두며 장식용 중복은 만들지 않는다. private/local-only source image는 공개 산출물에 포함하지 않는다.

## Acceptance gate

- 첫 20% 안에 독자가 해결할 구체적 문제 또는 이 기록을 남긴 이유를 이해한다.
- 새 개념은 그 필요가 드러난 뒤 정의된다.
- 모든 section의 개념 의존성이 선행 개념 또는 앞선 section에서 충족되며, 순환 의존이 없다.
- 추가한 내용은 문서 끝이 아니라 의존성상 가장 이른 유효 위치에 놓인다.
- 중요한 claim은 source, 실제 관찰·실행 결과, code, 인용, 표, timeline 또는 diagram에서 확인된다.
- 새 기록에는 purpose, visibility, 재열람 질문이 남고, source가 직접 말한 사실과 현재 해석·미결정이 구분된다.
- diagram 없이 prose만으로도 핵심 사실이 남고, diagram은 관계 이해를 실제로 줄여 준다.
- code와 diagram identifier가 source와 일치한다.
- summary는 본문에 없던 주장을 추가하지 않는다.
- 초급 독자가 따라갈 수 있고 숙련 독자가 잘못된 단순화를 발견하지 않는다.
- heading hierarchy에서 level을 건너뛰지 않고 목차 순서와 개념 의존 순서가 일치한다.
- code가 있으면 실제 compile·run 또는 명시한 정적 검사로 확인되고, output의 증거 상태가 표시된다.
- Mermaid가 있으면 default·dark theme에서 실제 render되며 source와 생성물의 identifier가 일치한다.
- Obsidian 정본이면 `repo://skills/standards/obsidian-compatibility.md`의 envelope·link·visibility gate를 함께 통과한다.
