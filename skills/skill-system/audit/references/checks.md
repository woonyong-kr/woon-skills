# 스킬 정적 검사 계약

## 등급

- `error`: 설치, routing, 안전 또는 정본 무결성을 깨므로 승인할 수 없음
- `warning`: 현재 동작할 수 있지만 품질 저하나 drift 가능성이 큼
- `advisory`: 선택적 개선이며 승격을 막지 않음

## 규격과 metadata

- `SKILL.md`와 YAML frontmatter가 존재한다.
- `name`은 64자 이하 kebab-case이며 directory와 같다.
- description은 기능과 사용 시점을 모두 포함한다.
- Woon 기본값 80 token을 넘으면 warning으로 `$budget`에 연결한다.
- `agents/openai.yaml`에 `display_name`, 25~64자의 `short_description`, 해당 `$skill`을 포함한 `default_prompt`가 있다.

## 구조와 중복

- 모든 상대 reference와 script가 존재하고 `SKILL.md`에서 한 단계로 연결된다.
- name은 catalog 전체에서 유일하다.
- 동일하거나 의미가 겹치는 description과 본문을 보고한다.
- `TODO`, placeholder, 죽은 경로와 사용되지 않는 asset을 보고한다.
- generated 파일에는 생성 주석 또는 machine-readable marker와 재생성 경로가 있다.

## Source

- 외부 원본은 URL, 확인 commit, license와 update policy를 기록한다.
- vendor 원본은 lock과 일치하며 직접 수정하지 않는다.
- Woon 파생본은 가져온 개념과 변경한 경계를 `sources/derivations.yaml`에 기록한다.
- 출처가 없는 Woon 고유 규칙과 외부 파생 규칙을 구분한다.

## Catalog 연결

- root `catalog.json`의 name·path·description이 `SKILL.md`에서 결정적으로 재생성된다.
- 필요한 effect·conflict가 선언된다.
- 최소 profile과 profile-resolution 사례가 있다.
- positive와 가까운 near-miss routing 사례가 있다.
- 주요 promise와 금지 효과에 behavior 사례가 있다.
- `installable: false` profile은 Codex·Claude 설치 대상에서 제외돼야 한다.

## 안전

- secret, 개인 token, machine별 절대 경로와 private 원문을 금지한다.
- Woon 정본을 다른 저장소에 복사하라는 지시를 금지한다.
- generated 파일 직접 수정과 승인 없는 push·deploy·delete를 금지한다.
- tool 권한과 `conflicts/effects.yaml`의 side effect가 일치해야 한다.

## 보고

각 결과에 등급, 파일, 필드 또는 줄, 확인한 사실, 영향과 최소 수정 조건을 기록한다. 정적 검사로 행동 효과나 실제 runtime token을 검증했다고 표현하지 않는다.
