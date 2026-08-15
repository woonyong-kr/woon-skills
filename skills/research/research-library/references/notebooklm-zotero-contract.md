# NotebookLM and Zotero Contract

## Ownership

| Layer | Owns | Does not own |
| --- | --- | --- |
| Zotero | chosen papers, bibliography metadata, attachment location, annotations | Woon canonical claims or rendered Wiki pages |
| NotebookLM | temporary research notebook, generated study aids, artifact Markdown | source truth or Woon search index |
| Woon intake plan | hashes, identifiers, promotion requirements | raw PDF, Zotero profile, Google session, generated content as fact |
| Woon compiler | accepted sources, claims, pages, receipts | Zotero and NotebookLM account state |

## NotebookLM Boundary

`nlm` is an audited third-party client over a private NotebookLM protocol, not a Google-supported service API. It can read an already logged-in browser profile and store Google session credentials, so it must never be installed as an unrestricted MCP server or given a whole-Vault directory.

Use a manually approved `nlm artifact export` only for a selected research notebook. Keep generated Markdown in a local export directory and create `notebooklm-export.json` next to it:

```json
{
  "version": 1,
  "tool": {
    "name": "nlm",
    "revision": "<40-character audited Git commit>"
  },
  "artifacts": [
    {
      "artifact_id": "<NotebookLM artifact ID>",
      "kind": "report",
      "path": "report.md",
      "sha256": "<sha256 of report.md>",
      "source_refs": ["doi:10.0000/example", "arxiv:2401.00001"]
    }
  ]
}
```

All artifact paths are relative to this manifest. The intake planner rejects hash drift, path escape, missing DOI/arXiv references, and YouTube URLs. When a Zotero export is supplied with the manifest, every artifact `source_ref` must match a DOI or arXiv ID in that selected collection. A valid plan only proves the exported bytes and declared evidence identity; it never proves a generated claim.

### Approved Markdown export

Use `woon knowledge notebooklm-export` rather than creating the manifest by hand. It runs the pinned `nlm artifact export` command for one already-generated artifact, refuses to overwrite a Markdown file or manifest, rejects video URLs, then records the artifact ID, Markdown hash, and declared DOI·arXiv references. It is a download-only bridge: it does not add NotebookLM sources, modify a notebook, or write to the Woon Vault.

The whole-notebook Obsidian export offered by third-party automation repositories is not a direct Vault import path. It can be useful as a local working export, but its source notes and generated artifacts must be selected and passed through this manifest plus intake plan before any canonical promotion.

## Zotero Boundary

Use Zotero as the literature library. Export the selected collection as CSL JSON or Better BibTeX JSON; the Woon planner reads only bibliographic fields and never reads the Zotero SQLite profile or copies attachments. Preserve PDFs in Zotero-managed local storage and respect license and access restrictions before quoting or archiving text.

The Obsidian `Citations` plugin may read the same CSL JSON to insert citations while writing. It is a convenience view, not the scholarly source of truth, and it must point at a local-only export. Do not enable automatic note creation into `wiki/`; literature notes first enter the review path above.

## Promotion

1. Resolve DOI/arXiv metadata against the publisher, arXiv, or a scholarly metadata provider.
2. Record what source text is licensed or accessible and the exact claim-supported excerpt.
3. Save a purpose-bound source through `$archive` or update existing compiler inputs through `$compile-knowledge`.
4. Compile, audit, reindex, and test the exact retrieval/citation behavior that the paper is meant to support.

## Checked references

These links establish tool capabilities and boundaries, not the truth of a paper or a generated summary. Recheck them when the tool or this contract changes.

- 2026-08-14: [Zotero export guidance](https://www.zotero.org/support/kb/exporting) distinguishes exporting a selected collection from backing up or transferring a whole library. Woon therefore reads only an explicitly chosen CSL JSON or Better BibTeX JSON export.
- 2026-08-14: [Obsidian Citations](https://github.com/hans/obsidian-citation-plugin) accepts BibTeX and CSL JSON exports for citation lookup and literature-note templates. Woon keeps those notes in a review folder rather than generating `wiki/` pages.
- 2026-08-14: [NotebookLM note guidance](https://support.google.com/notebooklm/answer/16262519?hl=en) allows notes to become sources. Woon does not perform that conversion automatically because generated notes and original sources have different evidentiary status.
- 2026-08-14: [`tmc/nlm`](https://github.com/tmc/nlm) documents browser-profile credential extraction and Markdown artifact export. Its pinned revision and the narrower Woon adoption decision are recorded in `sources/reviews/tmc-nlm.yaml`.
