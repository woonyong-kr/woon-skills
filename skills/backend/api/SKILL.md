---
name: api
description: HTTP·REST API resource, endpoint, request·response schema, error, pagination, idempotency와 versioning을 설계·검토할 때 사용한다.
---

# API

consumer task와 resource identity를 먼저 정의한다. method/status code를 의미에 맞게 쓰고 request validation은 boundary에서, authorization은 object access까지 확인한다.

schema는 required/optional/null을 구분하고 stable error code, human message, trace context를 제공한다. list는 deterministic order와 bounded pagination을 사용한다. retry 가능한 write는 idempotency contract를 설계한다.

breaking change는 version 또는 migration window를 명시하고 OpenAPI·implementation·contract test를 함께 갱신한다. internal model을 그대로 외부 schema로 노출하지 않는다.
