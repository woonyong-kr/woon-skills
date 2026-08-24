---
name: compile-knowledge
description: private woon-knowledge의 LLM Wiki source·claim·page spec·receipt를 추가·수정·감사·컴파일할 때 사용한다. catalog/llm-wiki 변경이나 receipt 불일치·stale 검색 복구에 사용한다.
---

# Compile Knowledge

`wiki/`는 Woon의 단일 지식 정본이다. 그중 `catalog/llm-wiki/pages.yaml`이 소유한 근거 문서만 compiler 산출물이며 source, accepted claim, page spec으로 갱신하고 Markdown 출력·receipt를 직접 고치지 않는다. `wiki/personal/`의 대화·프로젝트 문서는 같은 Wiki 안에 있지만 Core conversation-to-Wiki 경로가 관리하므로 compiler page로 복제하거나 덮어쓰지 않는다.

1. 먼저 `$knowledge`로 기존 canonical 문서와 관계 ID를 확인한다. 대화 한 건을 정본에 저장하는 일은 `$archive`, 외부 corpus 전수 수집은 `$ingest`에 넘긴다.
2. source body 또는 claim Markdown을 새로 쓰거나 고쳐 독자가 읽을 설명을 바꿀 때는 먼저 아래 명령으로 `$tech`의 learning harness를 읽는다. hash·receipt·관계만 고치는 변경에는 이 단계를 적용하지 않는다.

```bash
bash "$(woon resolve repo://skills/skills/writing/tech/scripts/learning-context.sh)"
```

3. 변경할 `catalog/llm-wiki/sources.yaml`, `claims.yaml`, `pages.yaml`을 읽고 [compiler contract](references/compiler-contract.md)의 필수 필드와 privacy 규칙을 적용한다. 원본은 덮어쓰지 않으며 locator에 머신 절대 경로·secret·private 원문을 넣지 않는다.
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
6. `woon_knowledge_compile_audit`과 `woon_knowledge_audit`을 모두 통과시킨다. receipt의 `compiler_projection_sha256`은 source·claim·page spec이 소유하는 compiler 본문을 검증하고, `output_sha256`은 해당 compile 시점의 전체 파일을 추적한다. 대화 자동화가 관리 marker 안의 현재 이해·시간 이력을 정상 갱신해 전체 파일 hash가 달라져도 compiler projection이 재현되면 stale이 아니다. marker 밖의 compiler 본문 변경은 계속 오류다. source 변경 뒤 search가 stale이면 compile이 먼저이고 reindex는 그 다음이다. compiler 입력·출력·index가 모두 current인지 확인한 뒤에만 완료를 말한다.
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
