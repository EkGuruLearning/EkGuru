/* =========================================================
   EkGuru — LANGUAGE PACK LOADER (Phase 7C §53 Stage 2)
   ---------------------------------------------------------
   Stage 2 = proof that the engines are reusable across languages.
   A language pack is the SAME data schema as the Hindi engines
   (items + concepts), just with a different target_language.
   This loader lists the packs and renders a pack THROUGH the
   existing engines — EkGuruVocab.renderFrom and
   EkGuruGrammar.renderFrom — so the reuse is real, not a copy.

   Honesty: a pack makes a language BETA (starter reference
   content). Hindi stays the only PRODUCTION language — that
   decision lives in the registry and in data/language-packs.json,
   not in this file.

   Window API: window.EkGuruLangPack
     ready()            -> Promise once the manifest is loaded
     list()             -> pack entries
     get(lang)          -> one entry
     packUrl(lang)      -> data URL for a pack (script-relative)
     render(el, lang)   -> render vocab + phrases + grammar of a
                           pack into el through the shared engines
   ========================================================= */
(function (root) {
  "use strict";

  var manifest = null;
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

  function load() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise(function (resolve, reject) {
      if (typeof root.fetch !== "function") { reject(new Error("no fetch")); return; }
      root.fetch(BASE_DIR + "data/language-packs.json", { cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("packs " + r.status)); })
        .then(function (d) { manifest = d.packs || []; resolve(manifest); })
        .catch(function (e) { reject(e); });
    });
    return readyPromise;
  }

  function get(lang) {
    return (manifest || []).filter(function (p) { return p.lang === lang; })[0] || null;
  }

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  var API = {
    ready: load,
    list: function () { return manifest || []; },
    get: get,
    packUrl: function (lang) {
      var p = get(lang);
      return p && p.file ? BASE_DIR + p.file : null;
    },
    render: function (el, lang) {
      if (!el) return;
      var p = get(lang);
      var url = API.packUrl(lang);
      if (!p || !url) { el.innerHTML = '<p class="muted">Language pack not found.</p>'; return; }

      var html =
        '<div class="lp-head">'
        + '<h3>' + esc(p.name) + ' <span class="lp-tag beta">BETA — starter</span></h3>'
        + '<p class="muted">' + esc(p.honestNote || "") + '</p>'
        + '<p class="muted">' + esc(p.counts.vocab) + ' words · ' + esc(p.counts.phrase) + ' phrases · '
        + esc(p.counts.grammar) + ' grammar concepts — rendered by the same engines that render Hindi.</p>'
        + '</div>'
        + '<h4>Vocabulary &amp; phrases</h4><div class="v-grid" id="lp-vocab"><p class="muted">Loading…</p></div>'
        + '<h4>Grammar reference</h4><div id="lp-grammar"><p class="muted">Loading…</p></div>';
      el.innerHTML = html;

      var V = root.EkGuruVocab, G = root.EkGuruGrammar;
      if (V && typeof V.renderFrom === "function") {
        V.renderFrom(document.getElementById("lp-vocab"), url, null,
                     { listen: true, speechTag: p.speechTag });
      } else {
        document.getElementById("lp-vocab").innerHTML = '<p class="muted">Vocab engine unavailable.</p>';
      }
      if (G && typeof G.renderFrom === "function") {
        G.renderFrom(document.getElementById("lp-grammar"), url);
      } else {
        document.getElementById("lp-grammar").innerHTML = '<p class="muted">Grammar engine unavailable.</p>';
      }
    }
  };

  root.EkGuruLangPack = API;
})(typeof window !== "undefined" ? window : globalThis);
