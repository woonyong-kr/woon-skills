"""Guard the advisory scanner's protected Markdown and read-only boundary."""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/writing/humanize/scripts/audit_korean_text.py"
spec = importlib.util.spec_from_file_location("audit_korean_text", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_review_locations_exclude_source_spans_and_keep_line_numbers():
    protected = '''---
summary: 이를 통해
---
```kotlin
println("이를 통해")
```
> 원문 인용: 이를 통해
    코드: 이를 통해
$$
\\text{이를 통해}
$$
`이를 통해`와 $\\text{이를 통해}$
[[folder/이를 통해|원문]] [근거](folder/이를-통해.md)
<!-- 이를 통해 -->
'''
    text = protected + "이를 통해 필터가 적용됩니다.\n"
    assert module.audit(protected) == []
    assert module.audit(text) == [{"code": "translationese-connectors", "line": 15, "match": "이를 통해"}]
    assert len(module.prose_only(text)) == len(text)


@pytest.mark.parametrize("json_output", [True, False])
def test_cli_is_advisory_and_leaves_input_bytes_untouched(tmp_path, json_output):
    path = tmp_path / "한국어.md"
    original = "이를 통해 2026-09-02(추정)의 P95 120ms를 확인한다.\n".encode()
    path.write_bytes(original)
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *(["--json"] if json_output else []), str(path)],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "cp1252"},
        check=True,
    )
    if json_output:
        payload = json.loads(result.stdout)
        assert payload["advisory_only"] is True
        assert payload["files"][0]["path"] == str(path)
        assert payload["files"][0]["findings"][0]["match"] == "이를 통해"
    else:
        assert "이를 통해" in result.stdout
        assert "자동 판정이 아닙니다" in result.stdout
    assert path.read_bytes() == original
