/* =========================================================
   EkGuru — GLOBAL SEARCH (Phase 7C §33, language-aware)
   ---------------------------------------------------------
   query → source → target → language → type → level → topic
   One index over real data only:
     · content graph (364 entities: lessons, quizzes, practice,
       phrases, review cards, grammar, pronunciation, culture)
     · authored vocabulary/phrase data (target script + roman)
     · authored grammar concepts
     · deterministic conversation scenarios
     · learning paths

   Matching, in priority order: exact title → prefix → token/
   substring → typo-tolerant (edit distance ≤ 1 on latin fields
   of length ≥ 4). Unicode-normalised and diacritic-folded, so
   "pani", "पानी", "paani" and "water" all find the same item.

   Window API: window.EkGuruSearch
     ready()         -> Promise once the index is built
     search(q, opts) -> ranked results [{type,id,title,subtitle,
                         url,language,level,topic,score}]
     render(el, q)   -> render a result list into el
   ========================================================= */
(function (root) {
  "use strict";

  var index = null;
  var readyPromise = null;

  function baseDir() {
    try {
      var cs = document.currentScript;
      if (cs && cs.src) {
        var p = cs.src.split("?")[0];
        return p.substring(0, p.lastIndexOf("/") + 1) + "../";
      }
    } catch (e) {}
    return "";
  }
  var BASE_DIR = baseDir();

  function dataUrl(path) {
    return BASE_DIR + path;
  }

  function fold(s) {
    var t = String(s == null ? "" : s);
    if (typeof t.normalize === "function") {
      t = t.normalize("NFC").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    } else {
      t = t.toLowerCase();
    }
    return t.replace(/[\u200B-\u200D\uFEFF]/g, "");
  }

  function load() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise(function (resolve, reject) {
      if (typeof root.fetch !== "function") { reject(new Error("no fetch")); return; }
      var G = root.EkGuruContent;
      var graphReady = (G && typeof G.ready === "function") ? G.ready().catch(function () { return []; }) : Promise.resolve([]);
      Promise.all([
        graphReady,
        root.fetch(dataUrl("data/vocab-phrase-data.json"), { cache: "no-store" }).then(function (r) { return r.json(); }).catch(function () { return { items: [] }; }),
        root.fetch(dataUrl("data/grammar-engine-data.json"), { cache: "no-store" }).then(function (r) { return r.json(); }).catch(function () { return { concepts: [] }; }),
        root.fetch(dataUrl("data/conversation-scenarios.json"), { cache: "no-store" }).then(function (r) { return r.json(); }).catch(function () { return { scenarios: [] }; })
      ]).then(function (parts) {
        var graph = parts[0] || [], vocab = parts[1] || {}, gram = parts[2] || {}, conv = parts[3] || {};
        var idx = [];

        (graph || []).forEach(function (e) {
          idx.push({
            type: e.type, id: e.id, title: e.title || e.id, subtitle: (e.level || "") + (e.topic ? " · " + e.topic : ""),
            url: e.url || null, language: e.target_language || "hi", level: e.level || null, topic: e.topic || null,
            fields: fold([e.title, e.topic, e.level].join(" "))
          });
        });

        (vocab.items || []).forEach(function (i) {
          idx.push({
            type: i.type, id: i.id, title: i.target, subtitle: i.roman + " — " + i.meaning,
            url: null, language: "hi", level: i.level || null, topic: i.topic || null,
            fields: fold([i.target, i.roman, i.meaning, i.pos].join(" ")), raw: i
          });
        });

        (gram.concepts || []).forEach(function (c) {
          idx.push({
            type: "grammar", id: c.id, title: c.concept, subtitle: c.pattern,
            url: c.sourceUrl || null, language: "hi", level: c.level || null, topic: "grammar",
            fields: fold([c.concept, c.pattern, (c.examples || []).map(function (e) { return e.target + " " + e.roman; }).join(" ")].join(" ")), raw: c
          });
        });

        (conv.scenarios || []).forEach(function (s) {
          idx.push({
            type: "conversation", id: s.id, title: s.title || s.id, subtitle: s.tagline || "Conversation scenario",
            url: "/learn/hindi/practice/conversation/?scenario=" + encodeURIComponent(s.id), language: "hi", level: s.level || "beginner", topic: s.topic || "conversation",
            fields: fold([s.title, s.tagline, (s.steps || []).map(function (st) { return st.line + " " + st.explanation; }).join(" ")].join(" ")), raw: s
          });
        });

        var PATHS = root.EKGURU_PATHS || [];
        PATHS.forEach(function (p) {
          idx.push({
            type: "path", id: p.slug, title: p.title, subtitle: p.tagline || "Learning path",
            url: "/learn/paths/" + p.slug + "/", language: "hi", level: p.level || null, topic: "path",
            fields: fold([p.title, p.tagline, p.goal].join(" "))
          });
        });

        index = idx;
        resolve(index);
      }).catch(function (e) { reject(e); });
    });
    return readyPromise;
  }

  function lev(a, b) {
    if (a === b) return 0;
    var m = a.length, n = b.length, d = [], i, j;
    if (Math.abs(m - n) > 2) return 3;
    for (i = 0; i <= m; i++) { d[i] = [i]; }
    for (j = 0; j <= n; j++) { d[0][j] = j; }
    for (i = 1; i <= m; i++) for (j = 1; j <= n; j++) {
      var cost = a[i - 1] === b[j - 1] ? 0 : 1;
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost);
    }
    return d[m][n];
  }

  function score(r, qf) {
    var f = r.fields || "";
    var title = fold(r.title || "");
    if (title === qf) return 100;
    if (title.indexOf(qf) === 0) return 90;
    if (f.indexOf(qf) !== -1) return 75;
    // token match
    var toks = f.split(/\s+/);
    for (var i = 0; i < toks.length; i++) if (toks[i] === qf) return 60;
    for (var j = 0; j < toks.length; j++) if (toks[j].indexOf(qf) === 0) return 50;
    // typo tolerance for latin-ish queries
    if (qf.length >= 4 && /^[a-z\s]+$/.test(qf)) {
      for (var k = 0; k < toks.length; k++) {
        if (toks[k].length >= 4 && lev(toks[k], qf) <= 1) return 40;
      }
    }
    return 0;
  }

  var API = {
    ready: load,
    search: function (q, opts) {
      if (!index) return [];
      var qf = fold(q);
      if (!qf) return [];
      opts = opts || {};
      var lang = opts.language || null;
      var type = opts.type || null;
      var out = [];
      index.forEach(function (r) {
        if (lang && r.language !== lang) return;
        if (type && r.type !== type) return;
        var s = score(r, qf);
        if (s > 0) out.push({ type: r.type, id: r.id, title: r.title, subtitle: r.subtitle, url: r.url, language: r.language, level: r.level, topic: r.topic, score: s });
      });
      out.sort(function (a, b) { return b.score - a.score; });
      return out.slice(0, (opts.limit || 20));
    },
    render: function (el, q, opts) {
      if (!el) return;
      var results = API.search(q, opts);
      if (!results.length) {
        el.innerHTML = '<p class="muted">No matches for “' + String(q).replace(/</g, "&lt;") + '”. Try a Hindi word, its romanisation (e.g. <em>paani</em>) or its English meaning (e.g. <em>water</em>).</p>';
        return;
      }
      el.innerHTML = '<ul class="search-results">' + results.map(function (r) {
        var link = r.url ? '<a href="' + r.url.replace(/"/g, "%22") + '">' + r.title.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</a>" : '<span class="s-title">' + r.title.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</span>";
        return '<li class="s-item"><span class="s-type">' + r.type + "</span>" + link
          + '<span class="s-sub">' + String(r.subtitle || "").replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</span>"
          + (r.level || r.topic ? '<span class="s-meta">' + (r.level || "") + (r.level && r.topic ? " · " : "") + (r.topic || "") + "</span>" : "")
          + "</li>";
      }).join("") + "</ul>";
    }
  };

  root.EkGuruSearch = API;
})(typeof window !== "undefined" ? window : globalThis);
