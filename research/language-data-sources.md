# Language Data Sources (Phase 13) + API Cross-Check Log (Phase 11)

Pass 1 · Date: 2026-09-14. Machine-readable registry:
`data/language-inventory/core/_sources.json` (71 keys: 33 batch-1 + 11 batch-2 + 27 batch-3).
Usage counts below are batch-1 actuals (southern-asia, 9 countries).

## 1. Source hierarchy (METHOD Phase 1 — applied)

| Tier | Sources used | Role |
|------|--------------|------|
| A — constitutions & statutes | 8 constitution keys + jk-official-languages-act-2020, official-languages-act-1963, madhesh-province-2021, sindh-official-status | official/national status ONLY. Never speaker numbers. |
| B — censuses & official stats | census-2011 (23), census-2021 (13), census-2023 (5), census-2022 (2), census-2012 (2), unhcr-2024 (1) | speaker estimates, status corroboration. Each census key is one country's one round. |
| C — reference works | ethnologue-27 (73), glottolog-5.x (2), islrtc (1), ref-summary (2) | codes, families, minority/indigenous coverage, sign. |
| D — agent placeholder | agent-knowledge (61) | Marks EVERY pass-1 gap explicitly. Must be 0 before Phase 16. |

Constitution keys (batch 1): constitution-8th-schedule (21), constitution-2004-art16 (8),
constitution-art343 (2), constitution-art3/13/15/16/18-19/251/7 + ch4 + generic (1–2 each).
Full names/URLs in `_sources.json`; URL-null entries carry a reason
(paywall, print-only, unstable-post-2021, etc.).

## 2. Key-by-key notes (curated — the traps)

- **ethnologue-27**: most-used (73). Edition-pinned (27th ed., 2024). Figures
  cited via the edition, not live site (paywall — figures must be re-verified
  from the edition or an accessible source in pass 2). Living-counts per
  country are Ethnologue's (count + confidence recorded per entry).
- **census-2011** (India): 15 years stale — no 2021 round ever happened
  (COVID + delays). All IN figures carry this caveat; see limitations doc.
- **census-2023** (Pakistan): first digital census; Sindh/Balochistan figures
  politically contested (language counts feed the NFC/seat formula).
  Medium confidence, dispute notes on bal/brh.
- **census-2021** (Nepal): mother-tongue list is the most granular in the
  batch (100+ returns); Tharu/Tamang/Magar/Gurung CLUSTER treatments trace here.
- **census-2022** (Bangladesh): confirms Bengali dominance; minority figures thin.
- **census-2012** (Sri Lanka): last full round; ethnicity⇄language mapping
  needs care (Moor ≠ fixed language).
- **constitution-2004-art16** (Afghanistan): post-2021 validity flagged —
  no new constitution; status "in practice" with medium confidence.
- **glottolog-5.x** (2): used ONLY for branch-vs-language rulings
  (Nuristani branch, Pamiri cluster). Never speaker numbers.
- **islrtc** (1): Indian Sign Language Training & Research Centre — ISL entry.
- **ref-summary** (2): secondary summaries where primary was inaccessible;
  weakest C-tier, first to replace in pass 2.
- **unhcr-2024** (1): Rohingya figures (no census covers refugees).
- **agent-knowledge** (61): the honest pile. Every one is a pass-2 task.

## 2b. Batch-2 keys (central-asia, 5 countries)

Tier A: kz-constitution-art7, kg-constitution, tj-language-law (2009),
tm-constitution, uz-language-law (1989/1995 + Latin 1993),
karakalpakstan-constitution (Karakalpak official).
Tier B: kz-census-2021 (19.17M), kg-census-2022 (6.94M), tj-census-2020
(~9.5M), tm-census-2022 (7.06M claimed, no language detail),
uz-stat-committee (ESTIMATES — last full census 1989).
All URLs null-with-portal-reason (archive pass 2).

## 2c. Batch-3 keys (western-asia, 16 countries) + Gulf-immigrant protocol

18 tier-A (constitutions/statutes incl. TR Art.3, IQ Art.4+125, IL 2018 law,
de-facto abkhazia-constitution) + 9 tier-B/C (AM/AZ/GE/JO censuses, IQ-2024 partial,
IL-CBS surveys, lb-no-census-1932 gap-record, sa-gastat, gulf-press-estimates).
Gulf-immigrant protocol (applied uniformly, documented here): enter (a) community-L1
cases (fil/ben/npi/sin), (b) community lingua-francas (hin/urd), (c) unambiguous
state groups (mal in AE/SA only); long-tail everything softer (tam/tel/splits) with
a NO-FABRICATION clause; arz folds into MSA planning everywhere (counts in long-tail);
entries require a citable size basis (pure guesses long-tail regardless of size).

## 3. Registry keys: used vs reserved

iso-639-3 (SIL table bulk check) — NOW USED (NP Magar mrd→mgp merger, AF afg code confirmation).
Still reserved for later passes: unesco-wal (Atlas endangerment flags — WAL fetch failed, manual pass),
wfd (sign-language authority — direct deaf-org consultation pending).

## 4. API / database cross-check log (Phase 11)

| Check | Method | Result (pass 1) |
|-------|--------|-----------------|
| ISO 639-3 code shapes | build QC: regex + 639-2 trap list + 639-1 pairing table | pass-1: Kannada knn→kan caught; pass-2 (2026-09-14): full SIL bulk check — see next row |
| SIL bulk (tab + macrolanguages + retirements, downloaded 2026-09-14) | 113 cited codes checked (entries + members): scope/type/Part1/retired | DONE batch-1 — 11 findings, all fixed: mrd retired→mgp (2026-07-15 merge), hye/mni demacroed (scope=I), doi/san macroed (dgo+xnr / cls+vsn), arb/npi/ory Part1→macro (ara/nep/ori), fas−tgk, kok+knn, nep+dty, san+xct→HISTORICAL. MUST re-run per batch (METHOD rule) |
| Ethnologue live | NOT queried (paywall; edition-pinned instead) | documented deviation, see §2 |
| Glottolog | consulted for 2 branch rulings (manual) | done for batch-1 needs |
| UNESCO WAL | fetch attempted 2026-09-14 — app is JS-only, no API/dump reachable | DEFERRED to manual pass (honest): endangerment flags unjoined; candidates noted in limitations §3 |
| Sign codes (web check 2026-09-14, WFD-adjacent sources) | afg/ins/nsp/pks/psc/sqs/wbs verified in SIL table; IPSL unity dispute (Zeshan 2000) noted on ins | PARTIAL — Afghan SL mis→afg fixed; BdSL/BT/MV genuinely uncoded (disputes stand, narrowed); direct deaf-org consultation still pending |
| Census portals | India 2011 tables (manual, prior knowledge); PK 2023 press releases; NP 2021 report | re-verify with URLs in pass 2 |
| Batch-2 pre-verification (2026-09-14) | 13 new codes vs SIL download (existence/scope/Part1/retirements) + full name-identity audit of batch-1 + long-tail code hunt | CLEAN except 1 real catch: uzn/uzs North/South swap (AF entry + canonical fixed). Rushani/Bartangi/Khufi/Lyuli confirmed uncoded |
| Batch-3 pre-verification (2026-09-14) | 25 new codes vs SIL + full sign-code hunt + long-tail hunt + retro batch-2 long-tail audit | 5 traps caught UPFRONT (adh=Adhola→ady, sqh=Shau→sqt, jor=Jorá→jos, ce→che incl. batch-2 fix, BT sign mis→dyl); ajp→apc 2023 merger applied; yid/zza/kur macro maps recorded |
| Batch-4 pre-verification (2026-09-14) | 75 new entry codes vs SIL download (existence/scope/Part1/retirements) + 10 sign codes + macro member maps | NO Batak macro (btk absent — bbc/btx/bts/akb/btm/btd peer codes); kxd Ref_Name IS 'Brunei'; bik scope=M (8 active, bhk retired); msa/zho member maps recorded; cnk=Khumi Chin; marma=rmz sibling of rki; traps caught upfront, zero post-author fixes |

## 5. Rules for batch authors (binding)

1. Every relation cites ≥1 source; official status MUST cite a tier-A key.
2. `agent-knowledge` is mandatory wherever the fact came from the compiler —
   never leave a fact sourceless, never dress agent knowledge as a citation.
3. New source? Register the key in `_sources.json` FIRST (name/URL-or-reason/
   evidence_type/priority), then cite it. The build flags unknown keys.
4. Census figures always carry the round year in the key (census-YYYY per
   country) — never a bare "census".
5. URL-null is allowed with a reason; reason-null is not.
