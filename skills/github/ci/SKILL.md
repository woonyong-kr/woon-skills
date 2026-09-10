---
name: ci
description: GitHub Actions workflow, PR check, CI 실패를 조사·수정하거나 workflow 권한·cache·matrix를 검토할 때 사용한다.
---

# CI

실패 조사라면 run·job·step·commit SHA와 로그의 첫 원인을 식별한다. 로컬 재현이 원인 판단에 필요하고 CI 조건을 재현할 수 있을 때 같은 명령을 실행한다.

새 workflow나 수정은 변경한 syntax·permissions·secret 경계·runner·cache·matrix를 중심으로 검증한다. 관련 commit SHA·workflow·입력·환경이 같은 성공 run은 재사용한다. 새 run에 push가 필요하면 현재 작업의 권한과 대상 영향을 확인하고, 로컬 통과와 원격 run 결과를 구분한다.

외부 CI 공급자의 로그는 접근 가능한 URL만 보고하고 내용을 추정하지 않는다.
