#!/usr/bin/env python3
"""Phase 7C tranche 2 — reusable engines + global My Learning, real Chromium (Gate D).

Verifies on /learn/my-learning/ (mobile viewport, 0 page errors):
  · goals engine     -> 11 goals with honest availability (available/partial/planned)
  · script engine    -> 9 scripts, only latn+deva PRODUCTION, rtl direction correct
  · grammar engine   -> 6 authored concepts rendered
  · vocab engine     -> 24 authored words rendered
  · progress dash    -> device-only counters (zeroes on clean profile)
  · offline box      -> honest empty state
  · language-aware search:
        "paani" (roman)   finds पानी
        "water" (english) finds पानी
        "पानी" (devanagari) finds पानी
        "past tense"      finds a grammar/lesson result
  · deterministic honesty strings present
Output: reports/phase7c-engines-test.json
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

    pg.goto(BASE + "/learn/my-learning/", wait_until="networkidle")
    # wait for engines to mount
    for _ in range(40):
        if pg.evaluate("() => document.querySelectorAll('#goals-app .goal').length > 0 && document.querySelectorAll('#grammar-app .g-concept').length > 0"):
            break
        pg.wait_for_timeout(250)
    pg.wait_for_timeout(1000)

    goals = pg.evaluate("() => Array.from(document.querySelectorAll('#goals-app .goal')).map(g => g.querySelector('.goal-name').innerText + '|' + g.querySelector('.goal-status').innerText)")
    note("goals", goals)
    if len(goals) != 11:
        fails.append("expected 11 goals, got %d" % len(goals))
    if not any("production" in g for g in goals):
        fails.append("no goal reported production (available)")

    scripts = pg.evaluate("() => Array.from(document.querySelectorAll('#script-app .scr')).map(s => s.innerText)")
    note("script_count", len(scripts))
    if len(scripts) != 9:
        fails.append("expected 9 scripts, got %d" % len(scripts))
    prod = [s for s in scripts if "production" in s]
    if len(prod) != 2:
        fails.append("expected exactly 2 PRODUCTION scripts, got %d" % len(prod))
    if not any("rtl" in s for s in scripts):
        fails.append("no rtl direction reported in script registry")

    gram = pg.evaluate("() => document.querySelectorAll('#grammar-app .g-concept').length")
    note("grammar_concepts", gram)
    if gram != 6:
        fails.append("expected 6 grammar concepts, got %d" % gram)

    vocab = pg.evaluate("() => document.querySelectorAll('#vocab-app .v-item').length")
    note("vocab_words", vocab)
    if vocab != 24:
        fails.append("expected 24 vocab words, got %d" % vocab)

    dash = pg.evaluate("() => document.getElementById('progress-dash').innerText")
    note("progress_dash", dash.replace("\n", " / ")[:140])
    if "lessons" not in dash.lower():
        fails.append("progress dashboard did not render")

    offline = pg.evaluate("() => document.getElementById('offline-app').innerText")
    note("offline_state", offline[:80])
    if "not saved" not in offline and "did not load" not in offline:
        fails.append("offline box missing honest empty state")

    body = pg.evaluate("() => document.body.innerText")
    if "Saved on this device" not in body and "saved on this device" not in body.lower():
        fails.append("device-only honesty string missing")
    if "noindex" not in pg.evaluate("() => document.querySelector('meta[name=robots]').content"):
        fails.append("my-learning must be noindex")

    # ---- language-aware search ----
    def search(q, wait=900):
        pg.fill("#learn-q", q)
        pg.wait_for_timeout(wait)
        return pg.evaluate("() => document.getElementById('learn-res').innerText")

    r1 = search("paani")
    note("search_paani", r1[:120].replace("\n", " | "))
    if "पानी" not in r1:
        fails.append("roman query 'paani' did not surface पानी")

    r2 = search("water")
    note("search_water", r2[:120].replace("\n", " | "))
    if "पानी" not in r2:
        fails.append("english query 'water' did not surface पानी")

    r3 = search("पानी")
    note("search_devanagari", r3[:120].replace("\n", " | "))
    if "पानी" not in r3:
        fails.append("devanagari query 'पानी' did not surface पानी")

    r4 = search("past tense")
    note("search_past_tense", r4[:120].replace("\n", " | "))
    if "पानी" in r4:
        pass
    if not r4 or "No matches" in r4:
        fails.append("query 'past tense' returned no results")

    # ---- family mode (privacy-safe child/family toggle) ----
    fam_btn = pg.evaluate("() => !!document.querySelector('#family-app button')")
    note("family_button_present", fam_btn)
    if not fam_btn:
        fails.append("family mode toggle did not mount")
    else:
        pg.click("#family-app button")
        pg.wait_for_timeout(300)
        pressed = pg.evaluate("() => document.querySelector('#family-app button').getAttribute('aria-pressed')")
        noTrack = pg.evaluate("() => localStorage.getItem('ekguru_no_track')")
        note("family_mode_on", {"pressed": pressed, "no_track": noTrack})
        if pressed != "true" or noTrack != "1":
            fails.append("family mode did not opt out of tracking")
        pg.click("#family-app button")  # back off
        pg.wait_for_timeout(200)

    # ---- SRS card model is language-agnostic (§31) ----
    card = pg.evaluate("() => { var r = window.EkGuruSRS.add({prompt:'पानी', answer:'water', language:'hi', target:'पानी', source:'en', category:'vocabulary', level:'beginner'}); return r.card; }")
    note("srs_card_language", card.get("language") if isinstance(card, dict) else card)
    if not isinstance(card, dict) or card.get("language") != "hi":
        fails.append("SRS card missing language field")
    if card.get("target") != "पानी":
        fails.append("SRS card missing target field")

    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-engines-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("engines + My Learning:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-22s %s" % (k, json.dumps(v, ensure_ascii=False)[:150]))
for x in fails:
    print("  FAIL", x)
