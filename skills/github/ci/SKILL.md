---
name: ci
description: GitHub Actions workflow, PR check, CI 실패를 조사·수정하거나 workflow 권한·cache·matrix를 검토할 때 사용한다.
---

# CI

1. 실패한 run, job, step, commit SHA를 정확히 식별한다.
2. 로그의 첫 원인과 뒤따른 증상을 분리하고 로컬에서 같은 명령을 재현한다.
3. workflow syntax, permissions, secrets 경계, runner OS, cache key, matrix 차이를 확인한다.
4. 최소 수정 뒤 YAML validation과 관련 테스트를 실행한다.
5. 새 run은 push가 필요하면 먼저 알리고, 기존 성공 run을 현재 증거로 쓰지 않는다.

외부 CI 공급자의 로그는 접근 가능한 URL만 보고하고 내용을 추정하지 않는다.
