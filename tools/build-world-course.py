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

A completed course marks its language Available. Honest limits: not Hindi-depth, no recorded audio.
Hindi remains the only PRODUCTION language. All audio is the browser's
computer voice, never a native recording.

Run: python3 tools/build-world-course.py            # all data modules
     python3 tools/build-world-course.py fr       # one language only (manifest keeps ALL)
"""
import importlib.util, json, os, sys, time, glob
from lib.speech_tags import speech_tag   # canonical BCP-47 tags
from lib.flashcard_section import flashcard_section, mount_script  # PHASE 9 decks

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
        "speech": c.get("speechTag") or speech_tag(code),
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
            '  <div class="note"><b>Full course.</b> Authored %s content, part of the free '
            'EkGuru %s course. Audio is your browser’s computer voice, not a native recording.</div>\n'
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
        '  <h1>%s Course <span style="display:inline-block;border-radius:999px;padding:2px 10px;font-size:.72rem;font-weight:700;color:#fff;background:#1a7f37;vertical-align:4px">Available</span></h1>\n'
        '  <p class="lede">A real, free %s course: lessons, practice, a quiz and a review deck — '
        'all running on the same engines as the Hindi course.</p>\n'
        '  <div class="note"><b>Honest status.</b> %s</div>\n'
        '  <h2>Lessons</h2>\n'
        '  <ul class="linklist">\n%s  </ul>\n'
        '  <h2>Practice and review</h2>\n'
        '  <ul class="linklist">\n'
        '  <li><a href="/languages/%s/practice/">Practice lab</a><span>Recognition drills on vocabulary and grammar, with the %s computer voice.</span></li>\n'
        '  <li><a href="/languages/%s/quiz/">Topic quiz</a><span>%d questions across lesson topics; available round lengths vary by topic.</span></li>\n'
        '  <li><a href="/languages/%s/review/">Review deck</a><span>Spaced repetition of the words and phrases, saved on this device only.</span></li>\n'
        '  </ul>\n'
        '  <p><a class="btn" href="/languages/%s/">%s starter pack</a> '
        '<a class="btn" href="/languages/">All languages</a></p>\n'
    ) % (esc_html(C["name"]), esc_html(C["name"]), esc_html(C["note"]), lessons,
         C["code"], C["name"], C["code"], len(C["QUIZ"]), C["code"], C["code"], C["name"])
    write_page("languages/%s/course/index.html" % C["code"], "../../../",
               "Learn %s — free course" % C["name"],
               "A free %s course: six lessons, a practice lab, a topic quiz and a spaced-repetition review deck — all in your browser." % C["name"],
               "languages/%s/course/" % C["code"],
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/%s/">%s</a> › Course'
               % (C["code"], esc_html(C["name"])),
               body, scripts=(), index=True)
    return "languages/%s/course/index.html" % C["code"]


def _explainer(C, kind):
    """Prose for the app pages.

    These pages are mostly a widget plus a note, which is honest but left them
    under the 250-word mark and made them look like filler to a reviewer (and
    to the AdSense "low value content" check, which is the reason this site was
    rejected the first time). Two short paragraphs that actually explain how
    the tool works fix that without padding.
    """
    n = esc_html(C["name"])
    if kind == "practice":
        return (
            '  <h2>How the %s practice drills work</h2>\n'
            '  <p>The drill shows one %s word or grammar point at a time and asks you to pick the meaning '
            'from four options. Every answer is explained, so a wrong one tells you why it was wrong rather '
            'than just marking it red, and the vocabulary comes from the same %s lessons on this site — '
            'nothing here is drawn from another course. Use the speaker button to hear the word before you '
            'answer; the computer voice is good enough to train the rhythm even where it clips a vowel.</p>\n'
            '  <h2>What the score means</h2>\n'
            '  <p>This is a recognition drill, not a fluency test: picking the right meaning is easier than '
            'producing the word, so a high score means you can read %s, not that you can speak it. Aim to '
            'finish a set without repeats, then come back the next day — the value is in the second pass, '
            'when the options look familiar and you have to remember rather than guess.</p>\n'
            % (n, n, n, n))
    return (
        '  <h2>How the %s review deck works</h2>\n'
        '  <p>Review is a small spaced-repetition deck: load it once and it holds a set of %s words and '
        'phrases from this course, then shows you each card again at growing intervals — today, in a few '
        'days, in a couple of weeks. Cards live in this browser only, so they follow the device, not an '
        'account, and clearing your browser data clears the deck.</p>\n'
        '  <h2>Using it well</h2>\n'
        '  <p>Answer out loud before you reveal the back — the deck is testing recall, not recognition. '
        'If a card keeps coming back, write the %s word in a sentence of your own; that is usually what '
        'makes it stick. Ten minutes a day is the whole routine, and skipping a day is fine: the schedule '
        'simply pushes the next card later rather than marking you down.</p>\n'
        % (n, n, n))


def build_practice(C):
    code = C["code"]
    body = (
        '  <h1>%s Practice <span style="display:inline-block;border-radius:999px;padding:2px 10px;font-size:.72rem;font-weight:700;color:#fff;background:#1a7f37;vertical-align:4px">Available</span></h1>\n'
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
    fc_html, fc_scripts = flashcard_section(code, C["name"])
    scripts = ["course-%s.js" % code, "practice-engine.js"] + fc_scripts
    if fc_html:
        body += fc_html + mount_script(code, C["name"], C["speech"])
    write_page("languages/%s/practice/index.html" % code, "../../../",
               "%s Practice — Vocabulary & Grammar Drills" % C["name"],
               "Free %s practice drills and flashcards: see a %s word or rule, pick the meaning, get the explanation. Computer voice playback, saved in your browser." % (C["name"], C["name"]),
               "languages/%s/practice/" % code,
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/%s/">%s</a> › Practice'
               % (code, esc_html(C["name"])),
               body + _explainer(C, "practice"),
               scripts=scripts, index=True)
    return "languages/%s/practice/index.html" % code


def build_quiz(C):
    code = C["code"]
    jsvar = C["jsvar"]
    name = esc(C["name"])
    quiz = C["QUIZ"]

    # Build a user-facing map from the repository quiz bank itself. It gives
    # learners an honest per-topic count and a direct route back to the lesson
    # that supplied each question, rather than implying that every topic has
    # 20 questions.
    topic_groups = {}
    for question in quiz:
        topic = str(question.get("topic") or "general")
        group = topic_groups.setdefault(topic, {"count": 0, "lessons": []})
        group["count"] += 1
        lesson_slug = question.get("lesson")
        if lesson_slug and lesson_slug not in group["lessons"]:
            group["lessons"].append(lesson_slug)

    lesson_by_slug = {lesson["slug"]: lesson for lesson in C["LESSONS"]}
    topic_rows = []
    for topic in sorted(topic_groups):
        group = topic_groups[topic]
        topic_label = topic.replace("_", " ").replace("-", " ").title()
        lesson_links = []
        for lesson_slug in group["lessons"]:
            lesson = lesson_by_slug.get(lesson_slug)
            if lesson:
                lesson_links.append(
                    '<a href="/languages/%s/lessons/%s/">%s</a>'
                    % (esc(code), esc(lesson_slug), esc(lesson["title"]))
                )
        count = group["count"]
        question_label = "question" if count == 1 else "questions"
        review_text = " · ".join(lesson_links) if lesson_links else "No source lesson is mapped yet."
        topic_rows.append(
            '<li><b>%s</b><span>%d %s<br>Review: %s</span></li>'
            % (esc(topic_label), count, question_label, review_text)
        )
    topic_map = "\n".join(topic_rows)

    # Use named literal tokens rather than positional %-formatting: the old
    # template accidentally shifted internal JS identifiers into visible copy
    # and put the language code in the quiz's runtime bindings.
    body = """  <h1>__NAME__ Topic Quiz <span style="display:inline-block;border-radius:999px;padding:2px 10px;font-size:.72rem;font-weight:700;color:#fff;background:#1a7f37;vertical-align:4px">Available</span></h1>
  <p class="lede">Practise with the __QUESTION_COUNT__ questions in the __NAME__ course bank. Choose a topic and a round size; each answer includes an explanation and a link to its source lesson.</p>
  <div class="row" style="gap:12px;flex-wrap:wrap;align-items:end">
    <div><label for="__CODE__-q-topic">Topic</label><br><select id="__CODE__-q-topic"></select></div>
    <div><label for="__CODE__-q-n">Round size</label><br><select id="__CODE__-q-n" disabled><option value="">Loading question counts…</option></select></div>
    <button type="button" class="btn" id="__CODE__-q-start" disabled>Start</button>
  </div>
  <p class="muted hint" style="font-size:.8rem;margin-top:8px">Question order is fixed for the day and changes on a later day. A shorter round may draw a different subset; an all-questions round uses the same topic bank in a different order.</p>
  <div id="__CODE__-q-body" style="margin-top:16px"></div>
  <h2>How the __NAME__ quiz works</h2>
  <p>The course bank currently contains __QUESTION_COUNT__ questions across __TOPIC_COUNT__ topics. The topic picker selects the question pool, and the round-size menu only offers lengths that pool can supply. After each answer, use the explanation and source-lesson link to repair a specific gap rather than repeating the same round without review.</p>
  <h2>Question bank by topic</h2>
  <p>Counts below are for the selected topic, not for the whole course. Choose “All available” for a complete pass through a smaller topic; its round may contain fewer than five questions because no extra questions are invented.</p>
  <ul class="linklist">
__TOPIC_MAP__
  </ul>
  <h2>Use a result to choose your next study step</h2>
  <p>Read the explanation, then open its linked lesson. If the same __NAME__ word or pattern trips you up again, write a fresh example before restarting. The score is feedback on recall from this small course bank; it is not a language-level placement or a fluency assessment.</p>
  <script>
  (function () {
    "use strict";
    function escText(s) {
      return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
    }
    function shuffle(a) {
      var o = a.slice();
      for (var i = o.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = o[i]; o[i] = o[j]; o[j] = t;
      }
      return o;
    }
    function dayShuffle(a, salt, when) {
      var d = when || new Date();
      var key = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0") + ":" + (salt || "");
      var h = 2166136261;
      for (var i = 0; i < key.length; i++) { h ^= key.charCodeAt(i); h = Math.imul(h, 16777619); }
      var s = h >>> 0;
      var rnd = function () {
        s |= 0; s = (s + 0x6D2B79F5) | 0;
        var t = Math.imul(s ^ (s >>> 15), 1 | s);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
      var o = a.slice();
      for (var j = o.length - 1; j > 0; j--) {
        var k = Math.floor(rnd() * (j + 1));
        var tmp = o[j]; o[j] = o[k]; o[k] = tmp;
      }
      return o;
    }

    var Q = [];
    var state = null;
    var topicSelect = document.getElementById("__CODE__-q-topic");
    var countSelect = document.getElementById("__CODE__-q-n");
    var startButton = document.getElementById("__CODE__-q-start");

    function questionsForTopic() {
      var topic = topicSelect.value;
      return Q.filter(function (q) { return q.topic === topic; });
    }
    function refreshRoundSizes() {
      var count = questionsForTopic().length;
      var choices = [5, 10, 20].filter(function (n) { return n < count; });
      var options = choices.map(function (n) {
        return '<option value="' + n + '">' + n + ' questions</option>';
      });
      if (count) options.push('<option value="all">All ' + count + ' available</option>');
      if (!options.length) options.push('<option value="">No questions available</option>');
      countSelect.innerHTML = options.join("");
      countSelect.disabled = !count;
      startButton.disabled = !count;
    }
    function startRound() {
      var pool = questionsForTopic();
      var requested = countSelect.value === "all" ? pool.length : parseInt(countSelect.value, 10);
      if (!pool.length || !requested || isNaN(requested)) {
        document.getElementById("__CODE__-q-body").innerHTML = '<p class="muted">No questions are available for this topic yet.</p>';
        return;
      }
      var use = dayShuffle(pool, "quiz:" + topicSelect.value).slice(0, Math.min(requested, pool.length));
      state = { i: 0, correct: 0, use: use, answered: false };
      renderQuestion();
    }
    function renderQuestion() {
      var box = document.getElementById("__CODE__-q-body");
      if (!state) { box.innerHTML = ""; return; }
      if (state.i >= state.use.length) {
        var pct = Math.round((state.correct / state.use.length) * 100);
        box.innerHTML = '<div class="note"><b>Round complete.</b> You got ' + state.correct + ' of ' + state.use.length + ' correct (' + pct + '%).' +
          '<p>Review any missed source lesson before choosing another round.</p>' +
          '<button type="button" class="btn" id="__CODE__-q-restart">Start this topic again</button></div>';
        box.querySelector("#__CODE__-q-restart").addEventListener("click", startRound);
        return;
      }
      state.answered = false;
      var q = state.use[state.i];
      var opts = shuffle((q.opts || []).slice());
      box.innerHTML = '<p class="muted">Question ' + (state.i + 1) + ' of ' + state.use.length + ' — ' + escText(q.topic) + '</p>' +
        '<p style="font-weight:700;font-size:1.05rem">' + escText(q.q) + '</p>' +
        opts.map(function (o, idx) {
          return '<button type="button" class="btn ghost" style="display:block;width:100%;text-align:left;margin:6px 0" data-opt="' + idx + '">' + escText(o) + '</button>';
        }).join("") +
        '<div id="__CODE__-q-fb" style="margin-top:10px"></div>';
      box.querySelectorAll("[data-opt]").forEach(function (button) {
        button.addEventListener("click", function () {
          if (state.answered) return;
          state.answered = true;
          box.querySelectorAll("[data-opt]").forEach(function (option) { option.disabled = true; });
          var chosen = opts[parseInt(button.getAttribute("data-opt"), 10)];
          var correct = chosen === q.a;
          if (correct) state.correct++;
          var feedback = box.querySelector("#__CODE__-q-fb");
          var lessonHref = q.lesson ? "/languages/__CODE__/lessons/" + encodeURIComponent(q.lesson) + "/" : "";
          var lessonLink = lessonHref ? '<p><a href="' + escText(lessonHref) + '">Review the source lesson</a></p>' : "";
          feedback.innerHTML = '<p style="font-weight:600;color:' + (correct ? "var(--green,#1a7f37)" : "var(--red,#b3261e)") + '">' +
            (correct ? "Correct." : "Not quite — the answer was “" + escText(q.a) + "”.") + '</p>' +
            '<p class="muted">' + escText(q.explain) + '</p>' + lessonLink +
            '<button type="button" class="btn" id="__CODE__-q-next">Next</button>';
          box.querySelector("#__CODE__-q-next").addEventListener("click", function () { state.i++; renderQuestion(); });
        });
      });
    }
    function init() {
      Q = (window.__JSVAR__ && window.__JSVAR__.quiz) || [];
      var topics = {};
      Q.forEach(function (q) { topics[q.topic] = true; });
      var names = Object.keys(topics).sort();
      topicSelect.innerHTML = names.map(function (topic) {
        return '<option value="' + escText(topic) + '">' + escText(topic.replace(/[_-]/g, " ").replace(/\b\w/g, function (ch) { return ch.toUpperCase(); })) + '</option>';
      }).join("");
      topicSelect.addEventListener("change", refreshRoundSizes);
      startButton.addEventListener("click", startRound);
      refreshRoundSizes();
    }
    if (window.__JSVAR__) init();
    else window.addEventListener("load", init);
  })();
  </script>
"""
    replacements = {
        "__NAME__": name,
        "__CODE__": esc(code),
        "__JSVAR__": jsvar,
        "__QUESTION_COUNT__": str(len(quiz)),
        "__TOPIC_COUNT__": str(len(topic_groups)),
        "__TOPIC_MAP__": topic_map,
    }
    for token, value in replacements.items():
        body = body.replace(token, value)

    write_page("languages/%s/quiz/index.html" % code, "../../../",
               "%s Quiz — Topic Questions with Explanations" % C["name"],
               "A free %s topic quiz with per-topic question counts, explanations and links to the source lessons." % C["name"],
               "languages/%s/quiz/" % code,
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/%s/">%s</a> › Quiz'
               % (code, esc(C["name"])),
               body, scripts=["course-%s.js" % code], index=True)
    return "languages/%s/quiz/index.html" % code

def build_review(C):
    code = C["code"]
    body = (
        '  <h1>%s Review <span style="display:inline-block;border-radius:999px;padding:2px 10px;font-size:.72rem;font-weight:700;color:#fff;background:#1a7f37;vertical-align:4px">Available</span></h1>\n'
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
    body = body + _explainer(C, "review")
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
    # merge: single-language rebuilds must not drop the other courses
    try:
        existing = json.load(open("data/courses.json", encoding="utf-8")).get("courses", [])
    except Exception:
        existing = []
    by_lang = {c["lang"]: c for c in existing}
    for c in summaries:
        by_lang[c["lang"]] = c
    manifest = {
        "generated": NOW,
        "policy": ("A language gets a course object only when real authored lessons + practice + quiz + "
                   "review exist. A completed course marks its language Available (still not Hindi-depth, still no "
                   "recorded audio). PRODUCTION remains Hindi only."),
        "courses": [by_lang[k] for k in sorted(by_lang)],
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


def build_sitemap_courses():
    """Regenerate sitemap-courses.xml from data/courses.json (all courses)."""
    try:
        courses = json.load(open("data/courses.json", encoding="utf-8")).get("courses", [])
    except Exception:
        courses = []
    urls = ["languages/"]
    for c in courses:
        code = c["lang"]
        try:
            m = load_course_data(code)
            slugs = [l["slug"] for l in m.LESSONS]
        except Exception:
            slugs = []
        urls.append("languages/%s/" % code)
        urls.append("languages/%s/course/" % code)
        for slug in slugs:
            urls.append("languages/%s/lessons/%s/" % (code, slug))
        urls += ["languages/%s/practice/" % code, "languages/%s/quiz/" % code,
                 "languages/%s/review/" % code]
    today = time.strftime("%Y-%m-%d", time.gmtime())
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml += ["  <url>", "    <loc>%s/%s</loc>" % (BASE, u),
                "    <lastmod>%s</lastmod>" % today,
                "    <changefreq>weekly</changefreq>", "    <priority>0.8</priority>", "  </url>"]
    xml.append("</urlset>")
    with open("sitemap-courses.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml) + "\n")
    print("sitemap-courses.xml: %d urls" % len(urls))


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
    build_sitemap_courses()


if __name__ == "__main__":
    main()
