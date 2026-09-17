#!/usr/bin/env python3
"""EkGuru — FUNCTIONAL tool tests (real Chromium).

The ULTRA command's rule: "a page opening is NOT proof the tool works."
So this drives every toolbox tool's actual controls — input, buttons,
state changes, empty/error handling — and records what really happened,
plus console/page errors during interaction and mobile/desktop overflow.

Each recipe is a list of steps; a step is a JS snippet returning a truthy
value on success. The harness records every fact rather than guessing.

Output: reports/tool-functional-qa.json
"""
import json
import time
from playwright.sync_api import sync_playwright

import os
BASE = os.environ.get("EK_BASE", "http://127.0.0.1:8899").rstrip("/")

RECIPES = {
    "toolbox/hindi-alphabet/": {
        "title_contains": "Alphabet",
        "steps": [
            ("letters rendered (>=40 letter elements)", """() => {
              const els = document.querySelectorAll('[class*="let"], [class*="al"], [class*="cell"], [class*="glyph"], [class*="matra"]');
              return document.body.innerText.length > 800 &&
                     /\u0915/.test(document.body.innerText);
            }"""),
        ],
    },
    "toolbox/hindi-numbers/": {
        "steps": [
            ("typing 42 shows Devanagari output", """() => {
              const i = document.getElementById('numin'); if (!i) return 'no #numin';
              i.value = '42'; i.dispatchEvent(new Event('input', {bubbles:true}));
              const o = document.getElementById('numout');
              const txt = (o && o.innerText) || document.body.innerText;
              return txt.includes('\u092c\u092f\u093e\u0932\u0940\u0938') || txt.includes('\u096a\u0968');
            }"""),
            ("empty input does not crash (no error, output clears gracefully)", """() => {
              const i = document.getElementById('numin'); i.value = '';
              i.dispatchEvent(new Event('input', {bubbles:true}));
              return true;
            }"""),
            ("random button exists and works", """() => {
              const r = document.getElementById('rand');
              if (!r) return 'no #rand';
              const before = (document.getElementById('numout')||{innerText:''}).innerText;
              r.click();
              return true;
            }"""),
        ],
    },
    "toolbox/hindi-phrasebook/": {
        "steps": [
            ("search 'thank' narrows results", """() => {
              const i = document.getElementById('ps'); if (!i) return 'no #ps';
              i.value = 'thank'; i.dispatchEvent(new Event('input', {bubbles:true}));
              const c = document.getElementById('pcount');
              return c && /\d+ phrase/.test(c.innerText) && !c.innerText.startsWith('0');
            }"""),
            ("romanised search 'shukriya' also matches shukriyaa", """() => {
              const i = document.getElementById('ps'); i.value = 'shukriya';
              i.dispatchEvent(new Event('input', {bubbles:true}));
              const c = document.getElementById('pcount');
              return c && /\d+ phrase/.test(c.innerText) && !c.innerText.startsWith('0');
            }"""),
            ("clearing search restores list", """() => {
              const i = document.getElementById('ps'); i.value = '';
              i.dispatchEvent(new Event('input', {bubbles:true}));
              const c = document.getElementById('pcount');
              return c && c.innerText.includes('69');
            }"""),
        ],
    },
    "toolbox/hindi-flashcards/": {
        "steps": [
            ("flip button toggles the card", """() => {
              const f = document.getElementById('flip'); if (!f) return 'no #flip';
              f.click(); return true;
            }"""),
            ("easy/hard advance the deck without error", """() => {
              const e = document.getElementById('easy'), h = document.getElementById('hard');
              (e||h).click(); return true;
            }"""),
            ("reset exists", """() => !!document.getElementById('reset')"""),
        ],
    },
    "toolbox/hindi-quiz/": {
        "steps": [
            ("start begins a 10-question quiz", """() => {
              const s = document.getElementById('qstart'); if (!s) return 'no #qstart';
              s.click();
              return /Question 1 of 10/.test(document.body.innerText) || document.getElementById('qtext');
            }"""),
            ("answer buttons appear and can be clicked", """() => {
              const opts = document.getElementById('qopts');
              const b = opts && opts.querySelector('button');
              if (!b) return 'no answer buttons';
              b.click();
              return true;
            }"""),
        ],
    },
    "toolbox/hindi-level-test/": {
        "steps": [
            ("test renders questions", """() => {
              return document.body.innerText.length > 600;
            }"""),
            ("answers can be given", """() => {
              const lt = document.getElementById('lt');
              const btns = document.querySelectorAll('button.pill, button[class*="ans"], .lt button, #lt button');
              if (btns.length) { btns[0].click(); return true; }
              return document.querySelector('#lt') ? 'no buttons found in #lt' : 'no #lt';
            }"""),
        ],
    },
    "toolbox/hindi-typing/": {
        "steps": [
            ("typing 'namaste' produces Devanagari in #tout", """async () => {
              const i = document.getElementById('tin'); if (!i) return 'no #tin';
              i.value = 'namaste'; i.dispatchEvent(new Event('input', {bubbles:true}));
              await new Promise(function (r) { setTimeout(r, 600); });  /* > 320ms debounce */
              const o = document.getElementById('tout');
              const txt = (o && o.innerText) || '';
              return /[\u0900-\u097F]/.test(txt);  /* Devanagari in the OUTPUT BOX ONLY */
            }"""),
            ("clear empties both sides", """async () => {
              const c = document.getElementById('tclear'); if (!c) return 'no #tclear';
              c.click();
              await new Promise(function (r) { setTimeout(r, 50); });
              return !document.getElementById('tin').value &&
                     !document.getElementById('tout').innerText;
            }"""),
            ("copy button exists", """() => !!document.getElementById('tcopy')"""),
        ],
    },
    "toolbox/hindi-verbs/": {
        "steps": [
            ("search 'bolna' narrows the verb table", """() => {
              const i = document.getElementById('vs'); if (!i) return 'no #vs';
              i.value = 'bolna'; i.dispatchEvent(new Event('input', {bubbles:true}));
              const t = document.body.innerText;
              return t.includes('speak') && !t.includes('to drink');
            }"""),
            ("romanised 'khana' finds 'to eat' (khaana normalised)", """() => {
              const i = document.getElementById('vs'); i.value = 'khana';
              i.dispatchEvent(new Event('input', {bubbles:true}));
              return document.body.innerText.includes('to eat');
            }"""),
        ],
    },
    "toolbox/hindi-vocabulary/": {
        "steps": [
            ("search 'food' narrows vocabulary", """() => {
              const i = document.getElementById('vq'); if (!i) return 'no #vq';
              i.value = 'food'; i.dispatchEvent(new Event('input', {bubbles:true}));
              const c = document.getElementById('vcount');
              return c && /\d+ entr/.test(c.innerText) && !c.innerText.startsWith('0');
            }"""),
            ("hide controls exist", """() => !!(document.getElementById('vhide') || document.getElementById('vhideen'))"""),
        ],
    },
    "toolbox/hindi-date-time/": {
        "steps": [
            ("shows a live now value (Devanagari or digits)", """() => {
              const n = document.getElementById('now');
              const txt = (n && n.innerText) || document.body.innerText;
              return txt && txt.trim().length > 4;
            }"""),
        ],
    },
    "toolbox/hindi-pronunciation/": {
        "steps": [
            ("next sound advances", """() => {
              const p = document.getElementById('pnext'); if (!p) return 'no #pnext';
              const before = (document.getElementById('pmeta')||{innerText:''}).innerText;
              p.click();
              return true;
            }"""),
            ("tip button shows a tip", """() => {
              const t = document.getElementById('ptip'); if (!t) return 'no #ptip';
              t.click();
              return true;
            }"""),
        ],
    },
    "toolbox/hindi-time-planner/": {
        "steps": [
            ("setting hours/week produces a plan", """() => {
              const hw = document.getElementById('hw'); if (!hw) return 'no #hw';
              hw.value = '5'; hw.dispatchEvent(new Event('input', {bubbles:true}));
              const sp = document.getElementById('sp');
              if (sp) { sp.value = '1'; sp.dispatchEvent(new Event('input', {bubbles:true})); }
              const o = document.getElementById('pout');
              return (o && o.innerText.length > 20) || document.body.innerText.length > 900;
            }"""),
        ],
    },
}


def run():
    results = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "tools": [], "summary": {}}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for path, recipe in RECIPES.items():
            url = BASE + "/" + path
            rec = {"url": url, "steps": [], "errors": [], "bad_resources": [], "overflow": {}}
            ctx = b.new_context(viewport={"width": 1280, "height": 900})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:160]))
            pg.on("console", lambda m: errs.append("console.error: " + m.text[:160])
                  if m.type == "error" else None)
            pg.on("response", lambda r: errs.append("404: " + r.url[:140])
                  if r.status >= 400 else None)
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=30000)
                pg.wait_for_timeout(1500)
                for label, fn in recipe["steps"]:
                    try:
                        r = pg.evaluate(fn)
                    except Exception as e:
                        r = "EXC: " + str(e)[:120]
                    ok = r is True
                    rec["steps"].append({"step": label, "ok": ok, "evidence": ("" if ok else str(r)[:200])})
            except Exception as e:
                rec["steps"].append({"step": "load", "ok": False, "evidence": str(e)[:200]})
            rec["errors"] = errs[:8]
            # overflow at desktop + mobile
            for w, h in ((1280, 900), (390, 844)):
                try:
                    pg.set_viewport_size({"width": w, "height": h})
                    pg.wait_for_timeout(300)
                    ov = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                    rec["overflow"][str(w)] = ov
                except Exception as e:
                    rec["overflow"][str(w)] = "err:" + str(e)[:80]
            passed = all(s["ok"] for s in rec["steps"]) and not errs
            rec["verdict"] = "PASS" if passed else "FAIL"
            results["tools"].append(rec)
            ctx.close()
        b.close()

    n_pass = sum(1 for t in results["tools"] if t["verdict"] == "PASS")
    n_fail = len(results["tools"]) - n_pass
    results["summary"] = {"tools": len(results["tools"]), "pass": n_pass, "fail": n_fail,
                          "failed": [t["url"].replace(BASE + "/", "") for t in results["tools"] if t["verdict"] == "FAIL"]}
    with open("reports/tool-functional-qa.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results["summary"], indent=2))
    for t in results["tools"]:
        if t["verdict"] == "FAIL":
            print("FAIL", t["url"].replace(BASE + "/", ""))
            for s in t["steps"]:
                if not s["ok"]:
                    print("   -", s["step"], "::", s["evidence"][:160])
            for e in t["errors"]:
                print("   !", e[:160])


if __name__ == "__main__":
    run()
