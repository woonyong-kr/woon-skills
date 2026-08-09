---
name: react
description: React·Next.js component, hook, state, render 성능, accessibility와 frontend folder 구조를 작성·검토할 때 사용한다.
---

# React

현재 framework/version, router, state library, component convention을 먼저 읽는다. component는 page/feature가 소유한 곳에 두고 실제로 재사용되는 stable UI만 shared로 올린다.

state는 가장 가까운 owner에 두며 server state를 client global store에 복제하지 않는다. effect는 external synchronization에만 쓰고 derived state 계산에 쓰지 않는다. `useMemo`/`useCallback`은 identity contract나 측정된 bottleneck이 있을 때만 추가한다.

semantic HTML, keyboard, focus, label과 UI state를 실제 render로 확인한다. 닫힌 modal·drawer는 unmount하거나 `hidden`·`inert`로 focus를 막고 CSS만으로 숨기지 않는다.

정적 진단 때만 [계약](references/static-analysis.md)을 읽고 점수로 완료를 판정하지 않는다.

React는 state·semantic DOM·event·async lifecycle을 소유하고 CSS로 상태를 대신하지 않는다. cascade·layout은 `$css`, 실제 viewport·focus·visual은 `$ui-test`, 화면과 backend를 잇는 journey는 `$e2e`에 맡기며 경계를 넘으면 함께 쓴다.
