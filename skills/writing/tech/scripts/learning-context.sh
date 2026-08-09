#!/usr/bin/env bash
set -euo pipefail

if ! command -v woon >/dev/null 2>&1; then
  echo "woon resolver is unavailable; learning-content standard is unverified" >&2
  exit 2
fi

standard_path="$(woon resolve repo://skills/standards/learning-content-quality.md)"
if [[ ! -f "$standard_path" ]]; then
  echo "learning-content standard does not exist: $standard_path" >&2
  exit 2
fi
sed -n '1,360p' "$standard_path"
