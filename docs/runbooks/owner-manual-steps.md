# Runbook: steps only the owner can do

Code cannot do these. They live in Google, Cloudflare or GitHub settings.
No secrets or personal data belong in this file.

## 1. Deploy or redeploy the Apps Script (intake, live feed)

The Google Sheet is "EkGuru DB" (its id is in `docs/HANDOVER-FOR-AI.md`).

1. Open the sheet, then Extensions → Apps Script.
2. Paste the current source: `apps-script/Unified.gs` (recommended), or
   `apps-script/Intake.gs` and `apps-script/LiveFeed.gs` separately.
3. Deploy → Manage deployments → edit (pencil) → Version: **New version** → Deploy.
   A first deployment is Deploy → New deployment → Web app, execute as Me,
   access Anyone.
4. Setup notes: `apps-script/UNIFIED-SETUP.md`, `apps-script/INTAKE-SETUP.md`,
   `apps-script/LIVE-FEED-SETUP.md`.

Redeploy whenever a PR changes a `.gs` file. Merging does not deploy it.

## 2. Turn the live feed on

The site reads sheet tutors and reviews only when a feed URL is set.

1. Copy the deployed web-app URL (`https://script.google.com/macros/s/<id>/exec`).
2. Put it in `js/site-config.js` at `feed.url` (about line 751) and open a PR.
3. Check: `curl "<url>?action=health"` returns JSON.

Until this is done, sheet changes have no public effect.

## 3. Search Console

- Property: `https://ekguru.shop`.
- Sitemaps → submit `sitemap.xml` and `sitemap-places.xml`.
- URL Inspection → Request indexing for pages the owner has approved as new.
- Rich Results Test on one page with FAQ markup after a schema change.

## 4. Hosting and redirects (Cloudflare and GitHub Pages)

- Pages source is the repository root on `main` (`CNAME`, `.nojekyll`).
  **Changing the source folder is migration phase 4** and needs a redirect map
  first (see `docs/architecture/REPO-STRUCTURE.md` §6).
- To add redirects for old URLs, export the top 404 paths from Cloudflare
  Analytics and redirect only real, previously-live URLs.

## 5. Decisions only the owner makes

Record each in `docs/decisions/YYYY-MM-DD-<topic>.md`.

- Lifting the noindex freeze on tutor profile pages.
- Approving a new indexable page (`owner_approved_new_indexable`).
- Waiving the language gate for a language (never done by code).
- Whether the build side decides tutor visibility by `active` (current) or by
  `approved` plus `active` (what the runtime does).

## 6. Sheet hygiene (in the sheet, not the repo)

- A tutor's public photo must be a public file or an image in `images/`;
  a private Drive link shows nothing on the site.
- `notification_email` per tutor, so booking mail reaches the tutor and not
  only the owner inbox.
- Tag test bookings as `test` so the dashboard does not count them as open.
- Remove blank spare tabs; fix the dashboard cell that shows `#REF!`.
