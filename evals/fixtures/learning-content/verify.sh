#!/usr/bin/env bash
set -euo pipefail

fixture_dir="$(cd "$(dirname "$0")" && pwd)"
build_dir="$(mktemp -d /tmp/woon-learning-fixture.XXXXXX)"
trap 'rm -rf -- "$build_dir"' EXIT

javac -encoding UTF-8 -d "$build_dir/java" "$fixture_dir/AddressLesson.java"
java -cp "$build_dir/java" AddressLesson > "$build_dir/output.txt"
python3 "$fixture_dir/verify.py" "$fixture_dir" "$build_dir/output.txt" "$build_dir/mermaid"

for source in "$build_dir"/mermaid/*.mmd; do
  "$fixture_dir/../../../skills/docs/diagram/scripts/verify-mermaid.sh" \
    "$source" "$build_dir/rendered" 640
done

echo "learning fixture: Java compile/run and Mermaid default/dark render passed"
