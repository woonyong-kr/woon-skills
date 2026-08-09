# CSS 품질 경계

요청에 해당하는 절만 적용한다. 기존 reset, token, browser target과 component ownership이 이 문서의 일반 예시보다 우선한다.

## Cascade와 reset

- selector를 늘리기 전에 cascade origin, layer, scope와 source order를 확인한다. 재사용 규칙은 낮은 specificity를 유지하고 `:where()`와 `:is()`를 같은 것으로 취급하지 않는다.
- `all: unset`은 거의 모든 property를 inherited 또는 initial 값으로 바꾼다. interactive element에 쓰면 display, typography, cursor와 focus를 포함해 필요한 state를 명시적으로 복원하고 keyboard 동작을 확인한다. component 하나를 초기화하려는 목적이면 `revert`·`revert-layer`나 좁은 property 목록을 먼저 검토한다.
- universal reset은 browser 기본의 유용한 margin·list·form state까지 지울 수 있다. 적용 범위를 문서화하고 heading, list, form, dialog와 third-party widget을 실제로 확인한다.

## 의미와 interaction

- 필수 text, separator, URL과 오류 설명을 `content`나 pseudo-element에만 두지 않는다. CSS generated content는 DOM과 accessibility tree에서 일관되게 제공되지 않으므로 의미 정보는 HTML에 둔다.
- `display: none`은 렌더와 accessibility tree를 숨길 뿐 media 재생·network·application state를 중단하는 명령이 아니다. 동작은 HTML attribute나 JavaScript state owner에서 멈춘다.
- `pointer-events: none`은 pointer hit testing만 바꾸며 keyboard focus나 disabled semantics를 만들지 않는다. native `disabled`, `aria-disabled`와 실제 event guard 중 상황에 맞는 계약을 구현한다.
- focus indicator를 제거하지 않는다. `:focus-visible`을 포함한 명확한 focus, keyboard 순서, hover가 없는 입력, reduced motion, forced colors와 충분한 contrast를 검증한다.

## Layout와 sizing

- 물리 방향 `left/right/top/bottom`보다 의미가 맞는 `inline/block` logical property를 우선하고 LTR·RTL 또는 vertical writing mode가 범위에 있으면 직접 확인한다.
- viewport 단위만으로 font size를 정하지 않는다. user font preference와 zoom을 보존하도록 하한·상한도 `px`가 아닌 relative unit으로 둔다. 예: `font-size: clamp(1rem, 0.875rem + 0.5vw, 1.25rem)`. `16px`·`20px`처럼 absolute bound를 제안하면서 `rem` 기반이라고 설명하지 말고, 200% zoom에서 clipping·overlap을 확인한다.
- mobile viewport 높이는 browser UI 변화가 있으므로 `vh`를 무조건 고정하지 않는다. content flow를 우선하고 필요한 경우 `svh`·`dvh`의 의미와 fallback을 target browser에서 확인한다.
- hover-only disclosure, 임의의 큰 `max-height`, 전역 `:empty`, replaced element의 pseudo-element처럼 환경 의존적인 trick은 핵심 동작으로 쓰지 않는다. keyboard·touch·dynamic content와 실패 상태가 있는 명시적 구현을 선택한다.

## 완료 조건

1. lint·build와 computed style에서 cascade 결과를 확인한다.
2. desktop·mobile, keyboard, 200% zoom, light·dark 및 지원 writing mode를 실제 render로 확인한다.
3. 변경 전후 screenshot은 같은 viewport·content·theme에서 비교한다.
4. 확인하지 못한 browser, assistive technology와 design 기준은 통과로 표현하지 않는다.
