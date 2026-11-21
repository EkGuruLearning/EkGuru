/* =========================================================
   EkGuru — "type an English day/month/time word, read it
   back in the target language" controller
   ---------------------------------------------------------
   The visitor types in ENGLISH and gets the answer in the
   language's own script and real usage. One controller for
   every time page; the page says which language with
   data-lang on the input. The data ships inline in
   js/time-data.js (generated from data/time/*.json) so the
   answer appears on the first keystroke, not after a fetch.

   Matching is a plain lowercase key lookup. Unknown input
   returns a short list of what is available, never a guess.
   ========================================================= */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  ready(function () {
    var input = document.getElementById("tIn");
    var out = document.getElementById("tOut");
    if (!input || !out) return;

    var lang = input.getAttribute("data-lang") || "pa";
    var lib = window.EkGuruTime && window.EkGuruTime.langs[lang];
    var btnrow = document.getElementById("tbtnrow");
    var copyBtn = document.getElementById("tcopyBtn");
    var lastText = "";

    function esc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }

    /* collapse everything into one lowercase English key -> record map */
    function index(lib) {
      var map = {};
      function add(list) {
        for (var i = 0; i < list.length; i++) {
          var e = list[i];
          var k = String(e.en || "").toLowerCase().trim();
          if (k && !map[k]) map[k] = { w: e.word, r: e.roman, a: e.also || [] };
        }
      }
      add(lib.days);
      add(lib.months);
      add(lib.desi_months);
      add(lib.time_words);
      return map;
    }

    var IDX = lib ? index(lib) : {};
    var KEYS = Object.keys(IDX).sort();

    function render(raw) {
      var value = String(raw || "").trim();
      if (!value) {
        out.innerHTML =
          '<div class="big" lang="' + lang + '"></div>' +
          '<div class="rom">Type an English word — a day, a month or a time word — ' +
          "and see it in " + esc((lib && lib.name) || lang) + ".</div>";
        lastText = "";
        if (btnrow) btnrow.hidden = true;
        return;
      }

      var key = value.toLowerCase();
      var hit = IDX[key];
      if (hit) {
        var also = hit.a && hit.a.length
          ? " <span class=\"alt\">or " + esc(hit.a.join(" / ")) + "</span>" : "";
        lastText = hit.w;
        out.innerHTML =
          '<div class="big" lang="' + lang + '">' + esc(hit.w) + "</div>" +
          '<div class="rom">' + esc(hit.r) + also + " — " + esc(value) + "</div>";
        if (btnrow) btnrow.hidden = false;
        return;
      }

      /* not found: offer the closest thing rather than a dead end */
      var starts = KEYS.filter(function (k) { return k.indexOf(key) === 0; });
      var hint = starts.length
        ? "Did you mean: " + starts.slice(0, 6).map(esc).join(", ") + "?"
        : "No match for that. Try a day like Monday, a month like March, or a time word like morning.";
      out.innerHTML =
        '<div class="big" lang="' + lang + '">?</div>' +
        '<div class="rom">' + hint + "</div>";
      lastText = "";
      if (btnrow) btnrow.hidden = true;
    }

    var timer = null;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { render(input.value); }, 60);
    });

    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        if (!lastText) return;
        var done = function () {
          copyBtn.textContent = "Copied";
          setTimeout(function () { copyBtn.textContent = "Copy"; }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(lastText).then(done, function () {});
        } else {
          var ta = document.createElement("textarea");
          ta.value = lastText;
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand("copy"); done(); } catch (e) {}
          document.body.removeChild(ta);
        }
      });
    }

    try {
      var q = new URLSearchParams(window.location.search).get("w");
      if (q) {
        input.value = q.slice(0, 40);
        render(input.value);
      }
    } catch (e) { /* no URLSearchParams: nothing to do */ }
  });
})();
