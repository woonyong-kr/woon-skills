# Canonical Knowledge MCP contract

- `woon_knowledge_search(query, limit)`: bounded snippets and stable IDs. Read-only.
- `woon_knowledge_get(canonical_id)`: complete body, metadata, path, and content revision. Read-only.
- `woon_knowledge_archive_conversation(canonical_id, title, domain, summary, purpose, body, difficulty, prerequisites, next_concepts, related, source_session_ids, expected_revision)`: creates one new ID or replaces one existing ID when `expected_revision` matches. `purpose` is a nonempty statement of why the document is retained and what future question, decision, or output it should support.
- `woon_knowledge_reindex()`: rebuilds the local FTS index from Markdown and exits.
- `woon_knowledge_compile(force=false)`: compiles stale source-schema inputs and rebuilds the index when output changes.
- `woon_knowledge_compile_audit()`: verifies page provenance and compiler receipts without mutation.
- `woon_knowledge_audit()`: checks ID/path, duplicate title, and unresolved learning relations.
- `woon_knowledge_history(canonical_id, limit)`: lists Git recovery points.
- `woon_knowledge_restore(...)`: destructive recovery. Requires commit ID, current revision, and `confirmed=true`.

An existing document without `expected_revision` is rejected. A new document with an expected revision is also rejected. These failures protect concurrent edits and are not reasons to write the file directly.

The revision comparison, normalized-title check, and `source_ids` ownership check are repeated inside one cross-process mutation lock. A `source_id` may belong to only one canonical document. The archive tool writes source, claim, page spec, Markdown output, and receipt as one compiler transaction. If index rebuild fails, the adapter restores the previous canonical bytes and compiler inputs; if a receipt, compiler output, or stored index generation differs from current inputs, search fails closed and requires compile or reindex.

Treat the revision returned by `woon_knowledge_get` as an opaque string and pass it unchanged. `publish`, `access`, `status`, `aliases`, YAML frontmatter, and H1 are not archive arguments or body content. The filesystem adapter deterministically writes `status: Canonical`, `publish: false`, `access: local-only`, the remaining structured metadata, and the title H1.

Before proposing or sending a payload, reject it if `body` starts with `---`, contains an H1, uses an undeclared argument, or contains an unverified relationship value.

For a non-executed example, return a corrected contract-shaped payload rather than only refusing. Use placeholders only for unknown required `canonical_id`, `title`, `domain`, `summary`, `purpose`, and `body`; default `difficulty` to `foundation` and unknown optional lists to `[]`. Never send a placeholder in a real MCP call.

## Learning relation IDs

`prerequisites`, `next_concepts`, and `related` accept only verified slash-separated canonical IDs such as `architecture/dependency-inversion`.

- Search and get the related canonical document before using its ID.
- Never pass a title, display label, translated phrase, or search keyword.
- If no canonical ID is verified, pass an empty array. Do not invent an ID from the title.
