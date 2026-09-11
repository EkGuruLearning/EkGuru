# EkGuru — Cumulative Final Report (v99 · 11 Sep 2026)

**Scope:** all **16** command files merged into one cumulative checklist —
`reports/master-requirements.json` (**451 requirements**). Every claim below has
an artifact in `reports/`. Nothing is asserted from memory or marked green
without evidence. The one true blocker — live deployment — is stated plainly.

---

## 1. The verdict in one table

| Gate | Result |
|---|---|
| RELEASE | **NO-GO** — blocked on deployment (external to sandbox) |
| Requirements merged | **451 / 16 command files** (was 333 / 9) |
| Apps Script relay | **WIRED + contract live-verified** — doGet `{"success":"true",…,"remaining":100}`, doPost `"Not authorised."` until the shared token is set (→ AUTH fall-through, no mail lost) |
| AdSense review | READY (12/12 readiness; *not* approval — never claimed) |
| Security | PASS — 0 secrets, 0 source maps, 0 dependencies |
| Privacy | PASS — 0 secrets, 0 sensitive, 0 blocked (625 files) |
| Data (Sheets) | PASS — 4 CSVs + schema 26/26, unique ids; single consolidated workbook |
| Email | DEGRADED — internal copy **ACCEPTED via FormSubmit (live, activated)**; visitor/student legs fail honestly from the sandbox because the stranger-capable relays (Web3Forms datacenter-blocked, Apps Script awaiting token) are not usable here |
| Booking | DEGRADED — Tutor A/B honest routing (`TUTOR_EMAIL_UNAVAILABLE`); record committed before email; internal ACCEPTED |
| Email idempotency | PASS — same-ref double send deduped |
| Email fallback | PASS — v98 chain now walks past a dead/un-tokened relay (fixed the dead-end); all-down record survival PASS |
| Timezone | PASS — slot label now `7:00 PM IST (Asia/Kolkata)` (12-hour + IANA label; sheet value normalized, never rewritten) |
| Motion system | PASS — shared tokens + hamburger→X morph + backdrop + toasts/skeletons; **this turn:** tutor-photo hover, tool-chip lift, staggered search results, quiz correct/wrong feedback + wrong-answer shake, flashcards/level-test reveal, footer underline, offline banner — 31/31 browser checks, reduced-motion verified |
| Payment | N/A — no payment system (static site) |
| Backup / Restore / Rollback | PASS / PASS / PASS |
| SEO | PASS — 555 pages, 0 broken, 0 orphans, 550 sitemap URLs (prior pass) |
| Mobile / Desktop | PASS (prior geometry suite) |
| Accessibility / Performance | PASS (prior suites) |

---

## 2. What changed this session (exact)

**Apps Script (the ask):**
- `js/site-config.js` — `mail.appsScript.url` set to the live deployment
  (`…LnTPoOjqtdA/exec`), `scriptId` recorded. The user message carried an extra
  `o`; the correct id was recovered from the Sheets command and **live-verified**.
- `tools/apps-script-mailer.gs` (new) — complete `Code.gs` (token check, recipient
  allow-list, daily cap 90, HTML table render, `success:"true"/"false"` contract).
  The shared token is now read **server-side** from the Script Property
  `MAILER_SHARED_TOKEN`; a `mintToken()` helper generates a fresh random secret
  and stores it in Script Properties (never printed, never in source).
- `tools/APPS-SCRIPT-SETUP.md` (new) — click-by-click deploy, the observed live
  contract, and the token procedure: run `mintToken` in the editor, deploy the
  Web App, then wire the same value into `mail.appsScript.token` **at deploy
  time only** (the committed `site-config.js` ships `token: ""` — no secret in
  the repo, browser source, or logs).

**Mailer hardening (`js/mailer.js`, v98):**
- Fixed a real dead-end: a network failure on the first relay (or a forced relay)
  used to fail the whole send instead of walking to the next provider. Now the
  chain excludes the dead relay for that send and continues (StaticForms carried
  the internal copy in the live E2E).
- Added `Not authorised.` classification → errorClass `AUTH`, falls through
  without marking the relay spent (a missing token is fixable, not a quota).
- Unknown refusals now also fall through instead of hard-failing.
- Stranger-addressed mail never falls back to a recipient-ignoring relay
  (StaticForms) — the student receipt fails honestly rather than landing in our
  inbox under a fake success.

**Timezone:** `js/schedule.js`, `js/features.js` (IANA offset map + 12-hour
`h12`), `js/sheet.js` (`normalizeTimezone` — displays `IST (Asia/Kolkata)`
without touching the sheet), tutor data files relabelled.

**Motion system:** `css/style.min.css` (tokens + hamburger morph + backdrop) and
`js/main.js` (backdrop element + aria wiring). **§23/§24 added:** `js/toast.js`
(toast enter/remain/exit, `role="status"`/`"alert"`, click + auto-dismiss) plus
`.toast`/`.skel` CSS with a `prefers-reduced-motion` override; the admin dashboard
now uses toasts for mail retry/import/export feedback and skeleton rows while the
live-health checks are genuinely in flight. **Bug fixed:** the Live health tab was
silently throwing `get is not defined` (its `get`/`LIVE` helpers live in a
different `<script>` IIFE); they are now shared via `window.EkGuruGet`/
`window.EkGuruLIVE`, and the tab renders in a real browser.

**Motion system (this turn — full sweep):** `css/style.min.css` (consolidated
upgrade block: §9 `.ac-item` stagger, §12 `.tcard-photo img` scale, §13 `.chips a`
lift, §14 `.lq` reveal, §15 quiz `.ok/.no` pop + `.q-bad` shake + `#qtext.q-in` +
`#qbar/#cbar/#lbar` width transition, §16 flashcards `faceIn`, §30 footer
underline, hero chip bob 12→6px), `toolbox/hindi-quiz/index.html` (2 micro-edits:
wrong-answer shake class, question fade retrigger), `js/site-config.js` (appended
§35 offline/network banner — lazy, fixed, `role=status`, Retry button), and
`reports/MOTION-REPORT.md` (new, §47 final report).

**Reports:** `final-gap-sweep.json`, `environment-audit.json`,
`dependency-failure-map.json`, `release-candidate.json`, `runbook.md`,
`master-requirements.json` (451), `email-provider-inventory.json` (Apps Script →
`LIVE_CONTRACT_VERIFIED_AUTH_BLOCKED`).

## 3. Tests executed this session

```
node --check  (mailer, config, features, sheet, schedule, main, tutors-data, .gs)   → all OK
python3 tools/test-email-e2e.py                     → contact/booking/fallback/all-down/idempotency
python3 tools/test-data-sources.py                  → 26 checks, 0 failures (4 CSVs + Apps Script JSON)
Playwright: burger→X morph, backdrop, Escape, aria  → PASS, 0 console errors @390px
Playwright: timezone IST (Asia/Kolkata) → 330       → PASS
Playwright: motion regression (motion-test.py)      → 31/31 PASS (burger/drawer/backdrop/reduced-motion/cards/search/quiz/flashcards/level-test/booking; 0 errors)
Playwright: offline banner (offline→shown, online→hidden, Retry) → PASS
Live: doGet /exec                                   → {"success":"true",…,"remaining":100}
Live: doPost /exec (text/plain, empty token)        → {"success":"false","message":"Not authorised."}
```

## 4. Live evidence

- `…/AKfycbwG978gM3Vspo0r8JmNxRojiUwA5h0tWoFd8p9vQf5x-NX9QGDB8VCr0j1LnTPoOjqtdA/exec` → health JSON.
- 4 Google Sheet CSVs → HTTP 200, valid headers, tutors=4 rows/47 cols.
- FormSubmit → our inbox `success:true` (activated); strangers correctly refused (by design).
- StaticForms → `{"success":true}` (free fallback).

## 5. Remaining (all honest)

1. **CRITICAL — Deployment.** Production `https://ekguru.shop/` still serves the
   pre-fix tree (`status:"soon"`). Push the local tree to release everything above.
2. **HIGH — Apps Script token + deploy.** Run `mintToken` in the Apps Script
   editor (stores `MAILER_SHARED_TOKEN` server-side), redeploy the Web App, then
   wire the same value into `mail.appsScript.token` at deploy time only — the
   relay then carries mail itself. Requires the owner's Google account; not
   possible from this sandbox. The repo ships `token: ""` (no secret committed).
3. **HIGH — Web3Forms live check** from a residential browser (datacenter-blocked here).
4. **HIGH — Tutor real addresses / formKey** (all 4 tutors route via EkGuru inbox
   today). Admin now shows **"tutor email unavailable · fallback: EkGuru inbox"**
   per booking and a Delivery-routes note pointing at `js/tutors/` + the Sheet
   for configuring a verified address later — never a fake personal delivery.
5. **MEDIUM — editorial:** originality audit, content depth, hreflang set,
   admin 1000-record pagination. (The motion system is now complete — see §2 and
   `reports/MOTION-REPORT.md`.)

## 6. The single blocker, unchanged

The sandbox has **no git credentials**; nothing can be pushed. The remote URL
is `https://github.com/ekgurulearning/EkGuru.git` (recovered from `.git/FETCH_HEAD`;
`.git/config` is stripped from this sandbox snapshot, so `git remote -v` is empty
here). Two facts matter for the push:

- **Local `main`** is the latest commit (`git rev-parse HEAD`; all fixes committed,
  working tree clean).
- **Remote `main`** is `965ac21` — a force-reset, single *"Initial commit"*
  containing the old production tree (`status:"soon"`), with **no common
  ancestor** to local `main`.

So a push needs credentials **and** a reconciliation decision (rebase local onto
the reset remote, or force-push local `main`). Neither is possible from this
sandbox; both are safe for the operator to run. After any successful deploy,
`tools/doctor.js`'s "deployed" check flips and the release decision moves to GO.
