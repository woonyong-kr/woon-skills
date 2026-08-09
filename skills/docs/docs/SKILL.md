---
name: docs
description: 저장소의 README, 설치·사용법, API 설명, CONTRIBUTING, runbook 같은 개발 문서를 코드와 실제 명령에 맞게 작성·갱신할 때 사용한다.
---

# Docs

이 스킬은 저장소 문서가 코드와 일치하게 만드는 용도다. 외부 라이브러리 사용법 조회는 `$lookup`, 의사결정 기록은 `$adr`, 기술 글은 `$tech`, 파일 형식 변환은 docx/pdf 도구를 쓴다.

1. 코드, manifest, lockfile, CI, script, `--help`를 source of truth로 읽는다.
2. 대상 독자와 수행할 작업을 정하고 prerequisites→steps→verification→troubleshooting 순으로 쓴다.
3. install/run 명령은 저장소에서 실제로 확인된 것만 사용한다. 관행으로 `pip install .` 같은 명령을 만들지 않는다.
4. 경로, option, output, version을 현재 구현과 대조한다.
5. 링크와 code block을 검사하고 가능하면 명령을 직접 실행한다.
6. 아직 구현되지 않은 기능은 계획 또는 제한으로 표시한다.

문서만 보고 성공했다고 하지 말고 문서가 가리키는 실제 동작까지 확인한다.

초보자 tutorial이나 개념 설명이 주목적이면 `woon resolve repo://skills/standards/learning-content-quality.md`로 내부 학습문서 표준을 읽고 문제→실행 예제→원인→개념→개선→연습 흐름을 적용한다.
