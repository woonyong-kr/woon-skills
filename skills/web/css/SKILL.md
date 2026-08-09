---
name: css
description: CSS cascade·specificity·selector, reset, layout, responsive sizing, logical property와 interaction style을 작성·검토·정리할 때 사용한다. React state나 실제 화면 검수에는 각각 react·ui-test를 쓴다.
---

# CSS

현재 styling stack, browser target, design token, reset과 component 경계를 먼저 읽는다. normal flow를 기본으로 두고 layout은 Grid·Flexbox, 방향은 logical property, 비율은 `aspect-ratio`처럼 의도가 드러나는 기능을 우선한다.

cascade layer와 낮은 specificity로 override 경로를 예측 가능하게 만든다. `:is()`는 가장 강한 인자의 specificity를 취하고 `:where()`는 0임을 구분한다. 전역 reset과 `!important`는 영향 범위와 대안을 확인한다.

CSS는 semantic HTML이나 실제 state 전환을 대신하지 않는다. focus, keyboard, zoom, reduced motion, contrast와 loading·disabled·hidden 상태를 보존한다. global reset, generated content, visibility, responsive type 또는 interaction을 바꾸면 [품질 경계](references/quality.md)를 읽는다.

문법·build만으로 끝내지 말고 target browser의 desktop·mobile, keyboard, 200% zoom과 필요한 writing mode에서 실제 render를 확인한다. 시각 회귀는 `$ui-test`, React component 경계는 `$react`를 함께 쓴다.
