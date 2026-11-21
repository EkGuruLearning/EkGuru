/* =========================================================
   EkGuru — "type a number, read it" controller
   ---------------------------------------------------------
   One controller for every numbers page. The page says which
   language with data-lang on the input, so adding Marathi or
   Kannada is a data file, not a second implementation.

   The data ships as js/numbers-data.js (generated from
   data/numbers/*.json) rather than being fetched. A numbers
   tool that shows nothing until a request lands feels broken,
   and this one has to answer on the first keystroke.
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
    var input = document.getElementById("numIn");
    var out = document.getElementById("out");
    if (!input || !out) return;

    var lang = input.getAttribute("data-lang") || "pa";
    var btnrow = document.getElementById("btnrow");
    var copyBtn = document.getElementById("copyBtn");
    var lastText = "";

    function esc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }

    function render(raw) {
      var value = String(raw || "").trim();
      var lib = window.EkGuruNumbers;
      if (!lib) return;

      if (!value) {
        out.innerHTML = '<div class="big" lang="pa">੨੫</div>' +
          '<div class="rom">ਪੰਝੀ · panjhi — twenty-five. Type a number above.</div>';
        lastText = "";
        if (btnrow) btnrow.hidden = true;
        return;
      }

      /* Digits only. Anything else is stripped rather than rejected — a
         visitor who types "25." or " 25 " meant 25. */
      var digits = value.replace(/[^0-9]/g, "");
      if (!digits) {
        out.innerHTML = '<div class="big" lang="pa">?</div>' +
          '<div class="rom">Numbers only — try 25 or 100.</div>';
        lastText = "";
        if (btnrow) btnrow.hidden = true;
        return;
      }
      var n = parseInt(digits, 10);
      if (n > 10000000) n = n % 10000000;

      var gur = lib.digits(n, lang);
      var hit = lib.word(n, lang);

      if (!hit) {
        /* The table covers 0-100 plus the round large numbers. Beyond that
           we can still write the digits, which is genuinely useful, and we
           say plainly what we are not giving. */
        out.innerHTML = '<div class="big" lang="pa">' + esc(gur) + "</div>" +
          '<div class="rom">' + esc(String(n)) + " in Gurmukhi digits. " +
          "The word for this one is built from the parts above and below — " +
          "start with the thousands word ਸੌ / ਹਜ਼ਾਰ / ਲੱਖ.</div>";
        lastText = gur;
        if (btnrow) btnrow.hidden = false;
        return;
      }

      var also = hit.a && hit.a.length ? " (also " + hit.a.join(" / ") + ")" : "";
      lastText = hit.w;
      out.innerHTML = '<div class="big" lang="pa">' + esc(gur) + "</div>" +
        '<div class="rom">' + esc(hit.w) + " · " + esc(hit.r) + also +
        " — " + esc(String(n)) + "</div>";
      if (btnrow) btnrow.hidden = false;
    }

    var timer = null;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      var v = input.value;
      timer = setTimeout(function () { render(v); }, 60);
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

    /* ?n=49 opens with the answer — the same shareable-link convention as
       the name tool. */
    try {
      var q = new URLSearchParams(window.location.search).get("n");
      if (q) {
        input.value = q.slice(0, 8);
        render(input.value);
      }
    } catch (e) { /* no URLSearchParams: nothing to do */ }
  });
})();
