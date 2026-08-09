# CSS browser fixture

`$css`가 구분하는 cascade와 semantic 경계를 실제 Chromium computed style과 DOM에서 확인한다.

- `:is()`는 가장 강한 인자의 specificity를 사용한다.
- `:where()`는 specificity를 추가하지 않는다.
- `all: unset`은 button의 display도 초기화한다.
- `pointer-events: none`은 disabled semantics를 만들지 않는다.
- generated content는 DOM text의 정본이 아니다.

```bash
./evals/fixtures/css/verify.sh
```

이 fixture는 CSS의 browser behavior만 검증한다. screen reader 조합, media network 중단과 200% zoom의 실제 화면 품질은 별도 UI 검증이 필요하다.
