# 테넌트 격리 기준

## Identity와 context

- authenticated principal의 membership·entitlement에서 tenant를 결정한다.
- route/header의 tenant ID는 요청 대상일 뿐 권한 증거가 아니다.
- async message·job에는 signed/validated tenant context를 명시적으로 전달한다.
- global admin·support impersonation은 별도 권한, reason, 시간 제한과 audit을 둔다.

## Isolation model

- pooled compute/data: 비용 효율이 높지만 모든 query·key·queue에서 논리 격리가 필요하다.
- separate schema/database: blast radius와 migration 비용의 trade-off를 측정한다.
- silo/deployment stamp: 높은 격리 대신 fleet 운영·비용·version drift를 관리한다.
- component마다 다른 model을 선택할 수 있으나 tenant placement의 정본과 routing을 하나로 둔다.

## Data와 resource

- shared table은 tenant column, composite unique/index와 필요 시 DB row-level policy를 적용한다.
- repository method가 tenant context 없이 조회·수정할 수 없게 API를 설계한다.
- cache·object key·search index·metric·log에 tenant namespace를 검증한다.
- queue·worker·connection·rate limit에 tenant fairness와 hard ceiling을 둔다.
- encryption key, backup, export·delete와 region placement 요구를 tenant policy에 연결한다.

## Migration과 검증

- tenant move는 source freeze/dual-read 여부, copy checksum, cutover version, rollback과 in-flight job 처리를 갖춘다.
- 다른 tenant의 같은 resource ID를 모든 read/write API에 주입한다.
- cache warmup, async redelivery, batch·admin endpoint와 export에서 cross-tenant leak을 검사한다.
- 한 tenant의 burst·poison job·large query가 다른 tenant latency와 availability에 미치는 영향을 측정한다.
- backup restore와 analytics projection에서도 tenant 경계가 유지되는지 확인한다.
