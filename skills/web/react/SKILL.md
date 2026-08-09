---
name: react
description: React·Next.js component, hook, state, render 성능, accessibility와 frontend folder 구조를 작성·검토할 때 사용한다.
---

# React

현재 framework/version, router, state library, component convention을 먼저 읽는다. component는 page/feature가 소유한 곳에 두고 실제로 재사용되는 stable UI만 shared로 올린다.

state는 가장 가까운 owner에 두며 server state를 client global store에 복제하지 않는다. effect는 external synchronization에만 쓰고 derived state 계산에 쓰지 않는다. `useMemo`/`useCallback`은 identity contract나 측정된 bottleneck이 있을 때만 추가한다.

semantic HTML, keyboard, focus, label, loading/error/empty state를 구현하고 실제 render로 확인한다.

React는 component와 application state, semantic DOM, event·async lifecycle을 소유한다. CSS로 disabled·hidden·loading 상태를 대신 만들지 않는다. cascade와 layout은 `$css`, 실제 viewport·focus·visual 검수는 `$ui-test`, 여러 화면과 backend를 잇는 business journey는 `$e2e`에 맡기고 한 변경이 경계를 넘으면 해당 스킬을 함께 적용한다.
