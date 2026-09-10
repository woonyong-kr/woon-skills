# 문맥 비용 측정 계약

## 측정 층

1. `inventory`: profile에 노출되는 모든 name·description
2. `activation`: 실제 선택된 `SKILL.md` 본문
3. `conditional`: 해당 작업에서 실제 읽은 reference
4. `runtime`: system, rules, history, MCP·tool schema를 포함한 실행기 사용량

모든 reference의 합계를 한 요청의 비용으로 보고하지 않는다. 실행 경로에서 읽힌 파일만 `conditional`에 포함한다.

## 증거 우선순위

1. Codex·Claude 실행기가 보고한 input, cached input, output token
2. 이름을 기록한 실제 tokenizer 측정
3. 문자·단어 기반 추정

하위 증거를 사용할 때는 `estimated`로 표시한다. 서로 다른 tokenizer 결과를 직접 비교하지 않는다.

## 기본 검토 기준

- description: `o200k_base` 80 token을 넘으면 축약 가능성을 검토한다.
- `SKILL.md`: 500 token을 넘으면 중복 제거와 조건부 reference 분리를 검토한다.
- description: 승인본보다 15 token 또는 20% 이상 증가하면 routing 개선 근거를 요구한다.
- 본문: 승인본보다 100 token 또는 20% 이상 증가하면 행동 개선 근거를 요구한다.
- 실제 실행 p95: 비교 가능한 표본에서 10% 이상 증가하면 필요성과 품질 trade-off를 검토한다. 현재 요청의 승인 범위 안에서는 별도 재승인 조건으로 삼지 않는다.

이는 자동 실패 기준이 아니다. 안전·정확성·routing 개선이 비용을 정당화할 수 있다. tokenizer가 없으면 description 180자를 임시 fallback으로 사용하되 실제 token 기준처럼 표현하지 않는다.

## 비교 조건

승인본과 후보본의 요청, profile, model, 도구, 권한과 fixture를 같게 유지한다. 필요한 비교를 한 번 수행하고 변동이나 미해결 위험을 확인할 때만 반복한다. 표본이 부족하면 개별 사용량만 보고하고 p50·p95를 안정적인 분포처럼 해석하지 않는다.

Codex와 Claude는 같은 Woon 정본과 합격 기준을 사용한다. 실행기별 adapter는 원시 usage를 공통 필드로 변환하며, 지원하지 않는 값은 `null`로 둔다.

## 최적화 순서

1. 사용하지 않는 profile·MCP·toolset 노출 제거
2. 중복되거나 모호한 description 정리
3. `SKILL.md`에서 일반 지식과 상세 예제를 제거
4. task별 reference 분리
5. 반복되는 결정적 작업을 script로 이동

이름을 모호하게 줄이거나 reference 탐색을 깊게 만들어 절감하지 않는다.

## 보고

측정 환경, 기준본, 각 층의 token, p50·p95, 품질 지표, 절감 후보와 미검증 범위를 함께 제시한다. 실제 사용량과 파일 token을 별도 표로 구분한다.
