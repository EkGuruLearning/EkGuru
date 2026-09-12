# Owner Release Commands (Phase 3)

Run these on YOUR machine, in the EkGuru repo, after pulling the Phase 3 build.
⚠️ Your GitHub repo was reset to a single "Initial commit" (ba859a9, 2026-09-11) that contains the OLD site plus `live-sheets/*.csv`. The full correct history lives in the Phase 2/3 build. A normal push will be REJECTED (non-fast-forward). Follow exactly:

## 1. Point git at your repo (only if `git remote -v` is empty)
```
git remote add origin https://github.com/ekgurulearning/EkGuru
```

## 2. Put the full Phase 2+3 build on top of main (FORCE, because of your reset)
```
git fetch origin
git checkout main
git add -A
git commit -m "Phase 2 + Phase 3 build"          # only if there are uncommitted changes
git push --force-with-lease origin main          # safer than -f: fails if someone else pushed
```
If `--force-with-lease` refuses, inspect `git fetch origin && git log origin/main --oneline -3` first. Only use `git push -f origin main` if you are sure the "Initial commit" history is disposable (the `live-sheets/*.csv` files ARE included in the Phase 3 build, so nothing is lost).

## 3. Verify the push
```
git ls-remote origin main     # must show the SAME hash as: git rev-parse HEAD
```

## 4. Verify Pages deployment
- GitHub repo → Settings → Pages → confirm source branch is `main` (root).
- Wait for the Pages build, then open https://ekguru.shop/ and confirm:
  - `/materials/` returns 200 (no longer 404)
  - `/faq/` returns 200
  - `/js/recovery.js` returns 200
  - home page footer shows the new build (check `sw.js` version bump)

## 5. Re-run live health
```
node tools/doctor.js
```
Then open `/admin.html` → Release status → the ladder should now show PUSHED / DEPLOYED / LIVE VERIFIED as GREEN only after you personally confirm each.

Never paste any token, password, or mailbox secret into chat or into a public file.
