# EkGuru Growth Plan & Complete Distribution Execution Kit (Nov 2026)

**PRIVATE INTERNAL PACKAGE** — Stored under `docs/marketing/growth-distribution-2026-11/`, which is automatically excluded from public deployment (`_site`) by `tools/build-public-dist.py` and verified clean of personal contact data by `node tools/test-public-surface.mjs`.

Every `https://ekguru.shop/...` URL across this entire kit has been programmatically checked against the repository tree so zero `404` links exist.

---

## Folder Map (100% of `GROWTH-PLAN-2026-11-24.md` & `DISTRIBUTION-KIT-2026-11-24.md`)

| Folder / File | What’s Inside | Status |
|---|---|---|
| `GROWTH-PLAN-2026-11-24.md` & `DISTRIBUTION-KIT-2026-11-24.md` | Original strategy & distribution source documents archived privately | Complete |
| `00_og_cover/` | Master SVG + PNG (`1200×630`) for the claim-safe site-wide `images/og-cover.{jpg,webp}` | Live in repo |
| `01_tutor_whatsapp_kit/` | `TUTOR_WHATSAPP_MESSAGES.md` + interactive copy-paste `tutor_whatsapp_dashboard.html` for all **19 public tutors** (Day 2 / Day 3 / Day 6 batches, `?ref=tutor-<slug>`, zero private contact fields) | Ready to send |
| `02_official_profile_first_3_posts/` | **Post 1** (`post_01_ekguru_intro_1080x1350.png`), **Post 2** (`post_02_name_in_hindi_tool_1080x1350.png`), **Post 3 Complete 4-Slide Devanagari Carousel** (`post_03_devanagari_tip_1080x1350.png` + `post_03_slide_02..04_*_1080x1350.png`), editable SVGs, and `OFFICIAL_POSTS_CAPTIONS.md` | Visually verified |
| `03_shorts_reels_pack/` | **3 Ready-to-Upload `1080×1920` (`9:16`) MP4 Videos** (`short_01_count_1_to_10_hindi_9x16.mp4`, `short_02_your_name_in_hindi_9x16.mp4`, `short_03_auto_ride_3_phrases_9x16.mp4`), cover PNGs, plus `SHORTS_AND_REELS_PACK.md` with **all 15 scripts** (Hindi + Marathi, Gujarati, Tamil, Telugu, Bengali) | Encoded & verified |
| `04_channel_copy_paste_pack/` | `CHANNEL_LAUNCH_PACK.md` (Reddit city & language posts + comment templates + NRI communities) and `GSC_INSPECT_URLS.txt` (priority URLs for Google Search Console) | URL-verified |
| `05_quora_and_whatsapp_pack/` | `QUORA_ANSWERS_PACK.md` (7 full 150–230 word answers mapped to real `/ask/...` URLs) + `WHATSAPP_TELEGRAM_HINGLISH_PACK.md` (Founder status + 7 city relocation messages) | Ready to paste |
| `06_backlink_outreach_pack/` | `OUTREACH_EMAILS_AND_QUERIES.md` (Google search queries + 3 email templates + 7-day follow-up), `outreach_tracker.csv`, and **printable A4 handout** `ekguru_hindi_class_home_practice_sheet_A4.{svg,png}` for Hindi schools & parent groups | Ready to send |
| `07_submissions_and_30day_tracker/` | `DIRECTORY_AND_ARTICLE_SUBMISSIONS.md` (Bing Webmaster Tools, AlternativeTo, Show HN, Product Hunt, full Dev.to / IndieHackers article) + `30_DAY_EXECUTION_TRACKER.md` (Day 1 → Day 30 checklist & review scorecards) | Ready to run |
| `scripts/` | Deterministic generators (`build_visual_assets.py`, `build_shorts_and_printables.py`, `build_distribution_kit.js`, `build_remaining_packs.js`) | Reproducible |

---

## URL Corrections Caught & Applied Automatically

Two draft URL patterns in the original notes would have hit `404` on production and were corrected everywhere in this kit:
1. `/learn/hindi/alphabet/` → **https://ekguru.shop/hindi/alphabet/**
2. Regional Indian courses (`/languages/<code>/course/` only exists for world languages) →
   - Marathi: **https://ekguru.shop/learn/marathi/**
   - Gujarati: **https://ekguru.shop/learn/gujarati/**
   - Tamil: **https://ekguru.shop/learn/tamil/**
   - Telugu: **https://ekguru.shop/learn/telugu/**
   - Punjabi: **https://ekguru.shop/learn/punjabi/**
   - Urdu: **https://ekguru.shop/learn/urdu/**
   - Bengali: **https://ekguru.shop/bengali/**
   *(Note: `/learn/kannada/` and `/learn/malayalam/` exist on disk as `noindex` drafts — excluded from active promotion per `GROWTH-PLAN-2026-11-24.md` Section 3 until native review is complete.)*
