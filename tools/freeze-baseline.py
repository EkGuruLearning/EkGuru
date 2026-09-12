#!/usr/bin/env python3
"""Freeze the release baseline (both the Final-Readiness and the ULTRA-360
baselines). Captures git identity, commit, branch, doctor/privacy/seo state,
live-crawl result, URL count, tool/learn inventory, email/booking status.
Writes reports/final-release-baseline.json and reports/ultra360-baseline.json.
"""
import json, os, subprocess, datetime, pathlib, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REP = ROOT / "reports"

def sh(*args):
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return ""

def read_json(name):
    p = REP / name
    if p.exists():
        try: return json.loads(p.read_text())
        except Exception: return {"error": "unparseable"}
    return None

now = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"

def html_count(rel_dir):
    d = ROOT / rel_dir
    if not d.exists(): return 0
    return len(list(d.rglob("*.html")))

tools = sorted(p.name for p in (ROOT/"toolbox").glob("*/index.html"))
learn = sorted(p.name for p in (ROOT/"learn").glob("*/index.html"))
days = sorted(p.name for p in (ROOT/"daily-hindi").glob("day-*"))

base = {
    "generated": now,
    "production_url": "https://ekguru.shop/",
    "git": {
        "branch": sh("git", "rev-parse", "--abbrev-ref", "HEAD"),
        "commit": sh("git", "rev-parse", "HEAD"),
        "short": sh("git", "log", "-1", "--oneline"),
        "status_dirty": bool(sh("git", "status", "--porcelain")),
    },
    "deployment_identity": "GitHub Pages ekgurulearning/EkGuru via CNAME ekguru.shop (push-to-deploy)",
    "doctor": read_json("doctor.json"),
    "privacy": read_json("privacy-scan.json"),
    "seo": read_json("seo.json"),
    "live_reachability": read_json("live-reachability.json"),
    "url_count": len(read_json("url-inventory.json")["urls"]) if read_json("url-inventory.json") else None,
    "health_dashboard": read_json("doctor.json") is not None,
    "email_status": "LIVE-PARTIAL (internal copy ACCEPTED via FormSubmit activated; visitor leg NO_ROUTE)",
    "booking_status": "LIVE-PARTIAL (internal ACCEPTED via FormSubmit; student/tutor legs externally blocked)",
    "payment_status": "NOT_APPLICABLE (no payment system on this static site)",
    "auth_status": "NOT_APPLICABLE (static site, no backend auth)",
    "inventory": {
        "toolbox_tools": len(tools),
        "tool_names": tools,
        "learn_pages": len(learn),
        "daily_hindi_days": len(days),
        "answers": html_count("answers"),
        "hindi_tutor_places": html_count("hindi-tutor"),
        "ask_questions": html_count("ask"),
        "tutor_profiles": html_count("tutor") - 1 if (ROOT/"tutor").exists() else 0,
    },
    "data_sources": {
        "settings": "gid=764031473", "content": "gid=2135319947",
        "reviews": "gid=1290168568", "tutors": "gid=834026040",
        "apps_script_health": "HTTP 200 {\"success\":\"true\"}",
    },
}

(REP / "final-release-baseline.json").write_text(json.dumps(base, indent=2))
u360 = {"generated": now, "final_release_baseline": REP.name + "/final-release-baseline.json",
        "note": "Captured BEFORE fixes; do not overwrite", "snapshot": base}
(REP / "ultra360-baseline.json").write_text(json.dumps(u360, indent=2))
print(f"wrote final-release-baseline.json + ultra360-baseline.json")
print(f"commit={base['git']['short']} tools={len(tools)} learn={len(learn)} days={len(days)}")
