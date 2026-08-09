"""Deterministic transaction and idempotency reference fixture."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Optional


class PayloadConflict(RuntimeError):
    """The same idempotency key was reused for a different intent payload."""


class ResponseLost(RuntimeError):
    """The local commit succeeded, but the caller did not receive the response."""


class InjectedFailure(RuntimeError):
    """A deterministic crash point interrupted the operation."""


class ProviderPayloadConflict(RuntimeError):
    """A provider key was reused for a different remote effect."""


def canonical_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(str(path), timeout=5, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 5000")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize(path: Path) -> None:
    with connect(path) as connection:
        connection.executescript(
            """
            PRAGMA journal_mode = WAL;
            CREATE TABLE idempotency (
                scope TEXT NOT NULL,
                key TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('processing', 'succeeded')),
                result_json TEXT,
                PRIMARY KEY (scope, key)
            );
            CREATE TABLE effects (
                effect_id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_intent TEXT NOT NULL,
                scope TEXT NOT NULL,
                key TEXT NOT NULL
            );
            CREATE TABLE outbox (
                event_id TEXT PRIMARY KEY,
                business_intent TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                sent INTEGER NOT NULL DEFAULT 0 CHECK (sent IN (0, 1))
            );
            CREATE TABLE inbox (
                consumer TEXT NOT NULL,
                event_id TEXT NOT NULL,
                PRIMARY KEY (consumer, event_id)
            );
            CREATE TABLE consumer_effects (
                consumer TEXT NOT NULL,
                business_intent TEXT NOT NULL,
                PRIMARY KEY (consumer, business_intent)
            );
            CREATE TABLE job_claims (
                job_id TEXT PRIMARY KEY,
                owner TEXT NOT NULL,
                fence INTEGER NOT NULL
            );
            CREATE TABLE fenced_resource (
                job_id TEXT PRIMARY KEY,
                fence INTEGER NOT NULL,
                value TEXT NOT NULL
            );
            CREATE TABLE remote_workflows (
                intent_id TEXT PRIMARY KEY,
                provider_key TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL CHECK (status IN ('unknown', 'succeeded')),
                charge_id TEXT
            );
            """
        )


def initialize_provider(path: Path) -> None:
    with connect(path) as connection:
        connection.executescript(
            """
            PRAGMA journal_mode = WAL;
            CREATE TABLE provider_charges (
                provider_key TEXT PRIMARY KEY,
                intent_id TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                charge_id TEXT NOT NULL
            );
            """
        )


def execute_payment(
    path: Path,
    scope: str,
    key: str,
    payload: dict[str, Any],
    fail_at: Optional[str] = None,  # noqa: UP045 - Python 3.9 compatibility
) -> dict[str, Any]:
    digest = canonical_digest(payload)
    business_intent = str(payload["intent_id"])
    connection = connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        existing = connection.execute(
            "SELECT payload_digest, status, result_json "
            "FROM idempotency WHERE scope = ? AND key = ?",
            (scope, key),
        ).fetchone()
        if existing is not None:
            if existing["payload_digest"] != digest:
                connection.execute("ROLLBACK")
                raise PayloadConflict(key)
            if existing["status"] != "succeeded":
                connection.execute("ROLLBACK")
                raise RuntimeError("request is still processing")
            result = json.loads(str(existing["result_json"]))
            connection.execute("COMMIT")
            return result

        connection.execute(
            "INSERT INTO idempotency(scope, key, payload_digest, status) "
            "VALUES (?, ?, ?, 'processing')",
            (scope, key, digest),
        )
        if fail_at == "after_claim":
            raise InjectedFailure(fail_at)

        connection.execute(
            "INSERT INTO effects(business_intent, scope, key) VALUES (?, ?, ?)",
            (business_intent, scope, key),
        )
        if fail_at == "after_mutation":
            raise InjectedFailure(fail_at)

        result = {"intent_id": business_intent, "status": "accepted"}
        result_json = json.dumps(result, ensure_ascii=False, sort_keys=True)
        connection.execute(
            "UPDATE idempotency SET status = 'succeeded', result_json = ? "
            "WHERE scope = ? AND key = ? AND status = 'processing'",
            (result_json, scope, key),
        )
        connection.execute(
            "INSERT INTO outbox(event_id, business_intent, payload_json) "
            "VALUES (?, ?, ?)",
            (f"payment:{scope}:{key}", business_intent, result_json),
        )
        if fail_at == "before_commit":
            raise InjectedFailure(fail_at)
        connection.execute("COMMIT")
        if fail_at == "after_commit":
            raise ResponseLost(key)
        return result
    except (InjectedFailure, sqlite3.Error):
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def relay_once(
    path: Path, broker: list[dict[str, str]], fail_after_publish: bool
) -> bool:
    connection = connect(path)
    try:
        row = connection.execute(
            "SELECT event_id, business_intent, payload_json "
            "FROM outbox WHERE sent = 0 ORDER BY event_id LIMIT 1"
        ).fetchone()
        if row is None:
            return False
        event = {
            "event_id": str(row["event_id"]),
            "business_intent": str(row["business_intent"]),
            "payload_json": str(row["payload_json"]),
        }
        broker.append(event)
        if fail_after_publish:
            raise InjectedFailure("after_publish")
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "UPDATE outbox SET sent = 1 WHERE event_id = ?", (event["event_id"],)
        )
        connection.execute("COMMIT")
        return True
    finally:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        connection.close()


def consume(path: Path, consumer: str, event: dict[str, str]) -> bool:
    connection = connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.execute(
                "INSERT INTO inbox(consumer, event_id) VALUES (?, ?)",
                (consumer, event["event_id"]),
            )
        except sqlite3.IntegrityError:
            connection.execute("ROLLBACK")
            return False
        connection.execute(
            "INSERT INTO consumer_effects(consumer, business_intent) VALUES (?, ?)",
            (consumer, event["business_intent"]),
        )
        connection.execute("COMMIT")
        return True
    finally:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        connection.close()


def claim_job(path: Path, job_id: str, owner: str) -> int:
    connection = connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT fence FROM job_claims WHERE job_id = ?", (job_id,)
        ).fetchone()
        fence = 1 if row is None else int(row["fence"]) + 1
        connection.execute(
            "INSERT INTO job_claims(job_id, owner, fence) VALUES (?, ?, ?) "
            "ON CONFLICT(job_id) DO UPDATE SET owner = excluded.owner, "
            "fence = excluded.fence",
            (job_id, owner, fence),
        )
        connection.execute("COMMIT")
        return fence
    finally:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        connection.close()


def write_fenced(path: Path, job_id: str, fence: int, value: str) -> bool:
    connection = connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        cursor = connection.execute(
            "INSERT INTO fenced_resource(job_id, fence, value) VALUES (?, ?, ?) "
            "ON CONFLICT(job_id) DO UPDATE SET fence = excluded.fence, "
            "value = excluded.value "
            "WHERE excluded.fence >= fenced_resource.fence",
            (job_id, fence, value),
        )
        connection.execute("COMMIT")
        return cursor.rowcount == 1
    finally:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        connection.close()


def start_remote_workflow(path: Path, intent_id: str, provider_key: str) -> None:
    """Persist local intent before calling a non-transactional provider."""
    with connect(path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT INTO remote_workflows(intent_id, provider_key, status) "
            "VALUES (?, ?, 'unknown')",
            (intent_id, provider_key),
        )
        connection.execute("COMMIT")


def provider_charge(
    path: Path,
    provider_key: str,
    payload: dict[str, Any],
    lose_response: bool = False,
) -> dict[str, str]:
    """Apply one remote effect per provider key and optionally lose its response."""
    digest = canonical_digest(payload)
    intent_id = str(payload["intent_id"])
    connection = connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        existing = connection.execute(
            "SELECT intent_id, payload_digest, charge_id "
            "FROM provider_charges WHERE provider_key = ?",
            (provider_key,),
        ).fetchone()
        if existing is not None:
            if existing["payload_digest"] != digest:
                connection.execute("ROLLBACK")
                raise ProviderPayloadConflict(provider_key)
            result = {
                "charge_id": str(existing["charge_id"]),
                "intent_id": str(existing["intent_id"]),
            }
            connection.execute("COMMIT")
            return result

        charge_id = f"charge:{provider_key}"
        connection.execute(
            "INSERT INTO provider_charges"
            "(provider_key, intent_id, payload_digest, charge_id) VALUES (?, ?, ?, ?)",
            (provider_key, intent_id, digest, charge_id),
        )
        connection.execute("COMMIT")
        if lose_response:
            raise ResponseLost(provider_key)
        return {"charge_id": charge_id, "intent_id": intent_id}
    except sqlite3.Error:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def reconcile_remote(
    local_path: Path,
    provider_path: Path,
    intent_id: str,
    fail_before_commit: bool = False,
) -> bool:
    """Resolve an unknown local workflow by querying the provider by stable key."""
    with connect(local_path) as local:
        workflow = local.execute(
            "SELECT provider_key, status FROM remote_workflows WHERE intent_id = ?",
            (intent_id,),
        ).fetchone()
    if workflow is None:
        raise KeyError(intent_id)
    if workflow["status"] == "succeeded":
        return True

    with connect(provider_path) as provider:
        charge = provider.execute(
            "SELECT charge_id FROM provider_charges WHERE provider_key = ?",
            (workflow["provider_key"],),
        ).fetchone()
    if charge is None:
        return False

    connection = connect(local_path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "UPDATE remote_workflows SET status = 'succeeded', charge_id = ? "
            "WHERE intent_id = ? AND status = 'unknown'",
            (charge["charge_id"], intent_id),
        )
        connection.execute(
            "INSERT INTO outbox(event_id, business_intent, payload_json) "
            "VALUES (?, ?, ?) ON CONFLICT(event_id) DO NOTHING",
            (
                f"remote:{intent_id}",
                intent_id,
                json.dumps(
                    {"charge_id": charge["charge_id"], "intent_id": intent_id},
                    ensure_ascii=False,
                    sort_keys=True,
                ),
            ),
        )
        if fail_before_commit:
            raise InjectedFailure("remote_result_before_commit")
        connection.execute("COMMIT")
        return True
    except (InjectedFailure, sqlite3.Error):
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def audit_provider_invariants(path: Path) -> list[str]:
    errors: list[str] = []
    with connect(path) as connection:
        duplicates = connection.execute(
            "SELECT COUNT(*) FROM ("
            "SELECT intent_id FROM provider_charges "
            "GROUP BY intent_id HAVING COUNT(*) > 1"
            ")"
        ).fetchone()[0]
        if duplicates:
            errors.append("one remote intent produced duplicate provider effects")
    return errors


def audit_invariants(path: Path) -> list[str]:
    errors: list[str] = []
    with connect(path) as connection:
        processing = connection.execute(
            "SELECT COUNT(*) FROM idempotency WHERE status = 'processing'"
        ).fetchone()[0]
        if processing:
            errors.append("stuck processing idempotency record")

        orphan_effects = connection.execute(
            """
            SELECT COUNT(*)
            FROM effects e
            LEFT JOIN idempotency i ON i.scope = e.scope AND i.key = e.key
            WHERE i.status IS NULL OR i.status != 'succeeded'
            """
        ).fetchone()[0]
        if orphan_effects:
            errors.append("business effect exists without a succeeded request")

        duplicates = connection.execute(
            "SELECT COUNT(*) FROM ("
            "SELECT business_intent FROM effects GROUP BY business_intent HAVING COUNT(*) > 1"
            ")"
        ).fetchone()[0]
        if duplicates:
            errors.append("one business intent produced duplicate effects")

        missing_outbox = connection.execute(
            """
            SELECT COUNT(*)
            FROM effects e
            LEFT JOIN outbox o ON o.business_intent = e.business_intent
            WHERE o.event_id IS NULL
            """
        ).fetchone()[0]
        if missing_outbox:
            errors.append("committed business effect has no outbox event")

        missing_remote_outbox = connection.execute(
            """
            SELECT COUNT(*)
            FROM remote_workflows w
            LEFT JOIN outbox o ON o.event_id = 'remote:' || w.intent_id
            WHERE w.status = 'succeeded' AND o.event_id IS NULL
            """
        ).fetchone()[0]
        if missing_remote_outbox:
            errors.append("succeeded remote workflow has no outbox event")
    return errors


def unsafe_split_claim(
    path: Path, scope: str, key: str, payload: dict[str, Any]
) -> None:
    """Known mutant: persist the claim in a separate transaction."""
    with connect(path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT INTO idempotency(scope, key, payload_digest, status) "
            "VALUES (?, ?, ?, 'processing')",
            (scope, key, canonical_digest(payload)),
        )
        connection.execute("COMMIT")


def unsafe_orphan_effect(path: Path, scope: str, key: str, intent_id: str) -> None:
    """Known mutant: commit the mutation without its idempotency result."""
    with connect(path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT INTO effects(business_intent, scope, key) VALUES (?, ?, ?)",
            (intent_id, scope, key),
        )
        connection.execute("COMMIT")
