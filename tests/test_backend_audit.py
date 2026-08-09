from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_backend.py"
SPEC = importlib.util.spec_from_file_location("audit_backend", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_backend_contract_is_complete() -> None:
    assert MODULE.audit_backend(ROOT) == []
