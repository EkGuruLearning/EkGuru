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

  function toArray(list) { return Array.prototype.slice.call(list); }

  /* ---- 1. motion + reveal ----
     THRESHOLD BUG (fixed 23 Nov 2026). This used `{ threshold: 0.12 }`,
     which asks "is 12% of this element on screen?". For a short section that
     is a fine question. For the tutor section it is an impossible one: on a
     phone the grid is one column, seventeen cards, roughly 7,000px tall, and
     the largest ratio that can ever be visible is viewport/section ≈ 0.09 —
     under the threshold no matter how far the visitor scrolls. The section
     therefore never got .hf-in, stayed at `opacity: 0` from the rule in
     css/home-future.css, and the tutor cards were blank on every phone and
     narrow window. Desktop (3 columns, ~2,600px) cleared the threshold, which
     is why it only ever looked broken on a small screen.

     The intent is "has this section started to enter the viewport", not "is a
     fixed share of it visible". rootMargin does that with threshold 0, and it
     works for a section of any height. A fallback timer and a scroll-into-view
     check cover the browsers where the observer is throttled or absent, so
     the content is never left hidden. */
    var REVEAL_AT = "0px 0px -50px 0px";

    function showEl(el) { el.classList.add("hf-in"); }

    if (!reduceMotion) {
      /* .hf-on is what turns the motion rules in css/home-future.css on at
         all — orbs, floats, the hero card transition, the [data-hf-reveal]
         hide/reveal pair. It must be set on the same condition as before:
         animation is opt-in and reduced-motion visitors never get it. */
      root.classList.add("hf-on");
      var revealEls = toArray(doc.querySelectorAll(".xp-sec, .xp-rail"));

      if ("IntersectionObserver" in window) {
        /* threshold 0 + a small negative bottom margin: fires as soon as the
           section's top edge is 50px inside the viewport. Height-independent. */
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) { showEl(en.target); io.unobserve(en.target); }
          });
        }, { rootMargin: REVEAL_AT, threshold: 0 });

        revealEls.forEach(function (el) {
          el.setAttribute("data-hf-reveal", "");
          io.observe(el);
        });

        /* Anything already on screen at load is shown at once: a short page
           may never produce a scroll event, and the observer's first callback
           can arrive after the first paint. */
        revealEls.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < (root.innerHeight || 800) && r.bottom > 0) showEl(el);
        });

        /* Watchdog: if the observer is throttled, blocked, or the tab was in
           the background during load, nothing may stay hidden. The old code
           had no watchdog here, so one missed callback meant a permanently
           invisible tutor section. `hf-stuck` is also the CSS hook that
           outranks the hidden state, so even a stylesheet-only failure is
           covered. */
        window.setTimeout(function () {
          toArray(doc.querySelectorAll("[data-hf-reveal]")).forEach(function (el) {
            el.classList.add("hf-stuck");
            showEl(el);
          });
          /* Last resort: if a section is still not visible for any reason,
             switch the whole page to the flat fallback. */
          var still = toArray(doc.querySelectorAll("[data-hf-reveal]")).filter(function (el) {
            return !el.classList.contains("hf-in");
          });
          if (still.length) root.classList.add("hf-fallback");
        }, 2500);
      } else {
        /* No IntersectionObserver (very old WebView, some in-app browsers):
           reveal on first scroll, and show everything immediately otherwise. */
        revealEls.forEach(function (el) { el.setAttribute("data-hf-reveal", ""); });
        var revealOnScroll = function () {
          toArray(doc.querySelectorAll("[data-hf-reveal]")).forEach(function (el) {
            var r = el.getBoundingClientRect();
            if (r.top < (root.innerHeight || 800)) showEl(el);
          });
        };
        window.addEventListener("scroll", revealOnScroll, { passive: true });
        revealOnScroll();
      }
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

/* ---- Phase 2 enhancements (all guarded, progressive) ---- */
  /* particles: fine pointer + motion consent + cap */
  if (!reduceMotion && finePointer) {
    var host2 = doc.createElement("div");
    host2.className = "hf-particles";
    host2.setAttribute("aria-hidden", "true");
    var N = Math.min(16, Math.max(6, Math.floor(window.innerWidth / 120)));
    for (var p = 0; p < N; p++) {
      var dot = doc.createElement("i");
      dot.className = "hf-particle";
      var size = 3 + ((p * 7) % 6);
      dot.style.width = size + "px";
      dot.style.height = size + "px";
      dot.style.left = ((p * 47) % 100) + "%";
      dot.style.animationDuration = (16 + (p % 7) * 4) + "s";
      dot.style.animationDelay = (-(p % 5) * 3) + "s";
      dot.style.opacity = (0.18 + ((p % 4) * 0.08)).toFixed(2);
      host2.appendChild(dot);
    }
    doc.body.appendChild(host2);
  }

  /* hero stat count-up: animate the "3 public tutors" number */
  var statEl = doc.querySelector("#stat-tutors");
  if (statEl && !reduceMotion) {
    var final = parseInt(statEl.textContent, 10) || 0;
    var cur = { v: 0 };
    var step = function () {
      cur.v = Math.min(final, cur.v + Math.max(1, Math.round(final / 18)));
      statEl.textContent = cur.v;
      if (cur.v < final) window.requestAnimationFrame(step);
    };
    /* start when the hero stats enter view */
    if ("IntersectionObserver" in window) {
      var io2 = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { step(); io2.disconnect(); }
        });
      }, { threshold: 0.4 });
      io2.observe(statEl);
    } else { step(); }
    /* keep the live value (main.js may overwrite); only animate once */
  }

  /* scroll progress hairline */
  if (!reduceMotion) {
    var bar = doc.createElement("div");
    bar.className = "hf-scrollbar";
    bar.setAttribute("aria-hidden", "true");
    var inner = doc.createElement("i");
    bar.appendChild(inner);
    doc.body.appendChild(bar);
    var tick2 = false;
    var onScroll2 = function () {
      if (tick2) return; tick2 = true;
      window.requestAnimationFrame(function () {
        var h = doc.documentElement.scrollHeight - window.innerHeight;
        var pct = h > 0 ? Math.min(100, Math.max(0, (window.scrollY || 0) / h * 100)) : 0;
        inner.style.width = pct + "%";
        tick2 = false;
      });
    };
    window.addEventListener("scroll", onScroll2, { passive: true });
    onScroll2();
  }

  /* typing practice inside the Hindi widget */
  if (host && !doc.querySelector("[data-hf-type]")) {
    var TYPE_WORDS = [
      { hi: "नमस्ते", roman: "namaste", en: "Hello" },
      { hi: "धन्यवाद", roman: "dhanyavaad", en: "Thank you" },
      { hi: "कृपया", roman: "kripya", en: "Please" },
      { hi: "हाँ", roman: "haan", en: "Yes" },
      { hi: "नहीं", roman: "nahi", en: "No" }
    ];
    var ti = 0;
    var typeRow = doc.createElement("div");
    typeRow.className = "hf-type-row";
    typeRow.setAttribute("data-hf-type", "");
    typeRow.innerHTML =
      '<input class="hf-type-input" type="text" autocomplete="off" spellcheck="false" ' +
      'aria-label="Type this word in Hindi script" placeholder="Type it…">' +
      '<span class="hf-type-hint" data-hf-type-msg></span>';
    var typeInput = typeRow.querySelector("input");
    var typeMsg = typeRow.querySelector("[data-hf-type-msg]");

    function typeState() {
      var w = TYPE_WORDS[ti];
      typeInput.setAttribute("placeholder", "Type: " + w.roman + " (" + w.en + ")");
      typeMsg.textContent = "";
      typeMsg.style.color = "";
    }
    function typeCheck(e) {
      if (e.key !== "Enter") return;
      var w = TYPE_WORDS[ti];
      var norm = typeInput.value.trim().toLowerCase().replace(/[।्]/g, "");
      var want = w.roman.toLowerCase();
      var ok = norm === want || norm === w.hi;
      typeMsg.textContent = ok ? "✓ Perfect!" : "Try again — " + w.roman;
      typeMsg.style.color = ok ? "var(--green, #1a7f37)" : "var(--red, #b3261e)";
      if (ok) {
        ti = (ti + 1) % TYPE_WORDS.length;
        setTimeout(typeState, 500);
      }
    }
    typeInput.addEventListener("keydown", typeCheck);

    /* insert under the stage */
    var stage = card.querySelector(".hf-stage");
    if (stage && stage.parentNode) stage.parentNode.insertBefore(typeRow, stage.nextSibling);
    typeState();
  }
})();
