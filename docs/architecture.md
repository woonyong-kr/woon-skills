# Architecture

`woon-skills`는 root catalog, skill source, profile, routing/effect policy를 소유하고 `woon-core`의 `woon skills`가 resolve·validate·install합니다.

```text
catalog.json + source lock + skills/<domain>/<name>
                ↓
      profile-resolution validation
                ↓
  semantic routing + behavior + budget eval
                ↓
        plan → staging → backup → install
                ↓
      manifest hash와 실제 폴더 재검증
```

## 소유권

- `skills/`: Woon canonical. 다른 저장소에 복사하지 않습니다.
- `catalog.json`: `SKILL.md`에서 생성한 이름·경로·description 검색 색인입니다.
- `vendor/`: upstream commit과 license를 고정하고 직접 수정하지 않습니다.
- `profiles/`: 설치할 reference와 `max_active`를 선언합니다.
- `conflicts/effects.yaml`: read/write/process/network와 GitHub side effect를 선언합니다.
- `sources/`: 외부 조사와 custom derivation 근거입니다.
- 설치 대상의 `.woon-installed.json`: Woon이 관리하는 이름과 content hash만 기록합니다.

설치 시 nested source path는 global short name으로 flatten됩니다. 그래서 모든 active skill name은 catalog 전체에서 유일해야 합니다. 관리하지 않는 동일 이름 폴더는 덮어쓰지 않습니다.

## token 경계

항상 노출되는 name/description은 80 `o200k_base` token을 기본 검토선으로 삼고 tokenizer가 없을 때만 180자를 추정 fallback으로 사용합니다. `SKILL.md` 500 token과 실제 실행 p95 10% 증가는 자동 실패가 아니라 품질 근거가 필요한 검토선입니다. 본문은 trigger 때만, reference는 실제 상세 규칙이 필요할 때만 읽습니다. MCP는 해당 작업에서만 on-demand로 활성화합니다.

knowledge profile은 전체 catalog나 vendor를 노출하지 않고 `safety, knowledge, archive, diagram` 4개만 설치합니다. private knowledge는 `repo://skills/skills/knowledge/...`를 참조하고 절대 사용자 경로를 commit하지 않습니다.

novel profile은 `safety, novel-handoff, novel-merge` 3개만 설치합니다. 소설 원문과 정본은 항상 private/local-only이며 스킬 원본은 `repo://skills/skills/novel/...`에만 둡니다. `$novel-handoff`는 맥락 prompt, `$novel-merge`는 정본 병합을 각각 소유하고 `$archive/$knowledge/$insight/$tech/$diagram`의 owner를 대체하지 않습니다.

## 이식성

repository path는 Woon registry가 `repo://<id>/...`로 해석합니다. Codex와 Claude는 같은 catalog·profile·스킬 정본을 사용하고 설치 대상만 OS 기본값 또는 machine-local `WOON_CODEX_SKILLS_HOME`, `WOON_CLAUDE_SKILLS_HOME`에서 정합니다. `installable: false` profile은 catalog·routing 평가 전용이며 `woon-core`가 target plan·install을 거부합니다.
