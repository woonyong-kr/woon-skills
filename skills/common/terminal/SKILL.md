---
name: terminal
description: 명령 실행, 저장소 상태 확인, 로그 수집, 좁은 진단과 안전한 수정이 필요한 터미널 작업에 사용한다. 커밋·배포 같은 외부 효과는 별도 승인을 따른다.
---

# Terminal

1. 실제 작업 경로와 저장소 상태를 먼저 확인한다.
2. 검색은 `rg`와 `rg --files`를 우선하고, 출력은 판단에 필요한 범위로 제한한다.
3. 진단 명령과 변경 명령을 분리한다. 실패하면 exit code와 stderr를 보존한다.
4. 사용자 입력·경로·secret을 shell 문자열 보간에 넣지 않는다.
5. dirty worktree에서는 관련 없는 변경을 건드리지 않는다.
6. 삭제·history rewrite·force push·deploy 전에는 정확한 대상과 복구 경로를 확인한다.
7. 실행한 명령, 결과, 미실행 계층을 구분해 보고한다.

같은 실패를 추측으로 반복하지 말고 경로, runtime, dependency, 권한, 입력을 하나씩 좁힌다.
