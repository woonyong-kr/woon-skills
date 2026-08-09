# 개인정보 lifecycle 기준

## Inventory와 최소화

- field별 subject, sensitivity, purpose, source, consumer, storage와 transfer를 기록한다.
- 목적에 필요하지 않은 field, raw payload와 장기 identifier를 수집하지 않는다.
- derived data·embedding·feature·support note도 원본 subject와 연결될 수 있으면 inventory에 포함한다.
- production data를 개발·test에 복사하지 않고 synthetic 또는 승인된 비식별 fixture를 사용한다.

## Access와 사용

- purpose, role, tenant, resource와 environment로 최소 권한을 적용한다.
- service·human support access를 분리하고 break-glass에 승인·만료·audit을 둔다.
- export·analytics·model 입력은 승인된 field allowlist와 destination을 사용한다.
- pseudonymization은 재식별 key와 access를 분리하며 anonymization으로 과장하지 않는다.

## Retention·delete·export

- data category별 retention 시작점, 기간, hold와 deletion owner를 정한다.
- 삭제는 primary DB뿐 아니라 cache, search, object, analytics, queue, log와 materialized copy를 추적한다.
- backup은 즉시 개별 삭제가 불가능할 수 있으므로 expiry, restore 뒤 re-delete 절차와 access 제한을 명시한다.
- soft delete는 product recovery state일 뿐 최종 삭제를 대체하지 않는다.
- export는 subject verification, scope, format, redaction과 delivery security를 검증한다.

## Audit와 검증

- audit은 actor, action, target, purpose/reason, decision, time와 integrity를 기록하되 민감 payload는 넣지 않는다.
- audit reader·retention과 tamper detection을 분리한다.
- 삭제·권한 회수 뒤 모든 projection에서 검색 불가한지 canary subject로 확인한다.
- 다른 tenant·subject의 export, support access, restore와 replay를 negative test한다.
- secret scanner만으로 개인정보 노출을 찾았다고 주장하지 않고 schema·flow·sample을 함께 감사한다.
