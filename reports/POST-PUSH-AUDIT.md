# EkGuru — Post-Push Deep Research + Forensic Audit + Fix All

Command: `EkGuru_PostPush_Deep_Research_And_Fix_All.md` (36 sections)
Date: 2026-09-11 · Method: independent inspection of current repo + live `https://ekguru.shop/`, real Chromium (Playwright), plus the existing toolchain re-run. No prior report was trusted.

---

## 1. Research findings (by severity)

### CRITICAL — fixed
1. **Apps Script relay was fail-open.** `tools/apps-script-mailer.gs` only checked the shared token *if one was configured*; with `MAILER_SHARED_TOKEN` empty, anyone with the public `/exec` URL could send as the owner. → **Now FAIL-CLOSED**: `doPost` refuses (`"Not authorised."`) until a token exists, and again on mismatch. `doGet` health now reports `configured:true/false`. Client (`js/mailer.js`) already classifies this as AUTH and walks to the next provider, so no mail is lost.

### HIGH — fixed
2. **Keyword stuffing (site-quality/AdSense risk).** 540 pages carried a 2.4 KB `<meta name="keywords">` blob, and `js/seo.js` injected ~26 more keyword channels at runtime (`keywords-extended`, `long-tail-keywords`, `audience/location/intent-keywords`, `og:keywords`, `article:tag` ×120, `video:tag` ×90, etc.). Google ignores meta-keywords for ranking; the pattern reads as stuffing. → **All removed**: static tags stripped from all 540 files; the runtime injection deleted from `js/seo.js`; `js/seo-engine.js` (36 KB phrase generator) reduced to a stub that keeps only the legitimate schema.org `knowsAbout` entities. Title/description/canonical/OG/Twitter/JSON-LD all verified intact afterwards.
3. **Hreflang duplicates.** 37 pages listed each language twice (`en` + `en-US`, `es` + `es-ES`, …) pointing at the same URL. → Deduped to one bare `hreflang` per language + `x-default` (the pages are language variants, not region variants).
4. **Desktop CLS 0.186 → 0.023.** Two root causes, both fixed:
   - The static hero lead was a truncated sentence; `js/i18n.js` swapped in the full text ~220 ms after first paint, growing the hero by 63 px. Static text now matches the i18n `en` value exactly.
   - The homepage prerender had **3 tutor cards** (Tara missing — the same "forgotten hand-edit" bug the registry warns about); `main.js` then injected the 4th. Tara's static card added (honest data: rating 5.0, no fake review/lesson counts). Mobile CLS: 0.013 → **0**.
5. **Privacy scanner CSV parser.** `tools/privacy.js` used `line.split(",")` → false positives/misses on quoted commas, escaped quotes, multiline cells. → Replaced with an RFC-4180 parser (quotes, `""` escapes, embedded newlines, UTF-8 BOM) + unit-tested. Live sheet scan: 4 sheets, 0 secrets, 0 sensitive, PASS.

### MEDIUM
6. **Tara's photo is still a placeholder** (`images/placeholder-tutor.jpg`); `images/tara.jpg` does not exist. Not fabricated — kept honest and already flagged by the admin "No real photo" check. Needs the owner's real image.
7. **Content self-similarity:** release-decision reports 210 VERY_HIGH self-similar pairs in a city/topic template cluster. Remediation is a content task (planned, not hidden).

### LOW
8. **EmailJS unconfigured** (empty `serviceId/templateId/publicKey`) — confirmed NOT counted as an active fallback anywhere.
9. Stale zip/bundle references in reports updated (v1/v2 → v4; 8de5b69 → edc76a7a).

---

## 2. Current live build

**MATCHING.** Every key file on `https://ekguru.shop/` is byte-identical to local:
`index.html`, `js/site-config.js` (status `"live"`), `js/features.js` (timezone `<select>`), `js/schedule.js`, `js/mailer.js`, `js/main.js`, `js/toast.js`, `toolbox/hindi-quiz/index.html`. Live CSS = 79,347 bytes = local. The old "stale / Coming Soon" state is gone. *(The fixes in this report are committed locally and await the next push.)*

## 3. URL health

`tools/live-crawl.js` against production: **565/565 OK, 0 redirects, 0 not-200**. `robots.txt` 200 + sitemap declared; `ads.txt` 200 + publisher id matches; homepage canonical `https://ekguru.shop/` 200.

## 4. SEO / content / tools

- `tools/seocheck.js`: 555 pages, 21,564 links, **0 broken, 0 orphans**, sitemap 13 files / 550 URLs — PASS.
- Tools verified in a real browser (empty/normal paths, no console errors): quiz, flashcards, level-test, plus learn/daily-hindi/answers/localized pages.
- Meta keywords removed site-wide; title/description/canonical/JSON-LD intact (verified in Chromium).

## 5. Email / booking / admin

- Apps Script `GET /exec` → HTTP 200 health JSON. `POST` → refused until the server-side `MAILER_SHARED_TOKEN` is set (fail-closed, by design).
- FormSubmit (internal copy) → `success:true` live. Visitor/stranger leg: refused by FormSubmit by design; Web3Forms unverifiable from this datacenter; Apps Script awaiting token. No "DELIVERED" claim made.
- Booking E2E: Tutor A/B honest routing (`TUTOR_EMAIL_UNAVAILABLE`, internal ACCEPTED, student leg external) — re-run, exit 0.
- Admin: bookings table now shows **`TUTOR EMAIL: UNAVAILABLE · FALLBACK: EKGURU INTERNAL`** with a tooltip pointing at the configure-later location.

## 6. Performance (local build, real Chromium)

| Metric | Desktop 1440×900 | Mobile 390×844 |
|---|---|---|
| TTFB | ~3.6 ms | ~2.1 ms |
| LCP | ~212 ms | ~160 ms |
| CLS | **0.023** (was 0.186) | **0** (was 0.013) |
| Load | ~559 ms | ~484 ms |
| Requests / bytes | 39 / 1.1 MB | 39 / 1.1 MB |

`reports/performance-budget.json` written.

## 7. Security

No `eval`/`new Function`/`document.write`; `innerHTML` paths escape user input (`esc()`); `window.open` uses `noopener`; no secrets/API keys in `js/` or `tools/` (broad scan clean); privacy scan 627 files, 0 secrets.

## 8. AdSense

Readiness **12/12** (readiness checks only — approval is Google's decision and is never claimed). The keyword-stuffing removal addresses the most likely site-quality objection. ads.txt/ownership code present.

## 9. Files changed (this turn)

- `tools/apps-script-mailer.gs` — fail-closed token; `configured` in doGet
- `tools/APPS-SCRIPT-SETUP.md` — fail-closed docs
- `tools/privacy.js` — RFC-4180 CSV parser
- `js/seo.js` — keyword-delivery engine removed (title/desc/canonical/JSON-LD kept)
- `js/seo-engine.js` — stubbed (entities only)
- `admin.html` — explicit `TUTOR EMAIL: UNAVAILABLE · FALLBACK: EKGURU INTERNAL`
- `index.html` — Tara static card added; hero lead text matches i18n; critical-CSS CLS guard
- `find-tutors.html`, `join.html`, `tutor.html` — critical-CSS CLS guard
- 540 × `*.html` — `<meta name="keywords">` removed
- 37 × `*.html` — duplicate region hreflang removed
- `reports/performance-budget.json` — new
- `reports/POST-PUSH-AUDIT.md` — this report
- `reports/master-requirements.json` — R119/R127/R148 → PASS (deployment verified); counts now PASS 287 · PARTIAL 97 · DEGRADED 6 · FAIL **0** · DEFERRED 25 · N_A 28 · READY 1 · PASS_LOCAL 7 = 451

## 10. Tests run

`node tools/privacy.js --sheets --live --json` (PASS) · `node tools/seocheck.js` (PASS) · `node tools/live-crawl.js` (565/565) · `node tools/doctor.js` (11/11) · `node tools/release-decision.js` (**GO**) · `python3 tools/test-email-e2e.py` (exit 0) · `python3 tools/test-data-sources.py` (26/0) · Playwright: motion 31/31, timezone ×2, 19-page console crawl (0 errors), CLS measurement ×3.

## 11. Remaining (honest, external)

1. **Push** this turn's fixes to `github.com/ekgurulearning/EkGuru` (no credentials in this sandbox — push attempts fail auth; everything is committed locally).
2. **Apps Script token deploy** — owner runs `mintToken` + redeploy, wires the same value into the client at deploy time (server-side secret; repo ships `token:""`).
3. **Web3Forms live check** from a residential browser (datacenter-blocked here).
4. **Tara's real photo** (placeholder until provided).
5. **Content cluster remediation** (210 self-similar pairs) — editorial task.
