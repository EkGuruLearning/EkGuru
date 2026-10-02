/* =========================================================
   EkGuru — GLOBAL SRS ENGINE v1 (per-language decks, device-only)
   ---------------------------------------------------------
   One transparent SM-2-lite engine for every language. Each language has its own deck under
   ekguru:srs:<code>:v1; nothing leaves the device and there is no account.

   Schedule: Again = 10 minutes (ease -0.2); Hard = x1.2 (ease -0.15); Good = x ease;
   Easy = x ease x1.3 (ease +0.15). Interval is capped at 3650 days, ease stays in 1.3..3.5.
   An unreadable, future or malformed saved deck is PRESERVED: it is never overwritten, and a
   verified import is the only way to replace it.

   Window API: window.EkGuruGlobalSRS (also emits the "ekguru:srs-review" event on each review)
   ========================================================= */
(function () {
  "use strict";
  if (window.EkGuruGlobalSRS && window.EkGuruGlobalSRS.version === 1) return;

  var VERSION = 1, PREFIX = "ekguru:srs:", DAY = 86400000, AGAIN_DELAY = 600000, MAX_CARDS = 10000;
  var FIELDS = ["card_id", "content_id", "language", "target", "source", "prompt", "answer", "category", "level",
    "skill", "country", "ease", "interval", "due_date", "review_count", "last_reviewed", "version", "added_at",
    "srs_eligible", "prompt_language"];
  var RESERVED = ["__proto__", "constructor", "prototype"];

  function validLang(lang) { return lang === "global" || /^[a-z]{2,3}$/.test(lang || ""); }
  function storageKey(lang) { return PREFIX + (validLang(lang) ? lang : "global") + ":v" + VERSION; }
  function validId(id) { return typeof id === "string" && /^[a-zA-Z0-9_.:-]{1,150}$/.test(id) && RESERVED.indexOf(id) < 0; }
  function own(o, k) { return Object.prototype.hasOwnProperty.call(o, k); }
  function text(v, max) { return typeof v === "string" && v.length <= max; }

  function validCard(c, lang, id) {
    if (!c || typeof c !== "object" || Array.isArray(c) || c.version !== VERSION || c.card_id !== id || !validId(id)) return false;
    if (c.language !== lang || c.srs_eligible !== true) return false;
    if (Object.keys(c).some(function (k) { return FIELDS.indexOf(k) < 0; })) return false;
    if (c.prompt_language !== undefined && c.prompt_language !== null && !/^[a-z]{2,3}$/.test(c.prompt_language)) return false;
    if (!text(c.prompt, 2000) || !text(c.answer, 2000) || !text(c.target, 2000) || !text(c.source, 2000) || !c.prompt || !c.answer) return false;
    if (!text(c.content_id, 200) || !text(c.category, 200) || !text(c.level, 200) || !text(c.skill, 200)) return false;
    if (c.country !== null && !text(c.country, 20)) return false;
    var finite = function (n, lo, hi) { return typeof n === "number" && isFinite(n) && n >= lo && n <= hi; };
    return finite(c.ease, 1.3, 3.5) && finite(c.interval, 0, 3650) && Number.isInteger(c.review_count) && c.review_count >= 0 &&
      c.review_count <= 1e7 && finite(c.due_date, 0, 1e14) && finite(c.last_reviewed, 0, 1e14) && finite(c.added_at, 0, 1e14);
  }

  function read(lang) {
    var scope = validLang(lang) ? lang : "global";
    try {
      var raw = localStorage.getItem(storageKey(scope));
      if (!raw) return { version: VERSION, cards: {} };
      var o = JSON.parse(raw);
      if (!o || o.version !== VERSION || !o.cards || typeof o.cards !== "object" || Array.isArray(o.cards) ||
          Object.keys(o).some(function (k) { return k !== "version" && k !== "cards"; }) ||
          Object.keys(o.cards).length > MAX_CARDS ||
          Object.keys(o.cards).some(function (id) { return !validCard(o.cards[id], scope, id); })) throw new Error("unreadable");
      return o;
    } catch (e) { return { version: VERSION, cards: {}, locked: true }; }
  }
  function write(lang, o) {
    if (o.locked) return false;
    try { localStorage.setItem(storageKey(lang), JSON.stringify({ version: o.version, cards: o.cards })); return true; }
    catch (e) { return false; }
  }
  function contentId(prompt, answer, lang) {
    var s = (lang || "") + "|" + String(prompt || "") + "|" + String(answer || ""), h = 0;
    for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
    return "c" + Math.abs(h).toString(36);
  }

  var SRS = {
    version: VERSION,
    validCard: validCard,
    isReadable: function (lang) { return !read(lang).locked; },

    add: function (spec) {
      if (!spec || typeof spec.prompt !== "string" || typeof spec.answer !== "string" || !spec.prompt || !spec.answer ||
          spec.prompt.length > 2000 || spec.answer.length > 2000) return { added: false, reason: "invalid card" };
      var lang = spec.language || "global";
      if (!validLang(lang)) return { added: false, reason: "invalid language" };
      var o = read(lang);
      if (o.locked) return { added: false, reason: "Unreadable saved deck preserved. Import a validated backup to replace it." };
      var id = spec.card_id || contentId(spec.prompt, spec.answer, lang);
      if (!validId(id)) return { added: false, reason: "invalid card id" };
      if (own(o.cards, id)) return { id: id, added: false, card: o.cards[id] };
      if (spec.srs_eligible === false) return { id: id, added: false, reason: "not eligible" };
      if (Object.keys(o.cards).length >= MAX_CARDS) return { added: false, reason: "Review deck capacity reached." };
      var now = Date.now();
      var card = {
        card_id: id, content_id: spec.content_id || id, language: lang, target: spec.target || spec.prompt, source: spec.source || "",
        prompt: spec.prompt, prompt_language: spec.prompt_language || null, answer: spec.answer, category: spec.category || "vocabulary",
        level: spec.level || "A1", skill: spec.skill || "vocabulary", country: spec.country || null, ease: 2.5, interval: 0,
        due_date: now, review_count: 0, last_reviewed: 0, version: VERSION, added_at: now, srs_eligible: true
      };
      if (!validCard(card, lang, id)) return { id: id, added: false, reason: "invalid card metadata" };
      o.cards[id] = card;
      if (!write(lang, o)) return { id: id, added: false, reason: "storage unavailable" };
      return { id: id, added: true, card: card };
    },

    has: function (id, lang) {
      if (!validId(id)) return false;
      if (lang) return own(read(lang).cards, id);
      return SRS.languages().some(function (l) { return own(read(l).cards, id); });
    },

    languages: function () {
      var out = [];
      try {
        for (var i = 0; i < localStorage.length; i++) {
          var k = localStorage.key(i), parts = k ? k.split(":") : [];
          if (parts.length === 4 && k.indexOf(PREFIX) === 0 && parts[3] === "v" + VERSION && validLang(parts[2]) && out.indexOf(parts[2]) < 0) out.push(parts[2]);
        }
      } catch (e) {}
      return out;
    },

    due: function (lang, limit) {
      var langs = lang ? [lang] : SRS.languages(), now = Date.now(), out = [];
      langs.forEach(function (l) {
        var o = read(l);
        Object.keys(o.cards).forEach(function (id) { if (o.cards[id].due_date <= now) out.push(o.cards[id]); });
      });
      out.sort(function (a, b) { return a.due_date - b.due_date; });
      return limit ? out.slice(0, limit) : out;
    },

    all: function (lang) {
      var langs = lang ? [lang] : SRS.languages(), out = [];
      langs.forEach(function (l) { var o = read(l); Object.keys(o.cards).forEach(function (id) { out.push(o.cards[id]); }); });
      return out;
    },

    count: function (lang) {
      var langs = lang ? [lang] : SRS.languages(), total = 0;
      langs.forEach(function (l) { total += Object.keys(read(l).cards).length; });
      return total;
    },

    dueCount: function (lang) { return SRS.due(lang).length; },

    isDue: function (id, lang) {
      if (!validId(id)) return false;
      var langs = lang ? [lang] : SRS.languages(), now = Date.now();
      return langs.some(function (l) { var o = read(l); return own(o.cards, id) && o.cards[id].due_date <= now; });
    },

    review: function (id, rating, lang) {
      if (["again", "hard", "good", "easy"].indexOf(rating) < 0 || !validId(id)) return null;
      var target = lang, o = null;
      if (lang) o = read(lang);
      else SRS.languages().some(function (l) { var x = read(l); if (own(x.cards, id)) { o = x; target = l; return true; } return false; });
      if (!o || o.locked || !own(o.cards, id)) return null;
      var c = o.cards[id], interval = c.interval || 0, ease = c.ease || 2.5;
      if (rating === "again") { interval = 0; ease = Math.max(1.3, ease - 0.2); }
      else if (rating === "hard") { interval = Math.max(1, interval * 1.2); ease = Math.max(1.3, ease - 0.15); }
      else if (rating === "good") { interval = interval === 0 ? 1 : Math.max(1, interval * ease); }
      else { interval = interval === 0 ? 3 : Math.max(1, interval * ease * 1.3); ease = Math.min(3.5, ease + 0.15); }
      c.interval = Math.min(3650, Math.round(interval * 10) / 10);
      c.ease = Math.round(ease * 100) / 100;
      c.review_count = Math.min(1e7, (c.review_count || 0) + 1);
      c.last_reviewed = Date.now();
      c.due_date = c.last_reviewed + (rating === "again" ? AGAIN_DELAY : Math.round(c.interval * DAY));
      if (!write(target, o)) return null;
      try { window.dispatchEvent(new CustomEvent("ekguru:srs-review", { detail: { language: target, card_id: id, rating: rating, level: c.level } })); } catch (e) {}
      return c;
    },

    remove: function (id, lang) {
      if (!validId(id)) return false;
      var removed = false;
      (lang ? [lang] : SRS.languages()).forEach(function (l) {
        var o = read(l);
        if (!o.locked && own(o.cards, id)) { delete o.cards[id]; if (write(l, o)) removed = true; }
      });
      return removed;
    },

    addMistake: function (questionId, lang, level, skill) {
      return SRS.add({ card_id: "mistake-" + questionId, language: lang || "global", prompt: "Mistake: " + questionId,
        answer: "Review needed", category: "mistake", level: level || "A1", skill: skill || "general", srs_eligible: true });
    },

    getDueCardsByLanguage: function () {
      var out = {};
      SRS.languages().forEach(function (l) { out[l] = SRS.due(l, 20); });
      return out;
    }
  };

  window.EkGuruGlobalSRS = SRS;
  if (window.EkGuruSRS) window.EkGuruSRS.global = SRS;
})();
