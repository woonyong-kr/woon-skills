#!/usr/bin/env bash
set -euo pipefail

if ! command -v woon >/dev/null 2>&1; then
  echo "woon resolver is unavailable; learning-content standard is unverified" >&2
  exit 2
fi

for standard_uri in \
  repo://skills/standards/learning-content-quality.md \
  repo://skills/standards/learning-writing-harness.md \
  repo://skills/standards/learning-style-corpus.yaml; do
  standard_path="$(woon resolve "$standard_uri")"
  if [[ ! -f "$standard_path" ]]; then
    echo "learning-content contract does not exist: $standard_path" >&2
    exit 2
  fi
  sed -n '1,420p' "$standard_path"
done
