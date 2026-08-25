---
name: ingest
description: 외부 폴더·Git 저장소·drop 문서 전체를 woon-knowledge에 파일별로 대조·중복 병합·변경 반영하고 완전성 catalog와 품질 검증까지 남길 때 사용한다.
---

# Ingest

입력 원천은 대조 중 읽기 전용으로 유지한다. 먼저 전체 활성 파일을 `source_id`, 상대 경로, content hash, 역할, privacy로 catalog화하고 `동일·metadata-only·병합·신규·이동·제외`로 분류한다. 수집이 승인된 원자료는 복사본을 남기지 않고 `woon-knowledge/wiki/private/_sources/knowledge/**` 또는 `woon-knowledge/wiki/private/_sources/novel/**`로 이동해 Wiki vault 하나가 소유한다. `.git`, editor 상태, cache, backup, secret은 본문 처리 대상에서 제외하되 제외 사유와 개수를 남긴다. 머신별 절대 경로와 원문 secret은 commit하지 않는다.

한 번에 문서 한 편만 처리한다. 그 문서의 기존 정본과 read-only corpus 후보를 `$knowledge`로 찾고, 같은 질문에 답하면 기존 문서에 병합한다. 같은 `source_id`의 내용 변경은 같은 정본 revision을 갱신하고, 내용이 같은 이동·별칭은 새 문서를 만들지 않는다. 서로 다른 사실은 조건과 시점을 분리하고 확인되지 않은 충돌은 `확인 필요`로 남긴다. `inbox/capture`는 임시 대기열, `inbox/daily`는 결과 projection이므로 두 README나 일일 자유 메모를 자동 source로 스캔하지 않는다. 일일 메모를 지식화하려면 사용자가 선택한 본문을 새 source range로 명시해야 한다. 대규모 일괄 복사, 경로만으로 덮어쓰기, private 원문의 기술 Wiki 혼입은 금지한다.

각 파일은 후보 생성 뒤 원천 보존, 중복 제거, 제목·목차·선형 설명, 코드·Mermaid 정합성, Obsidian link, privacy, target revision을 검사한다. PDF·웹·문서가 image를 참조하면 본문보다 먼저 asset inventory를 만들고 누락 여부를 검사한다. 실제 UI·측정 chart·강의 도판처럼 원본성이 설명의 일부이면 [source asset 계약](references/source-assets.md)을 읽고 hash 단일 원본으로 보존한다. 실패하면 같은 파일만 수정·재검사하고 통과한 뒤 다음 파일로 이동한다. LLM Wiki v2에서는 source evidence, accepted claim, page spec을 갱신하고 `$compile-knowledge`로 compile·receipt audit을 실행한다. `source-reconcile` 또는 `wiki/` 직접 쓰기로 우회하지 않는다. 상세 판정과 완료 조건은 [reconciliation](references/reconciliation.md)을 필요할 때만 읽는다.

이동형 영상·음성 자료는 기본적으로 Vault에 보관하지 않는다. 시스템 설계에 참고했다면 지속되는 것은 검증 가능한 설계 결정뿐이며, 영상 URL·설명·라이브 채팅·자막·자동 전사본을 source·claim·검색 색인에 넣지 않는다. 영상 자체가 장기 증거여야 하는 예외는 사용자가 영구 보관 범위와 재검토 주기를 명시하고 별도 수집 설계를 요청했을 때만 검토한다.

독자가 다시 읽을 Wiki 본문이나 page spec을 만들 때는 아래 명령으로 quality gate, 범용 writing harness, 표본 근거를 함께 읽는다. 자료의 성격에 맞는 route를 고르고, 원본의 사실·현재 해석·미결정·visibility·purpose·재열람 질문을 분리한다. 코드가 없는 조사·사건·결정·절차도 같은 계약을 따르며, source에 없는 의도·결론·실행 결과를 보완하지 않는다.

```bash
bash "$(woon resolve repo://skills/skills/writing/tech/scripts/learning-context.sh)"
```

완료는 catalog의 모든 활성 파일이 `merged`, `canonical`, `catalog-only`, `excluded` 중 하나이고 pending, 외부 보관 경로, 중복 source ownership이 0일 때만 선언한다. source figure가 있었다면 누락, 중복 bytes, 깨진 embed, orphan catalog, rights·access 위반도 모두 0이어야 한다. 마지막에 source 경계 receipt, `woon_knowledge_compile_audit`, `woon_knowledge_audit`, source catalog drift, Obsidian link·Mermaid·asset, 검색 표본, Git diff를 반복 검증한다. 자동 commit·push·publish는 하지 않는다.
