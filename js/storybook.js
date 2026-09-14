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
        u.lang = "hi-IN"; u.rate = 0.85;
        var v = pickVoice();
        if (v) u.voice = v;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
      } catch (e) {}
    });

    /* ---- scroll reveal ---- */
    var targets = document.querySelectorAll(
      ".sb-reveal,.vcard,.art h2,.sb-fig,.tracebox,.sb-band,.sb-callout," +
      ".art table,.quiz details,.hs-card,.linklist li,.prevnext a");
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
