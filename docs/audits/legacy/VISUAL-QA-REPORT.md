# EkGuru — Final Real-Browser Visual QA

**Branch:** `arena/2046092b-ekguru` @ `7ad9f99`
**Mode:** read-only. No source edits, no installs, no lockfile change, no commit/push, no deployment, no production Sheets, no real emails.

---

## Headline result

> **A real browser is NOT installed in this environment and could not be used.**
> **Every visual check is therefore `NOT VERIFIED`.**
>
> **Browser name/version: NONE — no browser was available.** No screenshots were
> captured, because there is nothing that can render a page. jsdom was **not**
> substituted for visual QA.

This is a hard environment limit, not a judgement about the page.

---

## 1. Is Playwright or another real browser installed? — **NO**

Exhaustively checked; nothing found:

| Looked for | Result |
|---|---|
| `playwright`, `playwright-core`, `@playwright/*`, `puppeteer`, `puppeteer-core` in `node_modules` | **none** |
| `package.json` dependencies | `{}` — no browser driver declared |
| `devDependencies` | `@resvg/resvg-js`, `ajv`, `ajv-formats`, `jsdom`, `terser` — **all non-browser** |
| `google-chrome`, `chromium`, `firefox`, `msedge`, `safari` on `PATH` | **none** |
| `/opt/google/chrome`, `/usr/lib/chromium`, `/snap/bin/chromium`, `/usr/bin/*firefox*` | **none** |
| `~/.cache/ms-playwright`, `~/.cache/puppeteer` (downloaded executables) | **none** |
| `wkhtmltoimage`, `wkhtmltopdf`, `phantomjs`, `electron`, `cutycapt`, `weasyprint` | **none** |
| Python `selenium`, `playwright`, `weasyprint` bindings | **none** |
| X display server (`$DISPLAY`, `/tmp/.X11-unix`) | **unset / absent** |
| CDP endpoints on 9222 / 9223 / 9515 | **closed** |

**Important:** the repo's own `tests/regression/test-browser-qa.mjs` (run by `npm test` as
`test:qa`) is **jsdom**, not a browser. It parses `support/index.html` as source to
assert release-mode facts. It produces no layout, no paint and no screenshot, so it
**cannot** stand in for visual QA.

Installing Playwright or Chromium was explicitly forbidden by your brief, so the
search stopped here rather than crossing that line.

## 2. Running the app locally — **DONE (serving correctly)**

The documented development command (`docs/RAZORPAY_INTERNATIONAL_API.md`) is:

```bash
npm start          # or: node server/server.js
```

| | |
|---|---|
| Command | `npm start` → `node server/server.js` |
| Bind | `0.0.0.0` (preview-compatible) |
| Port 3000 | already served the repo (**HTTP 200**) |
| Port 3001 | I started a second instance; **HTTP 200**, `pid 20246` |
| Live preview | `https://3001-{sandboxId}.e2b.app` |

Served assets verified against the working tree — byte-identical:

| Asset | HTTP | Bytes |
|---|---|---|
| `join.html` | 200 | 69,300 |
| `js/join-wizard.js` | 200 | 71,168 |
| `js/join-schema.js` | 200 | 20,151 |
| `js/intake.js` | 200 | 14,932 |
| `js/site-config.js` | 200 | 52,893 |
| `css/join-wizard.css` | 200 | 24,161 |

The server is static + mock-API only; nothing writes to the repo.

## 3.–5. Viewport testing, screenshots — **NOT VERIFIED**

| Viewport | No horizontal overflow | 7 steps | Prev/Next | Validation | Empty defaults | Review screen | Keyboard/focus | Submit + dbl-click |
|---|---|---|---|---|---|---|---|---|
| Desktop 1366 × 768 | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** |
| Mobile 360 × 800 | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** |
| Tablet 768 × 1024 | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** |

**Screenshots: NONE.** Without a rendering engine no screenshot can exist.

Horizontal overflow in particular is a pure layout property. It can only be
established by a layout engine that computes box sizes — static reading of CSS
**cannot** prove it, and I will not present it as if it could.

---

## 6. What *was* established — static facts only, explicitly non-visual

These are **structural/pre-logic** facts. They are **not** visual QA and must not be
reported as such. They are recorded only so the eventual human pass knows what to
expect.

| Fact | Value |
|---|---|
| Viewport meta | `width=device-width,initial-scale=1` (present) |
| Stylesheets | 4 external + 1 inline |
| Seven steps present in markup | **yes** — `jw-step-1` … `jw-step-7` |
| `.jw-back` / `.jw-next` | 1 each |
| Submit button | 1 — `type="submit"`, "Submit Tutor Application" |
| `#jw-duration`, `#jw-currency`, `#jw-hindi-level` | each first option `value=""`, label "Select", **no `selected` attribute** |
| Review header `[data-jw-pv-head]` | present; initial text `Your name` / `City, country` / avatar `?` — the deliberate fallback |
| Photo vs initials | no `<img>` in the header — initials path is the one wired |
| Labelled inputs | 39 `label[for]`; **0** inputs without an accessible name |
| ARIA live regions | 9 |
| `[tabindex]` / `[aria-current]` | 15 / 1 |

**CSS evidence, indicative only — NOT proof of rendering:**

- Breakpoints exist at `940px`, `640px`, `380px`, plus `prefers-reduced-motion` and `print`.
- At `≤640px` the form collapses to one column (`grid-template-columns: 1fr`), step
  chips hide their labels except the current one, and the day rows stack — i.e. the
  layout is *designed* for 360px, but only a browser can confirm it does not overflow.
- At `≤380px` time inputs get `min-width: 0; width: 100%` — again designed for narrow
  phones, unproven.
- Focus styling: 10 `:focus`/`:focus-visible` rules. The single `outline: none`
  (`css/join-wizard.css:602`, time inputs) is **not** an accessibility hole — it is
  immediately paired with `border-color` + `box-shadow: var(--jw-ring)`. Still
  unverified that the ring is *visible* against the real background.

---

## 7. Honest summary of prior evidence

Everything previously reported on the wizard UI came from **jsdom**, which has no
layout engine. That evidence covers *behaviour* (state, payload, text content) and is
sound for what it claims, but it says **nothing** about pixels. The `docs/audits/legacy/PREFLIGHT-AUDIT.md`
marked visual QA `NOT VERIFIED — pending`, and that marking still stands.

---

## 8. Exact human QA steps (2 minutes, in a real browser)

With the preview already serving `join.html`:

1. Open `/join.html` on the preview URL.
2. **Desktop 1366×768** → DevTools device toolbar, "Responsive", set 1366×768.
3. **Mobile** → 360×800. **Tablet** → 768×1024.
4. At each width, run in the console — expect `0`:

```js
document.documentElement.scrollWidth - document.documentElement.clientWidth
```

5. Walk all 7 steps with **Next**; press **Back** from step 2 to confirm state is kept.
6. Try **Next** with a required field blank → expect an inline error and no advance.
7. Confirm `duration`, `currency`, `hindi_level` still show **"Select"**.
8. On the review step, confirm your **name**, **city/country** and **initials** appear.
9. **Tab** through the form — every stop must show a visible ring.
10. Submission: do **not** hit the live endpoint. Mock it first —

```js
window.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve(
  { ok: true, reference: "EG-TEST01", mail: "skipped" }) });
```

then click Submit **twice quickly** and confirm exactly **one** request reached your
mock (the wizard also self-locks for 80 ms).

---

## 9. Confirmation

- **No source file changed.** `git status`: **7 modified, 16 untracked, 0 staged** —
  identical to before this turn.
- **No package installed, no lockfile change**, `package.json` untouched.
- **No commit, push, stage or reset.** `HEAD` still `7ad9f99`.
- **No deployment**, no Script Property, no production Sheet, **no real email**.
- The only side effect is a **local preview server on port 3001** (`pid 20246`),
  serving static files from the working tree.

**Stopping here. Visual QA remains `NOT VERIFIED` until a human runs §8 in a real
browser.**
