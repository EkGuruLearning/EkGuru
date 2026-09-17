# China Language Inventory — Deep Audit (Phase 6)

Batch: eastern-asia (pass 1) · Status: PRELIMINARY · Date: 2026-09-14

China is the inventory's scale extreme: one entry (cmn, 1.1B) outweighs the
next ten countries combined, while the census has NEVER asked a language
question — every figure below is an ethnicity-proxy estimate. This file is
the Phase 6 deep audit: the Art.4/Putonghua backbone, the Mandarin umbrella,
the missing-Sinitic gap (Jin + Min Bei/Dong uninventoried), and the
autonomous-area rulings pass 2 must make.

## 1. Coverage

- Entries: **17** (Mandarin + 6 Sinitic regionals + 6 autonomous-area
  languages + Yi + Miao + CSL + English).
- Living languages (Ethnologue 27, medium confidence): **≈300**.
- Census language data: **none** — 2020/2010/2000 censuses asked ethnicity
  (56 recognised groups), never language; ethnicity≠language mapping (§5)
  is the central data hazard.

## 2. Entries — table

| # | Language | 639-3 | Roles | Speakers (est.) | EkGuru |
|---|----------|-------|-------|-----------------|--------|
| 1 | Mandarin | cmn | official, national, widely-spoken | 1.1B (umbrella — §5) | P1 plan |
| 2 | Cantonese | yue | official-regional, regional, widely-spoken | 85M | P1 plan |
| 3 | Wu | wuu | regional | 80M | none |
| 4 | Min Nan | nan | regional | 50M (Hokkien-Taiwanese) | none |
| 5 | Hakka | hak | regional | 45M | none |
| 6 | Xiang | hsn | regional | 38M | none |
| 7 | Gan | gan | regional | 22M | none |
| 8 | Zhuang | zha | official-regional, regional | 14M | none |
| 9 | Uyghur | uig | official-regional, regional | 10M | none |
| 10 | Peripheral Mongolian | mvf | official-regional, regional | 3M | none |
| 11 | Tibetan | bod | official-regional, regional | 5M (umbrella — §6) | none |
| 12 | Korean | kor | official-regional, minority | 2M | none |
| 13 | Kazakh | kaz | official-regional, minority | 1.5M | none |
| 14 | Nuosu Yi | iii | regional | 8M | none |
| 15 | Hmong/Miao | hmn | regional | 10M (umbrella — §6) | none |
| 16 | Chinese Sign Language | csl | sign | n/a (north/south split) | none |
| 17 | English | eng | widely-spoken | L2 (education/business) | pack live |

## 3. Gap analysis (EkGuru coverage)

- P1 plans for cmn/yue are correct; cmn is the flagship Sinitic course.
- **Missing-Sinitic gap — CLOSED same-day**: Jin (`cjy` ~45M), Min Dong
  (`cdo` ~10M) and Min Bei (`mnp` ~10M) were added as pass-1 entries
  (audit-gap commit, low confidence); ≈65M speakers restored to the data.
  Pass 2 still verifies figures + Teochew/Huizhou splits (§8).
- wuu (80M, Shanghai — measurable youth-transmission decline) + nan (50M,
  cross-Strait) are the largest entered `none` Sinitic entries.
- Tujia (`tji`, 8M ethnicity / <100K speakers — the ethnicity≠language
  extreme), Manchu (`mnc`, ~10 L1, 10M ethnicity) and Hui (13M ethnicity,
  Mandarin-speaking) correctly have NO entries — the rule "ethnicity is not
  a language entry" (§5).
- Hong Kong Sign Language (`hks`) vs CSL (`csl`) split unentered — §8.

## 4. Constitutional backbone (what the entries cite)

- Constitution Art.4: all nationalities free to use and develop their own
  spoken/written languages; Art.19 (1982; amended): the state promotes
  nationwide Putonghua.
- 2000 National Language Law: Putonghua + standard simplified characters
  are the national/official standard; minority languages protected in
  autonomous areas (schools, courts, signage).
- Regional Autonomy Law (1984): autonomous-area governments use local
  languages alongside Putonghua — the legal basis for all six
  official-regional entries (zha/uig/mvf/bod/kor/kaz).
- Hong Kong/Macau Basic Laws: Chinese + English official; Cantonese the de
  facto Chinese standard (medium-of-instruction policy shifts TBD §8).

## 5. The Mandarin umbrella + ethnicity trap (read nothing at face value)

Two artefacts compound in China:

1. **Mandarin umbrella**: `cmn` 1.1B folds Putonghua-L2 (hundreds of
   millions) with northern/eastern Mandarin L1 continua (Northeastern,
   Beijing, Jilu, Jiaoliao, Zhongyuan, Lanyin, Jianghuai) — mutually
   intelligible in a chain, divergent at the ends. Band carries a
   confidence penalty; learner Mandarin = Putonghua/Beijing standard.
2. **Ethnicity≠language**: census ethnicity counts are routinely misquoted
   as speaker counts. Hui (13M, speak Mandarin), Manchu (10M, ~10 L1),
   Tujia (8M, <100K L1), Zhuang (18M ethnicity → 14M speakers — the LEAST
   lossy major mapping). Entries use speaker estimates, never ethnicity
   counts; any source conflating them is rejected in pass 2.

## 6. Code treatments specific to China

- **Chinese macro**: `zho` (macro; members incl. cmn/yue/wuu/nan/hak/hsn/gan
  + missing cjy/cdo/mnp — build bulk-note batch-4). Entries use
  individuals only; `zho` never cited for a variety.
- **Tibetan umbrella**: `bod` entry folds Ü-Tsang + Kham (`khg`) + Amdo
  (`adx`) — distinct ISO codes, limited mutual intelligibility. Macro-level
  entry holds for pass 1; split TBD pass 2.
- **Hmong/Miao umbrella**: `hmn` entry folds Hmong Daw/Mong Njua clusters —
  macro treatment TBD pass 2 (member codes hnj/mww + sisters).
- **Zhuang split**: `zha` entry folds Northern (`zgn`) + Southern (`zhn`) —
  distinct codes; split TBD pass 2.
- **Mongolian pair**: CN `mvf` (Chakhar standard, traditional script) vs MN
  `khk` (Khalkha, Cyrillic) — distinct codes AND scripts; separate packs.
- **CSL split**: `csl` entry folds Northern (Beijing) + Southern (Shanghai)
  CSL — low mutual intelligibility; HKSL (`hks`) separate code. Split TBD.
- **Uyghur/Kazakh scripts**: Arabic-script standards (CN side) vs
  Cyrillic/Latin reforms across the border (KZ) — script notes mandatory.

## 7. Cross-border entries (shared planning)

| Language | CN code | Other side | Note |
|----------|---------|------------|------|
| Cantonese | yue | HK/MO yue (de-facto official) | same code — one pack |
| Min Nan | nan | TW/MY/SG/PH nan | same code — one pack, cross-Strait notes |
| Hakka | hak | TW/MY/ID hak | same code — one pack |
| Korean | kor | KR/KP kor | same code — Yanbian notes fold into course |
| Kazakh | kaz | KZ kaz (official) | same code — script notes (Arabic vs Cyrillic/Latin) |
| Uyghur | uig | KZ/KG uig | same code — one pack |
| Tibetan | bod | IN/BT/NP bod + dialects | same code — exile-variety notes |
| Mongolian | mvf | MN khk (different code!) | distinct codes+scripts — separate packs |
| Nuosu Yi | iii | VN/LA Yi spillover | same code — one pack |
| Hmong | hmn | VN/LA/TH/US diaspora | same code — diaspora notes |
| Zhuang | zha | VN Tày/Nùng (sisters) | distinct codes — cross-notes |

## 8. Pass-2 verification list (China)

1. Jin/Min-Dong/Min-Bei figures — DONE as pass-1 entries (audit-gap commit); verify + Teochew/Huizhou splits.
2. Mandarin-umbrella split (Putonghua-L2 vs dialect-L1 quantification).
3. Tibetan split ruling (bod vs khg/adx entries?).
4. Hmong/Miao macro ruling (hmn members audit).
5. Zhuang split ruling (zgn/zhn entries?).
6. CSL split ruling (north/south + hks entries?).
7. Wu transmission-decline quantification (Shanghai youth surveys).
8. HK medium-of-instruction policy status (post-2020 Cantonese/Mandarin).
9. Yanbian Korean vitality (out-migration to KR/CN cities effect).
10. Uyghur/Kazakh script-note accuracy (Arabic-standard currency).
11. Mongolian-medium education status (post-2020 policy; traditional script).
12. Teochew (`teo`?) within nan — folded or split (chaozhou-shantou audit).
13. Huizhou (`czh`) + Pinghua threshold check (long-tail watch).
14. Ethnicity-conflation source audit (reject Hui/Manchu/Tujia misquotes).
