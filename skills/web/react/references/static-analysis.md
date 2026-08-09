# React 정적 진단 계약

정적 진단은 코드 후보를 찾는 도구다. 점수, `ok` 필드 또는 경고 수 하나로 frontend 완료를 판정하지 않는다.

## 실행

1. 프로젝트가 고정한 도구와 version을 먼저 쓴다. 없으면 Woon이 마지막으로 검토한 정확 version만 임시 실행하고 `@latest`를 재현 가능한 검증에 쓰지 않는다.
2. 첫 실행은 source와 config를 바꾸지 않는 report 모드로 제한한다. telemetry와 외부 supply-chain 조회는 기본으로 끄고, 필요하면 별도 목적과 network 범위를 확인한다.
3. skill·hook·CI 설치, config 변경, 자동 수정은 사용자가 그 변경을 요청했을 때만 수행한다.

현재 검토본의 offline 예시는 다음과 같다. 새 version을 승인하면 source review와 이 명령을 함께 갱신한다.

```bash
npx --yes react-doctor@0.9.11 . \
  --json --json-out /tmp/react-doctor-report.json \
  --no-telemetry --no-supply-chain --no-cache --yes
```

## 판독

- process exit code, report schema/version, error·warning 수, skipped·partial 상태를 함께 읽는다.
- `ok: true`는 scan이 보고서를 만들었다는 뜻일 수 있으므로 진단 0건이나 gate 통과로 추론하지 않는다. `ok: true`와 non-zero exit의 조합도 곧바로 tool 결함으로 단정하지 말고 exact version의 exit 계약과 남은 진단을 확인한다.
- changed scope는 base ref와 untracked 포함 여부를 기록한다. full scan과 같은 증거로 표현하지 않는다.
- 같은 rule의 반복은 root cause 하나인지 서로 다른 결함인지 code span과 실행 경로로 구분한다.

## 판단과 수정

각 finding마다 실제 framework/version, binding과 control flow, 사용자 동작, 기존 suppression·config·테스트를 대조한다. 재현하지 않은 경고를 자동 수정하거나 원격 recipe를 그대로 적용하지 않는다. 문서화된 controlled adapter가 parent callback으로 외부 상태를 동기화한다면 경고만으로 event handler 이동을 단정하지 말고 feedback loop·초기화·외부 갱신 계약을 먼저 검증한다. 의도적인 패턴이면 이유를 남기고 가장 좁은 line·file·rule 범위만 예외화한다. 전역 disable은 전체 codebase에서 규칙이 부적합하다는 증거가 있을 때만 검토한다.

수정 전후에는 같은 도구 version·scope·config로 report를 비교한다. 새 진단, 사라진 진단, 실행 실패와 분석 제외 파일을 분리한다. 점수 상승과 진단 감소가 typecheck·test·browser 결과를 대신하지 않는다.

## 완료 게이트

| 증거 | 소유자 | 증명하지 못하는 것 |
| --- | --- | --- |
| React 정적 진단 | `$react` | 실제 focus, responsive layout, network·저장 결과 |
| computed style·viewport·keyboard·screenshot | `$css`, `$ui-test` | backend authorization와 persistence |
| 여러 화면과 service를 잇는 journey | `$e2e` | 모든 시각적 완성도와 production 상태 |

한 층에서 실패하면 다른 층의 점수가 높아도 완료가 아니다. 원인 소유자에서 수정한 뒤 static → component/test → rendered UI → 필요한 E2E 순서로 다시 검증한다.
