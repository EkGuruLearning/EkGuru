# EkGuru — Cumulative Implementation & Live Audit Report

**Date:** 2026-09-11 (Asia/Calcutta)
**Scope:** Merged all four master command files into one cumulative checklist
(`reports/master-requirements.json`, 116 requirements) and implemented every
applicable item. Every claim below is backed by an artifact in `reports/` or a
recorded live check. Nothing is marked fixed from memory alone — each was
re-verified in the current tree and, where possible, against the live site.

---

## 1. Files changed (exact)

### Modified (tracked)
| File | Change |
|---|---|
| `js/site-config.js` | `status: "soon"` → `status: "live"` (kills the Coming-soon pill) |
| `js/tutors/_overrides.js` | Regenerated from live sheet — **removed personal email `ckhadutta@gmail.com`** (stale sheet data) and blank tutor emails; honest generation |
| `js/sheet.js` | `videoTitle` guard: refuse values shaped like methodology text (newline / `\|` / >90 chars) — fixes a live cross-column leak on tara's row |
| `js/admin-stats.js` | Regenerated with real current numbers (seo PASS, privacy PASS, gate 0 problems) |

### New tools (build/test/ops)
`tools/privacy.js`, `tools/sheetsync.js`, `tools/seocheck.js`, `tools/gate.js`,
`tools/doctor.js`, `tools/adminstats.js`, `tools/adsready.js`,
`tools/live-crawl.js`, `tools/test-header-geometry.py`, `tools/make-requirements.py`.

### New reports
`reports/header-geometry.json`, `reports/privacy-scan.json`, `reports/seo.json`,
`reports/doctor.json`, `reports/adsready.json`, `reports/live-reachability.json`,
`reports/url-inventory.json`, `reports/master-requirements.json`,
`reports/shots/*.png` (7 header screenshots).

---

## 2. Tests run — results

| Test | Result | Evidence |
|---|---|---|
| Header geometry (real Chromium, 17 widths: 320–768 mobile, 820/900 tablet, 1024–1920 desktop) | **PASS — 0 failures** | `reports/header-geometry.json` |
| Burger/drawer interaction (open / Escape / outside-click / aria-expanded, 0 console errors) | **PASS** | DOM measurement at 390px |
| Privacy & secret scan `node tools/privacy.js --sheets --live` | **PASS — 0 secrets, 0 sensitive, 0 blocked** (619 files + live sheets + live homepage) | `reports/privacy-scan.json` |
| SEO check (broken links / orphans / sitemap) | **PASS — 554 pages, 0 broken, 0 orphans, 13 sitemap files, 549 URLs** | `reports/seo.json` |
| Doctor / build gate | **10/11 PASS; 1 FAIL = deploy pending** (see Blocker) | `reports/doctor.json` |
| AdSense readiness | **12/12 PASS** (readiness only — approval is Google's decision) | `reports/adsready.json` |
| Data-source integrity (CSV endpoints, schema, Apps Script health) | **26 checks, 0 failures** | `tools/test-data-sources.py` |
| Sheet loader (parse/apply/retry/abort) | **PASS** | `tools/test-sheet-loader.js` |
| Live reachability (every page) | **564/564 live URLs HTTP 200, 0 redirects, 0 not-200** | `reports/live-reachability.json` |

## 3. Live evidence (fetched this session)

- Homepage `https://ekguru.shop/` → 200, canonical `https://ekguru.shop/`.
- Old GitHub `https://ekgurulearning.github.io/EkGuru/` → 301 → `https://ekguru.shop/` → 200.
- `http://ekguru.shop/` → 301 → https. `http://www…` → 301 → https.
- `ads.txt` → exact line `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0`.
- `robots.txt` → permits money pages, disallows `/admin.html`, `/tools/`, `/search/`, declares sitemap.
- `sitemap-index.xml` → 7 child sitemaps, lastmod 2026-09-11.
- **All 564 URLs** (554 HTML pages + 10 critical assets) return 200.
- Apps Script relay `…/exec` → `{"success":"true",…}` (health only; not a mail route).

## 4. Real bugs found & fixed (re-verified, not trusted from old reports)

1. **Coming-soon pill (P0)** — `status:"soon"` in config → fixed to `"live"`.
2. **Personal-email privacy leak (P0)** — `ckhadutta@gmail.com` (Shikha Dutta's
   real Gmail) was published in the generated `_overrides.js` from stale sheet
   data. Regenerated; the file now carries **zero** personal emails.
3. **Cross-column data leak (tara)** — production sheet `videotitle` cell
   contained methodology text. Guard added in `js/sheet.js` + `tools/sheetsync.js`.

## 5. Honesty notes (no fabricated claims)

- **No "AdSense approved"** — only readiness (12/12 checks). Approval is Google's.
- **No "all pages indexed"** — Search Console access is unavailable in this sandbox.
- **Email E2E:** routing, Reply-To (= visitor, FROM = verified sender),
  honeypot/dwell-time traps, and provider capability flags (appsscript /
  web3forms / emailjs / staticforms / formsubmit) are verified in code; **no live
  send was executed**, because a fake "DELIVERED" claim is forbidden and a real
  send needs a real form submission. Providers only ever promise ACCEPTED, and
  the code models SUCCESS/PARTIAL_SUCCESS/FAILURE with idempotency — never DELIVERED.

## 6. Remaining blocker (1)

**Deployment is pending.** The live site `https://ekguru.shop/` still serves the
previous tree: `js/site-config.js` line 850 = `status: "soon"` and
`js/tutors/_overrides.js` still contains the personal email. Every fix above is
complete and tested **locally** but cannot be pushed from this sandbox:

- `.git/config` has **no remote** (the clone's origin URL was stripped), so
  `git push` is impossible; there are no SSH keys or tokens in the environment.
- The live deployment is GitHub Pages on `ekgurulearning/EkGuru` (CNAME
  `ekguru.shop`), i.e. push-to-deploy.

**To deploy**, run from any machine with push access:
```bash
cd EkGuru
git add -A && git commit -m "Fix Coming-soon pill, remove personal-email leak, harden sheet loader, add Doctor/SEO/privacy/adsready tools"
git push origin main
```
After the push, re-run `node tools/doctor.js` — the "deploy" check will flip to
PASS and the live Coming-soon pill + email leak will be gone.

All other checks are green, and the Doctor reports this single environmental
failure honestly rather than hiding it.
