# EkGuru — AdSense Final Review Packet

Prepared 2026-09-26 against the repository (`arena/01a0deed-ekguru`, = `main` @ 8089f1e plus the remediation working tree) and the live site `https://ekguru.shop/`.

> **One-sentence status:** Every repository-controllable precondition is verified green; the remaining gates are a production redeploy and account-side Google setup — **final approval remains with Google. This packet does not claim, predict or imply that Google will approve the site.**

---

## 1. What was verified (and how)

| Area | Verification | Result |
|---|---|---|
| Publisher identity | `ads.txt` (repo + live over `fetch_page`) | Exactly one authorised line: `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0`. No other seller. Unchanged by this audit — correct ID kept, none created. |
| Ad runtime | `js/monetization/monetization.js` source | `ADS_RUNTIME_ENABLED = false` — ads are impossible to render today; the injector is additionally triple-gated (policy class, consent, runtime flag). |
| Page-class ad safety | `data-ad-class` sweep + `inject-ads.py` + adsfree tests | 0 ads on INTERACTIVE_LEARNING, UTILITY, TRANSACTIONAL, CONTACT, BOOKING, PAYMENT, ADMIN, ERROR, SEARCH, PLACEHOLDER, RESEARCH_REQUIRED, INCOMPLETE surfaces (2,636 pages tagged). |
| Content quantity/depth | `tools/audit-adsense-readiness.py` | content_depth **PASS**; thin **indexable** pages = **0** (962 low-word pages exist, all noindex research/utility surfaces — triage only). |
| Originality | audit originality + quarantine tool | 0 exact duplicate title groups; 0 exact duplicate meta groups; the 3 draft tutor pages carry unique "not published" titles. |
| Competitor-content removal | built-HTML greps | "attributed to", "Excerpt attributed", "Source profile" → **0 hits**. Review excerpts sourced from another marketplace deleted; ratings render only from on-site reviews (runtime gate: `reviewsCount > 0`). Homepage hero no longer hard-codes a 5.0★ claim. |
| Tutor numbers | `js/tutors/`, `tutors-sheet.csv` | Sushila G.: rating 0 / reviews 0 / lessons 0 / `superTutor: false` (unverifiable imports zeroed; price $6 kept = her real stated price). Verified tick retained = EkGuru's own verification decision. |
| Navigation/inventory | `tools/build-full-page-inventory.py` (2,637 URLs) | 0 broken internal links; 0 noindex-in-sitemap; 0 canonical mismatches; 1,007 indexable pages, all single-H1 + canonical + meta description (except the Search-Console verification file, intentionally plain). |
| Legal/trust | direct file audit | `about/`, `contact/`, `privacy/`, `terms/`, `cookie-policy/`, `disclaimer/`, `copyright/` — substantive, indexable, single-H1, canonicalised. |
| Consent honesty | banner + copy sweep | Local banner stores a localStorage choice only and is never described as a Google-certified CMP; analytics (GoatCounter, cookieless) load post-consent. |
| AdSense policy copy | sweep | No page claims or predicts approval; no ads-disguised-as-content patterns; no ad labels on tutor cards. |
| ads**ready** gate | `node tools/adsready.js --local --dry --quiet` | **13/13 local checks pass** (ads.txt, robots, sitemap index + 15 children, canonicals, all 7 legal pages, ≥100 substantive pages, country pages real). |

## 2. What remains before requesting review (owner actions, in order)

1. **Mirror tutor numbers into the owner Google Sheet** — `sushila-g`: rating `0`, reviewsCount `0`, lessonsCount `0`, superTutor `no` (priceUSD stays `6`). Without this, sheetsync restores the old imported numbers after deploy.
2. **Redeploy production from HEAD** — the repository (`8089f1e` + remediation, commit `ec5bba3`) is ahead of what production serves. Verified live 2026-09-26: the homepage still shows "**0** Tutor profiles", "**1.0★** Profile review average", a hard-coded "⭐ Displayed profile rating 5.0" chip, Sushila G.'s card with "★★★★★ 5.0 / 3 reviews / 40 lessons" (zeroed in the repo as unverifiable imports), the copy "Imported profiles currently list lessons from $6", and the three quarantined draft tutors through `tutor.html?id=`. Verify after redeploy: 2 tutor profiles, "prices from $6", **no** star chips on the hero card, draft tutor URLs show "not published" titles.
3. **Configure a Google-certified TCF CMP** (Funding Choices or another Google-certified provider) for EEA/UK/CH in the AdSense console, and test it from 3 European IPs. Until it exists, no personalised ads may serve in EEA/UK/CH.
4. **Search Console**: confirm property health; submit `https://ekguru.shop/sitemap.xml`; spot-inspect 5 representative URLs.
5. **Only then**: AdSense → Sites → request review.
6. **After approval only**: set `ADS_RUNTIME_ENABLED = true`; keep vignette/anchor/multiplex/Offerwall **off**; run a placement/consent pass per `docs/GOOGLE_MONETIZATION.md`.

## 3. Explicit non-claims

- No statement here or on the site says Google will approve, or has approved, EkGuru.
- Live-account facts (account standing, review status, CMP state, Search Console state) are **account-side** and were not fabricatable from this audit; they are listed as owner verifications, not results.
- The packet contains no invented seller IDs, CMP IDs, badge claims or partner claims.
- Rendered-browser QA (Playwright) could not run in the audit sandbox (Chromium download blocked); static + jsdom coverage stands, and the remaining rendered checks are listed in `reports/EKGURU-MONETIZATION-READINESS.md` §13 as an owner action, not asserted as done.

## 4. Artifacts in this packet

- `data/quality/full-page-inventory.json` — per-URL record for all 2,637 public pages.
- `data/quality/adsense-readiness.json` — greedy depth/originality/navigation/trust/SEO gate output.
- `data/quality/language-course-matrix.json` + `reports/EKGURU-GLOBAL-LANGUAGE-STATUS.md` — publishing/completeness truth for all 700 registry languages.
- `reports/EKGURU-MONETIZATION-READINESS.md` — 14-section monetization status with exact owner actions.

---

## 5. Addendum — 2026-09-27 master audit (branch `arena/01a0e08b-ekguru`, base `dfa30ad`)

Everything in sections 1–4 still holds; the numbers below were re-verified on 27 Sep against the current tree:

- **Ads.txt**: unchanged — `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0` (adsready local 13/13).
- **Inventory gate now fully clean** (was 1 exception): the Search-Console verification file `googleb3b0e3defc1daa17.html` (plain-text token) was wrapped in a minimal noindex HTML page with the token line preserved byte-for-byte. Result: `indexable_not_in_sitemap = 0`, `noindex_in_sitemap = 0`, `thin_indexable = 0`, `orphan_indexable = 0`, `broken_link_total = 0`, `canonical_mismatches = 0`, `duplicate_meta_groups_count = 0` (`data/quality/full-page-inventory.json`, regenerated 27 Sep).
- **New runtime gates close the live-sheet override hole.** Live QA on 26–27 Sep proved the production runtime re-served the stale sheet values (5.0 / 3 reviews / 40 lessons / "My name is Sashi" / Preply CTA) on every page load even after the repo zeroing. The repo now refuses them in code, so a stale sheet can no longer re-publish them:
  - `js/sheet.js` — the `rating`, `reviewsCount`, `lessonsCount`, `superTutor`, `preplyUrl` cells return `null` in `FIELDS` (never applied; update, create and record-only paths all skip nulls).
  - `js/reviews.js` — review rows with an external-marketplace `source` (preply/italki) are skipped with a logged reason; ratings derive only from site-native reviews.
  - `tools/sheetsync.js` — the build-side mirror of both gates (same policy, same warning), so `_overrides.js` can never bake them back.
  - `js/seo.js` + `tools/build-tutor-pages.js` — the Person schema's `sameAs` to the marketplace URL and the "Tutor-provided profile excerpt" label are gone from runtime and build paths; the Preply CTA is gone from `js/main.js` (both card and sidebar) and the pre-rendered pages.
  - Regression test: `tools/test-sheet-apply.js` now has a third pass that hands the loader the exact stale row (5 / 3 / 40 / superTutor / marketplace URL) and asserts none of it leaks while ordinary cells still apply — 34/34 checks pass.
- **Name mismatch fixed.** The bio self-introduction now reads "My name is Sushila" (matching the canonical display name "Sushila G." from the sheet's name column); the booking-form nickname "Sashi" is unchanged. The owner should confirm with the tutor which name she prefers — if the preference differs, the sheet's `name` column changes and the URL is rebuilt (see `reports/EKGURU-FINAL-AUDIT-REPORT.md`, OWNER_ACTION_REQUIRED).
- **CTA re-pointed.** The homepage hero button now reads "Find My Guru" (all 7 markets) and targets `/find-tutors.html` — the tutor-discovery surface, as the audit direction requires.
- **Regenerated artifacts**: `index.html` tutor cards, `tutor/sushila-g/`, `tutor/shikha-dutta/`, `feed.xml`, `data/copy-index.json`. `python3 tools/build-all.py check` → "every generated layer is up to date".
- **Owner Sheet item 1 above is now belt-and-braces.** The runtime refuses the stale cells regardless, but the sheet must still be corrected (rating 0 / reviews 0 / lessons 0 / superTutor no / preplyUrl blank / bio name, and the 3 marketplace-sourced review rows removed) so the owner's records and the site agree. Repo PASS ≠ live PASS until the owner updates the sheet and production is redeployed.
