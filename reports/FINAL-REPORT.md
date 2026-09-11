# EkGuru — Cumulative Final Report (v98 · 11 Sep 2026)

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
| Motion system | PASS — shared tokens + hamburger→X morph + backdrop, reduced-motion safe, 0 console errors at 390px |
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
- `tools/APPS-SCRIPT-SETUP.md` (new) — click-by-click deploy + the observed live
  contract + the one remaining step (the shared token).

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
`js/main.js` (backdrop element + aria wiring).

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
2. **HIGH — Apps Script token.** Set the shared word in both the script and
   `mail.appsScript.token`; the relay then carries mail itself.
3. **HIGH — Web3Forms live check** from a residential browser (datacenter-blocked here).
4. **HIGH — Tutor real addresses / formKey** (all 4 tutors route via EkGuru inbox today).
5. **MEDIUM — editorial:** originality audit, content depth, hreflang set,
   skeleton/toast motion layer, admin 1000-record pagination.

## 6. The single blocker, unchanged

The sandbox has **no git remote/credentials**; nothing can be pushed. All fixes
are local and packaged for release. After a deploy, `tools/doctor.js`'s
"deployed" check flips and the release decision moves to GO.
