#!/usr/bin/env python3
"""Phase 7C §21 — deterministic conversation engine, real Chromium (Gate C).

Verifies the scenario simulator end-to-end:
  · /learn/hindi/practice/conversation/ lists all 6 scenarios
  · labelled DETERMINISTIC (rule-based, not AI)
  · mounting a scenario shows the NPC line + 2 choices
  · picking the correct reply shows feedback + vocabulary
  · "Next line" advances the state machine
  · wrong reply shows the correction note
  · a full scenario reaches "Scenario complete"
  · no console/page errors; mobile viewport
Output: reports/phase7c-conversation-test.json
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

    pg.goto(BASE + "/learn/hindi/practice/conversation/", wait_until="networkidle")
    pg.wait_for_timeout(1500)

    n = pg.evaluate("() => document.querySelectorAll('#conv-app [data-sc]').length")
    note("scenario_count", n)
    if n != 6:
        fails.append("expected 6 scenarios, got %d" % n)

    labels = pg.evaluate("() => Array.from(document.querySelectorAll('#conv-app [data-sc]')).map(b => b.querySelector('span').innerText)")
    note("scenario_labels", labels)
    if "deterministic" not in pg.evaluate("() => document.body.innerText.toLowerCase()"):
        fails.append("deterministic labelling missing from page copy")

    pg.click('#conv-app [data-sc="introduction"]')
    pg.wait_for_timeout(500)
    npc = pg.evaluate("() => { var t=document.querySelector('#conv-stage .conv-npc-tag'); return t ? t.innerText : 'NONE'; }")
    note("npc_line", npc)
    tag = pg.evaluate("() => { var t=document.querySelector('#conv-stage .conv-tag'); return t ? t.innerText : 'NONE'; }")
    note("stage_deterministic_tag", tag)
    if tag != "Deterministic practice — rule-based, not AI":
        fails.append("deterministic tag missing in stage: %r" % tag)
    choices = pg.evaluate("() => document.querySelectorAll('#conv-stage .conv-choice').length")
    note("choices_step1", choices)
    if choices != 2:
        fails.append("expected 2 choices, got %d" % choices)

    # wrong reply first (second choice) → retry → correct (first)
    pg.click("#conv-stage .conv-choice >> nth=1")
    pg.wait_for_timeout(250)
    fb = pg.evaluate("() => document.querySelector('#conv-stage').innerText")
    note("wrong_feedback", fb[:100])
    if "Not quite" not in fb:
        fails.append("wrong reply did not show correction")
    pg.click("#conv-stage .conv-retry")
    pg.wait_for_timeout(250)
    pg.click("#conv-stage .conv-choice >> nth=0")
    pg.wait_for_timeout(250)
    fb2 = pg.evaluate("() => document.querySelector('#conv-stage').innerText")
    note("correct_feedback_has_vocab", "theek" in fb2)
    if "Correct" not in fb2:
        fails.append("correct reply not acknowledged")
    if "theek" not in fb2:
        fails.append("vocabulary not shown after correct reply")

    # advance through remaining steps to completion
    for _ in range(2):
        if pg.evaluate("() => !!document.querySelector('#conv-stage .conv-next')"):
            pg.click("#conv-stage .conv-next")
            pg.wait_for_timeout(250)
        pg.click("#conv-stage .conv-choice >> nth=0")
        pg.wait_for_timeout(250)
    done = pg.evaluate("() => document.querySelector('#conv-stage').innerText")
    note("completed", "Scenario complete" in done)
    if "Scenario complete" not in done:
        fails.append("scenario did not reach completion")

    # restart returns to step 1
    if pg.evaluate("() => !!document.querySelector('#conv-stage .conv-restart')"):
        pg.click("#conv-stage .conv-restart")
        pg.wait_for_timeout(250)
        again = pg.evaluate("() => document.querySelectorAll('#conv-stage .conv-choice').length")
        note("restart_shows_choices", again)
        if again != 2:
            fails.append("restart did not reset to step 1 (choices=%d)" % again)

    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-conversation-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("conversation engine:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-28s %s" % (k, json.dumps(v, ensure_ascii=False)[:120]))
for x in fails:
    print("  FAIL", x)
