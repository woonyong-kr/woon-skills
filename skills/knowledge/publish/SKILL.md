---
name: publish
description: private woon-knowledge의 승인된 문서를 공개 WIKI·사이트용 산출물로 선별·변환·검증해 발행할 때 사용한다. 내부 저장에는 사용하지 않는다.
---

# Publish

private source와 public output을 분리한다. `publish:true` 같은 metadata는 repository 공개 권한이 아니다.

1. 사용자가 공개를 승인한 canonical document와 포함 범위를 확정한다.
2. secret, 개인정보, 회사 내부 자료, 비공개 link, source session ID를 검사한다.
3. public schema와 link rule에 맞게 deterministic output을 만든다.
4. build와 rendered link/navigation을 검증한다.
5. repository visibility, target branch, destination을 다시 확인한다.
6. deploy/push는 명시적 승인 뒤 수행하고 live artifact identity를 확인한다.

private repository 자체를 public으로 바꾸지 않는다.
