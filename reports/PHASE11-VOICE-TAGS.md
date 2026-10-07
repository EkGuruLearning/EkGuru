# Phase 11 — voice tag registry audit (first increment)

**Status:** first registry/completeness increment. Phase 11 voice-system work is not complete; no runtime voice behavior or source tag values were changed.

**Source command:** `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/after fasst.md` — Phase 11, item 1.

## Scope and findings

- Extended `tools/test-voice.mjs` so the 18 explicitly named core course tags are checked against `data/languages/registry.json` and the generated `js/voice-languages.js` map.
- The dynamic audit covers all 90 registry rows marked `course` or `starter_pack`, plus language-pack codes present in that registry (30; all are already in the 90). It checks source-to-generated name/tag parity, parses each tag with Node's `Intl.getCanonicalLocales`, and checks that each audio manifest has the same language tag and an entries array.
- The generated map has 94 entries: the 90 registry languages plus four legacy two-letter aliases. The test checks those aliases resolve to their canonical course entry.
- Added a behavior check that the more-specific registry tags `kmr` and `pbu` are retained while same-language device aliases `ku` and `ps` still match. Node's `Intl` canonicalizer normalizes `kmr` to `ku` and `pbu` to `ps`; this was not treated as evidence to broaden either source tag.

## Checks run

- `node tools/test-voice.mjs` — **28/28 passed**. Device speech, audio and microphone behavior are mocked.
- `python3 tools/build-voice-languages.py --check` — current generated map: 94 tags, 0 supplied recordings.
- `node tools/build-runtime.mjs --check` — `js/voice.js` is current at 7,391 bytes (within the 10 KB limit).
- `python3 tools/test-course-voice-buttons.py` — voice controls cover 12,599 authored items across 92 published level pages in 18 languages; optional IPA rendering remains data-only.
- `node --check tools/test-voice.mjs` and `git diff --check` pass.

## Limits and next work

- This is an offline source-to-output consistency check plus Node locale parsing, **not** a full validation against every current IANA Language Subtag Registry record. No device voice inventory was queried; mocks do not establish Android, iOS, desktop, accent or pronunciation availability.
- No native-speaker or human review of language/region choices was performed. In particular, keep the `kmr`/`pbu` specificity under review rather than silently substituting a broader language tag.
- All 90 audio manifests currently have no supplied recordings. No recording provenance or human-recording coverage is claimed.
- Remaining Phase 11 items—page-wide button coverage beyond the existing checks, speed/slow/repeat UX review, fallback review, listening/speaking practice, stroke-order animation and physical-device/browser QA—remain open.
