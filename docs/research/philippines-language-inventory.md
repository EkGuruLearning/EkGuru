# Philippines Language Inventory — Deep Audit (Phase 6)

Batch: southeast-asia (pass 1) · Status: PRELIMINARY · Date: 2026-09-14

The Philippines runs the world's most ambitious mother-tongue education
policy (MTB-MLE in 19 languages) on top of a two-pillar official system
(Filipino + English) — and counts its languages through a census umbrella
("Bisaya") that folds three entry-class languages into one. This file is the
Phase 6 deep audit: the 1987 constitutional backbone, the Filipino/Tagalog
split, and the Bikol-macro + BARMM rulings pass 2 must make.

## 1. Coverage

- Entries: **15** (Filipino + English + 11 regionals + Hokkien + PSL).
- Living languages (Ethnologue 27, medium confidence): **≈175**.
- Census language data: **coarse** — PSA census mother-tongue tables use
  umbrella groupings (notably "Bisaya/Binisaya" folding ceb+hil+war, see
  §5); figures below split the umbrellas via Ethnologue, medium confidence.

## 2. Entries — table

| # | Language | 639-3 | Roles | Speakers (est.) | EkGuru |
|---|----------|-------|-------|-----------------|--------|
| 1 | Filipino | fil | official, national, widely-spoken, lingua-franca | 100M total (~30M L1) | P0 course |
| 2 | English | eng | official, widely-spoken | L2 (schools/law/BPO) | pack live |
| 3 | Cebuano | ceb | regional | 27M | none |
| 4 | Ilokano | ilo | regional | 11M | none |
| 5 | Hiligaynon | hil | regional | 11M | none |
| 6 | Bikol | bik | regional (macro) | 6.5M | none |
| 7 | Waray | war | regional | 3.5M | none |
| 8 | Kapampangan | pam | regional | 3.2M | none |
| 9 | Pangasinan | pag | regional | 2.2M | none |
| 10 | Maguindanao | mdh | regional | 2.2M | none |
| 11 | Maranao | mrw | regional | 2.2M | none |
| 12 | Tausug | tsg | regional | 1.8M | none |
| 13 | Chavacano | cbk | regional | 800K | none |
| 14 | Hokkien | nan | minority | 1M (Binondo/Manila) | none |
| 15 | Philippine Sign Language | psp | sign | n/a (RA 11106 national SL) | none |

## 3. Gap analysis (EkGuru coverage)

- Filipino is a P0 course (only P0 outside South Asia — scored on merits:
  100M + official + diaspora). Correct.
- ceb (27M) + ilo/hil (11M each) are the largest Austronesian `none`
  entries after jav/sun — the natural second wave if PH demand appears.
- Sama-Bajaw sea-nomad cluster (`sml` Central Sama, `ssb` Southern Sama,
  `bdl` West Coast Bajau — 3-country PH/MY/ID spread, ≈500K jointly) is
  entirely long-tail: individually below threshold, jointly entry-class.
  Pass 2 ruling: cross-border cluster survey.
- Spanish legacy (Ermita/Cavite elders, legal archives) correctly has NO
  entry — Chavacano (`cbk`) is the living Spanish-lexified entry.

## 4. Constitutional backbone (what the entries cite)

- 1987 Constitution Art.XIV s.6–7: Filipino is THE national language;
  Filipino + English are official "until otherwise provided by law";
  regional languages are auxiliary-official in their regions and auxiliary
  media of instruction.
- KWF (Komisyon sa Wikang Filipino): develops Filipino "on the basis of
  existing Philippine and other languages" — the legal engine of the
  fil/tgl distinction (see §6).
- MTB-MLE (DepEd 2009, K-12 2012): mother-tongue medium Grades 1–3 in 19
  languages; rollback bills from 2023 (early-exit to Filipino/English) —
  status TBD pass 2, course-text implications if it lands.
- RA 11106 (2018): Filipino Sign Language (`psp`) declared the national
  sign language — one of the few Asian states with SL statute.

## 5. The Bisaya umbrella (census artefact — do not take PSA tables at face value)

PSA census mother-tongue returns group "Bisaya/Binisaya" as ONE line that
in practice folds Cebuano (`ceb`), Hiligaynon (`hil`) and Waray (`war`) —
three mutually UNintelligible entry-class languages — plus Boholano and
minor Visayan varieties. Consequences:

- `ceb`/`hil`/`war` bands use Ethnologue splits, NOT PSA umbrella figures,
  with a confidence penalty; the PSA line is cited only as an upper bound.
- Name politics: "Bisaya" as ethnonym (Cebuano-speakers call their language
  Bisaya) vs "Bisaya" as census umbrella — entries use ISO Ref_Names
  (Cebuano/Hiligaynon/Waray) with Bisaya cross-notes.
- It is the test case for the rule "census folding does not delete a
  language" (same rule as Bhojpuri under the Hindi umbrella, IN audit §5).

## 6. Code treatments specific to the Philippines

- **Filipino/Tagalog dual**: PH entry uses `fil` (standardised national,
  Manila-Tagalog base + KWF lexicon); `tgl` (Tagalog proper) appears only
  in diaspora entries (US). Same-base, distinct standards — never merged.
- **Bikol macro**: `bik` (scope=M; 8 active members + `bhk` retired per SIL
  bulk 2026-09-14) — entry stays macro-level; member split (Central `bcl`
  vs Rinconada vs Catanduanes) TBD pass 2.
- **Chavacano varieties**: `cbk` single code covering Zamboanga (largest),
  Cavite, Ternate, Ermita(-extinct?) — variety vitality TBD pass 2.
- **Danaos pair**: `mdh` (Maguindanaon) + `mrw` (Maranao) — close sisters,
  distinct codes, BARMM's two pillars; separate entries, cross-noted.
- **Tausug**: `tsg` (Sulu archipelago + Sabah spillover) — trade lingua
  franca of the Sulu Sea; Jawi/Arabic-script heritage.
- **Kapampangan/Pangasinan**: `pam` + `pag` (Central Luzon) — distinct
  branches (not Tagalog dialects); entries hold.
- **Hokkien**: `nan` (Min Nan) — Binondo community; Mandarin (`cmn`) school
  subject with no L1 base, correctly unentered.

## 7. Cross-border entries (shared planning)

| Language | PH code | Other side | Note |
|----------|---------|------------|------|
| Filipino/Tagalog | fil | US tgl (diaspora 1.7M) | same base — diaspora notes fold into course |
| Tausug | tsg | MY Sabah tsg (Suluk) | same code — one pack |
| Maguindanao/Maranao | mdh/mrw | MY Sabah diaspora | same codes — diaspora notes |
| Ilokano | ilo | US Hawai'i diaspora | same code — diaspora notes |
| Sama-Bajaw | — (long-tail) | MY/ID cluster | 3-country survey TBD pass 2 |
| Hokkien | nan | MY/SG/TW/CN nan | same code — one pack, Binondo notes |
| Chavacano | cbk | — (PH only) | Spanish-lexified isolate-creole |

## 8. Pass-2 verification list (Philippines)

1. PSA census Bisaya-umbrella split (ceb/hil/war quantification).
2. MTB-MLE rollback status (Congress bills 2023–26; KWF position).
3. KWF Filipino-standard corpus (learner-Filipino text source).
4. Bikol member split (bcl vs Rinconada/Catanduanes entries?).
5. Chavacano variety vitality (Ermita extinct? Cavite/Ternate counts).
6. BARMM language law (Bangsamoro official-language posture; Arabic role).
7. Sama-Bajaw 3-country survey (entries vs cluster note).
8. PSL (psp) corpus + RA 11106 implementation (interpreter pipeline).
9. Spanish-legacy confirmation (no living L1 community — hold no-entry).
10. Yakan (`yka`) + other Sulu entries threshold check.
11. Filipino-L1 growth (Metro Manila shift) quantification.
12. BPO-English effect on English-L2 figures (upper-bound discipline).
