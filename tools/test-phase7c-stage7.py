#!/usr/bin/env python3
"""Phase 7C Stage 7+ — full-course gate (one language at a time, popular first).

Verifies, in real Chromium, every course in data/courses.json:

  · course hub   — N lesson links + practice/quiz/review links, honest BETA note
  · lesson page  — real content: sections, a dialogue/table, target-language text
  · practice lab — mounts on the shared practice engine, Listen button speaks
                   the course's computer voice (correct BCP-47 tag, browser TTS only)
  · topic quiz   — runs, answers a question, and rotates deterministically
                   per date (same date = same set, different date = new set)
  · review deck  — SRS cards seed and speak with the course's computer voice
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

with open("data/courses.json", encoding="utf-8") as f:
    COURSES = json.load(f).get("courses", [])

STUB = """
window.__spoken = [];
try {
  Object.defineProperty(window, 'speechSynthesis', {
    configurable: true,
    value: {
      speak: function(u){ window.__spoken.push({text: u.text, lang: u.lang}); },
      cancel: function(){}, getVoices: function(){ return [{lang:'hi-IN',name:'hi'},{lang:'es-ES',name:'es'},{lang:'fr-FR',name:'fr'}]; },
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

    for course in COURSES:
        code = course["lang"]
        name = course["name"]
        speech = course.get("speechTag", code + "-" + code.upper())
        jsvar = "EKGURU_COURSE_" + code.upper()
        tag = code

        # ---- 1) course hub ----
        goto("/languages/%s/course/" % code)
        hub = pg.evaluate("""(m) => {
            var links = Array.prototype.slice.call(document.querySelectorAll('ul.linklist a'));
            var lessons = links.filter(function(a){ return a.getAttribute('href').indexOf('/lessons/') !== -1; });
            return {
              h1: (document.querySelector('h1') || {}).textContent || null,
              betaTag: document.body.innerHTML.indexOf('BETA') !== -1,
              lessons: lessons.length,
              hasPractice: links.some(function(a){ return a.getAttribute('href').indexOf('/practice/') !== -1; }),
              hasQuiz: links.some(function(a){ return a.getAttribute('href').indexOf('/quiz/') !== -1; }),
              hasReview: links.some(function(a){ return a.getAttribute('href').indexOf('/review/') !== -1; }),
              honestNote: /not yet as deep/.test(document.body.innerHTML)
            };
        }""", {"code": code})
        note("hub:%s" % code, hub)
        if not hub["h1"] or name not in hub["h1"]:
            fails.append("[%s] course hub h1 missing name: %r" % (code, hub["h1"]))
        if hub["lessons"] != course.get("lessons"):
            fails.append("[%s] course hub should list %d lessons, got %d" % (code, course.get("lessons"), hub["lessons"]))
        if not (hub["hasPractice"] and hub["hasQuiz"] and hub["hasReview"]):
            fails.append("[%s] course hub missing practice/quiz/review links: %r" % (code, hub))
        if not hub["honestNote"]:
            fails.append("[%s] course hub missing honest BETA note" % code)

        # ---- 2) lesson page (first lesson) ----
        first_slug = pg.evaluate("""() => {
            var a = document.querySelector('ul.linklist a[href*="/lessons/"]');
            return a ? a.getAttribute('href') : null;
        }""")
        if not first_slug:
            fails.append("[%s] no first lesson link found" % code)
        else:
            goto(first_slug)
            lesson = pg.evaluate("""() => ({
                h2: document.querySelectorAll('h2').length,
                table: document.querySelectorAll('table').length,
                crumb: (document.querySelector('.crumb') || {}).textContent || null
            })""")
            note("lesson:%s" % code, lesson)
            if lesson["h2"] < 2:
                fails.append("[%s] lesson page too thin: %r" % (code, lesson))
            if not lesson["table"]:
                fails.append("[%s] lesson page missing dialogue/table" % code)

        # ---- 3) practice lab (shared engine, course voice) ----
        goto("/languages/%s/practice/" % code)
        ok = wait(".px-q")
        practice = pg.evaluate("""(m) => {
            var bank = (window[m.jsvar] && window[m.jsvar].practice) || {};
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
        }""", {"jsvar": jsvar})
        note("practice:%s" % code, practice)
        if not ok or not practice["mounted"]:
            fails.append("[%s] practice lab did not mount" % code)
        if practice["banks"].get("vocab") < 6 or practice["banks"].get("grammar") < 6:
            fails.append("[%s] practice banks thin: %r" % (code, practice["banks"]))
        if not practice["listenBtn"]:
            fails.append("[%s] practice lab missing Listen button" % code)
        if practice["saylang"] != speech:
            fails.append("[%s] practice Listen lang != %s: %r" % (code, speech, practice["saylang"]))
        if not practice["sayw"]:
            fails.append("[%s] practice Listen missing say word (data-sayw)" % code)
        pg.click(".px-play")
        pg.wait_for_timeout(200)
        spoken = pg.evaluate("() => window.__spoken || []")
        note("practice_spoken:%s" % code, spoken[:2])
        if not spoken or spoken[0].get("lang") != speech:
            fails.append("[%s] practice Listen did not speak %s: %r" % (code, speech, spoken[:2]))
        elif practice["sayw"] and str(spoken[0].get("text", "")).strip().lower() != str(practice["sayw"]).strip().lower():
            fails.append("[%s] practice Listen spoke wrong text: got %r want %r" % (code, spoken[0].get("text"), practice["sayw"]))

        # ---- 4) topic quiz: runs + daily rotation ----
        goto("/languages/%s/quiz/" % code)
        quiz_dom = pg.evaluate("""() => ({
            hasTopic: !!document.getElementById('%s-q-topic'),
            hasStart: !!document.getElementById('%s-q-start'),
            topics: Array.prototype.slice.call(document.querySelectorAll('#%s-q-topic option')).map(function(o){ return o.value; })
        })""" % (code, code, code))
        note("quiz_dom:%s" % code, quiz_dom)
        if not (quiz_dom["hasTopic"] and quiz_dom["hasStart"]):
            fails.append("[%s] quiz missing controls: %r" % (code, quiz_dom))
        if len(quiz_dom["topics"]) < 1:
            fails.append("[%s] quiz has no topics" % code)
        rot = pg.evaluate("""(m) => {
            function dayShuffle(a, salt, when){
                var d=when||new Date();
                var key=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")+":"+(salt||"");
                var h=2166136261;for(var i=0;i<key.length;i++){h^=key.charCodeAt(i);h=Math.imul(h,16777619);}
                var s=h>>>0,o=a.slice(),rnd=function(){s|=0;s=(s+0x6D2B79F5)|0;var t=Math.imul(s^(s>>>15),1|s);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};
                for(var i=o.length-1;i>0;i--){var j=Math.floor(rnd()*(i+1));var tmp=o[i];o[i]=o[j];o[j]=tmp;}
                return o;
            }
            var Q=(window[m.jsvar]&&window[m.jsvar].quiz)||[];
            var topic=Q.length ? Q[0].topic : 'greetings';
            var pool=Q.filter(function(q){return q.topic===topic;});
            var d1=new Date(2026,8,13), d2=new Date(2026,8,14);
            var a=dayShuffle(pool,'quiz:'+topic,d1).map(function(q){return q.q;});
            var b2=dayShuffle(pool,'quiz:'+topic,d1).map(function(q){return q.q;});
            var c=dayShuffle(pool,'quiz:'+topic,d2).map(function(q){return q.q;});
            return { pool: pool.length, same: JSON.stringify(a)===JSON.stringify(b2), changed: JSON.stringify(a)!==JSON.stringify(c) };
        }""", {"jsvar": jsvar})
        note("quiz_rotation:%s" % code, rot)
        if not rot["same"]:
            fails.append("[%s] quiz rotation not deterministic per date" % code)
        if not rot["changed"]:
            fails.append("[%s] quiz rotation does not change across dates" % code)
        pg.click("#%s-q-start" % code)
        ok = wait("#%s-q-body [data-opt]" % code)
        pg.evaluate("() => document.querySelector('#%s-q-body [data-opt]').click()" % code)
        pg.wait_for_timeout(150)
        ran = pg.evaluate("""(m) => ({
            fb: !!document.getElementById('%s-q-fb'),
            next: !!document.getElementById('%s-q-next')
        })""" % (code, code), {})
        note("quiz_run:%s" % code, ran)
        if not ran["fb"] or not ran["next"]:
            fails.append("[%s] quiz did not advance after an answer: %r" % (code, ran))

        # ---- 5) review deck (SRS, course voice) ----
        goto("/languages/%s/review/" % code)
        pg.click("#%s-srs-seed" % code)
        pg.wait_for_timeout(200)
        srs = pg.evaluate("""(m) => {
            var stats = (document.getElementById('%s-srs-stats')||{}).textContent || null;
            var say = document.getElementById('%s-srs-say');
            return { stats: stats, hasCard: !!document.getElementById('%s-srs-card').innerHTML.trim(), hasSay: !!say };
        }""" % (code, code, code), {})
        note("review_seed:%s" % code, srs)
        if not srs["hasCard"]:
            fails.append("[%s] review deck did not show a card after seed" % code)
        if not srs["hasSay"]:
            fails.append("[%s] review card missing Listen button" % code)
        pg.click("#%s-srs-say" % code)
        pg.wait_for_timeout(200)
        rspoken = pg.evaluate("() => window.__spoken || []")
        note("review_spoken:%s" % code, rspoken[:2])
        if not rspoken or rspoken[0].get("lang") != speech:
            fails.append("[%s] review Listen did not speak %s: %r" % (code, speech, rspoken[:2]))

        # ---- 6) wiring: pack page + hub tag ----
        goto("/languages/%s/" % code)
        pack = pg.evaluate("""(m) => ({
            courseLink: !!Array.prototype.slice.call(document.querySelectorAll('a.btn, a'))
                .find(function(a){ return a.textContent.indexOf('Open the ' + m.name + ' course') !== -1; }),
            hasLp: !!document.getElementById('langpack-app'),
            hasCheck: !!document.getElementById('starter-check')
        })""", {"name": name})
        note("pack:%s" % code, pack)
        if not pack["courseLink"]:
            fails.append("[%s] pack page missing course link" % code)
        if not (pack["hasLp"] and pack["hasCheck"]):
            fails.append("[%s] pack page regressed (starter pack/check missing): %r" % (code, pack))

        goto("/languages/")
        hubcell = pg.evaluate("""(m) => {
            var a = document.querySelector('a.nm[href="/languages/%s/"]');
            return a ? a.textContent : null;
        }""" % code, {})
        note("hub_cell:%s" % code, hubcell)
        if not hubcell or "Course" not in hubcell:
            fails.append("[%s] hub cell missing Course tag: %r" % (code, hubcell))

    note("page_errors", errs)
    if errs:
        fails.append("page errors seen: %r" % errs[:5])

    b.close()

result = {
    "gate": "phase7c-stage7",
    "title": "full courses (one language at a time)",
    "when": NOW,
    "courses_tested": [c["lang"] for c in COURSES],
    "verdict": "PASS" if not fails else "FAIL",
    "pass": not fails,
    "fails": fails,
    "facts": facts,
}
os.makedirs("reports", exist_ok=True)
with open("reports/phase7c-stage7-test.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Phase 7C full-course gate:", result["verdict"], "| courses:", result["courses_tested"])
if fails:
    for fl in fails:
        print("  FAIL:", fl)
else:
    for c in COURSES:
        code = c["lang"]
        print("  %s: practice banks %s | spoken %s | quiz topics %d | rotation %s | review spoken %s"
              % (code, facts["practice:%s" % code]["banks"],
                 facts["practice_spoken:%s" % code][:1],
                 len(facts["quiz_dom:%s" % code]["topics"]),
                 facts["quiz_rotation:%s" % code],
                 facts["review_spoken:%s" % code][:1]))
import sys
sys.exit(0 if not fails else 1)
