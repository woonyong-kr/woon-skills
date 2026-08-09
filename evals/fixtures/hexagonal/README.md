# Hexagonal 실행 fixture

`$hexagonal`의 동일한 경계가 Python, Java와 TypeScript에서 실제로 compile·실행되는지 확인한다.

- application이 소유하는 `PaymentAuthorizer` port
- 외부 SDK 표현을 격리하는 `VendorPaymentAdapter`
- 같은 업무 의도에 같은 idempotency key를 전달하는 use case
- core unit과 adapter contract 성격의 실행 검증

```bash
./evals/fixtures/hexagonal/verify.sh
```

검증 script는 생성물을 임시 directory에 만들고 종료 시 제거한다. TypeScript compiler는 `tsc` 또는 `TSC_JS` 환경 변수로 지정한 compiler entrypoint가 필요하다.
