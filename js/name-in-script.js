/* =========================================================
   EkGuru — "my name in Punjabi / Gujarati / …" tool
   ---------------------------------------------------------
   One controller for every script page. The page decides which
   script it is with data-script on #nameIn, so there is one
   implementation and no chance of the Punjabi page behaving
   differently from the Gujarati one.

   Two sources of truth for an answer, in this order:

   1. data/names/names.json — names whose spelling is curated,
      because a mechanical transliteration gets them wrong. The
      clearest example is Singh: सिंह → a pure mapping gives
      ਸਿਂਹ, and no Punjabi writes it that way. It is ਸਿੰਘ.
      When a curated entry exists we say so, and we show it is
      the spelling people actually use.

   2. The rule engine (js/translit.js → js/script-map.js) for
      everything else, labelled as phonetic rather than curated.
      For an uncommon name that is still the best answer
      available, but the visitor deserves to know which one
      they are looking at — a tattoo is permanent and this page
      is not a native speaker.
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
    var input = document.getElementById("nameIn");
    var out = document.getElementById("out");
    if (!input || !out) return;

    var script = input.getAttribute("data-script") || "gurmukhi";
    var btnrow = document.getElementById("btnrow");
    var copyBtn = document.getElementById("copyBtn");
    var explainBtn = document.getElementById("explainBtn");
    var explain = document.getElementById("explain");
    var help = document.getElementById("outHelp");
    var lastText = "";

    /* The curated list ships with the page as js/names-data.js, not as a
       fetch. It used to be fetched, and in testing the first keystroke
       often landed before the response did — so "Singh" rendered as the
       mechanical ਸਿਙ for a moment, which is the one answer this page
       exists to get right. 5 KB inline removes the race entirely. */
    var curatedFor = function (name) {
      var lib = window.EkGuruNames;
      return lib ? lib.lookup(name) : null;
    };

    function render(value) {
      var name = String(value || "").trim();
      if (!name) {
        out.innerHTML = '<div class="big">' + (input.getAttribute("data-placeholder-native") || "") +
          '</div><div class="rom">' + (input.getAttribute("data-placeholder-rom") || "") + "</div>";
        lastText = "";
        if (btnrow) btnrow.hidden = true;
        if (explain) explain.innerHTML = "";
        return;
      }

      var hit = curatedFor(name);
      var result, note, badge;

      if (hit) {
        result = hit[scriptShort(script)] || hit.pa;
        note = "This spelling is curated — it is how the name is actually written, " +
               "not a rule applied to the letters. Surnames like Singh are the reason " +
               "the list exists.";
        badge = "Curated spelling";
      } else {
        var r = window.EkGuruScriptMap.fromEnglish(name, script);
        result = r.text;
        note = "This is the phonetic spelling — the rule engine read the sounds and " +
               "wrote them in " + scriptName() + ". For an uncommon name that is the best " +
               "answer there is, but have a native speaker confirm it before anything permanent.";
        badge = r.complete ? "Phonetic spelling" : "Phonetic spelling — partial";
      }

      lastText = result;
      out.innerHTML = '<div class="big" lang="pa">' + esc(result) + "</div>" +
        '<div class="rom">' + esc(badge) + " · " + esc(name) + "</div>";
      if (btnrow) btnrow.hidden = false;
      if (help) help.textContent = note;
      if (explain && explain.getAttribute("data-open") === "1") showLetters(name, hit);
      else if (explain) explain.innerHTML = "";
    }

    function scriptShort(s) {
      return s === "gurmukhi" ? "pa" : s === "devanagari" ? "hi" : s;
    }

    function scriptName() {
      var n = window.EkGuruScriptMap && window.EkGuruScriptMap.names[script];
      return n ? n.en : script;
    }

    function esc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }

    /* Letter-by-letter only for the rule path: a curated spelling is a
       whole word, and splitting it into letters would invent a story
       about why each letter is there. */
    function showLetters(name, hit) {
      if (hit) {
        explain.innerHTML = '<p class="rom" style="margin-top:12px">A curated spelling is kept as a ' +
          "whole word. There is no letter-by-letter rule to show, because the spelling did not " +
          "come from one.</p>";
        return;
      }
      var r = window.EkGuruScriptMap.fromEnglish(name, script);
      var rows = "";
      var dev = Array.from(r.devanagari);
      var tgt = Array.from(r.text);
      /* Only pairs of equal length can be shown honestly; the orthography
         pass can merge or drop marks, so bail rather than misalign. */
      if (dev.length !== tgt.length) {
        explain.innerHTML = '<p class="rom" style="margin-top:12px">' + esc(r.devanagari) +
          " → " + esc(r.text) + " · " + esc(scriptName()) +
          " changes some clusters, so a letter-by-letter table would be misleading here.</p>";
        return;
      }
      for (var i = 0; i < dev.length; i++) {
        rows += "<tr><td>" + esc(dev[i]) + "</td><td>" + esc(tgt[i]) + '</td><td class="rom">' +
          "U+" + dev[i].codePointAt(0).toString(16).toUpperCase() + " → U+" +
          tgt[i].codePointAt(0).toString(16).toUpperCase() + "</td></tr>";
      }
      explain.innerHTML = '<table class="ex" style="margin-top:14px"><thead><tr><th>Devanagari</th><th>' +
        esc(scriptName()) + "</th><th>Codepoints</th></tr></thead><tbody>" + rows + "</tbody></table>";
    }

    var timer = null;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      var v = input.value;
      timer = setTimeout(function () { render(v); }, 90);
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

    if (explainBtn) {
      explainBtn.addEventListener("click", function () {
        var open = explain.getAttribute("data-open") === "1";
        explain.setAttribute("data-open", open ? "0" : "1");
        explainBtn.textContent = open ? "Show every letter" : "Hide letters";
        if (!open) showLetters(input.value.trim(), curatedFor(input.value));
        else explain.innerHTML = "";
      });
    }

    /* Shareable link: /name-in-punjabi/?q=Simran opens with the answer
       already on screen. Same parameter name as the Hindi tool, so the
       two pages can be linked with one convention. */
    try {
      var qp = new URLSearchParams(window.location.search);
      var q = qp.get("q") || qp.get("name");
      if (q) {
        input.value = q.slice(0, 60);
        render(input.value);
      } else {
        render(input.value);
      }
    } catch (e) {
      render(input.value);
    }

  });
})();
