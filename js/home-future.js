/* =========================================================
   EkGuru — HOME FUTURE LAYER (progressive enhancement)
   ---------------------------------------------------------
   Home page only. Everything here is an enhancement: with JS
   off, reduced motion on, or any API missing, the static page
   is complete without it. Three jobs:
     1. motion consent + scroll/reveal choreography
        (css/home-future.css owns the actual keyframes);
     2. header shadow after scrolling;
     3. a small Hindi practice widget in the hero — real
        words, transliteration, meaning, and (where the
        device has a Hindi voice) a listen button.
   No network, no storage, nothing uploaded.
   ========================================================= */
(function () {
  "use strict";
  var doc = document;
  var root = doc.documentElement;
  var reduceMotion = typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = typeof window.matchMedia === "function" &&
    window.matchMedia("(pointer: fine)").matches;

  /* ---- 1. motion + reveal ---- */
  if (!reduceMotion) {
    root.classList.add("hf-on");
    var revealEls = doc.querySelectorAll(".xp-sec, .xp-rail");
    if ("IntersectionObserver" in window && revealEls.length) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("hf-in"); io.unobserve(en.target); }
        });
      }, { threshold: 0.12 });
      revealEls.forEach(function (el) { el.setAttribute("data-hf-reveal", ""); io.observe(el); });
    }
    /* Gentle parallax on the hero orbs — transform only,
       throttled by rAF, fine pointers only. */
    var orbs = doc.querySelectorAll(".xp-hero .xp-orb");
    if (finePointer && orbs.length) {
      var ticking = false;
      window.addEventListener("scroll", function () {
        if (ticking) return; ticking = true;
        window.requestAnimationFrame(function () {
          var y = Math.min(window.scrollY || 0, 600);
          orbs.forEach(function (o, i) { o.style.translate = "0 " + (y * (i ? 0.05 : 0.09)) + "px"; });
          ticking = false;
        });
      }, { passive: true });
    }
  }

  /* ---- 2. header shadow ---- */
  var hdr = doc.querySelector(".hdr");
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle("hf-scrolled", (window.scrollY || 0) > 8); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* ---- 3. Hindi practice widget ---- */
  var host = doc.querySelector(".xp-hero-copy");
  if (!host || doc.querySelector("[data-hf-practice]")) return;

  var WORDS = [
    { hi: "नमस्ते", roman: "Namaste", en: "Hello / greetings" },
    { hi: "धन्यवाद", roman: "Dhanyavaad", en: "Thank you" },
    { hi: "कैसे हो?", roman: "Kaise ho?", en: "How are you?" },
    { hi: "मैं ठीक हूँ", roman: "Main theek hoon", en: "I am fine" },
    { hi: "मेरा नाम … है", roman: "Mera naam … hai", en: "My name is …" },
    { hi: "कृपया", roman: "Kripya", en: "Please" },
    { hi: "माफ़ कीजिए", roman: "Maaf keejiye", en: "Excuse me / sorry" },
    { hi: "फिर मिलेंगे", roman: "Phir milenge", en: "See you again" },
    { hi: "शुभ प्रभात", roman: "Shubh prabhaat", en: "Good morning" },
    { hi: "हाँ / नहीं", roman: "Haan / Nahi", en: "Yes / No" }
  ];
  var i = Math.floor(Math.random() * WORDS.length);

  var card = doc.createElement("section");
  card.className = "hf-card";
  card.setAttribute("data-hf-practice", "");
  card.setAttribute("aria-label", "Hindi practice: word of the moment");
  card.innerHTML =
    '<h2>✨ Hindi practice — try one now</h2>' +
    '<p class="hf-sub">No sign-up. Read it, hear it, say it out loud.</p>' +
    '<div class="hf-stage"><div class="hf-word" lang="hi" data-hf-word></div>' +
    '<div class="hf-meta"><div class="hf-roman" data-hf-roman></div>' +
    '<div class="hf-mean" data-hf-mean></div></div></div>' +
    '<div class="hf-actions">' +
    '<button type="button" class="hf-btn hf-primary" data-hf-listen>🔊 Listen</button>' +
    '<button type="button" class="hf-btn" data-hf-next>Next word →</button>' +
    '<span class="hf-progress" data-hf-progress aria-live="polite"></span></div>';

  var anchor = host.querySelector(".xp-stats") || host.querySelector(".xp-trust");
  if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(card, anchor.nextSibling);
  else host.appendChild(card);

  var wEl = card.querySelector("[data-hf-word]"),
      rEl = card.querySelector("[data-hf-roman]"),
      mEl = card.querySelector("[data-hf-mean]"),
      pEl = card.querySelector("[data-hf-progress]"),
      listenBtn = card.querySelector("[data-hf-listen]");

  function render(flip) {
    var w = WORDS[i];
    wEl.textContent = w.hi; rEl.textContent = w.roman; mEl.textContent = w.en;
    pEl.textContent = (i + 1) + " / " + WORDS.length;
    if (flip && !reduceMotion) {
      wEl.classList.remove("hf-flip"); void wEl.offsetWidth; wEl.classList.add("hf-flip");
    }
  }
  /* Speech goes through the one shared engine (js/voice.js):
     it picks an exact-language voice, never autoplays, and is
     honest when the device has none. No second speech path. */
  function speak() {
    var ok = false;
    try {
      ok = !!(window.EkGuruVoice && typeof window.EkGuruVoice.speak === "function" &&
              window.EkGuruVoice.speak(WORDS[i].hi, "hi", 0.85));
    } catch (e) { ok = false; }
    if (!ok) {
      listenBtn.disabled = true;
      listenBtn.textContent = "🔇 " + ((window.EkGuruVoice && window.EkGuruVoice.missing)
        ? window.EkGuruVoice.missing("hi") : "No Hindi voice on this device — read the transliteration instead.");
    }
  }
  card.querySelector("[data-hf-next]").addEventListener("click", function () {
    i = (i + 1) % WORDS.length; render(true);
  });
  listenBtn.addEventListener("click", speak);
  if ("speechSynthesis" in window && window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = function () {};
  }
  render(false);
})();
