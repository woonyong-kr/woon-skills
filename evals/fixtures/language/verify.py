from __future__ import annotations

import re
import sys
from pathlib import Path


root = Path(sys.argv[1])
checks: dict[str, bool] = {}

typescript = (root / "typescript" / "invoice-parser.ts").read_text()
checks["typescript_unknown_boundary"] = "input: unknown" in typescript and "any" not in typescript
checks["typescript_public_before_helper"] = typescript.index("export function") < typescript.index("function isRecord")

java = (root / "java" / "Invoice.java").read_text()
checks["java_explicit_import"] = "import java.util.Objects;" in java and "import java.util.*" not in java
checks["java_one_top_level_type"] = len(re.findall(r"^public (?:final )?class ", java, re.MULTILINE)) == 1

python = (root / "python" / "invoice_parser.py").read_text()
checks["python_no_mutable_default"] = "values: Mapping[str, object] | None = None" in python
checks["python_main_guard"] = 'if __name__ == "__main__":' in python

c_header = (root / "c" / "invoice.h").read_text()
c_source = (root / "c" / "invoice.c").read_text()
checks["c_self_contained_header"] = "#include <stdbool.h>" in c_header and "#include <stddef.h>" in c_header
checks["c_related_header_first"] = c_source.startswith('#include "invoice.h"')
checks["c_internal_linkage"] = "static bool add_without_overflow" in c_source
checks["c_pointer_contract"] = "amount_count" in c_header and "total_cents" in c_header

cpp_header = (root / "cpp" / "invoice.h").read_text()
cpp_source = (root / "cpp" / "invoice.cc").read_text()
checks["cpp_related_header_first"] = cpp_source.startswith('#include "invoice.h"')
checks["cpp_private_invariant"] = cpp_header.index("private:") < cpp_header.index("id_;")
checks["cpp_no_public_data"] = "public:\n  std::string id_;" not in cpp_header

csharp = (root / "csharp" / "InvoiceParser.cs").read_text()
project = (root / "csharp" / "LanguageFixture.csproj").read_text()
checks["csharp_nullable"] = "<Nullable>enable</Nullable>" in project
checks["csharp_private_field"] = "private readonly" in csharp and " _loader;" in csharp
checks["csharp_async_contract"] = "Task<string> LoadAsync" in csharp and "async void" not in csharp

failed = [name for name, passed in checks.items() if not passed]
if failed:
    raise SystemExit(f"language convention fixture failed: {failed}")

print(f"language convention fixture: {len(checks)} structural checks passed")
