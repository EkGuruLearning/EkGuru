# BUG FIX — Missing "Save & Next" / "Submit Application" Buttons

**Branch:** `arena/2046092b-ekguru`
**Scope:** `join.html`, `js/join-wizard.js`, `css/join-wizard.css` + 2 new test suites
**Backend:** untouched. No Apps Script change, no new endpoint, payments untouched.

---

## 1. Root cause

There were **two separate causes**, and neither was "a button is missing from the HTML".

### RC-1 — the buttons exist, but the CSS hides them until JavaScript claims the form

`.jw-nav` is visible only when the form carries the `.jw-on` class:

```css
/* css/join-wizard.css:196 */
.jw:not(.jw-on) .jw-step { display: block; }
.jw:not(.jw-on) .jw-nav,
.jw:not(.jw-on) .jw-jump { display: none; }
```

`.jw-on` is added by exactly one line, the first thing `init()` does:

```js
/* js/join-wizard.js:1219 */
form.classList.add("jw-on");
```

If that script does not run, or runs before a dependency it needs, **the fields
still render and still accept typing** — they are plain HTML — while the entire
navigation strip is `display:none`. That is precisely the reported symptom:
"the form allows me to fill in fields, but I cannot find a button."

This is not hypothetical. It is the current state of the **deployed** site:

| File | In the repo | In git (what Pages serves) |
|---|---|---|
| `js/join-wizard.js` | present, 1700 lines | **untracked — never committed** |
| `js/join-schema.js` | present | **untracked — never committed** |
| `css/join-wizard.css` | present | **untracked — never committed** |
| `join.html` | 995 lines, references all three | **407 lines, references none** |

`git show HEAD:join.html` holds the *old* single-page form — a `mailto:` form with
one `Send my application` button and no wizard at all. `HEAD:join.html` contains
**zero** references to `join-wizard`. So every push so far has published a
`join.html` from before the wizard existed; the wizard files are sitting in the
working tree, unserved.

**That is why "the buttons are missing" survives a push.** The fix has to include
committing the three files, or nothing changes on the live site no matter what
the CSS says.

### RC-2 — the profile-photo preview never displayed a Drive link

Reported second: "drive image ka link data hai vo preview mai dikhna chahiye ki
kiska hai". Two independent defects:

1. **Class-name mismatch.** The JS added `has-image`; the stylesheet styles
   `.has-img` (`css/join-wizard.css:537`). The tile could never leave its dashed
   empty state, so a *loaded* photo still looked like an empty box.
2. **A Drive share link is a web page, not an image.** `https://drive.google.com/file/d/<id>/view`
   put straight into a CSS `background-image` fetches an HTML document and
   renders nothing. The validator accepted the link, so the tutor saw a blank
   square and no error — the worst of both.

The repo already solves #2 for every public tutor card: `EkGuruSheet.photoUrl()`
in `js/sheet.js:219` rewrites the file id to `https://lh3.googleusercontent.com/d/<id>=w800`.
The form was simply not calling it.

---

## 2. Exact fix

### `js/join-wizard.js`

- **`photoPreviewUrl()`** (new) — resolves a pasted link through the site's single
  Drive resolver, `window.EkGuruSheet.photoUrl()`, instead of a second copy of the
  same regexes that could drift from the public pages. Falls back to a plain
  `https://` pass-through only if the resolver returns nothing.
- **`updatePhotoPreview()`** — now emits **`.has-img`** (matching the stylesheet),
  sets the preview from the *resolved* image URL, and labels the tile
  `role="img"` + `aria-label` so screen-reader users are told it loaded.
- **`clearPhotoPreview()`** (new) — one place that resets the tile, including the
  new broken state.
- **`probePhoto()`** (new) — a URL can pass every rule and still 404 (Drive file
  made private again). `background-image` fires no error event, so the tile is
  probed once with an `Image()`; on failure it shows ⚠️ and the sentence
  *"That link did not load a picture. In Google Drive, set sharing to Anyone with the link."*
  rather than leaving a blank square.
- **`renderPreview()`** — the review-step avatar now uses the same resolved URL.
  It previously checked only `/^https:\/\//`, so a Drive link produced a blank
  circle on the one screen where the tutor is supposed to confirm their face.

### `css/join-wizard.css`

- `.jw-photo-preview.is-broken` (new) — the visible failure state.
- `.jw-nav` — `position: relative; z-index: 1; min-height: 46px`; it is deliberately
  **not** sticky or fixed, so it can never cover the tutor's last field nor hide
  behind the page's own fixed Contact bubble.
- `≤640px` — Submit takes the **full row** at `min-height: 52px`; Previous/Next
  become `48px` and share a row. The card's bottom padding grows to `34px` so the
  last button clears the fixed `#contact-fab` (52×52, `bottom:14px`).
- `.jw-card { scroll-margin-bottom: 96px }` — a focused button never lands under
  a fixed corner element.

**No navigation logic changed.** `advance()`, `validateStep()`, `go()`,
`withStepLock()`, the submit handler, the dedupe identity, the honeypot ordering
and the payload contract are byte-identical. The only behaviour touched is the
photo preview and the responsive spacing.

---

## 3. Test results

`npm test` — **exit 0, 14/14 suites, 0 failures**:

| Suite | Result |
|---|---|
| razorpay (payments, unchanged) | 30/30 gates |
| join-wizard | pass |
| application-backend | 120 checks |
| defect-regressions (DEF-1…DEF-4) | 153 passed |
| wizard-sheets-e2e | 77 passed |
| **join-wizard-nav (new)** | **47 passed, 0 failed** |
| combined-code consolidation | 42 passed |
| browser-qa | 26 passed |
| runtime-qa | 143 passed |
| E2E gates / contract gates | 11/11 · 8/8 |
| live-feed | pass |

### New: `tests/regression/test-join-wizard-nav.mjs` — 47 checks

Covers the eight required regressions:

1. Next exists and is offered on steps 1–6 ✓
2. Previous is absent/disabled on step 1, present and enabled from step 2–7 ✓
3. Submit appears only on the review step; Next disappears there ✓
4. Buttons are wired — clicking Next advances, clicking Previous returns ✓
5. Invalid required fields block the **current step only**, set `aria-invalid`,
   render a summary, and move focus to the offending field ✓
6. Valid data advances ✓
7. Previous preserves every typed value; optional fields stay empty ✓
8. Final submission reaches the handler once, sets the in-flight guard, disables
   and relabels the button, and refuses a second and third press ✓

Plus: a failed send leaves the form unlocked with every answer intact and never
claims the application was received; and the full photo-preview matrix
(Drive `/file/d/`, Drive `open?id=`, direct `.jpg`, cleared, invalid).

### New: `tests/e2e/test-join-buttons-browser.mjs` — real Chromium (**SKIPPED here**)

`npm run test:browser`. It measures what only a layout engine can: computed
display/visibility, real `getBoundingClientRect` tap-target height, and
`document.elementFromPoint` to prove **nothing covers the button** — the fixed
Contact bubble, footer or a sticky bar. At 360 / 390 / 768 / 1366 px.

**It did not run.** Playwright and Chromium are not installed in this workspace
and the task forbids installing packages. The suite prints `SKIP` and exits 0
rather than passing silently, so CI cannot mistake absence for success. Run
`npm i -D playwright && npx playwright install chromium` to activate it.

**Therefore: no visual QA is claimed.** I have not seen this page rendered.

---

## 4. Remaining limitations

1. **No screenshot exists and none is claimed.** No browser, no Xvfb, no display
   in this environment. The jsdom suite proves behaviour; the Chromium suite
   proves pixels — and it has not been run. A human should load
   `/join.html` at 360 px and confirm the buttons before this is called done.
2. **RC-1 is a deployment problem, not only a code problem.** Committing the
   three wizard files is necessary but the push must actually land on the branch
   GitHub Pages builds from. If the live site still shows the one-button mailto
   form after this push, the Pages source is not this branch.
3. **`sw.js` caches aggressively.** A tutor who visited before may keep the old
   `join.html` until the service worker updates. Hard-refresh when verifying.
4. **The Drive preview depends on the file's sharing setting.** `lh3.googleusercontent.com`
   only serves files shared as *Anyone with the link*. The new ⚠️ state says so
   instead of failing silently, but it cannot make a private file render.
5. **Payments untouched** — `apps-script/Code.gs` was not modified, and no second
   submission endpoint was created. The wizard still posts to the single existing
   intake URL from `js/site-config.js`.
