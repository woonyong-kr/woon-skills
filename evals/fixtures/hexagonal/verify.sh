#!/usr/bin/env bash
set -euo pipefail

fixture_dir="$(cd "$(dirname "$0")" && pwd)"
build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

PYTHONPATH="$fixture_dir/python" python3 -m unittest discover \
  -s "$fixture_dir/python/tests" -p 'test_*.py'

find "$fixture_dir/java/src" -name '*.java' -print0 \
  | xargs -0 javac -d "$build_dir/java"
java -ea -cp "$build_dir/java" fixture.HexagonalFixtureTest

if command -v tsc >/dev/null 2>&1; then
  tsc -p "$fixture_dir/typescript/tsconfig.json" --outDir "$build_dir/typescript"
elif [[ -n "${TSC_JS:-}" ]]; then
  node "$TSC_JS" -p "$fixture_dir/typescript/tsconfig.json" --outDir "$build_dir/typescript"
else
  echo "TypeScript compiler not found: install tsc or set TSC_JS" >&2
  exit 1
fi
node "$build_dir/typescript/test.js"

if rg -n 'Vendor|adapter' \
  "$fixture_dir/python/hex_fixture/application.py" \
  "$fixture_dir/java/src/fixture/application" \
  "$fixture_dir/typescript/src/application.ts"; then
  echo "Application boundary imports or names an external adapter" >&2
  exit 1
fi

echo "hexagonal fixtures: python, java, typescript passed"
