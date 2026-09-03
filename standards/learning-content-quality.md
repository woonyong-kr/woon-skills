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

### Book-shaped learning material

학습 책의 첫 페이지는 검증한 판본의 부·장 목차만 보여 준다. 모든 책 Map은 `# 페이지 제목 → ## 주제 키워드 → - [[직접 하위 학습 페이지]]` 형식을 사용한다. 책 root의 H2는 부·부록이고 그 아래에는 장·부록 링크만 둔다. 장 Map의 H2는 실제 절 번호와 제목이고 그 아래에는 세부 절 링크만 둔다. H2 주제 키워드는 별도 wrapper page나 링크가 아니며 같은 화면에 더 깊은 후손을 펼치지 않는다. 원문에서 하위 항이 없는 Summary 같은 terminal section도 독립 leaf 링크 하나로 두고 설명·예제·실습은 그 leaf가 소유한다. book·chapter·appendix Map의 authored body는 비우며, 기존 원문 설명·예제·그림은 삭제하지 않고 가장 가까운 leaf로 provenance와 함께 이동한다. 정본 계층은 보통 `책 → 장 → 세부 학습 페이지`의 2~4단계로 제한하고, 탐색만 위한 빈 절 wrapper를 만들지 않는다. 더 깊은 원문 heading은 독립 탐색 단위가 꼭 필요하지 않다면 가까운 leaf 본문과 coverage locator에 보존한다. 정보량과 재탐색 필요가 명확한 경우에만 4단계보다 깊은 예외를 허용한다. 원문서가 주어지면 같은 판본의 공식 한국어판 목차를 먼저 찾고, 없을 때만 번호와 계층을 유지해 자연스럽게 번역한다. `2주·1달·5달`, `학습 자료`, `체크포인트`, `다시 열었을 때`를 별도 탐색 노드로 만들지 않는다.

하위 항을 가진 번호 section은 독립 wrapper page가 아니라 상위 Map의 H2 group이다. group 번호·제목과 같은 child, 또는 다시 descendant를 소유하는 section child를 두지 않는다. legacy wrapper의 reader prose는 첫 terminal leaf로 locator와 함께 이동하고 exact relocated span hash를 coverage manifest에 기록한 뒤 wrapper를 퇴역한다.

책의 PDF·HTML·EPUB 원본은 `Wiki → 리소스 → 책 원본`의 private local-only archive가 소유한다. archive 파일명은 문서 내부에서 확인한 실제 책 제목과 판으로 정규화하고 원래 파일명·SHA-256·권리 상태를 catalog에서 역추적한다. embedded image는 원본 bytes와 hash를 그대로 보존하고, scan에서 잘라낸 image는 원본 page locator·crop box·render 조건을 provenance로 남긴다. source archive와 Wiki source record의 hash가 일치하지 않으면 편입하지 않는다. 원본 저장과 목차 생성은 학습 완료 증거가 아니다.

권리 상태가 `processing-prohibited`이면 공개 목차·서지 이상의 본문 처리를 fail closed한다. 다만 사용자가 구매·소유한 원본을 직접 제공하고 이 private Vault 안에서의 처리를 명시적으로 승인했다면 `user-purchased-copy` ownership basis, byte-pinned archive, 권리 고지와 승인 receipt의 locator·SHA-256·승인일, `source-landed-private-local-only` scope를 근거로 `user-authorized-private` 상태를 사용할 수 있다. 이 상태는 local-only 책 정본의 전권 source-landed 편입과 한국어 원서의 no-op translation만 허용하며, 공개·재배포·외부 전송·모델 훈련에는 사용할 수 없다. demotion 뒤 복구는 blocked intake와 격리 manifest·entry bytes를 다시 대조하는 전용 원자 restore를 거쳐야 하고, 실패 시 intake·coverage·compiler output·asset·index를 모두 복구하되 구매 원본과 격리본은 그대로 보존한다.

#### Book four-phase workflow

책은 다음 네 phase를 한 canonical tree에서 단방향으로 진행한다. 번역본이나 개념 연결본을 별도 canonical로 만들지 않으며, 이미 검증한 source structure·element·provenance·coverage를 뒤 phase가 삭제·축약·재배정하지 않는다.

1. `source-landed`: 실제 제목으로 원본과 source image를 local-only archive에 고정한다. Map은 한국어 keyword와 direct child link bullet만 소유하고, leaf는 원문 언어·순서의 reader body와 모든 원문 code를 verbatim으로 exact-once 보존한다. 원문 그대로 독립 실행 가능한 code만 `run-*`으로 검증하고, fragment·dependency·intentional-error·placeholder는 source locator·hash와 static body hash를 고정한 static-only로 둔다. synthetic wrapper·대체 code는 만들지 않는다. node는 `reader_language`와 `source_prose_verified: true`를 기록한다. 이 phase에는 `korean_prose_reviewed`를 요구하지 않는다.
2. `translated`: 같은 leaf를 누락 없는 자연스러운 한국어로 갱신한다. `translation_required: true`이면 `reader_language: ko`와 `korean_prose_reviewed: true`를 모두 요구한다. 한국어 원서는 `translation_required: false`이며 source prose 검토 결과를 유지한 채 translation은 no-op로 기록한다. 새 한국어 canonical을 만들지 않는다.
3. `concept-linked`: 책 전체의 source 편입과 필요한 번역이 끝난 뒤 현재 book content hash를 기준으로 개념 canonical과 relation만 증분 연결한다. 이 phase는 reader body를 다시 생성하지 않으며 관계 대상·판단 근거·book content hash를 evidence로 남긴다.
4. `understanding-enriched`: 이후 대화에서 실제로 확인된 질문·오개념·실험을 source claim과 구분해 같은 leaf에 증분 보강한다. `source_session_ids`, source coverage hash, translation coverage hash를 evidence로 남기며 두 coverage를 줄이지 않는다. 계속 성장하는 phase이므로 그 자체는 전권 global completion blocker가 아니다.

promotion payload의 `workflow_phase`와 `translation_required`는 coverage manifest와 일치해야 한다. phase rollback, `translation_required` 변경, 이전 phase evidence 변경, source element 소유권 변경, 번역 뒤 delivery 감소를 fail closed한다. 과거 저장된 v6/schema 2 scope는 감사할 수 있지만 새 v7 승격 입력으로 재사용하지 않는다.

출판사 웹 목차가 생략했더라도 해당 판본의 PDF outline 또는 본문 heading에서 직접 확인되는 비번호 Summary·연습문제·해답·참고문헌은 원문 순서의 비번호 자식으로 유지한다. 다른 장과 형식을 맞추기 위해 원문에 없는 Summary를 만들거나, 확인된 비번호 section을 장 root의 임의 요약으로 흡수하지 않는다. source coverage manifest에는 공개 목차와 본문 구조의 차이를 함께 기록한다.

source structure inventory는 본문 장·절뿐 아니라 저자 서문·저자 소개·역자 서문, 부록, 참고문헌, 찾아보기를 원문 순서대로 포함한다. 판권은 source metadata로 분류할 수 있고 참고문헌·찾아보기는 canonical leaf 또는 locator가 고정된 metadata-only로 분류할 수 있지만, 의미 있는 front/back matter와 부록은 canonical leaf가 소유한다. 부록 code도 일반 본문과 같은 source element와 runnable gate를 통과한다.

가장 구체적인 절 문서는 `source-landed`에서 원문의 핵심 정보와 논리 순서를 원문 언어로 빠뜨리지 않고 보존하고, `translated`에서 같은 내용을 자연스러운 한국어로 전달해야 한다. 원문 그대로 독립 실행 가능한 code만 같은 source를 실행하는 `run-*` block으로 표현하고 compile·run·output을 검증한다. fragment, 외부 dependency, 의도적 compile error, placeholder처럼 원문을 바꾸지 않고는 독립 실행할 수 없는 code는 원문 static fence로 보존한다. 이때 `runnable_required: false`, 제한된 이유 code, 정확한 source locator·hash, static body hash와 고정 evidence를 source coverage manifest에 기록한다. 실행을 위해 원문 밖 synthetic harness·대체 구현·설명 문장을 leaf에 만들지 않는다. 원문에 없는 인출·전이 문제를 생성하지 않는다. 원문 밖 예측 질문·변형 지시·Reset 안내·완료 기준·검증 상태 문장과 `직접 확인하기`, `자료를 닫고 답하기`, `이전과 다음`, `완료 기준`, `검증 상태` section을 1·2차에 생성하지 않는다. 선형 이동은 Map과 `prerequisites`·`next_concepts` metadata가 소유한다.

책마다 산출물 밖의 source coverage manifest를 둔다. manifest에는 판본·ISBN·원문 hash·한국어 목차 근거와 전체 TOC leaf, leaf별 source locator를 기록한다. 원문의 문단·표·문제·그림·code block을 의미 단위로 검토해 `claim`, `example`, `caution`, `figure`, `code` element를 만들고, 각 element에 정확한 locator와 원문 span 또는 image bytes의 hash를 둔다. OCR line이나 익명 ordinal을 claim으로 세지 않으며 장별 총개수만 적는 count-only coverage도 허용하지 않는다. 모든 element는 정확히 하나의 leaf에 배정하고, non-code는 실제 독자 본문의 unique exact span과 span hash를, figure는 Mermaid·local image·prose 중 실제 delivery와 hash를 검증한다. figure의 prose delivery는 제목이나 caption 한 줄을 되풀이하지 않고, 독자가 그림 없이도 입력·변환·출력, 방향, 비교 또는 원인·결과를 재구성할 수 있는 실제 관계를 설명한다. 같은 leaf·종류·delivery span을 여러 source element가 공유해 수를 부풀리지 않는다. node별 다섯 종류의 expected·covered 값은 assignment에서 파생한 수와 모두 일치해야 한다. runnable로 바꿀 수 있는 예제 수, 실제 변환·검증 수, static으로 남긴 예제와 예외 이유도 기록한다. 문장 수나 링크 수는 완전성 근거가 아니다. 모든 예상 leaf가 존재하고 각 leaf가 `source-covered` 이상이며, 실행 코드가 있는 leaf는 실제 compile·run·output 대조를 통과해야 책 본문 완료로 판정한다.

외부 폴더에 여러 책·강의·표준·논문이 함께 들어오면 file count를 book count로 해석하지 않는다. source catalog의 모든 파일을 상위 자료 bundle 하나에만 배정하는 book intake manifest를 먼저 만들고 `book-intake-audit`으로 누락·중복 배정·권리 미확인 자료의 본문 승격을 차단한다. 정리 순서는 사용자가 지정한 언어·우선순위를 따르되, `structure-verified`와 `content-in-progress`를 `complete`로 보고하지 않는다.

문서는 세 층의 provenance를 한 leaf에서 구분한다. **source층**은 책의 원문 언어·논리·주장·예제·주의와 immutable coverage를 보존한다. **translation층**은 그 의미와 순서를 바꾸지 않는 자연스러운 한국어 delivery다. **학습자 보강층**은 사용자가 실제로 헷갈린 지점, 반례, 실행 trace를 source-derived claim과 구분해 추가한다. 보강에는 대화 provenance와 시점을 남기고, 일반화 가능한 개념은 개념 Wiki에 병합한 뒤 책 leaf에서 연결한다. 같은 설명을 양쪽에 복제하지 않으며 어느 후속 층도 앞선 층의 coverage를 줄이지 않는다.

책과 개념은 서로 다른 질문에 답한다. 책 leaf는 특정 판본의 설명 순서·예제·주의를 보존하고, 개념 문서는 책 밖의 질문·추가 근거·현재 버전·실험으로 독립 성장한다. 둘은 parent를 공유하거나 서로를 child로 소유하지 않고 relation과 wikilink로만 연결한다. 판본의 설명과 현재 개념이 다르면 두 상태와 적용 시점을 모두 남기며, 최신 개념으로 책을 고쳐 쓰거나 오래된 책 설명으로 개념을 되돌리지 않는다.

독자가 읽는 Wiki 본문에는 AI·compiler·agent가 지켜야 할 운영 문구를 쓰지 않는다. `이 절이 내용을 소유한다`, `위에서 아래로 연다`, `Run을 눌렀다고 완료가 아니다`, `coverage를 갱신한다`, `정본 writer를 사용한다` 같은 문장은 skill·manifest·receipt·학습 프로젝트의 책임이다. 책 root와 모든 장·절 Map은 authored prose 없이 실제 direct child 링크만 보여 준다. 장 도입·설명·예제·실행 결과는 원문 순서상 가장 가까운 첫 leaf가 소유한다. 판본·페이지·공식 문서 같은 provenance는 독자가 출처를 판단하는 데 필요한 최소 `판본과 근거`로 leaf 하단에 두고 작성 절차를 설명하지 않는다.

compiler가 검증한 일반 교과 개념의 출처는 `source → claim → page → receipt`가 소유한다. 같은 출처를 본문 문장마다 반복하지 않으며, inline citation이 없다는 이유만으로 근거 경계 실패로 판정하지 않는다. 본문은 일반 설명·구현 예시·특정 버전의 실제 실행·측정 결과를 서로 혼동하지 않아야 한다. `> 확인 범위:`가 있으면 그 문장을 적용 경계의 우선 근거로 사용하고, 본문이 그 경계를 직접 모순할 때만 실패로 판정한다.

품질 검토의 실패는 선택한 현재 Markdown anchor가 결함을 직접 입증할 때만 유효하다. 자연스러운 완전한 문장을 막연히 부족하다고 평가하거나, 일반 교과 설명을 inline citation 부재만으로 탈락시키는 판정은 오탐이다. 명확한 결함을 현재 문장에서 입증하지 못하면 통과시킨다.

## Gate scope

- 문서마다 같은 heading, 문장 수, code block 수, diagram 수를 강제하지 않는다.
- 어떤 작성 경로를 골랐더라도 독자가 관찰한 장면, 이유, 기술적 근거, 적용 경계 사이의 연결을 따라갈 수 있어야 한다.
- 짧은 참고 문서는 필요한 단계만 사용한다. 분량을 채우기 위해 역사, 일반론, 비유를 추가하지 않는다.
- `node_kind: root|hub|entity`인 탐색 페이지는 설명 장이 아니라 키워드 hyperlink surface다. H1과 직접 하위 키워드 링크만으로 판정하며, 본문 prose·근거 section·요약을 추가하라고 요구하지 않는다. 정보·판단·이력 품질은 링크된 detail·information·history 문서에서 검사한다.
- Novel 원자료는 `private/novel/**/source-*`, `event-*`, `judgment-*`, `people/*` 같은 중간 wrapper로 한 번 더 감싸지 않는다. 주제 hub의 2단 불릿 source index에서 내부 원본과 정본 인물로 바로 연결하고, 원본 수·hash·사건 section·판단 section·관계 수는 projection manifest가 대조한다. 링크 정확성·privacy·단일 소유권·manifest 완전성을 검사하되 원문을 projection에 복제하거나 설명 분량을 늘리지 않는다.

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
- output fence에는 `text` 또는 `console` language를 붙이고, 일반 학습 글은 실제 실행 결과와 예상 결과를 구분한다. 다만 책의 `source-landed`·`translated` leaf는 원문에 없는 `검증 상태` 라벨을 본문에 만들지 않고 실행 여부·output hash를 source coverage manifest와 receipt에만 기록한다. stdout과 stderr를 나누면 일반 학습 글에서는 각 channel 이름을 명시한다.
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
- 책이면 source coverage manifest의 예상 TOC leaf가 100% 대응되고, 원문의 claim·example·caution·figure·code semantic element가 stable locator·source hash·unique reader delivery로 exact-once 배정되며, assignment에서 파생한 all-kind count가 일치하고 학습자 보강이 원문 coverage를 줄이지 않는다.
- 책의 `source-landed` phase이면 실제 제목의 local-only archive와 source image inventory가 hash로 대조되고 모든 direct-content node의 `source_prose_verified`가 true다. 번역이 필요한 `translated` 이상이면 같은 leaf의 `reader_language`가 `ko`이고 `korean_prose_reviewed`가 true이며, phase rollback이나 immutable source·translation coverage 감소가 없다.
- 책 leaf와 개념 문서가 같은 설명을 중복 소유하지 않고, 판본 차이·현재 버전·사용자 보강의 provenance가 구분되며 관계 링크가 실제 canonical ID를 가리킨다.
- reader-facing 본문에 AI·compiler·agent 운영 지시나 문서 소유권 설명이 없고, provenance가 학습 내용을 밀어내지 않는다.
- Mermaid가 있으면 default·dark theme에서 실제 render되며 source와 생성물의 identifier가 일치한다.
- Obsidian 정본이면 `repo://skills/standards/obsidian-compatibility.md`의 envelope·link·visibility gate를 함께 통과한다.
- 원문 code가 fragment·dependency·intentional-error·placeholder 사유로 static fence에 남는 경우 원문 locator·source hash·static body hash와 고정 evidence를 검증한다. 같은 leaf에 synthetic `run-*` harness나 toy replacement를 자동 생성하지 않는다.
- 서로 다른 원문 code/example element가 같은 `run-*` block이나 같은 static fence delivery를 공유하면 coverage가 아니다. 각 원문 element는 고유한 reader delivery와 source locator·hash를 가져야 한다.
- 원문 그대로 독립 실행 가능한 code만 `run-*` block으로 검증한다. fragment·dependency·intentional-error·placeholder는 pinned static-only로 보존하며, 원문 listing을 synthetic wrapper·toy harness·출력 상수·임의 대체 code로 바꾸면 coverage가 아니다.
