---
name: review
description: 코드 diff나 PR의 결함, 회귀, 보안·성능 위험, 테스트 누락을 근거와 우선순위로 검토해 달라는 요청에 사용한다. 직접 수정 요청에는 쓰지 않는다.
---

# Review

1. 변경 목표, base, diff, 저장소 규칙을 확인한다.
2. 변경된 줄이 만드는 실제 실행 경로와 실패 경계를 추적한다.
3. correctness, data loss, security, compatibility, concurrency, performance, missing test 순으로 찾는다.
4. 각 finding은 재현 조건, 영향, 파일과 최소 line range, 수정 방향을 포함한다.
5. 불확실한 우려는 finding이 아니라 질문이나 미확인 사항으로 분리한다.
6. 스타일 취향과 기존 코드 문제는 요청 범위 밖이면 finding으로 올리지 않는다.

중요도 높은 finding부터 제시하고, 없으면 없다고 명확히 말한다. review 요청만으로 코드를 바꾸지 않는다.
