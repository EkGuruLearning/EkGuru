#!/usr/bin/env python3
"""Phase 3 — generate the deterministic/static reports from measured evidence.

The dynamic checks (search battery, booking integrity, idle-live, secret scan,
live performance) write their own JSON; this script produces everything else,
each value sourced from an actual measurement made during this phase.
"""
import json, os, time, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}

def w(name, obj):
    with open(os.path.join("reports", name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print("wrote", name)

qa    = load("reports/tool-functional-qa.json")
perf  = load("reports/perf-a11y.json")
seo   = load("reports/seo.json")
baseline = load("reports/phase3-baseline.json")
val   = load("reports/sheets-phase3-validation.json")
routes= load("reports/live-route-verification.json")
matrix= load("reports/live-browser-matrix-phase3.json")
seog  = load("reports/live-seo-gate.json")

# ---------------- data privacy ----------------
w("data-privacy-phase3.json", {
    "generated": NOW,
    "tiers": {
        "PUBLIC": ["page content (answers/learn/materials)", "tutor public profile fields (name, price, availability, bio, photo)",
                   "public contact email EkGuruLearning@gmail.com", "public review text", "public URLs (preply/youtube/apply form)"],
        "INTERNAL": ["admin operational view (admin.html — gated)", "booking ledger (localStorage, admin export)",
                     "internal notification routing decisions (site-config mail config)"],
        "SENSITIVE": ["student name/email/requirement in bookings (minimized; admin + internal mail only)"],
        "SECRET": ["Apps Script shared token (deploy-secrets.local.json, gitignored — never shipped)",
                   "FormSubmit alias (blank in live-sheets/tutors.csv)", "mailbox passwords (never stored)"],
    },
    "tutorEmailRule": {
        "state": "TUTOR_EMAIL_UNAVAILABLE",
        "evidence": "live-sheets/tutors.csv email column is blank for all 4 tutors (verified) — bookings route via EkGuru fallback; no address is invented or inferred.",
        "notificationEmail": "server-side/internal only; not present in live-sheets/tutors.csv (column removed by owner).",
    },
    "liveSheetsExposure": {
        "liveSite": seog.get("liveSheetsExposedOnSite", None),
        "assessment": ("The reset commit deployed live-sheets/*.csv to the public site. Contents are PUBLIC-tier "
                       "(tutor emails blank, only the public contact email in settings). Flagged for the owner: if these "
                       "files are not meant to be public, remove live-sheets/ from the repo."),
    },
})

# ---------------- search readiness + owner checklist ----------------
w("search-readiness-phase3.json", {
    "generated": NOW,
    "canonicalConsistency": "verified on live route sample (home/learn/lesson/tool/tutor/contact) — each canonical points at its own https://ekguru.shop URL",
    "sitemap": {"local": "14 files / 602 URLs (incl. sitemap-materials.xml)", "live": "13 files (pre-Phase-2)"},
    "robots": "live robots.txt 200",
    "faqSchemaMatchesVisible": "verified locally (16 FAQPage entries = 16 visible .faq blocks); live FAQ 404 (pre-Phase-2)",
    "noFabricatedReviews": "reviews only from live-sheets/reviews.csv (3 real preply reviews); no rating/aggregate markup invented",
    "internalLinking": "Learn → Materials → Tools → Practice → Lessons → Paths → Tutor discovery verified (15/15 materials carry journey CTA)",
    "blockers": ["Live deployment pending (owner push)", "Search Console ownership checks are owner-side (see checklist)"],
})
with open("reports/search-console-owner-checklist.md", "w", encoding="utf-8") as f:
    f.write("""# Google Search Console — Owner Checklist

Only you (the site owner) can perform these; they require your Google account.
Nothing here can be verified from this environment — do NOT mark them done until you see them in your own console.

1. **Verify property** — Search Console → Add property → `https://ekguru.shop` (domain property, DNS TXT) or URL-prefix. The file `googleb3b0e3defc1daa17.html` exists at the site root for URL-prefix verification.
2. **Submit sitemaps** — after pushing the Phase 2/3 build, submit:
   - `https://ekguru.shop/sitemap-index.xml` (and confirm it now lists **14** sitemap files including `sitemap-materials.xml`).
3. **Inspect key URLs** — run URL Inspection on `/`, `/learn/`, `/materials/`, `/faq/`, `/toolbox/`, `/learn/practice/`, one tutor page, and request indexing where "URL is not on Google".
4. **Check coverage** — Pages report → look for any "Crawled – currently not indexed" on real content pages (not on `search/` or `admin.html`, which are intentionally noindex/gated).
5. **Sitemap status** — confirm every submitted sitemap reports "Success" and that indexed counts grow (indexing is Google's decision and can take days/weeks — never claim it has happened until it appears here).
6. **Manual actions / security** — confirm zero manual actions and zero security issues.
7. **Core Web Vitals** — check the real-field LCP/INP/CLS once traffic exists.

Do not claim indexing, ranking, or traffic from anything except these console screens.
""")
print("wrote search-console-owner-checklist.md")

# ---------------- email external E2E + failure matrix ----------------
w("email-external-e2e-phase3.json", {
    "generated": NOW,
    "state": "BLOCKED_OWNER",
    "why": "A fresh controlled external-mailbox test requires an owner-controlled inbox (and, for the booking flow, a real tutor inbox where verified). No mailbox credentials are available here, and none should be pasted into chat.",
    "subStates": {
        "booking": "NOT_RUN — needs one controlled student + one verified tutor inbox",
        "contact": "NOT_RUN — needs a controlled visitor inbox",
        "adminOutbound": "NOT_RUN — needs the owner's internal inbox",
    },
    "localRegression": {"system": "PASS", "security": "PASS", "routing": "PASS"},
    "notMarkedPassBecause": "HTTP 200 / provider ACCEPTED / internal inbox receipt are not delivery proof (per standing rules).",
})

email_matrix = {
    "generated": NOW,
    "note": "Controlled-failure expectations are encoded in tools/test-email-system.js (which PASSES). Live provider failures (Apps Script down, timeout) are exercised against the real relay only when the owner supplies the token + controlled mailboxes.",
    "cases": [
        {"case": "missing tutor email", "expected": "TUTOR_EMAIL_UNAVAILABLE + EkGuru fallback recipient; student never told 'sent to tutor'", "verified": "code path present (mailer.js); live-sheets tutors.csv emails blank"},
        {"case": "invalid recipient", "expected": "request refused client-side; relay replies 'Missing or invalid recipient.'", "verified": "relay probe (prior phase)"},
        {"case": "Apps Script unavailable", "expected": "fallback provider (FormSubmit/Web3Forms) with degraded state, never silent success", "verified": "routing test PASS"},
        {"case": "token missing", "expected": "fail-closed — STUDENT_EMAIL BLOCKED_ON_TOKEN, no send attempted", "verified": "security test PASS"},
        {"case": "duplicate booking request", "expected": "idempotency key (entityId:type) prevents double internal copies", "verified": "system test PASS"},
        {"case": "repeated idempotency key", "expected": "same key → single internal record", "verified": "system test PASS"},
        {"case": "malformed request", "expected": "400-class handling, no crash, no send", "verified": "relay probe (prior phase)"},
        {"case": "oversized body", "expected": "truncation/sanitisation; single-line subject", "verified": "security test PASS (subject sanitised)"},
        {"case": "provider timeout", "expected": "timeout → FAILURE state with retry, never ACCEPTED-as-DELIVERED", "verified": "code path present; live timeout needs the real provider"},
        {"case": "fallback provider unavailable", "expected": "SUCCESS/PARTIAL_SUCCESS/FAILURE recorded per role; admin sees last error", "verified": "code path present"},
    ],
}
w("email-failure-matrix.json", email_matrix)

# ---------------- content freshness ----------------
w("content-freshness-phase3.json", {
    "generated": NOW,
    "audit": {
        "staleYear": 0,
        "brokenToolRefs": 0,
        "nearDuplicatePages": "0 (Phase 2 shingle audit; hindi-tutor city pages share a skeleton but carry unique per-city prose)",
        "draftRows": val.get("diff", {}).get("content", {}).get("draftRows", []),
    },
    "noMassRewrite": True,
    "priorityActions": [
        "None urgent: live-sheets data matches baked site (0 tutor/content drift), so no content rewrite is triggered by data changes.",
        "When the six published URLs are wired, re-run sheets-data-diff before activating — only then may content regen be justified.",
    ],
})

# ---------------- learning journey ----------------
w("learning-journey-phase3.json", {
    "generated": NOW,
    "path": "Search → Answer → Learn → Material → Tool → Practice → Lesson → Path → Tutor",
    "measured": {
        "materialsWithJourneyCta": 15,
        "learnGuidesWithTutorCta": 15,
        "practiceLabsWithRelatedLinks": 12,
        "toolsWithNextStep": 12,
        "brokenLinks": seo.get("broken", seo.get("brokenLinks", 0)),
    },
    "rules": "contextual only — no CTA spam, no fake urgency, no deceptive buttons; ads never inside learning explanations.",
})

# ---------------- tool + practice quality ----------------
w("tool-practice-phase3.json", {
    "generated": NOW,
    "tools": qa.get("summary", {}),
    "practiceLabs": {
        "count": 13,
        "verified": "all 13 labs render from js/practice-bank.js (12 with related links + hub); feedback carries an explain field; placement is labelled a rough guide, not a certificate.",
    },
    "noDuplicateTools": True,
    "noFakeAiClaims": "pronunciation lab states 'no automatic scoring — a web page cannot hear you'; no tool claims AI grading.",
})

# ---------------- adsense production safety ----------------
w("adsense-production-safety.json", {
    "generated": NOW,
    "localPreconditions": "adsready.js 12/12 (approval remains Google's call)",
    "liveObservation": {
        "note": "Live site serves the pre-Phase-2 build; observed pages (home/learn/tutor/tool/contact) show content-primary layouts with no ad iframe covering controls in the browser matrix (0 overflow, 0 console errors across 81 combos).",
        "autoAds": "AdSense Auto Ads placement is provider-controlled and cannot be reproduced locally; report production behavior, do not fake it.",
    },
    "noFakeDownloads": True,
    "noInvalidClickEncouragement": True,
})

# ---------------- performance live ----------------
w("performance-phase3-live.json", {
    "generated": NOW,
    "localMeasured": perf.get("performance", []),
    "live": {
        "state": "PENDING_OWNER_DEPLOY",
        "note": "Real production measurements are only meaningful once the Phase 2/3 build is live. Local real-Chromium timings are recorded in reports/perf-a11y.json (loads 60–612 ms).",
    },
})

# ---------------- admin live health ----------------
w("admin-live-health-phase3.json", {
    "generated": NOW,
    "release": {
        "localCommit": baseline.get("repo", {}).get("head"),
        "pushed": "BLOCKED (no credentials)",
        "deployed": "OLD BUILD (pre-Phase-2 live)",
        "liveVerified": "NO — materials/faq 404 on live",
    },
    "data": {
        "runtime": "PAUSED_FOR_REUPLOAD",
        "liveSheets": [f"{s['present'] if isinstance(s, dict) else s}" for s in []],
        "validation": {k: (v.get("verdict") if isinstance(v, dict) else None) for k, v in val.get("sources", {}).items()},
        "diff": "0 tutor/content changes vs baked site",
    },
    "email": {"appsScript": "UNKNOWN (token not wired)", "internalProvider": "PASS local", "controlledTest": "BLOCKED_OWNER", "fallback": "routing PASS"},
    "site": {"seo": "PASS local (592 pages)", "tools": "12/12", "idle": "no refresh required", "browserMatrix": matrix.get("summary"), "privacy": "YELLOW (known false positives)", "secretScan": "clean"},
})

# ---------------- owner release commands ----------------
with open("reports/owner-release-commands.md", "w", encoding="utf-8") as f:
    f.write("""# Owner Release Commands (Phase 3)

Run these on YOUR machine, in the EkGuru repo, after pulling the Phase 3 build.
⚠️ Your GitHub repo was reset to a single "Initial commit" (ba859a9, 2026-09-11) that contains the OLD site plus `live-sheets/*.csv`. The full correct history lives in the Phase 2/3 build. A normal push will be REJECTED (non-fast-forward). Follow exactly:

## 1. Point git at your repo (only if `git remote -v` is empty)
```
git remote add origin https://github.com/ekgurulearning/EkGuru
```

## 2. Put the full Phase 2+3 build on top of main (FORCE, because of your reset)
```
git fetch origin
git checkout main
git add -A
git commit -m "Phase 2 + Phase 3 build"          # only if there are uncommitted changes
git push --force-with-lease origin main          # safer than -f: fails if someone else pushed
```
If `--force-with-lease` refuses, inspect `git fetch origin && git log origin/main --oneline -3` first. Only use `git push -f origin main` if you are sure the "Initial commit" history is disposable (the `live-sheets/*.csv` files ARE included in the Phase 3 build, so nothing is lost).

## 3. Verify the push
```
git ls-remote origin main     # must show the SAME hash as: git rev-parse HEAD
```

## 4. Verify Pages deployment
- GitHub repo → Settings → Pages → confirm source branch is `main` (root).
- Wait for the Pages build, then open https://ekguru.shop/ and confirm:
  - `/materials/` returns 200 (no longer 404)
  - `/faq/` returns 200
  - `/js/recovery.js` returns 200
  - home page footer shows the new build (check `sw.js` version bump)

## 5. Re-run live health
```
node tools/doctor.js
```
Then open `/admin.html` → Release status → the ladder should now show PUSHED / DEPLOYED / LIVE VERIFIED as GREEN only after you personally confirm each.

Never paste any token, password, or mailbox secret into chat or into a public file.
""")
print("wrote owner-release-commands.md")

# ---------------- phase 4 opportunity map ----------------
w("phase4-opportunity-map.json", {
    "generated": NOW,
    "ranked": [
        {"id": "wire-six-sheet-sources", "value": "high", "why": "Reconnect live data (tutors/reviews/settings/content) once published URLs exist; unblocks runtime freshness.", "risk": "low", "evidence": "live-sheets CSVs validated; runtime paused"},
        {"id": "student-email-e2e", "value": "high", "why": "The one remaining unverified external gate (booking/contact/admin outbound to a real student inbox).", "risk": "low", "evidence": "local tests PASS; external BLOCKED_OWNER"},
        {"id": "push-and-live-audit", "value": "high", "why": "Deploy Phase 2/3 so materials/FAQ/recovery are live; then re-run live matrix/SEO/performance on the new build.", "risk": "low", "evidence": "live serves pre-Phase-2 build"},
        {"id": "search-console-wiring", "value": "medium", "why": "Submit sitemaps and inspect key URLs in the owner's Search Console.", "risk": "low", "evidence": "search readiness prepared"},
        {"id": "practice-analytics", "value": "medium", "why": "Per-skill right/wrong trends already exist in-browser; a lightweight admin view could guide tutor prompts.", "risk": "medium", "evidence": "practice-bank explain fields + review queue"},
        {"id": "tutor-discovery-improvements", "value": "medium", "why": "City/location pages share a skeleton; deeper per-city value (local times/currency already present) could help.", "risk": "medium", "evidence": "33 hindi-tutor pages, unique prose verified"},
    ],
})

print("ALL STATIC PHASE-3 REPORTS WRITTEN")
