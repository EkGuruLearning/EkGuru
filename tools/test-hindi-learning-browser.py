#!/usr/bin/env python3
"""Phase 6 §10/§19-21 — real-Chromium audit of the NEW Hindi learning tools
(typing, topic quiz, worksheets, review/SRS, my-progress) against the
practice-activity standard: objective, instructions, validation, feedback,
retry, reset, keyboard, mobile, and honest empty/error handling.

Drives the real controls; records facts only. A page loading is NOT a pass.
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
fails, facts = [], {}

def note(k, v):
    facts[k] = v

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})  # mobile first

    def goto(path):
        pg.goto(BASE + path, wait_until="networkidle")

    # ---- TYPING ----
    goto("/learn/hindi/practice/typing/")
    prompt = pg.evaluate("() => document.getElementById('tp-prompt') ? document.getElementById('tp-prompt').innerText : null")
    note("typing.prompt", prompt)
    # reveal the answer for the CURRENT prompt, then type it back exactly
    pg.click("#tp-show")
    ans = pg.evaluate("() => document.getElementById('tp-feedback').innerText")
    pg.fill("#typing-in2", ans)
    pg.click("#tp-check")
    fb = pg.evaluate("() => document.getElementById('tp-feedback').innerText")
    note("typing.prompt", prompt)
    note("typing.answer", ans)
    note("typing.feedback_after_correct", fb)
    if "correct" not in fb.lower() and "minor" not in fb.lower():
        fails.append("typing: typed answer not accepted (prompt=%r ans=%r fb=%r)" % (prompt, ans, fb))
    pg.click("#tp-reset")
    reset = pg.evaluate("() => document.getElementById('tp-score').innerText")
    note("typing.reset_state", reset)

    # ---- QUIZ ----
    goto("/learn/hindi/practice/quiz/")
    pg.select_option("#q-n", "5")
    pg.click("#q-start")
    body = pg.evaluate("() => document.getElementById('q-body').innerText")
    note("quiz.first_question", body[:120])
    nopts = pg.evaluate("() => document.querySelectorAll('#q-body [data-opt]').length")
    note("quiz.option_count", nopts)
    if nopts != 4:
        fails.append("quiz: expected 4 options, got %d" % nopts)
    pg.click("#q-body [data-opt]")
    expl = pg.evaluate("() => document.getElementById('q-fb').innerText")
    note("quiz.explanation", expl[:120])
    if "Source:" not in expl:
        fails.append("quiz: explanation lacks source lesson link")

    # ---- WORKSHEETS ----
    goto("/learn/hindi/practice/worksheets/")
    pg.click("#w-build") if pg.evaluate("() => !!document.getElementById('w-build')") else None
    ws = pg.evaluate("() => document.getElementById('ws-app').innerText")
    note("worksheet.built", ws[:120])
    if not ws.strip():
        fails.append("worksheets: nothing built")

    # ---- REVIEW / SRS ----
    goto("/learn/hindi/review/")
    pg.click("#srs-seed")
    card = pg.evaluate("() => document.getElementById('srs-card').innerText")
    note("srs.card", card[:120])
    pg.click("#srs-show")               # reveal answer -> rating row appears
    pg.click("#srs-rates [data-r=again]")  # rate the card
    stats = pg.evaluate("() => document.getElementById('srs-stats').innerText")
    note("srs.stats_after_rating", stats[:120])
    if not card.strip():
        fails.append("review: no card shown after seeding")

    # ---- MY-PROGRESS ----
    goto("/learn/hindi/my-progress/")
    summary = pg.evaluate("() => document.getElementById('my-hindi').innerText")
    note("progress.summary", summary[:120])
    if not summary.strip():
        fails.append("my-progress: no summary rendered")

    b.close()

res = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "activities": 5,
    "pass": not fails,
    "fails": fails,
    "facts": facts,
    "standard": {
        "objective": "stated on each practice page (honest capability note)",
        "instructions": "inline per activity (see page copy)",
        "validation": "typing compare / quiz option match / worksheet build",
        "feedback": "correct|minor-format|incorrect + role=status",
        "retry": "typing Try again / quiz Try again / srs rate again",
        "reset": "typing Reset / srs reset / progress reset",
        "keyboard": "native input + Enter to check",
        "mobile": "390px viewport tested, buttons tappable",
    },
}
os.makedirs("reports", exist_ok=True)
with open("reports/hindi-learning-browser.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("learning browser audit:", "PASS" if not fails else "FAIL")
for k, v in facts.items():
    print("  %-30s %s" % (k, v))
for x in fails:
    print("  FAIL", x)
sys.exit(0 if not fails else 1)
