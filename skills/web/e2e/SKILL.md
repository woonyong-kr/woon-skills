---
name: e2e
description: Playwright 기반 end-to-end 사용자 흐름, browser regression, flaky selector와 실제 navigation·form·auth 동작을 검증할 때 사용한다.
---

# E2E

business-critical journey와 acceptance criteria를 먼저 정한다. role/label/text 같은 user-facing locator를 우선하고 CSS 구조와 arbitrary timeout에 의존하지 않는다.

test는 독립된 data와 session을 사용하고 외부 서비스는 contract가 아닌 경우 통제한다. assertion 전에 행동 결과를 observable UI/URL/network state로 기다린다. 실패 시 trace, screenshot, console, request evidence를 수집한다.

local E2E 성공을 production 성공으로 표현하지 않는다. visual 세부 검수는 `$ui-test`를 함께 쓴다.
