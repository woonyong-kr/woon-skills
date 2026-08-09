# Operations

## Woon 스킬 변경

1. root `catalog.json`과 `$registry`로 기존 trigger, owner, effect와 source를 조사합니다.
2. `skills/<domain>/<short-name>/SKILL.md`를 만들거나 병합합니다.
3. description 80 token과 main body 500 token을 기본 검토선으로 삼고 procedure 중심으로 유지합니다.
4. 긴 규칙은 한 단계 `references/`로 옮깁니다.
5. `agents/openai.yaml`, effects, profile, profile-resolution, positive·near-miss routing과 behavior case를 갱신합니다.
6. `python scripts/build_catalog.py`로 root catalog를 재생성합니다.
7. `python scripts/audit_skills.py`와 `$audit` 정적 검사, `$budget` 문맥 검사, `$comply` 행동 scenario를 실행합니다.
8. Codex와 Claude 각각 plan→install→두 번째 plan `unchanged`를 확인합니다.

## vendor 업데이트

upstream을 별도 branch에서 가져와 license와 commit을 확인하고 `lock/sources.yaml`을 review PR로 갱신합니다. vendor 본문을 직접 고치지 않습니다. useful concept를 Woon에 반영할 때는 `sources/derivations.yaml`에 overlap과 변경점을 기록합니다.

## natural routing 평가

`evals/routing/` case는 명시 호출뿐 아니라 자연스러운 한국어 요청, 경계가 가까운 skill, 금지 선택을 포함합니다. 지원되는 Codex·Claude selector에서 같은 catalog와 기준으로 3회 실행해 primary recall, forbidden selection, agreement를 확인합니다. 아직 adapter가 없는 target은 `unverified`로 보고하며 keyword match나 profile resolution만으로 routing 품질을 주장하지 않습니다.

## 폐기

먼저 profile에서 제거하고 clean install에서 퇴역을 검증합니다. 원본은 `archive/`로 옮겨 이유와 대체 skill을 남깁니다. 설치된 unmanaged folder나 user change를 삭제하지 않습니다.

## 완료 조건

- schema와 nested catalog가 유효함
- root catalog가 최신이며 Codex·Claude가 같은 정본을 가리킴
- profile별 `max_active` 이내이며 knowledge는 4개만 노출
- unresolved conflict와 undeclared side effect가 없음
- semantic routing과 behavior boundary case 통과
- 두 번 설치한 뒤 plan이 `unchanged`
- absolute home path와 secret이 없음
- 실행한 검증과 미실행 production 계층이 구분됨
