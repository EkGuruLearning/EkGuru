#!/usr/bin/env python3
"""Phase 7C Stage 7+ — full courses, one language at a time, popular first.

A single, language-parameterized course generator. Each language's authored
content lives in tools/course-data/{code}.py (COURSE + LESSONS + PRACTICE +
QUIZ + REVIEW). This script builds, for every such module:

  js/course-{code}.js        — bank: practice / quiz / review (authored)
  languages/{code}/course/index.html         course hub
  languages/{code}/lessons/{slug}/index.html 6 lessons
  languages/{code}/practice/index.html       practice lab (shared engine)
  languages/{code}/quiz/index.html           topic quiz (daily rotation)
  languages/{code}/review/index.html         SRS review (reuses EkGuruSRS)

plus data/courses.json (manifest for registries + hub/pack pages).

Every course keeps its language BETA (not Hindi-depth, no recorded audio).
Hindi remains the only PRODUCTION language. All audio is the browser's
computer voice, never a native recording.

Run: python3 tools/build-language-course.py            # all data modules
     python3 tools/build-language-course.py fr         # one language only
"""
import importlib.util, json, os, sys, time, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# build-hindi-pages.py has a hyphen in its filename, so import it by path.
_spec = importlib.util.spec_from_file_location("build_hindi_pages", os.path.join(ROOT, "tools", "build-hindi-pages.py"))
_bhp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bhp)
head, foot, write_page, CORE_STYLE = _bhp.head, _bhp.foot, _bhp.write_page, _bhp.CORE_STYLE

NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
BASE = "https://ekguru.shop"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def esc_html(s):
    return str(s)


def load_course_data(code):
    path = os.path.join("tools", "course-data", code + ".py")
    spec = importlib.util.spec_from_file_location("course_" + code, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def cfg_of(m):
    c = m.COURSE
    code = c["lang"]
    return {
        "code": code,
        "name": c["name"],
        "native": c.get("native", c["name"]),
        "speech": c.get("speechTag", code + "-" + code.upper()),
        "note": c["note"],
        "jsvar": "EKGURU_COURSE_" + code.upper(),
        "bankfile": "js/course-%s.js" % code,
        "category": c["name"].lower(),
        "status": c.get("status", "BETA"),
        "LESSONS": m.LESSONS,
        "PRACTICE": m.PRACTICE,
        "QUIZ": m.QUIZ,
        "REVIEW": m.REVIEW,
    }


# --------------------------------------------------------------------------
# GENERATORS (parameterized on C)
# --------------------------------------------------------------------------

def lesson_html(C, l):
    secs = "".join(
        '  <h2>%s</h2>\n' % esc_html(h) +
        "".join('  <p>%s</p>\n' % p for p in paras)
        for h, paras in l["sections"])
    tbl = ""
    if "table" in l:
        headers, rows = l["table"]
        head_cells = "".join('<th>%s</th>' % esc_html(c) for c in headers)
        body_rows = "".join(
            '<tr>' + "".join('<td>%s</td>' % esc_html(c) for c in r) + '</tr>\n'
            for r in rows)
        tbl = ('  <table>\n  <thead><tr>%s</tr></thead>\n  <tbody>\n%s  </tbody>\n  </table>\n'
               % (head_cells, body_rows))
    return ('  <h1>%s</h1>\n'
            '  <p class="lede">%s</p>\n'
            '  <div class="note"><b>Beta course.</b> Authored %s content, part of the free '
            'EkGuru %s course in beta. Audio is your browser’s computer voice, not a native recording.</div>\n'
            '%s%s'
            '  <p style="margin-top:26px"><a class="btn" href="/languages/%s/course/">%s course</a> '
            '<a class="btn" href="/languages/%s/practice/">Practice</a> '
            '<a class="btn" href="/languages/%s/quiz/">Quiz</a> '
            '<a class="btn" href="/languages/%s/review/">Review</a></p>\n'
            % (esc_html(l["title"]), esc_html(l["desc"]), esc_html(C["name"]), esc_html(C["name"]),
               secs, tbl, C["code"], C["name"], C["code"], C["code"], C["code"]))


def build_lessons(C):
    made = []
    for l in C["LESSONS"]:
        path = "languages/%s/lessons/%s/index.html" % (C["code"], l["slug"])
        up = "../../../../"
        title = "%s — %s Course" % (l["title"], C["name"])
        crumb = ('<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › '
                 '<a href="/languages/%s/">%s</a> › <a href="/languages/%s/course/">Course</a> › %s'
                 % (C["code"], esc_html(C["name"]), C["code"], esc_html(l["title"])))
        write_page(path, up, title, l["desc"], "languages/%s/lessons/%s/" % (C["code"], l["slug"]),
                   crumb, lesson_html(C, l), scripts=(), index=True,
                   extra_style=".art table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.95rem}"
                               ".art th,.art td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}"
                               ".art th{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}")
        made.append(path)
    return made


def build_course_hub(C):
    lessons = "".join(
        '  <li><a href="/languages/%s/lessons/%s/">%s</a><span>%s</span></li>\n'
        % (C["code"], l["slug"], esc_html(l["title"]), esc_html(l["desc"][:90] + "…"))
        for l in C["LESSONS"])
    body = (
        '  <h1>%s Course <span class="tag beta" style="vertical-align:4px">BETA</span></h1>\n'
        '  <p class="lede">A real, free %s course: lessons, practice, a quiz and a review deck — '
        'all running on the same engines as the Hindi course.</p>\n'
        '  <div class="note"><b>Honest status.</b> %s</div>\n'
        '  <h2>Lessons</h2>\n'
        '  <ul class="linklist">\n%s  </ul>\n'
        '  <h2>Practice and review</h2>\n'
        '  <ul class="linklist">\n'
        '  <li><a href="/languages/%s/practice/">Practice lab</a><span>Recognition drills on vocabulary and grammar, with the %s computer voice.</span></li>\n'
        '  <li><a href="/languages/%s/quiz/">Topic quiz</a><span>20 multiple-choice questions with explanations; the set rotates daily.</span></li>\n'
        '  <li><a href="/languages/%s/review/">Review deck</a><span>Spaced repetition of the words and phrases, saved on this device only.</span></li>\n'
        '  </ul>\n'
        '  <p><a class="btn" href="/languages/%s/">%s starter pack</a> '
        '<a class="btn" href="/languages/">All languages</a></p>\n'
    ) % (esc_html(C["name"]), esc_html(C["name"]), esc_html(C["note"]), lessons,
         C["code"], C["name"], C["code"], C["code"], C["code"], C["name"])
    write_page("languages/%s/course/index.html" % C["code"], "../../../",
               "Learn %s — free course (beta)" % C["name"],
               "A free %s course in beta: six lessons, a practice lab, a topic quiz and a spaced-repetition review deck — all in your browser." % C["name"],
               "languages/%s/course/" % C["code"],
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/%s/">%s</a> › Course'
               % (C["code"], esc_html(C["name"])),
               body, scripts=(), index=True)
    return "languages/%s/course/index.html" % C["code"]


def build_practice(C):
    code = C["code"]
    body = (
        '  <h1>%s Practice <span class="tag beta" style="vertical-align:4px">BETA</span></h1>\n'
        '  <p class="lede">Recognition drills on %s vocabulary and grammar. Pick a bank, '
        'then answer — the explanation follows each answer.</p>\n'
        '  <div class="row" style="gap:10px;flex-wrap:wrap;margin:14px 0">\n'
        '    <button type="button" class="btn" id="%s-b-vocab">Vocabulary</button>\n'
        '    <button type="button" class="btn" id="%s-b-grammar">Grammar</button>\n'
        '  </div>\n'
        '  <div class="px-wrap" id="%s-practice"></div>\n'
        '  <script>\n'
        '  (function () {\n'
        '    function mount(bank) {\n'
        '      if (window.%s && window.%s.practice) {\n'
        '        window.EKGURU_PRACTICE_BANK = window.%s.practice;\n'
        '      }\n'
        '      var el = document.getElementById("%s-practice");\n'
        '      if (window.EkGuruPractice) window.EkGuruPractice.mount(el, {mode:"practice", bank:bank, count:10, speechLang:"%s"});\n'
        '    }\n'
        '    function on(id, bank) { var b = document.getElementById(id); if (b) b.addEventListener("click", function(){ mount(bank); }); }\n'
        '    on("%s-b-vocab", "vocabulary"); on("%s-b-grammar", "grammar");\n'
        '    var t = setInterval(function () {\n'
        '      if (window.EkGuruPractice && window.%s) { clearInterval(t); mount("vocabulary"); }\n'
        '    }, 100);\n'
        '    setTimeout(function(){ clearInterval(t); }, 5000);\n'
        '  })();\n'
        '  </script>\n'
    ) % (esc_html(C["name"]), esc_html(C["name"]), code, code, code,
         C["jsvar"], C["jsvar"], C["jsvar"], code, C["speech"],
         code, code, C["jsvar"])
    write_page("languages/%s/practice/index.html" % code, "../../../",
               "%s Practice — Vocabulary & Grammar Drills" % C["name"],
               "Free %s practice drills: see a %s word or rule, pick the meaning, get the explanation. Computer voice playback, saved in your browser." % (C["name"], C["name"]),
               "languages/%s/practice/" % code,
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/%s/">%s</a> › Practice'
               % (code, esc_html(C["name"])),
               body, scripts=["course-%s.js" % code, "practice-engine.js"], index=True)
    return "languages/%s/practice/index.html" % code


def build_quiz(C):
    code = C["code"]
    body = (
        '  <h1>%s Topic Quiz <span class="tag beta" style="vertical-align:4px">BETA</span></h1>\n'
        '  <p class="lede">20 multiple-choice questions with explanations, drawn from the %s lessons.</p>\n'
        '  <div class="row" style="gap:12px;flex-wrap:wrap;align-items:end">\n'
        '    <div><label for="%s-q-topic">Topic</label><br><select id="%s-q-topic"></select></div>\n'
        '    <div><label for="%s-q-n">Questions</label><br><select id="%s-q-n">\n'
        '      <option value="5">5</option><option value="10">10</option><option value="20">20</option></select></div>\n'
        '    <button type="button" class="btn" id="%s-q-start">Start</button>\n'
        '  </div>\n'
        '  <p class="muted" style="font-size:.8rem;margin-top:8px">Questions rotate each day for the same topic '
        '(rule-based, not random) — come back tomorrow for a new set.</p>\n'
        '  <div id="%s-q-body" style="margin-top:16px"></div>\n'
        '  <script>\n'
        '  (function () {\n'
        '    "use strict";\n'
        '    function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}\n'
        '    function shuffle(a){var o=a.slice();for(var i=o.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=o[i];o[i]=o[j];o[j]=t;}return o;}\n'
        '    function dayShuffle(a, salt, when){var d=when||new Date();var key=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")+":"+(salt||"");var h=2166136261;for(var i=0;i<key.length;i++){h^=key.charCodeAt(i);h=Math.imul(h,16777619);}var s=h>>>0;var o=a.slice();var rnd=function(){s|=0;s=(s+0x6D2B79F5)|0;var t=Math.imul(s^(s>>>15),1|s);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};for(var i=o.length-1;i>0;i--){var j=Math.floor(rnd()*(i+1));var tmp=o[i];o[i]=o[j];o[j]=tmp;}return o;}\n'
        '    var state = null, sel = document.getElementById("%s-q-topic");\n'
        '    function init() {\n'
        '      var Q = (window.%s && window.%s.quiz) || [];\n'
        '      var topics = {}; Q.forEach(function(q){ topics[q.topic]=1; });\n'
        '      sel.innerHTML = Object.keys(topics).map(function(t){ return \'<option value="\'+esc(t)+\'">\'+esc(t)+\'</option>\'; }).join("");\n'
        '      document.getElementById("%s-q-start").addEventListener("click", function(){\n'
        '        var topic = sel.value; var n = parseInt(document.getElementById("%s-q-n").value, 10);\n'
        '        var pool = Q.filter(function(q){ return q.topic === topic; });\n'
        '        var use = dayShuffle(pool, "quiz:" + topic).slice(0, n);\n'
        '        if (!use.length) { document.getElementById("%s-q-body").innerHTML = "<p class=\\"muted\\">No questions for this topic yet.</p>"; return; }\n'
        '        state = { i:0, correct:0, use:use }; renderQuestion();\n'
        '      });\n'
        '    }\n'
        '    function renderQuestion() {\n'
        '      var b = document.getElementById("%s-q-body");\n'
        '      if (!state || state.i >= state.use.length) { b.innerHTML = state ? "<p>Finished.</p>" : ""; return; }\n'
        '      var q = state.use[state.i];\n'
        '      var opts = shuffle(q.opts.slice());\n'
        '      b.innerHTML = \'<p class="muted">Question \' + (state.i+1) + \' of \' + state.use.length + \' — \' + esc(q.topic) + \'</p>\' +\n'
        '        \'<p style="font-weight:700;font-size:1.05rem">\' + esc(q.q) + \'</p>\' +\n'
        '        opts.map(function(o,idx){ return \'<button type="button" class="btn ghost" style="display:block;width:100%%;text-align:left;margin:6px 0" data-opt="\'+idx+\'">\'+esc(o)+\'</button>\'; }).join("") +\n'
        '        \'<div id="%s-q-fb" style="margin-top:10px"></div>\';\n'
        '      b.querySelectorAll("[data-opt]").forEach(function(btn){\n'
        '        btn.addEventListener("click", function(){\n'
        '          var chosen = opts[parseInt(btn.getAttribute("data-opt"),10)];\n'
        '          var ok = chosen === q.a; if (ok) state.correct++;\n'
        '          var fb = b.querySelector("#%s-q-fb");\n'
        '          fb.innerHTML = \'<p style="font-weight:600;color:\' + (ok ? "var(--green,#1a7f37)" : "var(--red,#b3261e)") + \'\">\' +\n'
        '            (ok ? "Correct." : "Not quite — the answer was “" + esc(q.a) + "”.") + \'</p>\' +\n'
        '            \'<p class="muted">\' + esc(q.explain) + \'</p>\' +\n'
        '            \'<button type="button" class="btn" id="%s-q-next">Next</button>\';\n'
        '          b.querySelector("#%s-q-next").addEventListener("click", function(){ state.i++; renderQuestion(); });\n'
        '        });\n'
        '      });\n'
        '    }\n'
        '    if (window.%s) init();\n'
        '    else window.addEventListener("load", init);\n'
        '  })();\n'
        '  </script>\n'
    ) % (esc_html(C["name"]), esc_html(C["name"]), code, code, code, code, code, code,
         code, C["jsvar"], C["jsvar"], code, code, code, code, code, code, code, code, C["jsvar"])
    write_page("languages/%s/quiz/index.html" % code, "../../../",
               "%s Quiz — Topic Questions with Explanations" % C["name"],
               "A free %s topic quiz: multiple-choice questions with explanations, drawn from the %s lessons. The set rotates daily." % (C["name"], C["name"]),
               "languages/%s/quiz/" % code,
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/%s/">%s</a> › Quiz'
               % (code, esc_html(C["name"])),
               body, scripts=["course-%s.js" % code], index=True)
    return "languages/%s/quiz/index.html" % code


def build_review(C):
    code = C["code"]
    body = (
        '  <h1>%s Review <span class="tag beta" style="vertical-align:4px">BETA</span></h1>\n'
        '  <p class="lede">A simple spaced-repetition deck for the %s words and phrases, saved on this device only.</p>\n'
        '  <div id="%s-srs-stats" style="margin:12px 0;font-weight:600"></div>\n'
        '  <div id="%s-srs-card" style="border:1px solid var(--line);border-radius:14px;padding:20px;background:var(--card,#fff)"></div>\n'
        '  <div id="%s-srs-empty" style="display:none" class="note">No %s cards due right now. Load the deck to start.</div>\n'
        '  <div style="margin-top:14px">\n'
        '    <button type="button" class="btn" id="%s-srs-seed">Load %s deck</button>\n'
        '    <button type="button" class="btn ghost" id="%s-srs-reset">Remove all %s cards</button>\n'
        '  </div>\n'
        '  <script>\n'
        '  (function () {\n'
        '    "use strict";\n'
        '    function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}\n'
        '    var queue = [], card = null;\n'
        '    function seed() {\n'
        '      var deck = (window.%s && window.%s.review) || [];\n'
        '      var added = 0;\n'
        '      deck.forEach(function (w) {\n'
        '        var r = window.EkGuruSRS.add({ prompt: w.p, answer: w.a, category: "%s", level: "beginner", language: "%s", target: w.p });\n'
        '        if (r.added) added++;\n'
        '      });\n'
        '      return added;\n'
        '    }\n'
        '    function paint() {\n'
        '      var st = document.getElementById("%s-srs-stats");\n'
        '      var due = window.EkGuruSRS.due().filter(function (c) { return c.language === "%s"; });\n'
        '      st.textContent = due.length + " %s cards due";\n'
        '      var box = document.getElementById("%s-srs-card");\n'
        '      var empty = document.getElementById("%s-srs-empty");\n'
        '      if (!queue.length) { queue = due; }\n'
        '      card = queue.shift() || null;\n'
        '      if (!card) { box.innerHTML = ""; empty.style.display = "block"; return; }\n'
        '      empty.style.display = "none";\n'
        '      var say = card.target || card.prompt;\n'
        '      box.innerHTML =\n'
        '        \'<p class="prompt">\' + esc(card.prompt) +\n'
        '        \'<button type="button" class="hi-listen" id="%s-srs-say" aria-label="Listen (computer voice)" aria-pressed="false"><span aria-hidden="true">🔊</span> Listen</button></p>\' +\n'
        '        \'<div class="answer" id="%s-srs-a" style="display:none;background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:10px;padding:12px 14px;margin:0 0 14px;color:var(--ink-2)"><b>\' + esc(card.answer) + \'</b></div>\' +\n'
        '        \'<button type="button" class="btn ghost" id="%s-srs-show">Show answer</button>\' +\n'
        '        \'<div class="rates" id="%s-srs-rates" style="display:none;margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">\' +\n'
        '        \'<button type="button" class="btn ghost" data-r="again">Again</button>\' +\n'
        '        \'<button type="button" class="btn ghost" data-r="hard">Hard</button>\' +\n'
        '        \'<button type="button" class="btn" data-r="good">Good</button>\' +\n'
        '        \'<button type="button" class="btn" data-r="easy">Easy</button></div>\';\n'
        '      var sayBtn = box.querySelector("#%s-srs-say");\n'
        '      if (sayBtn) sayBtn.addEventListener("click", function (e) {\n'
        '        e.preventDefault();\n'
        '        var A = window.EkGuruHindiAudio;\n'
        '        if (A && A.supported()) A.speak(String(card.target || card.prompt), sayBtn, "%s");\n'
        '      });\n'
        '      box.querySelector("#%s-srs-show").addEventListener("click", function () {\n'
        '        box.querySelector("#%s-srs-a").style.display = "block";\n'
        '        box.querySelector("#%s-srs-rates").style.display = "flex";\n'
        '        this.style.display = "none";\n'
        '      });\n'
        '      box.querySelectorAll("[data-r]").forEach(function (b) {\n'
        '        b.addEventListener("click", function () { window.EkGuruSRS.review(card.card_id, b.getAttribute("data-r")); paint(); });\n'
        '      });\n'
        '    }\n'
        '    document.getElementById("%s-srs-seed").addEventListener("click", function () { var n = seed(); queue = []; paint(); });\n'
        '    document.getElementById("%s-srs-reset").addEventListener("click", function () {\n'
        '      window.EkGuruSRS.all().forEach(function (c) { if (c.language === "%s") window.EkGuruSRS.remove(c.card_id); });\n'
        '      queue = []; paint();\n'
        '    });\n'
        '    if (window.EkGuruSRS) paint();\n'
        '    else window.addEventListener("load", paint);\n'
        '  })();\n'
        '  </script>\n'
    ) % (esc_html(C["name"]), esc_html(C["name"]), code, code, code, esc_html(C["name"]),
         code, esc_html(C["name"]), code, esc_html(C["name"]),
         C["jsvar"], C["jsvar"], C["category"], code,
         code, code, esc_html(C["name"]), code, code,
         code, code, code, code, code, C["speech"], code, code, code, code, code, code)
    write_page("languages/%s/review/index.html" % code, "../../../",
               "%s Review — spaced repetition" % C["name"],
               "Review the %s words and phrases you saved, on a simple spaced-repetition schedule that lives in your browser." % C["name"],
               "languages/%s/review/" % code,
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/%s/">%s</a> › Review'
               % (code, esc_html(C["name"])),
               body, scripts=["course-%s.js" % code, "hindi-srs.js", "hindi-audio.js"], index=False,
               extra_style=".hi-listen{display:inline-flex;align-items:center;gap:5px;margin:0 0 0 8px;padding:4px 10px;font-size:.82rem;line-height:1.4;border-radius:999px;border:1px solid var(--line);background:var(--bg-soft);color:var(--ink);cursor:pointer;vertical-align:middle}"
                            ".hi-listen.playing{background:var(--brand);border-color:var(--brand);color:#fff}"
                            "#%s-srs-card .prompt{font-size:1.15rem;font-weight:700;margin-bottom:14px}" % code)
    return "languages/%s/review/index.html" % code


def build_bank_js(C):
    data = {"practice": C["PRACTICE"], "quiz": C["QUIZ"], "review": C["REVIEW"]}
    js = ("/* EkGuru — %s COURSE BANK (authored, single source of truth).\n"
          "   Generated by tools/build-language-course.py — do not hand-edit. */\n"
          "window.%s = " % (C["name"].upper(), C["jsvar"])) + json.dumps(data, ensure_ascii=False, indent=1) + ";\n"
    with open(C["bankfile"], "w", encoding="utf-8") as f:
        f.write(js)
    return C["bankfile"]


def build_manifest(summaries):
    manifest = {
        "generated": NOW,
        "policy": ("A language gets a course object only when real authored lessons + practice + quiz + "
                   "review exist. A course keeps a language BETA (still not Hindi-depth, still no "
                   "recorded audio). PRODUCTION remains Hindi only."),
        "courses": summaries,
    }
    with open("data/courses.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return "data/courses.json"


def build_course(code):
    m = load_course_data(code)
    C = cfg_of(m)
    made = [build_bank_js(C)]
    made += build_lessons(C)
    made.append(build_course_hub(C))
    made.append(build_practice(C))
    made.append(build_quiz(C))
    made.append(build_review(C))
    summary = {
        "lang": C["code"], "name": C["name"], "native": C["native"], "speechTag": C["speech"],
        "status": C["status"],
        "lessons": len(C["LESSONS"]),
        "practiceItems": sum(len(v) for v in C["PRACTICE"].values()),
        "quizQuestions": len(C["QUIZ"]),
        "reviewCards": len(C["REVIEW"]),
        "url": "languages/%s/course/" % C["code"],
        "note": C["note"],
    }
    return summary, made


def main():
    codes = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not codes:
        codes = sorted(
            os.path.splitext(os.path.basename(p))[0]
            for p in glob.glob(os.path.join("tools", "course-data", "*.py"))
            if os.path.basename(p) != "__init__.py")
    summaries = []
    for code in codes:
        summary, made = build_course(code)
        summaries.append(summary)
        print("%s course built (%s):" % (summary["name"], code))
        for path in made:
            print("   ", path)
    build_manifest(summaries)
    print("manifest:", "data/courses.json (%d courses)" % len(summaries))


if __name__ == "__main__":
    main()
