/* =========================================================
   EkGuru — HINDI PRACTICE TOOLS  (v1)
   ---------------------------------------------------------
   Three small, dependency-free tools sharing the quiz bank and
   the fuzzy helpers:

     · TYPING TRAINER  (§11) — Roman prompt → learner types
       Devanagari. Normalises harmless Unicode/space/punct
       differences; states: correct / minor-format / incorrect.
     · TOPIC QUIZ      (§12) — topic + level + 5/10/15 questions
       from the canonical bank; score + explanations + retry +
       link back to the source lesson. Score is NOT fluency.
     · WORKSHEETS      (§13) — client-side printable worksheet
       (prompts + writing space + optional answers). Real
       window.print(); no fake download buttons.

   Mounted automatically from #typing-app / #quiz-app / #ws-app.
   ========================================================= */
(function () {
  "use strict";

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function shuffle(a) {
    var out = a.slice();
    for (var i = out.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  /* ---------- curated typing data (from real lesson content) ---------- */
  var TYPING = [
    ["namaste", "नमस्ते"], ["aap", "आप"], ["tum", "तुम"], ["kaise", "कैसे"],
    ["kya", "क्या"], ["shukriya", "शुक्रिया"], ["dhanyavaad", "धन्यवाद"],
    ["paani", "पानी"], ["roti", "रोटी"], ["chai", "चाय"], ["ghar", "घर"],
    ["dost", "दोस्त"], ["khaana", "खाना"], ["pyaar", "प्यार"], ["ek", "एक"],
    ["do", "दो"], ["teen", "तीन"], ["sau", "सौ"], ["subah", "सुबह"],
    ["shaam", "शाम"], ["aaj", "आज"], ["kal", "कल"], ["chacha", "चाचा"],
    ["maama", "मामा"], ["daada", "दादा"], ["naana", "नाना"], ["kitab", "किताब"],
    ["theek", "ठीक"], ["haan", "हाँ"], ["nahin", "नहीं"], ["main", "मैं"],
    ["hum", "हम"], ["achchha", "अच्छा"]
  ];

  var bank = function () {
    var Q = window.EKGURU_HINDI_QUIZ;
    return (Q && Q.questions) || [];
  };

  /* =========================================================
     TYPING TRAINER
     ========================================================= */
  function mountTyping(host) {
    var F = window.EkGuruFuzzy;
    var items = shuffle(TYPING);
    var pos = 0, done = 0, tries = 0;

    host.innerHTML =
      '<p class="muted">Type the Hindi word in Devanagari. Small differences in ' +
      'spacing or punctuation count as “minor format”, not wrong.</p>' +
      '<div class="row" style="align-items:center;gap:12px;flex-wrap:wrap">' +
      '<span class="lbl" style="font-weight:600">Roman prompt</span>' +
      '<span id="tp-prompt" style="font-size:1.3rem;font-weight:700">' + esc(items[0][0]) + '</span>' +
      '</div>' +
      '<div class="row" style="align-items:center;gap:12px;flex-wrap:wrap;margin-top:10px">' +
      '<label for="typing-in2" style="font-weight:600">Your Devanagari</label>' +
      '<input id="typing-in2" type="text" inputmode="text" autocomplete="off" ' +
      'style="flex:1;min-width:220px" aria-label="Type the Hindi word in Devanagari">' +
      '</div>' +
      '<div class="row" style="gap:10px;margin-top:12px;flex-wrap:wrap">' +
      '<button type="button" class="btn" id="tp-check">Check</button>' +
      '<button type="button" class="btn ghost" id="tp-show">Show answer</button>' +
      '<button type="button" class="btn ghost" id="tp-reset">Reset</button>' +
      '</div>' +
      '<p id="tp-feedback" role="status" style="margin:12px 0 0;font-weight:600"></p>' +
      '<p class="muted" id="tp-score" style="margin:6px 0 0"></p>';

    var prompt = host.querySelector("#tp-prompt");
    var input = host.querySelector("#typing-in2");
    var fb = host.querySelector("#tp-feedback");
    var score = host.querySelector("#tp-score");
    var answered = false;

    function paintScore() { score.textContent = done + " of " + items.length + " done (" + tries + " tries)."; }
    paintScore();

    function next() {
      pos++; answered = false; input.value = "";
      if (pos >= items.length) {
        prompt.textContent = "Done!";
        fb.textContent = "You finished all " + items.length + " words.";
        fb.style.color = "var(--ink)";
        input.disabled = true;
        return;
      }
      prompt.textContent = items[pos][0];
    }

    host.querySelector("#tp-check").addEventListener("click", function () {
      if (answered) { next(); return; }
      var r = F.compare(items[pos][1], input.value);
      tries++;
      if (r.state === "correct") {
        fb.style.color = "var(--green,#1a7f37)"; fb.textContent = "Correct — " + items[pos][1];
        done++; answered = true;
      } else if (r.state === "minor-format") {
        fb.style.color = "var(--accent,#b26a00)";
        fb.textContent = "Minor format difference — accepted: " + items[pos][1];
        done++; answered = true;
      } else if (r.state === "empty") {
        fb.style.color = "var(--red,#b3261e)"; fb.textContent = "Type the word first.";
      } else {
        fb.style.color = "var(--red,#b3261e)"; fb.textContent = "Not quite. Try again or show the answer.";
      }
      paintScore();
    });
    host.querySelector("#tp-show").addEventListener("click", function () {
      fb.style.color = "var(--ink)"; fb.textContent = items[pos][1];
    });
    host.querySelector("#tp-reset").addEventListener("click", function () {
      items = shuffle(TYPING); pos = 0; done = 0; tries = 0; answered = false;
      input.disabled = false; input.value = ""; prompt.textContent = items[0][0];
      fb.textContent = ""; fb.style.color = ""; paintScore();
    });
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") host.querySelector("#tp-check").click(); });
  }

  /* =========================================================
     TOPIC QUIZ
     ========================================================= */
  function mountQuiz(host) {
    var qs = bank();
    var topics = {}, levels = {};
    qs.forEach(function (q) { topics[q.topic] = 1; levels[q.level] = 1; });

    var topicOpts = Object.keys(topics).map(function (t) {
      return '<option value="' + esc(t) + '">' + esc(t) + '</option>';
    }).join("");
    var levelOpts = Object.keys(levels).map(function (l) {
      return '<option value="' + esc(l) + '">' + esc(l) + '</option>';
    }).join("");

    host.innerHTML =
      '<div class="row" style="gap:12px;flex-wrap:wrap;align-items:end">' +
      '<div><label for="q-topic">Topic</label><br><select id="q-topic">' + topicOpts + '</select></div>' +
      '<div><label for="q-level">Level</label><br><select id="q-level">' + levelOpts + '</select></div>' +
      '<div><label for="q-n">Questions</label><br><select id="q-n">' +
      '<option value="5">5</option><option value="10">10</option><option value="15">15</option></select></div>' +
      '<button type="button" class="btn" id="q-start">Start</button>' +
      '</div>' +
      '<div id="q-body" style="margin-top:16px"></div>';

    var state = null;

    function start() {
      var topic = host.querySelector("#q-topic").value;
      var level = host.querySelector("#q-level").value;
      var n = parseInt(host.querySelector("#q-n").value, 10);
      var pool = qs.filter(function (q) { return q.topic === topic && q.level === level; });
      var use = shuffle(pool).slice(0, n);
      if (!use.length) {
        host.querySelector("#q-body").innerHTML = '<p class="muted">No questions for this combination yet.</p>';
        return;
      }
      state = { use: use, i: 0, correct: 0 };
      renderQuestion();
    }

    function renderQuestion() {
      var body = host.querySelector("#q-body");
      if (state.i >= state.use.length) {
        var total = state.use.length;
        var per = Math.round(state.correct / total * 100);
        if (window.EkGuruProgress) window.EkGuruProgress.recordQuiz("topic-quiz", state.correct, total);
        body.innerHTML =
          '<h3>Score: ' + state.correct + ' / ' + total + ' (' + per + '%)</h3>' +
          '<p class="muted">A recognition score, not a fluency measure.</p>' +
          '<button type="button" class="btn" id="q-again">Try again</button>';
        body.querySelector("#q-again").addEventListener("click", start);
        return;
      }
      var q = state.use[state.i];
      var opts = shuffle(q.opts.slice());
      body.innerHTML =
        '<p class="muted">Question ' + (state.i + 1) + ' of ' + state.use.length + ' — ' + esc(q.topic) + '</p>' +
        '<p style="font-weight:700;font-size:1.05rem">' + esc(q.q) + '</p>' +
        opts.map(function (o, idx) {
          return '<button type="button" class="btn ghost" style="display:block;width:100%;text-align:left;margin:6px 0" data-opt="' + idx + '">' + esc(o) + '</button>';
        }).join("") +
        '<div id="q-fb" style="margin-top:10px"></div>';
      body.querySelectorAll("[data-opt]").forEach(function (b) {
        b.addEventListener("click", function () {
          var chosen = opts[parseInt(b.getAttribute("data-opt"), 10)];
          var ok = chosen === q.a;
          if (ok) state.correct++;
          var fb = body.querySelector("#q-fb");
          fb.innerHTML =
            '<p style="font-weight:600;color:' + (ok ? 'var(--green,#1a7f37)' : 'var(--red,#b3261e)') + '">' +
            (ok ? "Correct." : "Not quite — the answer was “" + esc(q.a) + "”.") + '</p>' +
            '<p class="muted">' + esc(q.explain) + '</p>' +
            '<p class="muted">Source: <a href="../../' + esc(q.lesson) + '/">' + esc(q.lesson.replace(/-/g, " ")) + '</a></p>' +
            '<button type="button" class="btn" id="q-next">Next</button>';
          body.querySelector("#q-next").addEventListener("click", function () { state.i++; renderQuestion(); });
        });
      });
    }

    host.querySelector("#q-start").addEventListener("click", start);
  }

  /* =========================================================
     WORKSHEETS
     ========================================================= */
  function mountWorksheet(host) {
    var qs = bank();
    var topics = {};
    qs.forEach(function (q) { topics[q.topic] = 1; });
    var topicOpts = Object.keys(topics).map(function (t) {
      return '<option value="' + esc(t) + '">' + esc(t) + '</option>';
    }).join("");

    host.innerHTML =
      '<div class="row" style="gap:12px;flex-wrap:wrap;align-items:end">' +
      '<div><label for="w-topic">Topic</label><br><select id="w-topic">' + topicOpts + '</select></div>' +
      '<div><label for="w-n">Prompts</label><br><select id="w-n">' +
      '<option value="5">5</option><option value="10">10</option><option value="15">15</option></select></div>' +
      '<div><label><input type="checkbox" id="w-ans" checked> include answer section</label></div>' +
      '<button type="button" class="btn" id="w-make">Make worksheet</button>' +
      '<button type="button" class="btn ghost" id="w-print">Print</button>' +
      '</div>' +
      '<div id="w-sheet" style="margin-top:16px"></div>';

    var made = [];

    host.querySelector("#w-make").addEventListener("click", function () {
      var topic = host.querySelector("#w-topic").value;
      var n = parseInt(host.querySelector("#w-n").value, 10);
      made = shuffle(qs.filter(function (q) { return q.topic === topic; })).slice(0, n);
      var withAns = host.querySelector("#w-ans").checked;
      var sheet = host.querySelector("#w-sheet");
      var lines = made.map(function (q, i) {
        return '<p style="font-weight:700">' + (i + 1) + '. ' + esc(q.q) + '</p>' +
               '<div style="border-bottom:1px solid var(--line);height:44px;margin:0 0 18px"></div>';
      }).join("");
      var ans = withAns ? '<h3>Answers</h3>' + made.map(function (q, i) {
        return '<p>' + (i + 1) + '. <b>' + esc(q.a) + '</b> — ' + esc(q.explain) + '</p>';
      }).join("") : "";
      sheet.innerHTML =
        '<div class="ws-page" style="background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px;max-width:640px">' +
        '<h2 style="margin:0 0 4px">Hindi worksheet — ' + esc(topic) + '</h2>' +
        '<p class="muted" style="margin:0 0 14px">Write your answers, then check the answer section.</p>' +
        lines + ans +
        '<p class="muted" style="margin-top:12px;font-size:.78rem">From the EkGuru Hindi quiz bank — free to print and share.</p>' +
        '</div>';
    });

    host.querySelector("#w-print").addEventListener("click", function () {
      if (!made.length) { host.querySelector("#w-make").click(); }
      window.print();
    });
  }

  /* ---------- auto-mount ---------- */
  function boot() {
    var t = document.getElementById("typing-app");
    var q = document.getElementById("quiz-app");
    var w = document.getElementById("ws-app");
    if (t) mountTyping(t);
    if (q) mountQuiz(q);
    if (w) mountWorksheet(w);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
