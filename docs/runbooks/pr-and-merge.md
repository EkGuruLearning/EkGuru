# Runbook: branch, pull request, CI, merge

One concern per PR. `main` deploys to the live site through GitHub Pages, so a
merge is a release.

## 1. Branch

```bash
git checkout main && git pull origin main
git checkout -b fix/<short-topic>        # or feat/ docs/ seo/
```

## 2. Gate locally

Run [`regenerate-and-gate.md`](regenerate-and-gate.md). `python3 tools/build-all.py check`
must exit 0.

## 3. Commit

Imperative subject, a body that says what changed and why. A PR that changes
generated output must also change its generator or source.

## 4. Open the PR

With the GitHub CLI:

```bash
git push -u origin <branch>
gh pr create --base main --title "<title>" --body-file <file>
```

If GraphQL is blocked in your environment, the REST route works:

```bash
gh api -X POST repos/EkGuruLearning/EkGuru/pulls \
  -f title="<title>" -f head="<branch>" -f base="main" -F body=@<file>
```

The PR body: what changed, why, how it was checked, and a test plan with the
two CI jobs below.

## 5. CI must be green

| Job | Covers |
|---|---|
| `checks` (`ci.yml`) | Indexing contract, master gate, content gates, readiness, sheet policy tests, tutor activation, output gates |
| `journeys` (`playwright.yml`) | Playwright run of the five public user journeys in Chromium |

`course-health.yml` and `live-guard.yml` are scheduled jobs; they do not block a PR.

```bash
gh api repos/EkGuruLearning/EkGuru/commits/<full-sha>/check-runs \
  --jq '[.check_runs[]|"\(.name)=\(.status)/\(.conclusion)"]'
```

## 6. Merge

Merge on the **full 40-character head sha**; a short sha is refused.

```bash
gh api -X PUT repos/EkGuruLearning/EkGuru/pulls/<n>/merge \
  -f sha=<full-40-char-head-sha> -f merge_method=merge -f commit_title="<title> (#<n>)"
```

If `main` moved and the merge reports a conflict, merge `main` into the branch.
Conflicts in generated files (`reports/*.json`, inventories) are resolved by
regenerating, not by hand-editing. Then re-run the gate and CI.

## 7. After the merge

- Live site updates through GitHub Pages in a few minutes.
- If the change needs owner action (Apps Script redeploy, `feed.url`, Search
  Console), say so in the PR and in
  [`owner-manual-steps.md`](owner-manual-steps.md).

## Never

- Commit or push personal data to this public repo.
- Merge with a red check, or skip the gate.
- Edit `data/quality/*` by hand to make a gate pass (the one exception is
  `owner_approved_new_indexable`, with a decision record).
