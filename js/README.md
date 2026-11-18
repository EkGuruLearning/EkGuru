# js/

Browser runtime. Plain JavaScript, no build step, loaded by pages with
`<script>` tags. About 160 files.

| Group | Files (examples) | Notes |
|---|---|---|
| Site settings | `site-config.js` | Feed URL, intake URL, currencies. `feed.url` is empty until the owner deploys the Apps Script |
| Tutors and sheet | `sheet.js`, `tutors/_registry.js` | Sheet-only tutors are published at runtime when `approved=yes`, `active` is not `no`, and there is a name and a real photo |
| Search and booking | `features.js` | Live search and the booking request modal |
| Course player | `course-player.js`, `course-<code>.js` | Progress and unlocks are kept on the learner's device |
| Learning tools | `flashcards-<code>.js`, `adaptive-practice.js`, `conversation-engine.js`, `voice.js` | Voice speaks only after a click |
| Admin | `admin-*.js` | Used by `admin.html` |
| Consent and analytics | `cookie-consent.js`, `analytics.js` | Cookie consent state; privacy-friendly analytics that set no cookie |

## Rules

- No framework, no bundler, no network call a page cannot work without.
- Never put an email address, phone number or secret in a file here. Tutor
  contact lives in the Google Sheet.
- A new behaviour needs a test that runs in CI (`tools/test-*`).
- `src/runtime/` is where runtime source will move (migration phase 3).
