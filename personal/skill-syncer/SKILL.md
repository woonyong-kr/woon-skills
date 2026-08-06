---
name: skill-syncer
description: Sync custom skills from the user's local skill workspace (/Users/woonyong/workspace/skills) into Claude or Codex so the latest local rules and scripts are available. Use this skill whenever the user says things like "스킬 동기화해줘", "스킬 업데이트해줘", "내 스킬 반영해줘", "새 스킬 적용해줘", or "sync my skills". Also trigger when the user mentions they've updated or created a skill in their workspace and wants those changes reflected in the active tools.
---

# Skill Syncer

사용자가 `/Users/woonyong/workspace/skills`에 만들거나 수정한 스킬을 Claude 또는 Codex의 스킬 디렉토리에 반영합니다.

## 동작 흐름

1. `scripts/sync_skills.py`를 실행해 소스 스킬을 대상 도구의 스킬 디렉토리에 복사합니다.
2. 결과(추가/업데이트/스킵된 스킬 목록)를 사용자에게 보고합니다.
3. 새 스킬 추가나 세션 재시작이 필요한 경우를 함께 안내합니다.

## 실행 방법

반드시 **Desktop Commander의 `start_process`** 를 사용해 Mac에서 직접 실행합니다.
Bash 도구(샌드박스 환경)로 실행하면 Claude 스킬 디렉토리를 찾지 못하므로 사용할 수 없습니다.

```bash
python3 /Users/woonyong/workspace/skills/skill-syncer/scripts/sync_skills.py --target all
```

실행 후 출력 결과를 읽어 사용자에게 요약해서 보고합니다.

특정 대상만 동기화하려면 `--target claude` 또는 `--target codex`를 사용합니다.

## 결과 보고 형식

스크립트 실행 결과를 아래 형식으로 정리해서 전달합니다:

```
[완료] claude 동기화
  대상:       /path/to/claude/skills
  추가됨     : [스킬명 목록]
  업데이트됨 : [스킬명 목록]
  변경 없음  : [스킬명 목록]

[완료] codex 동기화
  대상:       /path/to/.codex/skills
  추가됨     : [스킬명 목록]
  업데이트됨 : [스킬명 목록]
  변경 없음  : [스킬명 목록]

[안내] 새로 추가된 스킬은 도구에 따라 다음 세션부터 인식될 수 있습니다.
[안내] 기존 스킬 업데이트는 현재 세션에서 바로 반영될 수 있습니다.
```

## 주의사항

- Claude 대상은 활성 세션의 스킬 디렉토리를 자동으로 탐색합니다.
- Codex 대상은 `~/.codex/skills`를 사용하며 없으면 자동으로 생성합니다.
- 소스 디렉토리에 `skill-syncer` 폴더 자체도 있으면 함께 동기화됩니다(자기 자신 포함).
- 동기화는 단방향입니다(소스 → 대상 도구). 대상 쪽 변경은 소스에 반영되지 않습니다.
