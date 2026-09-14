#!/usr/bin/env python3
"""Phase 6 §6–§17 — generate the Hindi learning-product pages + decorate lessons.

Generates:
  /learn/hindi/review/            SRS review            (noindex)
  /learn/hindi/my-progress/       local progress        (noindex)
  /learn/hindi/practice/typing/   Roman→Devanagari      (index)
  /learn/hindi/practice/quiz/     topic quiz            (index)
  /learn/hindi/practice/worksheets/  printable sheets   (index)
  /learn/hindi/intermediate/      intermediate sequence (index)

Also (idempotently):
  · decorates the 15 lesson guides with the Phase 6 loop:
    mark-complete + save-offline slots, data-lesson-slug, and the
    shared js includes (srs / progress / audio / offline),
  · adds the new practice tools + review + progress to the Hindi hub
    navigation (and fixes a pre-existing `../practice//` double slash).

Run: python3 tools/build-hindi-pages.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop"

LESSONS = [
    "hindi-alphabet-for-beginners", "how-to-say-hello-in-hindi", "hindi-sentence-structure",
    "aap-tum-tu-hindi", "common-hindi-mistakes", "hindi-days-months-time",
    "hindi-family-words", "hindi-gender-masculine-feminine", "hindi-numbers-1-to-100",
    "hindi-or-urdu-difference", "hindi-phrases-for-travel", "hindi-verbs-present-past-future",
    "learn-hindi-from-bollywood", "learn-hindi-online-guide", "write-your-name-in-hindi",
]

CORE_STYLE = """
.art{max-width:760px;margin:0 auto;padding:0 20px 60px}
.art h1{font-size:2rem;line-height:1.25;margin:26px 0 10px}
.art .meta{color:var(--muted);font-size:.86rem;margin:0 0 26px}
.art h2{font-size:1.28rem;margin:34px 0 12px;padding-top:6px}
.art p,.art li{line-height:1.75}
.art ul,.art ol{padding-left:22px}
.art li{margin:7px 0}
.crumb{font-size:.84rem;color:var(--muted);padding:18px 0 0}
.crumb a{color:var(--muted)}
.lede{color:var(--ink-2);font-size:1.05rem;line-height:1.7;margin:0 0 22px}
.linklist{list-style:none;padding:0;margin:12px 0 0}
.linklist li{padding:10px 0;border-bottom:1px solid var(--line)}
.linklist li:last-child{border-bottom:0}
.linklist a{font-weight:600}
.linklist span{display:block;color:var(--muted);font-size:.87rem;margin-top:2px;line-height:1.5}
.note{background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:12px;padding:14px 16px;margin:14px 0;font-size:.94rem;color:var(--ink-2)}
.btn{margin:6px 6px 6px 0}
"""


def head(title, desc, url, up, index=True, extra_style=""):
    robots = "index, follow, max-snippet:-1, max-image-preview:large" if index else "noindex, follow"
    return """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="google-site-verification" content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" />
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s | EkGuru</title>
<meta name="description" content="%s">
<meta name="author" content="EkGuru">
<meta name="robots" content="%s">
<link rel="canonical" href="%s/%s">
<meta property="og:type" content="article">
<meta property="og:title" content="%s | EkGuru">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s/%s">
<meta property="og:image" content="%s/images/og-cover.jpg">
<meta property="og:site_name" content="EkGuru">
<meta property="article:published_time" content="2026-09-12">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<link rel="icon" href="%simages/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="%simages/apple-touch-icon.png">
<link rel="manifest" href="%smanifest.webmanifest">
<meta name="theme-color" content="#4f32d9">
<link rel="stylesheet" href="%scss/style.min.css">
<link rel="stylesheet" href="%scss/storybook.css">
<style>%s%s</style>
</head>
<body>
<div class="art">
""" % (title, desc, robots, BASE, url, title, desc, BASE, url, BASE, title, desc,
       up, up, up, up, up, CORE_STYLE, extra_style)


def foot(up, scripts=()):
    s = ""
    for src in scripts:
        s += '\n<script src="%sjs/%s" defer></script>' % (up, src)
    return """
</div>
<!-- ekguru:trust-footer:start -->
<footer class="pw-ftr">
  <nav aria-label="Site information">
    <a href="%s">Home</a>
    <a href="%sabout/">About</a>
    <a href="%scontact/">Contact</a>
    <a href="%sprivacy/">Privacy</a>
    <a href="%sterms/">Terms</a>
    <a href="%sdisclaimer/">Disclaimer</a>
  </nav>
  <p>
  © 2026 EkGuru — One Student. One Goal. One Guru.<br>
  Written and maintained by Prakash. Hindi lessons with native-speaking tutors, one to one.
  </p>
</footer>
<!-- ekguru:trust-footer:end -->
</body>
</html>
<script src="%sjs/site-config.js" defer></script>
<script src="%sjs/analytics.js" defer></script>
<script src="%sjs/toast.js" defer></script>
<!-- ekguru:recovery:start -->
<script src="%sjs/recovery.js" defer></script>
<!-- ekguru:recovery:end -->
%s
<script src="%sjs/storybook.js" defer></script>
<script defer>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("%ssw.js").catch(function () {});
  });
}
</script>
""" % (up, up, up, up, up, up, up, up, up, up, s, up, up)


def write_page(path, up, title, desc, url, crumb, body, scripts=(), index=True,
               extra_style=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html = head(title, desc, url, up, index=index, extra_style=extra_style)
    html += '    <p class="crumb">%s</p>\n' % crumb
    html += body
    html += foot(up, scripts)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ---------------------------------------------------------------------------
# §6  REVIEW
# ---------------------------------------------------------------------------
def sb_band(dev, en):
    return ('  <div class="sb-band"><span class="dev">%s</span>%s</div>\n') % (dev, en)

def sb_hero(up, file, alt, floats, caption):
    fl = []
    slots = [("top:8%;left:6%", "2rem", "-1s"), ("top:14%;right:8%", "1.6rem", "-3s"),
             ("bottom:24%;left:12%", "1.4rem", "-5s")]
    for i, t in enumerate(floats[:3]):
        pos, size, delay = slots[i % 3]
        fl.append('<span class="sb-float" style="%s;font-size:%s;animation-delay:%s">%s</span>'
                  % (pos, size, delay, t))
    return ('  <figure class="sb-hero">\n  <img src="%simages/%s" alt="%s" width="1536" height="1024" fetchpriority="high">\n  %s\n'
            '  <figcaption>%s</figcaption>\n  </figure>\n') % (up, file, alt, "\n  ".join(fl), caption)


def review_page():
    up = "../../../"
    body = """  <h1>Hindi Review — spaced repetition</h1>
  <p class="lede">A simple, transparent review system for the words and ideas you saved. It lives entirely in this browser.</p>
""" + sb_band("दोहराओ", "Repeat it till it sticks.") + """
  <div class="note"><b>How it works.</b> Each card is shown again on a schedule that grows with each correct answer. Four buttons: <b>Again</b> (starts over), <b>Hard</b>, <b>Good</b>, <b>Easy</b>. This is a simple SM-2-style schedule — not scientific perfection and not “AI personalisation”.</div>
  <div id="srs-stats" style="margin:12px 0;font-weight:600"></div>
  <div id="srs-card" style="border:1px solid var(--line);border-radius:14px;padding:20px;background:var(--card,#fff)"></div>
  <div id="srs-empty" style="display:none" class="note">No cards due right now. Add cards from any lesson (look for the “＋ Review” buttons), or load the starter deck.</div>
  <div style="margin-top:14px">
    <button type="button" class="btn" id="srs-seed">Load starter deck</button>
    <button type="button" class="btn ghost" id="srs-reset">Remove all cards</button>
  </div>
  <p class="muted" style="margin-top:14px">Cards are saved on this device only — no account, no upload, no sync.</p>
"""
    scripts = ["hindi-quiz-bank.js", "practice-bank.js", "hindi-srs.js", "hindi-audio.js"]
    extra = """
#srs-card .prompt{font-size:1.15rem;font-weight:700;margin-bottom:14px}
#srs-card .answer{display:none;background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:10px;padding:12px 14px;margin:0 0 14px;color:var(--ink-2)}
#srs-card .rates{display:flex;gap:8px;flex-wrap:wrap}
.hi-listen{display:inline-flex;align-items:center;gap:5px;margin:0 0 0 8px;padding:4px 10px;font-size:.82rem;line-height:1.4;border-radius:999px;border:1px solid var(--line);background:var(--bg-soft);color:var(--ink);cursor:pointer;vertical-align:middle}
.hi-listen.playing{background:var(--brand);border-color:var(--brand);color:#fff}
"""
    write_page("learn/hindi/review/index.html", up, "Hindi Review — spaced repetition",
               "Review the Hindi words and phrases you saved, on a simple spaced-repetition schedule that lives in your browser.",
               "learn/hindi/review/",
               '<a href="../../../">EkGuru</a> › <a href="../../">Learn Hindi</a> › <a href="../">Hindi</a> › Review',
               body, scripts=scripts, index=False, extra_style=extra)
    # the review UI is driven inline in the page — append it
    p = "learn/hindi/review/index.html"
    h = open(p, encoding="utf-8").read()
    h = h.replace("</body>", REVIEW_JS + "\n</body>")
    open(p, "w", encoding="utf-8").write(h)


REVIEW_JS = """<script>
(function () {
  "use strict";
  function boot() {
  var S = window.EkGuruSRS, queue = [], card = null;
  function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
  function deva(t){var m=String(t||"").match(/[\u0900-\u097F]+/);return m?m[0]:null;}
  function sayWord() {
    var w = deva(card.target) || deva(card.prompt);
    return w || null;
  }
  function paint() {
    var st = document.getElementById("srs-stats");
    st.textContent = S.count() + " cards · " + S.dueCount() + " due";
    var box = document.getElementById("srs-card");
    var empty = document.getElementById("srs-empty");
    if (!queue.length) { queue = S.due(); }
    card = queue.shift() || null;
    if (!card) { box.innerHTML = ""; empty.style.display = "block"; return; }
    empty.style.display = "none";
    var say = sayWord();
    box.innerHTML =
      '<p class="prompt">' + esc(card.prompt) +
        (say ? '<button type="button" class="hi-listen" id="srs-say" aria-label="Listen (computer voice)" aria-pressed="false"><span aria-hidden="true">🔊</span> Listen</button>' : "") +
      '</p>' +
      '<div class="answer" id="srs-a"><b>' + esc(card.answer) + '</b></div>' +
      '<button type="button" class="btn ghost" id="srs-show">Show answer</button>' +
      '<div class="rates" id="srs-rates" style="display:none;margin-top:10px">' +
      '<button type="button" class="btn ghost" data-r="again">Again</button>' +
      '<button type="button" class="btn ghost" data-r="hard">Hard</button>' +
      '<button type="button" class="btn" data-r="good">Good</button>' +
      '<button type="button" class="btn" data-r="easy">Easy</button></div>';
    var sayBtn = box.querySelector("#srs-say");
    if (sayBtn && say) {
      sayBtn.addEventListener("click", function (e) {
        e.preventDefault();
        var A = window.EkGuruHindiAudio;
        if (A && A.supported()) A.speak(say, sayBtn, "hi-IN");
      });
    }
    box.querySelector("#srs-show").addEventListener("click", function () {
      box.querySelector("#srs-a").style.display = "block";
      box.querySelector("#srs-rates").style.display = "flex";
      this.style.display = "none";
    });
    box.querySelectorAll("[data-r]").forEach(function (b) {
      b.addEventListener("click", function () { S.review(card.card_id, b.getAttribute("data-r")); paint(); });
    });
  }
  document.getElementById("srs-seed").addEventListener("click", function () {
    var r = S.seedStarter(); queue = []; paint();
    if (window.EkGuruToast) window.EkGuruToast.show(r.added + " cards added (from quiz bank + vocabulary).");
  });
  document.getElementById("srs-reset").addEventListener("click", function () {
    S.all().forEach(function (c) { S.remove(c.card_id); });
    queue = []; /* v31 fix: drop the stale in-memory queue so the empty state
                   renders instead of a phantom card the user just removed */
    paint();
  });
  paint();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else { boot(); }
})();
</script>
"""


# ---------------------------------------------------------------------------
# §8  MY PROGRESS
# ---------------------------------------------------------------------------
def progress_page():
    up = "../../../"
    body = """  <h1>My Hindi — progress on this device</h1>
  <p class="lede">Your own checklist: what you have read, finished and reviewed. <b>Saved on this device only</b> — no account, no upload, no cross-device sync.</p>
""" + sb_band("प्रगति", "Your journey, on this device.") + """
  <div id="my-hindi"></div>
  <div style="margin-top:18px">
    <button type="button" class="btn" id="mp-export">Export JSON</button>
    <button type="button" class="btn ghost" id="mp-import">Import JSON</button>
    <input type="file" id="mp-file" accept="application/json" style="display:none">
    <button type="button" class="btn ghost" id="mp-reset">Reset everything</button>
  </div>
  <p class="muted" style="margin-top:12px">Exports a JSON file you can keep or import back on another browser. Import accepts only EkGuru Hindi progress files and never touches your booking data.</p>
"""
    scripts = ["hindi-srs.js", "hindi-progress.js"]
    write_page("learn/hindi/my-progress/index.html", up, "My Hindi — progress on this device",
               "Your local Hindi learning checklist: lessons opened and completed, quiz scores, review cards and paths — saved only in this browser.",
               "learn/hindi/my-progress/",
               '<a href="../../../">EkGuru</a> › <a href="../../">Learn Hindi</a> › <a href="../">Hindi</a> › My Hindi',
               body, scripts=scripts, index=False)
    p = "learn/hindi/my-progress/index.html"
    h = open(p, encoding="utf-8").read()
    h = h.replace("</body>", PROGRESS_JS + "\n</body>")
    open(p, "w", encoding="utf-8").write(h)


PROGRESS_JS = """<script>
(function () {
  "use strict";
  function boot() {
  var P = window.EkGuruProgress;
  function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
  function dl(name, text, mime) {
    var b = new Blob([text], {type:(mime||"text/plain")+";charset=utf-8"});
    var u = URL.createObjectURL(b); var a = document.createElement("a");
    a.href = u; a.download = name; document.body.appendChild(a); a.click();
    document.body.removeChild(a); setTimeout(function(){URL.revokeObjectURL(u);},1000);
  }
  function paint() {
    var s = P.snapshot();
    var rows = [];
    rows.push('<div class="note"><b>Summary.</b> ' + s.lessonsOpened + ' lessons opened · ' +
      s.lessonsCompleted + ' marked complete · ' + s.reviewCards + ' review cards (' + s.reviewDue +
      ' due) · ' + s.pathsStarted + ' paths started.</div>');
    if (s.opened.length) {
      rows.push('<h2>Recently opened</h2><ul class="linklist">' + s.opened.slice(0,8).map(function(o){
        return '<li><span>' + esc(o.title) + '</span></li>'; }).join('') + '</ul>');
    }
    if (Object.keys(s.completed).length) {
      rows.push('<h2>Marked complete</h2><ul class="linklist">' +
        Object.keys(s.completed).map(function(k){return '<li><span>' + esc(s.completed[k].title) + '</span></li>';}).join('') + '</ul>');
    }
    if (Object.keys(s.quizzes).length) {
      rows.push('<h2>Quiz attempts</h2><ul class="linklist">' + Object.keys(s.quizzes).map(function(k){
        var q = s.quizzes[k]; return '<li><b>' + esc(k) + '</b><span>' + q.attempts + ' attempt(s) · best ' + q.best + ' / ' + q.total + '</span></li>'; }).join('') + '</ul>');
    }
    if (!s.lessonsOpened && !Object.keys(s.completed).length && !s.reviewCards) {
      rows.push('<div class="note">Nothing recorded yet. Open a lesson, mark one complete, or add a card to review — it will appear here.</div>');
    }
    document.getElementById("my-hindi").innerHTML = rows.join("");
  }
  document.getElementById("mp-export").addEventListener("click", function () {
    dl("ekguru-hindi-progress.json", P.exportJSON(), "application/json");
  });
  document.getElementById("mp-import").addEventListener("click", function () {
    document.getElementById("mp-file").click();
  });
  document.getElementById("mp-file").addEventListener("change", function (e) {
    var f = e.target.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function () { var res = P.importJSON(r.result); paint();
      if (window.EkGuruToast) window.EkGuruToast.show(res.ok ? "Imported." : res.error); };
    r.readAsText(f);
  });
  document.getElementById("mp-reset").addEventListener("click", function () {
    if (confirm("Clear all your Hindi progress on this device?")) { P.reset(); paint(); }
  });
  paint();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else { boot(); }
})();
</script>
"""


# ---------------------------------------------------------------------------
# PRACTICE HUB — the page the practice breadcrumb "Practice" points at.
# ---------------------------------------------------------------------------
def practice_hub():
    up = "../../../"
    body = """  <h1>Hindi Practice</h1>
  <p class="lede">Three small, honest practice tools that work in your browser — a typing trainer, a topic quiz and printable worksheets — plus the review deck and your local progress.</p>
""" + sb_band("अभ्यास", "Practice makes permanent.") + """
  <ul class="linklist">
    <li><a href="typing/">Hindi Typing Trainer</a><span>Roman prompt → type it in Devanagari, with harmless formatting differences accepted.</span></li>
    <li><a href="quiz/">Hindi Topic Quiz</a><span>Pick a topic and level, answer 5–15 questions, get an explanation with every answer.</span></li>
    <li><a href="worksheets/">Hindi Worksheets</a><span>Printable prompts with a writing space and an optional answer section.</span></li>
    <li><a href="conversation/">Hindi Conversation Practice</a><span>Deterministic scenario simulator — read a line, pick the reply. Rule-based, clearly not AI.</span></li>
    <li><a href="../review/">Hindi Review</a><span>Spaced repetition for the words and ideas you save.</span></li>
    <li><a href="../my-progress/">My Hindi</a><span>Your local checklist — saved on this device only.</span></li>
  </ul>
  <div class="note">Nothing here needs an account. Your answers and progress stay in this browser; nothing is uploaded.</div>
"""
    write_page("learn/hindi/practice/index.html", up, "Hindi Practice — typing, quiz, worksheets",
               "Free Hindi practice tools that run in your browser: a Roman-to-Devanagari typing trainer, a topic quiz with explanations, and printable worksheets.",
               "learn/hindi/practice/",
               '<a href="../../../">EkGuru</a> › <a href="../../">Learn Hindi</a> › <a href="../">Hindi</a> › Practice',
               body)


# ---------------------------------------------------------------------------
# §11 TYPING · §12 QUIZ · §13 WORKSHEETS
# ---------------------------------------------------------------------------
def tool_pages():
    up = "../../../../"
    crumb_base = ('<a href="../../../../">EkGuru</a> › <a href="../../../">Learn Hindi</a> › '
                  '<a href="../../">Hindi</a> › <a href="../">Practice</a> › ')

    write_page(
        "learn/hindi/practice/typing/index.html", up, "Hindi Typing Trainer — Roman to Devanagari",
        "Practise writing Hindi: read a Roman prompt (namaste), type the word in Devanagari (नमस्ते), and get instant feedback with harmless formatting differences accepted.",
        "learn/hindi/practice/typing/", crumb_base + "Typing",
        """  <h1>Hindi Typing Trainer — Roman to Devanagari</h1>
  <p class="lede">See a Roman prompt, type the word in Devanagari. Small differences in spacing or punctuation are accepted as “minor format”, not marked wrong.</p>
""" + sb_band("लिखो", "Type it in Devanagari.") + """
  <div id="typing-app"></div>
  <div class="note">This trainer checks your typed Devanagari against a curated word list from the lessons. It is not a full transliteration engine and makes no claim to be one.</div>
""", scripts=["hindi-fuzzy.js", "hindi-tools.js"])

    write_page(
        "learn/hindi/practice/quiz/index.html", up, "Hindi Topic Quiz",
        "Free Hindi quiz: pick a topic and level, answer 5, 10 or 15 multiple-choice questions from the lesson bank, and get an explanation with every answer.",
        "learn/hindi/practice/quiz/", crumb_base + "Quiz",
        """  <h1>Hindi Topic Quiz</h1>
  <p class="lede">Pick a topic and level, then answer 5, 10 or 15 questions. Every answer comes with an explanation and a link back to the source lesson.</p>
""" + sb_band("बताओ", "Answer with reasons.") + """
  <div id="quiz-app"></div>
  <div class="note">The score is a recognition score, not a fluency measure — nothing here is a certified test.</div>
""", scripts=["hindi-quiz-bank.js", "hindi-progress.js", "hindi-tools.js"])

    write_page(
        "learn/hindi/practice/worksheets/index.html", up, "Hindi Worksheets — printable practice",
        "Make a printable Hindi worksheet: choose a topic, pick 5–15 prompts, print it with a writing space and an optional answer section. Free, no download buttons.",
        "learn/hindi/practice/worksheets/", crumb_base + "Worksheets",
        """  <h1>Hindi Worksheets — printable practice</h1>
  <p class="lede">Build a worksheet from the quiz bank: choose a topic and a number of prompts, then print. Answers are included at the end unless you turn them off.</p>
""" + sb_band("काग़ज़", "Print it, write on it.") + """
  <div id="ws-app"></div>
""", scripts=["hindi-quiz-bank.js", "hindi-tools.js"])


# ---------------------------------------------------------------------------
# §21 CONVERSATION — deterministic scenario simulator (Phase 7C)
# ---------------------------------------------------------------------------
CONV_CSS = """
.conv-tag{display:inline-block;background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:999px;padding:2px 10px;font-size:.72rem;font-weight:700;margin:0 0 12px}
.conv-title{margin:4px 0 6px}
.conv-context{margin:0 0 14px}
.conv-npc{background:var(--card,#fff);border:1px solid var(--line);border-left:4px solid var(--accent,#b26a00);border-radius:10px;padding:12px 14px;margin:0 0 12px}
.conv-npc-tag{display:block;font-size:1.15rem;font-weight:700}
.conv-roman{display:block;color:var(--muted);font-size:.9rem}
.conv-en{display:block;font-size:.9rem;color:var(--ink-2)}
.conv-prompt{font-weight:600;margin:0 0 8px}
.conv-choices{display:flex;flex-direction:column;gap:8px;margin:0 0 12px}
.conv-choice{text-align:left;display:flex;flex-direction:column;align-items:flex-start}
.conv-choice .conv-roman{font-size:.82rem}
.conv-choice .conv-en{font-size:.8rem}
.conv-vocab{display:block;margin-top:8px;font-size:.85rem;color:var(--ink-2)}
.conv-fb{margin-top:12px}
"""


def conversation_page():
    up = "../../../../"
    crumb_base = ('<a href="../../../../">EkGuru</a> › <a href="../../../">Learn Hindi</a> › '
                  '<a href="../../">Hindi</a> › <a href="../">Practice</a> › ')
    body = """  <h1>Hindi Conversation Practice</h1>
  <p class="lede">A deterministic conversation simulator: you read a line, pick the reply, and get the reasoning behind the right answer. Every line is authored, basic, reviewed Hindi — a rule-based state machine, <b>not AI</b>.</p>
""" + sb_band("बातचीत", "Pick the reply, learn the why.") + """
  <div class="note"><b>Honest scope.</b> This teaches the shape of a conversation (greet → reply → close). It cannot listen to your pronunciation and it is not a live tutor — for real speaking practice, book a one-to-one lesson.</div>
  <div id="conv-app"><p class="muted">Loading scenarios…</p></div>
  <script defer>
  (function(){
    var el=document.getElementById("conv-app");
    if(!el)return;
    function whenReady(cb){
      if(window.EkGuruConversation){cb(window.EkGuruConversation);return;}
      var n=0,t=setInterval(function(){
        if(window.EkGuruConversation){clearInterval(t);cb(window.EkGuruConversation);}
        else if(++n>40){clearInterval(t);el.innerHTML='<p class="muted">Conversation practice is unavailable right now.</p>';}
      },100);
    }
    whenReady(function(C){
      C.ready().then(function(){
        var list=C.list();
        var html='<p class="muted">Choose a scenario:</p><div class="conv-choices">';
        list.forEach(function(s){
          html+='<button type="button" class="btn conv-choice" data-sc="'+s.id+'"><span>'+s.title+'</span>'
            +'<span class="conv-roman">'+s.level+' · goal: '+s.goal+'</span></button>';
        });
        html+='</div><div id="conv-stage"></div>';
        el.innerHTML=html;
        el.querySelectorAll("[data-sc]").forEach(function(b){
          b.addEventListener("click",function(){
            C.mount(document.getElementById("conv-stage"), b.getAttribute("data-sc"));
            b.scrollIntoView({behavior:"smooth",block:"start"});
          });
        });
      }).catch(function(){
        el.innerHTML='<p class="muted">Conversation practice is unavailable right now. The rest of this page works normally.</p>';
      });
    });
  })();
  </script>
"""
    write_page("learn/hindi/practice/conversation/index.html", up,
               "Hindi Conversation Practice — deterministic scenarios",
               "Practise basic Hindi conversations: read a line, pick the right reply, and see why. A deterministic, rule-based simulator — clearly not AI, no listening required.",
               "learn/hindi/practice/conversation/", crumb_base + "Conversation",
               body, scripts=["conversation-engine.js", "hindi-progress.js"],
               extra_style=CONV_CSS)


# ---------------------------------------------------------------------------
# §17 INTERMEDIATE
# ---------------------------------------------------------------------------
def intermediate_page():
    up = "../../../"
    body = """  <h1>Intermediate Hindi — assembled from real content</h1>
  <p class="lede">There is no invented “intermediate textbook” here. This is a sequence built from the genuinely intermediate material EkGuru already has: register and politeness, the Hindi–Urdu split, learner mistakes, verb tenses, and Bollywood as a learning tool.</p>
""" + sb_hero(up, "level-intermediate.jpg", "Storybook bazaar: fabric stalls, spices and a rickshaw", ["आप", "तुम", "तू"], "Politeness, tenses, and the real split.") + """
  <h2>Who this is for</h2>
  <p>You can read Devanagari and hold a basic conversation. You want to sound more natural and understand the choices real speakers make.</p>
  <h2>What you will be able to do</h2>
  <p>Choose the right level of politeness, understand why Hindi and Urdu overlap, stop making the mistakes that mark you as a learner, and start learning from the films and speech around you.</p>
  <h2>The sequence</h2>
  <ol class="linklist">
    <li><a href="../../aap-tum-tu-hindi/">Aap, Tum or Tu — Getting Politeness Right in Hindi</a><span>Hindi has three words for “you”, and choosing wrong can be genuinely rude.</span></li>
    <li><a href="../../hindi-verbs-present-past-future/">Hindi Verbs — Present, Past and Future</a><span>Every tense you need to hold a conversation, including the ne rule.</span></li>
    <li><a href="../../hindi-or-urdu-difference/">Hindi vs Urdu — The Real Difference</a><span>Why the two languages are treated as separate when speakers understand each other.</span></li>
    <li><a href="../../common-hindi-mistakes/">10 Mistakes Every Hindi Learner Makes</a><span>The errors that mark you out as a learner, and the fix for each.</span></li>
    <li><a href="../../learn-hindi-from-bollywood/">Learning Hindi from Bollywood</a><span>Films are a genuinely good way to learn — if you pick the right ones and use them properly.</span></li>
  </ol>
  <h2>Practice</h2>
  <ul class="linklist">
    <li><a href="../practice/quiz/">Hindi Topic Quiz</a><span>Multiple-choice questions with explanations, drawn from the lesson bank.</span></li>
    <li><a href="../practice/typing/">Hindi Typing Trainer</a><span>Write what you hear in Roman as Devanagari.</span></li>
    <li><a href="../review/">Hindi Review</a><span>Spaced repetition for the words and ideas you save.</span></li>
  </ul>
  <h2>Next step</h2>
  <p>When the structured lessons feel easy, the honest next step is conversation with a native speaker — <a href="../../../find-tutors.html">find a tutor</a> who will push you past the plateau.</p>
"""
    write_page("learn/hindi/intermediate/index.html", up, "Intermediate Hindi — assembled from real content",
               "An honest intermediate Hindi sequence built from EkGuru's existing content: politeness, verbs, Hindi vs Urdu, learner mistakes and learning from Bollywood.",
               "learn/hindi/intermediate/",
               '<a href="../../../">EkGuru</a> › <a href="../../">Learn Hindi</a> › <a href="../">Hindi</a> › Intermediate',
               body)


# ---------------------------------------------------------------------------
# decorate lessons with the Phase 6 loop
# ---------------------------------------------------------------------------
def decorate_lessons():
    changed = 0
    for slug in LESSONS:
        p = os.path.join("learn", slug, "index.html")
        if not os.path.exists(p):
            continue
        h = open(p, encoding="utf-8").read()
        orig = h
        # 1) data-lesson-slug on body
        if 'data-lesson-slug=' not in h:
            h = re.sub(r'<body([^>]*)>', lambda m: '<body data-lesson-slug="%s"%s>' % (slug, m.group(1)), h, count=1)
        # 2) mark-complete + offline slots right after the <h1>...</h1>
        if 'id="lesson-complete"' not in h:
            h = re.sub(r'(<h1[^>]*>.*?</h1>)', r'\1\n  <div id="lesson-complete"></div>\n  <div id="offline-ctl"></div>', h, count=1, flags=re.S)
        # 3) shared js includes before site-config.js
        if 'js/hindi-srs.js' not in h:
            h = h.replace('<script src="../../js/site-config.js" defer>',
                          '<script src="../../js/hindi-srs.js" defer></script>\n'
                          '<script src="../../js/hindi-progress.js" defer></script>\n'
                          '<script src="../../js/hindi-audio.js" defer></script>\n'
                          '<script src="../../js/hindi-offline.js" defer></script>\n'
                          '<script src="../../js/toast.js" defer></script>\n'
                          '<script src="../../js/site-config.js" defer>', 1)
        elif 'js/toast.js' not in h:
            # v31 fix: feedback layer (toast.js) was missing on lessons, so the
            # "＋ Review" button added cards silently. Add it without re-injecting
            # the whole Phase 6 block.
            h = h.replace('<script src="../../js/site-config.js" defer>',
                          '<script src="../../js/toast.js" defer></script>\n'
                          '<script src="../../js/site-config.js" defer>', 1)
        # 4) storybook visuals (v139): shared CSS + interactions, idempotent
        if 'css/storybook.css' not in h:
            h = h.replace('<link rel="stylesheet" href="../../css/style.min.css">',
                          '<link rel="stylesheet" href="../../css/style.min.css">\n'
                          '<link rel="stylesheet" href="../../css/storybook.css">', 1)
        if 'js/storybook.js' not in h:
            h = h.replace('<script src="../../js/site-config.js" defer>',
                          '<script src="../../js/storybook.js" defer></script>\n'
                          '<script src="../../js/site-config.js" defer>', 1)
        if h != orig:
            open(p, "w", encoding="utf-8").write(h)
            changed += 1
    return changed


def update_hub_nav():
    p = "learn/hindi/index.html"
    h = open(p, encoding="utf-8").read()
    orig = h
    changed = False

    # Phase 7C: the intermediate page exists (built in Phase 6) but the hub still
    # says "No Intermediate page yet" and nothing links to it — fix both so the
    # page is discoverable (de-orphans /learn/hindi/intermediate/).
    m = re.search(r'<p class="note">No Intermediate or Advanced page yet.*?</p>', h, re.S)
    if m:
        repl = ('<p class="note">There is now an <a href="intermediate/">intermediate sequence</a> — '
                'assembled from the genuinely intermediate material the site already has: register and '
                'politeness, the Hindi–Urdu split, learner mistakes, verb tenses, and Bollywood. '
                'There is still no Advanced page: we will not ship an empty level.</p>')
        h = h.replace(m.group(0), repl)
        changed = True

    # fix double slash bug
    h = h.replace('href="../practice//"', 'href="../practice/"')
    # add new tools after the existing practice-labs linklist items (before </ul>)
    if 'practice/quiz/' not in h:
        add = ('    <li><a href="practice/quiz/">Hindi Topic Quiz</a>'
               '<span>Multiple-choice questions from the lesson bank, with explanations.</span></li>\n'
               '    <li><a href="practice/typing/">Hindi Typing Trainer</a>'
               '<span>Roman prompt → type it in Devanagari.</span></li>\n'
               '    <li><a href="practice/worksheets/">Hindi Worksheets</a>'
               '<span>Printable prompts with writing space and answers.</span></li>\n'
               '    <li><a href="practice/conversation/">Hindi Conversation Practice</a>'
               '<span>Deterministic scenario simulator — rule-based, not AI.</span></li>\n'
               '    <li><a href="review/">Hindi Review</a>'
               '<span>Spaced repetition for the words you save.</span></li>\n'
               '    <li><a href="my-progress/">My Hindi</a>'
               '<span>Your local progress checklist (this device only).</span></li>\n')
        # insert before the last </ul> of the Practice labs section
        idx = h.find('<h2>Practice labs</h2>')
        if idx > 0:
            end = h.find('</ul>', idx)
            h = h[:end] + add + h[end:]
            changed = True
    # Phase 7C: add the conversation link on its own (idempotent)
    if 'practice/conversation/' not in h:
        add = ('    <li><a href="practice/conversation/">Hindi Conversation Practice</a>'
               '<span>Deterministic scenario simulator — rule-based, not AI.</span></li>\n')
        idx = h.find('<a href="review/">Hindi Review</a>')
        if idx > 0:
            # insert before the <li> that holds this review link
            li_start = h.rfind('<li>', 0, idx)
            h = h[:li_start] + add + h[li_start:]
            changed = True
    if changed and h != orig:
        open(p, "w", encoding="utf-8").write(h)
    return changed


def main():
    made = []
    review_page(); made.append("learn/hindi/review/index.html")
    progress_page(); made.append("learn/hindi/my-progress/index.html")
    practice_hub(); made.append("learn/hindi/practice/index.html")
    tool_pages()
    conversation_page(); made.append("learn/hindi/practice/conversation/index.html")
    made += ["learn/hindi/practice/typing/index.html",
             "learn/hindi/practice/quiz/index.html",
             "learn/hindi/practice/worksheets/index.html"]
    intermediate_page(); made.append("learn/hindi/intermediate/index.html")
    n_lessons = decorate_lessons()
    nav = update_hub_nav()
    print("generated pages:")
    for m in made:
        print("  ", m)
    print("decorated lessons:", n_lessons, "| hub nav updated:", nav)


if __name__ == "__main__":
    main()
