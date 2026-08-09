---
name: ingest
description: 외부 폴더·Git 저장소·drop 문서 전체를 woon-knowledge에 파일별로 대조·중복 병합·변경 반영하고 완전성 catalog와 품질 검증까지 남길 때 사용한다.
---

# Ingest

원천은 읽기 전용으로 유지한다. 먼저 전체 활성 파일을 `source_id`, 상대 경로, content hash, 역할, privacy로 catalog화하고 `동일·metadata-only·병합·신규·이동·외부보호·제외`로 분류한다. `.git`, editor 상태, cache, backup, secret은 본문 처리 대상에서 제외하되 제외 사유와 개수를 남긴다. 머신별 절대 경로와 원문 secret은 commit하지 않는다.

한 번에 문서 한 편만 처리한다. 그 문서의 기존 정본과 read-only corpus 후보를 `$knowledge`로 찾고, 같은 질문에 답하면 기존 문서에 병합한다. 같은 `source_id`의 내용 변경은 같은 정본 revision을 갱신하고, 내용이 같은 이동·별칭은 새 문서를 만들지 않는다. 서로 다른 사실은 조건과 시점을 분리하고 확인되지 않은 충돌은 `확인 필요`로 남긴다. 대규모 일괄 복사, 경로만으로 덮어쓰기, private 원문의 기술 Wiki 혼입은 금지한다.

각 파일은 후보 생성 뒤 원천 보존, 중복 제거, 제목·목차·선형 설명, 코드·Mermaid 정합성, Obsidian link, privacy, target revision을 검사한다. 실패하면 같은 파일만 수정·재검사하고 통과한 뒤 다음 파일로 이동한다. 저장은 `$archive`의 optimistic revision과 원자적 index 계약을 사용한다. 상세 판정과 완료 조건은 [reconciliation](references/reconciliation.md)을 필요할 때만 읽는다.

완료는 catalog의 모든 활성 파일이 `merged`, `canonical`, `catalog-only`, `external-private`, `excluded` 중 하나이고 pending과 중복 source ownership이 0일 때만 선언한다. 마지막에 `woon_knowledge_audit`, source catalog drift, Obsidian link·Mermaid, 검색 표본, Git diff를 반복 검증한다. 자동 commit·push·publish는 하지 않는다.
