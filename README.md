# woon-skills

Woon이 직접 유지하는 스킬을 짧은 이름과 작은 profile로 선택·설치하는 canonical catalog입니다. `woon-skills` 원본이 항상 우선이고, 없는 기능만 Codex에 설치된 skill/plugin을 fallback으로 사용합니다.

## 빠른 시작

```bash
rg -n '커밋|문서|Java' catalog.json
woon skills validate --profile core
woon skills plan --profile core,python --target codex
woon skills install --profile core,python --target codex
woon skills install --profile core,python --target claude
woon skills eval-routing --executor all --repeat 3
woon skills doctor
```

루트 `catalog.json`은 모든 Woon 정본의 이름·domain·경로·description을 `SKILL.md`에서 생성한 색인입니다. 다른 저장소에서는 `woon resolve repo://skills/catalog.json`으로 위치를 찾습니다. 여기서 필요한 스킬을 먼저 찾고 Woon에 없을 때만 각 target의 installed skill/plugin을 fallback으로 사용합니다. `python scripts/audit_skills.py`로 metadata·link·catalog drift를 검사합니다.

`core`는 `$quality·$safety·$terminal·$verify·$commit` 5개뿐입니다. 모든 스킬을 설치하지 말고 저장소에 맞는 profile을 추가합니다.

| 작업 | profile | Woon 스킬 |
|---|---|---|
| 공통 개발 | `development` | `$quality·$naming·$refactor` |
| Python | `python` | `$python·$pytest` |
| Java | `java` | `$java` |
| TypeScript | `typescript` | `$ts` |
| Spring/JPA | `spring` | `$spring·$spring-test·$spring-sec·$jpa` |
| GitHub | `github` | `$pr·$issue·$ci·$release·$notify` |
| 개발 문서 | `docs` | `$docs·$lookup·$adr·$diagram` |
| private knowledge | `knowledge` | `$safety·$knowledge·$archive·$diagram` |
| knowledge 공개 | `knowledge-publish` | knowledge + `$publish` |
| 기술·커리어 글 | `publishing` | `$docs·$diagram·$career·$interview·$tech` |
| 웹 | `web` | `$react·$e2e·$ui-test` |
| 스킬 관리 | `skill-system` | `$registry·$audit·$comply·$budget` |

## 문서 스킬의 차이

- `$docs`: 현재 저장소의 README, 설치법, API 설명, runbook을 실제 code/manifest/`--help`에 맞춥니다.
- `$lookup`: 현재 version의 외부 library/framework 공식 문서를 찾습니다.
- `$adr`: 하나의 architecture 결정과 대안·결과를 기록합니다.
- `$tech`: 근거와 한계가 있는 기술 글·학습 글을 씁니다.
- `$career`: 이력서·경력기술서·cover letter를 실제 개인 기여에 맞춥니다.
- `$diagram`: Markdown 안의 Mermaid 관계도를 만듭니다.
- `$knowledge`: private 정본과 read-only corpus를 검색·조회·감사합니다.
- `$archive`: 현재 대화를 기존 private 정본에 중복 없이 저장합니다.
- `$publish`: 승인한 private 정본만 public 산출물로 분리합니다.

DOCX, PDF, PPTX, XLSX와 Google Docs 같은 설치 plugin 스킬은 파일 형식·도구 축입니다. 예를 들어 이력서 내용에는 `$career`, DOCX 산출에는 `documents`가 함께 선택될 수 있으며 서로 대체하지 않습니다.

## 구조

```text
skills/<domain>/<short-name>/   Woon이 직접 유지하는 단일 원본
catalog.json                    SKILL.md에서 생성한 Codex·Claude 공통 검색 색인
scripts/build_catalog.py        root catalog 결정적 생성·검사
scripts/audit_skills.py         metadata·link·catalog drift 정적 검사
vendor/<origin>/<name>/         upstream commit에 고정한 비교·fallback 원본
profiles/                       작고 목적별인 활성 집합
conflicts/                      side effect와 실제 충돌
evals/profile-resolution.yaml   deterministic profile 회귀
evals/routing/                  natural-language semantic routing 평가
sources/                        조사한 upstream과 Woon 파생 근거
archive/                        활성 catalog에서 퇴역했지만 보존한 자료
```

`SKILL.md`는 decision과 절차만 담고, 상세 언어 규칙과 예제는 그 작업에서만 여는 한 단계 `references/`에 둡니다. machine-specific 절대 경로는 commit하지 않고 다른 저장소는 `repo://skills/...`로 원본을 참조합니다. Codex와 Claude에는 같은 Woon 원본을 설치하고 target별 복사본을 별도 편집하지 않습니다.

외부 스킬 조사와 채택 판단은 [source catalog](sources/catalog.yaml), Woon 스킬로 병합한 근거는 [derivations](sources/derivations.yaml)에 있습니다.
