/* =========================================================
   EkGuru — GRAMMAR ENGINE (Phase 7C §29, reusable)
   ---------------------------------------------------------
   Data-driven grammar renderer. Each concept carries concept,
   pattern, examples (target script + roman + gloss), exceptions,
   learner note, common mistakes, level and prerequisite, and
   links to the real published lesson it summarises. No grammar
   is invented here — the data file is authored and checked.

   Window API: window.EkGuruGrammar
     ready()          -> Promise resolved once data loaded
     list()           -> all concepts
     get(id)          -> one concept
     byLevel(level)   -> concepts at a level
     render(el, id)   -> render one concept card into el
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
        return p.substring(0, p.lastIndexOf("/") + 1) + "../data/grammar-engine-data.json";
      }
    } catch (e) {}
    return "data/grammar-engine-data.json";
  }
  var DATA_URL = dataUrl();

  function load() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise(function (resolve, reject) {
      if (typeof root.fetch !== "function") { reject(new Error("no fetch")); return; }
      root.fetch(DATA_URL, { cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("grammar " + r.status)); })
        .then(function (d) { cache = d.concepts || []; resolve(cache); })
        .catch(function (e) { reject(e); });
    });
    return readyPromise;
  }

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  function find(id) {
    return (cache || []).filter(function (c) { return c.id === id; })[0] || null;
  }

  function conceptHTML(c) {
    var ex = (c.examples || []).map(function (e) {
      return '<li><span class="g-target">' + esc(e.target) + '</span> <span class="g-roman">' + esc(e.roman) + '</span><span class="g-gloss">' + esc(e.gloss) + "</span></li>";
    }).join("");
    var exc = (c.exceptions || []).map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("");
    var mis = (c.commonMistakes || []).map(function (m) { return "<li>" + esc(m) + "</li>"; }).join("");
    var h = '<article class="g-concept">'
      + '<h3 class="g-name">' + esc(c.concept) + "</h3>"
      + '<p class="g-pattern"><b>Pattern:</b> <span dir="auto">' + esc(c.pattern) + "</span></p>"
      + '<div class="g-meta">Level: ' + esc(c.level || "—")
      + (c.prerequisite ? " · Prerequisite: " + esc(c.prerequisite) : "")
      + (c.sourceUrl ? ' · <a href="' + esc(c.sourceUrl) + '">Read the full lesson: ' + esc(c.sourceTitle || c.concept) + "</a>" : "")
      + "</div>"
      + "<h4>Examples</h4><ul class=\"g-ex\">" + ex + "</ul>"
      + (exc ? "<h4>Exceptions</h4><ul class=\"g-exc\">" + exc + "</ul>" : "")
      + '<p class="g-note"><b>Learner note:</b> ' + esc(c.learnerNote || "") + "</p>"
      + (mis ? "<h4>Common mistakes</h4><ul class=\"g-mis\">" + mis + "</ul>" : "")
      + "</article>";
    return h;
  }

  var API = {
    ready: load,
    list: function () { return cache || []; },
    get: find,
    byLevel: function (lvl) { return (cache || []).filter(function (c) { return c.level === lvl; }); },
    render: function (el, id) {
      if (!el) return;
      var c = find(id);
      if (!c) { el.innerHTML = '<p class="muted">Grammar concept not found.</p>'; return; }
      el.innerHTML = conceptHTML(c);
    },
    renderAll: function (el, filter) {
      if (!el) return;
      var list = (cache || []).filter(function (c) {
        return !filter || filter(c);
      });
      if (!list.length) { el.innerHTML = '<p class="muted">No grammar concepts match.</p>'; return; }
      el.innerHTML = list.map(conceptHTML).join("");
    }
  };

  root.EkGuruGrammar = API;
})(typeof window !== "undefined" ? window : globalThis);
