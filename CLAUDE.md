# EkGuru: rules for AI assistants working in this repo

Read `README.md` and `docs/architecture/REPO-STRUCTURE.md` first. Then follow
these. They come from real failures in this repo.

## Before you change files

- A root folder is a public URL. Never move or rename one.
- Find the generator before editing a page. Edit the generator or its source.
- Check `docs/ROADMAP-FIXES.md` for the item you are about to do.

## Regeneration and gate

- Use the sequence in `docs/runbooks/regenerate-and-gate.md`, in order.
- `python3 tools/build-all.py check` must exit 0 before you push.
- If a run was interrupted and hundreds of files show as modified, re-run the
  whole sequence. Do not commit the stripped state.

## Indexing

- New pages are noindex. Do not edit the `pages` map in
  `data/quality/indexing-baseline.json`. An owner-approved new page goes under
  `owner_approved_new_indexable` with a decision record.
- Update the page count in `tools/test-reading-layer.mjs` when pages are added.

## Content honesty

- Do not bulk-generate course text. A language is publishable only with a
  native reviewer's record; you cannot create one.
- Do not add claims the site cannot back up ("verified", "native", counts).

## Privacy and secrets

- The repo is public. No emails, phone numbers, private Drive links or secrets
  in commits, PRs or docs. Applicant-level findings go in a private file.
- Never commit `deploy-secrets.local.json` or `*.local.csv`.

## Git and PRs

- One concern per PR. Branch names `feat/ fix/ docs/ seo/`.
- Follow `docs/runbooks/pr-and-merge.md`. Merge only when `checks` and
  `journeys` are green, on the full 40-character head sha.
- If an action is blocked by a permission prompt or a policy check, do not work
  around it. Report it and leave it undone.

## Owner-only steps

Apps Script deployment, `feed.url`, Search Console and hosting settings are the
owner's. Merging does not deploy Apps Script. See
`docs/runbooks/owner-manual-steps.md`.
