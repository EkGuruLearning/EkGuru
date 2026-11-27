# What ekguru.shop publishes — and what it never will (17 Nov 2026)

## The one fact behind everything
The repository is **public** and the site is a **static** site. There is no
server between a visitor and the files. So two things are true at once:

1. **Anything in the deploy set is downloadable by URL.** `js/print-sheet.js`
   is visible at `/js/print-sheet.js` because the browser has to download it
   to run it. Every website in the world works like this — open DevTools on
   any site and its JavaScript is there. This is not a leak. Minifying or
   obfuscating only makes it harder to read, never impossible, and it makes
   our own debugging worse, so we do not do it.
2. **Therefore nothing secret or personal may ever be in a committed file.**
   Secrets live in Apps Script *Script Properties* (`EK_ADMIN_TOKEN`,
   `MAILER_SHARED_TOKEN`) and in the payment server's environment
   (`RAZORPAY_KEY_SECRET`). Tutor and student contact details live only in
   the Google Sheet; the browser reads the sheet through `Unified.gs`, which
   strips `email`, `notification_email`, `contact_email`, `booking_id` and
   anything phone/UPI/bank-like before answering.

## What changed on 17 Nov 2026
| Before | After |
|---|---|
| GitHub Pages served the **repository root**: `/tools/…`, `/reports/…`, `/docs/…`, `/apps-script/Unified.gs`, `/server/…`, `/csv/…`, `/live-sheets/tutors.csv` were all live URLs. | `.github/workflows/pages.yml` publishes **only** the folder built by `tools/build-public-dist.py` (HTML, css/, js/, data/, images/, sitemaps, robots, ads.txt, CNAME, sw.js). |
| `live-sheets/*.csv` and `tutors-sheet.csv` — stale sheet exports with `email / notification_email / formKey` columns — sat in the repo. | Deleted. The sheet is read only through the feed. |
| No automated check. | `tests/regression/test-public-surface.mjs` runs in CI, in `build-all check` and in `sheet-sync` before every commit: no private dir in the deploy set, no e-mail other than the site's own, no phone-like number in tutor data, no secret-shaped string, every sitemap URL and sw.js precache entry still present. |
| `sitemap-tutors.xml` was not well-formed XML (`image:` prefix undeclared). | Fixed in `build-tutor-pages.js`. |

## ONE-TIME owner steps
1. **GitHub → EkGuruLearning/EkGuru → Settings → Pages → Build and deployment → Source: "GitHub Actions".**
   The first successful `pages` run normally flips this by itself; if the
   deploy step fails with "Not Found" or mentions the publishing source,
   set it by hand and re-run the workflow. CNAME / HTTPS are untouched.
2. **Cloudflare (interim, optional — protects today, before step 1 is live):**
   Security → WAF → Custom rules → Create → *Block* when
   ```
   (http.request.uri.path matches "^/(tools|reports|docs|research|apps-script|server|csv|live-sheets|tests|src|\\.github)/")
   or (http.request.uri.path in {"/package.json" "/package-lock.json" "/playwright.config.mjs" "/FINAL_REPORT.md" "/REAL-LIFE-TEST-REPORT.md" "/U0-ACCEPTANCE-REPORT.md" "/tutors-sheet.csv"})
   ```
   Keep it after step 1 too — it costs nothing and is a second lock.
3. **Redeploy `apps-script/Unified.gs` 2.1.1** (Deploy → Manage deployments →
   edit → New version). Same deployment, so the `/exec` URL stays.

## Reading the Cloudflare request log you pasted
Nothing in it is an attack.
- `17.166.*` (US) — Applebot (Siri/Spotlight indexing), fetching pages and the JS/CSS they reference.
- `2a03:2880:*` (US) — Facebook's link-preview crawler hitting `/`.
- `114.119.*` (SG) — Huawei PetalBot; `43.130.*`, `49.232.*` — Tencent cloud crawlers.
- `2405:201:*`, `2401:4900:*` (IN) — Jio / Airtel addresses, i.e. you and your testers.
- `/live-sheets/reviews.csv → 404` from an Indian address: that file never existed in the
  live build (`fallbackCsvUrl` is blank); the request was typed/visited directly.
- `/cdn-cgi/speculation`, `/cdn-cgi/rum` — Cloudflare's own features (Speed Brain, Web Analytics).
- `cacheStatus: dynamic` on HTML is Cloudflare's default (HTML is not cached unless a
  Cache Rule says so); `expired`/`revalidated` on `.js` is normal cache churn after a deploy.

## If you want the *code* itself private
That is a hosting decision, not a code change:
- GitHub Pages from a **private** repo needs a paid GitHub plan for an organisation, **or**
- move hosting to **Cloudflare Pages** (free, private GitHub repo allowed, same domain —
  you already use Cloudflare DNS). Build command: `python3 tools/build-public-dist.py --out _site`,
  output directory `_site`. The Apps Script, the sheet and every URL stay the same.
Either way the deploy set stays identical to what `build-public-dist.py` produces.
