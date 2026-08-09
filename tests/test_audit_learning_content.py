from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_learning_content.py"
SPEC = importlib.util.spec_from_file_location("audit_learning_content", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
audit_learning_content = MODULE.audit_learning_content


class AuditLearningContentTest(unittest.TestCase):
    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "evals/quality").mkdir(parents=True)
        (root / "evals/behavior").mkdir(parents=True)
        (root / "evals/results").mkdir(parents=True)
        (root / "standards").mkdir(parents=True)
        shutil.copy(
            ROOT / "evals/quality/learning-content.yaml",
            root / "evals/quality/learning-content.yaml",
        )
        shutil.copy(
            ROOT / "evals/behavior/learning-content.yaml",
            root / "evals/behavior/learning-content.yaml",
        )
        shutil.copy(
            ROOT / "standards/learning-content-quality.md",
            root / "standards/learning-content-quality.md",
        )
        shutil.copy(
            ROOT / "evals/results/learning-content-2026-08-10.yaml",
            root / "evals/results/learning-content-2026-08-10.yaml",
        )
        return root

    def test_accepts_current_quality_contract(self) -> None:
        self.assertEqual(audit_learning_content(self.make_root()), [])

    def test_rejects_too_few_trials(self) -> None:
        root = self.make_root()
        path = root / "evals/quality/learning-content.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace("trials: 3", "trials: 1"),
            encoding="utf-8",
        )
        self.assertTrue(
            any("trials" in error for error in audit_learning_content(root))
        )

    def test_rejects_unknown_rubric_requirement(self) -> None:
        root = self.make_root()
        path = root / "evals/quality/learning-content.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "require: [problem_before_definition, runnable_example_and_output, causal_walkthrough]",
                "require: [unknown_rule]",
                1,
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("unknown rubric" in error for error in audit_learning_content(root))
        )

    def test_rejects_unknown_hard_fail_rule(self) -> None:
        root = self.make_root()
        path = root / "evals/quality/learning-content.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "forbid: [claimed_unrun_output_as_actual, invented_execution_result]",
                "forbid: [unknown_failure]",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("unknown hard-fail" in error for error in audit_learning_content(root))
        )

    def test_rejects_incomplete_candidate_repetitions(self) -> None:
        root = self.make_root()
        path = root / "evals/results/learning-content-2026-08-10.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "scores: [18, 18, 18]", "scores: [18, 18, 14]", 1
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("full-score passes" in error for error in audit_learning_content(root))
        )

    def test_rejects_unexplained_incomplete_hardening(self) -> None:
        root = self.make_root()
        path = root / "evals/results/learning-content-2026-08-10.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "status: blocked_by_external_rate_limit", "status: incomplete", 1
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any(
                "unknown usability hardening status" in error
                for error in audit_learning_content(root)
            )
        )


if __name__ == "__main__":
    unittest.main()
