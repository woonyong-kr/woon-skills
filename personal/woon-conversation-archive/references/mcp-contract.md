# Canonical Knowledge MCP contract

- `woon_knowledge_search(query, limit)`: bounded snippets and stable IDs. Read-only.
- `woon_knowledge_get(canonical_id)`: complete body, metadata, path, and content revision. Read-only.
- `woon_knowledge_archive_conversation(...)`: creates one new ID or replaces one existing ID when `expected_revision` matches.
- `woon_knowledge_reindex()`: rebuilds the local FTS index from Markdown and exits.
- `woon_knowledge_audit()`: checks ID/path, duplicate title, and unresolved learning relations.
- `woon_knowledge_history(canonical_id, limit)`: lists Git recovery points.
- `woon_knowledge_restore(...)`: destructive recovery. Requires commit ID, current revision, and `confirmed=true`.

An existing document without `expected_revision` is rejected. A new document with an expected revision is also rejected. These failures protect concurrent edits and are not reasons to write the file directly.
