#!/usr/bin/env python3
"""Phase 7C Stage 4 — starter-pack learning experience, real Chromium (Gate K).

Verifies the BETA starter packs are genuinely usable, honestly:
  · browser-TTS "Listen" buttons on every pack card (computer voice, never
    called native/recorded), utterance language = the pack's BCP-47 tag
  · a deterministic rule-based "Starter check" (8 fixed questions, not AI,
    nothing saved) that a learner can complete end-to-end
  · Hindi PRODUCTION flow is UNCHANGED (no listen buttons injected there)
  · 0 page errors
Output: reports/phase7c-starter-test.json
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

# ---- manifest/registry assertions (Python-side) ----
manifest = json.load(open("data/language-packs.json", encoding="utf-8"))
packs = {p["lang"]: p for p in manifest["packs"]}
note("pack_speechTags", {c: packs[c]["speechTag"] for c in sorted(packs)})
if sorted(packs) != sorted(["en", "es", "bn", "ta", "te", "mr", "gu", "pa", "ur",
                            "fr", "ar", "de", "ja", "ko", "zh", "ru", "pt", "it", "nl", "pl",
                            "tr", "fa", "he", "th", "vi", "id", "ms", "sw", "uk"]):
    fails.append("manifest should have 29 packs")
if packs["ar"]["speechTag"] != "ar-SA" or packs["fa"]["speechTag"] != "fa-IR" \
   or packs["he"]["speechTag"] != "he-IL" or packs["ms"]["speechTag"] != "ms-MY":
    fails.append("RTL/extra speech tags wrong: %s" % {c: packs[c]["speechTag"] for c in ("ar", "fa", "he", "ms")})

STUB = """
window.__spoken = [];
try {
  Object.defineProperty(window, 'speechSynthesis', {
    configurable: true,
    value: {
      speak: function(u){ window.__spoken.push({text: u.text, lang: u.lang}); },
      cancel: function(){}, getVoices: function(){ return [{lang:'es-ES',name:'es'},{lang:'bn-IN',name:'bn'},{lang:'ar-SA',name:'ar'},{lang:'zh-CN',name:'zh'}]; },
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

    # ---- Spanish detail page ----
    pg.goto(BASE + "/languages/es/", wait_until="networkidle")
    wait("#langpack-app .v-item")
    pg.wait_for_timeout(800)
    es = pg.evaluate("""() => {
        var t = document.body.innerText;
        return {
            listen: document.querySelectorAll('#langpack-app .hi-listen').length,
            say: document.querySelectorAll('#langpack-app [data-say]').length,
            computerVoice: t.indexOf('computer voice') >= 0,
            checkLabel: t.indexOf('Not an exam') >= 0 || t.indexOf('not an exam') >= 0,
            questions: document.querySelectorAll('#starter-check .sc-q').length
        };
    }""")
    note("es_detail", es)
    if es["listen"] != 36 or es["say"] != 36:
        fails.append("es detail: expected 36 listen buttons, got %r" % (es["listen"], es["say"]))
    if not es["computerVoice"]:
        fails.append("es detail: missing honest 'computer voice' label")
    if not es["checkLabel"]:
        fails.append("es detail: missing 'not an exam' honesty")
    if es["questions"] != 1:
        fails.append("es detail: starter check should show 1 question at a time")

    # click a Listen button -> utterance language es-ES
    pg.click("#langpack-app .hi-listen >> nth=0")
    pg.wait_for_timeout(300)
    spoken = pg.evaluate("() => window.__spoken")
    note("es_spoken", spoken[:1])
    if not spoken or spoken[0].get("lang") != "es-ES" or spoken[0].get("text") != "hola":
        fails.append("es listen: expected es-ES utterance, got %r" % spoken[:1])

    # complete the 8-question check deterministically
    got_correct = 0
    for _ in range(8):
        right = pg.evaluate("() => { var q=document.querySelector('#starter-check .sc-q'); "
                            "var b=q.querySelector('.sc-opt'); return b ? b.getAttribute('data-opt') : null; }")
        if right is None:
            fails.append("starter check: no options at step")
            break
        pg.click('#starter-check .sc-opt[data-opt="%s"]' % right)
        pg.wait_for_timeout(150)
        fb = pg.evaluate("() => document.querySelector('#starter-check .sc-fb').textContent")
        if fb.startswith("Correct"):
            got_correct += 1
        nxt = pg.evaluate("() => { var b=document.querySelector('#starter-check .sc-nav button'); return b ? b.textContent : null; }")
        if nxt is None:
            fails.append("starter check: no next button")
            break
        pg.click("#starter-check .sc-nav button")
        pg.wait_for_timeout(150)
    done = pg.evaluate("() => { var t=document.querySelector('#starter-check').innerText; return t; }")
    note("es_check_done", done[:140])
    if got_correct != 8:
        fails.append("starter check: expected 8 correct answers, got %d" % got_correct)
    if "nothing is saved" not in done or ("8" not in done):
        fails.append("starter check: final summary missing honest 'nothing is saved'")

    # ---- a non-Latin pack (Bengali) ----
    pg.goto(BASE + "/languages/bn/", wait_until="networkidle")
    wait("#langpack-app .v-item")
    pg.wait_for_timeout(500)
    pg.click("#langpack-app .hi-listen >> nth=0")
    pg.wait_for_timeout(300)
    bn = pg.evaluate("() => window.__spoken[window.__spoken.length - 1]")
    note("bn_spoken", bn)
    if not bn or bn.get("lang") != "bn-IN":
        fails.append("bn listen: expected bn-IN utterance, got %r" % bn)

    # ---- RTL pack (Arabic) — Stage 5 ----
    pg.goto(BASE + "/languages/ar/", wait_until="networkidle")
    wait("#langpack-app .v-item")
    pg.wait_for_timeout(500)
    ar = pg.evaluate("""() => {
        var t = document.body.innerText;
        return {
            listen: document.querySelectorAll('#langpack-app .hi-listen').length,
            rtl: getComputedStyle(document.querySelector('#langpack-app .v-target') || document.body).direction
        };
    }""")
    note("ar_detail", ar)
    if ar["listen"] != 36:
        fails.append("ar detail: expected 36 listen buttons, got %d" % ar["listen"])
    pg.click("#langpack-app .hi-listen >> nth=0")
    pg.wait_for_timeout(300)
    ar_sp = pg.evaluate("() => window.__spoken[window.__spoken.length - 1]")
    note("ar_spoken", ar_sp)
    if not ar_sp or ar_sp.get("lang") != "ar-SA" or ar_sp.get("text") != "أنا":
        fails.append("ar listen: expected ar-SA utterance 'أنا', got %r" % ar_sp)

    # ---- CJK pack (Chinese) — Stage 5 ----
    pg.goto(BASE + "/languages/zh/", wait_until="networkidle")
    wait("#langpack-app .v-item")
    pg.wait_for_timeout(500)
    pg.click("#langpack-app .hi-listen >> nth=0")
    pg.wait_for_timeout(300)
    zh_sp = pg.evaluate("() => window.__spoken[window.__spoken.length - 1]")
    note("zh_spoken", zh_sp)
    if not zh_sp or zh_sp.get("lang") != "zh-CN" or zh_sp.get("text") != "我":
        fails.append("zh listen: expected zh-CN utterance '我', got %r" % zh_sp)

    # ---- Hindi PRODUCTION regression: no listen buttons injected ----
    pg.goto(BASE + "/learn/my-learning/", wait_until="networkidle")
    pg.wait_for_timeout(1500)
    hi = pg.evaluate("""() => ({
        items: document.querySelectorAll('#vocab-app .v-item').length,
        say: document.querySelectorAll('#vocab-app [data-say]').length,
        listen: document.querySelectorAll('#vocab-app .hi-listen').length
    })""")
    note("hindi_regression", hi)
    if hi["items"] < 1:
        fails.append("hindi regression: vocab items not found")
    if hi["say"] or hi["listen"]:
        fails.append("hindi regression: listen buttons leaked into Hindi cards (%r)" % hi)

    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-starter-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("starter-pack learning experience:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-18s %s" % (k, json.dumps(v, ensure_ascii=False)[:130]))
for x in fails:
    print("  FAIL", x)
