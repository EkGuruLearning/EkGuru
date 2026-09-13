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

## Source hierarchy (agent assumption — owner's Phase 1 text arrived truncated)

Owner's spec pasted into chat was cut off at the "PHASE 1 — SOURCE
HIERARCHY" header. Until the full text arrives, this hierarchy applies:

1. National constitutions / statutes (official status) — `constitution`
2. National census bureaus (speaker numbers, mother tongues) — `census-<cc>-<year>`
3. Ethnologue (living-language counts, L1 estimates) — `ethnologue-27`
4. Glottolog (language-vs-dialect identity) — `glottolog-5.x`
5. UNESCO / UN data — `unesco`, `un`
6. "Languages of X" reference summaries (cross-check only, NEVER the
   sole source for a disputed claim) — `ref-summary`
7. EkGuru's own restcountries-derived registry (starting point only) — `ekguru-registry`
8. Agent training knowledge, flagged explicitly — `agent-knowledge`
   (confidence capped at `medium`; upgraded by verification passes)

Every language-country relationship carries `sources[]` + `confidence`.
Where sources disagree, the disagreement is preserved in `notes` with
`confidence: low` and `disputed: true`.

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
- Pass 2 (planned): per-country source re-check of every `medium`/
  `low` item against primary sources; upgrades confidence.
- The validator (`tools/validate-inventory.py`) enforces schema +
  reports coverage; it cannot verify facts — facts are verified by
  passes, recorded in `sources`/`confidence`.

## File layout

    data/language-inventory/
      METHOD.md                 this file
      sovereign-194.json        generated skeleton (cca2/cca3/name/region)
      supplement-3.json         PS / TW / XK (not in the 194)
      core/<subregion>.json     researched batches, e.g. southern-asia.json
