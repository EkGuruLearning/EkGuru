# EkGuru — Monetization Readiness Report (final audit)

Repository state: `arena/01a0deed-ekguru` (= `main` @ 8089f1e plus this remediation working tree), audited 2026-09-26 against production `https://ekguru.shop/`.
Machine-readable inputs: `data/quality/full-page-inventory.json`, `data/quality/adsense-readiness.json`, `data/quality/language-course-matrix.json`, `data/affiliate-programs.json`.
**No claim in this file predicts Google approval.** Statuses describe only what the repository and its tests can prove.

STATUS vocabulary: **READY** (verifiably done repo-side), **PARTIAL** (repo-side done, owner account-side or deploy action outstanding), **BLOCKED** (a hard gate currently fails), **DISABLED** (deliberately off; turning it on prematurely would itself be a policy risk).

---

## 1. AdSense — **PARTIAL**

**Reason.** Every repo-controllable precondition is green: ads.txt carries exactly the authorised account line (`google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0` — unchanged, no invented seller); all 6 trust/legal pages exist and are substantive; 0 thin indexable pages; 0 broken internal links; 100% canonical coverage (2,636 pages); sitemap/noindex consistency clean (0 leaks); 0 duplicate title/meta groups; ads are off site-wide (`js/monetization/monetization.js` `ADS_RUNTIME_ENABLED = false`) so no page can show ads before approval; the excluded page classes (interactive learning, utility, transactional, contact, booking, payment, admin, error, search, placeholder, research, incomplete) are policy-tagged via `data-ad-class` and enforced by `inject-ads` + adsfree gate tests. Two things remain outside the repo: (a) **live production is behind HEAD** (`ca23191` live vs `8089f1e`+remediation in tree — `fetch_page` of the live homepage still shows pre-remediation content), and (b) a **Google-certified TCF CMP for EEA/UK/CH** must be configured account-side before any personalised serving.

**Exact owner action.** (1) Copy the mirrored tutor-sheet values into the owner Google Sheet (`sushila-g` rating 0 / reviewsCount 0 / lessonsCount 0 / superTutor no, priceUSD 6) so sheetsync cannot restore the old numbers. (2) Trigger the production deploy from HEAD and hard-refresh-verify `/`, `/ads.txt`, one tutor profile. (3) Only then, in the AdSense console: configure a Google-certified CMP with TCF for EEA/UK/CH and request site review. (4) After approval only, set `ADS_RUNTIME_ENABLED = true` with vignette/anchor/multiplex/Offerwall OFF.

## 2. Affiliate — **DISABLED**

**Reason.** Generic architecture exists and is fully tested, but `data/affiliate-programs.json` holds **zero approved programs** and `activation_master_switch: false`. `js/affiliate/affiliate.js` is not wired into any page; if invoked it *neutralises* `a[data-affiliate]` anchors. `tools/test-affiliate-disclosure.mjs` passes 10/10 (no sponsored link, no tracking param, no disclosure text can appear without an approved, enabled program and an allowed placement; excluded page classes can never activate). No "official partner" claims exist; `monetization-disclosure/` names no merchant as a partner.

**Exact owner action.** Do nothing until a real program approves EkGuru. Then: fill one program object (owner_status/approval_status/tracking_id/country_eligibility/allowed_traffic/commission_rules/cookie_duration/disclosure_text/allowed_placements/terms_url+reviewed_at), set it APPROVED + enabled, and only then flip the master switch. Never invent IDs.

## 3. Razorpay — **PARTIAL**

**Reason.** Full server architecture is in `server/` + Apps Script contract: order create/verify/webhook with HMAC signature verification before parsing, idempotent reconciliation, per-currency support summaries, frontend dismissal/failure paths. Test suites pass: 11/11 payments E2E + 8/8 Apps Script contract gates. The site UI is in honest `COMING_SOON` mode — the support form renders an inert "online support coming soon" state and mock checkout is hard-blocked on production. No keys, no secrets, no hardcoded payment details in repo.

**Exact owner action.** In Apps Script: set LIVE mode + real Razorpay keys as script properties (never in repo), configure the webhook URL + secret in the Razorpay dashboard, complete Razorpay KYC/international payments enablement, then run the health endpoint and one ₹1 live test before enabling the UI mode.

## 4. Tutor Revenue — **PARTIAL** (deliberately gated behind 1–3)

**Reason.** Two genuine, consented tutor profiles are published (Sushila G., Shikha Dutta — real people, real photos, YouTube intro `Ykic7gkyHjg`). Three draft profiles are quarantined (noindex, unique "not published" titles, no marketplace data). Booking is enquiry-based and truthful. There is **no paid-lesson checkout yet** — by policy, tutor revenue activates only after quality/deploy/ads/affiliates order and after payments exist.

**Exact owner action.** Keep activation deferred until Razorpay is live; then build tutor-priced checkout against the same payments stack, with tutor consent for payouts. Do not pre-announce revenue shares.

## 5. Digital Products — **DISABLED**

**Reason.** No digital products exist in repo; none are advertised. Creating one prematurely (or fake store pages) would violate the thin-content rule.

**Exact owner action.** Only after a genuine asset exists (e.g., a real PDF course pack with real pages), add a product page + checkout; wire disclosure + terms updates.

## 6. Sponsorship — **DISABLED**

**Reason.** No sponsorship inventory, no sponsors, no "advertise with us" claims. Policy: sponsorship comes last in the activation order.

**Exact owner action.** None now. Later: a clearly-labelled sponsorship page with real rates only.

## 7. Google Account Setup — **PARTIAL**

**Reason.** Repo-side artifacts are correct and minimal: ads.txt = exactly one authorised line; `googleb3b0e3defc1daa17.html` Search Console verification file present and untouched; no invented CMP IDs anywhere; publisher ID `pub-8175326569491671` is the only AdSense ID in tree. Account-side state (Search Console property health, AdSense site status, CMP configuration) is **not verifiable from a repository** and is not claimed here.

**Exact owner action.** In Search Console: confirm the property is verified+crawling and submit `sitemap.xml`. In AdSense: confirm the account is in good standing and complete §1 step 3. Record the certified CMP's identity only after it is actually configured.

## 8. Privacy / Consent — **PARTIAL**

**Reason.** `privacy/` (842 words) and `cookie-policy/` (501 words) are honest and specific: GoatCounter is cookieless and consent-gated, the local banner stores only a localStorage choice, and the banner is **not presented as a Google-certified CMP** anywhere. Analytics load only after consent (plus the consent-gated outbound events in the affiliate engine). What the repo cannot do: a TCF-certified CMP for EEA/UK/CH personalised ads is an account-side product; until it exists, EEA/UK/CH must get no personalised ads.

**Exact owner action.** Configure a Google-certified CMP (Funding Choices or another Google-certified provider) account-side for EEA/UK/CH, test a consent string in 3 EEA IP geos, and keep the local banner for non-ad purposes; do not "upgrade" its legal status in copy.

## 9. Payment (support site feature) — **PARTIAL**

**Reason.** Support/checkout UX is deliberately `COMING_SOON`: honest inert form, no fake processors, no test cards, no fake success screens; public support summary endpoint provably leaks no private data (contract gate 8). Depends entirely on §3 completion.

**Exact owner action.** Same as §3, then flip the feature flag and display the real payment page with the published refund/support terms.

## 10. Legal — **READY**

**Reason.** `about/`, `contact/`, `privacy/`, `terms/`, `cookie-policy/`, `disclaimer/`, `copyright/` all exist, are indexable, single-H1, canonicalised, and substantive (word counts 575–842). Tutor-import wording is labelled; unverifiable revenue and rating claims were removed site-wide. Caveat noted by the audit tool: file presence is not legal compliance — jurisdictional review remains the owner's.

**Exact owner action.** Optional legal review for target jurisdictions before paid services start; update `terms/` when Razorpay activates (refunds, payout terms).

## 11. SEO — **READY**

**Reason.** Full-page inventory (2,637 pages): 0 broken internal links; 0 canonical mismatches; 0 noindex-in-sitemap; 1,007 indexable pages all with single H1, canonical, meta description (sole exception: the Google verification file); hreflang families present; robots.txt references sitemap index; 15 child sitemaps exist; feed.xml present.

**Exact owner action.** After redeploy, submit sitemap in Search Console (§7) and spot-check 5 URLs in GSC URL inspection.

## 12. Content Quality — **READY** (with honest review queues)

**Reason.** Post-remediation: 0 thin indexable pages; 0 exact duplicate title/meta groups; no competitor attribution/copy remains ("attributed to", "Excerpt attributed", "Source profile" = 0 hits in built HTML; Preply excerpts deleted; ratings now render only from on-site reviews with count > 0); courses pass all placeholder/rail/count tests (29/29). The audit keeps an honest REVIEW_REQUIRED sampling queue (template intro groups ×5, repeated paragraph groups ×304 across noindex research surfaces; course files 751 heuristic rows) — these are triage lists, not failures, and mostly concern deliberately-noindexed research pages.

**Exact owner action.** When time permits, editorially diversify template intros on the noindex research surfaces; no release gate.

## 13. Browser QA — **PARTIAL**

**Reason.** Every sandbox-possible check passes: full `npm test` (payments 11/11, Apps Script contract 8/8), `npm run test:courses` 29/29, `test-affiliate-disclosure.mjs` 10/10, experience-DOM tests, full `build-all.py check` chain green (copy index, search index, sitemaps, shell 2,635, page layer, ads-free policy). Rendered-browser audits (`tools/audit-runtime-errors.py`, `audit-perf-a11y.py`) require Playwright's Chromium download, which this sandbox's network blocks — they were not executed here and that is stated, not hidden.

**Exact owner action.** On any machine with network: `pip install playwright && playwright install chromium`, serve the repo (`node server/server.js`), run both audit tools; fix anything flagged before the AdSense review request.

## 14. Production QA — **BLOCKED**

**Reason.** Live production is **behind the repository**, and this is now evidence-verified. `fetch_page` of the live homepage (2026-09-26) still serves the pre-remediation state, notably: (a) title "…| EkGuru — 1-on-1 Hindi Lessons" vs the repo's shorter title; (b) broken zero-stats "**0** Tutor profiles", "**1.0★** Profile review average" rendered next to the contradictory hard-coded chip "⭐ Displayed profile rating 5.0"; (c) a direct "★★★★★ **5.0** / 3 reviews / 40 lessons" card claim for Sushila G. — values the repo zeroed as unverifiable marketplace imports; (d) quarantined draft tutors (Hemlata, Tara, Sarshtee) visible via the legacy `tutor.html?id=` shell with a placeholder image for two of them; (e) the user-facing wording "Imported profiles currently list lessons from $6". The repo fixes all of these (2 published profiles, honest fallbacks, unique quarantine titles, zeroed numbers). The final AdSense gate is defined on the **live** site, so production currently fails it. `https://ekguru.shop/ads.txt` was re-fetched live: it serves the exact authorised line — that is contractually fine and must not change.

**Exact owner action.** Mirror the sheet values (§1 step 1), then deploy HEAD to production and verify: `/` shows 2 tutor profiles / prices from $6 / **no** star-rating chips / no "0 tutors · 1.0★" counters; a draft tutor URL returns the quarantined "not published" title; `ads.txt` unchanged; one A1 level page per complete language loads. Then and only then request the AdSense site review.

---

### Summary

| # | Section | Status |
|---|---|---|
| 1 | AdSense | PARTIAL |
| 2 | Affiliate | DISABLED |
| 3 | Razorpay | PARTIAL |
| 4 | Tutor Revenue | PARTIAL (gated) |
| 5 | Digital Products | DISABLED |
| 6 | Sponsorship | DISABLED |
| 7 | Google Account Setup | PARTIAL |
| 8 | Privacy/Consent | PARTIAL |
| 9 | Payment | PARTIAL |
| 10 | Legal | READY |
| 11 | SEO | READY |
| 12 | Content Quality | READY |
| 13 | Browser QA | PARTIAL |
| 14 | Production QA | BLOCKED |

Only §14 + the account-side items inside §1/§7/§8 remain, and every one is an owner action — the repository itself is monetization-clean.
