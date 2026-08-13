---
name: site-promotion
description: private Woon 정본을 블로그·포트폴리오 공개 후보로 변환하거나 portfolio 노출 항목을 직접 선택하며 claim·개인정보·승인을 관리할 때 사용한다.
---

# Site Promotion

`woon-knowledge`의 깊은 정본을 `woon-site`에 복사하지 않고, 검증된 claim ledger에서 목적별 public candidate를 만든다. 일반 기술 글, 이력서 문구, private 저장, UI 구현에는 각각 `$tech`, `$career`, `$archive`, `$react`를 쓴다.

1. `$knowledge`로 source를 검색·조회하고 `canonical_id`·revision·source type·현재 재검증 여부를 고정한다.
2. claim마다 사실, 수치 조건, 개인·팀·사후 확장 소유권, 공개 권리와 근거를 분리한다. 입력에 없는 ownership·rights는 각각 `unresolved`·`unknown`이며 요청 문장이나 인접 claim에서 가져오지 않는다. rights 때문에 본문을 보류해도 private 값만 제외한 claim ledger와 metric context는 생략하지 않는다.
3. destination이 blog이면 [블로그 계약](references/blog-contract.md), portfolio이면 [포트폴리오 계약](references/portfolio-contract.md)을 읽는다. 둘 다 요청되면 하나의 ledger에서 별도로 쓰고 문장을 재사용하지 않는다.
4. `Claim ledger` → `기술 블로그 후보` → `포트폴리오 후보` 순서로 candidate와 [승격 계약](references/promotion-contract.md)의 영수증을 대화에 제시한다. private 값은 제외 유형과 건수만 적고 원문을 다시 쓰지 않는다. 이 단계에서는 파일을 쓰지 않는다.
5. 사용자가 방금 본 candidate, destination과 포함 범위를 명시해 반영 승인한 뒤에만 `woon-site` public source를 쓴다. 승인 뒤에도 commit·push·deploy는 하지 않는다.
6. 대상 저장소의 schema·claims·images·build·rendered route를 검증하고 확인한 계층과 미검증 계층을 분리한다.

`좋아`, `진행해`, `써 줘`, 과거의 포괄 승인은 공개 권리나 반영 승인이 아니다. private 정본 수정, 공개 대상 자동 선택, unsupported claim 보강, 승인 범위 밖 파일 변경을 금지한다.
