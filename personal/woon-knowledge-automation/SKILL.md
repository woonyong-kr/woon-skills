---
name: woon-knowledge-automation
description: Run and diagnose the private woon-knowledge one-shot pipeline. Use for imports/drop ingestion, Codex candidates, lineage, deletion, vector indexing, search, or launchd checks.
---

# Woon Knowledge Automation

Use repository-owned commands and configuration. Do not invent a parallel watcher, daemon, database schema, or hidden source of truth.

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

Use the one-shot runner for normal ingestion:

```bash
<knowledge-repo>/scripts/run-knowledge-automation.sh
```

Use individual commands for diagnosis or explicit control:

```bash
woon knowledge scan
woon knowledge status
woon knowledge process
woon knowledge index
woon knowledge search --query '<query>' --limit 5
```

`process` must run Codex with the configured model and output schema. `index` must use the configured embedding and vector-store adapters. Providers may run only for the duration of a command.

## Interpret outputs

- Keep raw files under `sources/imports/drop` as evidence until the workflow records their lineage.
- Treat `knowledge-ops/candidates` as normalized drafts for human inspection, not approved truth.
- Treat `knowledge-ops/review` as exceptions only: conflicts, unsupported input, policy violations, or failed processing.
- Search the active raw-source index for grounded answers. Do not automatically promote a candidate to canonical Wiki content.
- When a source is deleted, run the pipeline so the tombstone and stale-vector deletion are recorded before considering cleanup complete.

## Verify automation

Install or refresh the event-triggered job only when the user authorized automation:

```bash
<knowledge-repo>/scripts/install-knowledge-automation-launchd.sh
launchctl print "gui/${UID}/org.woonyong.knowledge-automation"
```

Require `KeepAlive = false`. Confirm no Codex, FastEmbed, LanceDB, ONNX, or Woon process remains after a run. Inspect `~/Library/Logs/woon-knowledge/automation.out.log` and `automation.err.log` for the receipt.

## Change adapters

Change only `config/knowledge-workflow.yaml`. Keep embedding and vector storage behind separate interfaces. Before switching revisions, models, dimensions, normalization, or stores, create a new index identity and perform export/import or a full rebuild; never mix incompatible vectors in one index.
