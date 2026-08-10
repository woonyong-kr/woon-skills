# Source asset 계약

## 먼저 inventory한다

본문을 병합하기 전에 source Markdown·PDF·웹·문서가 참조하거나 포함한 figure를 전수 열거한다. asset identity는 정확한 bytes의 SHA-256인 `asset://sha256/<hash>`다. 파일명이나 경로가 달라도 hash가 같으면 한 파일만 저장한다. perceptual hash는 유사 후보를 찾는 보조값일 뿐 동일성 판정에 쓰지 않는다.

각 record에는 다음을 둔다.

- `source_id`, source 내부 locator, MIME, byte SHA-256, pixel 크기
- source 문서와 본문 위치, caption·alt
- PDF면 문서 ID, page, figure 또는 영역, 추출 방식
- 웹이면 canonical URL, 확인 시각, 원문 MIME
- provenance, rights basis, access, publish scope
- target 문서와 canonical asset 경로
- `embedded`, `mermaid-preferred`, `link-only`, `external-private`, `placeholder`, `unreferenced` 중 하나의 판정과 이유

머신별 절대 경로는 commit하지 않는다. 출처가 local PDF라면 catalog의 stable source ID만 남기고 실제 경로는 Git-ignored local registry로 해석한다.

## 무엇을 본문에 보존하는가

다음을 모두 만족하면 source image를 본문 위치에 매핑한다.

1. UI screenshot, 물리 장치, 실제 측정 chart, 강의·PDF figure, 정확한 화면 배치처럼 Mermaid로 재구성하면 원본 증거가 손실된다.
2. 본문 pane에서 확대 없이 핵심 label을 식별하거나 원본 크기로 열 수 있다.
3. image의 주장·버전·identifier가 본문과 모순되지 않는다.
4. caption과 alt가 image가 답하는 질문을 설명한다.
5. 공개 문서라면 복제·공개할 권리 근거가 확인된다.

source image와 Mermaid가 서로 다른 질문에 답하면 둘 다 둘 수 있다. 이때 source image는 외형·원자료를, Mermaid는 코드 호출·상태 전이·인과관계를 담당한다. 같은 내용을 장식용으로 두 번 반복하지 않는다.

다음이면 `mermaid-preferred` 또는 `link-only`로 남긴다.

- 흐리거나 clipping·깨진 문자·잘못된 순서·오래된 기술 주장이 있다.
- code call, memory, sequence, state처럼 검증 가능한 의미 구조를 Mermaid가 더 정확히 보존한다.
- 본문의 기존 Mermaid와 같은 정보만 반복한다.
- 권리 근거가 없거나 공개 범위가 불분명하다.

AI-generated raster는 source evidence를 대신할 수 없다. source image가 부족하면 확인된 사실만 Mermaid로 보완한다.

## privacy와 권리

- `private/local-only` source asset은 공개 Wiki 경로로 복사하거나 public Markdown에서 참조하지 않는다.
- private figure의 hash·caption도 개인 정보가 될 수 있으므로 public catalog에 노출하지 않는다.
- 공개 권리가 불명확한 PDF·웹 figure는 원문 URL·page를 인용하고 local-only preview 또는 `link-only`로 둔다.
- crop, resize, format 변환본은 파생 asset이다. 원본 hash와 변환 recipe를 함께 기록한다.

## 적용과 검증

asset copy와 Markdown mapping은 읽어 둔 source hash와 target revision이 같을 때 한 변경 단위로 반영한다. 반영 후 다음을 검사한다.

- source figure omission 0
- 동일 SHA-256의 canonical file 1개
- broken embed와 orphan asset record 0
- catalog의 hash와 실제 bytes 일치
- public 문서에서 private/local-only asset 참조 0
- caption·alt·provenance·rights 판정 누락 0
- light/dark Obsidian과 공개 renderer에서 clipping·대비·확대 동작 확인

검사를 통과하지 못한 asset은 문서 완료로 계산하지 않는다.
