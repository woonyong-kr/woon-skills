# woon-skills

Woon이 직접 유지하는 스킬을 짧은 이름과 작은 profile로 선택·설치하는 canonical catalog입니다. `woon-skills` 원본이 항상 우선이고, 없는 기능만 Codex에 설치된 skill/plugin을 fallback으로 사용합니다.

## 빠른 시작

```bash
rg -n '커밋|문서|Java' catalog.json
woon skills validate --profile core
woon skills plan --profile core,python --target codex
woon skills install --profile core,python --target codex
woon skills install --profile core,python --target claude
woon skills eval-routing --executor codex --repeat 1
woon skills doctor
```

루트 `catalog.json`은 모든 Woon 정본의 이름·domain·경로·description을 `SKILL.md`에서 생성한 색인입니다. 다른 저장소에서는 `woon resolve repo://skills/catalog.json`으로 위치를 찾습니다. 여기서 필요한 스킬을 먼저 찾고 Woon에 없을 때만 각 target의 installed skill/plugin을 fallback으로 사용합니다. `python scripts/audit_skills.py`로 metadata·link·catalog drift와 upstream source review를 검사합니다.

`core`는 `$quality·$safety·$terminal·$verify·$commit` 5개뿐입니다. 모든 스킬을 설치하지 말고 저장소에 맞는 profile을 추가합니다.

| 작업                     | profile               | Woon 스킬                                                                 |
| ------------------------ | --------------------- | ------------------------------------------------------------------------- |
| 공통 개발                | `development`       | `$quality·$naming·$refactor·$test`                                   |
| LLM·agent 개발          | `ai`                | development +`$agent-audit`                                             |
| Python                   | `python`            | `$python·$pytest`                                                      |
| Java                     | `java`              | `$java`                                                                 |
| TypeScript               | `typescript`        | `$ts`                                                                   |
| Spring/JPA               | `spring`            | `$spring·$spring-test·$spring-sec·$jpa`                              |
| backend 기본 설계        | `backend`           | `$domain·$hexagonal·$api·$tx`                                        |
| 분산 backend             | `distributed`       | `$tx·$event·$job·$protocol·$resilience·$capacity·$observe·$test` |
| worker·batch            | `worker`            | `$tx·$event·$job·$resilience·$capacity·$observe·$test`            |
| SaaS·multi-tenant       | `saas`              | `$domain·$api·$tx·$tenant·$auth·$privacy·$test`                   |
| data·storage            | `data`              | `$cache·$migration·$postgres·$storage`                               |
| 운영 기반                | `ops`               | `$capacity·$container·$docker·$observe`                              |
| 인증·개인정보·보안     | `security`          | `$auth·$privacy·$security`                                            |
| GitHub                   | `github`            | `$pr·$issue·$ci·$release·$notify`                                   |
| 개발 문서                | `docs`              | `$docs·$lookup·$adr·$diagram`                                        |
| private knowledge        | `knowledge`         | `$safety·$knowledge·$archive·$ingest·$compile-knowledge·$tech·$diagram` |
| 논문·NotebookLM 지식화   | `research-library`  | knowledge +`$research·$research-library`                                 |
| LLM Wiki maintenance     | `knowledge-compile` | `$safety·$knowledge·$compile-knowledge·$diagram·$tech`               |
| AI 보조 학습             | `learning`          | `$guided-learning·$kotlin-in-action-14-days·$tech·$diagram`          |
| 대화 기반 문제 해결 회고 | `insight`           | `$insight`                                                              |
| private 소설 작업        | `novel`             | `$safety·$novel-handoff·$novel-merge`                                 |
| 지식→사이트 공개 후보   | `site-promotion`    | `$safety·$verify·$knowledge·$site-promotion`                           |
| knowledge 공개           | `knowledge-publish` | knowledge +`$publish`                                                   |
| 기술·커리어 글          | `publishing`        | `$docs·$diagram·$career·$interview·$tech`                           |
| 웹                       | `web`               | `$css·$react·$e2e·$ui-test`                                          |
| 스킬 관리                | `skill-system`      | `$registry·$audit·$comply·$budget`                                   |

## 스킬 작성과 실행 기준

목적·적용 범위·필수 불변조건·완료 증거를 먼저 정합니다. 모델이 이미 수행할 수 있는 일반 설명, 역할놀이, 고정된 사고 단계와 같은 규칙의 복제를 줄이고, 실제 의존 순서나 복구 위험이 있는 절차만 순서를 고정합니다. 상세 예시·도구 명령은 필요한 reference에서 읽습니다.

현재 사용자 지시와 대화에서 확보한 대상·권한을 재사용합니다. 맡긴 범위의 가역적 준비·수정·검증은 완료하고, 아직 권한이 없는 외부 효과나 되돌리기 어려운 행동만 구체적인 결과를 제시한 뒤 확인합니다. skill 때문에 중단하거나 승인이 필요하면 해당 파일·조항과 실제 적용 이유를 밝힙니다. 일반적인 우려만으로 새 승인 단계를 만들지 않습니다.

검증 선택·동일 입력의 통과 근거 재사용·임시물 정리는 `repo://core/standards/code.yaml`을 따릅니다. 도구는 현재 사용 가능성과 실제 효과로 선택하고, 역할 이름을 여러 agent 생성 지시로 해석하지 않습니다. 결과와 변경 이유·검증·미확인 범위를 간결한 한국어로 보고하며 모든 요청에 고정 보고 양식을 적용하지 않습니다.

이 기준은 [OpenAI의 모델 사용 지침](https://developers.openai.com/api/docs/guides/latest-model)과 [skill 작성 지침](https://learn.chatgpt.com/docs/build-skills)을 2026-09-09에 확인해 반영했습니다. 모델 설정이나 공급 skill을 바꾸는 계약은 아니며, 특정 모델 이름을 개별 skill에 반복하지 않습니다.

## 문서 스킬의 차이

- `$docs`: 현재 저장소의 README, 설치법, API 설명, runbook을 실제 code/manifest/`--help`에 맞춥니다.
- `$lookup`: 현재 version의 외부 library/framework 공식 문서를 찾습니다.
- `$adr`: 하나의 architecture 결정과 대안·결과를 기록합니다.
- `$tech`: 근거와 한계가 있는 기술 글·학습 글을 씁니다.
- `$humanize`: `humanizer-kr`의 한국어 교정 기준으로 원뜻·말투·기술 용어를 보존하며 번역투와 반복을 다듬습니다. `personal` profile에 포함됩니다.
- `$guided-learning`: 학습자가 먼저 답하고 실행하도록 한 질문씩 인출·실습·전이·검증을 진행합니다.
- `$kotlin-in-action-14-days`: 다섯 AI 학습 파트너와 책 16개 장을 14일 경로로 진행하고 실제 설명·실행·전이 증거로 진도를 판정합니다.
- `$career`: 이력서·경력기술서·cover letter를 실제 개인 기여에 맞춥니다.
- `$diagram`: Markdown 안의 Mermaid 관계도를 만듭니다.
- `$knowledge`: private 정본과 read-only corpus를 검색·조회·감사합니다.
- `$archive`: 현재 대화를 기존 private 정본에 중복 없이 저장합니다.
- `$compile-knowledge`: source·accepted claim·page spec에서 receipt가 있는 Wiki를 결정론적으로 컴파일합니다.
- `$insight`: 대화에서 실수·가설·전환·해결·검증을 근거로 연결해 재사용할 통찰을 만듭니다. 저장은 하지 않습니다.
- `$novel-handoff`: 소설 정본을 수정하지 않고 로컬 전체 또는 외부 비식별 맥락 prompt를 만듭니다.
- `$novel-merge`: 다른 AI 대화를 사건 lineage와 단일 catalog 기준으로 private 소설 정본에 병합합니다.
- `$publish`: 승인한 private 정본만 public 산출물로 분리합니다.

DOCX, PDF, PPTX, XLSX와 Google Docs 같은 설치 plugin 스킬은 파일 형식·도구 축입니다. 예를 들어 이력서 내용에는 `$career`, DOCX 산출에는 `documents`가 함께 선택될 수 있으며 서로 대체하지 않습니다.

## 구조

```text
skills/<domain>/<short-name>/   Woon이 직접 유지하는 단일 원본
catalog.json                    SKILL.md에서 생성한 Codex·Claude 공통 검색 색인
scripts/build_catalog.py        root catalog 결정적 생성·검사
scripts/audit_skills.py         metadata·link·catalog drift 정적 검사
scripts/audit_sources.py        upstream commit·license·전수 skill review 검사
scripts/audit_backend.py        backend owner·routing·행동·단일 원본 검사
scripts/audit_insight.py        대화 통찰 owner·routing·행동·예산 형태 검사
scripts/audit_novel.py          소설 privacy·inventory·routing·행동 계약 검사
vendor/<origin>/<name>/         upstream commit에 고정한 비교·fallback 원본
profiles/                       작고 목적별인 활성 집합
conflicts/                      side effect와 실제 충돌
evals/profile-resolution.yaml   deterministic profile 회귀
evals/routing/                  natural-language semantic routing 평가
sources/reviews/                upstream 저장소별 모든 skill의 채택·병합·거부 판정
sources/                        조사한 upstream과 Woon 파생 근거
archive/                        활성 catalog에서 퇴역했지만 보존한 자료
```

`SKILL.md`는 decision과 절차만 담고, 상세 언어 규칙과 예제는 그 작업에서만 여는 한 단계 `references/`에 둡니다. machine-specific 절대 경로는 commit하지 않고 다른 저장소는 `repo://skills/...`로 원본을 참조합니다. Codex와 Claude에는 같은 Woon 원본을 설치하고 target별 복사본을 별도 편집하지 않습니다.

외부 스킬 조사와 채택 판단은 [source catalog](sources/catalog.yaml), Woon 스킬로 병합한 근거는 [derivations](sources/derivations.yaml)에 있습니다.
