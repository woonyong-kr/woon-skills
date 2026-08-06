#!/bin/bash
# setup-skills.sh
# 현재 프로젝트의 .claude/skills/ 에 모든 스킬 symlink를 설정합니다.
# 사용법: bash /Users/woonyong/workspace/skills/setup-skills.sh [프로젝트_경로]

SKILLS_SRC="/Users/woonyong/workspace/skills"
PROJECT="${1:-$(pwd)}"
SKILLS_DST="$PROJECT/.claude/skills"

echo "🔗 스킬 symlink 설정 중..."
echo "   소스: $SKILLS_SRC"
echo "   대상: $SKILLS_DST"
echo ""

mkdir -p "$SKILLS_DST"

count=0
for skill_dir in "$SKILLS_SRC"/*/; do
  skill=$(basename "$skill_dir")
  if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
    ln -sfn "$skill_dir" "$SKILLS_DST/$skill"
    count=$((count + 1))
  fi
done

echo "✅ 총 $count 개 스킬 symlink 완료 → $SKILLS_DST"
