# tools/

Generators, audits and tests. About 330 files; roughly 111 are tests
(`test-*`) and 109 are build, apply, author, inject or repair scripts. Phases
1 and 2 of the migration will split them into `tests/` and `generators/`
(see `docs/architecture/REPO-STRUCTURE.md` §6). Until then, new files follow
the naming below so the split stays mechanical.

| Prefix | Job | Writes site files? |
|---|---|---|
| `build-*` | Generate pages, data, sitemaps, reports | Yes |
| `apply-*`, `inject-*`, `repair-*`, `author-*` | Patch or author content in place | Yes |
| `audit-*`, `check-*` | Read and report | No (may write `reports/`, `data/quality/`) |
| `test-*` | Tests | No |

Subfolders: `lib/` shared helpers, `ultra/` the indexing contract
(`contract.py`; the decorative layer is `apply-ultra.py` and `lib/ultra_content.py`), `templates/` page templates, `lang-data/` and `course-data/`
authored inputs, `assets/` fonts for image generation.

## Run

```bash
python3 tools/build-all.py check     # the master gate
python3 tools/ultra/contract.py      # indexing and canonical freeze
python3 tools/language-gate.py       # language publication gate
```

Regeneration order matters: `docs/runbooks/regenerate-and-gate.md`.

## Conventions

- Start every file with a header: purpose, inputs, outputs, command.
- One verb per file. Do not mix a generator and a test.
- Generators write only to the folders their header names.
- Do not commit `__pycache__/`, scratch patches or caches.
