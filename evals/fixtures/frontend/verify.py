from __future__ import annotations

import json
import re
import sys
from html import unescape


document = sys.stdin.read()
status = re.search(r'<body[^>]*data-status="([^"]+)"', document)
results = re.search(r'<pre id="results">(.*?)</pre>', document, re.DOTALL)

if status is None or results is None:
    raise SystemExit("frontend fixture result was not rendered")

checks = json.loads(unescape(results.group(1)))
failed = [name for name, passed in checks.items() if passed is not True]
if status.group(1) != "pass" or failed:
    raise SystemExit(f"frontend fixture failed: {failed}")

print(f"frontend browser fixture: {len(checks)} checks passed")
