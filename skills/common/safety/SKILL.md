---
name: safety
description: 삭제, 덮어쓰기, Git history 재작성, force push, 배포, 운영 변경처럼 복구가 어렵거나 외부에 영향이 있는 작업 전에 사용한다.
---

# Safety

1. 요청이 해당 효과를 명시적으로 허용하는지 확인한다.
2. read-only 명령으로 정확한 대상, 범위, 현재 상태를 확정한다.
3. broad path, unresolved variable, glob을 destructive target으로 쓰지 않는다.
4. backup, branch, trash, dry-run처럼 가장 쉽게 복구할 방법을 우선한다.
5. account 생성, OAuth grant, token 발급, publish는 별도 권한 없이는 멈춘다.
6. 실행 뒤 대상과 영향, 복구 가능 여부를 다시 확인한다.

승인이 필요하면 수행할 명령과 되돌리는 방법을 함께 제시한다. 진단만 요청받았으면 수정하지 않는다.
