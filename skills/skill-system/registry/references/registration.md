# 스킬 등록 계약

## 검색 순서

1. `woon resolve repo://skills/catalog.json`으로 찾은 root catalog의 Woon canonical
2. 선택한 Codex·Claude target에 설치된 fallback
3. `vendor/`에 고정한 비교 원본
4. 공식 최신 source

Woon에 같은 기능이 있으면 그것을 우선한다. 반환된 machine-local 절대 경로는 실행에만 사용하고 catalog나 문서에는 저장하지 않는다. fallback은 Woon에 없는 기능만 사용하며 별도 정본 복사본을 만들지 않는다.

## 소유권과 분리

등록 전에 목적, primary trigger, near-miss, owner, read/write/network 등 effect와 금지 행동을 적는다.

- 같은 요청에서 항상 함께 필요하고 owner·effect가 같으면 병합한다.
- 독립 호출이 가능하거나 owner·effect가 다르면 분리한다.
- 언어 공통 규칙은 `$quality`, 어휘는 `$naming`, 언어별 구조는 해당 언어 스킬이 소유한다.
- 행동 검증, 정적 감사와 토큰 측정은 각각 `$comply`, `$audit`, `$budget`이 소유한다.

## 이름

사용자가 `$name`으로 자연스럽게 부를 수 있는 가장 짧은 이름을 고른다. 한 단어를 우선하지만 강제하지 않는다. 기존 Woon 이름, Codex·Claude fallback, 일반 명령과 의미가 충돌하거나 routing near-miss가 실패하면 짧은 수식어를 붙인다.

이름을 바꿀 때는 profile, routing, 문서와 설치 manifest 영향을 확인한다. 영구 alias를 만들지 말고 migration 기간과 제거 조건을 기록한다.

## 등록 파일

- `skills/<domain>/<name>/SKILL.md`
- `agents/openai.yaml`: display name, 한국어 짧은 설명, `$name`을 포함한 기본 요청
- 필요할 때만 `references/`, `scripts/`, `assets/`
- `sources/catalog.yaml` 또는 `sources/derivations.yaml`
- `conflicts/effects.yaml`과 필요한 conflict
- 최소 `profiles/*.yaml`
- profile-resolution, positive·near-miss routing, behavior 사례
- 재생성한 root `catalog.json`

Codex와 Claude는 같은 파일을 설치하며 target별 문구를 별도 정본으로 만들지 않는다. 호환 차이는 실행기 adapter나 machine-local 설정에서 처리한다.

## Source 방식

- `vendor`: 원문과 license를 유지하고 commit에 고정
- `derivation`: 유용한 개념만 Woon 규칙으로 재작성하고 변경점을 기록
- `fallback`: Woon에 복사하지 않고 target 설치본을 필요할 때 사용
- `native`: Woon 고유 요구이며 소유 근거를 기록

## 승격과 퇴역

신규·변경 스킬은 `$audit → $budget → $comply`와 사용자 승인을 통과하기 전 기본 profile에 넣지 않는다. `eval`처럼 `installable: false`인 profile은 catalog 검사에만 사용한다.

퇴역 시 profile과 routing에서 먼저 제거하고 dependent reference와 clean install을 검증한다. 원본은 이유와 대체 스킬을 기록해 `archive/`에 보존한다. 관리하지 않는 Codex·Claude 설치 폴더는 삭제하지 않는다.
