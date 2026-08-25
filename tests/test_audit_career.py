import unittest
from pathlib import Path

from scripts.audit_career import audit_career

ROOT = Path(__file__).resolve().parents[1]


class AuditCareerTest(unittest.TestCase):
    def test_current_career_contract_and_behavior_cases_are_complete(self) -> None:
        self.assertEqual(audit_career(ROOT), [])


if __name__ == "__main__":
    unittest.main()
