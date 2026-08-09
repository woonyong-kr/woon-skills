# 비-REST protocol 계약

## 선택

- gRPC: typed unary·streaming과 service-to-service deadline propagation이 필요할 때 검토한다.
- GraphQL: client가 다양한 read projection을 조합해야 할 때 검토하되 resolver fan-out·authorization·cost를 제한한다.
- WebSocket: 양방향 장기 연결과 낮은 latency가 필요할 때 사용하며 reconnect·resume를 별도 설계한다.
- SSE: server→client event stream과 HTTP 기반 reconnect가 충분할 때 사용한다.
- webhook: provider가 consumer endpoint로 비동기 결과를 보내야 할 때 서명·dedup·retry 계약을 둔다.

## 공통 계약

- schema field number/name 재사용, required 변경과 enum unknown 처리 등 protocol별 호환 규칙을 지킨다.
- deadline·cancellation을 전파하되 remote effect 취소로 오해하지 않는다.
- error는 stable machine code, safe message, retryability와 correlation을 제공한다.
- stream에는 ordering 단위, sequence, heartbeat, max message, flow control과 resume cursor를 둔다.
- client·server 모두 bounded buffer와 slow consumer 정책을 가진다.
- authentication handshake 뒤에도 message·field·object authorization을 검증한다.

## Protocol별 위험

- gRPC: deadline 기본 부재, status와 domain error 혼동, retry policy의 idempotency 조건을 확인한다.
- GraphQL: N+1, unbounded depth·complexity, field-level auth와 partial error를 검증한다.
- WebSocket: reconnect duplicate, session fixation, origin 검증과 backpressure를 확인한다.
- SSE: `Last-Event-ID`, replay retention과 proxy buffering을 확인한다.
- webhook: raw body signature, timestamp tolerance, key rotation, replay와 빠른 ack 뒤 durable processing을 검증한다.

## 검증

- 구 client↔신 server와 신 client↔구 server
- unknown field·enum과 removed/deprecated field
- mid-stream disconnect, reconnect, duplicate와 reorder
- slow consumer, oversized message와 auth revocation
- deadline 직전 server commit과 response loss
- webhook signature 변조·replay·out-of-order delivery
