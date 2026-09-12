# EkGuru — Critical Email Routing + Booking Record + Multi-Provider Failover — Final Report

> **STATUS UPDATE (11 Sep, later the same day):** re-probed from a real
> browser origin — **FormSubmit is now ACTIVATED for `EkGuruLearning@gmail.com`**
> (answers `{"success":"true"}`) and still correctly refuses strangers.
> The internal copy therefore goes out **via FormSubmit (live)** again, not
> StaticForms. The tables below document the earlier "needs activation" finding;
> the activation link has since been clicked and the relay works. The
> stranger-addressed legs are unchanged: they need a stranger-capable relay
> (Apps Script — live, awaiting its token — or Web3Forms, which is
> datacenter-blocked here). Also: **Apps Script is now wired** into
> `js/site-config.js` and live-verified (`doGet` health JSON + `doPost`
> `"Not authorised."` until the shared token is set).

**Date:** 2026-09-11 (Asia/Calcutta)
**Command:** `EkGuru_ULTRA_Critical_Email_Booking_Routing_Failover_Command.md` (P0)
**Rule honoured:** completion claimed only from real end-to-end evidence —
`reports/email-e2e.json` (real Chromium against real provider endpoints) and
`reports/provider-probe.json` (direct live probes). No `DELIVERED` claim is made
anywhere; the provider only ever confirms **ACCEPTED**.

---

## 1. Verdict

| Area | Result | Basis |
|---|---|---|
| Contact — internal copy | **PASS (ACCEPTED)** | live send via **StaticForms** after FormSubmit fallback |
| Contact — visitor copy | **UNVERIFIED** | routes via Web3Forms; blocked from this datacenter (Cloudflare 403) — works from real user browsers |
| Booking — tutor routing | **PASS (honest)** | Tutor A & B both resolve; no hard-coded generic tutor inbox |
| Booking — internal record | **PASS (ACCEPTED)** | live send via StaticForms |
| Booking — student copy | **UNVERIFIED** | routes via Web3Forms (same datacenter limit) |
| Fallback (per provider) | **PASS** | FormSubmit "needs Activation" → StaticForms carried it, live |
| All providers down | **PASS** | honest failure + record survived + ledger problem recorded |
| Idempotency | **PASS** | same ref sent twice → internal role deduped |
| Admin retry (booking + contact) | **PASS** | retry from record room, `force` re-send, audited |
| Negative tests | **PASS** | bad email rejected; empty name/message rejected |

Overall: **DEGRADED, not GREEN** — everything verifiable from this environment
passes; the Web3Forms legs cannot be verified from a datacenter IP and are
stated as UNVERIFIED rather than faked.

---

## 2. Provider inventory (live evidence)

`reports/email-provider-inventory.json` — statuses from real requests:

| Provider | Status | Evidence |
|---|---|---|
| Web3Forms | configured (5 keys), **unverifiable from datacenter** | curl → HTTP 403 "server IP (Pro plan)"; browser fetch → no response |
| StaticForms | **LIVE_VERIFIED** | `{"success":true,"message":"Form submitted successfully"}` |
| FormSubmit | **NOT_ACTIVATED_RETIRED** | every address → `"This form needs Activation..."` |
| EmailJS | not configured | empty service/template/public key |
| Apps Script | not configured | empty url/token |

Capability matrix: `reports/email-provider-matrix.json`.

---

## 3. Real mailbox evidence (`reports/email-e2e.json`)

- **A — contact:** internal copy **ACCEPTED via StaticForms**; visitor copy
  `FAILED` with `errorClass: NETWORK` (Web3Forms unreachable from datacenter —
  not a code fault).
- **B — booking Tutor A (sushila-g) vs Tutor B (tara):** both report
  `tutorEmailStatus: TUTOR_EMAIL_UNAVAILABLE` (no personal address on file) and
  the internal record **ACCEPTED via StaticForms**. The hard-coded generic
  tutor-email bug is gone: no tutor is faked as owning the platform inbox.
- **C — fallback (Web3Forms blocked):** internal copy still **ACCEPTED via
  StaticForms**.
- **D — all providers down:** `thrown: "Failed to fetch"` (honest), and
  `record_survived: true`, `problems_include_all_down: true`.
- **E — negative:** invalid email rejected with a clear message.
- **F — idempotency:** same ref twice → the internal role was deduped (no second
  StaticForms request); the failed visitor role correctly retried.

---

## 4. Bugs found and fixed (all real)

1. **FormSubmit "needs Activation" was thrown as a fatal error.** The code
   claimed our inbox was "activated in v49 and stays forever"; the live endpoint
   says otherwise. → `js/mailer.js` now classifies the activation refusal as a
   **permanent** error, retires the relay for the month, and falls back (our own
   inbox is carried by StaticForms, free). Contact form and booking records now
   survive a dead FormSubmit.
2. **Hard-coded generic tutor email.** Three tutor files carried
   `EkGuruLearning@gmail.com` (the platform inbox) as the tutor's personal
   email. → cleared to `""`; bookings now report `TUTOR_EMAIL_UNAVAILABLE`
   honestly instead of pretending a personal delivery.
3. **No idempotency.** → `ekguru_mail_sent_v1` store + `guarded()` keys
   `CONTACT-{ref}-VISITOR/INTERNAL`, `BOOKING-{ref}-TUTOR/STUDENT/INTERNAL`.
4. **`delivered` vocabulary** overstated reality. → results now carry
   `state: ACCEPTED` + per-role `emailStates`; UI says "accepted"/"routed".
5. **Booking could disappear on email failure.** → `js/features.js` now commits
   the record **before** sending (status `sending`), then updates to `sent` or
   `email_degraded`; the student is told the request is saved, not "failed".
6. **No admin retry / incident alerts.** → retry buttons in the Bookings and
   Contact record rooms, and a deduplicated Incidents panel in the Mail centre.

---

## 5. Files changed

- `js/mailer.js` — activation classification + fallback; `ownInboxRelay(to)`;
  idempotency store + `guarded()`; `force` retry; `state`/`via`/`errorClass` on
  every result; `tutorEmailStatus`; per-role `emailStates`; `sentLog`/`clearSent`.
- `js/features.js` — commit-before-send; `email_degraded` handling; ref reuse;
  tutor-unavailable receipt note; richer ledger entries.
- `js/contact.js` — ledger `emailStates`/`via`/failed recipients.
- `js/store.js` — snapshot fields (`tutorEmailStatus`, `tutorEmailNote`,
  `emailStates`, `error`).
- `js/ledger.js` — `tutorEmailStatus` + `emailStates` fields.
- `js/i18n.js` — `book.emailDegraded` (7 languages).
- `js/tutors/hemlata.js`, `js/tutors/sushila-g.js`, `js/tutors/tara.js` —
  removed the platform-inbox placeholder email.
- `admin.html` — honest delivery-route text; Bookings "Emails" column + retry;
  contact records + retry; Incidents panel; sent-log clear; References "Via".
- New tools: `tools/test-email-e2e.py`, `tools/probe-providers.py`,
  `tools/make-email-reports.py`, `tools/merge-email-requirements.py`.
- New reports: `email-provider-inventory.json`, `email-provider-matrix.json`,
  `email-e2e.json`, `provider-probe.json`.
- Backups of all edited files: `reports/backups-20260911/`.

---

## 6. Remaining blockers (exact)

1. **Web3Forms delivery** cannot be verified from this sandbox (Cloudflare
   blocks datacenter IPs). Verify from a real user browser; the site is
   configured with 5 valid-UUID keys.
2. **FormSubmit activation** — open `tools/mail-activate.html` and click the
   activation link FormSubmit emailed to `EkGuruLearning@gmail.com`, then clear
   the quota/sent stores in the Mail centre. Until then StaticForms carries
   your-own-inbox mail (free, working).
3. **Deployment** — the whole tree (including these fixes) is staged locally and
   not pushed; production still serves the pre-fix tree (no git remote in the
   sandbox).
4. **Real tutor email addresses** — none are on file; the honest state is
   `TUTOR_EMAIL_UNAVAILABLE` until personal addresses (or formKey aliases) are
   added.

**Live status: DEGRADED (email/booking).** No GREEN claim is made for any
provider leg that was not actually observed to accept a message.
