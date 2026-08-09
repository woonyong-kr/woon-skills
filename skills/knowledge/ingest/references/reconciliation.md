# Source reconciliation contract

## 파일별 상태 전이

1. `discovered`: 상대 경로와 bytes를 읽고 SHA-256을 계산한다.
2. `matched`: 동일 `source_id`, 동일 content hash, 경로 후보, 제목·질문 후보를 순서대로 대조한다.
3. `planned`: `keep`, `merge`, `create`, `alias`, `catalog-only`, `external-private`, `exclude` 중 하나만 선택한다.
4. `validated`: 원천의 유효한 고유 정보가 보존되고 금지 결과가 없는지 검사한다.
5. `applied`: 읽어 둔 target revision과 source hash가 그대로일 때만 원자적으로 반영한다.
6. `verified`: catalog, canonical Markdown, index generation, Obsidian graph가 같은 결과를 가리킨다.

중단 뒤에는 `verified`부터 건너뛰고 첫 미완료 항목부터 재개한다. source hash나 target revision이 바뀌면 해당 항목을 `planned`로 되돌려 다시 병합한다.

## 식별과 중복

- 최초 `source_id`는 `source://<repo>/<percent-encoded-relative-path>`로 만들고 이후 catalog refresh에서 재사용한다. 절대 경로를 쓰지 않는다.
- 같은 경로의 content hash 변경은 update 후보이며 신규 문서 근거가 아니다.
- 다른 경로의 같은 content hash는 rename·alias 후보다. 이전 catalog의 identity를 재사용하고 정본을 복제하지 않는다.
- 같은 source를 두 canonical ID가 소유하면 hard failure다.
- 제목 유사성만으로 병합하지 않는다. 두 문서가 같은 질문·책임·독자에게 답하는지 확인한다.
- rename과 내용 변경이 동시에 일어나 identity를 확인할 수 없으면 자동 생성하지 않고 `확인 필요`로 둔다.

## 병합 판정

다음 순서로 한 파일만 비교한다.

1. target의 frontmatter, access, publish, canonical identity는 target이 소유한다.
2. source와 target의 제목, section, 코드 fence, Mermaid node, wikilink를 구조 단위로 대조한다.
3. source에만 있는 검증 가능한 설명·예제·경계 조건은 가장 가까운 target section에 삽입한다.
4. target에만 있는 최신 설명과 링크는 source에 없다는 이유로 삭제하지 않는다.
5. 서로 모순되면 조건·버전·시점을 확인한다. 확인하지 못하면 양쪽 주장을 사실로 합성하지 않는다.
6. 같은 설명의 표현 차이는 한 번만 남기고 용어와 identifier를 문서 전체에서 통일한다.

## 파일별 hard gate

- source hash와 적용 직전 hash 일치
- target revision과 적용 직전 revision 일치
- YAML frontmatter 1개, H1 1개, title 일치
- code fence와 Mermaid fence 닫힘
- 유효한 고유 source 정보의 누락 0
- 의미 중복 section 0
- private locator, secret, 개인 원문이 public 문서에 노출되지 않음
- 모든 wikilink가 활성 문서에 연결된다. `_quarantine`, backup, export는 연결 대상으로 인정하지 않음
- 후보 검토와 deterministic check가 모두 통과

하나라도 실패하면 그 파일은 적용하지 않는다. 전체 수치가 좋아도 개별 실패를 평균으로 상쇄하지 않는다.

## 전체 완료 조건

- 활성 source records + 명시적 exclusions = 전수 inventory
- pending, conflicting source ownership, duplicate canonical identity = 0
- source 재스캔 결과 drift = 0
- canonical audit, index generation, Obsidian link, Mermaid 검증 통과
- private 원문은 `external-private`로 catalog화하고 복제·공개하지 않음
- 변경 문서별 source hash, before/after revision, 판정, 검증 결과가 ledger에 존재
