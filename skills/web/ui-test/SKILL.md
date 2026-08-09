---
name: ui-test
description: 웹 UI의 실제 render, responsive layout, interaction, focus, overflow, light·dark mode와 screenshot 회귀를 검수할 때 사용한다.
---

# UI Test

code와 build만 보지 말고 target route를 browser에서 연다. desktop/mobile viewport에서 first screen, content hierarchy, navigation, form states, overflow와 focus order를 확인한다.

변경 전후 screenshot은 같은 viewport·data·theme로 비교한다. 색상만으로 상태를 전달하지 않는지, text clipping과 keyboard trap이 없는지 확인한다. expected design이 있으면 spacing·type·layout 차이를 구체적으로 기록한다.

발견한 문제와 이미 수정한 문제를 구분하고 실제 click path를 함께 보고한다.

문제의 소유자를 구분한다. state·DOM·event lifecycle은 `$react`, cascade·layout·responsive style은 `$css`, 여러 화면과 backend 결과를 잇는 회귀 자동화는 `$e2e`가 수정한다. screenshot 유사도만으로 keyboard, accessibility tree, network side effect나 business 성공을 통과시키지 않는다.
