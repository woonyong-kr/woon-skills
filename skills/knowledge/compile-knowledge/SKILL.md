---
name: compile-knowledge
description: private woon-knowledge의 LLM Wiki source·claim·page spec·receipt를 추가·수정·감사·컴파일할 때 사용한다. catalog/llm-wiki 변경이나 receipt 불일치·stale 검색 복구에 사용한다.
---

# Compile Knowledge

`wiki/`는 Woon의 단일 지식 정본이며 모든 페이지가 `woon-knowledge/docs/wiki-information-architecture.md`의 `canonical_id`·`node_kind`·`parent`·`keywords`·`view_mode` 계약을 따른다. 그중 `catalog/llm-wiki/pages.yaml`이 소유한 근거 본문만 compiler 산출물이며 source, accepted claim, page spec으로 갱신하고 Markdown 출력·receipt를 직접 고치지 않는다. 대화·프로젝트 문서는 같은 Wiki 안에 있지만 conversation-to-Wiki 경로가 관리하므로 compiler page로 복제하거나 덮어쓰지 않는다. Core가 생성하는 `woon-wiki-overview`, `woon-wiki-children`, `woon-wiki-latest`, `woon-wiki-timeline` block은 같은 파일의 파생 view이며 compiler projection과 receipt 입력에서 제외한다.

1. 먼저 `$knowledge`로 기존 canonical 문서와 관계 ID를 확인한다. 대화 한 건을 정본에 저장하는 일은 `$archive`, 외부 corpus 전수 수집은 `$ingest`에 넘긴다.
2. source body 또는 claim Markdown을 새로 쓰거나 고쳐 독자가 읽을 설명을 바꿀 때는 먼저 아래 명령으로 `$tech`의 learning harness를 읽는다. hash·receipt·관계만 고치는 변경에는 이 단계를 적용하지 않는다.

```bash
bash "$(woon resolve repo://skills/skills/writing/tech/scripts/learning-context.sh)"
```

3. 변경할 `catalog/llm-wiki/sources.yaml`, `claims.yaml`, `pages.yaml`을 읽고 [compiler contract](references/compiler-contract.md)의 필수 필드와 privacy 규칙을 적용한다. 원본은 덮어쓰지 않으며 locator에 머신 절대 경로·secret·private 원문을 넣지 않는다.

책 원문을 Wiki에 편입할 때는 본문을 쓰기 전에 판본이 일치하는 목차를 먼저 고정한다.

책 편입은 [책 4단계 품질 계약](../../../standards/learning-content-quality.md#book-four-phase-workflow)을 따르는 단방향 상태 전이다. 네 단계는 별도 번역본·개념판·학습판 페이지를 만드는 절차가 아니라 같은 canonical leaf를 증분 갱신하는 절차다. 미래 promotion payload는 `workflow_phase`, `translation_required`와 node별 `reader_language`, `source_prose_verified`를 명시하며, 이전 phase나 이미 검증한 source structure·element·delivery를 되돌리거나 줄이지 않는다.

- 원서의 판권·ISBN·판·전체 장·절 번호를 원문 PDF 또는 출판사 페이지에서 확인한다.
- 같은 판본의 공식 한국어판이 있으면 출판사나 서점의 전체 목차를 찾아 장·절 번호와 번역 용어를 대조한다. 검색 결과 제목만 보고 한국어판이 있다고 가정하지 않는다.
- 한국어판 목차가 없을 때만 번호와 계층을 유지한 채 자연스러운 한국어로 번역한다. 번역 때문에 절을 병합·분할·재번호화하지 않는다.
- 책 Map은 `# 책 제목 → ## 부·부록 → 장·부록 링크 불릿`, 장 Map은 `# N장 제목 → ## 의미 있는 절·주제 키워드 → 세부 학습 페이지 링크 불릿`으로 통일한다. `부`, `장`, `절`, `항`, `부록`, `요약`을 표준 한국어 구조 용어로 사용하고 영문 `Part`, `Chapter`, `Section`, `Subsection`, `Appendix`, `Summary`는 source metadata·alias·필요한 최초 병기에만 남긴다. H2는 탐색용 wrapper page나 `N장` 같은 제목 반복이 아니며, 같은 H2 아래의 링크는 모두 해당 Map의 direct child다. 하위 항이 없는 절·요약도 독립 leaf 링크 하나로 두고 원문 설명·예제·그림·실습은 그 leaf가 소유한다. book·chapter·appendix Map의 authored body에는 설명 문장·코드·그림·운영 안내를 두지 않는다. 기존 Map에 source-derived 본문이 있으면 삭제하지 말고 가장 가까운 leaf로 source locator와 함께 이동한 뒤 Map을 비운다. `학습 자료`, `체크포인트`, `다시 열었을 때` 같은 학습 활동은 별도 navigation child로 만들지 않는다.
- 번호가 붙은 source section에 실제 하위 항이 있으면 section 자체를 wrapper page로 만들지 않고 상위 Map의 H2 group으로 둔다. direct child는 그 H2의 terminal leaf여야 한다. 과거 wrapper에 원문 prose가 있으면 첫 terminal leaf로 locator와 함께 이동하고 `retired_source_section_wrappers`에 wrapper·map·group·first leaf·exact relocated span hash를 기록한다. group과 같은 번호·제목의 child나 descendant를 다시 소유하는 section wrapper가 남으면 promotion을 중단한다.
- 표지 뒤의 저자 서문·저자 소개·역자 서문과 본문 뒤의 부록·참고문헌·찾아보기도 source structure inventory에 원문 순서대로 넣는다. 의미 있는 서문·소개·역자 서문·부록은 canonical leaf로 보존하고, 판권은 source metadata로 분류한다. 참고문헌·찾아보기는 독립 leaf 또는 locator가 고정된 `metadata-only` 중 실제 탐색 방식에 맞게 하나를 택한다. 어느 쪽도 inventory에서 생략하지 않으며 부록의 code는 일반 본문과 같은 runnable contract를 적용한다.
- 목차 근거 URL·확인일·판본 경계를 source 또는 page provenance에 남긴다. 원서와 한국어판의 판본이나 구조가 다르면 원서 구조를 정본으로 삼고 번역 용어만 참고했다고 명시한다.
- `source-landed`에서는 원문 언어와 순서를 보존한 독자 본문을 같은 leaf에 편입하고 `source_prose_verified: true`를 근거로 고정한다. 이 단계는 번역 품질을 판정하지 않으므로 `korean_prose_reviewed`를 요구하지 않는다. `translated`에서는 같은 leaf를 핵심 정보와 논리 순서를 빠뜨리지 않는 자연스러운 한국어로 갱신하고 `reader_language: ko`, `korean_prose_reviewed: true`를 요구한다. 한국어 원서는 `translation_required: false`로 두고 source 본문 검토를 통과하면 번역은 no-op이다.
- 원문의 모든 의미 단위를 `claim`, `example`, `caution`, `figure`, `code` source element로 분해한다. 한 element는 원문 문단·표·문제·그림·code block처럼 독립 의미를 보존하는 최소 단위이며 OCR line, 임의 ordinal, 장별 총개수는 element가 아니다. 각 element는 종류·semantic unit·정확한 source locator·원문 span 또는 image bytes의 SHA-256에서 계산한 stable ID를 갖고 정확히 하나의 leaf에 배정한다. non-code element는 독자 본문에 정확히 한 번 존재하는 delivery span과 그 SHA-256을 고정하며, 같은 leaf·종류·span을 여러 element가 재사용할 수 없다. figure는 Mermaid block·local image·prose span 중 실제 독자가 보는 표현의 hash를 검증한다. prose로 전달하는 figure는 `그림 N의 제목` 같은 짧은 label 반복이 아니라 입력·변환·출력, 방향, 비교 또는 원인·결과 중 그 그림이 답하는 실제 관계를 설명해야 한다. node별 claim·example·caution·figure·code 수는 assignment에서 파생되어야 하며 count-only coverage를 허용하지 않는다.
- `claim semantic unit 5`, `unnumbered source code segment` 같은 내부 inventory·ordinal 문장과 `한다이다`, `줄인다을` 같은 자동 결합 흔적은 독자 본문에 쓰지 않는다. delivery span은 자연스러운 한국어 문장 자체여야 하며, 내부 원문 대조 정보는 manifest와 provenance가 소유한다.
- 원문의 모든 code 예시는 위 semantic inventory에 exact-once 배정하고 verbatim으로 보존한다. 원문 그대로 독립 실행 가능한 예제만 해당 언어의 고유한 `run-*` block 하나로 만들고 source·compile·run·output을 receipt에서 검증한다. 서로 다른 원문 code/example element를 하나의 대표 실행 block에 공동 배정하지 않는다. fragment, 외부 dependency, 의도적 compile error, placeholder처럼 원문을 바꾸지 않고는 독립 실행할 수 없는 예제는 원문 static fence로 보존하고 manifest에 `runnable_required: false`, `fragment|dependency|intentional-error|placeholder` 이유 code, 정확한 source locator·hash, static body hash와 고정 evidence를 남긴다. 원문 listing을 설명 주석만 있는 fence, 출력 상수를 그대로 적은 block, synthetic wrapper·harness나 대체 code로 바꾸지 않는다. 원문 밖 실행 전 예측·변형 지시·Reset 안내·완료 기준·검증 상태 prose도 leaf body에 추가하지 않는다. 독립 실행 가능한 원문 code가 미검증이거나 static 예외의 source·body·evidence가 고정되지 않으면 그 범위를 `code-verified`·`reviewed` 또는 완료로 판정하지 않는다.
- 책마다 source coverage manifest를 유지한다. manifest는 판본·ISBN·원문 hash, 확인한 한국어 목차 근거, 예상 부·장·절·세부 절 ID와 source locator, semantic inventory extraction method·policy hash, 모든 source element와 exact reader delivery를 기록한다. 상태는 `toc-only`, `drafted`, `source-covered`, `code-verified`, `reviewed`만 사용하고, 예상 leaf가 없거나 locator·중요 항목 대조가 남으면 책을 완료로 판정하지 않는다. 빈 shell, 제목만 있는 페이지, count-only manifest, 원문 hash가 없는 element, 본문에 없는 delivery evidence는 coverage로 세지 않는다. promotion payload와 coverage manifest schema가 바뀌면 과거 payload를 변환해 재검토하며 버전 숫자나 hash만 바꿔 재사용하지 않는다.
- 외부 폴더에 여러 자료가 섞여 있으면 source catalog의 모든 file locator를 정확히 하나의 book·extract·course·standard·paper·tutorial bundle에 배정한 `catalog/book-intake/<source>.json`을 먼저 만들고 `woon knowledge book-intake-audit`을 통과한다. file count를 책 권수로 보고하지 않으며, 미배정·중복 배정·권리 미확인 상용 원문의 본문 승격을 허용하지 않는다.
- 원문 기반 설명과 학습 대화 보강을 서로 다른 provenance로 추적한다. 원문층은 새 대화 때문에 삭제·축약·대체하지 않는다. `understanding-enriched`에서만 대화에서 확인된 오개념·추가 질문·실행 결과를 해당 leaf의 보강 claim으로 병합하고 `source_session_ids`와 시점을 남긴다. 일일 대화 취합도 같은 identity·optimistic revision·중복 병합 계약을 따르며, 새 보강은 기존 source·translation coverage hash를 바꾸거나 감소시키면 실패한다. 이 단계는 계속 성장하는 상태이므로 전권 완료의 global blocker가 아니다.
- `source-landed`와 `translated` leaf authored body에는 원문에 없는 인출·전이 문제, 예측·변형·Reset 안내, `직접 확인하기`, `자료를 닫고 답하기`, `이전과 다음`, `완료 기준`, `검증 상태` section을 만들지 않는다. 선형 이동은 Map과 `prerequisites`·`next_concepts` metadata가 소유한다. `understanding-enriched`에서도 실제 대화·실행 근거를 기존 문맥에 자연스럽게 병합하고 위 workflow section을 템플릿처럼 반복 생성하지 않는다.
- 원문의 권리나 출처가 불명확하거나 AI 처리 금지가 명시돼 있으면 fail closed한다. 공개 출판사 목차로 구조만 검증할 수는 있지만, 본문을 추출·번역·claim으로 승격하지 않고 `toc-only` 또는 Review로 남긴다.
- 사용자가 구매·소유한 원본을 직접 제공하고 이 private Vault 안에서의 처리를 명시적으로 승인한 경우에만 별도 `user-authorized-private` 권리 상태를 사용할 수 있다. 이 상태는 byte-pinned `private/local-only` source archive에서 같은 범위의 `source-landed` 책 정본을 복구·편입하는 권한일 뿐이다. intake에는 `user-purchased-copy` ownership basis, source archive path·SHA-256, 권리 고지 locator·SHA-256, 사용자 승인 receipt locator·SHA-256·승인일과 `source-landed-private-local-only` scope를 고정한다. `external-transmission-prohibited`, `model-training-prohibited`, `publication-prohibited`, `redistribution-prohibited` 제한은 항상 함께 유지하며 공개·배포·외부 전송·모델 훈련을 승인한 것으로 확대 해석하지 않는다.
- `processing-prohibited`로 demotion된 책을 다시 편입할 때는 일반 `book-promote`로 우회하지 않고 `book-rights-restore`의 apply:false preflight와 단일 원자 적용을 사용한다. 현재 blocked intake hash와 격리 manifest·entry bytes, immutable archive hash, 승인 receipt를 모두 다시 대조한 뒤 intake를 `user-authorized-private`로 바꾸고 책 정본과 coverage를 함께 복구한다. 어느 단계든 실패하면 intake·compiler input/output·coverage·asset·index를 rollback하며, 격리본과 구매 원본은 삭제하거나 덮어쓰지 않는다.
- 책 leaf와 일반 개념 문서는 서로 다른 canonical identity다. 책 leaf는 “이 판본의 이 절이 무엇을 어떤 순서·예제로 설명하는가”를, 개념 문서는 “여러 근거와 현재 기술 기준에서 이 개념을 어떻게 이해하는가”를 소유한다. 책에 없는 질문·추가 자료·새 버전·실험은 개념 문서를 성장시키며 책 원문층에 소급 삽입하지 않는다. 책의 독해를 위해 필요한 보강만 책 leaf에 두고, 일반화된 설명은 개념 canonical에 한 번만 남긴 뒤 양쪽을 `related_to` 또는 본문 wikilink로 연결한다.
- 책 판본과 현재 개념 근거가 다르면 어느 한쪽을 덮어쓰지 않는다. 책에는 출간 판본의 설명과 현재 차이를, 개념에는 현재 근거와 적용 버전을 남기고 서로 연결한다. 같은 문단·예제·결론을 양쪽에 복제하거나 같은 parent tree로 합치지 않는다.
- 책 본문 편입과 개념 Wiki 확장은 서로 다른 phase다. `source-landed`와 필요한 `translated`가 책 전체에서 끝난 뒤에만 `concept-linked`를 실행한다. 새로 생긴 leaf body를 재생성하지 않고 현재 book content hash를 기준으로 기존 개념과 관계만 증분 대조·연결한다. 관계 evidence에는 대상 canonical ID, 현재 책 본문 hash, 판단 근거를 남긴다.
- 책은 한 번에 한 장씩 처리한다. 최초 1회 고정한 판본·목차·source structure·source element inventory를 재사용하고, hash가 바뀌지 않은 leaf·번역·실행 receipt·quality review를 다시 생성하거나 다시 평가하지 않는다. `source-landed`의 각 장은 `목차 범위 고정 → 원문 언어·순서로 source element exact-once delivery → code exact-one runnable 검증 → apply:false preflight → merge-scope 원자 적용 → scoped audit`로 끝낸다. 번역이 필요하면 같은 장·leaf를 `translated` phase에서 한국어로 갱신하되 immutable source inventory와 provenance를 그대로 유지한다. 다른 장이 legacy·pending이면 전권 manifest를 교체하지 않고 `catalog/book-coverage-scopes/<book>/<chapter>.json` fragment를 사용하며, 검증된 장·phase만 완료로 보고한다.
- 여러 agent가 책을 병렬 생성하더라도 공용 Vault writer는 하나뿐이다. agent는 격리된 hash-pinned 산출물만 만들고, 현재 writer가 검증·적용 중인 동안 같은 책의 payload·catalog·generated Markdown을 다시 만들거나 덮어쓰지 않는다. 실패한 preflight나 rollback은 원인을 고친 같은 장만 재생성하며 전권 초안과 다른 완료 장을 재작업하지 않는다.
- AI·compiler·agent를 위한 작성 절차, page ownership, completion gate, navigation 설명은 reader-facing 책 본문에 넣지 않는다. 이런 계약은 skill·source coverage manifest·receipt·학습 프로젝트가 소유한다. 독자에게 필요한 판본·page locator·현재 공식 문서 근거만 leaf 하단의 짧은 provenance로 남긴다.
4. 새 source에는 원문 hash, 보존 본문, 그리고 "왜 보존하는가 / 어떤 미래 질문·결정·산출물에 쓸 것인가"를 한 문장으로 쓴 nonempty `purpose`를 둔다. legacy-wiki 이관본은 당시 목적을 추정해 덧쓰지 않는다. 대신 `curation.yaml`의 `current_use`에 지금 이 문서를 학습·설명·검색에 쓰는 이유를 적고, 그 근거(`basis`)와 확정 여부(`status`)를 남긴다. `current_use`는 현재 운영 판단이지 과거 source intent가 아니다. claim은 해당 source ID와 채택 근거, page spec은 한 output path와 현재 source/claim 집합을 가진다. 같은 conversation 문서를 갱신하면 기존 원문·claim을 지우거나 다시 렌더하지 말고 `archived/superseded`와 후속 ID로 이력을 남긴다. public page에는 public provenance만 연결한다. 미확인 주장·충돌은 `review-queue.yaml`에 남기고 accepted claim으로 만들지 않는다.
5. `woon_knowledge_compile`을 호출한다. 직접 Markdown 변경 또는 receipt 오류가 있으면 source/claim/page spec을 고친 뒤 다시 컴파일한다. `--force`는 compiler 변경 또는 receipt 전체 재생성이 필요한 경우에만 쓴다.

기존 compiler catalog에 `curation.yaml`이 아직 없으면, 첫 전환에서만 아래 명령으로 빈 historical purpose를 건드리지 않고 모든 page spec의 provisional current-use record를 만든다. 이 명령은 기존 curation을 덮어쓰지 않는다.

```bash
woon knowledge initialize-curation --vault <vault>
```

자동 문구의 생성 규칙을 고쳤거나 기존 페이지에 새 curated·archive source를 연결했을 때는 `legacy-page-metadata`와 `provisional`인 record만 아래 명령으로 갱신한다. 이 명령은 direct source가 전부 legacy인지 다시 확인해, `curated-wiki`가 있으면 `manual-review/confirmed`, legacy가 없는 새 source만 있으면 `archive-request/confirmed`로 바로잡는다. 이미 `manual-review` 또는 `confirmed`인 record는 이 명령이 바꾸지 않는다.

```bash
woon knowledge refresh-provisional-curation --vault <vault>
```

과거 archive 구현이나 중단된 작업 때문에 현재 page spec에 속하지 않는 conversation source·claim이 남았고, 같은 locator의 현재 successor가 하나로 확인되면 아래 명령으로 비파괴 이력으로 정규화한다. 서로 다른 locator이거나 successor가 여럿이면 자동으로 고르지 않고 audit 오류로 남긴다.

```bash
woon knowledge reconcile-superseded-revisions --vault <vault>
```
6. compile 뒤 Core의 Wiki view refresh를 실행하고 `woon_knowledge_compile_audit`과 `woon_knowledge_audit`을 모두 통과시킨다. receipt의 `compiler_projection_sha256`은 source·claim·page spec이 소유하는 compiler 본문을 검증하고, `output_sha256`은 해당 compile 시점의 전체 파일을 추적한다. Core 관리 block이 정상 갱신돼 전체 파일 hash가 달라져도 compiler projection이 재현되면 stale이 아니다. marker 밖의 compiler 본문 변경은 계속 오류다. source 변경 뒤 search가 stale이면 compile, Wiki view refresh, reindex 순서로 실행한다. compiler 입력·출력·tree view·index가 모두 current인지 확인한 뒤에만 완료를 말한다.
7. 독자가 읽는 학습 본문을 새로 쓰거나 고쳤다면, 현재 receipt `output_sha256`와 writing harness hash를 함께 담은 quality review payload를 갱신하고 아래 gate를 실행한다. 한 페이지라도 누락·보류·stale이면 compiler 정합성은 통과해도 문서 품질은 미검증으로 보고한다.

```bash
woon knowledge evaluate-quality \
  --vault <vault> \
  --reviews <content-quality-reviews.json> \
  --standard "$(woon resolve repo://skills/standards/learning-writing-harness.md)" \
  --prompt "$(woon resolve repo://skills/standards/learning-quality-review-prompt.md)"
```

650개처럼 전체 corpus를 검토할 때는 payload를 추정해 채우지 않는다. 먼저 `quality-review-plan`으로 현재 page·receipt·writing harness·review prompt가 묶인 immutable batch를 만들고, LLM 또는 사람이 각 batch의 `*.result.json`만 작성한다. `assemble-quality-reviews`가 plan과 현재 receipt를 다시 대조해 하나의 payload로 조립한 뒤에만 위 gate를 실행한다. plan 생성 뒤 문서나 표준이 바뀌면 이전 판정은 stale이며 새 plan부터 다시 시작한다.

```bash
woon knowledge quality-review-plan \
  --vault <vault> \
  --standard "$(woon resolve repo://skills/standards/learning-writing-harness.md)" \
  --prompt "$(woon resolve repo://skills/standards/learning-quality-review-prompt.md)" \
  --output <new-empty-plan-directory> \
  --batch-size 2 \
  --max-batch-chars 24000
```

로컬 Ollama가 있고 Vault를 외부에 보내지 않아도 되는 경우에는 아래 명령으로 아직 없는 batch 결과만 만든다. 기본 batch는 최대 2페이지이면서 Markdown 합계가 `24,000`자를 넘지 않으므로, 큰 페이지는 혼자 검토하고 작은 페이지들만 함께 검토한다. `--max-batch-chars`는 이 상한을 바꾸며, 한 페이지가 상한보다 큰 경우에는 그 페이지를 쪼개지 않고 단독 batch로 남긴다. `OLLAMA_HOST`가 loopback이 아니면 실행을 거부하며, 생성 온도는 0으로 고정한다. review는 기준마다 현재 문서의 서로 다른 anchor를 남긴다. model JSON이 page ID·receipt hash·rubric·근거 계약을 어기면 오류를 넣어 같은 batch를 최대 세 번 다시 요청하고, 끝내 맞지 않으면 결과 파일을 쓰지 않는다. `--max-attempts 1..5`로 한계를 바꿀 수 있다. 전체 corpus에서는 `--continue-on-error true`로 실패 batch의 ID와 오류를 report에 남기면서 다음 batch를 계속 검토한다. 기존 result는 덮어쓰지 않으므로 중단 뒤 같은 명령으로 재개할 수 있다. 결과는 quality evaluator receipt일 뿐 source·claim·page 정본이나 검색 색인이 아니므로, reviewer의 해석을 새 지식으로 편입하지 않는다.

```bash
woon knowledge review-quality-ollama \
  --plan <new-empty-plan-directory>/manifest.json \
  --results <quality-review-results-directory> \
  --model qwen3:4b-instruct \
  --batch quality-001
```

plan 생성 뒤 일부 페이지의 receipt만 바뀌었다면 이전 plan이나 result를 직접 고치거나 복사하지 않는다. 아래 명령은 새 immutable plan과 새 results directory를 만들고, writing harness·review prompt·Markdown hash가 모두 같은 **완전한 batch**만 검증해 재사용한다. 변경된 페이지가 있는 batch와 기존에 실패·누락된 batch는 새 results directory에 쓰지 않으므로, 같은 `review-quality-ollama` 명령이 그 batch만 다시 검토한다.

```bash
woon knowledge rebase-quality-review-plan \
  --vault <vault> \
  --prior-plan <old-plan-directory>/manifest.json \
  --prior-results <old-results-directory> \
  --standard "$(woon resolve repo://skills/standards/learning-writing-harness.md)" \
  --prompt "$(woon resolve repo://skills/standards/learning-quality-review-prompt.md)" \
  --output <new-plan-directory> \
  --results <new-results-directory> \
  --batch-size 2 \
  --max-batch-chars 24000
```

컴파일 실패 시 output 파일을 수동 복구하지 않는다. Git diff로 source catalog 변경을 검토하고 필요한 입력만 되돌린 후 재컴파일한다. 자동 commit, push, publish는 하지 않는다.
