# Woon 저장소 규칙

이 문서는 `.woon/repository.yaml`이 있는 저장소 또는 Woon 저장소 간 소유권을 판단할 때만 적용한다.

## 정본 소유권

- `woon-core`: 정책 모델, registry, resolver, compiler와 CLI
- `woon-skills`: 스킬 원본, profile, routing·effect 정책과 source lock
- `woon-env`: 편집기와 실행 환경의 선언적 의도와 adapter
- `woon-knowledge`: 비공개 지식 정본과 검색·보관 평가
- `woon-site`: 공개 글의 편집 정본
- output 저장소: 생성 결과만 보관하며 직접 편집하지 않음

교차 저장소 파일을 복사하지 않는다. `woon-core/registry/repositories.yaml`에 등록된 `repo://<id>/...` 참조를 사용하고 resolver로 실제 경로를 확인한다. 머신별 절대 경로는 Git에서 제외된 `.local/`에만 둔다.

## 루트와 설정 배치

- Woon 공통 저장소 메타데이터는 `.woon/repository.yaml`에 둔다.
- 제품 설정과 사용자가 편집하는 설정은 `config/`에 둔다.
- GitHub가 경로를 강제하는 CI 파일은 `.github/workflows/`에 둔다.
- 도메인 소유 YAML은 소유자 가까이에 둔다. 스킬 profile은 `profiles/`, adapter 계약은 `adapters/`, 잠금 기록은 `lock/`에 둔다.
- `pyproject.toml`, `package.json` 같은 빌드 명세는 도구가 요구하는 위치에 둔다.
- 루트 파일 수만 줄이려고 YAML을 이동하지 않는다. 목적지의 소유자가 하나로 명확하고 모든 소비자를 함께 갱신하고 검증할 수 있을 때 이동한다.
- 코드 저장소는 `src/<package>/`와 `tests/`를 기본으로 한다. 지식, 스킬 목록, 생성 결과물과 설정 저장소에는 역할 중심 폴더를 사용한다.
- 생성 표시가 있는 `AGENTS.md`와 설정 결과물을 직접 편집하지 않는다. 정본 설정을 수정한 뒤 다시 생성한다.

## 이름과 변경 경계

- 저장소와 일반 폴더는 `kebab-case`, Python package는 `lower_snake_case`, Java package segment는 소문자 계층형 이름을 사용한다.
- `.github`처럼 도구가 강제하는 경로와 output 저장소 이름은 예외로 유지한다.
- 정본 역할이 다른 저장소를 물리적으로 합치지 않는다.
- interface, 폴더 구조, workflow 또는 소유권이 바뀌면 같은 변경에서 관련 문서와 검증 규격도 갱신한다.
- push, deploy, visibility 변경과 외부 공개는 별도 승인이 없으면 실행하지 않는다.
