---
name: protocol
description: gRPC·GraphQL·WebSocket·Server-Sent Events·webhook 같은 비-REST backend protocol의 schema, deadline, streaming, error, compatibility, retry와 delivery 계약을 설계·검토할 때 사용한다.
---

# Protocol

기술 유행보다 interaction shape와 failure semantics로 protocol을 선택한다.

1. unary·query·subscription·bidirectional stream·server callback 중 실제 흐름을 정의한다.
2. [Protocol 기준](references/contracts.md)으로 schema evolution, deadline, cancellation, backpressure, auth와 error mapping을 정한다.
3. write retry·webhook dedup은 `$tx`, event stream은 `$event`, overload는 `$capacity`를 함께 적용한다.
4. old/new client·server 조합과 network interruption을 contract test로 검증한다.

transport 성공을 업무 성공으로 간주하지 않는다. 결과에는 protocol 선택 근거, compatibility matrix, delivery·ordering·resume와 security boundary를 포함한다.
