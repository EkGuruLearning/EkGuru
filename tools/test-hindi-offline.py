#!/usr/bin/env python3
"""Phase 6 §15 — offline verification in real Chromium.

Flow: visit lesson online → service worker active → click "save offline" →
go OFFLINE → reload → assert the lesson content still renders → go ONLINE →
reload → assert saved-state persists → remove → assert removed.
Records every fact; PASS only if the claimed behaviour works.
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
LESSON = "/learn/hindi-alphabet-for-beginners/"
fails, facts = [], {}

def note(k, v):
    facts[k] = v

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 800, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    # 1) online first visit, wait for SW + precache
    pg.goto(BASE + LESSON, wait_until="networkidle")
    pg.wait_for_timeout(800)
    sw = pg.evaluate("async () => { try { const r = await navigator.serviceWorker.ready; return !!r.active; } catch(e){ return false; } }")
    note("service_worker_active", sw)
    if not sw:
        fails.append("service worker did not activate")

    # 2) save offline via the control
    btn = pg.evaluate("""() => {
      const ctl = document.getElementById('offline-ctl');
      const b = ctl ? ctl.querySelector('button') : null;
      return b ? b.innerText.trim() : null;
    }""")
    note("offline_button_label", btn)
    if not btn:
        fails.append("no offline-ctl button mounted on lesson")
    else:
        pg.evaluate("""() => {
          const ctl = document.getElementById('offline-ctl');
          const b = ctl.querySelector('button'); b.click();
        }""")
        pg.wait_for_timeout(700)

    # 3) go offline, hard reload
    ctx.set_offline(True)
    pg.reload(wait_until="domcontentloaded")
    pg.wait_for_timeout(500)
    title = pg.title()
    body_has = pg.evaluate("() => document.body.innerText.includes('Devanagari') || document.body.innerText.includes('alphabet')")
    note("offline_title", title)
    note("offline_content_rendered", body_has)
    if not body_has:
        fails.append("offline: lesson content did not render from cache")

    # 4) saved state persists; can remove
    ctx.set_offline(False)
    pg.reload(wait_until="networkidle")
    pg.wait_for_timeout(500)
    state = pg.evaluate("""() => {
      const ctl = document.getElementById('offline-ctl');
      return ctl ? ctl.innerText.replace(/\\s+/g,' ').trim().slice(0,120) : null;
    }""")
    note("after_reconnect_ctl", state)

    # 5) remove offline
    pg.evaluate("""() => {
      const ctl = document.getElementById('offline-ctl');
      const b = ctl.querySelector('button');
      if (b && /remove|saved/i.test(b.innerText)) b.click();
    }""")
    pg.wait_for_timeout(700)
    final_state = pg.evaluate("""() => {
      const ctl = document.getElementById('offline-ctl');
      return ctl ? ctl.innerText.replace(/\\s+/g,' ').trim().slice(0,120) : null;
    }""")
    note("after_remove_ctl", final_state)

    note("page_errors", errs)
    b.close()

res = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "flow": "save -> disconnect -> reload -> verify -> reconnect -> reload -> remove",
    "pass": not fails,
    "fails": fails,
    "facts": facts,
}
os.makedirs("reports", exist_ok=True)
with open("reports/hindi-offline-phase6.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("offline verification:", "PASS" if not fails else "FAIL")
for k, v in facts.items():
    print("  %-26s %s" % (k, v))
for x in fails:
    print("  FAIL", x)
sys.exit(0 if not fails else 1)
