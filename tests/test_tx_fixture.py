from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals" / "fixtures" / "tx"
sys.path.insert(0, str(FIXTURE))
SPEC = importlib.util.spec_from_file_location(
    "tx_fixture_verify", FIXTURE / "verify.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_transaction_failure_matrix() -> None:
    assert MODULE.main() == 0
