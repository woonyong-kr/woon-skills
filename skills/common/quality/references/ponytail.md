# Ponytail과 Woon

Codex의 모든 코드 설계·작성·수정·오류 수정·리팩터링·리뷰에는 공식 `ponytail@ponytail` plugin의 `ponytail`을 `full`로 적용한다. 본문은 설치 plugin이 소유하며 Woon에 복제하지 않는다. Woon `quality`는 프로젝트 계약과 변경 경계, `test`와 `verify`는 위험에 맞는 검증, `safety`는 외부 효과를 계속 담당한다.

- 가장 적은 코드로 사용자가 요청한 동작 전체를 구현한다. 짧게 만들기 위해 요구사항, 데이터 보존, 보안, 호환성이나 필요한 검사를 생략하지 않는다.
- 기존 테스트 도구와 의미 있는 통과 근거를 재사용한다. Ponytail의 작은 실행 검사 원칙은 새 자체 검사·새 파일·프레임워크 금지를 강제하지 않는다. 검증 범위는 `repo://core/standards/code.yaml`을 따른다.
- 한국어 응답, 사용자가 요청한 설명과 진행 보고를 보존한다. 일반 문장 교정은 `humanize`, 새 기술 학습 글은 `tech`가 소유한다.
- `ponytail-review`와 `ponytail-audit`은 복잡성 검토다. 일반 코드 리뷰의 정확성·보안 검사를 대체하지 않는다. 단축한 코드 줄 수나 비용 절감은 이 환경에서 측정한 근거 없이 주장하지 않는다.
- 설치·기본 full 적용은 자동 commit·push·배포·새 작업·숨은 subagent 실행을 허용하지 않는다. 사용자가 나중에 명시적으로 모드를 바꾸거나 중단하면 그 지시를 따른다.

## 설치와 확인

공식 `codex plugin marketplace add DietrichGebert/ponytail`과 `codex plugin add ponytail@ponytail`을 사용한다. 갱신 전 exact upstream commit과 hook 명령·호출 스크립트를 검토하고 설치 bytes를 비교한다. `codex plugin list --json`의 enabled 상태와 공식 `hooks/list`의 enabled·currentHash·trustStatus를 따로 확인한다. 검토한 현재 hook 정의만 신뢰하며 변경된 hash는 다시 검토한다.

기본 모드는 upstream resolver의 `full`이며, 환경 변수와 사용자 설정의 override도 확인한다. SessionStart matcher는 `startup|resume|clear|compact`다. UserPromptSubmit은 모드 명령 추적이며 일반 프롬프트마다 전체 지침을 다시 넣는 hook이 아니다. 기존 활성 작업의 적용을 새 세션의 자동 로드로 추정하지 않는다.

검증 기록은 plugin 버전·commit·설치 hash, 신뢰 상태, hook 출력의 full 지침, 실제 runtime 문맥 로드를 구분한다. 직접 hook 실행과 schema 검증은 runtime의 모델 요청에 전달됐다는 증거가 아니다. 새 세션·재개·압축 중 실행하지 않은 경계는 미검증으로 남긴다. 설정이나 상태 플래그만으로 실제 적용 완료를 주장하지 않는다.
