#!/usr/bin/env python3
"""Phase 7C Stage 6 — everyday polish + honest tooling (Gate M).

Verifies, in real Chromium:
  · global-nav rename: "More on EkGuru" block is now "Learn languages"
    (heading + aria-label) on the home page and one inner page
  · voice everywhere: the languages hub shows a Listen button (computer
    voice, correct BCP-47 tag) for every language cell; the SRS review
    card and the vocabulary practice lab show a Listen button for the
    Devanagari word
  · daily rotation: practice dayShuffle is deterministic per date+salt
    (rule-based, not AI) and changes across dates
Output: reports/phase7c-stage6-test.json
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

STUB = """
window.__spoken = [];
try {
  Object.defineProperty(window, 'speechSynthesis', {
    configurable: true,
    value: {
      speak: function(u){ window.__spoken.push({text: u.text, lang: u.lang}); },
      cancel: function(){}, getVoices: function(){ return [{lang:'hi-IN',name:'hi'},{lang:'ar-SA',name:'ar'},{lang:'zh-CN',name:'zh'}]; },
      addEventListener: function(){}, removeEventListener: function(){}
    }
  });
} catch(e) { window.__defineErr = e.message; }
window.SpeechSynthesisUtterance = function(t){ this.text = t; this.lang = ''; };
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    ctx.add_init_script(STUB)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    def wait(sel, n=60):
        for _ in range(n):
            if pg.evaluate("() => document.querySelectorAll('%s').length > 0" % sel):
                return True
            pg.wait_for_timeout(250)
        return False

    # ---- 1) global-nav rename (home + one inner page) ----
    for url in ("/", "/answers/"):
        pg.goto(BASE + url, wait_until="networkidle")
        nav = pg.evaluate("""() => {
            var n = document.querySelector('.eg-globalnav');
            if (!n) return null;
            return { aria: n.getAttribute('aria-label'),
                     heading: (n.querySelector('.eg-gn-h') || {}).textContent || null };
        }""")
        note("nav:" + url, nav)
        if not nav or nav["aria"] != "Learn languages" or nav["heading"] != "Learn languages":
            fails.append("%s global-nav not renamed: %r" % (url, nav))

    # ---- 2) languages hub: every cell has a Listen button ----
    pg.goto(BASE + "/languages/", wait_until="networkidle")
    wait(".lang-cell")
    pg.wait_for_timeout(800)
    hub = pg.evaluate("""() => {
        var cells = document.querySelectorAll('.lang-grid .lang-cell');
        var withSay = 0, listens = 0, tags = {};
        cells.forEach(function (c) {
            var s = c.querySelector('[data-say]');
            if (s) { withSay++; tags[s.getAttribute('data-say-lang')] = s.getAttribute('data-say'); }
        });
        return { cells: cells.length, withSay: withSay,
                 listens: document.querySelectorAll('.lang-grid .hi-listen').length,
                 arTag: (document.querySelector('.lang-grid [data-say-lang="ar-SA"]') || {}).getAttribute ? true : false };
    }""")
    note("hub_listen", hub)
    if hub["cells"] != 30:
        fails.append("hub should have 30 cells, got %d" % hub["cells"])
    if hub["withSay"] != 30:
        fails.append("hub should have 30 [data-say] cells, got %d" % hub["withSay"])
    if hub["listens"] != 30:
        fails.append("hub should mount 30 listen buttons, got %d" % hub["listens"])

    # click the Arabic listen button -> ar-SA utterance of العربية
    pg.click('.lang-grid .lang-cell.lb [data-say-lang="ar-SA"] .hi-listen')
    pg.wait_for_timeout(300)
    spoken = pg.evaluate("() => window.__spoken")
    ar = spoken[-1] if spoken else None
    note("hub_ar_spoken", ar)
    if not ar or ar.get("lang") != "ar-SA" or ar.get("text") != "العربية":
        fails.append("hub ar listen: expected ar-SA 'العربية', got %r" % ar)

    # ---- 3) SRS review: Listen button on a card that has a Devanagari word ----
    pg.goto(BASE + "/learn/hindi/review/", wait_until="networkidle")
    pg.wait_for_timeout(800)
    pg.evaluate("() => { var b = document.getElementById('srs-seed'); if (b) b.click(); }")
    pg.wait_for_timeout(500)
    srs = pg.evaluate("""() => {
        var seen = 0, hasSay = false, deva = /[\\u0900-\\u097F]/;
        while (seen < 60) {
            var c = document.getElementById('srs-card');
            var t = (c && c.innerText) || '';
            if (deva.test(t) && document.querySelector('#srs-card #srs-say')) { hasSay = true; break; }
            var g = document.querySelector('#srs-card [data-r="good"]');
            if (!g) {
                var show = document.querySelector('#srs-card #srs-show');
                if (show) { show.click(); continue; }
                break;
            }
            g.click(); seen++;
        }
        return { hasSay: hasSay, seen: seen };
    }""")
    note("srs_review", srs)
    if not srs["hasSay"]:
        fails.append("srs review card: no Listen button on any card with Devanagari")

    # ---- 4) vocabulary practice lab: Listen button for Devanagari ----
    pg.goto(BASE + "/learn/practice/vocabulary/", wait_until="networkidle")
    pg.wait_for_timeout(1000)
    prac = pg.evaluate("""() => {
        var t = document.body.innerText;
        return { hasListen: !!document.querySelector('.px-play'),
                 hasNote: t.indexOf('computer voice') >= 0 };
    }""")
    note("practice_listen", prac)
    if not prac["hasListen"]:
        fails.append("vocabulary practice: no Listen button on the drill")

    # ---- 5) daily rotation determinism (rule-based, not AI) ----
    pg.goto(BASE + "/learn/practice/daily/", wait_until="networkidle")
    pg.wait_for_timeout(1000)
    pg.evaluate("() => { var b = document.querySelector('#daily-pick [data-n]'); if (b) b.click(); }")
    pg.wait_for_timeout(600)
    rot = pg.evaluate("""() => {
        var P = window.EkGuruPractice;
        if (!P || !P.dayShuffle) return { ok: false, why: 'no hook' };
        var a = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14];
        var d1 = new Date('2026-09-13T00:00:00Z');
        var d2 = new Date('2026-09-14T00:00:00Z');
        var same1 = P.dayShuffle(a, 'daily:10', d1).join(',');
        var same2 = P.dayShuffle(a, 'daily:10', d1).join(',');
        var other = P.dayShuffle(a, 'daily:10', d2).join(',');
        return { ok: true, deterministic: same1 === same2, rotated: same1 !== other,
                 note: (document.body.innerText.indexOf('rotates each day') >= 0) };
    }""")
    note("daily_rotation", rot)
    if not rot.get("ok"):
        fails.append("daily rotation: hook missing: %r" % rot)
    else:
        if not rot["deterministic"]:
            fails.append("daily rotation: not deterministic for same date")
        if not rot["rotated"]:
            fails.append("daily rotation: set did not change across dates")

    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-stage6-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("stage6 everyday polish + honest tooling:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-22s %s" % (k, json.dumps(v, ensure_ascii=False)[:120]))
for x in fails:
    print("  FAIL", x)
