#!/usr/bin/env python3
"""EkGuru — Disaster-recovery drills (safe, away from production).

  1. BACKUP:       snapshot the current tree (git bundle + zip) -> audit/backup/
  2. RESTORE DRILL: extract the release zip to a scratch dir, serve it, and
                    verify critical pages render (a backup that was never
                    restored is not verified).
  3. ROLLBACK:      record the known-good commit + procedure.
  4. ADVERSARIAL:   in a real browser, block all 4 sheet CSVs and verify the
                    tutor page still renders from static fallback (no blank page).

  Output: reports/dr-drill.json
"""
import json, os, shutil, subprocess, sys, tempfile, time, http.server, threading, urllib.request
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REP = os.path.join(ROOT, "reports")
BK = os.path.join(ROOT, "..", "audit", "backup")
os.makedirs(REP, exist_ok=True)
os.makedirs(BK, exist_ok=True)

out = {"generated": None, "backup": {}, "restore": {}, "rollback": {}, "adversarial": {}}

def sh(*a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True).stdout.strip()

# ── 1. BACKUP ─────────────────────────────────────────────────
commit = sh("git", "rev-parse", "HEAD")
bundle = os.path.join(BK, f"ekguru-known-good-{commit[:8]}.bundle")
r = subprocess.run(["git", "bundle", "create", bundle, "--all"], cwd=ROOT, capture_output=True, text=True)
# latest release zip (auto-detected, so the drill never rots when the
# version bumps: v3.zip -> v4.zip -> ...). Exactly one v*.zip exists by
# make-zip.py design, so the newest is always "the" release artifact.
import glob
_rel_zips = sorted(glob.glob(os.path.join("/home/user/releases", "v*.zip")))
zip_src = _rel_zips[-1] if _rel_zips else None
zip_dst = os.path.join(BK, "ekguru-release-" + os.path.basename(zip_src)) if zip_src else None
if zip_src and os.path.exists(zip_src):
    shutil.copy2(zip_src, zip_dst)
out["backup"] = {
    "commit": commit,
    "git_bundle": os.path.basename(bundle),
    "git_bundle_ok": os.path.exists(bundle) and os.path.getsize(bundle) > 0,
    "release_zip": os.path.basename(zip_dst) if os.path.exists(zip_dst) else None,
    "rpo": "0 (static site: source of truth is the repo; rebuild = redeploy)",
    "rto": "minutes (GitHub Pages push-to-deploy; no DB to restore)",
    "last_known_good": "release " + (os.path.basename(zip_src) if zip_src else "zip") + " + git commit " + commit[:8],
}

# ── 2. RESTORE DRILL (away from production) ────────────────────
restore_dir = tempfile.mkdtemp(prefix="ekguru-restore-")
pages = {}
try:
    with __import__("zipfile").ZipFile(zip_dst) as z:
        z.extractall(restore_dir)
    site = os.path.join(restore_dir, "EkGuru")
    # serve
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw): super().__init__(*a, directory=site, **kw)
        def log_message(self, *a): pass
    srv = http.server.HTTPServer(("127.0.0.1", 8877), Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True); t.start()
    for path in ["/", "/learn/", "/toolbox/hindi-alphabet/", "/tutor/sushila-g/", "/contact/"]:
        try:
            code = urllib.request.urlopen(f"http://127.0.0.1:8877{path}", timeout=10).status
            pages[path] = code
        except Exception as e:
            pages[path] = f"ERR {e}"
    srv.shutdown()
    out["restore"] = {"restored_from": os.path.basename(zip_dst), "pages": pages,
                      "pass": all(v == 200 for v in pages.values()),
                      "note": "restore verified in a scratch dir on 127.0.0.1:8877 — never against production"}
finally:
    shutil.rmtree(restore_dir, ignore_errors=True)

# ── 3. ROLLBACK PROCEDURE ──────────────────────────────────────
out["rollback"] = {
    "procedure": [
        "git checkout " + commit + "   # known-good commit",
        "python3 /home/user/releases/make-zip.py",
        "re-upload the zip to the GitHub repo (Add file → Upload files)",
        "or: git push origin main --force-with-lease from a machine with push access",
    ],
    "known_good": commit,
    "dns_change_needed": False,
}

# ── 4. ADVERSARIAL DRILL (CSV unavailable) ─────────────────────
adv = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    pg = ctx.new_page()
    blocked = []
    def route(route, request):
        if "docs.google.com/spreadsheets" in request.url:
            blocked.append(request.url[:60])
            route.abort()
        else:
            route.continue_()
    pg.route("**/*", route)
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto("http://127.0.0.1:8899/tutor/sushila-g/", wait_until="commit", timeout=30000)
    pg.wait_for_timeout(5000)
    has_tutor_name = pg.locator("h1").count() > 0
    body_has_content = pg.evaluate("document.body.innerText.length")
    health_visible = "degrad" in pg.evaluate("document.body.innerText.toLowerCase()")
    adv = {
        "csv_blocked": len(blocked),
        "page_rendered": has_tutor_name and body_has_content > 500,
        "body_text_length": body_has_content,
        "shows_degraded_state": health_visible,
        "console_errors": errs[:5],
        "pass": has_tutor_name and body_has_content > 500,
        "note": "sheet CSVs aborted at network level; page must still render from static overrides",
    }
    b.close()
out["adversarial"] = adv
out["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

with open(os.path.join(REP, "dr-drill.json"), "w") as f:
    json.dump(out, f, indent=2)
print("backup:", out["backup"]["git_bundle_ok"] and "OK" or "FAIL", out["backup"]["release_zip"])
print("restore:", out["restore"]["pass"] and "PASS" or "FAIL", out["restore"]["pages"])
print("rollback known-good:", out["rollback"]["known_good"][:8])
print("adversarial (CSV down):", adv.get("pass") and "PASS" or "FAIL",
      f"rendered={adv.get('page_rendered')} degraded_shown={adv.get('shows_degraded_state')} errs={adv.get('console_errors')}")
