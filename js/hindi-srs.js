/* =========================================================
   EkGuru — REVIEW DECK COMPATIBILITY UI (v2)
   ---------------------------------------------------------
   Keeps the original window.EkGuruSRS API (Hindi review page, world-language review pages,
   "Add to review" buttons) but scheduling now belongs to the shared per-language engine
   (js/global-srs.js, deck key ekguru:srs:<code>:v1). The page's data-learning-language picks the deck.

   One-time migration: cards from the original single deck (ekguru:hindi:v1:review) are COPIED with
   their real schedules. The original key is never deleted. A persistent marker means the copy never
   runs again on its own, so a card you removed (or a verified import) cannot silently come back.
   Copying again is an explicit, confirmed recovery (EkGuruSRS.copyLegacyDeck()).
   ========================================================= */
(function (w) {
  "use strict";
  if (w.EkGuruSRS && w.EkGuruSRS._shared) return;
  var LEGACY = "ekguru:hindi:v1:review", MARKER = "ekguru:hindi:shared-srs-migration:v1";
  function core() { return w.EkGuruGlobalSRS; }
  function current() { return document.documentElement.getAttribute("data-learning-language") || "hi"; }
  function idFor(prompt, answer) {
    var s = String(prompt || "") + "|" + String(answer || ""), h = 0;
    for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
    return "c" + Math.abs(h).toString(36);
  }
  function level(l) { return { beginner: "A1", elementary: "A2", intermediate: "B1", advanced: "C1" }[l] || l || "A1"; }

  function migrate(force) {
    if (!core()) return false;
    var before = {}, writes = {}, changed = [];
    try {
      if (localStorage.getItem(MARKER) !== null && !force) return true;
      var raw = localStorage.getItem(LEGACY), old = raw ? JSON.parse(raw) : null;
      if (old && (old.version !== 1 || !old.cards || typeof old.cards !== "object" || Array.isArray(old.cards) || Object.keys(old.cards).length > 10000)) throw new Error("Unreadable legacy review deck preserved.");
      Object.keys(old && old.cards || {}).forEach(function (id) {
        var c = old.cards[id], l = c && c.language || "hi";
        if (!c || !/^[a-z]{2,3}$/.test(l)) throw new Error("Invalid legacy card.");
        var mapped = { card_id: id, content_id: String(c.content_id || id), language: l, target: String(c.target || c.prompt), source: String(c.source || ""),
          prompt: c.prompt, prompt_language: null, answer: c.answer, category: String(c.category || "vocabulary"), level: level(c.level), skill: "vocabulary",
          country: c.country || null, ease: c.ease, interval: c.interval, due_date: c.due_date, review_count: c.review_count, last_reviewed: c.last_reviewed,
          version: 1, added_at: c.added_at, srs_eligible: true };
        if (!core().validCard(mapped, l, id) || !core().isReadable(l)) throw new Error("Invalid or unreadable saved review data preserved.");
        var key = "ekguru:srs:" + l + ":v1";
        if (!writes[key]) writes[key] = JSON.parse(localStorage.getItem(key) || '{"version":1,"cards":{}}');
        if (!Object.prototype.hasOwnProperty.call(writes[key].cards, id)) writes[key].cards[id] = mapped;
      });
      Object.keys(writes).forEach(function (k) { before[k] = localStorage.getItem(k); });
      // The in-progress marker is written FIRST: a crash or quota failure cannot silently rerun the copy.
      localStorage.setItem(MARKER, "pending");
      Object.keys(writes).forEach(function (k) { changed.push(k); localStorage.setItem(k, JSON.stringify(writes[k])); });
      localStorage.setItem(MARKER, "done");
      return true;
    } catch (e) {
      changed.reverse().forEach(function (k) { try { if (before[k] === null) localStorage.removeItem(k); else localStorage.setItem(k, before[k]); } catch (_) {} });
      try { localStorage.setItem(MARKER, "failed"); } catch (_) {}
      if (w.EkGuruUI) w.EkGuruUI.toast("Legacy review migration did not finish. Original data were preserved. Export before an explicit retry.");
      return false;
    }
  }

  var api = {
    version: 1, _shared: true,
    copyLegacyDeck: function () {
      return w.confirm("Copy missing cards from the original deck? This can restore cards you removed. Export your learning backup first.") ? migrate(true) : false;
    },
    add: function (spec) {
      if (!core()) return { added: false, reason: "Review engine unavailable" };
      var card = Object.assign({}, spec, { language: spec.language || current(), level: level(spec.level), card_id: spec.card_id || idFor(spec.prompt, spec.answer) });
      return core().add(card);
    },
    has: function (id, lang) { return !!(core() && core().has(id, lang || current())); },
    due: function (limit) { return core() ? core().due(current(), limit) : []; },
    all: function () { return core() ? core().all(current()) : []; },
    count: function () { return core() ? core().count(current()) : 0; },
    dueCount: function () { return core() ? core().dueCount(current()) : 0; },
    review: function (id, rating) { return core() ? core().review(id, rating, current()) : null; },
    remove: function (id) { return !!(core() && core().remove(id, current())); },
    starterDeck: function () {
      if (current() !== "hi") return [];
      var out = [], q = w.EKGURU_HINDI_QUIZ, b = w.EKGURU_PRACTICE_BANK;
      if (q && q.questions) q.questions.forEach(function (x) { out.push({ prompt: x.q, answer: x.a + " — " + x.explain, category: x.topic, level: level(x.level), language: "hi" }); });
      if (b && b.vocabulary) b.vocabulary.forEach(function (x) { out.push({ prompt: x.q, answer: x.a + " — " + (x.explain || ""), category: "vocabulary", level: "A1", language: "hi" }); });
      return out;
    },
    seedStarter: function () {
      var cards = api.starterDeck(), added = 0;
      cards.forEach(function (c) { if (api.add(c).added) added++; });
      return { total: cards.length, added: added };
    },
    mountAddButtons: function () {
      document.querySelectorAll("[data-hi-card]").forEach(function (el) {
        if (el.hasAttribute("data-hi-card-mounted")) return;
        el.setAttribute("data-hi-card-mounted", "1");
        var spec; try { spec = JSON.parse(el.getAttribute("data-hi-card")); } catch (_) { return; }
        if (!spec || !spec.p || !spec.a) return;
        var b = document.createElement("button");
        b.type = "button"; b.className = "hi-review-add";
        b.setAttribute("aria-label", "Add " + spec.p + " to its language review deck");
        function paint() {
          var added = api.has(idFor(spec.p, spec.a), spec.l || current());
          b.textContent = added ? "✓ In review" : "＋ Add to review";
          b.setAttribute("aria-pressed", String(added));
        }
        paint();
        b.addEventListener("click", function (e) {
          e.preventDefault();
          var r = api.add({ prompt: spec.p, answer: spec.a, category: spec.c || "vocabulary", language: spec.l || current(), target: spec.p });
          paint();
          if (w.EkGuruUI) w.EkGuruUI.toast(r.added ? "Saved to its language review deck." : (r.reason || "Already in this language review deck."));
        });
        el.appendChild(b);
      });
    }
  };
  w.EkGuruSRS = api;
  function boot() { migrate(); api.mountAddButtons(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})(window);
