#!/usr/bin/env bash
set -euo pipefail

fixture_dir="$(cd "$(dirname "$0")" && pwd)"
build_dir="$(mktemp -d /tmp/woon-language-fixture.XXXXXX)"
trap 'rm -rf -- "$build_dir"' EXIT

python3 "$fixture_dir/verify.py" "$fixture_dir"

npx --yes --package typescript@5.9.3 tsc \
  --strict --target ES2022 --module Node16 --moduleResolution Node16 --noEmit \
  "$fixture_dir/typescript/invoice-parser.ts"

javac -d "$build_dir/java" "$fixture_dir/java/Invoice.java"
python3 -m py_compile "$fixture_dir/python/invoice_parser.py"

clang -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Werror \
  "$fixture_dir/c/invoice.c" "$fixture_dir/c/invoice_test.c" \
  -o "$build_dir/c-fixture"
"$build_dir/c-fixture"

clang++ -std=c++20 -Wall -Wextra -Wpedantic -Wconversion -Werror \
  "$fixture_dir/cpp/invoice.cc" "$fixture_dir/cpp/invoice_test.cc" \
  -o "$build_dir/cpp-fixture"
"$build_dir/cpp-fixture"

dotnet build "$fixture_dir/csharp/LanguageFixture.csproj" \
  --nologo --verbosity quiet --output "$build_dir/csharp" \
  --property:BaseIntermediateOutputPath="$build_dir/csharp-obj/"
DOTNET_ROLL_FORWARD=Major dotnet "$build_dir/csharp/LanguageFixture.dll"

echo "language compiler fixture: TypeScript, Java, Python, C, C++ and C# passed"
