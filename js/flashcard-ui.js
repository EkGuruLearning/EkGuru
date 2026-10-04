/* =========================================================
   EkGuru — FLASHCARD LAB  (v1, PHASE 9)
   ---------------------------------------------------------
   Drives the per-language decks written by
   tools/build-flashcards.py (js/flashcards-<code>.js).

   Contract (the honest framing this site keeps everywhere):
   · Cards are the authored course vocabulary — nothing is
     generated here, invented here, or fetched from a server.
   · Playback is the device's computer voice via js/voice.js,
     on click only. Never autoplay, never a native-accent claim.
   · Cards you save go to js/global-srs.js (this browser only).
   · Progress lives in this browser only. No account, no upload.
   · Flipping hides only the meaning: the word itself never
     leaves the accessibility tree, and the meaning is a real
     element in the DOM (aria-hidden toggles on flip).

   Usage:
     EkGuruFlashcards.mount(el, {code:"de", speech:"de-DE",
                                 direction:"ltr", name:"German"})
   ========================================================= */
(function () {
  "use strict";

  var PREFIX = "ekguru:flashcards:";
  var CATEGORY_LABELS = {
    greetings: "Greetings", numbers: "Numbers", food: "Food & drink",
    travel: "Travel", family: "Family & people", time: "Time & dates",
    colors: "Colours", body: "Body & health", verbs: "Verbs",
    adjectives: "Adjectives", phrases: "Phrases", nouns: "Nouns",
    other: "Other"
  };

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function store(lang) {
    try {
      return JSON.parse(localStorage.getItem(PREFIX + lang + ":v1") || "{}") || {};
    } catch (e) { return {}; }
  }
  function save(lang, data) {
    try { localStorage.setItem(PREFIX + lang + ":v1", JSON.stringify(data)); } catch (e) {}
  }
  function categoryLabel(c) {
    return CATEGORY_LABELS[c] || c.charAt(0).toUpperCase() + c.slice(1);
  }
  function prefersReduced() {
    try { return matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { return false; }
  }
  function speak(text, lang, el) {
    /* js/voice.js is the ONLY speech engine in js/ (a rule the voice test
       enforces). The lab never calls speechSynthesis itself, and never
       pretends the fallback is a voice: without the provider it says so. */
    if (window.EkGuruVoice && typeof window.EkGuruVoice.speak === "function") {
      return window.EkGuruVoice.speak(String(text), lang, 0.8);
    }
    var msg = el && el.querySelector(".fc-msg");
    if (msg) msg.textContent = "Voice playback is unavailable on this page — the shared voice control is not loaded.";
    return false;
  }

  function mount(el, cfg) {
    if (!el) return null;
    cfg = cfg || {};
    var code = cfg.code || el.getAttribute("data-eg-flashcards") || "";
    var deck = window["EKGURU_FLASHCARDS_" + String(code).toUpperCase()];
    if (!deck || !deck.cards || !deck.cards.length) {
      el.innerHTML = '<p class="fc-empty">No flashcards are published for this language yet. ' +
        'The deck is built from the course vocabulary, so it appears when the course does.</p>';
      return null;
    }

    var speech = cfg.speech || deck.speech || code;
    var rtl = (cfg.direction || deck.direction || "ltr") === "rtl";
    var state = {
      cat: "all",
      order: [],
      index: 0,
      flipped: false,
      progress: store(code)
    };
    state.cards = deck.cards.slice();

    var H = (window.__fcH = window.__fcH || 0);
    var uid = "fc" + (++H) + "-" + code;
    window.__fcH = H;

    function filtered() {
      return state.cat === "all" ? state.cards : state.cards.filter(function (c) {
        return c.cat === state.cat;
      });
    }
    function rebuild(shuffle) {
      state.order = filtered();
      if (shuffle) {
        for (var i = state.order.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          var t = state.order[i]; state.order[i] = state.order[j]; state.order[j] = t;
        }
      }
      state.index = 0;
      state.flipped = false;
    }
    function card() { return state.order[state.index] || null; }
    function markSeen(c) {
      if (!c) return;
      if (!state.progress.seen) state.progress.seen = {};
      if (!state.progress.seen[c.id]) {
        state.progress.seen[c.id] = 1;
        state.progress.seenCount = Object.keys(state.progress.seen).length;
        save(code, state.progress);
      }
    }

    function chipsHtml() {
      var cats = deck.categories || {};
      var order = ["all"].concat(Object.keys(cats).sort(function (a, b) {
        return (cats[b] || 0) - (cats[a] || 0);
      }));
      return order.map(function (c) {
        var count = c === "all" ? state.cards.length : (cats[c] || 0);
        return '<button type="button" class="fc-chip" data-fc-cat="' + esc(c) + '"' +
          ' aria-pressed="' + (state.cat === c ? "true" : "false") + '">' +
          esc(c === "all" ? "All" : categoryLabel(c)) +
          ' <span class="fc-chip-n">' + count + "</span></button>";
      }).join("");
    }

    function cardHtml() {
      var c = card();
      if (!c) return '<p class="fc-empty">No cards in this category.</p>';
      var lang = ' lang="' + esc(code) + '"' + (rtl ? ' dir="rtl"' : "");
      var back = esc(c.en);
      var roman = c.r ? '<span class="fc-roman" dir="ltr">' + esc(c.r) + "</span>" : "";
      return '<div class="fc-card" id="' + uid + '-card" data-flipped="' + (state.flipped ? "true" : "false") + '">' +
        '<button type="button" class="fc-face" id="' + uid + '-flip" data-fc="flip"' +
        ' aria-pressed="' + (state.flipped ? "true" : "false") + '"' +
        ' aria-describedby="' + uid + '-hint">' +
        '<span class="fc-side fc-side-front"' + lang + ">" + esc(c.t) + roman + "</span>" +
        '<span class="fc-side fc-side-back"' + (state.flipped ? "" : " aria-hidden=\"true\"") + ">" +
        back + "</span>" +
        "</button></div>";
    }

    function progressHtml() {
      var total = state.order.length;
      var seen = state.progress.seenCount || 0;
      return "Card " + (total ? state.index + 1 : 0) + " of " + total +
        " · " + seen + " of " + state.cards.length + " seen";
    }

    function render() {
      var c = card();
      el.innerHTML =
        '<div class="fc-head"><h2 class="fc-title">' + esc(cfg.name || deck.name || code) +
          " flashcards</h2>" +
        '<p class="fc-note">Front: the ' + esc(cfg.name || deck.name || code) +
          " word. Back: its meaning and reading. Saved cards go to your review queue in this browser only.</p></div>" +
        '<div class="fc-chips" role="group" aria-label="Filter cards by category">' + chipsHtml() + "</div>" +
        '<div class="fc-stage">' + cardHtml() + "</div>" +
        '<p class="fc-progress" id="' + uid + '-progress" role="status" aria-live="polite">' + progressHtml() + "</p>" +
        '<p class="fc-hint" id="' + uid + '-hint">Enter or Space flips the card · arrow keys move between cards.</p>' +
        '<div class="fc-actions">' +
          '<button type="button" class="btn btn-ghost" data-fc="prev">← Previous</button>' +
          '<button type="button" class="btn btn-primary" data-fc="next">Next card →</button>' +
          '<button type="button" class="btn btn-ghost" data-fc="shuffle">Shuffle</button>' +
          '<button type="button" class="btn btn-ghost" data-fc="speak"' + (c ? "" : " disabled") + ">🔊 Speak</button>" +
          '<button type="button" class="btn btn-ghost" data-fc="review"' + (c ? "" : " disabled") + ">＋ Add to review</button>" +
        "</div>" +
        '<p class="fc-msg" role="status" aria-live="polite"></p>';
      var cardEl = el.querySelector(".fc-card");
      if (cardEl && prefersReduced()) cardEl.setAttribute("data-reduced-motion", "true");
      if (c) markSeen(c);
      el.setAttribute("data-fc-ready", "1");
    }

    function move(delta) {
      if (!state.order.length) return;
      state.index = (state.index + delta + state.order.length) % state.order.length;
      state.flipped = false;
      render();
      var flip = el.querySelector("#" + uid + "-flip");
      if (flip) flip.focus();
    }
    function flip() {
      state.flipped = !state.flipped;
      var cardEl = el.querySelector(".fc-card");
      var btn = el.querySelector("#" + uid + "-flip");
      var back = el.querySelector(".fc-side-back");
      if (!cardEl || !btn) return;
      cardEl.setAttribute("data-flipped", state.flipped ? "true" : "false");
      btn.setAttribute("aria-pressed", state.flipped ? "true" : "false");
      /* The front (the word) never leaves the accessibility tree; only the
         meaning is hidden until the learner asks for it. */
      if (back) back.setAttribute("aria-hidden", state.flipped ? "false" : "true");
      markSeen(card());
    }

    el.addEventListener("click", function (ev) {
      var chip = ev.target.closest ? ev.target.closest("[data-fc-cat]") : null;
      if (chip && el.contains(chip)) {
        state.cat = chip.getAttribute("data-fc-cat");
        rebuild(false);
        render();
        return;
      }
      var btn = ev.target.closest ? ev.target.closest("[data-fc]") : null;
      if (!btn || !el.contains(btn)) return;
      var action = btn.getAttribute("data-fc");
      var c = card();
      if (action === "flip") return flip();
      if (action === "prev") return move(-1);
      if (action === "next") {
        if (state.flipped) markSeen(c);
        return move(1);
      }
      if (action === "shuffle") { rebuild(true); render(); return; }
      if (action === "speak" && c) { speak(c.t, speech, el); return; }
      if (action === "review" && c) {
        var msg = el.querySelector(".fc-msg");
        var res = window.EkGuruGlobalSRS && window.EkGuruGlobalSRS.add
          ? window.EkGuruGlobalSRS.add({
              prompt: c.t, answer: c.en, language: code, level: c.level,
              category: c.cat, skill: "vocabulary", target: c.t, source: "flashcards"
            })
          : { added: false, reason: "Review is unavailable on this page." };
        if (res && (res.added || res.id)) {
          if (!state.progress.saved) state.progress.saved = {};
          state.progress.saved[c.id] = 1;
          save(code, state.progress);
          if (msg) msg.textContent = "Saved to your review queue — it will come back on a schedule.";
        } else if (msg) {
          msg.textContent = (res && res.reason) || "Could not save this card.";
        }
        return;
      }
    });

    el.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowRight") { ev.preventDefault(); move(1); }
      else if (ev.key === "ArrowLeft") { ev.preventDefault(); move(-1); }
    });

    rebuild(false);
    render();
    return {
      language: code,
      count: state.cards.length,
      categories: Object.keys(deck.categories || {}),
      state: state
    };
  }

  window.EkGuruFlashcards = { version: 1, mount: mount, CATEGORY_LABELS: CATEGORY_LABELS };
})();
