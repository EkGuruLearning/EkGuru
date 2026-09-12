/* =========================================================
   EkGuru — VOCABULARY + PHRASE ENGINE (Phase 7C §30, reusable)
   ---------------------------------------------------------
   Generic renderer over authored vocabulary/phrase items. Each
   item has target script, romanisation, source-language meaning,
   part of speech, register, topic, level and its real source.
   Renders an "Add to review" hook through EkGuruSRS where the
   card model is language-agnostic.

   Window API: window.EkGuruVocab
     ready()                 -> Promise resolved once data loaded
     list(filter)            -> all items (optionally filtered)
     get(id)                 -> one item
     byType("word"|"phrase")
     byTopic(topic)
     byLevel(level)
     render(el, id)          -> one item card
     renderList(el, filter)  -> many item cards
   ========================================================= */
(function (root) {
  "use strict";

  var cache = null;
  var readyPromise = null;

  function dataUrl() {
    try {
      var cs = document.currentScript;
      if (cs && cs.src) {
        var p = cs.src.split("?")[0];
        return p.substring(0, p.lastIndexOf("/") + 1) + "../data/vocab-phrase-data.json";
      }
    } catch (e) {}
    return "data/vocab-phrase-data.json";
  }
  var DATA_URL = dataUrl();

  function load() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise(function (resolve, reject) {
      if (typeof root.fetch !== "function") { reject(new Error("no fetch")); return; }
      root.fetch(DATA_URL, { cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("vocab " + r.status)); })
        .then(function (d) { cache = d.items || []; resolve(cache); })
        .catch(function (e) { reject(e); });
    });
    return readyPromise;
  }

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  function find(id) {
    return (cache || []).filter(function (i) { return i.id === id; })[0] || null;
  }

  function itemHTML(i, compact) {
    var h = '<article class="v-item" data-vid="' + esc(i.id) + '" data-hi-card="' + esc(JSON.stringify({ p: i.target, a: i.meaning, c: i.topic || "vocabulary" })) + '">'
      + '<p class="v-target" lang="hi" dir="auto">' + esc(i.target) + "</p>"
      + '<p class="v-roman">' + esc(i.roman) + "</p>"
      + '<p class="v-meaning">' + esc(i.meaning) + "</p>";
    if (!compact) {
      if (i.pos) h += '<span class="v-pos">' + esc(i.pos) + "</span>";
      if (i.register) h += '<span class="v-reg">' + esc(i.register) + "</span>";
      h += '<span class="v-topic">' + esc(i.topic || "") + "</span>";
    }
    h += "</article>";
    return h;
  }

  var API = {
    ready: load,
    list: function () { return cache || []; },
    get: find,
    byType: function (t) { return (cache || []).filter(function (i) { return i.type === t; }); },
    byTopic: function (t) { return (cache || []).filter(function (i) { return i.topic === t; }); },
    byLevel: function (l) { return (cache || []).filter(function (i) { return i.level === l; }); },
    render: function (el, id) {
      if (!el) return;
      var i = find(id);
      if (!i) { el.innerHTML = '<p class="muted">Item not found.</p>'; return; }
      el.innerHTML = itemHTML(i, false);
      if (root.EkGuruSRS && typeof root.EkGuruSRS.mountAddButtons === "function") root.EkGuruSRS.mountAddButtons();
    },
    renderList: function (el, filter) {
      if (!el) return;
      var list = (cache || []).filter(function (i) { return !filter || filter(i); });
      if (!list.length) { el.innerHTML = '<p class="muted">No items match.</p>'; return; }
      el.innerHTML = list.map(function (i) { return itemHTML(i, true); }).join("");
      if (root.EkGuruSRS && typeof root.EkGuruSRS.mountAddButtons === "function") root.EkGuruSRS.mountAddButtons();
    }
  };

  root.EkGuruVocab = API;
})(typeof window !== "undefined" ? window : globalThis);
