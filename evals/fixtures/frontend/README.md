# Frontend integration fixture

`verify.sh`는 실제 Chromium에서 frontend 소유 경계의 최소 동작을 확인한다.

- semantic disabled와 event 차단
- 닫힌 navigation의 DOM·focus 노출 정합성
- 최신 async 결과 소유와 optimistic rollback
- form error association·focus
- deterministic initial theme와 modal focus 복귀
- stable list identity, duplicate submit 차단, business 결과 증거

이 fixture는 browser DOM 동작을 검증하지만 screen reader 조합, 실제 React concurrent rendering, 실제 결제 backend, 시각적 완성도와 production 환경을 증명하지 않는다. 해당 층은 프로젝트별 component test, `$ui-test`, `$e2e`와 production 관찰로 별도 검증한다.
