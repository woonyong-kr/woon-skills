---
name: budget
description: skills, agents, MCP, rules가 사용하는 context token을 측정하고 description·본문·reference·profile을 줄이면서 품질을 유지할 때 사용한다.
---

# Budget

profile별 항상 로드되는 이름·description과 실제 trigger 때 로드되는 SKILL body·reference를 분리해 측정한다.

1. character/token estimate와 active skill 수 baseline
2. 긴 description을 concrete trigger 180자 이내로 축약
3. 중복 설명을 제거하고 procedure만 main에 유지
4. 상세 표·예제는 관련 task에서만 읽는 reference로 이동
5. 같은 side effect와 trigger는 병합, 독립 trigger는 분리
6. MCP는 on-demand, toolset 최소화
7. routing recall·precision과 behavior eval이 유지되는지 재검증

token 감소만으로 성공이라 하지 않는다. 모호한 이름, 숨은 reference chain, 잦은 동시 activation이 늘면 되돌린다.
