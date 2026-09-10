---
name: ui-test
description: 웹 UI의 실제 render, responsive layout, interaction, focus, overflow, light·dark mode와 screenshot 회귀를 검수할 때 사용한다.
---

# UI Test

변경한 route·component를 target browser에서 열고 요청의 acceptance criteria에 해당하는 실제 동작을 확인한다. layout·responsive 변화는 관련 viewport, interaction 변화는 navigation·form state·focus, 공통 shell 변화는 영향받는 화면으로 범위를 넓힌다.

시각 차이를 검증할 때 변경 전후 screenshot은 같은 viewport·data·theme로 비교한다. 색상만으로 상태를 전달하지 않는지, text clipping과 keyboard trap이 없는지 확인한다. expected design이 있으면 spacing·type·layout 차이를 구체적으로 기록한다.

발견한 문제와 이미 수정한 문제를 구분하고 실제 click path를 함께 보고한다.

문제의 소유자를 구분한다. state·DOM·event lifecycle은 `$react`, cascade·layout·responsive style은 `$css`, 여러 화면과 backend 결과를 잇는 회귀 자동화는 `$e2e`가 수정한다. screenshot 유사도만으로 keyboard, accessibility tree, network side effect나 business 성공을 통과시키지 않는다.
