/* =========================================================
   EkGuru — HINDI SRS / REVIEW  (v1)
   ---------------------------------------------------------
   A transparent, client-side spaced-repetition engine for the
   Hindi learning product. Honest limits:

     · Data lives ONLY in this browser (localStorage), versioned
       under ekguru:hindi:v1:review. No account, no upload, no
       cross-device sync, and no claim of "AI personalisation".
     · The schedule is a simple SM-2-lite: ease, interval,
       due_date, review_count, last_reviewed. Again / Hard /
       Good / Easy are the only four answers.

   Cards enter the deck two ways:
     · "Add to review" buttons mounted next to any element that
       carries data-hi-card (see build-hindi-audio.py).
     · The review page's "Load starter deck", seeded from the
       quiz bank and the practice vocabulary bank.

   Window API: window.EkGuruSRS
   ========================================================= */
(function () {
  "use strict";

  var KEY = "ekguru:hindi:v1:review";
  var VERSION = 1;

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return { version: VERSION, cards: {} };
      var o = JSON.parse(raw);
      if (o && o.version === VERSION && o.cards) return o;
      return { version: VERSION, cards: {} };
    } catch (e) { return { version: VERSION, cards: {} }; }
  }
  function write(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }

  function contentId(prompt, answer) {
    var s = String(prompt || "") + "|" + String(answer || "");
    var h = 0;
    for (var i = 0; i < s.length; i++) { h = (h * 31 + s.charCodeAt(i)) | 0; }
    return "c" + Math.abs(h).toString(36);
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  var SRS = {
    version: VERSION,

    add: function (spec) {
      var o = read();
      var id = spec.card_id || contentId(spec.prompt, spec.answer);
      if (o.cards[id]) return { id: id, added: false, card: o.cards[id] };
      var now = Date.now();
      var card = {
        card_id: id,
        content_id: spec.content_id || id,
        prompt: spec.prompt || "",
        answer: spec.answer || "",
        category: spec.category || "vocabulary",
        level: spec.level || "beginner",
        ease: 2.5,
        interval: 0,
        due_date: now,
        review_count: 0,
        last_reviewed: 0,
        version: VERSION,
        added_at: now
      };
      o.cards[id] = card;
      write(o);
      return { id: id, added: true, card: card };
    },

    has: function (id) { return !!read().cards[id]; },

    due: function (limit) {
      var o = read(), now = Date.now(), out = [];
      Object.keys(o.cards).forEach(function (id) {
        var c = o.cards[id];
        if (c.due_date <= now) out.push(c);
      });
      out.sort(function (a, b) { return a.due_date - b.due_date; });
      return limit ? out.slice(0, limit) : out;
    },

    all: function () {
      var o = read();
      return Object.keys(o.cards).map(function (id) { return o.cards[id]; });
    },

    count: function () { return Object.keys(read().cards).length; },
    dueCount: function () { return this.due().length; },

    /* rating: "again" | "hard" | "good" | "easy" */
    review: function (card_id, rating) {
      var o = read();
      var c = o.cards[card_id];
      if (!c) return null;
      var day = 86400000;
      var interval = c.interval || 0;
      var ease = c.ease || 2.5;
      if (rating === "again") {
        interval = 0; ease = Math.max(1.3, ease - 0.2);
      } else if (rating === "hard") {
        interval = Math.max(1, interval * 1.2); ease = Math.max(1.3, ease - 0.15);
      } else if (rating === "good") {
        interval = interval === 0 ? 1 : Math.max(1, interval * ease);
      } else { /* easy */
        interval = interval === 0 ? 3 : Math.max(1, interval * ease * 1.3);
        ease = Math.min(3.5, ease + 0.15);
      }
      c.interval = Math.round(interval * 10) / 10;
      c.ease = Math.round(ease * 100) / 100;
      c.review_count = (c.review_count || 0) + 1;
      c.last_reviewed = Date.now();
      c.due_date = c.last_reviewed + Math.round(c.interval * day);
      o.cards[card_id] = c;
      write(o);
      return c;
    },

    remove: function (card_id) {
      var o = read();
      if (!o.cards[card_id]) return false;
      delete o.cards[card_id];
      write(o);
      return true;
    },

    /* ---- starter deck from the quiz bank + practice vocabulary ---- */
    starterDeck: function () {
      var out = [];
      var Q = window.EKGURU_HINDI_QUIZ;
      if (Q && Q.questions) {
        Q.questions.forEach(function (q) {
          out.push({ prompt: q.q, answer: q.a + " — " + q.explain,
                     category: q.topic, level: q.level });
        });
      }
      var B = window.EKGURU_PRACTICE_BANK;
      if (B && B.vocabulary) {
        B.vocabulary.forEach(function (v) {
          out.push({ prompt: v.q, answer: v.a + " — " + (v.explain || ""),
                     category: "vocabulary", level: "beginner" });
        });
      }
      return out;
    },

    seedStarter: function () {
      var cards = this.starterDeck(), added = 0;
      cards.forEach(function (c) { if (SRS.add(c).added) added++; });
      return { total: cards.length, added: added };
    },

    /* ---- "Add to review" buttons for [data-hi-card] elements ---- */
    mountAddButtons: function () {
      var items = document.querySelectorAll("[data-hi-card]");
      items.forEach(function (el) {
        if (el.getAttribute("data-hi-card-mounted")) return;
        el.setAttribute("data-hi-card-mounted", "1");
        var spec = null;
        try { spec = JSON.parse(el.getAttribute("data-hi-card")); } catch (e) {}
        if (!spec || !spec.p) return;
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "hi-review-add";
        btn.setAttribute("aria-label", "Add “" + spec.p + "” to review");
        renderAddState(btn, spec);
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          var r = SRS.add({ prompt: spec.p, answer: spec.a, category: spec.c || "vocabulary" });
          renderAddState(btn, spec);
          if (window.EkGuruToast) window.EkGuruToast.show(r.added ? "Added to review" : "Already in review");
        });
        el.appendChild(btn);
      });
    }
  };

  function renderAddState(btn, spec) {
    var added = SRS.has(contentId(spec.p, spec.a));
    btn.innerHTML = added ? "✓ Review" : "＋ Review";
    btn.setAttribute("aria-pressed", added ? "true" : "false");
    btn.classList.toggle("added", added);
  }

  window.EkGuruSRS = SRS;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { SRS.mountAddButtons(); });
  } else {
    SRS.mountAddButtons();
  }
})();
