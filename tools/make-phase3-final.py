#!/usr/bin/env python3
"""Phase 3 §22/§23/§24 — final gate, release manifest, owner handoff."""
import json, os, time, subprocess, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}

gates = {
    "repository_state_known": True,
    "push_verified_or_owner_blocked": "OWNER_BLOCKED (exact commands in reports/owner-release-commands.md)",
    "deployment_verified_or_owner_blocked": "OWNER_BLOCKED (live serves pre-Phase-2 build: /materials/ /faq/ 404)",
    "live_route_checks": load("reports/live-route-verification.json").get("summary"),
    "live_browser_matrix": load("reports/live-browser-matrix-phase3.json").get("summary"),
    "live_seo_checks": {"robots": 200, "sitemaps": 13, "leaks": "none", "liveSheetsExposed": True},
    "sheets_validated_or_correctly_paused": "VALIDATED (4/4 PASS) + runtime still PAUSED_FOR_REUPLOAD (correct)",
    "data_privacy_passed": True,
    "student_email_e2e_verified_or_owner_blocked": "BLOCKED_OWNER",
    "email_failure_matrix": "DONE (reports/email-failure-matrix.json)",
    "booking_snapshot_integrity": load("reports/booking-snapshot-integrity.json").get("pass"),
    "admin_live_health_updated": "DONE (8-state release ladder)",
    "search_quality": load("reports/search-quality-phase3.json").get("summary"),
    "tool_practice_quality": load("reports/tool-functional-qa.json").get("summary"),
    "production_ads_safety": "12/12 local preconditions; live observation clean",
    "production_performance": load("reports/performance-phase3-live.json").get("note"),
    "security_privacy": {"runtimeTokenHits": 0, "clientTokenBlank": True, "secretsGitignored": True},
    "idle_live_final": load("reports/idle-live-final.json").get("summary"),
    "release_zip": "PENDING (built in the next step of this turn)",
    "final_report": True,
}
overall = "YELLOW_PARTIAL_VERIFICATION"
gate = {
    "generated": NOW,
    "gates": gates,
    "overall": overall,
    "whyNotGreen": "Deployment to ekguru.shop, GitHub push, and the external student-email E2E test are owner-blocked. "
                   "Everything verifiable from this environment is measured and recorded; the three external gates "
                   "cannot be marked GREEN without owner action.",
}
with open("reports/phase3-final-gate.json", "w", encoding="utf-8") as f:
    json.dump(gate, f, indent=2)
print("wrote phase3-final-gate.json ->", overall)

# ---------------- owner handoff ----------------
handoff = """# Phase 3 — Owner Handoff

Read this first. It lists only what YOU must do; everything I could verify is already done and committed.

## A. Exact Git commands
The GitHub repo was reset to a single "Initial commit" (ba859a9) that contains the OLD site + `live-sheets/*.csv`. The full Phase 2+3 build (with that data preserved) is in the local repo. A normal push is REJECTED — force-push is required:

```
cd <path-to-EkGuru>
git remote add origin https://github.com/ekgurulearning/EkGuru   # only if missing
git fetch origin
git push --force-with-lease origin main
git ls-remote origin main     # must equal: git rev-parse HEAD
```

Only use `git push -f origin main` if `--force-with-lease` refuses and you have confirmed the "Initial commit" history is disposable (nothing is lost: `live-sheets/*.csv` are inside this build).

## B. Exact Google Sheets action
The six runtime data sources are still PAUSED_FOR_REUPLOAD. To reactivate:
1. In each Google Sheet: File → Share → Publish to web → CSV → publish.
2. Paste the six published URLs into `js/site-config.js` (the four `csvUrl` fields + the GitHub-URLs and EkGuru.shop-URLs sources) — NOT into chat, NOT into any public place that ships the links (they are public-read URLs, but keep them in the config mechanism).
3. Run `python3 tools/test-data-sources.py` and only activate sources whose schema, rows, and privacy classification pass.
Your current data already lives in `live-sheets/{content,reviews,settings,tutors}.csv` (validated: 4/4 PASS, 0 private emails) — those are snapshots, not the runtime source.

## C. Exact email E2E action (one controlled test)
Using a mailbox you control (not the site's own inbox):
1. Open a tutor page → book a trial with that controlled address.
2. Confirm the STUDENT inbox receives the confirmation (subject, reference number, tutor identity, no duplicates).
3. Confirm the tutor (if they have a verified inbox) and EkGuru internal each receive theirs.
4. Record the results in `reports/email-external-e2e-phase3.json` as VERIFIED / PARTIAL / FAILED.
Never paste mailbox passwords anywhere.

## D. Exact production verification URL list
After pushing, open each and confirm 200 + correct content:
- https://ekguru.shop/           (home)
- https://ekguru.shop/learn/
- https://ekguru.shop/materials/   ← must change from 404 to 200
- https://ekguru.shop/faq/         ← must change from 404 to 200
- https://ekguru.shop/js/recovery.js  ← must change from 404 to 200
- https://ekguru.shop/find-tutors.html
- https://ekguru.shop/tutor/sushila-g/
- https://ekguru.shop/contact/
- https://ekguru.shop/admin.html   (release ladder must show the new commit)

## E. What is verified (already done, in reports/)
- Local build: SEO PASS (592 pages, 0 broken), tools 12/12, booking snapshot immutability PASS, security scan clean (0 runtime token hits), idle/recovery clean on the new build, live browser matrix 81 combos / 0 problems, live performance measured, live-sheets CSVs validated 4/4.
- Production (current, pre-Phase-2 build): 10/12 routes verified; /materials/ and /faq/ 404 (expected — not yet deployed).

## F. What is blocked
1. GitHub push — no credentials in this environment.
2. Live deployment — ekguru.shop serves the old build until you push.
3. Six published Sheet URLs — not supplied; runtime stays PAUSED.
4. Student email E2E — needs your controlled mailbox.

## G. What must NOT be changed manually
- Do not re-edit generated files by hand: js/admin-stats.js, js/materials-registry.js, js/learn-quality.js, search-index.json, materials/*, faq/index.html — they regenerate from tools/ (build-materials.py, build-faq.py, build-search-index.py, learn-tools-audit.py, adminstats.js).
- Do not paste the Apps Script token into any committed file; it lives only in deploy-secrets.local.json (gitignored) and is wired by tools/wire-token.py.
- Do not invent tutor email addresses — blank means TUTOR_EMAIL_UNAVAILABLE (EkGuru fallback).
"""
with open("reports/phase3-owner-handoff.md", "w", encoding="utf-8") as f:
    f.write(handoff)
print("wrote phase3-owner-handoff.md")
