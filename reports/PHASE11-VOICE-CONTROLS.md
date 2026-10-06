# Phase 11, item 2 — voice controls (increment)

**Status:** source, generated-page and mocked-runtime checks pass in a clean staged-tree fixture. Native-browser, keyboard, assistive-technology, physical-device voice and human linguistic review remain pending; this is not a release-readiness claim.

This increment follows the Phase 11 voice-tag registry audit in [`PHASE11-VOICE-TAGS.md`](PHASE11-VOICE-TAGS.md). It adds no authored vocabulary or examples and does not claim that synthetic speech is a native recording.

## Work completed

- Added a page-wide structural audit for native voice buttons, link nesting, hidden controls and explicit `type="button"` within forms.
- Updated the language-course and topic generators so a speaker button is never inserted inside an existing link. Target text in links retains appropriate `lang` attribution; the link remains the single interactive control.
- Updated the migration patcher to detach existing voice buttons from links while preserving authored text and protecting script/style contents. The transform is idempotent.
- Extended mixed Marathi/Hindi fixtures and generated-page audits; Hindi-labelled cells and `lang="hi"` spans are excluded from Marathi coverage counts.
- Added native, named speaker buttons beside the 32 spoken language names in the language directory. The shared runtime now honors legacy `data-lang` values and supplies missing accessible names to recognized controls when it mounts.
- Retained the shared speed, slow, repeat and stop behavior, with mocked UX checks for availability, state, labels and playback rate.

## Checks run

On a clean fixture made from the staged tree:

- Page-wide structural audit: **67,146 native voice controls across 869 of 2,754 HTML pages**; no controls nested in links; form controls explicitly use `type="button"`.
- Authored course-content audit: **12,599 items across 92 published levels in 18 languages**.
- Language-course/topic generator audit: **306 course pages, 297 topic pages and 9 hubs**; visible wording preserved and Hindi examples kept distinct from Marathi controls.
- Voice runtime suite: **28/28** mocked checks.
- Mounted controls: **20/20** jsdom checks, including all 32 language-directory buttons, explicit `data-lang` routing and legacy Storybook naming.
- Speed/replay UX: **8/8** jsdom checks.
- `tools/build-runtime.mjs --check`: generated `js/voice.js` matches `src/runtime/voice.js` at **7,671 bytes**.

These are repository, static-markup and mocked-DOM results. The page-wide structural count does not assert that every HTML page should contain a voice control; pages without scoped spoken learning content were not treated as gaps solely because they lack one.

## Still pending

- Verify keyboard activation/focus and the accessible-name computation in a native browser, then test with assistive technology.
- Verify actual voice availability, playback and rate behavior on Android, iOS and desktop devices; mocks do not establish device support or pronunciation quality.
- Obtain native-speaker/human review of language tags, examples and pronunciation; automated checks are not linguistic approval.
- Review any remaining Phase 11 work items, including listening/speaking practice and stroke-order animation, separately rather than marking the whole phase complete.
