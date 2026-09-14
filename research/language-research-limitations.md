# Language Research Limitations (Phase 15)

Pass 1 · Date: 2026-09-14. Read this before trusting any number in the inventory.

## 1. What this dataset is (and isn't)

- A **desk-research compilation** (pass 1 complete 2026-09-14: 194/194
  countries, 1338 entries, 1976 relations, 692 living canonical), not
  fieldwork. No speaker was interviewed; no community was consulted.
  1692/1976 relations lean partly on `agent-knowledge` (86%).
- **Preliminary flag is OFF** (`"preliminary": false` — coverage-gated at
  194/194), but pass-1 agent-compiled status stands until verification
  pass 2 replaces sources. Review queue: 0 open; report status COMPLETE
  (pass-1 sense only).
- **No learning pages may be generated from it yet** (Phase 16 gate).
  Course planning use of P0/P1 is indicative only.

## 2. Census staleness & politics (the big one)

Batch-2 additions: Uzbekistan has had NO census since 1989 (all figures estimated);
Turkmenistan's 2022 census published ~no language detail (all figures soft);
the UZ Tajik count (~1.7M official) is widely believed undercounted (dispute recorded
on the entry).
Batch-3 additions: Türkiye asks NO language question (all TR figures estimated);
Lebanon has had NO census since 1932 (lb-no-census-1932 gap-record cited);
Iraq's 2024 language detail still publishing; Syria's constitutional order is
transitional (post-Dec-2024); Gulf expat L1 splits are the softest numbers in the
dataset (press-estimates, ~2x variance, no-fabrication protocol enforced).

| Country | Latest usable round | Problem |
|---------|--------------------|---------|
| India | 2011 | 15 years old; no 2021 round; Hindi umbrella folds 100M+ non-Hindi returns |
| Pakistan | 2023 (digital) | contested in Sindh/Balochistan; Brahui folded into Balochi; Karachi Bengali/Rohingya undercounted |
| Bangladesh | 2022 | thin minority detail; Bihari/Urdu figures soft |
| Nepal | 2021 | best in batch; still mother-tongue self-report (prestige bias toward Nepali) |
| Sri Lanka | 2012 | ethnicity⇄language mapping (Moors, Vedda) |
| Afghanistan | none since 1979 | ALL figures are estimates; post-2021 ground truth unknowable from desk |
| Bhutan/Maldives/Iran | 2017/2022/2016 echoes | small-population noise; Iran has no language question (figures are scholarly estimates) |

## 3. Known soft spots (batch 1 — each is a pass-2 task)

1. **Ethnologue paywall**: 73 citations trace to edition 27 via secondary
   knowledge, not the live database. Any figure challenged in review must be
   re-sourced to the edition or replaced.
2. **Sign languages** (9 entries): code audit done 2026-09-14 (afg fixed ex-mis; ins/nsp/pks/psc/sqs
   confirmed; BD/BT/MV genuinely uncoded). Direct deaf-org consultation STILL pending; ISL dialect
   spread unresolved. Text-first readiness cap (PARTIAL) is a policy choice, documented in METHOD.
3. **Macro/code disputes** (pass-2 SIL bulk 2026-09-14 resolved the batch-1 set: mni/hye are scope=I
   individuals, NOT macros — claims withdrawn; doi/san ARE macros — members recorded; mrd retired→mgp;
   fas−tgk). Still open: Rajasthani macro; Hazaragi haz (may deserve PK entry); Pothohari pho;
   Marwari/Dhatki/Parkari Koli threshold batch (PK long-tail); Sambalpuri spv (ori-macro member, IN long-tail).
4. **Speaker bands are wide by design** (order-of-magnitude); point estimates
   in batch notes are midpoints, not measurements.
5. **Scripts reduced to one primary** per language (Kokborok, Konkani, Kashmiri,
   Sindhi, Punjabi-cross-border are multi-script — noted, not modelled).
6. **TTS/translation flags are capability proxies** (major-engine coverage
   knowledge), not tested integrations. TTS confidence recorded where shaky
   (npi: medium).
7. **Classical/liturgical/historical roles** don't affect scores the same way
   across batches yet — Pali/Prakrit (IN long-tail) vs Latin-type cases in
   future batches need a uniform rule (pass-2 METHOD amendment).
8. **English everywhere**: eng appears in 7/9 batch countries as official or
   working language; its score (57, P1) will move a lot as countryCount fills.
9. **Diaspora unmodelled**: learner demand from diaspora (Punjabi-Canada,
   Bengali-UK, Tamil-Malaysia…) is invisible to this schema. Phase 8's
   learningDemandProxy is a band proxy, not demand data.
10. **L1-less officials score artificially low** (known formula artifact): arb sits P2-40
    (speakerReach bottom band — MSA has no L1) despite 13 official statuses and 400M+ users.
    The final Phase-8 formula needs an official-reach/L2 term; until then the ekguru
    recommendation text (arb: recommended-course) carries the true verdict, not the band.
11. **The knn incident**: Kannada shipped one build under the wrong code
    (knn) and was caught by review, not by automation — the 639-1 guard now
    covers 37 pairs, but unlisted pairs have no net. Extend the table per batch.

## 4. Confidence semantics (how to read the labels)

- **high**: two independent tiers agree (e.g. constitution + census), or one
  tier-A source for a pure status fact. Still desk research.
- **medium**: single tier-B/C source, or tiers disagree on numbers but agree
  on the fact. Default for speaker figures.
- **low**: agent-knowledge only, or sources span >3× on the number, or the
  ground situation post-dates the source (Afghanistan). 41 relations carry
  review flags — the report lists them.

## 5. What would make this dataset trustworthy (pass-2 exit criteria)

1. `agent-knowledge` citations → 0 (replaced by tier A/B/C or explicit
   expert-consultation records).
2. SIL bulk check green per batch (batch-1 item closed 2026-09-14; re-run rule in METHOD).
3. UNESCO WAL endangerment flags joined (fetch failed — manual pass); WFD/deaf-org sign review done.
4. Every disputed/note-heavy entry (AF cluster, PK threshold batch, IN §8
   list) resolved or escalated to an expert with a dated record.
5. Census URLs archived per figure (Wayback where portals rot).
6. Independent re-check of a 10% sample by a second compiler.
7. 194/194 coverage — scores recomputed final, `"preliminary": false` — DONE 2026-09-14.

Until then: this inventory is a **working map with the swamps marked**, not a
survey. The swamps are marked honestly — that is its current value.

## 6. Pass-1 completion record (2026-09-14 — canonical + audits + flags)

- **Canonical 100%**: all 447 `_canonical.json` entries cover every
  official/national/widely-spoken code incl. group members
  (pbt/pst, kab/tmh/mzb/shy, nch/ncj/nhe/nhw, wlc/wni/zdj, mig/mks/mxb).
  Derived canonical: 694 living+historical; curated: 447.
- **P0 = 12** (ben/fil/guj/hin/kan/mal/mar/pan/ron/tam/tel/urd): Romanian
  joined P0 on the final recompute — score mechanics working as designed
  (EU official + 25M + diaspora + full TTS/MT). P1 = 52, P0/P1 = 64.
- **13 deep audits** in research/: IN/NG/ID/PG/PH/ZA/CN/RU/TR/IR/MY/TH/VN.
  Two "serious" gaps found by audits were closed same-day as pass-1
  entries: CN cjy/cdo/mnp, RU lez/dar/inh/ady, ID nan (+8 entries, 1338).
- **TTS/MT flags**: every P0 flag resolved (true/false, no nulls). MT
  resolved for all P0/P1. TTS stays honestly null for 9 P1 codes —
  pass-2 MUST verify each against live engines (Google Cloud TTS /
  Azure / Translate-app audio) before any voice-feature planning:

| # | Code | Language | MT | TTS | Why suspected-but-unconfirmed |
|---|------|----------|----|-----|-------------------------------|
| 1 | hau | Hausa | ✓ | ? | major-engine audio likely; untested |
| 2 | kmr | Kurmanji | ✓ | ? | Kurdish audio exists? variety unclear |
| 3 | nya | Chichewa | ✓ | ? | Nyanja audio unconfirmed |
| 4 | sna | Shona | ✓ | ? | audio unconfirmed |
| 5 | snd | Sindhi | ✓ | ? | text yes; audio likely absent |
| 6 | som | Somali | ✓ | ? | audio likely; untested |
| 7 | sot | Southern Sotho | ✓ | ? | audio unconfirmed |
| 8 | wol | Wolof | ✓ | ? | audio unconfirmed |
| 9 | yor | Yoruba | ✓ | ? | audio likely; untested |

- Deliberate nulls elsewhere (Fula varieties, Quechua/Kichwa, Pashto
  varieties, Kituba pair) record VARIETY-match uncertainty, not engine
  ignorance — pass 2 resolves per-variety, never by macro assumption.
