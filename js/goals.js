/* =========================================================
   EkGuru — GOAL SYSTEM (Phase 7C §15, deterministic)
   ---------------------------------------------------------
   Eleven supported goals. Availability is computed from the REAL
   content graph by topic — a goal is only selectable where enough
   real content exists (PRODUCTION >= 10 entities, PARTIAL >= 1,
   PLANNED = 0). Rules, not AI. Falls back to honest PLANNED if
   the content graph is unavailable.

   Window API: window.EkGuruGoals
     ready()            -> Promise once goals + graph are loaded
     list()             -> all goals with computed availability
     availability(id)   -> {status, entities, note}
     render(el)         -> render all goals with honest status
   ========================================================= */
(function (root) {
  "use strict";

  var cache = null;
  var readyPromise = null;
  var MIN_PRODUCTION = 10;

  function dataUrl() {
    try {
      var cs = document.currentScript;
      if (cs && cs.src) {
        var p = cs.src.split("?")[0];
        return p.substring(0, p.lastIndexOf("/") + 1) + "../data/goals-phase7c.json";
      }
    } catch (e) {}
    return "data/goals-phase7c.json";
  }
  var DATA_URL = dataUrl();

  function load() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise(function (resolve) {
      var G = root.EkGuruContent;
      var gReady = (G && typeof G.ready === "function") ? G.ready() : Promise.resolve([]);
      Promise.all([
        root.fetch(DATA_URL, { cache: "no-store" }).then(function (r) { return r.json(); }),
        gReady
      ]).then(function (parts) {
        var d = parts[0];
        MIN_PRODUCTION = d.minForProduction || 10;
        var goals = (d.goals || []).map(function (g) {
          var n = 0;
          if (G && typeof G.byTopic === "function") {
            g.topics.forEach(function (t) { n += G.byTopic(t).length; });
          }
          var status = n === 0 ? "PLANNED" : (n >= MIN_PRODUCTION ? "PRODUCTION" : "PARTIAL");
          return {
            id: g.id, name: g.name, blurb: g.blurb, pathSlug: g.pathSlug || null,
            honestNote: g.honestNote || null, status: status, entities: n
          };
        });
        cache = goals;
        resolve(cache);
      }).catch(function () {
        // No graph / no fetch: every goal is honestly unknown, not faked.
        cache = [];
        resolve(cache);
      });
    });
    return readyPromise;
  }

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  var API = {
    ready: load,
    list: function () { return cache || []; },
    availability: function (id) {
      var g = (cache || []).filter(function (x) { return x.id === id; })[0];
      return g || { id: id, status: "PLANNED", entities: 0, note: "not loaded" };
    },
    render: function (el) {
      if (!el) return;
      var goals = cache || [];
      if (!goals.length) { el.innerHTML = '<p class="muted">Goals are loading… (if this persists, the content graph is unavailable and goals are reported as PLANNED.)</p>'; return; }
      var badge = { PRODUCTION: "available", PARTIAL: "partial", PLANNED: "planned" };
      el.innerHTML = '<ul class="goal-list">' + goals.map(function (g) {
        var b = badge[g.status] || "planned";
        var note = g.honestNote ? '<p class="muted">' + esc(g.honestNote) + "</p>" : "";
        return '<li class="goal goal-' + b + '"><span class="goal-name">' + esc(g.name) + '</span>'
          + '<span class="goal-status ' + b + '">' + g.status.toLowerCase() + " · " + g.entities + " items</span>"
          + '<p class="goal-blurb">' + esc(g.blurb) + "</p>" + note + "</li>";
      }).join("") + "</ul>";
    }
  };

  root.EkGuruGoals = API;
})(typeof window !== "undefined" ? window : globalThis);
