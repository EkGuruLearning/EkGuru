# tests/

Today this folder holds only fixtures (`fixtures/*.tsv`, sample sheet tabs for
the sheet-policy tests). The 111 `test-*` scripts still live in `tools/`.

Migration phase 1 moves them to `tests/unit/` (see
`docs/architecture/REPO-STRUCTURE.md` §6). Target shape:

```
tests/
├── fixtures/      sample data
├── unit/          python and node tests that read the repo
├── data-sources/  tests that call live endpoints (CI only)
└── e2e/           Playwright journeys
```

Rules: tests may read `src/`, `data/` and the generated site; they never write
files the site serves; a generator never imports from here.
