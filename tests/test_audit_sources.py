from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_sources.py"
SPEC = importlib.util.spec_from_file_location("audit_sources", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
audit_sources = MODULE.audit_sources


CATALOG = """\
version: 1
repositories:
  - id: example
    upstream: https://github.com/example/skills
    checked_commit: 0123456789abcdef0123456789abcdef01234567
    checked_version: 1.0.0
    license: MIT
"""

REVIEW = """\
version: 1
repository: example/skills
upstream: https://github.com/example/skills
checked_commit: 0123456789abcdef0123456789abcdef01234567
checked_version: 1.0.0
checked_at: 2026-08-09
license: MIT
scope:
  skill_files: 1
decision: adopted-selectively
skills:
  - name: example
    purpose: example purpose
    overlap: existing owner
    decision: retain-existing
    reason: no measured gap
"""


class AuditSourcesTest(unittest.TestCase):
    def make_root(self, review: str = REVIEW, catalog: str = CATALOG) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "sources" / "reviews").mkdir(parents=True)
        (root / "sources" / "catalog.yaml").write_text(catalog, encoding="utf-8")
        (root / "sources" / "reviews" / "example.yaml").write_text(
            review, encoding="utf-8"
        )
        return root

    def test_accepts_review_matching_catalog_and_skill_count(self) -> None:
        self.assertEqual(audit_sources(self.make_root()), [])

    def test_rejects_incorrect_skill_count(self) -> None:
        root = self.make_root(REVIEW.replace("skill_files: 1", "skill_files: 2"))
        self.assertTrue(any("skill_files" in error for error in audit_sources(root)))

    def test_rejects_duplicate_skill_names(self) -> None:
        duplicate = (
            REVIEW
            + """\
  - name: example
    purpose: another purpose
    overlap: another owner
    decision: reject
    reason: duplicate source name
"""
        )
        root = self.make_root(duplicate.replace("skill_files: 1", "skill_files: 2"))
        self.assertTrue(
            any("duplicate skill" in error for error in audit_sources(root))
        )

    def test_rejects_commit_mismatch(self) -> None:
        root = self.make_root(
            REVIEW.replace(
                "0123456789abcdef0123456789abcdef01234567",
                "fedcba9876543210fedcba9876543210fedcba98",
            )
        )
        self.assertTrue(any("checked_commit" in error for error in audit_sources(root)))

    def test_rejects_version_mismatch(self) -> None:
        root = self.make_root(
            REVIEW.replace("checked_version: 1.0.0", "checked_version: 2.0.0")
        )
        self.assertTrue(
            any("checked_version" in error for error in audit_sources(root))
        )


if __name__ == "__main__":
    unittest.main()
