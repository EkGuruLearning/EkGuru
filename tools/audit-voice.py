#!/usr/bin/env python3
"""Phase 7B §9 — VOICE deep real test (real Chromium).

Follows the command's 14-step voice investigation plus the §20 provider
matrix. Instruments window.speechSynthesis.speak so we record whether an
utterance is REALLY invoked and which lifecycle events fire (onstart/onend/
onerror) — a PASS is never just `speechSynthesis in window`.

Honest environment note: headless Chromium has the Web Speech API but may
have zero installed voices, so getVoices() can be empty and onstart may not
fire. We record whatever really happens instead of assuming.

Output: reports/phase7b-audio-runtime.json
"""
import json, os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "http://127.0.0.1:8899"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
LESSON = "/learn/how-to-say-hello-in-hindi/"

INSTRUMENT = """
window.__voice = { events: [], utterances: 0 };
(function () {
  if (!window.speechSynthesis) return;
  var orig = window.speechSynthesis.speak.bind(window.speechSynthesis);
  window.speechSynthesis.speak = function (u) {
    window.__voice.utterances += 1;
    var prev = { s: u.onstart, e: u.onend, er: u.onerror };
    var push = function (n) { return function () { window.__voice.events.push(n); }; };
    u.onstart = function (ev) { window.__voice.events.push("start"); if (prev.s) prev.s(ev); };
    u.onend   = function (ev) { window.__voice.events.push("end");   if (prev.e) prev.e(ev); };
    u.onerror = function (ev) { window.__voice.events.push("error");  if (prev.er) prev.er(ev); };
    return orig(u);
  };
})();
"""

fails, facts = [], {}

def note(k, v):
    facts[k] = v

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    ctx.add_init_script(INSTRUMENT)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    # ---- 1. open real Hindi lesson ----
    pg.goto(BASE + LESSON, wait_until="networkidle")
    pg.wait_for_timeout(500)

    # ---- 2. audio control exists ----
    btns = pg.evaluate("() => document.querySelectorAll('button.hi-listen').length")
    note("listen_buttons", btns)
    if btns == 0:
        fails.append("no .hi-listen audio controls on lesson")
    note("honest_label_present", pg.evaluate(
        "() => document.body.innerText.includes('computer voice')"))

    # ---- 3. voices: wait for async population ----
    pg.wait_for_timeout(1000)  # give voiceschanged a chance
    voices = pg.evaluate("() => (window.speechSynthesis.getVoices()||[]).map(v=>v.lang)")
    hi_voices = [v for v in voices if v.lower().startswith("hi")]
    note("voice_count", len(voices))
    note("hi_in_voices", hi_voices)
    note("speechSynthesis_present", pg.evaluate("() => 'speechSynthesis' in window"))

    def snapshot(tag):
        return pg.evaluate("""() => ({
            speaking: speechSynthesis.speaking,
            pending: speechSynthesis.pending,
            paused: speechSynthesis.paused,
        })""")

    # ---- 4. click Listen ----
    if btns:
        pg.click("button.hi-listen >> nth=0")
        pg.wait_for_timeout(250)
        lbl = pg.evaluate("() => document.querySelector('button.hi-listen .hi-listen-lbl').innerText")
        pressed = pg.evaluate("() => document.querySelector('button.hi-listen').getAttribute('aria-pressed')")
        note("after_listen.label", lbl)
        note("after_listen.aria_pressed", pressed)
        note("after_listen.state", snapshot("listen"))
        pg.wait_for_timeout(600)
        note("after_listen.state_600ms", snapshot("listen"))
        note("after_listen.events", pg.evaluate("() => window.__voice.events"))
        note("utterances_invoked", pg.evaluate("() => window.__voice.utterances"))

    # ---- 5. Stop ----
    if btns:
        # button label should now be "Stop"; clicking stops
        pg.click("button.hi-listen >> nth=0")
        pg.wait_for_timeout(200)
        lbl2 = pg.evaluate("() => document.querySelector('button.hi-listen .hi-listen-lbl').innerText")
        pressed2 = pg.evaluate("() => document.querySelector('button.hi-listen').getAttribute('aria-pressed')")
        note("after_stop.label", lbl2)
        note("after_stop.aria_pressed", pressed2)
        note("after_stop.state", snapshot("stop"))

    # ---- 6. Listen again (replay) ----
    if btns:
        pg.click("button.hi-listen >> nth=0")
        pg.wait_for_timeout(200)
        note("replay.utterances", pg.evaluate("() => window.__voice.utterances"))

    # ---- 7. navigate away then return ----
    pg.goto(BASE + "/index.html", wait_until="domcontentloaded")
    pg.wait_for_timeout(300)
    pg.goto(BASE + LESSON, wait_until="networkidle")
    pg.wait_for_timeout(500)
    note("after_return.buttons_remounted", pg.evaluate("() => document.querySelectorAll('button.hi-listen').length"))
    note("after_return.speaking", pg.evaluate("() => speechSynthesis.speaking"))

    # ---- 8. mobile viewport repeat ----
    mctx = b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    mctx.add_init_script(INSTRUMENT)
    mpg = mctx.new_page()
    mpg.goto(BASE + LESSON, wait_until="networkidle")
    mpg.wait_for_timeout(500)
    mbtns = mpg.evaluate("() => document.querySelectorAll('button.hi-listen').length")
    note("mobile.listen_buttons", mbtns)
    if mbtns:
        mpg.locator("button.hi-listen").first.tap()
        mpg.wait_for_timeout(250)
        note("mobile.after_tap.label", mpg.evaluate("() => document.querySelector('button.hi-listen .hi-listen-lbl').innerText"))
        note("mobile.utterances_invoked", mpg.evaluate("() => window.__voice.utterances"))
        mpg.locator("button.hi-listen").first.tap()  # stop
    mctx.close()

    # ---- 9. §20 provider matrix (no crash, honest states) ----
    matrix = pg.evaluate("""() => {
        const A = window.EkGuruAudioProvider;
        const tags = ['hi-IN', 'es-ES', 'fr-FR', 'ar-SA', 'xx-XX', ''];
        const out = {};
        if (!A) return null;
        tags.forEach(function (t) {
            try { out[t] = { resolve: A.resolve(t), describe: A.describe(t).label }; }
            catch (e) { out[t] = { error: String(e) }; }
        });
        return out;
    }""")
    note("provider_matrix", matrix)
    if matrix is None:
        fails.append("EkGuruAudioProvider missing on lesson")
    else:
        if matrix["hi-IN"]["resolve"] not in ("BROWSER_TTS", "UNAVAILABLE"):
            fails.append("hi-IN resolve unexpected: %s" % matrix["hi-IN"]["resolve"])

    note("page_errors", errs)
    b.close()

# ---- 10. §20 provider logic with ENUMERATED voices (stubbed) ----
# Verifies the v31 fix: when voices are enumerated and none match the
# requested tag, resolve() must return UNAVAILABLE (not BROWSER_TTS).
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    ctx.add_init_script("""
        var __fake = [{lang: 'en-US', name: 'A'}, {lang: 'hi-IN', name: 'H'}];
        Object.defineProperty(window.speechSynthesis, 'getVoices',
            { value: function () { return __fake; } });
    """)
    pg = ctx.new_page()
    pg.goto(BASE + LESSON, wait_until="networkidle")
    pg.wait_for_timeout(300)
    enum_matrix = pg.evaluate("""() => {
        const A = window.EkGuruAudioProvider;
        return { hi: A.resolve('hi-IN'), es: A.resolve('es-ES'), xx: A.resolve('xx-XX') };
    }""")
    note("provider_with_enumerated_voices", enum_matrix)
    if enum_matrix["hi"] != "BROWSER_TTS":
        fails.append("with a hi-IN voice, resolve(hi-IN) should be BROWSER_TTS, got %s" % enum_matrix["hi"])
    if enum_matrix["es"] != "UNAVAILABLE":
        fails.append("no es-ES voice present, resolve(es-ES) should be UNAVAILABLE, got %s" % enum_matrix["es"])
    if enum_matrix["xx"] != "UNAVAILABLE":
        fails.append("resolve(xx-XX) should be UNAVAILABLE, got %s" % enum_matrix["xx"])
    b.close()

ok = not fails and not errs
res = {
    "generated": NOW,
    "pass": ok,
    "fails": fails,
    "facts": facts,
    "environment": {
        "voice_count": facts.get("voice_count"),
        "hi_in_voices": facts.get("hi_in_voices"),
        "utterances_invoked": facts.get("utterances_invoked"),
        "note": "headless Chromium may ship zero voices; if so, actual audible speech is"
                " impossible in this harness and that fact is recorded, never papered over.",
    },
}
with open("reports/phase7b-audio-runtime.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("voice runtime:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-28s %s" % (k, json.dumps(v, ensure_ascii=False)[:110]))
for x in fails:
    print("  FAIL", x)
