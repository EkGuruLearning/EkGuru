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
      if (r0 >= 0.5 && r0 <= 1.5) ttsRate = r0;
    } catch (eRate) {}
    var hindiVoice = null, voiceTried = false;
    function pickVoice() {
      if (voiceTried || !("speechSynthesis" in window)) return hindiVoice;
      voiceTried = true;
      try {
        var vs = window.speechSynthesis.getVoices() || [];
        for (var i = 0; i < vs.length; i++) {
          if (vs[i].lang && vs[i].lang.toLowerCase().indexOf("hi") === 0) {
            hindiVoice = vs[i]; break;
          }
        }
      } catch (e) {}
      return hindiVoice;
    }
    if ("speechSynthesis" in window) {
      try {
        window.speechSynthesis.getVoices();
        window.speechSynthesis.onvoiceschanged = function () {
          voiceTried = false; pickVoice();
        };
      } catch (e) {}
    }
    document.addEventListener("click", function (ev) {
      var b = ev.target.closest ? ev.target.closest(".spk,[data-sb-say]") : null;
      if (!b || !("speechSynthesis" in window)) return;
      ev.stopPropagation();
      ev.preventDefault();
      try {
        var text = b.getAttribute("data-sb-say") || b.textContent;
        var u = new SpeechSynthesisUtterance((text || "").trim());
        u.lang = "hi-IN"; u.rate = ttsRate;
        var v = pickVoice();
        if (v) u.voice = v;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
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

    /* ---- scroll reveal ---- */
    var targets = document.querySelectorAll(
      ".sb-reveal,.vcard,.trace-cell,.art h2,.pw h2,.answer h2,.ans h2," +
      ".sb-fig,.tracebox,.sb-band,.sb-callout," +
      ".bara-wrap,.art table,.pw table,.answer table,.ans table," +
      ".quiz details,.hs-card,.linklist li,.prevnext a");
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
        var RATES = [0.6, 0.85, 1, 1.25];
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
          pill.innerHTML = "🎙 <b>" + (RATES[ri] === 1 ? "1" : RATES[ri]) +
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
      if (!("speechSynthesis" in window)) return;
      var DEVA = /[\u0900-\u097F]/;
      var ONLY = /^[\u0900-\u097F\s\u200C\u200D।?!·,;:'"()\-–—\/]+$/;
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
        var phrases = t.match(/[\u0900-\u097F][\u0900-\u097F ]{0,41}/g) || [];
        var best = "";
        for (var pi = 0; pi < phrases.length; pi++) {
          var cand = phrases[pi].trim().replace(/ +/g, " ");
          if (cand.length > best.length) best = cand;
        }
        if (best.length < 2 || !/[अ-ह]/.test(best)) continue;
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
          toc.innerHTML = "<summary>On this page · इस पेज पर (" + h2s.length +
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
            if (!/^[\u0900-\u097F]+$/.test(w)) continue;
            if (STOP[w]) continue;
            if (seenW[w]) continue;
            seenW[w] = 1;
            words.push(w);
          }
        }
        if (words.length >= 3) {
          var keys = document.createElement("div");
          keys.className = "sb-keys";
          var kh = '<span class="sb-keys-label">Key words — tap to hear · सुनने के लिए दबाएँ:</span>';
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
  } catch (e) { /* storybook never breaks the page */ }
})();
