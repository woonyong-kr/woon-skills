#!/usr/bin/env python3
"""Run deterministic failure and mutation checks for the tx skill."""

from __future__ import annotations

import json
import tempfile
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path

from model import (
    InjectedFailure,
    PayloadConflict,
    ResponseLost,
    audit_provider_invariants,
    audit_invariants,
    claim_job,
    connect,
    consume,
    execute_payment,
    initialize,
    initialize_provider,
    provider_charge,
    reconcile_remote,
    relay_once,
    start_remote_workflow,
    unsafe_orphan_effect,
    unsafe_split_claim,
    write_fenced,
)


def scalar(path: Path, query: str) -> int:
    with closing(connect(path)) as connection:
        return int(connection.execute(query).fetchone()[0])


def fresh(root: Path, name: str) -> Path:
    path = root / f"{name}.sqlite3"
    initialize(path)
    return path


def test_atomic_rollback(root: Path) -> None:
    for failure in ("after_claim", "after_mutation", "before_commit"):
        path = fresh(root, f"rollback-{failure}")
        try:
            execute_payment(
                path,
                "tenant-a",
                "key-1",
                {"intent_id": "pay-1", "amount": "1000"},
                fail_at=failure,
            )
        except InjectedFailure:
            pass
        else:
            raise AssertionError(f"{failure} did not interrupt the transaction")
        assert scalar(path, "SELECT COUNT(*) FROM idempotency") == 0
        assert scalar(path, "SELECT COUNT(*) FROM effects") == 0
        assert scalar(path, "SELECT COUNT(*) FROM outbox") == 0


def test_response_loss_replay(root: Path) -> None:
    path = fresh(root, "response-loss")
    payload = {"intent_id": "pay-2", "amount": "2000"}
    try:
        execute_payment(path, "tenant-a", "key-2", payload, fail_at="after_commit")
    except ResponseLost:
        pass
    else:
        raise AssertionError("response-loss point did not run")
    replay = execute_payment(path, "tenant-a", "key-2", payload)
    assert replay == {"intent_id": "pay-2", "status": "accepted"}
    assert scalar(path, "SELECT COUNT(*) FROM effects") == 1
    assert audit_invariants(path) == []


def test_payload_conflict(root: Path) -> None:
    path = fresh(root, "payload-conflict")
    execute_payment(path, "tenant-a", "key-3", {"intent_id": "pay-3", "amount": "3000"})
    try:
        execute_payment(
            path, "tenant-a", "key-3", {"intent_id": "pay-3", "amount": "9999"}
        )
    except PayloadConflict:
        pass
    else:
        raise AssertionError("same key with different payload was accepted")
    assert scalar(path, "SELECT COUNT(*) FROM effects") == 1


def test_concurrent_duplicate(root: Path) -> None:
    path = fresh(root, "concurrent")
    payload = {"intent_id": "pay-4", "amount": "4000"}

    def invoke(_: int) -> dict[str, str]:
        return execute_payment(path, "tenant-a", "key-4", payload)

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(invoke, range(8)))
    assert all(result == results[0] for result in results)
    assert scalar(path, "SELECT COUNT(*) FROM effects") == 1
    assert scalar(path, "SELECT COUNT(*) FROM outbox") == 1
    assert audit_invariants(path) == []


def test_outbox_redelivery(root: Path) -> None:
    path = fresh(root, "outbox")
    execute_payment(path, "tenant-a", "key-5", {"intent_id": "pay-5", "amount": "5000"})
    broker: list[dict[str, str]] = []
    try:
        relay_once(path, broker, fail_after_publish=True)
    except InjectedFailure:
        pass
    else:
        raise AssertionError("relay crash point did not run")
    assert relay_once(path, broker, fail_after_publish=False)
    assert len(broker) == 2
    consumed = [consume(path, "ledger", event) for event in broker]
    assert consumed == [True, False]
    assert scalar(path, "SELECT COUNT(*) FROM consumer_effects") == 1


def test_fencing(root: Path) -> None:
    path = fresh(root, "fencing")
    fence_a = claim_job(path, "job-1", "worker-a")
    fence_b = claim_job(path, "job-1", "worker-b")
    assert fence_b > fence_a
    assert write_fenced(path, "job-1", fence_b, "new")
    assert not write_fenced(path, "job-1", fence_a, "stale")
    with closing(connect(path)) as connection:
        row = connection.execute(
            "SELECT fence, value FROM fenced_resource WHERE job_id = 'job-1'"
        ).fetchone()
    assert int(row["fence"]) == fence_b
    assert row["value"] == "new"


def test_remote_unknown_reconciliation(root: Path) -> None:
    local_path = fresh(root, "remote-local")
    provider_path = root / "remote-provider.sqlite3"
    initialize_provider(provider_path)
    payload = {"intent_id": "pay-remote", "amount": "9000"}
    provider_key = "provider-key-1"
    start_remote_workflow(local_path, "pay-remote", provider_key)

    try:
        provider_charge(provider_path, provider_key, payload, lose_response=True)
    except ResponseLost:
        pass
    else:
        raise AssertionError("provider response-loss point did not run")

    with closing(connect(local_path)) as connection:
        status = connection.execute(
            "SELECT status FROM remote_workflows WHERE intent_id = 'pay-remote'"
        ).fetchone()[0]
    assert status == "unknown"

    replay = provider_charge(provider_path, provider_key, payload)
    assert replay == {
        "charge_id": "charge:provider-key-1",
        "intent_id": "pay-remote",
    }
    assert scalar(provider_path, "SELECT COUNT(*) FROM provider_charges") == 1

    try:
        reconcile_remote(
            local_path, provider_path, "pay-remote", fail_before_commit=True
        )
    except InjectedFailure:
        pass
    else:
        raise AssertionError("local reconciliation crash point did not run")

    with closing(connect(local_path)) as connection:
        status = connection.execute(
            "SELECT status FROM remote_workflows WHERE intent_id = 'pay-remote'"
        ).fetchone()[0]
    assert status == "unknown"

    assert reconcile_remote(local_path, provider_path, "pay-remote")
    assert reconcile_remote(local_path, provider_path, "pay-remote")
    assert scalar(local_path, "SELECT COUNT(*) FROM outbox") == 1
    assert audit_invariants(local_path) == []
    assert audit_provider_invariants(provider_path) == []


def assert_mutant_detected(
    root: Path, name: str, mutate: Callable[[Path], None], expected: str
) -> None:
    path = fresh(root, name)
    mutate(path)
    errors = audit_invariants(path)
    if expected not in errors:
        raise AssertionError(f"mutant {name} escaped: {errors}")


def test_mutants(root: Path) -> None:
    payload = {"intent_id": "pay-mutant", "amount": "7000"}
    assert_mutant_detected(
        root,
        "split-claim",
        lambda path: unsafe_split_claim(path, "tenant-a", "key-a", payload),
        "stuck processing idempotency record",
    )
    assert_mutant_detected(
        root,
        "orphan-effect",
        lambda path: unsafe_orphan_effect(
            path, "tenant-a", "key-b", "pay-mutant-orphan"
        ),
        "business effect exists without a succeeded request",
    )

    path = fresh(root, "new-key-per-retry")
    execute_payment(path, "tenant-a", "attempt-1", payload)
    execute_payment(path, "tenant-a", "attempt-2", payload)
    errors = audit_invariants(path)
    assert "one business intent produced duplicate effects" in errors

    provider_path = root / "provider-new-key-mutant.sqlite3"
    initialize_provider(provider_path)
    provider_charge(provider_path, "attempt-1", payload)
    provider_charge(provider_path, "attempt-2", payload)
    assert "one remote intent produced duplicate provider effects" in (
        audit_provider_invariants(provider_path)
    )


def main() -> int:
    tests = [
        test_atomic_rollback,
        test_response_loss_replay,
        test_payload_conflict,
        test_concurrent_duplicate,
        test_outbox_redelivery,
        test_fencing,
        test_remote_unknown_reconciliation,
        test_mutants,
    ]
    with tempfile.TemporaryDirectory(prefix="woon-tx-") as directory:
        root = Path(directory)
        for test in tests:
            test(root)
    print(json.dumps({"status": "ok", "checks": len(tests)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
