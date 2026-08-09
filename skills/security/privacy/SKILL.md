---
name: privacy
description: backend·data system의 개인정보 분류, 최소 수집, consent, retention, export, 삭제, masking, audit와 log·analytics·backup 전파를 설계할 때 사용한다. 공개 문서 선별만에는 사용하지 않는다.
---

# Privacy

법률을 추측하지 말고 적용 관할·정책을 확인하면서 기술적 data lifecycle을 증명한다.

1. data field별 subject, sensitivity, purpose, lawful basis/consent, owner와 processor를 inventory한다.
2. [개인정보 lifecycle 기준](references/lifecycle.md)으로 수집→사용→공유→보존→export→삭제를 추적한다.
3. tenant 격리는 `$tenant`, access control은 `$auth`·`$security`, immutable audit signal은 `$observe`와 함께 설계한다.
4. production copy, log, cache, search, analytics, queue, backup과 support tool까지 deletion·redaction 범위를 검증한다.

`publish`, encryption 또는 soft delete 하나로 privacy를 충족했다고 주장하지 않는다. 결과에는 data map, retention·deletion contract, 접근·감사 경계와 확인한 정책·미확정 법률 사항을 구분한다.
