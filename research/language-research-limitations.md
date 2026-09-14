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
2. **Sign languages**: pass-2 SIL-table audit 2026-09-14 (7927-code
   table, 161 sign) resolved the code layer fully: 20 countries SIL-confirmed
   genuinely uncoded (BD/MV/KZ/KG/TJ/TM/UZ/AE/QA/KW/BH/OM/IQ/SY/LB/YE/AZ/
   GE/BN/TL + HT — wbs is IN-side, not BD; hps is Hawai'i, not Haitian);
   BT dyl confirmed CORRECT (batch-11 Damin claim was false memory).
   Fixed: pjm→pso (Polish), PE psl→prl (Peruvian; psl is Puerto Rican),
   hez→her (Herero), qom→tob (Toba), wra→wba (Warao) — 4 fabricated codes
   caught. Canonical hps/psl relabelled per SIL (spares, no relations).
   Direct deaf-org consultation STILL pending; ISL dialect spread
   unresolved. Text-first readiness cap (PARTIAL) is a policy choice,
   documented in METHOD.
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

- **Canonical 100% (pass-1 sense: 447; pass-2 final: 711 — see §7)**:
  all `_canonical.json` entries cover every official/national/
  widely-spoken code incl. group members (pbt/pst, kab/tmh/mzb/shy,
  nch/ncj/nhe/nhw, wlc/wni/zdj, mig/mks/mxb). Derived canonical: 694
  living+historical; curated: 711 (every derived code + spares).
- **P0 = 12** (ben/fil/guj/hin/kan/mal/mar/pan/ron/tam/tel/urd): Romanian
  joined P0 on the final recompute — score mechanics working as designed
  (EU official + 25M + diaspora + full TTS/MT). P1 = 54 (bho/mai promoted
  by pass-2 MT evidence), P0/P1 = 66. **Zero null flags** across all P0/P1.
- **14 deep audits** in research/: IN/NG/ID/PG/PH/ZA/CN/RU/TR/IR/MY/TH/VN
  + ET (audit-14, pass-2: 8 entries census-pinned, +7 missing majors —
  hdy/kbr/drs/gmv/gof/dwr/sgw — 1345 entries; stv held, Gurage ruling).
  Two "serious" gaps found by audits were closed same-day as pass-1
  entries: CN cjy/cdo/mnp, RU lez/dar/inh/ady, ID nan (+8 entries, 1338).
- **TTS/MT flags — PASS-2 PILOT DONE 2026-09-14** (89 TTS + 45 MT flips,
  evidence: Google-Cloud-TTS 61-locale list + Azure-Speech-TTS 125-locale
  list + Google-Translate language table + MS-Translator language table;
  4 A-priority sources registered in `_sources.json`). The 9-code TTS
  hit-list resolved: **som TRUE** (Azure so-SO UbaxNeural — the ONLY one);
  hau/yor/snd/sna/nya/sot/wol/kmr all FALSE (no voice on either engine).
  MT corrections: 14 TRUE→FALSE overclaims fixed (wol/fon/mos/umb/ven/mah/
  zgh/nhe/nde/kon/roh/cnr/sat/kik), 24 FALSE/NULL→TRUE underclaims fixed
  (kri/mai/bho/div/dzo/tet/hil/pam/pag/pnb/san/doi/bik/bak/chv/kas/brx +
  gaa/yua/fij/ssw/nso/tsn/mni), mkw TRUE→NULL (Google lists ktu only),
  kab/gil/hez/tsz/quc NULL→FALSE (both engines absent). TTS corrections:
  bel/hat/lat/kir/ceb TRUE→FALSE, kat/lao/khm/mya/amh/mlt/khk/prs→TRUE,
  xml→FALSE/FALSE (sign n/a). MS-only MT evidence: ton/bod/uzn/iu/quh stays;
  Google-only: quh/grn/aym/bam/gaz/san. Deliberate nulls kept: pbu/pbt/pst
  (ps voices exist, variety TBD), Fula varieties (ff MT exists, variety
  TBD), che (Yandex-only MT).

- Deliberate nulls elsewhere (Fula varieties, Quechua/Kichwa, Pashto
  varieties, Kituba pair) record VARIETY-match uncertainty, not engine
  ignorance — pass 2 resolves per-variety, never by macro assumption.

## 7. Pass-2 canonical completion (2026-09-14 — batches 8–11)

- **Canonical 711/711 = 100% TRUE**: every derived code (694) now has a
  curated canonical entry; codes lacking canonical = 0; script-null = 0;
  native-null = 1 (sgh, deliberate — no standard orthography).
  Batches: 8 (41 codes, 1M+ band incl. wuu/hsn/gan/aec/hmn),
  9a/9b (73, 100K–1M band), 10a/10b/10c (90, sub-100K spoken),
  11 (60 sign languages), + top-up (21 thin sign, 31 spoken natives).
- **Every batch-8–11 MT verdict is row-verified** against the saved
  Google-Translate (394 rows) + MS-Translator (288 rows) tables, not
  assumed. Surprises caught by probing: scn/ach/hrx/szl/bua/mhr(chm-row)/
  ltg/crh/haw TRUE (Google); pap TRUE Google-only (MS memory corrected);
  fao/hsb/dsb/iku TRUE MS-only; gla TRUE (gd experimental row).
  False memories corrected by probes: jje/esu/rue have NO row either
  engine (FALSE, not TRUE); Toba hit was Batak bbc, not Qom; Scots hits
  were Scots Gaelic only (sco FALSE); Limburgan li ≠ lim (NULL).
- **Corrections folded in**: xml canonical was Dravidian/Malayalam while
  relations use it as Malaysian Sign — fixed to Sign/Sgnw (ISO agrees);
  arn note wording fixed; tah confirmed absent from relations (no
  canonical needed — PF out of sovereign scope).
- **Deliberate MT-nulls now 24** (bxm/jvn/frr/stq/fui/qus/rmn/rmc/iii/
  lim added to the pilot set): each records a variety/code-match question
  (Google jv/bua/fy/ff/qu/rom/li rows, retired chm, Argentine Quichua),
  never engine ignorance. TTS-nulls: pbt/pbu/pst only (ps-voice
  variety TBD); all other 708 canonical carry explicit TRUE/FALSE both
  flags.
- Relation-grain backlog after completion: low-confidence ≈ 360 entries
  (medium 853 — the default band for speaker figures, §4), disputed 23;
  flag-unknowns are now confined to the deliberate-null set above.

## 8. Pass-2 dispute resolution (2026-09-14 — SIL-table audit)

- **Disputed 23 → 2.** Resolved 21: 20 uncoded-sign code disputes
  (SIL-table-confirmed genuinely uncoded, dated notes, disputed=false,
  confidence stays low, WFD consultation pending §5.3) + TR Adyghe
  speaker range narrowed 100–300k → 70–120k (last sourced diaspora
  split 1997: TR 71K/JO 44K/SY 25K; l1 set 100K, total 120K).
- **Held 2 (correctly)**: GE xmf (state-dialect vs ISO-language —
  political, unresolvable from desk; SIL xmf individual/living cited,
  expert escalation §5.4) and LK ved (isolate vs Indo-Aryan identity).
- **4 fabricated codes caught and fixed** (pjm/hez/qom/wra never in
  SIL) + 2 mislabelled sign codes (hps→Hawai'i, psl→Puerto Rican;
  Peruvian→prl, Haitian→mis). Full 711-canonical × SIL cross-check is
  now green. 2 A/C sources registered (97 total).
- Process note: the `_sources.json` top-level/inner-`sources` shape
  bit once (review-open jumped to 30 — new keys at wrong level);
  fixed same run, review-open back to 0.
- Tooling note: parallel same-file edits race (last write wins) — the
  §8 append was silently lost once and re-applied sequentially. Never
  batch two edits to one file.

## 9. Pass-2 null resolution (2026-09-14 — 639-1 audit + MI evidence)

- **MT-nulls 24 → 14.** Resolved 10: lim→TRUE (Google li IS 639-1 for
  lim — the batch-8 TBD was wrong), abk→TRUE (Google ab row found by
  systematic audit), dyu/emk→TRUE (explicit Bambara mutual
  intelligibility, served via Google bm), qus→TRUE (Southern Chinchay
  with quh, close to Cusco), qvi→FALSE (Northern Kichwa unintelligible
  to Southern-based qu), iii/kmb→FALSE (verified absent both engines),
  che→FALSE (Big-Tech absent; Yandex out of flag scope §3.6),
  frr/stq→FALSE (fy is Western-only; N/Saterland unintelligible).
  Plus msa/zho FALSE→TRUE (literal macro verdicts; spares, members
  carry practical verdicts). 7 C/D/B sources registered (104 total).
- **Held 14 (all documented variety-match questions)**: Fula set
  (fub/fuc/fuf/fuh/fum/fuv/fui — Google 'Fulfulde | ff' cover-term,
  training variety undocumented), ps set (pbt/pst MT + pbt/pbu/pst
  TTS — ps collective, variety TBD), rom set (rmn/rmc — macro row),
  mkw (ktu-only listing), bxm (weak MI evidence only), jvn
  (Surinamese-Javanese divergence unmeasured). Rule: flip only on
  explicit evidence, never by macro assumption (dyu/emk/qus had it;
  these 14 do not).
- Full 639-1→639-3 row-code audit (Google 188 + MS 128 distinct codes)
  is green: every other MT flag matches the engine rows (twi TRUE via
  'Twi (Akan) | ak', fat correctly FALSE, mon→khk, orm→gaz, pus/ps
  held, que members resolved, uzb→uzn Northern-only correct).
