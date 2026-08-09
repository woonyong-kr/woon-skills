---
name: history
description: Git commit 이력 조사, bisect, reflog 복구, commit message 재작성, cherry-pick, revert처럼 history를 분석하거나 조작할 때 사용한다.
---

# History

먼저 `git status`, 현재 branch, HEAD SHA, upstream, 공유 여부를 확인한다.

- 원인 추적: `git log`, `git show`, `git blame`, 필요하면 검증 명령을 포함한 `git bisect`.
- 안전한 취소: 이미 공유된 변경은 기본적으로 `git revert`.
- 복구: `git reflog`에서 SHA를 확인하고 새 branch로 보존한 뒤 복구.
- 재작성: 로컬·개인 history라는 증거와 backup ref가 있을 때만 수행.

`reset --hard`, force push, 광범위 history rewrite는 사용자의 명시적 승인 없이 실행하지 않는다. 전후 commit graph와 blob 보존 여부를 확인한다.
