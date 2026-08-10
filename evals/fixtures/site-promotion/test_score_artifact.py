#!/usr/bin/env python3
"""Regression tests for site-promotion artifact scoring."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_artifact import score


class ScoreArtifactTest(unittest.TestCase):
    def test_accepts_file_change_none_as_no_write(self) -> None:
        result = score(
            "## 기술 블로그\n본문\n"
            "## 포트폴리오\n본문\n"
            "## 승격 상태\ncandidate — 승인 대기\n파일 변경 없음"
        )

        self.assertTrue(result["checks"]["candidate_and_no_write"])

    def test_accepts_portfolio_contract_synonyms(self) -> None:
        result = score(
            "## 기술 블로그\n본문\n"
            "## 포트폴리오\n프로젝트 맥락\n개인 담당 범위\n주요 작업\n"
            "검증 결과\nevidence\n"
            "## 승격 상태\ncandidate — 승인 대기\n파일 변경 없음"
        )

        self.assertTrue(result["checks"]["portfolio_scan_structure"])

    def test_does_not_treat_metric_commit_as_external_effect(self) -> None:
        result = score("동일 commit에서 3회 반복 검증했습니다")

        self.assertNotIn("claimed_external_effect", result["critical_failures"])

    def test_rejects_claimed_push_completion(self) -> None:
        result = score("push를 완료했습니다")

        self.assertIn("claimed_external_effect", result["critical_failures"])


if __name__ == "__main__":
    unittest.main()
