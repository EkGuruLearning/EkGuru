# EkGuru final 4-work report

**Release label:** READY FOR OWNER REVIEW

**GATE 0 SHA (this branch start / `main` HEAD when the work began):** `94d7a7f10574e1f001290838db667d9e463f4473`

**Date:** 2026-09-19

This is not AdSense approval. This is not a claim that every language now has expert C5. Extra tracks that were not authored are unpublished.

---

## GATE 0 — starting point

| Item | Result |
|---|---|
| Branch | `arena/01a0bb33-ekguru` from `94d7a7f` |
| Do not assume old PR tests | Re-measured from this SHA |
| Live site | https://ekguru.shop/ — **BROWSER_NOT_VERIFIED** from this workspace |

## GATE 1 — placeholder census (before repair)

| Item | Result |
|---|---|
| Extra-level JSON that matched placeholder tokens | 445 / 445 (historical) |
| After repair | **0 / all course JSON** (`tools/test-course-placeholders.mjs`) |
| Phase-11 A1 | Was placeholder; now `content_status=INCOMPLETE`, `indexable=false` |

## Phases 2–10 — extra-level policy

CEFR is A1–C2 plus half-steps A1+…C1+. **A3, B3, C3, C4, C5 are EkGuru extension tracks, not CEFR.** They are published only when `tools/lib/extended_banks.py` has an authored pack.

| Track | Authored now | Otherwise |
|---|---|---|
| A3 | `ar de en es fr hi it ja pt` | INCOMPLETE + noindex + dropped from sitemap |
| B3 | `en es fr` | same |
| C3 C4 C5 | none | same |

Practice/quiz/test items on authored extras are **re-asks of that lesson’s vocab/grammar/dialogue**, not invented glosses.

## Phases 11–13 — generator rewrite (source, not hand-patch)

| File | Change |
|---|---|
| `tools/generate-extended-courses.py` | Refuses to write. `--force-placeholders` exits. `generate_lesson_content` raises. |
| `tools/repair-extended-levels.py` | Writes REAL from banks or INCOMPLETE stubs |
| `tools/lib/placeholders.py` | Token scan |
| `tools/lib/extended_banks*.py` | Authored packs |
| `tools/build-course-levels.py` | Index only publishable files; noindex stubs; sitemap omits unpublished; extra tracks not described as CEFR; `counts_of` reads `level.test`; 0-item tests not advertised |

Hand-editing 445 JSON files was rejected: the next generator run would have restored fakes.

## Phases 14–20 — catalogue honesty

| Item | Result |
|---|---|
| Unique course codes | 89 |
| `complete: true` | 38 (CEFR A1–C2 authored) |
| `complete: false` | 51 (including all phase-11/12/13) |
| Top-level `levels` | A1–C2 only |
| `extension_tracks` | A3 B3 C3 C4 C5 |
| Per-course `levels` | Only REAL levels, with recounted `lessons` / `test_items` |
| Kannada | `kn` already a course language in `languages.json`. **No second Kannada course invented.** Catalogue still has no `kn` row — **not invented here**. |
| Nepali | Canonical course code **`npi`**. Aliases `ne`, `nep`. Phase-11 `npi` is INCOMPLETE. **No `/languages/ne/` course.** |
| Aliases | `data/global/language-code-map.json` (`fil`/`tl`, `uzn`/`uz`, `zsm`/`ms`, `ht`/`ht2`, `zh`/`cmn`, `ar`/`arb`, `az`/`azj`) |
| Blocked new codes | `ne uz ms tl tgl ht2 arb cmn azj` |

## Phases 21–28 — AdSense / monetization (no approval claim)

| Item | Result |
|---|---|
| Publisher id in repo | `ca-pub-8175326569491671` |
| Live / dashboard approval | **ACCOUNT_SIDE_NOT_VERIFIABLE** |
| Cookie default | `advertising: false` (`js/cookie-consent.js`) |
| gtag default | ad_storage / ad_user_data / ad_personalization / analytics_storage **denied** |
| `js/monetization.js` | Ads only if `consent.advertising === true` (was default-allow when consent missing) |
| Level pages | `data-ad-class="INTERACTIVE_LEARNING"`; no `adsbygoogle` loader |
| Google certified CMP id | **ACCOUNT_SIDE_NOT_VERIFIABLE** — not invented |
| Rendered ad in a browser | **BROWSER_NOT_VERIFIED** |
| Phrase never used | “AdSense guaranteed approved.” |

Evidence file: `data/quality/adsense-readiness.json`

## Phases 29–36 — worldwide SEO

| Item | Result |
|---|---|
| Canonical | Self-canonical on complete CEFR pages (test) |
| hreflang | `en` + `x-default` on level pages (English UI). **Not** 700 fake language alternates |
| `sitemap-levels.xml` | 278 URLs = 38×(ladder+6 CEFR) + 12 authored extras |
| C3–C5 in sitemap | **0** |
| `robots.txt` | Now lists `sitemap-levels.xml` (already in `sitemap-index.xml`) |
| Unpublished extras / incomplete langs | `noindex, follow` stubs, not in sitemap |
| Schema | Course + Breadcrumb on published levels; ItemList only published rungs |
| Thin / duplicate language pages | No new country/language farm. Aliases do not spawn URLs |
| `how-levels-work/` | CEFR has no A3/C4; optional authored EkGuru extensions explained |

## Phases 37–40 — tests

| Command | Result |
|---|---|
| `node tools/test-course-placeholders.mjs` | PASS 7 |
| `node tools/test-course-levels.mjs` | PASS 29 |
| `npm test` (payments) | **not re-run this slice** — do not treat as green without a run |
| `npm run test:courses` | added (placeholders + course-levels) |

`test-course-levels.mjs` no longer assumes 273 pages / 39 languages / “no noindex ever”. It checks the **38 complete** CEFR courses.

## Phases 41–43 — residual risk

1. **Most extra tracks are unpublished.** Only 12 REAL extra files. That is honest, not finished curriculum.
2. **51 catalogue languages have no authored A1–C2.** Their old placeholder A1–C2 JSON was replaced with INCOMPLETE stubs. Those URLs still exist as noindex holders.
3. **Kannada `kn`** is `course` in `languages.json` but not a catalogue course. Not fabricated.
4. **Nepali** needs an authored bank before `npi` can be `complete`.
5. **AdSense, CMP, live ads:** account/browser unverified.
6. **Level pages after rebuild** do not re-run the full storybook/page-layer/ads injectors. They carry INTERACTIVE_LEARNING, support band, and a chapter marker from `compose()` so the course-level tests hold. A later full site inject is still the owner’s pipeline.
7. **C3–C5** remain unpublished for every language.

---

## What was not done (on purpose)

- Did not machine-translate 89 C5 courses.
- Did not rename `word_1` to `vocab_1`.
- Did not add 700 language/country pages.
- Did not claim Google approval.
- Did not touch Razorpay / payment architecture.

---

## Owner checklist

- [ ] Accept unpublished extra levels as noindex stubs, or fund authored banks in `tools/lib/extended_banks*.py`
- [ ] Confirm AdSense / CMP in the Google account (**not verifiable here**)
- [ ] Run `npm test` (payments) on a machine with those secrets
- [ ] Optional: full `inject-storybook.py` / `build-page-layer.py` pass on `languages/*/level/`
- [ ] Nepali: author `npi` or keep incomplete
- [ ] Kannada: add a real `kn` course only with authored A1–C2, never a thin duplicate

**READY FOR OWNER REVIEW**
