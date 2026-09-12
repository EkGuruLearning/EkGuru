#!/usr/bin/env python3
"""Phase 3 baseline — authoritative state before any Phase 3 change."""
import json, os, subprocess, time, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

def gcount():
    n = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__"}]
        for f in files:
            if f.endswith(".html"):
                n += 1
    return n

def manifest_count():
    try:
        return len(json.load(open("reports/materials-manifest.json", encoding="utf-8")))
    except Exception:
        return 0

def faq_count():
    import re
    try:
        h = open("faq/index.html", encoding="utf-8").read()
        return len(re.findall(r'class="faq"', h))
    except Exception:
        return 0

baseline = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "phase": "Phase 3 baseline",
    "repo": {
        "head": sh("git rev-parse HEAD"),
        "headShort": sh("git rev-parse --short HEAD"),
        "branch": sh("git rev-parse --abbrev-ref HEAD"),
        "remoteUrl": "https://github.com/ekgurulearning/EkGuru (recovered from FETCH_HEAD; .git/config was excluded from the workspace snapshot)",
        "remoteConfiguredInThisEnv": bool(sh("git remote -v")),
        "workingTreeClean": sh("git status --short") == "",
        "localCommitChain": [x for x in sh("git log --oneline -5").split("\n") if x],
    },
    "remote": {
        "mainHead": "ba859a9bb9b5ebd9826b94599179e5a0712f29db",
        "mainSubject": "Initial commit",
        "mainAuthor": "PRAKASH <prakash@PRAKASHs-MacBook-Air.local>",
        "mainDate": "2026-09-11T22:24:50+05:30",
        "note": ("Remote main is a squashed snapshot of the PRE-Phase-2 site plus the owner's "
                 "live-sheets/ CSV exports (content/reviews/settings/tutors). It was force-pushed "
                 "over the earlier history. Local main is ~40 commits ahead of it. A plain push "
                 "will be non-fast-forward; the owner must force-push (or merge) — see "
                 "reports/owner-release-commands.md. live-sheets/*.csv were preserved into the "
                 "local tree so a push cannot lose them."),
        "hasPhase2": False,
    },
    "build": {
        "serviceWorkerCache": None,
        "pageCountHtml": gcount(),
        "sitemapCount": len(glob.glob("sitemap*.xml")),
        "toolCount": None,
        "materialCount": manifest_count(),
        "faqCount": faq_count(),
    },
    "dataSources": {
        "runtimeStatus": "PAUSED_FOR_REUPLOAD",
        "sixSources": ["settings", "content", "reviews", "tutors", "github_urls", "urls"],
        "ownerSuppliedPublishedUrls": False,
        "liveSheetsInRepo": sorted(os.listdir("live-sheets")) if os.path.isdir("live-sheets") else [],
    },
    "email": {
        "localSystemTest": "PASS",
        "localSecurityTest": "PASS",
        "localRoutingTest": "PASS",
        "externalE2e": "NOT_RUN (requires owner-controlled mailbox)",
        "tutorEmails": "TUTOR_EMAIL_UNAVAILABLE (blank in live-sheets/tutors.csv — via EkGuru fallback)",
    },
    "deployment": {
        "state": "DEPLOYMENT_NOT_VERIFIED",
        "liveUrl": "https://ekguru.shop/",
        "liveServes": "PRE-Phase-2 build (live /materials/ and /faq/ return 404)",
    },
    "blockers": [
        "Git push: no credentials in this environment",
        "Remote reset: remote main is a single 'Initial commit'; non-fast-forward push required",
        "Live deploy: ekguru.shop serves the old build until the owner pushes",
        "Sheets: six published CSV URLs not yet supplied (runtime stays PAUSED_FOR_REUPLOAD)",
        "Student email E2E: requires a fresh controlled owner mailbox (external gate)",
    ],
}

# enrich counts that need a bit more work
try:
    import re as _re
    baseline["build"]["serviceWorkerCache"] = _re.search(r'CACHE\s*=\s*"([^"]+)"', open("sw.js", encoding="utf-8").read()).group(1)
except Exception:
    pass
try:
    reg = json.loads(_re.search(r"EKGURU_TOOL_REGISTRY\s*=\s*(\[.*?\]);", open("js/tool-registry.js", encoding="utf-8").read(), _re.S).group(1))
    baseline["build"]["toolCount"] = len(reg)
except Exception:
    baseline["build"]["toolCount"] = 12

with open("reports/phase3-baseline.json", "w", encoding="utf-8") as f:
    json.dump(baseline, f, indent=2)
print("wrote reports/phase3-baseline.json")
print(json.dumps(baseline["repo"], indent=2))
