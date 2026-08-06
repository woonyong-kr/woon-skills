# Operations

## 개인 스킬 변경

1. `personal/<name>/SKILL.md`와 필요한 `scripts/`, `references/`만 수정합니다.
2. description을 180자 이하로 유지합니다.
3. 필요한 side effect를 `conflicts/effects.yaml`에 선언합니다.
4. `woon skills validate --profile <profile>`을 실행합니다.
5. `woon skills plan --profile <profile> --target <target>`에서 변경 범위를 확인합니다.
6. 설치 후 같은 plan이 모두 `unchanged`인지 확인합니다.

## vendor 업데이트

1. upstream 변경을 별도 branch에서 가져옵니다.
2. 라이선스와 source commit을 확인합니다.
3. `lock/sources.yaml`의 commit을 갱신합니다.
4. 기존 profile의 routing, conflict, effect 회귀를 검증합니다.
5. 자동 병합하지 않고 review PR로 반영합니다.

## 폐기

사용하지 않는 스킬은 먼저 profile에서 제거합니다. 설치 검증이 끝난 뒤 원본을 `retired/`로 옮기고 사유와 대체 스킬을 기록합니다. 이력 보존 없이 바로 삭제하지 않습니다.

## 완료 조건

- macOS, Linux, Windows CI가 통과합니다.
- 기본 profile이 최대 활성 개수를 넘지 않습니다.
- unresolved conflict와 undeclared side effect가 없습니다.
- 두 번 설치한 뒤 plan이 `unchanged`입니다.
- 운영 파일에 사용자 home 절대경로가 없습니다.
