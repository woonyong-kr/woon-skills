---
name: woon-knowledge-automation
description: Run and diagnose the private woon-knowledge one-shot pipeline. Use for imports/drop ingestion, Codex candidates, lineage, deletion, vector indexing, search, or launchd checks.
---

# Woon Knowledge Automation

Use the `woon-core` CLI as the only executable implementation and `woon-knowledge` as the private configuration and data workspace. This skill is optional operating guidance for Codex, not a runtime dependency. Do not invent a parallel watcher, daemon, database schema, or hidden source of truth.

## Locate the workspace

Resolve repositories before acting:

```bash
woon resolve knowledge
woon resolve core
```

Treat `woon-knowledge` as private. Before every push, verify:

```bash
gh repo view woonyong-kr/woon-knowledge --json isPrivate --jq .isPrivate
```

Stop unless the result is `true`. Preserve unrelated or in-progress changes; never reset or bulk-rewrite the repository.

## Run the pipeline

Use the core-owned one-shot command for normal ingestion:

```bash
woon knowledge automation run
```

Use individual commands for diagnosis or explicit control:

```bash
woon knowledge scan
woon knowledge status
woon knowledge process
woon knowledge index
woon knowledge search '<query>' --limit 5
woon knowledge stage
```

`process` must wait for the configured whole-inbox stability receipt and run Codex with the configured model and output schema. `index` must use the configured embedding and vector-store adapters. `stage` is the only supported automatic staging path. Providers may run only for the duration of a command.

For a source above `processing.streaming_threshold_mib` or `retrieval.read_full_document_under_tokens`, multiple Codex calls are expected: chunk map, bounded fan-in reductions, then one final candidate with the original source ID. Do not bypass this by loading the whole file into a prompt. Indexing must respect `retrieval.embedding_batch_size`; search must read candidate offsets first and stream only the selected document context.

## Interpret outputs

- Keep raw files under `sources/imports/drop` as evidence until the workflow records their lineage.
- Apply `.knowledgeignore` independently from `.gitignore`; never assume an ignored Git path is excluded from ingestion.
- A `sanitized` source is available through its redacted derivative. Never send or stage its raw path. Confirm the raw copy exists under the ignored local quarantine and tell the user to rotate a real credential.
- A `quarantined` source blocks only that file. Continue unrelated safe files.
- Files above the configured regular-Git threshold must be Git LFS tracked before staging. If LFS is unavailable, leave only that large file unstaged and report it.
- Keep `ingestion.whole_file_scan_max_mib`, `processing.streaming_threshold_mib`, `processing.map_reduce_fan_in`, `retrieval.embedding_batch_size`, and `retrieval.read_full_document_max_mib` in the repository config instead of hard-coding local overrides.
- Treat `knowledge-ops/candidates` as normalized drafts for human inspection, not approved truth.
- Treat `knowledge-ops/review` as exceptions only: conflicts, unsupported input, policy violations, or failed processing.
- Search the active raw-source index for grounded answers. Do not automatically promote a candidate to canonical Wiki content.
- When a source is deleted, run the pipeline so the tombstone and stale-vector deletion are recorded before considering cleanup complete.
- Never run `git add sources/imports/drop` or `git add -A` for automation output. Run `woon knowledge stage` and inspect the staged diff.

## Verify automation

Install or refresh the event-triggered job only when the user authorized automation:

```bash
woon knowledge automation install
woon knowledge automation status
```

Use `woon knowledge automation disable`, `enable`, and `uninstall` instead of editing the generated plist. Require `keep_alive: false`. Confirm no Codex, FastEmbed, LanceDB, ONNX, or Woon process remains after a run. Inspect `~/Library/Logs/woon-knowledge/automation.out.log` and `automation.err.log` for the receipt.

## Change adapters

Change only `config/knowledge-workflow.yaml`. Keep embedding and vector storage behind separate interfaces. Before switching revisions, models, dimensions, normalization, or stores, create a new index identity and perform export/import or a full rebuild; never mix incompatible vectors in one index.
