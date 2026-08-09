---
name: woon-conversation-archive
description: Archive an AI conversation as one deduplicated canonical learning document in private woon-knowledge. Use when asked 지금까지 대화를 정리해 줘, 위키에 저장해 줘, or 세션을 아카이빙해 줘.
---

# Woon Conversation Archive

Turn a conversation into one human-readable and AI-searchable canonical Markdown document. Use the Woon Knowledge MCP tools as the write boundary; do not create blog, portfolio, source-copy, or review variants.

## Resolve the private vault

Read the current conversation and the referenced archived task if the user names one. Resolve the vault without hard-coded paths:

```bash
woon resolve knowledge
```

Read `ai-reference/canonical-learning-document-standard.md` before drafting. Treat `woon-knowledge` as private. This workflow does not commit or push unless the user separately requests it.

## Find the canonical target

1. Extract decisions, explanations, examples, evidence, and unresolved questions from the conversation.
2. Search two or three stable Korean and technical keywords with `woon_knowledge_search`.
3. If a matching concept exists, call `woon_knowledge_get` and read its complete body and revision.
4. Use a new `canonical_id` only when no existing document answers the same question.

Do not decide identity from title wording alone. Different terms can describe the same concept; similar keywords can describe different conditions.

## Build one revised document

Follow these rules:

- Preserve verified facts, code identifiers, conditions, and the user's decisions.
- Remove conversational order, repeated questions, apologies, status narration, and AI filler.
- Put prerequisites before the current concept and advanced material after it.
- Integrate new facts into the relevant existing section instead of appending a second summary.
- If sources conflict, separate version, environment, or time conditions. Do not select a winner without evidence.
- Keep technical identifiers in their original form and write explanations in Korean.
- Add only diagrams that answer a question more clearly than prose. Use the `woon-markdown-diagrams` skill for them.

The `body` sent to MCP must not contain YAML frontmatter or an H1. The repository creates those fields and the navigation section.

## Save with concurrency protection

For a new concept, call `woon_knowledge_archive_conversation` without `expected_revision`. For an existing concept, pass exactly the revision returned by `woon_knowledge_get`. If the revision changed, read the document again and redo the merge; never force an overwrite.

Provide:

- `canonical_id`: `domain/topic-slug`
- `title`, `domain`, one-sentence `summary`
- `difficulty`: `foundation`, `intermediate`, or `advanced`
- `prerequisites`, `next_concepts`, `related`
- available Codex task/session IDs as `source_session_ids`
- the complete revised body

After saving, call `woon_knowledge_audit`. Report the clickable `wiki/canonical/...` path and whether the file was created or updated. If audit fails, repair only the affected document or relationship before reporting completion.

## Fallback when MCP is unavailable

Use `woon knowledge search`, `get`, `audit`, and `index` for diagnosis. Do not bypass the optimistic write contract with direct overwrite. Restore a previous version only after the user explicitly selects a Git revision and confirms recovery.

Read [MCP contract](references/mcp-contract.md) when tool inputs or failure behavior are unclear.
