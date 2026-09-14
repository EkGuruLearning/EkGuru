/* EkGuru storybook interactions (v139) — flip cards, scroll reveal, TTS.
   No dependencies. Safe to include on any Hindi page: everything is
   guarded, degrades without IntersectionObserver/speechSynthesis, and
   never hides content when JS fails (gated on html.sb-js). */
(function () {
  "use strict";
  try {
    var reduceMotion = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.documentElement.classList.add("sb-js");

    /* ---- flip cards ---- */
    function bindFlip(scope) {
      var cards = (scope || document).querySelectorAll(".vcard");
      for (var i = 0; i < cards.length; i++) {
        (function (c) {
          if (c.getAttribute("data-sb-flip")) return;
          c.setAttribute("data-sb-flip", "1");
          if (!c.hasAttribute("tabindex")) c.setAttribute("tabindex", "0");
          if (!c.hasAttribute("role")) c.setAttribute("role", "button");
          c.addEventListener("click", function (ev) {
            if (ev.target.closest && ev.target.closest(".spk,.say")) return;
            c.classList.toggle("flip");
          });
          c.addEventListener("keydown", function (ev) {
            if (ev.key === "Enter" || ev.key === " ") {
              ev.preventDefault();
              c.classList.toggle("flip");
            }
          });
        })(cards[i]);
      }
    }
    bindFlip(document);

    /* ---- speech: any .spk / [data-say] speaks Hindi ----
       Rate is global + persisted: the speed pill writes
       ekguru_tts_rate and every speak uses it. */
    var RATE_KEY = "ekguru_tts_rate";
    var ttsRate = 0.85;
    try {
      var r0 = parseFloat(window.localStorage && localStorage.getItem(RATE_KEY));
      if (r0 >= 0.15 && r0 <= 1.5) ttsRate = r0;
    } catch (eRate) {}
    /* ---- page language (v151): every language speaks its own ----
       Derived from the URL: /languages/<code>/ uses the code,
       /learn/<indian-slug>/ maps to its ISO code, root /<slug>/
       topic hubs (v152) do the same, everything else is Hindi context. Latin-script pages keep pill+dock+themes
       but skip script-based buttons (English cannot be told apart
       from French by script, so guessing would mis-speak). */
    var LANG_SLUG = { bengali: "bn", gujarati: "gu", kannada: "kn",
      malayalam: "ml", marathi: "mr", punjabi: "pa", tamil: "ta",
      telugu: "te", urdu: "ur" };
    var SCRIPTS = {
      hi: "\\u0900-\\u097F", mr: "\\u0900-\\u097F", bn: "\\u0980-\\u09FF",
      pa: "\\u0A00-\\u0A7F", gu: "\\u0A80-\\u0AFF", ta: "\\u0B80-\\u0BFF",
      te: "\\u0C00-\\u0C7F", kn: "\\u0C80-\\u0CFF", ml: "\\u0D00-\\u0D7F",
      ur: "\\u0600-\\u06FF", ar: "\\u0600-\\u06FF", fa: "\\u0600-\\u06FF",
      he: "\\u0590-\\u05FF", ru: "\\u0400-\\u04FF", uk: "\\u0400-\\u04FF",
      th: "\\u0E00-\\u0E7F", ko: "\\uAC00-\\uD7AF\\u1100-\\u11FF",
      ja: "\\u3040-\\u309F\\u30A0-\\u30FF\\u4E00-\\u9FFF" };
    var pageLang = "hi", scriptRange = "";
    try {
      var langParts = (location.pathname || "").split("/");
      for (var langIdx = 0; langIdx < langParts.length; langIdx++) {
        if (langParts[langIdx] === "languages" && langParts[langIdx + 1]) {
          pageLang = langParts[langIdx + 1]; break;
        }
        if (langParts[langIdx] === "learn" && LANG_SLUG[langParts[langIdx + 1]]) {
          pageLang = LANG_SLUG[langParts[langIdx + 1]]; break;
        }
        if (langIdx === 1 && LANG_SLUG[langParts[langIdx]]) {
          pageLang = LANG_SLUG[langParts[langIdx]]; break;
        }
      }
      scriptRange = SCRIPTS[pageLang] || "";
    } catch (eLang) {}
    var RX_ANY = scriptRange ? new RegExp("[" + scriptRange + "]") : null;
    var RX_PHRASE = scriptRange ?
      new RegExp("[" + scriptRange + "][" + scriptRange + " ]{0,41}", "g") : null;
    var RX_WORD = scriptRange ?
      new RegExp("^[\\u200C\\u200D" + scriptRange + "]+$") : null;
    var pageVoice = null, voiceTried = false;
    function pickVoice() {
      if (voiceTried || !("speechSynthesis" in window)) return pageVoice;
      voiceTried = true;
      try {
        var vs = window.speechSynthesis.getVoices() || [];
        for (var i = 0; i < vs.length; i++) {
          if (vs[i].lang && (vs[i].lang.toLowerCase().indexOf(pageLang) === 0 ||
              (pageLang === "he" && vs[i].lang.toLowerCase().indexOf("iw") === 0))) {
            pageVoice = vs[i]; break;
          }
        }
      } catch (e) {}
      return pageVoice;
    }
    /* ---- voice nudge (v154): when this device has no voice for the
       page language, the browser falls back to its default voice — on
       Indian phones often Hindi — so Bengali/Tamil/French sound wrong.
       Say so honestly, once per language, with install steps. ---- */
    var LANG_NAMES = { hi: "Hindi", bn: "Bengali", gu: "Gujarati",
      kn: "Kannada", ml: "Malayalam", mr: "Marathi", pa: "Punjabi",
      ta: "Tamil", te: "Telugu", ur: "Urdu", ar: "Arabic", fr: "French",
      es: "Spanish", de: "German", ja: "Japanese", ko: "Korean",
      zh: "Chinese", ru: "Russian", pt: "Portuguese", it: "Italian",
      he: "Hebrew", th: "Thai", fa: "Persian", tr: "Turkish" };
    /* UI strings follow the page language (v154): TOC + key-words labels
       are no longer hardcoded Hindi. Unmapped codes fall back to
       English-only — never another language's words. */
    var UI_STRINGS = {
      hi: ["इस पेज पर", "सुनने के लिए दबाएँ"],
      bn: ["এই পাতায়", "শোনার জন্য চাপ দিন"],
      gu: ["આ પાના પર", "સાંભળવા માટે દબાવો"],
      kn: ["ಈ ಪುಟದಲ್ಲಿ", "ಕೇಳಲು ಒತ್ತಿರಿ"],
      ml: ["ഈ പേജിൽ", "കേൾക്കാൻ അമർത്തുക"],
      mr: ["या पानावर", "ऐकण्यासाठी दाबा"],
      pa: ["ਇਸ ਪੰਨੇ ’ਤੇ", "ਸੁਣਨ ਲਈ ਦਬਾਓ"],
      ta: ["இந்தப் பக்கத்தில்", "கேட்க அழுத்தவும்"],
      te: ["ఈ పేజీలో", "వినడానికి నొక్కండి"],
      ur: ["اس صفحے پر", "سننے کے لیے دبائیں"],
      ar: ["في هذه الصفحة", "اضغط للاستماع"],
      fr: ["Sur cette page", "Touchez pour écouter"],
      es: ["En esta página", "Toca para escuchar"],
      de: ["Auf dieser Seite", "Zum Anhören tippen"],
      ja: ["このページ", "タップして聞く"],
      ko: ["이 페이지에서", "탭하여 듣기"],
      zh: ["本页", "点击收听"],
      ru: ["На этой странице", "Нажмите, чтобы прослушать"],
      pt: ["Nesta página", "Toque para ouvir"],
      it: ["In questa pagina", "Tocca per ascoltare"],
      he: ["בדף זה", "הקש/י להאזנה"],
      th: ["ในหน้านี้", "แตะเพื่อฟัง"],
      fa: ["در این صفحه", "برای شنیدن ضربه بزنید"],
      tr: ["Bu sayfada", "Dinlemek için dokunun"] };
    function uiToc() {
      var s = UI_STRINGS[pageLang];
      return s ? "On this page · " + s[0] : "On this page";
    }
    function uiKeys() {
      var s = UI_STRINGS[pageLang];
      return s ? "Key words — tap to hear · " + s[1] + ":" : "Key words — tap to hear:";
    }
    function voiceNudge() {
      try {
        if (!("speechSynthesis" in window)) return;
        var vs0 = [];
        try { vs0 = window.speechSynthesis.getVoices() || []; } catch (eVs) {}
        if (!vs0.length) return; /* not enumerated yet; voiceschanged retries */
        if (pickVoice()) return; /* native voice present: stay silent */
        var apiOkNow = (typeof Audio !== "undefined") && !voiceApiFailed &&
          (typeof navigator === "undefined" || navigator.onLine !== false);
        if (apiOkNow) return; /* API voice covers this device: stay silent */
        var k = "ekguru_voice_nudge_" + pageLang, dismissed = false;
        try { dismissed = window.localStorage.getItem(k) === "1"; } catch (eLs) {}
        if (dismissed || document.querySelector(".sb-voicenudge")) return;
        var nm = LANG_NAMES[pageLang] || "this language";
        var bar = document.createElement("div");
        bar.className = "sb-voicenudge";
        bar.setAttribute("role", "note");
        var tx = document.createElement("span");
        tx.textContent = "🔊 No " + nm + " voice on this device, so speech may sound wrong. " +
          "Install one free: Android Settings → System → Languages → " +
          "Text-to-speech → Google TTS ⚙ → Install voice data.";
        var x = document.createElement("button");
        x.type = "button"; x.className = "sb-voicenudge-x";
        x.setAttribute("aria-label", "Dismiss");
        x.textContent = "Got it";
        x.addEventListener("click", function () {
          try { window.localStorage.setItem(k, "1"); } catch (eDs) {}
          if (bar.parentNode) bar.parentNode.removeChild(bar);
        });
        bar.appendChild(tx); bar.appendChild(x);
        var host = document.querySelector(".sb-chapter") || document.querySelector("h1");
        if (host && host.parentNode) host.parentNode.insertBefore(bar, host.nextSibling);
        else if (document.body) document.body.insertBefore(bar, document.body.firstChild);
      } catch (eN) {}
    }
    if ("speechSynthesis" in window) {
      try {
        window.speechSynthesis.getVoices();
        window.speechSynthesis.onvoiceschanged = function () {
          voiceTried = false; pickVoice(); voiceNudge();
        };
      } catch (e) {}
    }
    try { voiceNudge(); } catch (eNudge) {}
    /* ---- EkGuru Voice Engine (v156): free API voice + smart local ----
       Layer 1 (primary): Google Translate TTS audio — no key, no CORS
         problem (plain media playback), works even with ZERO local
         voices, which is exactly the "voice doesn't work" case.
       Layer 2 (fallback): speechSynthesis with RANKED voices
         (exact region > Google/Microsoft neural > prefix > default).
       Offline / API error / no Audio -> layer 2 automatically, and
       long text is chunked (raw TTS silently dies on long input).
       Exposed as window.EkGuruVoice for the practice/audio engines. */
    var voiceAudio = null, voiceRun = 0, voiceApiFailed = false,
    voiceKeep = null, voiceApiDeadUntil = 0;
    function voiceTl(base) {
      base = String(base || "hi").toLowerCase();
      if (base === "he") return "iw";
      if (base === "zh") return "zh-CN";
      return base;
    }
    function voiceChunk(text) {
      var t = String(text || "").replace(/\s+/g, " ").trim();
      if (!t) return [];
      if (t.length <= 190) return [t];
      var bits = t.split(/([\u0964?!\.\u3002\u061F\u06D4\n]+)/);
      var out = [], cur = "";
      for (var i = 0; i < bits.length; i++) {
        if ((cur + bits[i]).length > 190 && cur) { out.push(cur.trim()); cur = ""; }
        cur += bits[i];
      }
      if (cur.trim()) out.push(cur.trim());
      var fin = [];
      for (var j = 0; j < out.length; j++) {
        if (out[j].length <= 190) { fin.push(out[j]); continue; }
        var words = out[j].split(" "), wcur = "";
        for (var k = 0; k < words.length; k++) {
          if ((wcur + " " + words[k]).trim().length > 190 && wcur) { fin.push(wcur.trim()); wcur = ""; }
          wcur += " " + words[k];
        }
        if (wcur.trim()) fin.push(wcur.trim());
      }
      return fin;
    }
    function rankVoice(vs, base) {
      base = String(base || "hi").toLowerCase();
      var best = null, bs = -1, prefName = "";
      try {
        var pj = JSON.parse(window.localStorage.getItem("ekguru_voice_pref_" + base) || "null");
        if (pj && pj.name) prefName = pj.name;
      } catch (ePref) {}
      for (var i = 0; i < vs.length; i++) {
        var v = vs[i] || {};
        var l = String(v.lang || "").toLowerCase();
        if (!l) continue;
        var s = 0;
        if (l === base || l.indexOf(base + "-") === 0 || l.indexOf(base + "_") === 0) s += 100;
        else if (l.indexOf(base) === 0) s += 50;
        else if (base === "he" && l.indexOf("iw") === 0) s += 100;
        else continue;
        var nm = String(v.name || "").toLowerCase();
        if (nm.indexOf("google") > -1) s += 30;
        if (nm.indexOf("natural") > -1 || nm.indexOf("neural") > -1) s += 25;
        if (nm.indexOf("microsoft") > -1) s += 15;
        if (nm.indexOf("samsung") > -1) s += 10;
        if (v.default) s += 5;
        if (prefName && v.name === prefName) s += 1000;
        if (s > bs) { bs = s; best = v; }
      }
      return best;
    }
    function voiceStop() {
      voiceRun++;
      try { if (voiceKeep) clearInterval(voiceKeep); } catch (eK) {}
      voiceKeep = null;
      try { if (voiceAudio) voiceAudio.pause(); } catch (e) {}
      voiceAudio = null;
      try { if ("speechSynthesis" in window) window.speechSynthesis.cancel(); } catch (e) {}
    }
    function voiceSpeak(text, langTag, rate, onend) {
      var t = String(text || "").trim();
      if (!t) return false;
      voiceStop();
      var run = ++voiceRun;
      var base = String(langTag || "hi").split(/[-_]/)[0].toLowerCase() || "hi";
      function done(ok) { if (typeof onend === "function") { try { onend(ok); } catch (e) {} } }
      function localSpeak(str, forced) {
        try {
          if (!("speechSynthesis" in window) || typeof SpeechSynthesisUtterance === "undefined") {
            done(false); return false;
          }
          var u = new SpeechSynthesisUtterance(str);
          u.lang = langTag; u.rate = rate || 1;
          var rv = forced || null;
          if (!rv) { try { rv = rankVoice(window.speechSynthesis.getVoices() || [], base); } catch (e) {} }
          if (rv) u.voice = rv;
          var finished = false, keep = null;
          function fin(ok) {
            if (finished) return; finished = true;
            if (keep) { try { clearInterval(keep); } catch (e) {} }
            if (voiceKeep === keep) voiceKeep = null;
            done(ok);
          }
          try { u.onend = function () { fin(true); }; u.onerror = function () { fin(false); }; } catch (e) {}
          /* Chrome desktop freezes long utterances (~15s): resume keepalive. */
          try {
            if (window.speechSynthesis.resume) {
              keep = setInterval(function () { try { window.speechSynthesis.resume(); } catch (e) {} }, 5000);
              voiceKeep = keep;
            }
          } catch (e) {}
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(u);
          return true;
        } catch (e) { done(false); return false; }
      }
      /* API-dead memory: modern Chrome ORB-blocks the free endpoint, so
         after one real failure skip it for 7 days (retried automatically). */
      function apiDead() {
        if (Date.now() < voiceApiDeadUntil) return true;
        try {
          var v = parseInt(window.localStorage.getItem("ekguru_api_dead") || "0", 10);
          if (Date.now() < v) { voiceApiDeadUntil = v; return true; }
        } catch (e) {}
        return false;
      }
      function markApiDead() {
        voiceApiFailed = true;
        if (typeof navigator !== "undefined" && navigator.onLine === false) return;
        voiceApiDeadUntil = Date.now() + 7 * 86400000;
        try { window.localStorage.setItem("ekguru_api_dead", String(voiceApiDeadUntil)); } catch (e) {}
      }
      function apiAlive() {
        voiceApiFailed = false; voiceApiDeadUntil = 0;
        try { window.localStorage.removeItem("ekguru_api_dead"); } catch (e) {}
      }
      /* Layer 1: ranked local voice — instant, offline, neural when present. */
      var match = null;
      var canLocal = ("speechSynthesis" in window) && typeof SpeechSynthesisUtterance !== "undefined";
      if (canLocal) { try { match = rankVoice(window.speechSynthesis.getVoices() || [], base); } catch (e) {} }
      if (match) return localSpeak(t, match);
      /* Layer 2: free API audio — last resort for legacy browsers. */
      var useApi = (typeof Audio !== "undefined") &&
        (typeof navigator === "undefined" || navigator.onLine !== false) && !apiDead();
      if (!useApi) { var r0 = localSpeak(t); voiceNudge(); return r0; }
      var chunks = voiceChunk(t), ci = 0;
      function playNext() {
        if (run !== voiceRun) return;
        if (ci >= chunks.length) { done(true); return; }
        var remainder = chunks.slice(ci).join(" ");
        var au = null;
        try {
          au = new Audio();
          voiceAudio = au;
          au.preload = "auto";
          au.playbackRate = rate || 1;
          au.src = "https://translate.googleapis.com/translate_tts?ie=UTF-8&tl=" +
            encodeURIComponent(voiceTl(base)) + "&client=tw-ob&q=" + encodeURIComponent(chunks[ci]);
        } catch (e) { markApiDead(); voiceAudio = null; localSpeak(remainder); voiceNudge(); return; }
        var settled = false;
        function failToLocal() {
          if (settled || run !== voiceRun) return;
          settled = true;
          markApiDead(); voiceAudio = null; localSpeak(remainder); voiceNudge();
        }
        try {
          au.addEventListener("error", failToLocal);
          au.addEventListener("playing", apiAlive);
          au.addEventListener("ended", function () {
            if (run !== voiceRun) return;
            settled = true; apiAlive(); ci++; playNext();
          });
          var pr = au.play();
          if (pr && typeof pr.catch === "function") pr.catch(failToLocal);
        } catch (e) { failToLocal(); }
      }
      playNext();
      return true;
    }
    function listVoices(base) {
      var out = [], prefName = "";
      try {
        var pj = JSON.parse(window.localStorage.getItem("ekguru_voice_pref_" + base) || "null");
        if (pj && pj.name) prefName = pj.name;
      } catch (ePref) {}
      try {
        var vs = window.speechSynthesis.getVoices() || [];
        for (var i = 0; i < vs.length; i++) {
          var v = vs[i] || {}, l = String(v.lang || "").toLowerCase(), s = -1;
          if (l === base || l.indexOf(base + "-") === 0 || l.indexOf(base + "_") === 0) s = 100;
          else if (l.indexOf(base) === 0) s = 50;
          else if (base === "he" && l.indexOf("iw") === 0) s = 100;
          if (s < 0) continue;
          var nm = String(v.name || "").toLowerCase();
          if (nm.indexOf("google") > -1) s += 30;
          if (nm.indexOf("natural") > -1 || nm.indexOf("neural") > -1) s += 25;
          if (prefName && v.name === prefName) s += 1000;
          out.push({ name: v.name || "", lang: v.lang || "", score: s });
        }
        out.sort(function (a, b) { return b.score - a.score; });
      } catch (e) {}
      return out;
    }
    function voiceTry(text, langTag, rate, voiceName) {
      try {
        if (!("speechSynthesis" in window)) return false;
        var u = new SpeechSynthesisUtterance(String(text || "").trim());
        u.lang = langTag; u.rate = rate || 1;
        var vs = window.speechSynthesis.getVoices() || [];
        for (var i = 0; i < vs.length; i++) {
          if (vs[i] && vs[i].name === voiceName) { u.voice = vs[i]; break; }
        }
        voiceStop();
        window.speechSynthesis.speak(u);
        return true;
      } catch (e) { return false; }
    }
    try {
      window.EkGuruVoice = { speak: voiceSpeak, stop: voiceStop,
        _chunk: voiceChunk, _rank: rankVoice, _tl: voiceTl,
        _list: listVoices, _try: voiceTry,
        apiFailed: function () { return !!voiceApiFailed; } };
    } catch (eVoice) {}
    document.addEventListener("click", function (ev) {
      var b = ev.target.closest ? ev.target.closest(".spk,[data-sb-say]") : null;
      if (!b) return;
      if (!("speechSynthesis" in window) && typeof Audio === "undefined") return;
      ev.stopPropagation();
      ev.preventDefault();
      voiceNudge();
      try {
        var text = b.getAttribute("data-sb-say") || b.textContent;
        voiceSpeak((text || "").trim(), pageLang === "hi" ? "hi-IN" : pageLang, ttsRate);
        try {
          b.classList.add("tapped");
          setTimeout(function () { b.classList.remove("tapped"); }, 550);
        } catch (eTap) {}
      } catch (e) {}
    });

    /* ---- trace grids: [data-traces] renders self-drawing letters ----
       data-traces="अ,आ,इ"  data-roman="a,aa,i" (parallel, comma lists) */
    (function traces() {
      var grids = document.querySelectorAll("[data-traces]");
      for (var g = 0; g < grids.length; g++) {
        var letters = (grids[g].getAttribute("data-traces") || "").split(",");
        var romans = (grids[g].getAttribute("data-roman") || "").split(",");
        var html = "";
        for (var i = 0; i < letters.length; i++) {
          var L = (letters[i] || "").trim();
          if (!L) continue;
          var R = ((romans[i] || "").trim() || "·");
          html += '<div class="trace-cell" style="transition-delay:' + Math.min(i, 12) * 45 + 'ms">' +
            '<svg viewBox="0 0 80 80" aria-hidden="true"><text x="40" y="62">' +
            L.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</text></svg>" +
            '<span class="rm">' + R.replace(/</g, "&lt;") + "</span>" +
            '<button class="say" data-sb-say="' + L.replace(/"/g, "&quot;") + '">🔊</button></div>';
        }
        grids[g].innerHTML = html;
      }
    })();

    /* ---- barakhadi lab: [data-bara] renders the 12-form chart ----
       Consonants × the 12 matra signs; varga filter buttons switch rows. */
    (function bara() {
      var host = document.querySelector("[data-bara]");
      if (!host) return;
      var MATRA = ["", "ा", "ि", "ी", "ु", "ू", "ृ", "े", "ै", "ो", "ौ", "ं", "ः"];
      var VROM = ["a", "aa", "i", "ee", "u", "oo", "ri", "e", "ai", "o", "au", "an", "ah"];
      var VARGAS = [
        { n: "क वर्ग · throat", rows: [["क", "k"], ["ख", "kh"], ["ग", "g"], ["घ", "gh"], ["ङ", "ng"]] },
        { n: "च वर्ग · palate", rows: [["च", "ch"], ["छ", "chh"], ["ज", "j"], ["झ", "jh"], ["ञ", "ny"]] },
        { n: "ट वर्ग · roof", rows: [["ट", "ṭ"], ["ठ", "ṭh"], ["ड", "ḍ"], ["ढ", "ḍh"], ["ण", "ṇ"]] },
        { n: "त वर्ग · teeth", rows: [["त", "t"], ["थ", "th"], ["द", "d"], ["ध", "dh"], ["न", "n"]] },
        { n: "प वर्ग · lips", rows: [["प", "p"], ["फ", "ph"], ["ब", "b"], ["भ", "bh"], ["म", "m"]] },
        { n: "अंतस्थ + ऊष्म · rest", rows: [["य", "y"], ["र", "r"], ["ल", "l"], ["व", "v"], ["श", "sh"], ["ष", "sh"], ["स", "s"], ["ह", "h"]] }
      ];
      var btns = document.createElement("div");
      btns.className = "bara-btns";
      var wrap = document.createElement("div");
      wrap.className = "bara-wrap";
      host.appendChild(btns);
      host.appendChild(wrap);
      function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;"); }
      function render(vi) {
        var h = '<table class="bara"><caption>Tap any cell to hear it. 12 forms × ' +
          VARGAS[vi].rows.length + " letters.</caption><thead><tr><th></th>";
        for (var m = 0; m < 13; m++) h += "<th>" + VROM[m] + "</th>";
        h += "</tr></thead><tbody>";
        var rows = VARGAS[vi].rows;
        for (var r = 0; r < rows.length; r++) {
          h += "<tr><th>" + esc(rows[r][0]) + "</th>";
          for (var c = 0; c < 13; c++) {
            var form = rows[r][0] + MATRA[c];
            var rom = rows[r][1] + VROM[c];
            h += '<td><button data-sb-say="' + esc(form) + '">' + esc(form) +
              "<small>" + esc(rom) + "</small></button></td>";
          }
          h += "</tr>";
        }
        wrap.innerHTML = h + "</tbody></table>";
        var all = btns.querySelectorAll("button");
        for (var b = 0; b < all.length; b++) {
          all[b].classList.toggle("on", b === vi);
        }
      }
      for (var v = 0; v < VARGAS.length; v++) {
        (function (vi) {
          var btn = document.createElement("button");
          btn.type = "button";
          btn.textContent = VARGAS[vi].n;
          btn.addEventListener("click", function () { render(vi); });
          btns.appendChild(btn);
        })(v);
      }
      render(0);
    })();

    /* ---- theme lift (v154): the banner palette becomes the page
       palette, so headings/tables/buttons follow the content theme. ---- */
    try {
      var chEl = document.querySelector(".sb-chapter");
      if (chEl && document.body) {
        var chAc = "", chTi = "";
        try { chAc = chEl.style.getPropertyValue("--sb-accent") || ""; } catch (eA) {}
        try { chTi = chEl.style.getPropertyValue("--sb-tint") || ""; } catch (eT) {}
        if ((!chAc || !chTi) && window.getComputedStyle) {
          try {
            var chCs = window.getComputedStyle(chEl);
            chAc = chAc || chCs.getPropertyValue("--sb-accent") || "";
            chTi = chTi || chCs.getPropertyValue("--sb-tint") || "";
          } catch (eC) {}
        }
        if (chAc) document.body.style.setProperty("--sb-accent", chAc.trim());
        if (chTi) document.body.style.setProperty("--sb-tint", chTi.trim());
      }
    } catch (eTheme) {}
    /* ---- scroll reveal ---- */
    var targets = document.querySelectorAll(
      ".sb-reveal,.vcard,.trace-cell,.art h2,.pw h2,.answer h2,.ans h2," +
      ".sb-fig,.tracebox,.sb-band,.sb-callout," +
      ".bara-wrap,.art table,.pw table,.answer table,.ans table," +
      ".quiz details,.hs-card,.linklist li,.prevnext a," +
      ".lang-cell,.v-item,.ob-card,.card,.fact,.howto,.faq");
    if ("IntersectionObserver" in window && !reduceMotion) {
      var io = new IntersectionObserver(function (entries) {
        for (var i = 0; i < entries.length; i++) {
          if (entries[i].isIntersecting) {
            entries[i].target.classList.add("shown");
            io.unobserve(entries[i].target);
          }
        }
      }, { threshold: 0.12 });
      for (var j = 0; j < targets.length; j++) {
        var t = targets[j];
        var sibs = t.parentNode ? t.parentNode.children : [];
        var idx = Array.prototype.indexOf.call(sibs, t);
        if (idx > 0) t.style.transitionDelay = Math.min(idx, 8) * 55 + "ms";
        io.observe(t);
      }
    } else {
      for (var k = 0; k < targets.length; k++) {
        targets[k].classList.add("shown");
      }
    }

    /* ---- speed pill: one global TTS speed control (v142) ----
       Fixed bottom-right, cycles 0.6× → 0.85× → 1× → 1.25×.
       Label is English-first so foreign learners get it; title
       carries the Hindi. Shown whenever speech works. */
    if ("speechSynthesis" in window) {
      try {
        var RATES = [0.2, 0.4, 0.6, 0.85, 1, 1.25];
        var pill = document.createElement("button");
        pill.type = "button";
        pill.className = "sb-speed";
        pill.title = "Speech speed · बोलने की गति — tap to change";
        pill.setAttribute("aria-label", "Change speech speed");
        var ri = 0;
        for (var q = 0; q < RATES.length; q++) {
          if (Math.abs(RATES[q] - ttsRate) < 0.01) ri = q;
        }
        function paintRate() {
          ttsRate = RATES[ri];
          var icon = RATES[ri] < 0.6 ? "🐢" : (RATES[ri] >= 1 ? "🐇" : "🎙");
          pill.innerHTML = icon + " <b>" + (RATES[ri] === 1 ? "1" : RATES[ri]) +
            "×</b> <span>speed</span>";
          try {
            if (window.localStorage) localStorage.setItem(RATE_KEY, String(RATES[ri]));
          } catch (e) {}
        }
        paintRate();
        pill.addEventListener("click", function (ev) {
          ev.stopPropagation();
          ri = (ri + 1) % RATES.length;
          paintRate();
        });
        document.body.appendChild(pill);
      } catch (e) {}
    }

    /* ---- auto-mount: Devanagari cells get a speaker (v142) ----
       Any .art td/li/strong/quiz-summary that is pure short
       Devanagari text and has no interactive child gets a mini 🔊. Skips links and
       buttons (barakhadi cells already speak). Capped so giant
       tables stay fast. */
    (function autoSpeak() {
      if (!("speechSynthesis" in window) || !RX_ANY) return;
      var DEVA = RX_ANY;
      /* Wrappers differ by section — always the OUTER one, because
         on ask/answers pages the h2s and lists live outside the
         inner .answer/.ans: .art (learn/materials), .pw
         (hindi/toolbox/daily-hindi/global), .qw (ask), .aw (answers). */
      /* p and linklist spans join the list: the pure-Devanagari +
         42-char gates keep long/mixed text untouched. */
      var els = document.querySelectorAll(
        ".art td,.art li,.art strong,.art p,.art .quiz summary," +
        ".pw td,.pw li,.pw strong,.pw p,.qw td,.qw li,.qw strong,.qw p," +
        ".aw td,.aw li,.aw strong,.aw p,.art .linklist span");
      var added = 0;
      for (var i = 0; i < els.length && added < 80; i++) {
        var el = els[i];
        if (el.querySelector("a,button,input,select,textarea,[data-sb-say]")) continue;
        var t = (el.textContent || "").replace(/\s+/g, " ").trim();
        if (t.length < 1 || t.length > 120 || !DEVA.test(t)) continue;
        /* Speak the longest Hindi phrase inside — pure lines speak
           whole, mixed lines ("1 — एक (ek)") speak just "एक". The
           Hindi voice never has to chew English. */
        var phrases = RX_PHRASE ? (t.match(RX_PHRASE) || []) : [];
        var best = "";
        for (var pi = 0; pi < phrases.length; pi++) {
          var cand = phrases[pi].trim().replace(/ +/g, " ");
          if (cand.length > best.length) best = cand;
        }
        if (best.length < 2) continue;
        var b = document.createElement("button");
        b.type = "button";
        b.className = "say say-auto";
        b.setAttribute("data-sb-say", best);
        b.setAttribute("aria-label", "Listen: " + best);
        b.textContent = "🔊";
        el.appendChild(document.createTextNode(" "));
        el.appendChild(b);
        added++;
      }
    })();

    /* ---- marquee: duplicate strip content for a seamless loop ---- */
    var strips = document.querySelectorAll(".sb-strip .row");
    for (var s = 0; s < strips.length; s++) {
      strips[s].innerHTML += strips[s].innerHTML;
    }

    /* ---- hero parallax: floats drift with the pointer (desktop) ---- */
    if (!reduceMotion && window.matchMedia &&
        window.matchMedia("(pointer: fine)").matches) {
      var heroes = document.querySelectorAll(".sb-hero,.sb-scene");
      for (var m = 0; m < heroes.length; m++) {
        (function (hero) {
          var floats = hero.querySelectorAll(".sb-float");
          if (!floats.length) return;
          var raf = null;
          hero.addEventListener("mousemove", function (ev) {
            if (raf) return;
            raf = requestAnimationFrame(function () {
              raf = null;
              var r = hero.getBoundingClientRect();
              var dx = (ev.clientX - r.left) / r.width - 0.5;
              var dy = (ev.clientY - r.top) / r.height - 0.5;
              for (var f = 0; f < floats.length; f++) {
                var depth = 6 + (f % 3) * 6;
                floats[f].style.marginLeft = (-dx * depth) + "px";
                floats[f].style.marginTop = (-dy * depth) + "px";
              }
            });
          });
          hero.addEventListener("mouseleave", function () {
            for (var f = 0; f < floats.length; f++) {
              floats[f].style.marginLeft = "";
              floats[f].style.marginTop = "";
            }
          });
        })(heroes[m]);
      }
    }

    /* ---- ultra visuals (v145): progress, TOC, key words, mastery, confetti ----
       Everything here is DERIVED from the page itself or the visitor's
       own device data. No invented content, ever. Each block is wrapped
       so one failure cannot stop the others. */
    try {
      var segs = (location.pathname || "").split("/");
      document.body.setAttribute("data-section", segs[1] || "home");
      if (segs[1] === "learn" && segs[2]) {
        document.body.setAttribute("data-sub", segs[2]);
      }
    } catch (e0) {}

    /* reading progress bar */
    try {
      var prog = document.createElement("div");
      prog.className = "sb-progress";
      prog.setAttribute("aria-hidden", "true");
      var progFill = document.createElement("i");
      prog.appendChild(progFill);
      document.body.appendChild(prog);
      var progTick = false;
      function progUpdate() {
        progTick = false;
        var h = document.documentElement;
        var max = h.scrollHeight - h.clientHeight;
        if (max < 60) { prog.style.display = "none"; return; }
        var st = h.scrollTop || document.body.scrollTop || 0;
        var p = Math.max(0, Math.min(1, st / max));
        progFill.style.width = (p * 100).toFixed(1) + "%";
      }
      window.addEventListener("scroll", function () {
        if (progTick) return;
        progTick = true;
        if (window.requestAnimationFrame) window.requestAnimationFrame(progUpdate);
        else setTimeout(progUpdate, 80);
      });
      progUpdate();
    } catch (e1) {}

    /* auto table of contents from the page's own h2s */
    try {
      var wrap = document.querySelector(".art,.pw,.qw,.aw");
      if (wrap) {
        var h2s = wrap.querySelectorAll("h2");
        if (h2s.length >= 3) {
          var toc = document.createElement("details");
          toc.className = "sb-toc";
          toc.setAttribute("open", "");
          var shown = Math.min(h2s.length, 14);
          var ol = "";
          for (var ti = 0; ti < shown; ti++) {
            var hid = "sb-s" + (ti + 1);
            h2s[ti].setAttribute("id", hid);
            var ht = (h2s[ti].textContent || "").replace(/\s+/g, " ").trim().slice(0, 70);
            ol += '<li><a href="#' + hid + '">' +
              ht.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</a></li>";
          }
          if (h2s.length > shown) {
            ol += '<li class="more">+' + (h2s.length - shown) + " more below ↓</li>";
          }
          toc.innerHTML = "<summary>" + uiToc() + " (" + h2s.length +
            ")</summary><ol>" + ol + "</ol>";
          var tocAnchor = wrap.querySelector(".sb-hint") || wrap.querySelector("h1");
          if (tocAnchor && tocAnchor.parentNode) {
            tocAnchor.parentNode.insertBefore(toc, tocAnchor.nextSibling);
          } else if (wrap.firstChild) {
            wrap.insertBefore(toc, wrap.firstChild);
          }
        }
      }
    } catch (e2) {}

    /* key-words strip: the page's own Hindi words as TTS chips */
    try {
      var wrap2 = document.querySelector(".art,.pw,.qw,.aw");
      if (wrap2) {
        var seenW = {}, words = [];
        var STOP = {"मैं": 1, "हम": 1, "तुम": 1, "आप": 1, "वह": 1, "वे": 1,
          "यह": 1, "ये": 1, "वो": 1, "जो": 1, "है": 1, "हैं": 1, "हूँ": 1,
          "हूं": 1, "हो": 1, "हों": 1, "था": 1, "थे": 1, "थी": 1, "थीं": 1};
        var knodes = wrap2.querySelectorAll("p,li,td");
        var TRIMRE = /^[।?!·,;:'"“”‘’()\[\]–—-]+|[।?!·,;:'"“”‘’()\[\]–—-]+$/g;
        for (var ni = 0; ni < knodes.length && words.length < 14; ni++) {
          var chunks = (knodes[ni].textContent || "").split(/\s+/);
          for (var ci = 0; ci < chunks.length && words.length < 14; ci++) {
            var w = chunks[ci].replace(TRIMRE, "");
            TRIMRE.lastIndex = 0;
            if (w.length < 2 || w.length > 24) continue;
            if (!RX_WORD || !RX_WORD.test(w)) continue;
            if (STOP[w]) continue;
            if (seenW[w]) continue;
            seenW[w] = 1;
            words.push(w);
          }
        }
        if (words.length >= 3) {
          var keys = document.createElement("div");
          keys.className = "sb-keys";
          var kh = '<span class="sb-keys-label">' + uiKeys() + '</span>';
          for (var wi = 0; wi < words.length; wi++) {
            var we = words[wi].replace(/&/g, "&amp;");
            kh += ' <button type="button" class="say" data-sb-say="' +
              we.replace(/"/g, "&quot;") + '">🔊 ' + we.replace(/</g, "&lt;") + "</button>";
          }
          keys.innerHTML = kh;
          var kAnchor = wrap2.querySelector(".sb-toc") ||
            wrap2.querySelector(".sb-hint") || wrap2.querySelector("h1");
          if (kAnchor && kAnchor.parentNode) {
            kAnchor.parentNode.insertBefore(keys, kAnchor.nextSibling);
          }
        }
      }
    } catch (e3) {}

    /* practice stats strip: the visitor's OWN device data, read-only */
    try {
      if (location.pathname.indexOf("/practice") > -1) {
        var store = {};
        try { store = JSON.parse(window.localStorage.getItem("ekguru_mastery_v1") || "{}") || {}; }
        catch (e3b) { store = {}; }
        var w3 = document.querySelector(".art,.pw,.qw,.aw") || document.body;
        var mdiv = document.createElement("div");
        mdiv.className = "sb-mastery";
        var ids = Object.keys(store);
        if (!ids.length) {
          mdiv.innerHTML = "📊 <b>Your progress saves on this device.</b> " +
            "Finish a round below and your stats appear here.";
        } else {
          var touched = ids.length, answers = 0, days = {};
          for (var mi = 0; mi < ids.length; mi++) {
            var rec = store[ids[mi]] || {};
            answers += Number(rec.seen) || 0;
            if (rec.last) {
              var dd = new Date(rec.last);
              days[dd.getFullYear() + "-" + dd.getMonth() + "-" + dd.getDate()] = 1;
            }
          }
          var dayCount = Object.keys(days).length;
          function dkey(d) { return d.getFullYear() + "-" + d.getMonth() + "-" + d.getDate(); }
          var streak = 0;
          var cursor = new Date();
          if (!days[dkey(cursor)]) cursor = new Date(cursor.getTime() - 86400000);
          while (days[dkey(cursor)]) {
            streak++;
            cursor = new Date(cursor.getTime() - 86400000);
          }
          mdiv.innerHTML = "📊 <b>Your practice on this device:</b> " + touched +
            " words touched · " + answers + " answers · " + dayCount +
            " day" + (dayCount === 1 ? "" : "s") +
            (streak > 1 ? ' · <b class="sb-streak">🔥 ' + streak + "-day streak</b>" : "");
        }
        var mAnchor = w3.querySelector ? (w3.querySelector(".sb-hint") || w3.querySelector("h1")) : null;
        if (mAnchor && mAnchor.parentNode) {
          mAnchor.parentNode.insertBefore(mdiv, mAnchor.nextSibling);
        } else if (w3.firstChild) {
          w3.insertBefore(mdiv, w3.firstChild);
        }
      }
    } catch (e4) {}

    /* celebration when a practice round finishes */
    try {
      var pxRoot = document.getElementById("practice-root");
      if (pxRoot && "MutationObserver" in window && !reduceMotion) {
        var celebrated = false;
        var raf2 = window.requestAnimationFrame || function (f) { return setTimeout(f, 16); };
        function burstFn() {
          var cv = document.createElement("canvas");
          cv.className = "sb-confetti";
          cv.width = window.innerWidth; cv.height = window.innerHeight;
          document.body.appendChild(cv);
          var cx = cv.getContext("2d");
          if (!cx) { cv.parentNode.removeChild(cv); return; }
          var cols = ["#4f32d9", "#c2407d", "#ffb703", "#2a9d8f", "#e63946"];
          var ps = [];
          for (var cpi = 0; cpi < 130; cpi++) {
            ps.push({ x: cv.width / 2, y: cv.height * 0.35,
              vx: (Math.random() - 0.5) * 14, vy: Math.random() * -11 - 3,
              s: Math.random() * 7 + 3, c: cols[cpi % cols.length], r: Math.random() * 6.28 });
          }
          var t0 = Date.now();
          (function frame() {
            var el = Date.now() - t0;
            cx.clearRect(0, 0, cv.width, cv.height);
            for (var ki = 0; ki < ps.length; ki++) {
              var p = ps[ki];
              p.vy += 0.35; p.x += p.vx; p.y += p.vy; p.r += 0.1;
              cx.save(); cx.translate(p.x, p.y); cx.rotate(p.r);
              cx.fillStyle = p.c;
              cx.globalAlpha = el > 1600 ? Math.max(0, 1 - (el - 1600) / 800) : 1;
              cx.fillRect(-p.s / 2, -p.s / 4, p.s, p.s / 2);
              cx.restore();
            }
            if (el < 2500) { raf2(frame); }
            else if (cv.parentNode) { cv.parentNode.removeChild(cv); }
          })();
        }
        var obs = new MutationObserver(function () {
          var done = pxRoot.querySelector(".px-done");
          if (done && !celebrated) { celebrated = true; try { burstFn(); } catch (e5) {} }
          if (!done) { celebrated = false; }
        });
        obs.observe(pxRoot, { childList: true, subtree: true });
      }
    } catch (e6) {}
    /* chapter theming (v147): the baked banner carries the
       chapter palette; copy it to the page so progress bar, TOC,
       key-words and background all follow the chapter. */
    try {
      var ch = document.querySelector(".sb-chapter");
      if (ch && ch.style && ch.style.getPropertyValue) {
        var acc = ch.style.getPropertyValue("--sb-accent");
        var tint = ch.style.getPropertyValue("--sb-tint");
        if (acc) document.body.style.setProperty("--sb-accent", acc);
        if (tint) {
          document.body.style.setProperty("--sb-tint", tint);
          document.body.classList.add("sb-themed");
        }
      }
    } catch (e7) {}

    /* ---- voice picker panel (v157): choose the exact voice ----
       Lists every on-device voice for the page language with Try
       buttons; the pick persists per language and wins ranking. */
    function voiceBase() {
      return String(pageLang || "hi").split(/[-_]/)[0].toLowerCase() || "hi";
    }
    function voicePrefKey(b) { return "ekguru_voice_pref_" + b; }
    function closeVoicePanel() {
      try {
        var p = document.querySelector(".sb-vpanel");
        if (p && p.parentNode) p.parentNode.removeChild(p);
      } catch (e) {}
    }
    function openVoicePanel() {
      try {
        closeVoicePanel();
        var base = voiceBase();
        var nm = (typeof LANG_NAMES !== "undefined" && LANG_NAMES[base]) || "this language";
        var list = [];
        try { list = window.EkGuruVoice._list(base) || []; } catch (e) {}
        var pref = null;
        try { pref = JSON.parse(window.localStorage.getItem(voicePrefKey(base)) || "null"); } catch (e) {}
        var pan = document.createElement("div");
        pan.className = "sb-vpanel";
        pan.setAttribute("role", "dialog");
        pan.setAttribute("aria-label", "Choose voice");
        var hd = document.createElement("div"); hd.className = "sb-vpanel-h";
        var tt = document.createElement("b"); tt.textContent = "🎙 Voice for " + nm;
        var xx = document.createElement("button");
        xx.type = "button"; xx.className = "sb-vpanel-x";
        xx.textContent = "✕"; xx.setAttribute("aria-label", "Close");
        xx.addEventListener("click", closeVoicePanel);
        hd.appendChild(tt); hd.appendChild(xx); pan.appendChild(hd);
        var box = document.createElement("div"); box.className = "sb-vpanel-list";
        if (!list.length) {
          var em = document.createElement("p"); em.className = "sb-vpanel-empty";
          em.textContent = "No " + nm + " voice on this device yet — speech uses the default voice. " +
            "Install one free: Android Settings → System → Languages → Text-to-speech → Google TTS ⚙ → Install voice data.";
          box.appendChild(em);
        }
        for (var i = 0; i < list.length; i++) {
          (function (it) {
            var row = document.createElement("div"); row.className = "sb-vpanel-row";
            var isPref = !!(pref && it.name === pref.name);
            if (isPref) row.className += " is-pref";
            var lb = document.createElement("span"); lb.className = "sb-vpanel-name";
            lb.textContent = (it.name || it.lang) + " · " + it.lang + (isPref ? " ✓" : "");
            var tryB = document.createElement("button");
            tryB.type = "button"; tryB.className = "sb-vpanel-try"; tryB.textContent = "Try";
            tryB.addEventListener("click", function () {
              var sample = "Hello";
              try {
                var f = document.querySelector("[data-sb-say]");
                if (f) sample = ((f.getAttribute("data-sb-say") || f.textContent) || "Hello").trim() || "Hello";
              } catch (e) {}
              try { window.EkGuruVoice._try(sample, pageLang === "hi" ? "hi-IN" : pageLang, ttsRate, it.name); } catch (e) {}
            });
            var useB = document.createElement("button");
            useB.type = "button"; useB.className = "sb-vpanel-use";
            useB.textContent = isPref ? "Using" : "Use";
            if (!isPref) useB.addEventListener("click", function () {
              try {
                window.localStorage.setItem(voicePrefKey(base),
                  JSON.stringify({ name: it.name, lang: it.lang }));
              } catch (e) {}
              openVoicePanel();
            });
            row.appendChild(lb); row.appendChild(tryB); row.appendChild(useB);
            box.appendChild(row);
          })(list[i]);
        }
        pan.appendChild(box);
        document.body.appendChild(pan);
        setTimeout(function () { try { pan.classList.add("in"); } catch (e) {} }, 30);
      } catch (e) {}
    }
    /* ---- app dock (v150): Back · Home · Next/Up on every page ----
       All targets derived — history, the page's own prevnext chain,
       URL parents. Nothing invented, nothing hardcoded. */
    try {
      var dock = document.createElement("nav");
      dock.className = "sb-dock";
      dock.setAttribute("aria-label", "Page navigation");
      /* Site root from our own script URL: correct on a domain root
         and on a /subpath/ deploy alike. */
      var sbRoot = "/";
      try {
        var meSrc = document.currentScript && document.currentScript.src;
        if (meSrc && meSrc.indexOf("/js/storybook.js") > -1) {
          sbRoot = meSrc.split("/js/storybook.js")[0] + "/";
        }
      } catch (eD0) {}
      var dSegs = (location.pathname || "").split("/").filter(function (x) { return !!x; });
      var upHref = dSegs.length > 1 ? "../" : "";
      /* Next = the page's own "Next →" link when it has one (topic
         chain), else Up to the parent section. */
      var nxHref = "", nxLabel = "Up ↑";
      var pnx = document.querySelectorAll(".prevnext a");
      for (var pni = 0; pni < pnx.length; pni++) {
        if ((pnx[pni].textContent || "").indexOf("Next") > -1) {
          nxHref = pnx[pni].getAttribute("href") || "";
          nxLabel = "Next →";
          break;
        }
      }
      if (!nxHref) nxHref = upHref;
      function dockBtn(href, label, cls, act) {
        var a = document.createElement("a");
        a.className = "sb-dock-btn " + cls;
        a.textContent = label;
        a.setAttribute("href", href || "#");
        if (act) a.setAttribute("data-act", act);
        return a;
      }
      dock.appendChild(dockBtn("#", "← Back", "sb-d-back", "back"));
      dock.appendChild(dockBtn(sbRoot, "🏠 Home", "sb-d-home", ""));
      if (nxHref) dock.appendChild(dockBtn(nxHref, nxLabel, "sb-d-next", ""));
      var vb = dockBtn("#", "\uD83C\uDFA4", "sb-d-voice", "voice");
      vb.setAttribute("aria-label", "Choose voice");
      vb.title = "Choose voice";
      dock.appendChild(vb);
      document.body.appendChild(dock);
      dock.addEventListener("click", function (ev) {
        var a = ev.target.closest ? ev.target.closest("a") : null;
        if (!a) return;
        if (a.getAttribute("data-act") === "voice") {
          ev.preventDefault();
          try {
            if (document.querySelector(".sb-vpanel")) closeVoicePanel();
            else openVoicePanel();
          } catch (eDV) {}
          return;
        }
        if (a.getAttribute("data-act") === "back") {
          ev.preventDefault();
          try {
            if (window.history && history.length > 1) { history.back(); return; }
          } catch (eD1) {}
          if (upHref) location.href = upHref;
          return;
        }
        var href = a.getAttribute("href");
        if (!href || href === "#" || reduceMotion) return;
        ev.preventDefault();
        try { document.body.classList.add("sb-leaving"); } catch (eD2) {}
        setTimeout(function () { location.href = href; }, 180);
      });
      setTimeout(function () { try { dock.classList.add("in"); } catch (eD3) {} }, 60);
    } catch (e8) {}
  } catch (e) { /* storybook never breaks the page */ }
})();
