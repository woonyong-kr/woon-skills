---
name: pr
description: GitHub Pull Request를 조회·작성·검토·수정·병합하거나 review comment를 처리할 때 사용한다. 일반 Git 커밋에는 사용하지 않는다.
---

# PR

1. 저장소, base/head, diff, CI, PR template과 기존 convention을 확인한다.
2. 제목은 실제 변경 결과를 요약하고 본문은 문제·해결·검증·한계를 담는다.
3. 변경 내용과 근거 없는 주장, 실행하지 않은 테스트를 넣지 않는다.
4. 생성·수정·comment·merge 전 대상 PR과 외부 효과를 명확히 한다.
5. review feedback은 actionable 여부와 현재 코드 적용 가능성을 확인한 뒤 좁게 처리한다.
6. merge는 required checks와 approval, 저장소 merge policy를 확인한다.

가능하면 `gh pr view|diff|checks`로 읽고 `gh pr create|edit|comment|merge`로 명시된 작업만 수행한다. 요청 없이 push하거나 merge하지 않는다.
