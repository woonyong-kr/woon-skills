# 스킬 행동 평가 계약

## 목적과 소유권

`$comply`는 변경된 스킬의 routing·권한·행동을 실제 산출물과 부수 효과로 평가한다. 정적 구조는 `$audit`, 문맥 비용은 `$budget`, catalog·설치는 `$registry`가 소유한다. 기준본 비교·실제 효과·출처 가림의 원칙은 기존 Woon derivation을 유지하며 특정 실행기나 모델을 필수로 고정하지 않는다. 검증 범위와 근거 재사용은 `repo://core/standards/code.yaml`을 따른다.

## 사례와 기준본

기존 사례에서 변경한 실패 경계를 선택한다. 사례의 `id`, `prompt`, `require`, `forbid`는 유지하고, fixture·critical·evidence는 필요한 경우에 쓴다. 요청에 정답이나 스킬 문장을 노출하지 않는다. 새 사례는 기존 사례가 포착하지 못하는 중요한 회귀를 다룰 때만 추가한다.

단순 계약 충돌 수정은 관련 정적 검사와 한 번의 행동 확인으로 검증할 수 있다. 개선 효과를 비교하려면 기존 승인본 또는 해당 지시를 제외한 `no-guidance control`과 후보본을 같은 model·도구·권한·입력에서 대조한다. 신규 보안·권한 불변조건에 관찰된 실패를 인위적으로 만들 것을 요구하지 않는다. 비교 근거가 없으면 효과 향상은 `unverified`다.

## 실행과 판정

1. 실제 diff·파일·명령·tool effect를 먼저 검사하고, 응답이 규칙을 인용했다는 이유로 통과시키지 않는다.
2. 치명적인 권한·secret·정본 손실은 한 번이라도 발생하면 실패다. 평균 점수로 상쇄하지 않는다.
3. 설명력처럼 결정적으로 확인할 수 없는 항목만 출처를 가린 의미 비교로 판단한다. 상충하는 판정은 근거를 좁혀 확인하며 해결 전에는 `unverified` 또는 `unstable`로 남긴다.
4. 필요한 사례를 한 번 실행한다. 결과 변동·미해결 실패·고위험 경계가 추가 근거를 요구할 때만 다른 표현·누락·도구 실패나 미공개 입력으로 넓힌다. 3회·5회 반복이나 무실패 두 라운드를 모든 변경의 필수 gate로 삼지 않는다.
5. 실패 원인을 고친 뒤 영향받는 사례만 다시 확인한다. 입력·환경이 같은 통과 근거는 재사용한다. 충분한 표본 없이 일치율·p95를 안정성의 증거로 보고하지 않는다.

## 기록과 종료

실행기는 다음 공통 필드로 관찰값을 기록한다. 지원하지 않는 usage나 시간은 `null`이며 추정값과 실제값을 구분한다.

```yaml
case_id: string
variant: baseline | candidate
trial: integer
executor: string
model: string
prompt_digest: string
fixture_digest: string | null
output_artifacts: [path]
tool_events: []
commands: []
duration_ms: integer | null
tokens:
  input: integer | null
  cached: integer | null
  output: integer | null
grader_results: []
```

선택한 수용 기준을 충족하고 해결되지 않은 필수 실패가 없으면 종료한다. 정본 수정·설치가 이미 허용된 범위이면 평가 결과에 대한 재승인을 만들지 않는다. 새로운 외부 효과나 범위 확대는 `$safety`에서 다룬다.

보고에는 계약 통과 여부, 실제 증거, 남은 위험과 비교 효과의 상태를 구분한다. 같은 조건의 비교가 있으면 `verified improvement` 또는 `regression`, 변동이 해결되지 않으면 `unstable`, 비교나 필수 실행 근거가 없으면 `unverified`다. 정적 통과나 한 번의 성공은 모델 전반의 품질 보장이 아니다. 임시 원시 trace는 private로 유지하고 완료 뒤 복구에 필요하지 않으면 정리한다.
