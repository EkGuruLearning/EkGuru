# Language Data Sources (Phase 13) + API Cross-Check Log (Phase 11)

Pass 1 · Date: 2026-09-14. Machine-readable registry:
`data/language-inventory/core/_sources.json` (33 keys). Usage counts below are
batch-1 actuals (southern-asia, 9 countries).

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

## 3. Unused registry keys (reserved for pass 2)

iso-639-3 (SIL table bulk check), unesco-wal (Atlas endangerment flags),
wfd (sign-language authority). Registered now so batch authors cite them
uniformly later; the build's iso-bulk-verification OPEN item tracks this.

## 4. API / database cross-check log (Phase 11)

| Check | Method | Result (pass 1) |
|-------|--------|-----------------|
| ISO 639-3 code shapes | build QC: regex + 639-2 trap list + 639-1 pairing table (37 pairs) | 84/84 valid; 1 real bug caught & fixed (Kannada knn→kan, 2026-09-14); guard negative-tested |
| SIL iso639-3.tab bulk | not yet run (needs table download) | OPEN — pass 2 |
| Ethnologue live | NOT queried (paywall; edition-pinned instead) | documented deviation, see §2 |
| Glottolog | consulted for 2 branch rulings (manual) | done for batch-1 needs |
| UNESCO WAL | not yet queried | pass 2 (endangerment flags) |
| WFD / deaf-org | not yet queried | pass 2 (all 5 sign entries + ISL) |
| Census portals | India 2011 tables (manual, prior knowledge); PK 2023 press releases; NP 2021 report | re-verify with URLs in pass 2 |

## 5. Rules for batch authors (binding)

1. Every relation cites ≥1 source; official status MUST cite a tier-A key.
2. `agent-knowledge` is mandatory wherever the fact came from the compiler —
   never leave a fact sourceless, never dress agent knowledge as a citation.
3. New source? Register the key in `_sources.json` FIRST (name/URL-or-reason/
   evidence_type/priority), then cite it. The build flags unknown keys.
4. Census figures always carry the round year in the key (census-YYYY per
   country) — never a bare "census".
5. URL-null is allowed with a reason; reason-null is not.
