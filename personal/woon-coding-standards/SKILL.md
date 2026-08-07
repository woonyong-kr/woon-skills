---
name: woon-coding-standards
description: Use when coding or reviewing. Apply cross-project defaults for placement, naming, immutability, errors, concurrency, and verification after repository rules.
---

# Coding Standards

Use this skill as the shared floor across projects. Treat the current repository's `AGENTS.md`, contribution guide, architecture decisions, formatter, linter, type checker, and tests as higher-priority evidence.

## Workflow

1. Read the repository rules and the code surrounding the requested change.
2. State the responsibility of the changed behavior in one sentence.
3. Put the code beside the policy or data it owns, not beside the caller that happens to need it.
4. Make the smallest change that satisfies the request.
5. Run the narrowest relevant formatter, linter, type check, and test.
6. Report what was verified and what remains unverified.

## Code placement

Choose the location by responsibility and dependency direction.

- Domain policy belongs in the domain or core layer and must not import UI, database, network, or framework implementations.
- Application orchestration belongs in a use-case or service layer and depends on explicit ports or interfaces when a real replacement or test boundary exists.
- Database, network, filesystem, framework, and vendor code belongs in adapters or infrastructure.
- Input parsing and validation belongs at the system boundary before untrusted values reach core policy.
- Shared utilities are allowed only when multiple callers share the same stable meaning. Similar-looking code with different reasons to change stays separate.
- Follow the repository's existing layout when it already expresses these responsibilities clearly.

Do not add a layer, interface, or abstraction only to resemble an architecture diagram. Require a demonstrated dependency boundary, replacement point, or isolated test need.

## Naming and structure

- Use names that reveal domain meaning and units; avoid unexplained abbreviations and generic names such as `data`, `value`, `manager`, or `util`.
- Name functions with a verb that describes their observable result.
- Keep a function focused on one responsibility and prefer early returns over deeply nested control flow.
- Comments explain intent, constraints, and trade-offs; they do not translate obvious code.
- Match the repository's language and framework conventions before applying a personal preference.

## Data and side effects

- Prefer immutable data flow at ownership boundaries. Copy before sorting or transforming a shared collection.
- Make mutation local and explicit when it is required for performance or by an API contract.
- Do not hide I/O, network calls, writes, global state, or process execution behind a pure-looking helper.
- Preserve the original error as a cause and add actionable context at the boundary where meaning is known.
- Reject invalid external input before it changes persistent or shared state.

Example:

```typescript
const sortedMarkets = [...markets].sort((left, right) => right.volume - left.volume)
```

## Concurrency and performance

- Run work concurrently only when operations are independent and concurrency limits and partial failures are acceptable.
- Use `Promise.all` only when one failure may fail the whole group; otherwise choose explicit per-task error handling.
- Add `useMemo`, `useCallback`, caches, indexes, batching, or parallelism only for a required identity contract or a measured bottleneck.
- Record the relevant measurement when making a performance claim.

## Evidence boundary

KISS, DRY, YAGNI, immutability, and readability are review heuristics, not universal empirical guarantees.

- Prefer clarity until current code, tests, profiling, incidents, or review history demonstrates a narrower rule.
- Extract duplication after the repeated behavior and its change boundary are understood; do not apply DRY mechanically.
- Separate a policy default from a measured claim. Do not invent defect-rate, review-time, render-cost, or query-cost evidence.

## Completion gate

Before reporting completion:

- every changed line traces to the requested behavior;
- unrelated user changes remain untouched;
- format, lint, type check, and tests were run where available;
- user-visible behavior was checked when practical;
- unrun integration, E2E, deployment, or production checks are named explicitly.
