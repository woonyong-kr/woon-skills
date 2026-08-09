# Learning content fixture

`immutable-address.md`는 문제→실행 code·실제 output→원인→개념→개선→경계→연습→정리 순서를 검증하는 독립 Markdown 표본이다. 원본 강의 문장·코드·그림을 복제하지 않는다.

`verify.sh`는 Java source와 문서 code의 일치, 실제 output, 개념 도입 순서, Mermaid identifier·번호 flow를 검사하고 두 diagram을 default·dark theme로 render한다.

`score_artifact.py`는 held-out Markdown의 단일 Java block을 실제 compile·run하고 문서 output과 대조한다. 이어 source identifier, 개념 순서, Mermaid default·dark render, 경계·연습·정리를 18점 rubric과 hard-fail로 판정한다. agent별 token·duration은 실행기가 제공한 별도 결과에 기록하고 이 점수와 섞지 않는다.

`run_trial.py`는 Git에서 제외된 격리 경로에 Codex 또는 Claude 원시 결과·Markdown·score JSON을 남긴다. 기준본과 후보본에는 같은 `held-out-exception.md`를 전달하며, 후보 home에는 검증할 profile만 설치한다. `--model`을 생략하면 결과에 `executor-default-unverified`라고 기록하므로 정식 비교에는 명시한다.
