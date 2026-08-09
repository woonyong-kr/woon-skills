#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: verify-mermaid.sh <source.mmd> <output-dir> [max-viewbox-width]" >&2
  exit 64
fi

source_file="$1"
output_dir="$2"
max_viewbox_width="${3:-0}"
if [[ ! -f "$source_file" ]]; then
  echo "Mermaid source does not exist: $source_file" >&2
  exit 66
fi
mkdir -p "$output_dir"

if command -v mmdc >/dev/null 2>&1; then
  runner=(mmdc)
elif command -v npx >/dev/null 2>&1; then
  runner=(npx --offline --yes @mermaid-js/mermaid-cli@11.12.0)
else
  echo "Mermaid renderer unavailable; install a repository-pinned mmdc first" >&2
  exit 2
fi

name="$(basename "$source_file" .mmd)"
default_output="$output_dir/${name}-default.svg"
dark_output="$output_dir/${name}-dark.svg"

if ! "${runner[@]}" --input "$source_file" --output "$default_output" --theme default --backgroundColor transparent; then
  echo "Mermaid renderer unavailable or default render failed" >&2
  exit 2
fi
if ! "${runner[@]}" --input "$source_file" --output "$dark_output" --theme dark --backgroundColor transparent; then
  echo "Mermaid dark render failed" >&2
  exit 1
fi
test -s "$default_output"
test -s "$dark_output"
python3 - "$default_output" "$dark_output" "$max_viewbox_width" <<'PY'
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

maximum = float(sys.argv[3])
for raw_path in sys.argv[1:3]:
    path = Path(raw_path)
    root = ET.parse(path).getroot()
    view_box = root.attrib.get("viewBox", "").split()
    if len(view_box) != 4:
        raise SystemExit(f"SVG viewBox is missing or invalid: {path}")
    width = float(view_box[2])
    if maximum > 0 and width > maximum:
        raise SystemExit(
            f"SVG natural width {width:.1f}px exceeds {maximum:.1f}px: {path}"
        )
PY
printf 'mermaid render passed: %s %s\n' "$default_output" "$dark_output"
