/* =========================================================
   EkGuru — STARTER PRACTICE (Phase 7C Stage 4)
   ---------------------------------------------------------
   A deterministic, rule-based "starter check" for language
   packs. It is NOT an exam, NOT adaptive, and NOT AI:
   it always asks the same 8 questions (the first 8 words of
   the pack, with fixed distractors), marks right/wrong, and
   shows an honest total. Nothing is saved — the score stays
   on the device. No network beyond the pack JSON already in
   the repo.

   Window API: window.EkGuruStarter
     renderCheck(el, lang) -> renders the 8-question check
   ========================================================= */
(function (root) {
  "use strict";

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  function loadPack(lang) {
    return new Promise(function (resolve, reject) {
      var LP = root.EkGuruLangPack;
      if (!LP) { reject(new Error("no langpack")); return; }
      LP.ready().then(function () {
        var p = LP.get(lang);
        var url = LP.packUrl(lang);
        if (!p || !url) { reject(new Error("no pack")); return; }
        root.fetch(url, { cache: "no-store" })
          .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("pack " + r.status)); })
          .then(function (d) { resolve(d); })
          .catch(reject);
      }).catch(reject);
    });
  }

  function buildQuestions(d) {
    var words = (d.items || []).filter(function (i) { return i.type === "word"; });
    if (words.length < 8) return [];
    var qs = [];
    for (var i = 0; i < 8; i++) {
      var correct = words[i];
      var opts = [correct];
      // fixed, deterministic distractors from later in the list
      for (var k = 1; k <= 3; k++) {
        var cand = words[(i + k * 4) % words.length];
        if (cand && cand !== correct && opts.indexOf(cand) < 0) opts.push(cand);
      }
      // top up from the very end if any distractor collided
      var j = words.length - 1;
      while (opts.length < 4 && j >= 0) {
        if (opts.indexOf(words[j]) < 0) opts.push(words[j]);
        j--;
      }
      qs.push({ word: correct, options: opts });
    }
    return qs;
  }

  function render(el, questions, langName) {
    var state = { i: 0, score: 0 };
    function qHTML(q, n) {
      var opts = q.options.map(function (o) {
        return '<button class="btn btn-ghost btn-sm sc-opt" type="button" data-opt="' + esc(o.id) + '">' + esc(o.meaning) + '</button>';
      }).join("");
      return '<div class="sc-q">'
        + '<p class="sc-count">Question ' + (n + 1) + ' of ' + questions.length + '</p>'
        + '<p class="sc-word" lang="' + esc(q.word.language || "") + '" dir="auto">' + esc(q.word.target) + '</p>'
        + '<p class="muted">What does it mean?</p>'
        + '<div class="sc-opts">' + opts + '</div>'
        + '<p class="sc-fb" aria-live="polite"></p>'
        + '<div class="sc-nav"></div>'
        + '</div>';
    }
    function draw() {
      if (state.i >= questions.length) {
        el.innerHTML = '<div class="sc-done">'
          + '<p class="sc-count">Finished</p>'
          + '<p>You got <b>' + state.score + ' of ' + questions.length + '</b>. '
          + 'This is practice — nothing is saved and your result stays on this device. '
          + 'It is a fixed rule-based check, not an exam and not AI.</p>'
          + '<button class="btn btn-primary btn-sm" type="button" id="sc-again">Restart</button>'
          + '</div>';
        var again = document.getElementById("sc-again");
        if (again) again.addEventListener("click", function () { state.i = 0; state.score = 0; draw(); });
        return;
      }
      var q = questions[state.i];
      el.innerHTML = qHTML(q, state.i);
      var fb = el.querySelector(".sc-fb");
      var nav = el.querySelector(".sc-nav");
      var buttons = el.querySelectorAll(".sc-opt");
      buttons.forEach(function (b) {
        b.addEventListener("click", function () {
          var picked = b.getAttribute("data-opt");
          var right = picked === q.word.id;
          buttons.forEach(function (x) { x.disabled = true; });
          if (right) {
            state.score += 1;
            b.classList.add("sc-right");
            fb.textContent = "Correct — “" + q.word.target + "” means “" + q.word.meaning + "”.";
          } else {
            b.classList.add("sc-wrong");
            buttons.forEach(function (x) { if (x.getAttribute("data-opt") === q.word.id) x.classList.add("sc-right"); });
            fb.textContent = "Not quite — “" + q.word.target + "” means “" + q.word.meaning + "”.";
          }
          var next = document.createElement("button");
          next.type = "button";
          next.className = "btn btn-primary btn-sm";
          next.textContent = state.i === questions.length - 1 ? "Finish" : "Next";
          next.addEventListener("click", function () { state.i += 1; draw(); });
          nav.appendChild(next);
        });
      });
    }
    draw();
  }

  var API = {
    renderCheck: function (el, lang) {
      if (!el) return;
      el.innerHTML = '<p class="muted">Loading starter check…</p>';
      var name = (root.EkGuruLangPack && root.EkGuruLangPack.get(lang) && root.EkGuruLangPack.get(lang).name) || lang;
      loadPack(lang).then(function (d) {
        var qs = buildQuestions(d);
        if (!qs.length) { el.innerHTML = '<p class="muted">Not enough words in this pack for a check.</p>'; return; }
        el.innerHTML = '<p class="muted">A fixed rule-based check — the same ' + qs.length + ' questions every time. Not an exam, not AI, nothing is saved.</p>';
        var box = document.createElement("div");
        box.className = "sc-box";
        el.appendChild(box);
        render(box, qs, name);
      }).catch(function () {
        el.innerHTML = '<p class="muted">Starter check unavailable right now.</p>';
      });
    }
  };

  root.EkGuruStarter = API;
})(typeof window !== "undefined" ? window : globalThis);
