/* =========================================================
   EkGuru — PRACTICE ENGINE  (v100)
   ---------------------------------------------------------
   Drives every practice lab from js/practice-bank.js. One
   engine, several modes, no per-page logic duplicated.

   Modes
     practice    a shuffled run through one bank
     daily       N mixed questions across all banks
     review      the mastery queue (a simple box system)
     placement   the diagnostic run, with an honest result

   HONEST FRAMING, enforced here:
   · Multiple choice tests recognition and recall — never the
     ability to speak or to follow a native speaker at speed.
   · The mastery "boxes" are a simple review scheduler, NOT
     clinical spaced repetition, and the UI says so.
   · The placement result is a rough starting point, NOT a
     certified level. Pronunciation playback is a computer
     voice, and there is no automatic pronunciation scoring —
     nothing here measures your accent.
   · Everything is stored in this browser only. No account, no
     upload, no score leaves the device.
   ========================================================= */
(function () {
  "use strict";

  var KEY = "ekguru_mastery_v1";

  function bank(name) {
    return (window.EKGURU_PRACTICE_BANK || {})[name] || [];
  }

  function allBanks() {
    var B = window.EKGURU_PRACTICE_BANK || {};
    var out = [];
    Object.keys(B).forEach(function (k) {
      if (k === "placement") return;         // placement is its own run
      if (k === "speaking") return;          // speaking is self-graded, its own mode
      B[k].forEach(function (item, i) { out.push({ bank: k, index: i, item: item }); });
    });
    return out;
  }

  /* ---------- mastery store (a simple box system) ---------- */
  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; }
  }
  function write(m) { try { localStorage.setItem(KEY, JSON.stringify(m)); } catch (e) {} }

  function keyOf(entry) {
    /* A stable id for an item: bank + a hash of the question. */
    var q = String(entry.item.q || entry.item.words || entry.item.a || "").slice(0, 60);
    var h = 0;
    for (var i = 0; i < q.length; i++) { h = (h * 31 + q.charCodeAt(i)) | 0; }
    return entry.bank + ":" + Math.abs(h);
  }

  var BOX_DELAY_DAYS = [0, 0, 1, 3, 7, 21];  // box 0..5

  function dueEntries() {
    var m = read(), now = Date.now(), out = [];
    allBanks().forEach(function (e) {
      var k = keyOf(e), r = m[k];
      if (!r || r.box < 2) { out.push(e); return; }
      var delay = BOX_DELAY_DAYS[r.box] || 21;
      if (r.last + delay * 86400000 <= now) out.push(e);
    });
    return out;
  }

  function record(entry, correct) {
    var m = read(), k = keyOf(entry);
    var r = m[k] || { box: 0, streak: 0, last: 0, seen: 0 };
    r.seen = (r.seen || 0) + 1;
    if (correct) {
      r.box = Math.min(5, r.box + 1);
      r.streak += 1;
    } else {
      r.box = Math.max(0, r.box - 1);
      r.streak = 0;
    }
    r.last = Date.now();
    m[k] = r;
    write(m);
  }

  /* ---------- helpers ---------- */
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
  function speak(text) {
    try {
      if (!("speechSynthesis" in window)) return false;
      var u = new SpeechSynthesisUtterance(String(text));
      u.lang = "hi-IN";
      u.rate = 0.8;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
      return true;
    } catch (e) { return false; }
  }

  /* ---------- the flow ---------- */
  function mount(el, cfg) {
    cfg = cfg || {};
    var entries;
    var mode = cfg.mode || "practice";

    if (mode === "review") {
      entries = dueEntries();
    } else if (mode === "daily") {
      entries = shuffle(allBanks()).slice(0, cfg.count || 10);
    } else if (mode === "placement") {
      entries = bank("placement").map(function (item, i) { return { bank: "placement", index: i, item: item }; });
    } else if (mode === "speak") {
      entries = bank("speaking").map(function (item, i) { return { bank: "speaking", index: i, item: item }; });
      entries = shuffle(entries).slice(0, cfg.count || entries.length);
    } else {
      var src = bank(cfg.bank).map(function (item, i) { return { bank: cfg.bank, index: i, item: item }; });
      entries = shuffle(src).slice(0, cfg.count || src.length);
    }

    var state = { i: 0, score: 0, answered: false, answerWords: [] };
    var box = el;

    function note() {
      var s;
      if (mode === "placement") {
        s = "A rough diagnostic, not a certified placement test. It suggests where to start — it does not grade you.";
      } else if (mode === "speak") {
        s = "Say the phrase out loud before you reveal it. This page cannot hear you — the only scoring here is your own honesty. Playback is a computer voice, not a native accent.";
      } else if (mode === "review") {
        s = "A simple review box system (not clinical spaced repetition). Items you get wrong come back sooner; items you get right wait longer.";
      } else if (mode === "daily") {
        s = "Daily practice: a short mixed run. Recognition practice only — it does not test speaking or listening to a native speaker at speed.";
      } else {
        s = "Practice, not a test: multiple choice measures recognition of forms, not conversation. No score leaves this browser.";
      }
      return '<p class="px-note">' + esc(s) + "</p>";
    }

    function render() {
      if (!entries.length) {
        box.innerHTML = '<div class="px-done" role="status"><div class="px-done-ic">✓</div>' +
          "<h3>Nothing due right now</h3>" +
          "<p>Your review queue is empty — either nothing has been practised yet, or everything is scheduled for later.</p>" +
          '<p><a class="btn btn-primary" href="./vocabulary/">Start practising</a></p></div>';
        return;
      }
      if (state.i >= entries.length) return finish();
      var e = entries[state.i], item = e.item;
      state.answered = false;
      state.answerWords = [];

      if (mode === "speak") return renderSpeak(e, item);

      var type = item.words ? "order" : "choice";

      var optsHtml = "";
      if (type === "order") {
        var words = shuffle(item.words).map(function (w, i) {
          return '<button type="button" class="px-word" data-w="' + i + '">' + esc(w) + "</button>";
        }).join("");
        optsHtml =
          '<div class="px-order" aria-label="Words to arrange">' + words + "</div>" +
          '<div class="px-answer" aria-label="Your sentence" aria-live="polite"></div>' +
          '<div class="px-order-btns">' +
            '<button type="button" class="btn btn-ghost px-undo">⌫ Undo</button>' +
            '<button type="button" class="btn btn-ghost px-clear">Clear</button>' +
          "</div>";
      } else {
        optsHtml = '<div class="px-opts" role="list">' +
          shuffle(item.opts).map(function (o, i) {
            return '<button type="button" class="px-opt" data-i="' + i + '" role="listitem">' + esc(o) + "</button>";
          }).join("") + "</div>";
      }

      var listenHtml = "";
      if (item.tts) {
        listenHtml = '<button type="button" class="btn px-play">🔊 Play again</button> ' +
          '<span class="px-tts-note">(computer voice — good for recognition, not a native accent)</span>';
      }

      box.innerHTML =
        '<div class="px-head">' +
          '<span class="px-count">' + (mode === "placement" ? "Question " : "Practice ") +
            (state.i + 1) + " of " + entries.length + "</span>" +
          '<span class="px-score">' + state.score + " right</span>" +
        "</div>" +
        '<div class="px-bar"><span style="width:' + Math.round(state.i / entries.length * 100) + '%"></span></div>' +
        '<div class="px-q">' + esc(item.q) + "</div>" +
        listenHtml +
        optsHtml +
        '<div class="px-fb" aria-live="polite" hidden></div>' +
        '<div class="px-next-wrap"><button type="button" class="btn btn-primary px-next" hidden>Next →</button></div>' +
        note();

      var next = box.querySelector(".px-next");
      function showNext() {
        next.hidden = false;
        next.focus();
      }

      if (type === "order") {
        var answerEl = box.querySelector(".px-answer");
        box.querySelectorAll(".px-word").forEach(function (b) {
          b.addEventListener("click", function () {
            if (state.answered) return;
            if (b.dataset.used) return;
            b.dataset.used = "1";
            b.classList.add("px-used");
            state.answerWords.push(b.textContent);
            answerEl.textContent = state.answerWords.join(" ");
          });
        });
        var undo = box.querySelector(".px-undo");
        undo.addEventListener("click", function () {
          if (state.answered) return;
          if (!state.answerWords.length) return;
          state.answerWords.pop();
          answerEl.textContent = state.answerWords.join(" ");
          /* un-mark the word we removed */
          var target = state.answerWords.join(" ");
          box.querySelectorAll(".px-word").forEach(function (b) {
            if (b.dataset.used && target.indexOf(b.textContent) === -1) {
              delete b.dataset.used; b.classList.remove("px-used");
            }
          });
        });
        box.querySelector(".px-clear").addEventListener("click", function () {
          if (state.answered) return;
          state.answerWords = [];
          answerEl.textContent = "";
          box.querySelectorAll(".px-word").forEach(function (b) {
            delete b.dataset.used; b.classList.remove("px-used");
          });
        });
        next.addEventListener("click", function () {
          if (!state.answered) {
            var correct = state.answerWords.join(" ") === item.answer.join(" ");
            state.answered = true;
            record(e, correct);
            var fb = box.querySelector(".px-fb");
            if (correct) { state.score++; fb.className = "px-fb ok"; }
            else fb.className = "px-fb bad";
            fb.hidden = false;
            fb.innerHTML = (correct ? "✓ Correct — " : "✗ Not quite. The answer is: <b>") +
              (correct ? "" : esc(item.answer.join(" ")) + "</b>") +
              '<div class="px-explain">' + esc(item.explain || "") + "</div>";
            showNext();
          } else { state.i++; render(); }
        });
      } else {
        box.querySelectorAll(".px-opt").forEach(function (b) {
          b.addEventListener("click", function () {
            if (state.answered) return;
            state.answered = true;
            var chosen = b.textContent;
            var correct = chosen === item.a;
            record(e, correct);
            var fb = box.querySelector(".px-fb");
            fb.hidden = false;
            box.querySelectorAll(".px-opt").forEach(function (o) {
              o.disabled = true;
              if (o.textContent === item.a) o.classList.add("px-right");
              else if (o === b && !correct) o.classList.add("px-wrong");
            });
            if (correct) { state.score++; fb.className = "px-fb ok"; fb.innerHTML = "✓ Correct"; }
            else { fb.className = "px-fb bad"; fb.innerHTML = "✗ Not quite — the answer is <b>" + esc(item.a) + "</b>"; }
            fb.innerHTML += '<div class="px-explain">' + esc(item.explain || "") + "</div>";
            showNext();
          });
        });
        next.addEventListener("click", function () { state.i++; render(); });
      }

      var play = box.querySelector(".px-play");
      if (play) {
        play.addEventListener("click", function () {
          if (!speak(item.tts)) play.textContent = "Playback unavailable in this browser";
        });
        speak(item.tts);   // play once on load
      }
    }

    function renderSpeak(e, item) {
      box.innerHTML =
        '<div class="px-head">' +
          '<span class="px-count">Phrase ' + (state.i + 1) + " of " + entries.length + "</span>" +
          '<span class="px-score">' + state.score + " said right</span>" +
        "</div>" +
        '<div class="px-bar"><span style="width:' + Math.round(state.i / entries.length * 100) + '%"></span></div>' +
        '<div class="px-q" style="font-size:1.45rem;line-height:1.6">' + esc(item.q) + "</div>" +
        '<button type="button" class="btn px-play">🔊 Play (computer voice)</button>' +
        '<div class="px-fb" aria-live="polite" hidden></div>' +
        '<div class="px-next-wrap">' +
          '<button type="button" class="btn btn-ghost px-reveal">Reveal</button> ' +
          '<button type="button" class="btn btn-primary px-next" hidden>Next →</button>' +
        "</div>" +
        note();

      var fb = box.querySelector(".px-fb");
      var reveal = box.querySelector(".px-reveal");
      var next = box.querySelector(".px-next");
      var play = box.querySelector(".px-play");
      play.addEventListener("click", function () {
        if (!speak(item.q)) play.textContent = "Playback unavailable in this browser";
      });
      reveal.addEventListener("click", function () {
        reveal.hidden = true;
        fb.hidden = false;
        fb.className = "px-fb ok";
        fb.innerHTML = "<b>" + esc(item.a) + "</b>" +
          '<div class="px-explain">' + esc(item.explain || "") + "</div>" +
          '<div style="margin-top:10px">How did you do? ' +
            '<button type="button" class="btn btn-ghost px-good">I said it right</button> ' +
            '<button type="button" class="btn btn-ghost px-bad">Not yet</button></div>';
        var good = box.querySelector(".px-good"), bad = box.querySelector(".px-bad");
        function graded(correct) {
          record(e, correct);
          if (correct) state.score++;
          if (good) good.disabled = true;
          if (bad) bad.disabled = true;
          next.hidden = false;
          next.focus();
        }
        good.addEventListener("click", function () { graded(true); });
        bad.addEventListener("click", function () { graded(false); });
      });
      next.addEventListener("click", function () { state.i++; render(); });
    }

    function finish() {
      var pct = entries.length ? Math.round(state.score / entries.length * 100) : 0;
      var body;
      if (mode === "placement") {
        var suggestion = placementSuggestion(state.score, entries.length);
        body = '<div class="px-done" role="status"><div class="px-done-ic">✓</div>' +
          "<h3>Diagnostic complete</h3>" +
          "<p>You got <b>" + state.score + " of " + entries.length + "</b>.</p>" +
          '<div class="px-explain">' + esc(suggestion) + "</div>" +
          '<div class="px-done-btns">' +
            '<a class="btn btn-primary" href="' + suggestionUrl(suggestion) + '">Start here</a> ' +
            '<a class="btn btn-ghost" href="./">All practice</a>' +
          "</div></div>";
      } else if (mode === "speak") {
        body = '<div class="px-done" role="status"><div class="px-done-ic">✓</div>' +
          "<h3>Round complete</h3>" +
          "<p>You practised " + entries.length + " phrase" + (entries.length === 1 ? "" : "s") + ". " +
          "Speaking is a physical skill — it only improves with repetition, so do it again tomorrow.</p>" +
          '<div class="px-done-btns">' +
            '<button type="button" class="btn btn-primary px-again">Another round</button> ' +
            '<a class="btn btn-ghost" href="./">All practice</a>' +
          "</div></div>";
      } else {
        body = '<div class="px-done" role="status"><div class="px-done-ic">✓</div>' +
          "<h3>" + (mode === "daily" ? "Daily practice done" : "Round complete") + "</h3>" +
          "<p>" + state.score + " of " + entries.length + " correct.</p>" +
          '<div class="px-done-btns">' +
            '<button type="button" class="btn btn-primary px-again">Another round</button> ' +
            '<a class="btn btn-ghost" href="./">All practice</a>' +
          "</div></div>";
      }
      box.innerHTML = body;
      var again = box.querySelector(".px-again");
      if (again) again.addEventListener("click", function () {
        state.i = 0; state.score = 0; render();
      });
    }

    function placementSuggestion(right, total) {
      var r = right / total;
      if (r >= 0.9) return "You are well past the basics. Start with Grammar Foundations to tighten word order, gender and tenses — then Speaking Starter to put it into speech.";
      if (r >= 0.7) return "You have the core. Everyday Hindi is the right next step — conversation, plans and opinions — with Grammar Foundations for the rules you still guess at.";
      if (r >= 0.5) return "You know some Hindi but the script or the grammar is shaky. Do Reading Hindi to lock in Devanagari, then Hindi From Zero's grammar stage.";
      return "Start with Hindi From Zero — the script first, then first words. Everything else builds on it, and it is two or three weeks of steady work.";
    }
    function suggestionUrl(s) {
      if (s.indexOf("Grammar Foundations") === 0) return "../../paths/grammar-foundations/";
      if (s.indexOf("Everyday Hindi") === 0) return "../../paths/everyday-hindi/";
      if (s.indexOf("Reading Hindi") === 0) return "../../paths/reading-hindi/";
      return "../../paths/hindi-from-zero/";
    }

    render();
  }

  window.EkGuruPractice = {
    mount: mount,
    masteryCount: function () { return Object.keys(read()).length; },
    dueCount: function () { return dueEntries().length; }
  };
})();
