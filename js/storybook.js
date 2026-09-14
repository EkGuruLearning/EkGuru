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

    /* ---- speech: any .spk / [data-say] speaks Hindi ---- */
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
      ".sb-reveal,.vcard,.trace-cell,.art h2,.sb-fig,.tracebox,.sb-band,.sb-callout," +
      ".bara-wrap,.art table,.quiz details,.hs-card,.linklist li,.prevnext a");
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
      var els = document.querySelectorAll(".art td,.art li,.art strong,.art .quiz summary");
      var added = 0;
      for (var i = 0; i < els.length && added < 80; i++) {
        var el = els[i];
        if (el.querySelector("a,button,input,select,textarea,[data-sb-say]")) continue;
        var t = (el.textContent || "").replace(/\s+/g, " ").trim();
        if (t.length < 1 || t.length > 42 || !DEVA.test(t) || !ONLY.test(t)) continue;
        var b = document.createElement("button");
        b.type = "button";
        b.className = "say say-auto";
        b.setAttribute("data-sb-say", t);
        b.setAttribute("aria-label", "Listen: " + t);
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
  } catch (e) { /* storybook never breaks the page */ }
})();
