# EkGuru Production Runbook (v98 · 11 Sep 2026)

Static site + browser-side mail chain + Google Sheets data + Apps Script relay.
No backend, no server cron. Every "system" below is a page-load component or a
browser-side flow.

| System | Purpose | Owner | Health check | Common failures | Recovery |
|---|---|---|---|---|---|
| **Booking** | Student → tutor request; record committed before email | Prakash | admin.html → Bookings tab (per-browser) | Email provider down, tutor has no address | Record already saved (`email_degraded`); admin retry re-sends; mailto fallback for the student |
| **Email chain** | Apps Script → Web3Forms → StaticForms → FormSubmit | Prakash | admin.html → Mail centre / provider matrix | Token missing (`Not authorised`), quota, activation, network | Chain auto-falls-through (v98); fix token → `js/site-config.js` `mail.appsScript.token` |
| **Apps Script relay** | Own-Gmail sending, no activation, ~90/day | Prakash | `GET …/exec` → `{"success":"true",…}` | Wrong deployment URL (extra letter), no "Anyone" access, token | Re-deploy Web App (Execute as Me / Anyone); correct id `…LnTPoOjqtdA` |
| **Sheets data** | Tutors/reviews/settings/content CSVs | Prakash | `python3 tools/test-data-sources.py` | Tab deleted → gid changes (HTTP 400) | Use Import → Replace CURRENT sheet (never "Replace spreadsheet"); update `csvUrl` gid in `js/site-config.js` |
| **Search** | Client-side index | Prakash | Search box on site | Index stale after content add | Rebuild index (tools) and redeploy |
| **SEO** | Canonical/sitemap/robots/ads.txt | Prakash | `ads.txt`, sitemap.xml | Old-domain refs, accidental noindex | `tools/seocheck.js`, domain sweep |
| **Health** | Provider + subsystem checks | Prakash | admin.html → Health | Datacenter IP bot-gated (false red) | Re-test from residential browser |
| **Privacy/security** | No secrets in client, no PII leaks | Prakash | `node tools/privacy.js` | Accidental key/token commit | Fix + redeploy; rotate key |
| **Copy protection** | Fingerprint/version/similarity | Prakash | contentguard tools | False positives | Allowlist + re-scan |
| **Backup** | Pre-edit snapshots | Prakash | `reports/backups-*/` | Missing snapshot | `tools/freeze-baseline.py` before destructive changes |
| **Deployment** | GitHub Pages → 301 → https://ekguru.shop | Prakash | `curl -I https://ekguru.shop/` | Stale files, `status:"soon"` persisted | Push + hard refresh + re-run live smoke |
| **Admin** | Unified records/ledger/health | Prakash | admin.html (passcode) | Locked out | Passcode reset in `js/gate.js` (session key `ekguru_admin_ok`) |
| **Analytics** | Consent-gated events | Prakash | analytics dashboard | Missing events | Verify `track()` wiring per page |

## Top 3 things to do right now
1. **Deploy** the local tree to production (it is ahead of live; live still shows `status:"soon"`).
2. **Set the Apps Script token** in `js/site-config.js` (script answers `Not authorised.` until then).
3. **Re-run** `python3 tools/test-email-e2e.py` from a real browser to confirm Apps Script carries the internal copy.

## Escalation
- Any email that fails still lands in the ledger with its `via`/`state`/`error` — open admin.html → Incidents.
- Never claim DELIVERED for a provider that only says ACCEPTED.
