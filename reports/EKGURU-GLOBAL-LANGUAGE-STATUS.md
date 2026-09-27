# EkGuru — Global Language Status (final audit)

Generated 2026-09-26, re-verified 2026-09-27 on `arena/01a0e08b-ekguru` (base `dfa30ad`): every registry total, readiness/priority distribution and the 10-complete-course list below were recounted from the data files on the current tree and match.
Machine-readable source: `data/quality/language-course-matrix.json` (join of all registries with the pages actually on disk).

**Truth rule for this file**: every number below is counted from repository data. Nothing is estimated, and nothing claims what a language will "soon" contain.

---

## 1. Language registry totals

| Registry | Size | What it is |
|---|---|---|
| `data/global/languages.json` | **700 languages** | Canonical registry: ISO 639‑3 `language_id`, ISO 639‑1 where one exists, script, family, aliases, `language_type` (CANONICAL_LANGUAGE / MACROLANGUAGE / SIGN_LANGUAGE / …) |
| `data/global/language-support-readiness.json` | 733 records | Per-language tooling/data readiness |
| `data/global/language-priority.json` | 700 records | Traffic-style priority scoring |
| `data/global/language-country-relations.json` | 1,983 relations | Language ↔ country links with status/category |
| `data/courses/index.json` | 89 course codes | Languages that have a course surface at all |

### Readiness distribution (all 733 readiness records)

| Readiness | Count |
|---|---|
| READY | 71 |
| PARTIAL | 191 |
| RESEARCH_REQUIRED | 438 |
| NOT_FEASIBLE_YET | 33 |

### Priority distribution (all 700 registry entries)

| Priority | Count |
|---|---|
| P0 | 12 |
| P1 | 54 |
| P2 | 85 |
| P3 | 367 |
| P4 | 182 |

The three duplicate canonical display names in the registry (kituba, nepali, tamasheq) are legitimate ISO 639‑3 modelling — genuinely different languages or a language + its macrolanguage cluster: `lang:ktu`/`lang:mkw`, `lang:npi`/`lang:nep` (MACROLANGUAGE), `lang:tmh`/`lang:taq`. They are **not** publishing collisions, and the code map (§3) blocks alias URL families.

---

## 2. What is actually published

**18 languages have any indexable public course surface.** Every other language in the registry is unpublished research (noindex, out of sitemap, no ads) or does not exist as a page at all.

### 2a. Complete courses — A1 through C2 genuinely published: **10**

Counts are summed from the course data files (including extension tracks); on-page numbers are generated from the same files, so they match by construction. These are honest counts — a "complete" EkGuru language today means a structured, modestly-sized course, not a 500-lesson library.

| Code | Language | Native | Script | Countries (relation rows) | Levels | Lessons | Vocabulary | Dialogue lines | Questions | Test items | Indexable | In sitemap | Readiness | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hi | Hindi | हिन्दी | Deva | 10 | A1–C2 | 44 | 352 | 176 | 748 | 70 | yes | yes | READY | P0 |
| ur | Urdu | اردو | Arab | 9 | A1–C2 | 44 | 352 | 176 | 748 | 70 | yes | yes | READY | P0 |
| gu | Gujarati | ગુજરાતી | Gujr | 1 | A1–C2 | 36 | 288 | 144 | 612 | 60 | yes | yes | READY | P0 |
| mr | Marathi | मराठी | Deva | 1 | A1–C2 | 36 | 288 | 144 | 612 | 60 | yes | yes | READY | P0 |
| pa | Punjabi | ਪੰਜਾਬੀ | Guru | 3 | A1–C2 | 36 | 288 | 144 | 612 | 60 | yes | yes | READY | P0 |
| ta | Tamil | தமிழ் | Taml | 4 | A1–C2 | 36 | 288 | 144 | 612 | 60 | yes | yes | READY | P0 |
| te | Telugu | తెలుగు | Telu | 1 | A1–C2 | 36 | 288 | 144 | 612 | 60 | yes | yes | READY | P0 |
| es | Spanish | español | Latn | 28 | A1–C2 | 52 | 418 | 208 | 884 | 80 | yes | yes | READY | P1 |
| fr | French | français | Latn | 40 | A1–C2 | 52 | 418 | 208 | 884 | 80 | yes | yes | READY | P1 |
| zh | Chinese (Mandarin) | 普通话 | Hans | 7 | A1–C2 | 44 | 352 | 177 | 748 | 70 | yes | yes | READY | P1 |

### 2b. Published partial courses — A1–B2 real and indexable, C1–C2 not claimed: **8**

Course UI and sitemap list **only the published levels** for these; the unbuilt C-level stub files stay noindexed and out of sitemap (verified by `test-course-levels.mjs` rail checks: each hub rail holds exactly its published levels — ar 4/4, de 4/4, it 4/4, ja 4/4, ko 4/4, pt 4/4, ru 4/4, bn 4/4).

| Code | Language | Published levels | Lessons | Questions | Indexable | In sitemap | Priority |
|---|---|---|---|---|---|---|---|
| ar | Arabic | A1–B2 | 44 | 748 | yes | yes | P1 |
| bn | Bengali | A1–B2 | 44 | 748 | yes | yes | P0 |
| de | German | A1–B2 | 44 | 748 | yes | yes | P1 |
| it | Italian | A1–B2 | 44 | 748 | yes | yes | P1 |
| ja | Japanese | A1–B2 | 44 | 748 | yes | yes | P1 |
| ko | Korean | A1–B2 | 44 | 748 | yes | yes | P1 |
| pt | Portuguese | A1–B2 | 44 | 748 | yes | yes | P1 |
| ru | Russian | A1–B2 | 44 | 748 | yes | yes | P1 |

### 2c. Catalog/research entries with no published level: **71**

`af, am, az, bg, bo, ca, cs, cy, da, dz, el, en, et, eu, fa, fi, fil, fj, ga, gn, ha, he, hr, ht, hu, hy, id, ig, is, ka, kk, km, ku, lo, lt, lv, mi, mk, ml, mn, mt, my, nl, no, npi, pl, ps, qu, ro, rw, si, sk, sl, sm, so, sq, sr, st, sv, sw, th, tk, tr, ug, uk, uzn, vi, xh, yo, zsm, zu`

For these, any on-disk surface (starter pack, level stub, research page) is **noindex, absent from every sitemap, and ad-free by page class**. The public catalogue does not claim they have lessons. `languages/af/` level stubs verified noindexed in the ad-readiness review queue.

---

## 3. Canonical code resolution (audit §8 answer)

Canonical course codes are locked by `data/global/language-code-map.json`: *"One language, one course code. Aliases must never spawn a second course or a second URL family."* `blocked_new_course_codes` = `ne, uz, ms, tl, tgl, ht2, arb, cmn, azj`.

| Course code | Canonical course | ISO 639-1 | ISO 639-3 target | Aliases (blocked from duplicating) | State |
|---|---|---|---|---|---|
| ar | Arabic (Standard) | ar | arb | arb, ara, standard-arabic | A1–B2 published |
| zh | Chinese (Mandarin) | zh | cmn | cmn, zho, chi, mandarin | Complete A1–C2 |
| az | Azerbaijani | az | azj | azj, aze | INCOMPLETE — unpublished (noindex stub only) |
| npi | Nepali | ne | npi | ne, nep | INCOMPLETE — note in map: "Do not also emit /languages/ne/" |
| fil | Filipino (course; Tagalog is alias) | tl | fil | tl, tgl, tagalog | not published |
| ht | Haitian Creole | ht | hat | hat, ht2 | not published |
| uzn | Uzbek | uz | uzn | uz, uzb | not published |
| zsm | Malay (Standard) | ms | zsm | ms, msa, standard-malay | not published |

**Disk verification** (this audit): no `/languages/ne/`, `/languages/uz/`, `/languages/tl/`, `/languages/arb/`, `/languages/cmn/`, or `/languages/azj/` directory exists. The single exception in tree is `languages/ms/` — a **noindex** starter-pack page, absent from sitemap; the canonical Malay course URL family is `languages/zsm/` (the registry ISO 639-3 code). No alias has spawned a second indexable course. Registry modelling for the other named cases from the audit brief: Odia `lang:ory` (Orya), Assamese `lang:asm` (iso1 `as`), Bhojpuri `lang:bho`, Maithili `lang:mai`, Sindhi `lang:snd` (iso1 `sd`), Dari `lang:prs`, Mandarin `lang:cmn` (Hans) — all present as canonical entries with correct scripts and no public thin pages.

---

## 4. Publish/noindex policy compliance (this audit's verdict)

| Gate check | Result |
|---|---|
| Indexable thin pages (audit triage threshold) | **0** (`data/quality/adsense-readiness.json`, `thin_indexable_page_count: 0`) |
| noindex page leaking into a sitemap | **0** (`data/quality/full-page-inventory.json`, sitemap consistency) |
| Broken internal links across 2,637 pages | **0** |
| Duplicate title / duplicate meta groups (exact) | **0** |
| Manufactured placeholder tokens in course JSON | **0** (`test-course-placeholders.mjs`, 29 checks pass) |
| Published rails listing unpublished levels | **0** across all 89 course entries |
| Ads on any page of an excluded class (interactive, utility, transactional, contact, booking, payment, admin, error, search, placeholder, research, incomplete) | **0** — AdSense is disabled site-wide at runtime until owner activation |
| Orphan indexable pages | **1** — `googleb3b0e3defc1daa17.html`, the Search Console verification file; must remain exactly as-is |

**Hard rule restated**: a language only becomes indexable when its content is real and its on-page counts exactly match its data. Nothing in this audit found a violation.
