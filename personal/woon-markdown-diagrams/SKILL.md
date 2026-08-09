---
name: woon-markdown-diagrams
description: Create neutral Mermaid diagrams in Markdown. Use for architecture, state, sequence, class, ER, memory, or flow diagrams that must work in light and dark mode.
---

# Woon Markdown Diagrams

Create a Mermaid diagram only when it makes a relationship, state change, or sequence easier to learn than prose. Keep the diagram in the Markdown document; do not create a separate AI image, SVG, or PNG by default.

## Choose one question

Write the question in one sentence before drawing. Select one diagram type:

- value or data movement: `flowchart LR`
- hierarchy or stepwise structure: `flowchart TD`
- time-ordered calls: `sequenceDiagram`
- state transitions: `stateDiagram-v2`
- type and implementation relations: `classDiagram`
- table cardinality: `erDiagram`

If the drawing answers more than one question, split it. Do not mix inheritance, runtime calls, database relations, and deployment topology in one diagram.

## Keep it readable

- Use at most 9 nodes in one overview.
- Keep one node to one action or state and at most 3 short lines.
- Split at domain boundaries or abstraction levels before lines begin to cross.
- Use the same grammar for sibling labels.
- Put a condition on an arrow only when it changes the path.
- Match every class, method, field, route, and file name to the source exactly.

## Language and theme

Use Korean for explanatory labels and preserve technical identifiers such as `KnowledgeSearchIndex`, `expected_revision`, and `wiki/canonical`.

Do not hard-code `fill`, `color`, `#ffffff`, `#000000`, or semantic red/green `classDef` values. Let the Markdown renderer select foreground and background for light/dark mode. Express emphasis with position, borders, shapes, labels, solid lines, or dotted lines rather than color.

## Verify

1. Compare the diagram's arrows with the actual order or dependency.
2. Check identifiers against code or source material.
3. Confirm a reader can distinguish branch, failure, and success without color.
4. Render in both light and dark mode when the current app provides a preview.
5. Split the diagram if text clips, edges cross, or the aspect ratio becomes difficult to scan.

Read [diagram checklist](references/diagram-checklist.md) for the final quality gate.
