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
    var scriptVariant = input.getAttribute("data-variant") || null;
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

    /* Non-Indic scripts (Arabic, Greek, Cyrillic, Hangul, Kana,
       Ethiopic) have their own engine in js/non-indic-scripts.js.
       They do not share the Devanagari abugida structure, so they
       cannot go through script-map.js. */
    var NON_INDIC = ["arabic", "greek", "cyrillic", "hangul", "kana", "ethiopic"];
    var isNonIndic = NON_INDIC.indexOf(script) !== -1;

    function fromEnglish(name) {
      if (isNonIndic) {
        return window.EkGuruNonIndic.fromEnglish(name, script, scriptVariant);
      }
      return window.EkGuruScriptMap.fromEnglish(name, script);
    }

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

      /* For non-Indic scripts, a curated entry only counts if it
         actually has a field for this script. Otherwise the entry
         exists for an Indic script and would fall back to hit.pa,
         producing Punjabi for an Arabic page. */
      var curatedHit = hit;
      if (hit && isNonIndic && !hit[scriptShort(script)]) {
        curatedHit = null;
      }

      if (curatedHit) {
        result = curatedHit[scriptShort(script)] || hit.pa;
        note = "This spelling is curated — it is how the name is actually written, " +
               "not a rule applied to the letters. Surnames like Singh are the reason " +
               "the list exists.";
        badge = "Curated spelling";
      } else {
        var r = fromEnglish(name);
        result = r.text;
        note = "This is the phonetic spelling — the rule engine read the sounds and " +
               "wrote them in " + scriptName() + ". For an uncommon name that is the best " +
               "answer there is, but have a native speaker confirm it before anything permanent.";
        badge = r.complete ? "Phonetic spelling" : "Phonetic spelling — partial";
      }

      lastText = result;
      out.innerHTML = '<div class="big" lang="' + script + '">' + esc(result) + "</div>" +
        '<div class="rom">' + esc(badge) + " · " + esc(name) + "</div>";
      if (btnrow) btnrow.hidden = false;
      if (help) help.textContent = note;
      if (explain && explain.getAttribute("data-open") === "1") showLetters(name, curatedHit);
      else if (explain) explain.innerHTML = "";
    }

    function scriptShort(s) {
      var map = {
        "gurmukhi": "pa", "devanagari": "hi",
        "arabic": "ar", "greek": "el", "cyrillic": "ru",
        "hangul": "ko", "kana": "ja", "ethiopic": "am"
      };
      return map[s] || s;
    }

    function scriptName() {
      var n;
      if (isNonIndic && window.EkGuruNonIndic) {
        n = window.EkGuruNonIndic.names[script];
      } else if (window.EkGuruScriptMap) {
        n = window.EkGuruScriptMap.names[script];
      }
      return n ? n.en : script;
    }

    function esc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }

    /* Letter-by-letter only for the rule path: a curated spelling is a
       whole word, and splitting it into letters would invent a story
       about why each letter is there.
       For non-Indic scripts the Devanagari intermediate is not a
       meaningful comparison, so we show the script's own characters
       and their codepoints instead. */
    function showLetters(name, hit) {
      if (hit) {
        explain.innerHTML = '<p class="rom" style="margin-top:12px">A curated spelling is kept as a ' +
          "whole word. There is no letter-by-letter rule to show, because the spelling did not " +
          "come from one.</p>";
        return;
      }
      var r = fromEnglish(name);
      if (isNonIndic) {
        var chars = Array.from(r.text);
        var rows = "";
        for (var i = 0; i < chars.length; i++) {
          rows += "<tr><td>" + esc(chars[i]) + '</td><td class="rom">U+' +
            chars[i].codePointAt(0).toString(16).toUpperCase() + "</td></tr>";
        }
        explain.innerHTML = '<table class="ex" style="margin-top:14px"><thead><tr><th>' +
          esc(scriptName()) + "</th><th>Codepoint</th></tr></thead><tbody>" + rows + "</tbody></table>";
        return;
      }
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
        var val = input.value.trim();
        var hitForExplain = curatedFor(val);
        if (hitForExplain && isNonIndic && !hitForExplain[scriptShort(script)]) hitForExplain = null;
        if (!open) showLetters(val, hitForExplain);
        else explain.innerHTML = "";
      });
    }

    /* Shareable link: /name-in-punjabi/?n=Simran (or ?q= / ?name=) opens
       with the answer already on screen — unified with /name-in-hindi/. */
    if (btnrow && !document.getElementById("shareLinkBtn")) {
      var shareBtn = document.createElement("button");
      shareBtn.type = "button";
      shareBtn.id = "shareLinkBtn";
      shareBtn.textContent = "Share link";
      shareBtn.addEventListener("click", function () {
        var typed = String(input.value || "").trim();
        if (!typed) return;
        var base = window.location.origin + window.location.pathname;
        var surl = base + "?n=" + encodeURIComponent(typed);
        var done = function () {
          shareBtn.textContent = "Link copied!";
          setTimeout(function () { shareBtn.textContent = "Share link"; }, 1600);
        };
        if (navigator.share) {
          navigator.share({
            title: typed + " in " + scriptName() + " — " + (lastText || ""),
            url: surl
          }).catch(function () {});
        } else if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(surl).then(done, done);
        } else {
          var ta = document.createElement("textarea");
          ta.value = surl;
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand("copy"); } catch (e) {}
          document.body.removeChild(ta);
          done();
        }
        try { if (window.EkGuruAnalytics) window.EkGuruAnalytics.event("name_share", script); } catch (e) {}
      });
      btnrow.appendChild(shareBtn);
    }

    try {
      var qp = new URLSearchParams(window.location.search);
      var q = qp.get("n") || qp.get("q") || qp.get("name");
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
