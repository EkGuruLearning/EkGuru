# EkGuru — Growth Plan & Distribution Kit Execution Package (Nov 2026)

> **PRIVATE INTERNAL DIRECTORY (`docs/marketing/`)** — Automatically excluded from the public `_site` build by `tools/build-public-dist.py` and enforced by `tools/test-public-surface.mjs`.

## 1. Saved Master Documents
- [`GROWTH-PLAN-2026-11-24.md`](./GROWTH-PLAN-2026-11-24.md) — Audit & 30-day honest growth strategy
- [`DISTRIBUTION-KIT-2026-11-24.md`](./DISTRIBUTION-KIT-2026-11-24.md) — Copy-paste distribution playbook

## 2. Repository Fixes Completed (Growth Plan Section 6)
- **6(a) Claim-Safe Open Graph Cover (`images/og-cover.jpg` & `images/og-cover.webp`, `1200×630`):** Replaced the old cover (which contained *"Verified native tutors"* / *"From $3"* / *"7 languages"* and a tutor photo) with a crisp, honest, vector-rendered EkGuru brand cover aligned 100% with site disclosures. Editable SVG saved in [`00_og_cover/ekguru_og_cover_1200x630.svg`](./00_og_cover/ekguru_og_cover_1200x630.svg).
- **6(b) Stale Time/Days Pages Fixed:** Fixed `learning_code()` in `tools/apply-ultra.py` for `days-and-months-in-<lang>` and rebuilt `days-and-months-in-{gujarati,kannada,telugu,urdu}/index.html` via `tools/build-time-pages-bodies.py`. Both `build-time-pages-bodies.py --check` and `apply-ultra.py --check` now pass with 0 stale pages.
- **6(c) Crawler-Visible Static Tutor Cards on `find-tutors.html`:** Extended `tools/build-home-tutors.js` so `#find-list` in `find-tutors.html` ships all 19 active public tutor cards in static HTML for first-pass crawlers while keeping `tools/ultra/contract.py` (index + canonical freeze) and live JS filtering 100% intact.
- **6(d) Weekly Workflows (`live-guard.yml` & `course-health.yml`):** Updated `tools/weekly-guard.sh` so Cloudflare `cf-mitigated: challenge` responses on datacenter runner IPs verify local file invariants and log `⚠️ CF_CHALLENGE` instead of masking real failures, while real HTTP/SSL/policy errors still exit 1. Updated `tools/course-health.py` to auto-ensure the `course-health` label and update issues via GitHub REST API.
- **6(e) Page-Specific `og:image:alt` & `twitter:image:alt`:** Updated `tools/build-phase7-pages.py` template and replaced hardcoded *"EkGuru — free, self-paced Hindi learning"* across `start/`, `languages/`, all 29 `languages/*/index.html` hubs, `find-tutors.html`, and `tutor/index.html` with each page's actual title without altering `robots` or `canonical`.
- **6(f) PR #63:** Verified already closed on GitHub.
- **6(g) Commission Honesty:** Kept truthful disclosure (`EkGuru does not collect tutor-lesson payments in this release` on `find-tutors.html`) with zero fabricated marketplace/commission claims.

## 3. Ready-to-Use Distribution Assets
1. **[`01_tutor_whatsapp_kit/`](./01_tutor_whatsapp_kit/)**
   - `TUTOR_WHATSAPP_MESSAGES.md` — Personalized messages + `?ref=tutor-<slug>` links for all **19 live public tutors** (grouped into Day 2, Day 3, and Day 6 batches).
   - `tutor_whatsapp_dashboard.html` — Open locally in any browser for 1-click **Copy Message** & **Open in WhatsApp** buttons with tick-box progress tracking.
2. **[`02_official_profile_first_3_posts/`](./02_official_profile_first_3_posts/)**
   - `post_01_ekguru_intro_1080x1350.png` (+ `.svg`)
   - `post_02_name_in_hindi_tool_1080x1350.png` (+ `.svg`)
   - `post_03_devanagari_tip_1080x1350.png` (+ `.svg`)
   - `OFFICIAL_POSTS_CAPTIONS.md` — Ready captions for Instagram, X, LinkedIn, and Facebook.
3. **[`03_shorts_reels_pack/SHORTS_AND_REELS_PACK.md`](./03_shorts_reels_pack/SHORTS_AND_REELS_PACK.md)**
   - 3 complete 25-second Shorts/Reels scripts (`1–10 Hindi Numbers`, `Your Name in Hindi`, `3 Auto Ride Phrases`) + links to the rendered `9:16` master videos in `docs/marketing/ekguru-brand-ad/06_exports/`.
4. **[`04_channel_copy_paste_pack/`](./04_channel_copy_paste_pack/)**
   - `CHANNEL_LAUNCH_PACK.md` — Pre-filled Reddit posts (`r/pune`, `r/hyderabad`, `r/chennai`, `r/ahmedabad`, `r/kolkata`, `r/hindi`), Quora answers, and university/blogger outreach emails.
   - `GSC_INSPECT_URLS.txt` — Exact 10 URLs to submit in Google Search Console on Day 1.
