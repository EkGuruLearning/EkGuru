# Contributing to EkGuru

This applies to people and to AI assistants alike.

## Before you change anything

1. Read [`docs/architecture/REPO-STRUCTURE.md`](docs/architecture/REPO-STRUCTURE.md).
   A root folder is a public URL; do not move it.
2. Find out whether the file is generated. If a generator writes it, change the
   generator or its source data.
3. Check [`docs/ROADMAP-FIXES.md`](docs/ROADMAP-FIXES.md) so you do not duplicate
   or contradict an open item.

## The workflow

| Step | Do | Detail |
|---|---|---|
| 1 | Branch from `main` | `feat/`, `fix/`, `docs/`, `seo/`. One concern per PR |
| 2 | Change the source | Never hand-edit a generated page |
| 3 | Regenerate | [`docs/runbooks/regenerate-and-gate.md`](docs/runbooks/regenerate-and-gate.md) |
| 4 | Gate | `python3 tools/build-all.py check` exits 0 |
| 5 | PR | [`docs/runbooks/pr-and-merge.md`](docs/runbooks/pr-and-merge.md). Fill in the template |
| 6 | CI green | `checks` and `journeys` |
| 7 | Merge | On the full head sha |

## Hard rules

- **No personal data** in commits, PRs or docs: no emails, phone numbers,
  private Drive links, secrets. The repo is public.
- **Indexing freeze.** New pages are noindex. Making one indexable needs a
  recorded owner approval ([`docs/runbooks/add-page-or-language.md`](docs/runbooks/add-page-or-language.md)).
- **No bulk-generated course text.** A language is publishable only with a
  native reviewer's record. Code does not create review records.
- **No claims the site cannot back up.** Verified, native, certified, counts of
  tutors or languages: each must be true on the day it ships.
- **Do not weaken a gate to make it pass.** Fix the cause, or write an owner
  decision explaining the waiver.
- **Never commit** `deploy-secrets.local.json` or `*.local.csv`.

## Code conventions

- Tools: one verb per file (`build-`, `apply-`, `audit-`, `author-`, `inject-`,
  `repair-`, `test-`), each starting with a header: purpose, inputs, outputs,
  command.
- Browser code: plain JavaScript, no framework, no network call on page load
  that the page cannot work without.
- Tests: a new behaviour gets a test that runs in CI. Tests do not write files
  the site serves.
- Commits: imperative subject, body says what and why.

## Where things go

See §4 of the structure doc. In short: course data in `data/courses/`,
generators in `tools/`, browser code in `js/`, decisions in `docs/decisions/`,
how-tos in `docs/runbooks/`.

## Ownership

Owner decisions (indexing, language waivers, hosting) are made by the site
owner and written to `docs/decisions/`. CODEOWNERS and branch protection are not
yet enabled; see item 25 in the roadmap.
