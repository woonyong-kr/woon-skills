# woon-skills

Codex와 Claude가 작업에 필요한 스킬만 결정적으로 선택·설치하도록 관리하는 Woon 스킬 카탈로그입니다. 모든 스킬을 한꺼번에 설치하지 않습니다.

## 빠른 시작

먼저 [`woon`](https://github.com/woonyong-kr/woon-core/releases) 바이너리와 Woon 저장소를 준비합니다.

```text
<woon-root>/
├── woon-core/
└── woon-skills/
```

```bash
woon skills validate --profile core
woon skills plan --profile core,python --target codex
woon skills install --profile core,python --target codex
woon skills doctor
```

Windows PowerShell에서도 같은 명령을 사용합니다. 저장소 위치는 고정하지 않으며 `woon init --root <path>` 또는 `WOON_HOME`으로 찾습니다.

## 구조

```text
personal/    직접 유지하는 스킬
vendor/      upstream commit에 고정된 외부 스킬
profiles/    실제로 활성화할 작은 스킬 집합
conflicts/   중복 trigger와 side effect 선언
lock/        출처·commit·업데이트 정책
evals/       routing 회귀 사례
```

기본 `core` profile은 20개 이하로 유지합니다. 설치기는 대상 폴더의 실제 hash를 다시 확인하며, 관리하지 않는 기존 스킬을 덮어쓰지 않습니다. 변경 파일은 먼저 staging하고 기존 관리 파일은 backup한 뒤 적용합니다.

## 원칙

- `personal/`은 직접 수정하고 검증합니다.
- `vendor/` 업데이트는 lock된 upstream commit을 바꾸는 review PR로만 받습니다.
- profile에 넣기 전 description, trigger 충돌, side effect를 검토합니다.
- `SKILL.md`는 절차 중심으로 유지하고 긴 설명과 예제는 `references/`로 분리합니다.
- 사용자별 경로와 token은 저장소에 기록하지 않습니다.
- 설치는 `woon skills`만 사용하며 별도 전체 복사 스크립트를 두지 않습니다.

설계는 [architecture](docs/architecture.md), 유지보수 절차는 [operations](docs/operations.md)를 참고하세요.

## 지원 환경

`woon` CLI 기준으로 macOS, Linux, Windows를 지원합니다. 경로 결합은 OS API를 사용하고, 공백이 있는 경로를 회귀 테스트하며, 세 운영체제의 GitHub Actions에서 동일한 profile 해석을 검증합니다.

## 라이선스

각 vendor 스킬의 라이선스와 upstream 조건이 우선합니다. 출처 정보는 `lock/sources.yaml`에서 관리합니다.
