# data/

Source data, datasets and quality reports. About 1,500 files.

| Folder or file | Kind | Edit by hand? |
|---|---|---|
| `courses/` | Source. Course JSON, `phase-N/<code>_<level>.json`, plus `index.json` (the release manifest) | Yes, as authored content. Never bulk-generate |
| `schemas/`, `editorial/`, `reviews/` | Source. Schemas, editorial rules, native-review records | Reviews only by a human reviewer |
| `content/`, `topics/`, `global/`, `languages/`, `language-research/`, `language-inventory/` | Source and research inputs for generators | Yes |
| `flashcards/`, `themes/`, `audio-manifest/`, `learning/` | Datasets the runtime and builders read | Check the writer first |
| `courses.json`, `content-graph.json`, `copy-index.json` | Generated indexes | No |
| `lang-<code>.json` | Language data read by the language-pack builders | Check `tools/build-lang-packs.py` before editing |
| `quality/` | **Gate output.** Language gate, indexing baseline, page inventory, audits | No. Gates write it |
| `audit/`, `research/` | Audit and research records | Rarely |

## The two files that guard publishing

- `quality/indexing-baseline.json`: the frozen index, noindex and canonical
  state of every existing page. The only hand edit allowed is adding a new,
  owner-approved page under `owner_approved_new_indexable`, with a decision
  record in `docs/decisions/`.
- `quality/language-gate.json`: why each language is or is not publishable.
  A native reviewer's record in `reviews/<code>.json` is required to open one.

No personal data in this folder.
