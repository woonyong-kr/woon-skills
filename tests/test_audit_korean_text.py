"""Guard the advisory scanner's protected Markdown and read-only boundary."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

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


def test_cli_is_advisory_and_leaves_input_bytes_untouched(tmp_path):
    path = tmp_path / "reader.md"
    original = "이를 통해 2026-09-02(추정)의 P95 120ms를 확인한다.\n".encode()
    path.write_bytes(original)
    result = subprocess.run([sys.executable, str(SCRIPT), "--json", str(path)], capture_output=True, text=True, check=True)
    payload = json.loads(result.stdout)
    assert payload["advisory_only"] is True
    assert payload["files"][0]["findings"]
    assert path.read_bytes() == original
