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
  var packCache = {};   // Phase 7C Stage 2: per-URL cache for language packs

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

  function load(url) {
    url = url || DATA_URL;
    if (url === DATA_URL) {
      if (readyPromise) return readyPromise;
      readyPromise = fetchItems(url);
      return readyPromise;
    }
    if (packCache[url]) return packCache[url];
    packCache[url] = fetchItems(url);
    return packCache[url];
  }

  function fetchItems(url) {
    return new Promise(function (resolve, reject) {
      if (typeof root.fetch !== "function") { reject(new Error("no fetch")); return; }
      root.fetch(url, { cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("vocab " + r.status)); })
        .then(function (d) {
          var items = d.items || [];
          if (url === DATA_URL) cache = items;
          resolve(items);
        })
        .catch(function (e) { reject(e); });
    });
  }

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }

  function find(id) {
    return (cache || []).filter(function (i) { return i.id === id; })[0] || null;
  }

  function itemHTML(i, compact, opts) {
    var listen = opts && opts.listen && opts.speechTag;
    var target = '<p class="v-target" lang="' + esc(i.language || "hi") + '" dir="auto"'
      + (listen ? ' data-say="' + esc(i.target) + '" data-say-lang="' + esc(opts.speechTag) + '"' : "")
      + '>' + esc(i.target) + "</p>";
    var h = '<article class="v-item" data-vid="' + esc(i.id) + '" data-hi-card="' + esc(JSON.stringify({ p: i.target, a: i.meaning, c: i.topic || "vocabulary", l: i.language || "hi" })) + '">'
      + target
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
    },
    /* Phase 7C Stage 2: render an arbitrary language pack through this same
       engine (reuse proof). Defaults to the Hindi data file.
       opts.listen + opts.speechTag add honest browser-TTS "Listen" buttons
       (Stage 4) — never on the default Hindi path. */
    renderFrom: function (el, url, filter, opts) {
      if (!el) return;
      load(url).then(function (items) {
        var list = items.filter(function (i) { return !filter || filter(i); });
        if (!list.length) { el.innerHTML = '<p class="muted">No items match.</p>'; return; }
        el.innerHTML = list.map(function (i) { return itemHTML(i, true, opts); }).join("");
        if (root.EkGuruSRS && typeof root.EkGuruSRS.mountAddButtons === "function") root.EkGuruSRS.mountAddButtons();
        if (opts && opts.listen && root.EkGuruHindiAudio && typeof root.EkGuruHindiAudio.mountSay === "function") {
          root.EkGuruHindiAudio.mountSay();
        }
      }).catch(function () {
        el.innerHTML = '<p class="muted">Language pack unavailable.</p>';
      });
    }
  };

  root.EkGuruVocab = API;
})(typeof window !== "undefined" ? window : globalThis);
