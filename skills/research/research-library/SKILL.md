---
name: research-library
description: Zotero로 논문·서지를 수집하고 NotebookLM Markdown 산출물을 Woon 정본 후보로 검증할 때 사용한다. 논문 PDF, CSL JSON, DOI·arXiv ID, NotebookLM 보고서·학습 가이드·flashcard export, Obsidian 문헌 노트를 다룰 때 적용한다.
---

# Research Library

Zotero는 논문과 서지의 선택·보관자이고, NotebookLM은 선별한 자료로 질문하고 학습물을 만드는 작업대다. 어느 쪽도 Woon의 source·claim·page·receipt 정본을 직접 바꾸지 않는다.

Codex의 설치 target은 한 프로필을 동기화하는 방식이므로 `$research-library`를 설치하기 전에 반드시 `woon skills plan --profile research-library --target codex`를 확인한다. 현재 활성 지식 스킬을 자동으로 교체하지 않으며, 일반 Wiki 작업은 `knowledge` 프로필을 그대로 사용한다.

1. Zotero에는 사용자가 선택한 collection만 넣고, PDF와 개인 라이브러리 DB는 Vault 밖에 둔다. Zotero export는 CSL JSON으로 만들어 `.local/` 또는 별도 local-only 작업 폴더에 둔다.
2. NotebookLM에는 purpose가 있는 작은 source bundle만 넣는다. `nlm auth`, `source add`, `source sync`, delete, share는 Google 계정·파일 전송·외부 상태를 바꾸므로 사용자가 그 작업을 명시적으로 요청한 경우에만 실행한다. 전체 Vault, Novel, 대화 원문, 영상 URL을 `source sync`에 넘기지 않는다.
3. 사용자가 artifact 하나를 골랐고 `nlm auth`를 명시적으로 승인한 경우에만 아래 명령으로 Markdown과 manifest를 함께 만든다. `--source-ref`에는 선택한 Zotero collection에 실제로 있는 DOI·arXiv ID만 쓴다. 명령은 artifact 하나를 다운로드할 뿐 source upload, notebook 수정, Wiki 저장을 하지 않는다.

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

5. intake plan이 통과해도 자동 저장하지 않는다. 실제 원문·라이선스·인용 범위를 확인한 뒤 `$archive` 또는 `$compile-knowledge`로 source, accepted claim, page spec을 만들고 compiler audit·search reindex·answer citation evaluation을 실행한다.

Zotero/NotebookLM의 설치·output·privacy·Obsidian 연결 기준은 [export contract](references/notebooklm-zotero-contract.md)를 읽는다.
