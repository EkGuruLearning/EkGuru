#!/usr/bin/env python3
"""Phase 7C §9/§50 — content-graph engine + languages hub, real Chromium.

Gate C for the Phase 7C content graph:
  · /languages/ renders the hub (Phase 7 regression: >=20 cells, Available/Coming)
  · the page shows a LIVE content-inventory line read from data/content-graph.json
  · window.EkGuruContent query API works (byType/byLanguage/byLevel/byGoal/get/stats)
  · every count traces to real extracted content (no fabricated numbers)
  · no console/page errors

Output: reports/phase7c-graph-test.json
"""
import json, os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "http://127.0.0.1:8899"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
fails, facts = [], {}

def note(k, v):
    facts[k] = v

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    # ---- languages hub + live inventory ----
    pg.goto(BASE + "/languages/", wait_until="networkidle")
    pg.wait_for_timeout(1200)
    cells = pg.evaluate("() => document.querySelectorAll('.lang-cell').length")
    has_avail = pg.evaluate("() => document.body.innerText.includes('Available now') && document.body.innerText.includes('Hindi')")
    has_coming = pg.evaluate("() => document.body.innerText.includes('Coming soon')")
    note("hub.cells", cells)
    note("hub.available/coming", [has_avail, has_coming])
    if cells < 20 or not has_avail or not has_coming:
        fails.append("languages hub regression (%d cells)" % cells)

    stats_line = pg.evaluate("() => document.getElementById('cg-stats').innerText")
    note("hub.live_inventory", stats_line[:160])
    if "Live content inventory" not in stats_line:
        fails.append("live inventory line not rendered: %r" % stats_line[:80])

    # ---- content graph query API ----
    q = pg.evaluate("""async () => {
        await window.EkGuruContent.ready();
        const C = window.EkGuruContent;
        return {
            total: C.all().length,
            stats: C.stats(),
            lessons: C.byType('lesson').length,
            quizzes: C.byType('quiz').length,
            phrases: C.byType('phrase').length,
            review: C.byType('review_card').length,
            hi: C.byLanguage('hi').length,
            es: C.byLanguage('es').length,
            travel: C.byGoal('travel').length,
            beginner: C.byLevel('beginner').length,
            one: C.get('lesson:how-to-say-hello-in-hindi') ? C.get('lesson:how-to-say-hello-in-hindi').title : null,
        };
    }""")
    note("graph.query", q)
    if q["total"] < 300:
        fails.append("content graph too small: %d" % q["total"])
    if q["quizzes"] != 45:
        fails.append("expected 45 quizzes, got %d" % q["quizzes"])
    if q["review"] != 65:
        fails.append("expected 65 review cards, got %d" % q["review"])
    if q["phrases"] != 69:
        fails.append("expected 69 phrases, got %d" % q["phrases"])
    if q["hi"] == 0:
        fails.append("no Hindi entities")
    if q["es"] != 0:
        fails.append("Spanish should have 0 entities (no fabricated content), got %d" % q["es"])
    if not q["one"]:
        fails.append("get(lesson:how-to-say-hello-in-hindi) returned null")
    if q["travel"] == 0:
        fails.append("byGoal(travel) empty")

    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-graph-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("phase7c graph test:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-26s %s" % (k, json.dumps(v, ensure_ascii=False)[:150]))
for x in fails:
    print("  FAIL", x)
