---
name: migration
description: database schema·data migration을 expand/contract, backfill, rollback, compatibility와 배포 순서까지 안전하게 설계·검증할 때 사용한다.
---

# Migration

현재 schema, row count, traffic, lock 특성, application compatibility를 확인한다. production 변경은 expand→dual compatible code→bounded backfill→verify→contract 순으로 나눈다.

DDL lock, index build, null/default rewrite, foreign key validation, replication lag를 DB version에 맞게 확인한다. backfill은 resumable·idempotent하고 batch size는 측정해 제한한다. rollback이 data loss를 복구하지 못하면 roll-forward 전략을 명시한다.

dry-run/staging, counts/checksum, application metric과 rollback trigger를 정의하고 승인 없이 production apply하지 않는다.
