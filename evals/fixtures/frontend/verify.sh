#!/usr/bin/env bash
set -euo pipefail

fixture_dir="$(cd "$(dirname "$0")" && pwd)"

if command -v google-chrome >/dev/null 2>&1; then
  browser_bin="$(command -v google-chrome)"
elif command -v chromium >/dev/null 2>&1; then
  browser_bin="$(command -v chromium)"
elif [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
  browser_bin="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else
  echo "Chrome or Chromium is required for the frontend fixture" >&2
  exit 1
fi

"$browser_bin" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --virtual-time-budget=1000 \
  --dump-dom \
  "file://$fixture_dir/index.html" \
  | python3 "$fixture_dir/verify.py"
