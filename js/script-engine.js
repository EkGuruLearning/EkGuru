/* =========================================================
   EkGuru — SCRIPT ENGINE (Phase 7C §27, reusable)
   ---------------------------------------------------------
   Reading direction, Unicode normalisation and transliteration
   routing for any script in the registry. Honest by design:
     · only Latin (source) and Devanagari (Hindi) are PRODUCTION;
     · every other script reports PLANNED — no fake support;
     · Devanagari→Latin transliteration for arbitrary text is NOT
       offered as a guess: romanisation for course content comes
       from the authored data, and Latin→Devanagari uses the
       existing EkGuruTranslit rule engine (never claimed perfect).

   Window API: window.EkGuruScript
     ready()            -> Promise resolved once registry loaded
     list()             -> all script records
     get(id)            -> one record
     direction(id)      -> "ltr" | "rtl" | null
     isRtl(id)          -> boolean
     supported(id)      -> true only for PRODUCTION scripts
     normalize(text)    -> Unicode NFC + strip zero-width marks
     foldLatin(text)    -> lowercase + strip combining marks (search helper)
     transliterate(text, from, to) -> latin→deva via EkGuruTranslit,
                                      else {ok:false, reason}
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
        return p.substring(0, p.lastIndexOf("/") + 1) + "../data/script-registry-phase7c.json";
      }
    } catch (e) {}
    return "data/script-registry-phase7c.json";
  }
  var DATA_URL = dataUrl();

  function load() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise(function (resolve, reject) {
      if (typeof root.fetch !== "function") { reject(new Error("no fetch")); return; }
      root.fetch(DATA_URL, { cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("script-registry " + r.status)); })
        .then(function (d) { cache = d.scripts || []; resolve(cache); })
        .catch(function (e) { reject(e); });
    });
    return readyPromise;
  }

  function find(id) {
    return (cache || []).filter(function (s) { return s.id === id; })[0] || null;
  }

  var API = {
    ready: load,
    list: function () { return cache || []; },
    get: find,
    direction: function (id) { var s = find(id); return s ? s.direction : null; },
    isRtl: function (id) { return API.direction(id) === "rtl"; },
    supported: function (id) { var s = find(id); return !!(s && s.productionStatus === "PRODUCTION"); },
    normalize: function (text) {
      if (text == null) return "";
      var t = String(text);
      if (typeof t.normalize === "function") t = t.normalize("NFC");
      return t.replace(/[\u200B-\u200D\uFEFF]/g, "");
    },
    foldLatin: function (text) {
      var t = API.normalize(text).toLowerCase();
      if (typeof t.normalize === "function") {
        t = t.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      }
      return t;
    },
    transliterate: function (text, from, to) {
      if (!text) return { ok: false, reason: "empty input" };
      if (from === "latn" && to === "deva") {
        var T = root.EkGuruTranslit;
        if (!T || typeof T.transliterate !== "function") {
          return { ok: false, reason: "transliteration engine not loaded" };
        }
        var out = T.transliterate(text);
        return { ok: true, output: out, engine: "rule-based (EkGuruTranslit)", approximate: true };
      }
      if (from === "deva" && to === "latn") {
        return { ok: false, reason: "Devanagari→Latin for arbitrary text is not generated; romanisation is authored in the course data" };
      }
      return { ok: false, reason: "script pair not supported yet (" + from + "→" + to + ")" };
    }
  };

  root.EkGuruScript = API;
})(typeof window !== "undefined" ? window : globalThis);
