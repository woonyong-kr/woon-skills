#!/usr/bin/env sh
set -eu

fixture_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$fixture_dir/verify.py"
