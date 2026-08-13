# LLM Wiki compiler contract

## Inputs

- `sources.yaml`: `source_id`, kind, safe locator, original/normalized SHA-256, privacy, lifecycle, title, body. New non-`legacy-wiki` sources additionally require a nonempty `purpose` that states why the knowledge is retained and what future question, decision, or output it supports. Conversation provenance may also carry `source_session_ids`.
- `claims.yaml`: only `status: accepted` claims render. Each claim declares one or more source IDs and Markdown supported by those sources.
- `pages.yaml`: exactly one safe `.md` output path, frontmatter whose title matches `title`, source IDs, claim IDs, and either `source-body` or `claims` rendering.
- `relations.yaml`: derived learning edges for review. It does not replace canonical page validation.
- `receipts.yaml`: compiler-owned input/output hashes. Never edit it manually.
- `review-queue.yaml`: unresolved, rejected, or conflicting candidates. It is not a render input.

## Gates

- A page may reference only existing source and accepted-claim IDs.
- Every claim evidence ID must belong to that page's source set.
- A public page may use only `privacy: public` sources.
- A new source without a concrete retention purpose is rejected; legacy migrations preserve the historical source as-is rather than inventing past intent.
- The compiler requires matching frontmatter title and H1, a nonempty body, a safe path, and receipt hashes that match output bytes.
- Retrieval fails closed when a catalog change, output change, or receipt mismatch is detected.

## Operations

- `woon_knowledge_compile(force=false)`: writes only stale outputs and rebuilds the local index when an output changed.
- `woon_knowledge_compile_audit()`: verifies reproducibility and receipts without mutation.
- `woon_knowledge_reindex()`: only after a current compiler audit; it cannot make stale inputs valid.
- `woon_knowledge_archive_conversation(...)`: writes a conversation source, accepted claim, and page spec atomically before compiling the canonical output.

Legacy Wiki migration uses one `legacy-wiki` source and `legacy-document` accepted claim per existing page. This proves reproduction and preserves the original evidence; it does not claim that every old paragraph was independently fact-checked.
