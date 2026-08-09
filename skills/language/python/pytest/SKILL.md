---
name: pytest
description: Python pytest unit·integration test, fixture, parametrization, monkeypatch, async test를 작성·진단·정리할 때 사용한다.
---

# Pytest

행동과 failure boundary를 먼저 정하고 test name을 `test_<behavior>_<condition>`으로 쓴다. Arrange–Act–Assert를 짧게 유지하며 여러 조건은 `parametrize`하되 실패 의미가 흐려지면 분리한다.

fixture는 reusable lifecycle 또는 expensive setup에만 쓰고 숨은 autouse state를 피한다. I/O boundary는 `tmp_path`, `monkeypatch`, fake adapter로 격리하며 domain logic까지 mock하지 않는다. exception은 type과 중요한 message/context를 확인한다.

bug fix는 재현 test가 먼저 실패하는지 확인하고 수정 뒤 관련 test, full relevant suite, coverage requirement를 실행한다. arbitrary sleep과 test order 의존을 만들지 않는다.
