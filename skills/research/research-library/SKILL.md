---
name: research-library
description: Zotero로 논문·서지를 수집하고 NotebookLM Markdown 산출물을 Woon 정본 후보로 검증할 때 사용한다. 논문 PDF, CSL JSON, DOI·arXiv ID, NotebookLM 보고서·학습 가이드·flashcard export, Obsidian 문헌 노트를 다룰 때 적용한다.
---

# Research Library

Zotero는 논문과 서지의 선택·보관자이고, NotebookLM은 선별한 자료로 질문하고 학습물을 만드는 작업대다. 어느 쪽도 Woon의 source·claim·page·receipt 정본을 직접 바꾸지 않는다.

설치가 필요한 경우 현재 활성 profile과 `woon skills plan`을 확인한다. `personal`처럼 이 skill을 포함한 기존 profile을 유지하고, 단일 작업 때문에 `research-library` profile로 바꿔 다른 활성 skill을 퇴역시키지 않는다. 설치 상태와 무관하게 catalog의 정본을 직접 읽어 작업할 수 있다.

1. Zotero에는 사용자가 선택한 collection만 넣고, PDF와 개인 라이브러리 DB는 Vault 밖에 둔다. Zotero export는 CSL JSON으로 만들어 `.local/` 또는 별도 local-only 작업 폴더에 둔다.
2. NotebookLM에는 purpose가 있는 작은 source bundle만 넣는다. `nlm auth`, `source add`, `source sync`, delete, share는 Google 계정·파일 전송·외부 상태를 바꾸므로 사용자가 그 작업을 명시적으로 요청한 경우에만 실행한다. 전체 Vault, Novel, 대화 원문, 영상 URL을 `source sync`에 넘기지 않는다.
3. 사용자가 선택한 artifact의 다운로드를 요청했고 승인된 인증 상태가 있으면 아래 명령으로 Markdown과 manifest를 만든다. 새 `nlm auth`나 browser credential 접근이 실제로 필요할 때만 해당 인증 작업의 권한을 확인한다. `--source-ref`에는 선택한 Zotero collection에 실제로 있는 DOI·arXiv ID만 쓴다. 명령은 artifact 하나를 다운로드할 뿐 source upload, notebook 수정, Wiki 저장을 하지 않는다.

```bash
woon knowledge notebooklm-export \
  --artifact-id "<artifact-id>" \
  --kind "report" \
  --source-ref "doi:<identifier>" \
  --tool-revision "<pinned-nlm-commit>" \
  --output ./.local/research/report.md \
  --manifest ./.local/research/notebooklm-export.json \
  --nlm "$(command -v nlm)"
```

4. 다음 명령으로 외부 도구를 다시 호출하지 않는 intake plan을 먼저 만든다. `metadata-ready`는 서지 metadata만 확인된 상태이고, `derived-review-required`는 NotebookLM이 만든 파생물이라 claim 검토 전에는 검색·정본에 넣을 수 없다는 뜻이다.

```bash
woon knowledge research-intake-plan \
  --purpose "이 자료를 다시 찾아 어떤 학습·결정·설명에 쓸지" \
  --zotero ./library.json \
  --notebooklm-manifest ./notebooklm-export.json \
  --output ./research-intake-plan.json
```

5. intake plan 통과는 정본 저장 권한이나 claim 검증을 뜻하지 않는다. 사용자가 저장까지 요청했다면 실제 원문·라이선스·인용 범위를 확인한 뒤 `$archive` 또는 `$compile-knowledge`로 반영하고, 해당 skill이 소유한 범위의 compiler·검색·인용 검증을 적용한다. 다운로드만 요청했다면 로컬 export에서 마친다.

Zotero/NotebookLM의 설치·output·privacy·Obsidian 연결 기준은 [export contract](references/notebooklm-zotero-contract.md)를 읽는다.
