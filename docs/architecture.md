# Architecture

## 역할

`woon-skills`는 스킬 원본과 선택 규칙만 소유합니다. workspace 탐색과 설치 실행은 `woon-core`의 `woon skills` 명령이 담당합니다.

```text
profile + source lock + conflict/effect rules
                    ↓
             woon skills plan
                    ↓
          staging → backup → install
                    ↓
       manifest hash와 실제 폴더 재검증
```

## 소유권 경계

- `personal/<name>/`: 이 저장소에서 직접 유지합니다.
- `vendor/<origin>/<name>/`: `lock/sources.yaml`의 upstream commit에서 가져옵니다.
- `profiles/<name>.yaml`: 활성 스킬 reference와 최대 개수를 선언합니다.
- `conflicts/conflicts.yaml`: 함께 활성화할 수 없는 스킬을 선언합니다.
- `conflicts/effects.yaml`: write, process, network, commit, push, merge, release, delete 권한을 선언합니다.
- 설치 대상의 `.woon-installed.json`: Woon이 관리하는 폴더와 content hash만 기록합니다.

설치 대상에 manifest가 소유하지 않는 같은 이름의 폴더가 있으면 중단합니다. manifest와 실제 hash가 다르면 `update`, 폴더가 사라졌으면 `repair`, profile에서 빠졌으면 `retire`로 계획합니다.

## 이식성

저장소 파일에는 절대 사용자 경로를 넣지 않습니다. `woon-core/registry/repositories.yaml`의 상대 디렉터리와 Woon root locator만 사용합니다. Codex와 Claude 설치 위치는 OS 기본값 또는 다음 machine-local 환경 변수로 결정합니다.

- `WOON_CODEX_SKILLS_HOME`
- `WOON_CLAUDE_SKILLS_HOME`
