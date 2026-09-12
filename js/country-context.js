/* =========================================================
   EkGuru — COUNTRY-CONTEXT ENGINE (Phase 7C §34/§12/§13)
   ---------------------------------------------------------
   Adds a country/context lens on shared Hindi content. A context
   (India visitor, NRI/heritage) is made of MODULES; each module
   reuses the real published phrases and links — the engine never
   invents phrases. The shared course (Hindi Basics) is linked,
   not duplicated: contexts point back to the language course.

   Data relationships with the country registry stay data-driven
   through EkGuruContent.byCountry(cca2); the context here is the
   presentation layer.

   Window API: window.EkGuruCountryContext
     ready()                    -> Promise once loaded
     list()                     -> all contexts
     get(id)                    -> one context
     render(el, id, opts)       -> render a context into el
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
        return p.substring(0, p.lastIndexOf("/") + 1) + "../data/country-context-phase7c.json";
      }
    } catch (e) {}
    return "data/country-context-phase7c.json";
  }
  var DATA_URL = dataUrl();

  function load() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise(function (resolve, reject) {
      if (typeof root.fetch !== "function") { reject(new Error("no fetch")); return; }
      root.fetch(DATA_URL, { cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("country-context " + r.status)); })
        .then(function (d) { cache = d.contexts || []; resolve(cache); })
        .catch(function (e) { reject(e); });
    });
    return readyPromise;
  }

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  function find(id) {
    return (cache || []).filter(function (c) { return c.id === id; })[0] || null;
  }

  function phraseRow(p) {
    return '<li class="cc-phrase"><span class="cc-target" lang="hi" dir="auto">' + esc(p.target) + '</span>'
      + '<span class="cc-roman">' + esc(p.roman) + '</span>'
      + '<span class="cc-meaning">' + esc(p.meaning) + "</span></li>";
  }

  function moduleHTML(m) {
    var phrases = (m.phrases || []).map(phraseRow).join("");
    var links = (m.links || []).map(function (l) {
      return '<li><a href="' + esc(l.url) + '">' + esc(l.title) + "</a></li>";
    }).join("");
    return '<section class="cc-mod">'
      + "<h3>" + esc(m.title) + "</h3>"
      + (phrases ? '<ul class="cc-phrases">' + phrases + "</ul>" : "")
      + (links ? '<ul class="cc-links">' + links + "</ul>" : "")
      + "</section>";
  }

  var API = {
    ready: load,
    list: function () { return cache || []; },
    get: find,
    render: function (el, id) {
      if (!el) return;
      var c = find(id);
      if (!c) { el.innerHTML = '<p class="muted">Context not found.</p>'; return; }
      var modules = (c.modules || []).map(moduleHTML).join("");
      el.innerHTML =
        '<div class="cc-head"><h2>' + esc(c.title) + "</h2>"
        + '<p class="cc-sub">' + esc(c.subtitle) + "</p>"
        + '<p class="muted">Audience: ' + esc(c.audience) + '</p>'
        + (c.honestNote ? '<p class="note cc-note">' + esc(c.honestNote) + "</p>" : "")
        + "</div>"
        + '<p class="cc-shared">Shared language course: <a href="/learn/hindi/">' + esc(c.sharedCourse || "Hindi Basics") + "</a> — the context below adds a lens, it does not replace the course.</p>"
        + modules;
      if (root.EkGuruSRS && typeof root.EkGuruSRS.mountAddButtons === "function") root.EkGuruSRS.mountAddButtons();
    }
  };

  root.EkGuruCountryContext = API;
})(typeof window !== "undefined" ? window : globalThis);
