# EkGuru — 194-Country Language Inventory: Method

RESEARCH dataset, not course content. Answers: "194 countries mein log
kaun-kaun si languages bolte/sign karte hain, aur EkGuru ko kin
languages ko support karna chahiye?" No learning pages are generated
from this data until a language is explicitly promoted to course/pack
work (Phase 0 rule 8).

## The 194 (reconciled 13 Sep 2026)

Base = `reports/country-registry-phase7.json`, entries with
`independent=true`: **exactly 194 = 193 UN members + Vatican City**
(the source flags VA `unMember=true`; real-world: Vatican is a UN
observer, not a member — documented, not "fixed", because the flag
shape belongs to the upstream data).

- `sovereign-194.json` is generated from that filter. Never hand-edit;
  regenerate with `tools/validate-inventory.py --regen-skeleton`.
- Supplement (NOT counted in 194, inventoried so no major language is
  missed): Palestine (UN observer), Taiwan (disputed), Kosovo
  (partially recognised) → `supplement-3.json`.
- Registry header bug fixed v132: `sovereignStates` was 195
  (Vatican double-counted). Now 194.

## Source hierarchy (owner Phase 1 — exact)

PRIORITY A: national census/statistical offices · government language
portals · constitutional/legal language records · UNESCO / World
Atlas of Languages · Ethnologue/SIL (where accessible and licensable)
· Glottolog · ISO 639 datasets · official linguistic surveys ·
reputable academic linguistic databases.

PRIORITY B: major universities · recognized linguistic institutes ·
national education/culture ministries · high-quality research
publications.

PRIORITY C: secondary sources, cross-checking ONLY.

Never a country-language relationship from an SEO article/blog alone.
`core/_sources.json` registries every source key used in batches with
`source_name`, `source_url` (null only with a stated reason),
`evidence_type`, and priority A/B/C. Agent-compiled facts use key
`agent-knowledge` (below C, confidence capped at `medium`) until a
verification pass replaces them.

## Schema map (owner Phases 2–5)

Working research lives in `core/<subregion>.json` (one entry per
country, `languages[]` with `roles[]`). The BUILD (`tools/build-
inventory.py`) normalizes this into the owner shapes without loss:

- Phase 2 country inventory: one row per role — a language with roles
  [official, widely-spoken] appears in BOTH the official_languages
  and widely_spoken_languages arrays. Never collapsed.
- Phase 3 relationship record: country_id, language_id, names,
  iso_639_1/3, glottocode (null unless certain — never guessed),
  family, script, status_in_country, category, speaker band,
  country evidence, structured source, confidence, ekguru_priority,
  ekguru_reason, needs_human_review.
- Phase 4 canonical languages: dedup key = iso639_3 (real codes
  only). `mis` entries are NEVER canonical — each stays a
  per-country record with id `lang:mis:<CCA2>:<slug>`.
- Phase 5 language types: CANONICAL_LANGUAGE · VARIETY · DIALECT ·
  MACROLANGUAGE · SIGN_LANGUAGE, plus one documented extension —
  CLUSTER: a constitution/census-named cluster (Pashto, Nuristani,
  Tharu…) whose members carry individual codes. Forcing CLUSTER into
  MACROLANGUAGE would violate Phase 0 rules 12/15, so the deviation
  is explicit here and in every build output.
- Status enum LIVING/ENDANGERED/…: LIVING unless a Priority-A/B
  source says otherwise. Agent suspicion goes in notes, never in
  the status field (spec: do not infer endangered status).

## Speaker bands (Phase 3/7)

100M+ · 10M–100M · 1M–10M · 100K–1M · 10K–100K · <10K · unknown.
Bands derive from L1 estimates (else totals, else unknown).

## Priority + readiness (Phases 8–9)

Full scoring rules live in `tools/build-inventory.py` header and are
re-printed in every build output (transparent, no hidden weights).
All scores are PRELIMINARY until 194/194 coverage — the
number-of-countries component is incomplete by construction.

## Roles (closed enum)

`official` (state-wide) · `official-regional` · `national` (symbolic/
national language without full official function) · `widely-spoken`
· `lingua-franca` · `regional` · `indigenous` · `minority` ·
`immigrant` · `sign` · `liturgical` · `historical` (no L1 community)
· `extinct`.

## Listing thresholds (so "complete" stays honest)

- Official / national / widely-spoken / lingua-franca / sign: ALWAYS
  listed individually.
- Regional / indigenous / minority / immigrant: listed individually
  when EITHER officially recognised (constitution, statute,
  scheduled list) OR ≈100k+ L1 speakers. Below that, named in
  `notes` only for exceptional cases (e.g. the country's only
  indigenous language).
- The long tail is NEVER silently dropped: every country carries
  `livingLanguages: {count, source}` (Ethnologue/Glottolog figure)
  so the gap between "listed" and "existing" is explicit.

## Speaker numbers

Order-of-magnitude estimates (`l1`, `total`), each with `asOf` and
`confidence`. Census years differ per country; Ethnologue editions
differ per language. False precision is a bug: round to 2 significant
figures, never present a sum as exact.

## Language-vs-dialect (rules 12–16)

- Identity follows Glottolog/Ethnologue treatment; deviations are
  flagged `disputed: true` with both treatments in `notes`.
- Macrolanguages keep their ISO 639-3 macrolanguage code AND a note
  naming the covered varieties (e.g. `fas` Persian: Western/Eastern/
  Tajik treatments differ by country).
- Scripts are attributes (`scripts[]`), never identities. Families
  are attributes (`family`), never entries.
- Constitution-named CLUSTERS (e.g. "Nuristani", "Pamiri", "Tharu")
  are `group: true` entries with `iso639_3: "mis"` (ISO 639-3's
  reserved code for uncoded-in-one-code cases) and explicit
  `members[]` of individual codes. This names what the state names
  without pretending a cluster is one language.

## EkGuru recommendation (per language)

`ekguru: {status, recommendation}` where status ∈
`course` (full course exists) · `pack` (starter pack exists) ·
`recommended-course` · `recommended-pack` · `watch` (notable but no
action) · `none`. Recommendations weigh: speaker base, learner
demand, official status, script/tts feasibility, and content cost.
Tiny languages are inventoried, never auto-promoted (rule 8).

## Verification passes

- Pass 1 (this build): agent-compiled from hierarchy above.
- Pass 2 (batch-1 done 2026-09-14): SIL bulk check (tab +
  macrolanguages + retirements, fresh download) over EVERY cited code
  incl. members; sign-code audit; findings fixed + recorded in
  `research/language-data-sources.md` §4. RULE: re-run the SIL bulk for
  every new batch before commit — retirements happen mid-project
  (mrd→mgp merged 2026-07-15).
- Pass 2 (still pending): per-country source re-check of every `medium`/
  `low` item against primary sources; deaf-org consultation; UNESCO WAL
  manual flags. Upgrades confidence.
- The validator (`tools/validate-inventory.py`) enforces schema +
  reports coverage; it cannot verify facts — facts are verified by
  passes, recorded in `sources`/`confidence`.

## File layout

    data/language-inventory/
      METHOD.md                 this file
      sovereign-194.json        generated skeleton (cca2/cca3/name/region)
      supplement-3.json         PS / TW / XK (not in the 194)
      core/<subregion>.json     researched batches, e.g. southern-asia.json
