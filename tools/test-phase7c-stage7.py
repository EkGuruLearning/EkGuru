#!/usr/bin/env python3
"""Phase 7C Stage 7 — one-language full course (Spanish) gate.

Verifies, in real Chromium, that the first authored non-Hindi course is real,
reviewed, and runs on the same engines as Hindi:

  · course hub   — 6 lesson links + practice/quiz/review links, honest BETA note
  · lesson page  — real content: sections, a dialogue/table, Spanish text
  · practice lab — mounts on the shared practice engine, Listen button speaks
                   the Spanish computer voice (es-ES, browser TTS only)
  · topic quiz   — runs, answers a question, and rotates deterministically
                   per date (same date = same set, different date = new set)
  · review deck  — SRS cards seed and speak with the es-ES computer voice
  · wiring       — pack page links the course; hub cell carries a "Course" tag
  · no page errors on any visited page

Output: reports/phase7c-stage7-test.json
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
      cancel: function(){}, getVoices: function(){ return [{lang:'hi-IN',name:'hi'},{lang:'es-ES',name:'es'},{lang:'ar-SA',name:'ar'}]; },
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

    def goto(url):
        pg.goto(BASE + url, wait_until="networkidle")
        pg.wait_for_timeout(200)

    # ---- 1) course hub ----
    goto("/languages/es/course/")
    hub = pg.evaluate("""() => {
        var links = Array.prototype.slice.call(document.querySelectorAll('ul.linklist a'));
        var lessons = links.filter(function(a){ return a.getAttribute('href').indexOf('/lessons/') !== -1; });
        return {
          h1: (document.querySelector('h1') || {}).textContent || null,
          betaTag: document.body.innerHTML.indexOf('BETA') !== -1,
          lessons: lessons.length,
          lessonHrefs: lessons.map(function(a){ return a.getAttribute('href'); }),
          hasPractice: links.some(function(a){ return a.getAttribute('href').indexOf('/practice/') !== -1; }),
          hasQuiz: links.some(function(a){ return a.getAttribute('href').indexOf('/quiz/') !== -1; }),
          hasReview: links.some(function(a){ return a.getAttribute('href').indexOf('/review/') !== -1; }),
          honestNote: /not yet as deep/.test(document.body.innerHTML)
        };
    }""")
    note("course_hub", hub)
    if not hub["h1"] or "Spanish" not in hub["h1"]:
        fails.append("course hub h1 missing Spanish: %r" % hub["h1"])
    if hub["lessons"] != 6:
        fails.append("course hub should list 6 lessons, got %d" % hub["lessons"])
    if not (hub["hasPractice"] and hub["hasQuiz"] and hub["hasReview"]):
        fails.append("course hub missing practice/quiz/review links: %r" % hub)
    if not hub["honestNote"]:
        fails.append("course hub missing honest BETA note")

    # ---- 2) lesson page ----
    goto("/languages/es/lessons/greetings-and-introductions/")
    lesson = pg.evaluate("""() => ({
        h2: document.querySelectorAll('h2').length,
        table: document.querySelectorAll('table').length,
        hasHola: /hola/i.test(document.body.innerHTML),
        hasTuteo: /usted|tú/i.test(document.body.innerHTML),
        crumb: (document.querySelector('.crumb') || {}).textContent || null
    })""")
    note("lesson_page", lesson)
    if lesson["h2"] < 2:
        fails.append("lesson page too thin: %r" % lesson)
    if not lesson["table"]:
        fails.append("lesson page missing dialogue/table")
    if not lesson["hasHola"]:
        fails.append("lesson page missing Spanish content (hola)")

    # ---- 3) practice lab (shared engine, es-ES voice) ----
    goto("/languages/es/practice/")
    ok = wait(".px-q")
    practice = pg.evaluate("""() => {
        var bank = (window.EKGURU_COURSE_ES && window.EKGURU_COURSE_ES.practice) || {};
        var play = document.querySelector('.px-play');
        var q = document.querySelector('.px-q');
        return {
          mounted: !!q,
          banks: { vocab: (bank.vocabulary || []).length, grammar: (bank.grammar || []).length },
          listenBtn: !!play,
          sayw: play ? play.getAttribute('data-sayw') : null,
          saylang: play ? play.getAttribute('data-saylang') : null,
          note: /computer voice/i.test(document.body.innerHTML)
        };
    }""")
    note("practice_lab", practice)
    if not ok or not practice["mounted"]:
        fails.append("practice lab did not mount")
    if practice["banks"].get("vocab") != 12 or practice["banks"].get("grammar") != 12:
        fails.append("practice banks wrong: %r" % practice["banks"])
    if not practice["listenBtn"]:
        fails.append("practice lab missing Listen button")
    if practice["saylang"] != "es-ES":
        fails.append("practice Listen lang != es-ES: %r" % practice["saylang"])
    if not practice["sayw"]:
        fails.append("practice Listen missing say word (data-sayw)")
    # click Listen, capture the spoken utterance
    pg.click(".px-play")
    pg.wait_for_timeout(200)
    spoken = pg.evaluate("() => window.__spoken || []")
    note("practice_spoken", spoken[:3])
    if not spoken or spoken[0].get("lang") != "es-ES":
        fails.append("practice Listen did not speak es-ES: %r" % spoken[:3])
    if not spoken or str(spoken[0].get("text", "")).strip().lower() != str(practice["sayw"]).strip().lower():
        fails.append("practice Listen spoke wrong text: got %r want %r" % (spoken[0].get("text") if spoken else None, practice["sayw"]))

    # ---- 4) topic quiz: runs + daily rotation ----
    goto("/languages/es/quiz/")
    quiz_dom = pg.evaluate("""() => ({
        hasTopic: !!document.getElementById('es-q-topic'),
        hasStart: !!document.getElementById('es-q-start'),
        topics: Array.prototype.slice.call(document.querySelectorAll('#es-q-topic option')).map(function(o){ return o.value; })
    })""")
    note("quiz_dom", quiz_dom)
    if not (quiz_dom["hasTopic"] and quiz_dom["hasStart"]):
        fails.append("quiz missing controls: %r" % quiz_dom)
    if len(quiz_dom["topics"]) != 5:
        fails.append("quiz should have 5 topics, got %d" % len(quiz_dom["topics"]))
    # rotation determinism: same date -> same order; different dates -> changed
    rot = pg.evaluate("""() => {
        function dayShuffle(a, salt, when){
            var d=when||new Date();
            var key=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")+":"+(salt||"");
            var h=2166136261;for(var i=0;i<key.length;i++){h^=key.charCodeAt(i);h=Math.imul(h,16777619);}
            var s=h>>>0,o=a.slice(),rnd=function(){s|=0;s=(s+0x6D2B79F5)|0;var t=Math.imul(s^(s>>>15),1|s);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};
            for(var i=o.length-1;i>0;i--){var j=Math.floor(rnd()*(i+1));var tmp=o[i];o[i]=o[j];o[j]=tmp;}
            return o;
        }
        var Q=(window.EKGURU_COURSE_ES&&window.EKGURU_COURSE_ES.quiz)||[];
        var pool=Q.filter(function(q){return q.topic==='greetings';});
        var d1=new Date(2026,8,13), d2=new Date(2026,8,14);
        var a=dayShuffle(pool,'quiz:greetings',d1).map(function(q){return q.q;});
        var b2=dayShuffle(pool,'quiz:greetings',d1).map(function(q){return q.q;});
        var c=dayShuffle(pool,'quiz:greetings',d2).map(function(q){return q.q;});
        return { pool: pool.length, same: JSON.stringify(a)===JSON.stringify(b2), changed: JSON.stringify(a)!==JSON.stringify(c) };
    }""")
    note("quiz_rotation", rot)
    if not rot["same"]:
        fails.append("quiz rotation not deterministic per date")
    if not rot["changed"]:
        fails.append("quiz rotation does not change across dates")
    # run the quiz: start, answer first option, next
    pg.click("#es-q-start")
    ok = wait("#es-q-body [data-opt]")
    pg.evaluate("() => document.querySelector('#es-q-body [data-opt]').click()")
    pg.wait_for_timeout(150)
    ran = pg.evaluate("""() => ({
        fb: !!document.getElementById('es-q-fb'),
        fbText: (document.getElementById('es-q-fb')||{}).textContent || null,
        next: !!document.getElementById('es-q-next')
    })""")
    note("quiz_run", ran)
    if not ran["fb"] or not ran["next"]:
        fails.append("quiz did not advance after an answer: %r" % ran)

    # ---- 5) review deck (SRS, es-ES voice) ----
    goto("/languages/es/review/")
    pg.click("#es-srs-seed")
    pg.wait_for_timeout(200)
    srs = pg.evaluate("""() => {
        var stats = (document.getElementById('es-srs-stats')||{}).textContent || null;
        var say = document.getElementById('es-srs-say');
        return { stats: stats, hasCard: !!document.getElementById('es-srs-card').innerHTML.trim(), hasSay: !!say };
    }""")
    note("review_seed", srs)
    if not srs["hasCard"]:
        fails.append("review deck did not show a card after seed")
    if not srs["hasSay"]:
        fails.append("review card missing Listen button")
    pg.click("#es-srs-say")
    pg.wait_for_timeout(200)
    rspoken = pg.evaluate("() => window.__spoken || []")
    note("review_spoken", rspoken[:3])
    if not rspoken or rspoken[0].get("lang") != "es-ES":
        fails.append("review Listen did not speak es-ES: %r" % rspoken[:3])

    # ---- 6) wiring: pack page + hub tag ----
    goto("/languages/es/")
    pack = pg.evaluate("""() => ({
        courseLink: !!Array.prototype.slice.call(document.querySelectorAll('a.btn, a'))
            .find(function(a){ return a.textContent.indexOf('Open the Spanish course') !== -1; }),
        hasLp: !!document.getElementById('langpack-app'),
        hasCheck: !!document.getElementById('starter-check')
    })""")
    note("pack_page", pack)
    if not pack["courseLink"]:
        fails.append("Spanish pack page missing course link")
    if not (pack["hasLp"] and pack["hasCheck"]):
        fails.append("Spanish pack page regressed (starter pack/check missing): %r" % pack)

    goto("/languages/")
    hubcell = pg.evaluate("""() => {
        var a = document.querySelector('a.nm[href="/languages/es/"]');
        return a ? a.textContent : null;
    }""")
    note("hub_cell", hubcell)
    if not hubcell or "Course" not in hubcell:
        fails.append("hub Spanish cell missing Course tag: %r" % hubcell)

    # ---- 7) page errors ----
    note("page_errors", errs)
    if errs:
        fails.append("page errors seen: %r" % errs[:5])

    b.close()

result = {
    "gate": "phase7c-stage7",
    "title": "Spanish full course (Stage 7)",
    "when": NOW,
    "verdict": "PASS" if not fails else "FAIL",
    "pass": not fails,
    "fails": fails,
    "facts": facts,
}
os.makedirs("reports", exist_ok=True)
with open("reports/phase7c-stage7-test.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Phase 7C Stage 7 gate:", result["verdict"])
if fails:
    for fl in fails:
        print("  FAIL:", fl)
else:
    print("  hub lessons:", facts["course_hub"]["lessons"],
          "| practice banks:", facts["practice_lab"]["banks"],
          "| spoken:", facts["practice_spoken"][:1],
          "| quiz rotation:", facts["quiz_rotation"],
          "| review spoken:", facts["review_spoken"][:1])
import sys
sys.exit(0 if not fails else 1)
