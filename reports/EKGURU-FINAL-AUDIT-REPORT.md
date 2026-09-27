# EkGuru — Final Audit Report (master audit)

**Date:** 2026-09-27
**Branch:** `arena/01a0e08b-ekguru` (base `dfa30ad7f91c4cec44c868f014292b333d3203db` = origin/main tip)
**Live site:** https://ekguru.shop
**Per-phase detail:** `reports/phase-results.json` · **Forensics:** `reports/content-forensic.json` · **Inventory:** `data/quality/full-page-inventory.json`

> **Truth rules applied throughout:** every number is counted from repository data or observed via `fetch_page`; nothing is estimated. No tutors, reviews, ratings, lesson counts, traffic, AdSense state, affiliate IDs, payment state, verification, statistics, publisher/merchant/Razorpay/CMP IDs, addresses, registrations, offices, certifications, partnerships or awards were created or fabricated. Unknowns stay unknown; live production output wins over the repo for production status; account-side items stay owner actions. Google AdSense approval is neither claimed, predicted nor implied anywhere in this audit.

---

## 1. Executive summary

The repository was audited end-to-end (24 phases) and hardened. The central defect found was a **content-integrity hole**: the runtime fetched the owner's Google Sheet on every page load and re-published its values over the repo — and the live Sheet still carried an external marketplace's metrics for one tutor (5.0 rating / 3 reviews / 40 lessons), her marketplace profile URL (rendered as a CTA button + `sameAs` in the Person schema), a bio self-introduction under a nickname that contradicted her canonical display name, and three review rows that belong to that marketplace. This was proven live (the production homepage still served all of it on 26–27 Sep 2026 even after the repo zeroed the numbers).

The fix has two halves:

1. **Data** — the sheet records, the baked override snapshot, the tutor files and the generated pages all now agree: Sushila G. publishes 0/0/0 (no on-site reviews exist), no marketplace link, and the canonical name in her bio.
2. **Code gates** — the sync pipeline now *refuses* the problematic cells regardless of what the Sheet contains: `js/sheet.js` (runtime, all three apply paths), `js/reviews.js` (marketplace-sourced reviews skipped), mirrored in `tools/sheetsync.js` (build side), with the `sameAs`/CTA/excerpt-label removed from `js/seo.js`, `js/main.js` and `tools/build-tutor-pages.js`. A new adversarial regression pass in `tools/test-sheet-apply.js` hands the loader the exact stale row and asserts none of it leaks — a regression now fails the suite.

**Every repo-controllable gate passes.** What remains is owner-owned: correcting the live Sheet, redeploying production, and the account-side Google setup (certified TCF CMP, Search Console, AdSense review request). Until then, **live production fails the content-freshness gate and the repo's PASS does not make the live site PASS.**

**FINAL STATUS: `CONTROLLABLE_READY_OWNER_ACTION_REQUIRED`**

---

## 2. What was verified and done (by gate)

### 2.1 Content forensics (Phase 2) — PASS

- 34 findings classified (`reports/content-forensic.json`): KEEP / REWRITE / REMOVE / NOINDEX / RESEARCH, each with file, line, match, classification and replacement.
- **Second full-tree grep after fixes:** **zero** preply/italki attribution in any published page or rendered string. `tutor/`, `index.html`, `find-tutors.html`, all language homes, join pages: 0. `js/i18n.js`: 0.
- Remaining mentions, all classified and non-published: (a) the new enforcement code itself (gate comments + `MARKETPLACE_SOURCES`), (b) `preplyUrl: ""` empty values, (c) the legitimate `/ask/` editorial comparison pages and the links/URLs that point to them (search-index, sitemaps), (d) the private noindex `admin.html`, (e) the owner's record fields in the CSV packs (documented as record-only), (f) internal audit artifacts (`data/`, `reports/`, `research/`), (g) build tooling.
- Known prior findings re-verified against the repo (not assumed): Preply attribution ✓ removed, "Source profile: 5.0" ✓ removed, Sashi/Sushila mismatch ✓ fixed, external ratings ✓ gated, stray 5.0★ ✓ gone from repo (live-only residue noted in §7).
- No `Math.random`/lorem/sample content; the single "coming soon" is an honest feature counter; "verified" occurrences are data-process or negative-form (the badge is not publicly rendered); "best/official/guaranteed/certified" are listicles or negative-form; no competitor CDN images; the IndexNow key is by-design public.

### 2.2 Tutor data (Phase 3) — PASS

Source of truth = registry-ordered `js/tutors/*.js` + generated `js/tutors/_overrides.js`, loaded identically in browser and build by `tools/lib/site-data.js` (no second truth file was created — the loader's contract forbids re-implementing the transforms).

| Tutor | State | Evidence |
|---|---|---|
| sushila-g | **published** — $6/50min, 3yr, verified, 0/0/0, preplyUrl `""`, bio "My name is **Sushila**" | file + override + regenerated pages + sheet row all agree |
| shikha-dutta | **published** — $8/50min, 16yr, verified, 0/0/0 | unchanged, verified |
| hemlata, tara | **sheet-hidden** (`active=no`) — noindex profile pages, out of roster/sitemaps | by design; live sheet showed them visible (stale) → owner intent needed |
| sarshtee-baliyan | legitimate **draft** — noindex, not in registry | by design |

- **Name mismatch fixed:** bio now matches the canonical display name "Sushila G." (sheet `name` column, "shown everywhere"); "Sashi" remains the booking-form nickname only. **Owner to confirm with the tutor** which name she prefers.
- **3 marketplace review rows removed** from `csv/ekguru_reviews.csv` and `live-sheets/reviews.csv` (source=preply: Tomasz, Jon, Matthew).
- Sheet `#help` rows rewritten to the 27 Sep record-only policy (rating/reviewsCount/lessonsCount/superTutor/preplyUrl = owner's records; the site derives from on-site data only).

### 2.3 The sync-contract gates (new, this session)

| Layer | Gate | Where |
|---|---|---|
| Runtime apply | `rating`, `reviewsCount`, `lessonsCount`, `superTutor`, `preplyUrl` transforms return `null` → never applied (update, create **and** record-only paths all skip nulls); `verified` kept (owner flag, not publicly rendered) | `js/sheet.js` FIELDS |
| Runtime reviews | rows with external-marketplace `source` skipped with logged reason; ratings derive from site-native reviews only | `js/reviews.js` |
| Build sync | identical policy in `buildTutor` + `buildReviews`, so `_overrides.js` can never bake them back | `tools/sheetsync.js` |
| Runtime SEO | Person schema: no `sameAs` to marketplace, no "profile excerpt" meta-label | `js/seo.js` |
| Profile UI | Preply CTA gone (card + sidebar); review label = "Left through EkGuru"; join-form field genericised | `js/main.js` |
| Pre-rendered pages | CTA, sameAs, excerpt label, marketplace review source text removed; regenerated | `tools/build-tutor-pages.js` |
| Home cards | "Source profile: ★…" and "…lists N lessons" wording gone; on-site reviews only | `tools/build-home-tutors.js` |
| Strings | `pf.preply*`, `pf.sourceUnverified`, `pf.profileLessons`, `hero.stat2` removed (7 markets); `pf.leftOnSite` added; `tutors.all` = "Find My Guru" → `/find-tutors.html` | `js/i18n.js` + 7 homepages |
| Regression | adversarial third pass: exact stale row (5/3/40/superTutor/marketplace URL) → none leaks, ordinary cells still apply | `tools/test-sheet-apply.js` (34/34) |

### 2.4 SEO hard gate (Phase 7) — PASS

- Every indexable page canonicalises to `https://ekguru.shop/<path>` (0 mismatches); one H1 per page; unique title/meta (0 duplicate title groups, 0 duplicate meta groups).
- hreflang spot-checks (home, find-tutors, tutor, learn): 7 locales + `x-default`, absolute URLs, mutually consistent.
- No `AggregateRating` schema anywhere — no rating without real evidence.

### 2.5 Thin-page gate (Phase 8) — PASS

`thin_indexable = 0`; `indexable_not_in_sitemap = 0`; `noindex_in_sitemap = 0`; `orphan_indexable = 0`; `broken_link_total = 0`. 962 short pages exist but are **all noindex** research/utility surfaces (triage list, not a publication defect), none carries ads. The last indexable exception — the Google Search-Console token file — was wrapped in a minimal noindex HTML page with the token line preserved byte-for-byte (plus viewport + main).

### 2.6 Languages (Phase 9) — PASS

Recounted from disk 27 Sep (all match `reports/EKGURU-GLOBAL-LANGUAGE-STATUS.md`): **700** registry languages; readiness 733 (READY 71 / PARTIAL 191 / RESEARCH_REQUIRED 438 / NOT_FEASIBLE_YET 33); priority 700 (P0 12 / P1 54 / P2 85 / P3 367 / P4 182); **1,983** country relations; **89** course codes, **10 complete A1–C2** (es fr gu hi mr pa ta te ur zh), 18 languages with any indexable course surface. No country-name-substitution content; no mass near-identical SEO pages; copy-index originality: 0 duplicate groups across 1,665 page fingerprints.

### 2.7 Course-level claims (Phase 10) — PASS

`data/courses/index.json` (hi: `complete=true`, 6 CEFR levels × 6 lessons × 10 test_items, A3 extension published, PUBLISHABLE_COMPLETE). On-page claims ("A1 to C2, 36 lessons") match authored content exactly (6×6=36). `test-course-levels.mjs` 29/29, `test-course-placeholders.mjs` 7/7.

### 2.8 Sitemaps / robots / ads.txt (Phases 11–12) — PASS

Sitemap index + 15 children all exist and consistent; robots declares the sitemap and Disallows only `/admin.html`, `/tools/`, `/search/` (public `/toolbox/` explicitly allowed — the v71 fix intact). **ads.txt is unchanged: exactly** `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0` — verified in repo and live (`/ads.txt` re-fetched 26–27 Sep).

### 2.9 Legal / consent / page classes / monetization (Phases 13–16) — PASS

- 7 trust/legal pages: substantive, indexable, single-H1, canonicalised. No invented address/registration/office/certification/partnership/award (the old Jaipur-address TODO was **not** added).
- Consent: fail-closed (`ADVERTISING_AVAILABLE=false`), honest copy, never described as a Google-certified CMP, no invented CMP IDs. **Owner** must configure a Google-certified TCF CMP for EEA/UK/CH account-side before personalised serving.
- Ads: `ADS_RUNTIME_ENABLED=false` (triple-gated injector); 0 ads on all 12 excluded page classes; no fake buttons/ads styled as tutor cards.
- Affiliate: registry empty + master switch off; `test-affiliate-disclosure.mjs` green; default-disabled as required.

### 2.10 Security / a11y / mobile (Phases 17–18) — PASS

No secrets in repo; HMAC verified before body parse (Razorpay server); admin private + noindex + Disallowed; new-tab links `rel=noopener`. Mobile: 0 viewport issues across 2,637 pages. A11y: 0 flags on indexable pages; the 3 remaining flags are all noindex internal surfaces (private dashboard, token file, internal email preview).

---

## 3. Tests and preflights (Phases 19–21)

| Suite | Result |
|---|---|
| `node tools/test-sheet-apply.js` | **34/34** (incl. new stale-sheet regression pass) |
| `node tools/test-browser-qa.mjs` | 26/26 |
| `node tools/test-runtime-qa.mjs` | 142/142 |
| `node tools/test-consent-release.mjs` | 12/12 |
| `node tools/test-ad-policy.mjs` | 18/18 |
| `node tools/test-affiliate-disclosure.mjs` | pass |
| `node tools/test-course-levels.mjs` | 29/29 |
| `node tools/test-course-placeholders.mjs` | 7/7 |
| `node tools/test-question-api.mjs` | 32/32 |
| `node tools/test-search-facets.mjs` | pass (82 countries, 16 languages, 341 pages) |
| `node tools/test-copy-index.mjs` | pass (1,665 fingerprints) |
| `test-shell-drawer / test-experience-dom / test-level-visuals (35) / test-offline-playable (21) / test-print-sheet-dom (17) / test-print-visible (27) / test-refresh-quiet (26)` | all pass |

Preflights (Phase 20) — all four exist and pass (none `COMMAND_MISSING`):
- `python3 tools/audit-adsense-readiness.py --selftest` → ok
- `python3 tools/audit-adsense-readiness.py` → `pages=2634 thin=962 thin_indexable=0 ads=0`
- `node tools/adsready.js --local` → **13/13**
- `python3 tools/build-all.py check` → **"every generated layer is up to date"**

Environment notes: `npm install` was required (jsdom devDependency; `node_modules` absent at start). `tools/test-data-sources.py` and `tools/test-sheet-loader.js` need outbound HTTPS to `docs.google.com`, which this sandbox blocks (TLS EOF before parsing) — **UNKNOWN in-sandbox**, not a code failure; run them in CI. Playwright/Chromium rendered QA cannot run here (no browser binary) — the project-native jsdom suites cover the browser path and are green.

---

## 4. Live QA (Phase 22) — BLOCKED (owner-owned)

`fetch_page https://ekguru.shop` (26–27 Sep 2026) shows production serving the **pre-remediation state**: Sushila hero "★★★★★ 5.0"; card "★★★★★ 5.0 · 3 reviews · 40 lessons" (marketplace lessons); bio "Hello! My name is Sashi…"; all 5 tutors visible (live sheet `active=yes` for hemlata/tara contradicts the repo's `active=no`); "0 Tutor profiles" hero stat; "Profile prices from $6" (honest). Live `/ads.txt` serves the correct authorised line.

- **Repo PASS ≠ live PASS; live wins for production status.** The stale Sheet overrode the repo's zeroing on every page load — which is why the code gates exist: after a redeploy, the stale Sheet can no longer re-publish marketplace metrics, the profile link or marketplace reviews, even before the owner fixes it.
- The Sheet's published CSV endpoints are unreachable from this sandbox (SSL 35 / HTTP 500), so the live Sheet state was inferred from the `live-sheets/` snapshots (last touched at base commit) plus observed live behavior — they match.

---

## 5. Blockers

1. **Live production behind HEAD** (content freshness + the stale-override hole closed only in code) — owner redeploy.
2. **Live Sheet uncorrected** — owner update (the runtime now refuses its bad cells, but owner records should agree with the site).
3. **Google-certified TCF CMP** not configured (account-side) — required before any personalised serving in EEA/UK/CH.
4. Rendered-browser (Playwright) + network-dependent suites not runnable in this sandbox — CI/owner action.

None of these is repo-controllable.

## 6. OWNER_ACTION_REQUIRED (in order)

1. **Update the live Google Sheet** (URLs/gids in `js/site-config.js`, gids: tutors 1631273256, reviews 298809212): `sushila-g` → rating `0`, reviewsCount `0`, lessonsCount `0`, superTutor `no`, preplyUrl **blank**, bio "My name is Sushila…"; remove or hide the 3 marketplace-sourced review rows (Tomasz, Jon, Matthew); set `hemlata`/`tara` `active` per owner intent (repo says hidden; live says visible).
2. **Confirm with Sushila** which name she wants displayed ("Sushila" vs "Sashi"). If it differs from the current canonical, change the sheet `name` column and rebuild the URL/profile.
3. **Redeploy production from this branch's HEAD**; hard-refresh verify `/`, `/ads.txt`, `/tutor/sushila-g/` (expect: 2 tutor cards, no star chips, "No on-site reviews yet", no Preply button, "My name is Sushila").
4. **Search Console:** property health, submit `https://ekguru.shop/sitemap-index.xml`, spot-inspect 5 representative URLs.
5. **AdSense console:** configure a Google-certified TCF CMP for EEA/UK/CH and test from 3 European IPs; **then** request site review.
6. **Only after approval:** set `ADS_RUNTIME_ENABLED=true` in `js/monetization/monetization.js` with vignette/anchor/multiplex/Offerwall **off**.
7. **CI/connected machine:** run `python3 tools/test-data-sources.py`, `node tools/test-sheet-loader.js` and the Playwright rendered-QA path.

## 7. Files changed (this session)

Code gates: `js/sheet.js`, `js/reviews.js`, `tools/sheetsync.js`, `js/seo.js`, `js/main.js`, `tools/build-tutor-pages.js`, `tools/build-home-tutors.js`
Tutor data: `js/tutors/sushila-g.js`, `js/tutors/_overrides.js`, `js/tutors/hemlata.js`, `js/tutors/tara.js`, `tutors-sheet.csv`, `csv/ekguru_tutors.csv`, `live-sheets/tutors.csv`, `csv/ekguru_reviews.csv`, `live-sheets/reviews.csv`
Strings/pages: `js/i18n.js`, `index.html`, `join.html` + `ar|de|es|fr|ja|pt/join.html`, 6 language homepages, `robots.txt` (comment), `googleb3b0e3defc1daa17.html`
Regenerated: `index.html` (tutor block), `tutor/sushila-g/index.html`, `tutor/shikha-dutta/index.html`, `feed.xml`, `data/copy-index.json`, `data/quality/full-page-inventory.json`, `data/quality/adsense-readiness.json`
Test: `tools/test-sheet-apply.js` (rewritten to the new contract + regression pass)
Reports: `reports/content-forensic.json` (second grep COMPLETE), `reports/EKGURU-GLOBAL-LANGUAGE-STATUS.md` (re-verified), `docs/ADSENSE-FINAL-REVIEW-PACKET.md` (addendum), `reports/EKGURU-MONETIZATION-READINESS.md` (addendum), `reports/phase-results.json`, `reports/EKGURU-FINAL-AUDIT-REPORT.md`

## 8. FINAL STATUS

**`CONTROLLABLE_READY_OWNER_ACTION_REQUIRED`** — every repo-controllable gate (content forensics, tutor data truth, homepage, profiles, booking safety, SEO, thin pages, language matrix, course claims, sitemaps/robots, ads.txt, legal, consent, ad page classes, monetization, security, a11y/mobile, test suite, preflights, jsdom browser QA) passes with evidence; the remaining items are the owner's Sheet update, production redeploy, and Google account-side setup.

Google AdSense approval remains Google's decision and is not guaranteed by this audit.

---

## 9. Addendum — second execution, 2026-09-27 (ultra-deep re-verify + build-side hardening)

Command: "ULTRA DEEP AUTONOMOUS IMPLEMENTATION" + "FINAL ULTRA-HEAVY REPAIR" — every prior PASS re-proven from the current tree; new controls implemented where the command required them.

**Re-verified (not trusted from memory):** all 4 preflights re-run green; full inventory regenerated (2,637 / 1,007 / 1,630, all consistency gates 0); language registries recounted; live `/`, `/ads.txt`, `/robots.txt`, `/tutor/sushila-g/` re-fetched; second-generation forensic grep over **post-build** output: 0 competitor words, 0 attribution phrases, 0 stale strings.

**Live drift re-proven (DEPLOYMENT_DRIFT):** production still serves "0 Tutor profiles", "★★★★★ 5.0 · 3 reviews · 40 lessons", "My name is Sashi", 5 visible tutors, the old CTA, and — newly found — the "Imported weekly times" caption on the tutor page. `/ads.txt` is current. Deployment = owner merge (GitHub Pages from `main`).

**New engineering controls (all green, all wired into `build-all.py check`):**
- `tools/test-sheetsync-policy.js` (new, 10/10) — build-side anti-regression: `sheetsync.js` refactored to export `buildTutor`/`buildReviews` behind a `require.main` guard; the adversarial stale row (5/3/40/superTutor/marketplace URL) provably bakes nothing on the build side, mirroring the runtime gate proven by `test-sheet-apply.js`.
- `tools/test-no-competitor-attribution.js` (new) — build-fail gate over 2,562 public HTML + 105 public JS files: no marketplace links, no attribution phrases in public HTML or rendered JS strings (comment-aware scanner), every absolute URL on a calibrated allowlist, canonical/hreflang/og self-referencing `https://ekguru.shop`, no non-empty `preplyUrl` literal, no `sameAs` from `preplyUrl`.
- `.github/workflows/ci.yml` (new) — connected-CI home for what this sandbox cannot run: network data-source tests, the full jsdom suite, master build check. First Actions run happens on push/PR.

**Fixes the new gate + live inspection surfaced (all at the source, then rebuilt):**
- `find-tutors.html` — "imported profile schedule" → "tutor-provided schedule"
- `tools/build-tutor-pages.js` — rendered caption "Imported weekly times for …" → "The tutor-provided schedule for …"
- `js/seo.js` — runtime FAQ JSON-LD "imported USD prices … external-platform terms" → tutor-stated wording

**New evidence artifacts:** `reports/tutor-data-audit.json` (loader-generated, 0 leaks), `reports/public-page-ad-readiness.json` (810/1,827/0 runtime), `reports/source-of-truth-map.json` (13 entities + anti-stale-fallback contract), `reports/current-execution-baseline.json`, `reports/EKGURU-MASTER-EVIDENCE.json` (final_status: **DEPLOYMENT_DRIFT**).

**Status change:** `CONTROLLABLE_READY_OWNER_ACTION_REQUIRED` → **`DEPLOYMENT_DRIFT`** — the accurate value per the audit's own vocabulary, because live production demonstrably fails the content gates until the PR is merged. Everything repo-controllable is done and gated; the owner's actions are unchanged in substance (merge, sheet update, name confirmation, CMP, Search Console, AdSense review, post-approval flag flip).

Google AdSense approval remains Google's decision and is not guaranteed by this audit.
