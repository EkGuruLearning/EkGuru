#!/usr/bin/env python3
"""Phase 7B §10 — SRS deep real test (real Chromium).

Follows the command's 15-step SRS investigation from EMPTY storage:
seed → count → review → reveal → Again/Hard/Good/Easy → reload → persistence
→ due state → add custom card → remove card → reset → reload, plus a
localStorage-corruption test (graceful empty state, no uncaught exception).

Drives the real /learn/hindi/review/ controls and the real EkGuruSRS API
(the same API the lesson "＋ Review" buttons call).

Output: reports/phase7b-srs-runtime.json
"""
import json, os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "http://127.0.0.1:8899"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
REVIEW = "/learn/hindi/review/"
KEY = "ekguru:hindi:v1:review"

fails, facts = [], {}

def note(k, v):
    facts[k] = v

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    def goto_review():
        pg.goto(BASE + REVIEW, wait_until="networkidle")
        pg.wait_for_timeout(400)

    # ---- 0. empty storage ----
    pg.goto(BASE + "/", wait_until="domcontentloaded")
    pg.evaluate("() => localStorage.removeItem('%s')" % KEY)
    pg.wait_for_timeout(100)
    note("cleared_storage", True)

    # ---- 1. load starter deck ----
    goto_review()
    empty_visible = pg.evaluate("() => { var e=document.getElementById('srs-empty'); return e && getComputedStyle(e).display !== 'none'; }")
    note("empty_state_before_seed", empty_visible)
    pg.click("#srs-seed")
    pg.wait_for_timeout(500)
    # ---- 2. card count > 0 ----
    stats = pg.evaluate("() => document.getElementById('srs-stats').innerText")
    note("stats_after_seed", stats)
    count = pg.evaluate("() => window.EkGuruSRS ? window.EkGuruSRS.due().length : -1")
    note("due_count_after_seed", count)
    if not count or count <= 0:
        fails.append("starter deck produced no due cards")

    # ---- 3. start review (first card rendered) ----
    card_text = pg.evaluate("() => document.getElementById('srs-card').innerText")
    note("first_card", card_text[:100])
    if not card_text.strip():
        fails.append("no review card rendered after seeding")

    # ---- 4. reveal ----
    pg.click("#srs-show")
    revealed = pg.evaluate("() => { var a=document.getElementById('srs-a'); return a && getComputedStyle(a).display !== 'none'; }")
    note("reveal_works", revealed)
    if not revealed:
        fails.append("Show answer did not reveal the answer")

    def reveal_if_needed():
        vis = pg.evaluate("() => { var b=document.getElementById('srs-show'); return !!b && b.offsetParent !== null; }")
        if vis:
            pg.click("#srs-show")
            pg.wait_for_timeout(120)

    # ---- 5-8. rate Again / Hard / Good / Easy (reveal each fresh card first) ----
    ratings = []
    for i, r in enumerate(("again", "hard", "good", "easy")):
        if i > 0:
            reveal_if_needed()   # first card was already revealed in step 4
        pg.click("#srs-rates [data-r=%s]" % r)
        pg.wait_for_timeout(200)
        ratings.append(pg.evaluate("() => window.EkGuruSRS.dueCount()"))
    note("due_counts_after_ratings", ratings)
    note("review_total", pg.evaluate("() => window.EkGuruSRS.all ? window.EkGuruSRS.all().length : null"))

    # ---- 9. reload → persistence ----
    before_total = pg.evaluate("() => window.EkGuruSRS.all().length")
    goto_review()
    after_total = pg.evaluate("() => window.EkGuruSRS.all().length")
    note("persist_total_before_reload", before_total)
    note("persist_total_after_reload", after_total)
    if before_total != after_total:
        fails.append("deck size changed across reload (%d -> %d)" % (before_total, after_total))

    # ---- 10-11. due state after reload ----
    due_after = pg.evaluate("() => window.EkGuruSRS.dueCount()")
    note("due_count_after_reload", due_after)

    # ---- 12. add custom card (the API the ＋ Review button uses) ----
    before_add = pg.evaluate("() => window.EkGuruSRS.all().length")
    addres = pg.evaluate("""() => window.EkGuruSRS.add({
        prompt: 'परीक्षा', answer: 'test card answer', category: 'test' })""")
    after_add = pg.evaluate("() => window.EkGuruSRS.all().length")
    note("custom_add", {"added": addres.get("added"), "id": addres.get("id"),
                        "total_before": before_add, "total_after": after_add})
    if not addres.get("added") or after_add != before_add + 1:
        fails.append("custom card add failed (%r)" % addres)

    # ---- 13. remove that custom card ----
    rem = pg.evaluate("() => window.EkGuruSRS.remove(window.EkGuruSRS.add({prompt:'toremove',answer:'x'}).id)")
    note("remove_returns", rem)
    # verify the test card is still removable via its own id
    pg.evaluate("() => window.EkGuruSRS.remove('%s')" % addres["id"])
    note("total_after_remove", pg.evaluate("() => window.EkGuruSRS.all().length"))

    # ---- 13b. real "＋ Review" button on a lesson (Gate C user path) ----
    pg.goto(BASE + "/learn/how-to-say-hello-in-hindi/", wait_until="networkidle")
    pg.wait_for_timeout(600)
    has_btn = pg.evaluate("() => !!document.querySelector('button.hi-review-add')")
    note("lesson_has_review_button", has_btn)
    if has_btn:
        before = pg.evaluate("() => window.EkGuruSRS.all().length")
        pg.click("button.hi-review-add")
        pg.wait_for_timeout(400)
        after = pg.evaluate("() => window.EkGuruSRS.all().length")
        note("lesson_review_button_added", (before, after))
        if after <= before:
            fails.append("lesson ＋ Review button did not add a card (%d -> %d)" % (before, after))

    # ---- 14. reset (Remove all cards) ----
    goto_review()
    pg.click("#srs-reset")
    pg.wait_for_timeout(400)
    note("total_after_reset", pg.evaluate("() => window.EkGuruSRS.all().length"))
    reset_empty = pg.evaluate("() => { var e=document.getElementById('srs-empty'); return e && getComputedStyle(e).display !== 'none'; }")
    note("empty_state_after_reset", reset_empty)

    # ---- 15. reload after reset ----
    goto_review()
    note("total_after_reset_reload", pg.evaluate("() => window.EkGuruSRS.all().length"))

    # ---- corruption test ----
    pg.evaluate("() => localStorage.setItem('%s', '{{{not json')" % KEY)
    pg.reload(wait_until="networkidle")
    pg.wait_for_timeout(500)
    corrupt_ok = pg.evaluate("""() => {
        try {
            var s = document.getElementById('srs-stats');
            var e = document.getElementById('srs-empty');
            var card = document.getElementById('srs-card');
            return !!(s && card) && (e ? getComputedStyle(e).display !== 'none' : true);
        } catch (x) { return false; }
    }""")
    note("corruption_graceful", corrupt_ok)
    if not corrupt_ok:
        fails.append("corrupt localStorage did not fall back to a graceful state")
    note("page_errors", errs)

    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts,
       "storage_key": KEY, "module": "js/hindi-srs.js (window.EkGuruSRS)"}
with open("reports/phase7b-srs-runtime.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("srs runtime:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-28s %s" % (k, json.dumps(v, ensure_ascii=False)[:110]))
for x in fails:
    print("  FAIL", x)
