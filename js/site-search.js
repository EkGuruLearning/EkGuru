/* ==========================================================================
   EkGuru — SITE SEARCH ENGINE  (v200)
   --------------------------------------------------------------------------
   Search across the whole site, in the visitor's browser.

   WHAT CHANGED FROM THE INLINE VERSION
   ------------------------------------
   The old /search/ page ran ~60 lines of inline JavaScript: it scored every
   row, printed 40 identical links and stopped there. It worked, and it told
   the reader nothing — no highlighting, no keyboard use, no way to see which
   section a result came from, no memory of what you just searched, and no
   help at all when nothing matched.

   This is the same index and the same promise (nothing you type leaves the
   device), with the parts that make a search page usable:

     · highlighting of the matched words in the title and snippet
     · keyboard control: / to focus, ↑ ↓ to move, Enter to open, Esc to clear
     · a count per section, and the section badge on every result
     · "no results" is a state with suggestions, not a dead end
     · recent searches kept in localStorage — on this device only
     · results are announced to screen readers through aria-live
     · the query is mirrored into ?q= so a result page can be linked to

   INDEX FORMAT (search-index.json, written by tools/build-search-index.py)
     { "u": url, "t": title, "d": description, "s": section, "k": keywords }

   OPTIONAL ENHANCEMENT: js/hindi-fuzzy.js, when present, expands a Roman
   query ("paani") into Devanagari forms ("पानी") and back, so a learner who
   cannot type the script still finds the page.

   Public API:  window.EkGuruSiteSearch = { run, focus, index }
   ========================================================================== */
(function (root, doc) {
  "use strict";

  var ICONS = {
    Answer: "💬", Country: "🌍", "Daily Hindi": "📅", Home: "🏠", Language: "🗣️",
    Lesson: "📘", Location: "📍", Material: "📄", Page: "📃", Phrases: "💬",
    Practice: "🎯", Question: "❓", Tool: "🧰", Tutor: "👩‍🏫", Vocabulary: "🔤"
  };

  var HINTS = [
    ["Devanagari works", "Type पानी, किताब or नमस्ते — the index is Unicode-normalised."],
    ["Roman works too", "“paani”, “kitab”, “namaste” find the same pages when the fuzzy helper is loaded."],
    ["Try a place", "Japan, UAE, Brazil — browse the country guides that passed publication review."],
    ["Try a tool", "flashcards, alphabet, transliteration, numbers."],
    ["Search by type", "Use the filter chips to see only lessons, tools, tutors or materials."],
    ["Search by country", "Pick your country in the Country list — lesson times come in your local time and prices in your currency."],
    ["Search by language", "The Language list keeps the pages written for speakers of your first language."]
  ];

  var POPULAR = ["numbers", "past tense", "Devanagari", "flashcards", "Japan", "kids", "pronunciation", "worksheets"];

  var IDX = null;
  var ready = null;
  var SECTIONS = {};
  var state = { q: "", section: "", country: "", lang: "", active: -1, results: [] };

  var q = doc.getElementById("q");
  var res = doc.getElementById("res");
  var sc = doc.getElementById("sc");
  var sf = doc.getElementById("sf");
  var cf = doc.getElementById("c-country");
  var lf = doc.getElementById("c-lang");
  var live = doc.getElementById("search-live");

  if (!res) return;   /* not the search page */

  /* Base prefix: /search/ is one level down, and the site is served from a
     sub-path on GitHub Pages — derive it instead of hardcoding. */
  var BASE = (function () {
    var s = doc.currentScript;
    var src = s && s.src ? s.src : "";
    var m = src.match(/^(.*?)\/js\/site-search\.js/);
    return m ? m[1] + "/" : "../";
  })();

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function say(msg) {
    if (live) live.textContent = msg;
  }

  /* ---------- loading ---------------------------------------------------- */

  function load() {
    if (ready) return ready;
    ready = fetch(BASE + "search-index.json", { cache: "force-cache" })
      .then(function (r) { return r.json(); })
      .then(function (json) {
        IDX = json || [];
        IDX.forEach(function (row) { SECTIONS[row.s] = (SECTIONS[row.s] || 0) + 1; });
        paintSectionCounts();
        buildFacets(IDX);
        return IDX;
      })
      .catch(function () {
        sc.textContent = "Could not load the search index. The section links below still work.";
        IDX = [];
        return IDX;
      });
    return ready;
  }

  /* ---------- facets: country and language ------------------------------
     Prakash: "search mai done se search ho ... country or language".

     Published country guides and location pages are in the index, as are
     published language starter/course hubs and translated market pages. The
     section pills answer "what kind of page is this"; these two answer the
     question a visitor actually has — "for MY country" and "for MY
     language" — and they combine with the pills rather than replacing them.

     The facets are derived from the publication-filtered index at load, so a
     page appears only after its release gate allows search discovery.
     ---------------------------------------------------------------------- */

  /* A country slug from a URL, or "" — the two shapes the site uses. */
  function countryOf(u) {
    var m = /^learn-hindi-from-([a-z0-9-]+)(?:\/|$)/.exec(u);
    if (m) return m[1];
    m = /^hindi-tutor\/([a-z0-9-]+)\//.exec(u);
    if (m) return m[1];
    return "";
  }

  /* A language slug from a URL, or "". Three shapes: the "for speakers"
     guides ("learn-hindi-for-japanese-speakers/"), the starter packs
     ("languages/ja/") and the seven translated markets ("ja/hindi/").

     The three shapes spell the same language three different ways — the
     guides use the English name, the packs and markets use the ISO code —
     so returning the raw slug would put "Japanese" and "ja" in the dropdown
     as two separate languages, each with half the pages. LANG_ALIAS is
     filled from the index itself (the starter pack's title carries the
     name: "Learn Japanese basics") before the facets are counted. */
  var LANG_ALIAS = Object.create(null);
  var ISO_LANGUAGE = {
    ar: "arabic", bn: "bengali", de: "german", es: "spanish",
    fr: "french", id: "indonesian", it: "italian", ja: "japanese",
    ko: "korean", pl: "polish", pt: "portuguese", ru: "russian",
    tr: "turkish", ur: "urdu", vi: "vietnamese", zh: "chinese"
  };

  function langSlugFromUrl(u) {
    var m = /^learn-hindi-for-([a-z0-9-]+)-speakers(?:\/|$)/.exec(u);
    if (m) return m[1];                                   /* japanese */
    m = /^languages\/([a-z]{2,3})\//.exec(u);
    if (m) return m[1];                                   /* ja */
    m = /^([a-z]{2})\/hindi(?:\/|$)/.exec(u);
    if (m) return m[1];                                   /* ja */
    return "";
  }

  function languageOf(u) {
    var slug = langSlugFromUrl(u);
    return LANG_ALIAS[slug] || slug;
  }

  function slugify(name) {
    return String(name).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  }

  /* Code → English name, learned from the starter packs. */
  function learnLanguageNames(index) {
    index.forEach(function (row) {
      var m = /^languages\/([a-z]{2,3})\//.exec(row.u);
      if (!m) return;
      var t = String(row.t || "");
      /* "Learn Japanese basics — free starter pack", "Learn Kannada — free
         course", "Learn Arabic with EkGuru …": the name is what sits between
         "Learn" and the first noun-ish separator. */
      var n = /^Learn ([A-Za-zÀ-ÿ' .-]+?)(?:\s+basics|\s+with EkGuru|\s*[—-])/.exec(t) ||
              /^Learn ([A-Za-zÀ-ÿ' .-]+)$/.exec(t);
      if (n) LANG_ALIAS[m[1]] = slugify(n[1]);
    });
    /* "ja/hindi/" is the Japanese-language site, so its language is Japanese
       even where no starter pack exists. */
    index.forEach(function (row) {
      var m = /^([a-z]{2})\/hindi(?:\/|$)/.exec(row.u);
      if (m && LANG_ALIAS[m[1]]) return;
      if (m) LANG_ALIAS[m[1]] = ISO_LANGUAGE[m[1]] || m[1];
    });
  }

  var SMALL = { and: 1, of: 1, the: 1, "in": 1, for: 1, "a": 1, to: 1, st: 1 };

  function pretty(slug) {
    return String(slug).split("-").map(function (w, i) {
      if (i && SMALL[w]) return w;
      return w.charAt(0).toUpperCase() + w.slice(1);
    }).join(" ")
      .replace(/\bUsa\b/, "USA").replace(/\bUae\b/, "UAE")
      .replace(/\bUk\b/, "UK").replace(/\bGcc\b/, "GCC");
  }

  /* The starter packs carry the language name in their title
     ("Learn Japanese basics — free starter pack"), which beats mapping a
     code through a table that would go stale. */
  function languageLabel(slug, index) {
    for (var i = 0; i < index.length; i++) {
      var row = index[i];
      if (languageOf(row.u) !== slug) continue;
      var t = String(row.t || "");
      var m = /^Learn ([A-Za-zÀ-ÿ' ]+?) basics/.exec(t);
      if (m) return m[1];
      m = /^Learn ([A-Za-zÀ-ÿ' ]+?) with EkGuru/.exec(t);
      if (m) return m[1];
      m = /Hindi for ([A-Za-zÀ-ÿ' ]+?) Speakers/.exec(t);
      if (m) return m[1] + " speakers";
      if (t) return t.split(" — ")[0];
    }
    return pretty(slug);
  }

  /* The facet key is the English name, so the label is the key itself. */
  function languageLabel2(slug) {
    if (slug.length === 2 && /^[a-z]{2}$/.test(slug)) {
      /* No starter pack to learn the name from — the ISO code is all we have. */
      return slug.toUpperCase();
    }
    return pretty(slug);
  }

  function buildFacets(index) {
    learnLanguageNames(index);
    var countries = Object.create(null), langs = Object.create(null);
    index.forEach(function (row) {
      var c = countryOf(row.u);
      if (c) countries[c] = (countries[c] || 0) + 1;
      var l = languageOf(row.u);
      if (l) langs[l] = (langs[l] || 0) + 1;
    });
    function options(map, label) {
      return Object.keys(map).sort(function (a, b) {
        return map[b] - map[a] || a.localeCompare(b);
      }).map(function (k) {
        return '<option value="' + esc(k) + '">' + esc(label(k)) +
          " (" + map[k] + ")</option>";
      }).join("");
    }
    if (cf) cf.innerHTML = '<option value="">Every country</option>' + options(countries, pretty);
    if (lf) lf.innerHTML = '<option value="">Every language</option>' +
      options(langs, languageLabel2);
  }

  function matchesFacets(row) {
    if (state.country && countryOf(row.u) !== state.country) return false;
    if (state.lang && languageOf(row.u) !== state.lang) return false;
    return true;
  }

  /* ---------- matching --------------------------------------------------- */

  /* js/hindi-fuzzy.js is optional, and it is requested AFTER this file in the
     page, so it must be looked up at match time rather than at load time —
     capturing it here would always capture null. Without it, exact and prefix
     matching still work, so the page never depends on it. */
  function fuzzy() {
    return root.EkGuruFuzzy || null;
  }

  function forms(word) {
    var FZ = fuzzy();
    if (!FZ || !FZ.expand) return [word];
    try {
      var out = FZ.expand(word) || [word];
      return out.length ? out : [word];
    } catch (e) { return [word]; }
  }

  function scoreRow(row, terms) {
    var t = String(row.t || "").toLowerCase();
    var d = String(row.d || "").toLowerCase();
    var k = String(row.k || "").toLowerCase();
    var total = 0;

    for (var i = 0; i < terms.length; i++) {
      var w = terms[i];
      var best = 0;
      var alts = forms(w);
      for (var f = 0; f < alts.length; f++) {
        var v = alts[f];
        var penalty = (v === w) ? 0 : 1;
        if (t.indexOf(v) > -1) best = Math.max(best, 12 - penalty);
        else if (t.indexOf(v) === 0) best = Math.max(best, 14 - penalty);
        else if (d.indexOf(v) > -1) best = Math.max(best, 5 - penalty);
        else if (k.indexOf(v) > -1) best = Math.max(best, 2 - penalty);
      }
      if (best <= 0) return 0;   /* every term must appear somewhere */
      total += best;
    }

    var phrase = terms.join(" ");
    if (t.indexOf(phrase) > -1) total += 18;
    if (d.indexOf(phrase) > -1) total += 6;
    if (t.toLowerCase() === phrase) total += 12;
    /* Shorter titles are more likely to be the page you meant. */
    total += Math.max(0, 6 - Math.floor((row.t || "").length / 12));
    return total;
  }

  function search(index, query, section) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    var out = [];
    for (var i = 0; i < index.length; i++) {
      var row = index[i];
      if (section && row.s !== section) continue;
      if (!matchesFacets(row)) continue;
      var sc2 = scoreRow(row, terms);
      if (sc2 > 0) out.push({ row: row, score: sc2 });
    }
    out.sort(function (a, b) {
      return b.score - a.score || String(a.row.t).localeCompare(String(b.row.t));
    });
    return out.slice(0, 60);
  }

  /* ---------- highlighting ---------------------------------------------- */

  function mark(text, terms) {
    var safe = esc(text);
    if (!terms.length) return safe;
    var parts = terms
      .filter(function (t) { return t.length > 1; })
      .map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); });
    if (!parts.length) return safe;
    try {
      return safe.replace(new RegExp("(" + parts.join("|") + ")", "gi"), "<mark>$1</mark>");
    } catch (e) {
      return safe;
    }
  }

  /* ---------- rendering -------------------------------------------------- */

  function snippet(text) {
    var s = String(text || "");
    return s.length > 190 ? s.slice(0, 187).replace(/\s+\S*$/, "") + "…" : s;
  }

  function render(hits, terms) {
    state.results = hits;
    state.active = -1;

    if (!terms.length) {
      res.innerHTML = "";
      if (q) q.setAttribute("aria-expanded", "false");
      return;
    }

    if (!hits.length) {
      var suggestions = POPULAR.slice(0, 5).map(function (p) {
        return '<a class="xp-chip" href="?q=' + encodeURIComponent(p) + '">' + esc(p) + "</a>";
      }).join(" ");
      res.innerHTML =
        '<div class="xp-empty"><b>Nothing matched “' + esc(state.q) + '”</b>' +
        "<p>Try one word instead of a phrase, or a simpler form — search understands both " +
        '<span class="xp-script" lang="hi">पानी</span> and “paani”.</p>' +
        '<div class="xp-filters" style="justify-content:center">' + suggestions + "</div>" +
        '<p style="margin-top:14px"><a class="btn btn-ghost" href="?">Clear the search</a>' +
        ' <a class="btn btn-ghost" href="../learn/">Browse free guides instead</a></p></div>';
      if (q) q.setAttribute("aria-expanded", "false");
      return;
    }

    if (q) q.setAttribute("aria-expanded", "true");

    var group = {};
    hits.forEach(function (h) {
      var s = h.row.s || "Page";
      (group[s] = group[s] || []).push(h);
    });

    var html = "";
    Object.keys(group)
      .sort(function (a, b) { return (SECTIONS[b] || 0) - (SECTIONS[a] || 0); })
      .forEach(function (section) {
        var rows = group[section];
        html += '<h2 class="xp-results-head">' + (ICONS[section] || "🔎") + " " + esc(section) +
          ' <small>' + rows.length + (rows.length === 1 ? " result" : " results") + "</small></h2>";
        html += '<div class="xp-results" role="listbox" aria-label="' + esc(section) + ' results">';
        rows.forEach(function (h) {
          var r = h.row;
          html +=
            '<a class="xp-result" role="option" aria-selected="false" href="' + BASE + esc(r.u) + '">' +
              '<span class="xp-result-ico" aria-hidden="true">' + (ICONS[r.s] || "🔎") + "</span>" +
              "<span>" +
                '<span class="xp-result-title">' + mark(r.t, terms) + "</span>" +
                '<span class="xp-result-snippet">' + mark(snippet(r.d), terms) + "</span>" +
                '<span class="xp-result-meta"><span class="xp-badge">' + esc(r.s || "Page") + "</span>" +
                "<span>" + esc(r.u) + "</span></span>" +
              "</span>" +
            "</a>";
        });
        html += "</div>";
      });

    res.innerHTML = html;
    say(hits.length + (hits.length === 1 ? " result" : " results") + " for " + state.q);
  }

  /* ---------- history --------------------------------------------------- */

  function remember(query) {
    if (!query || query.length < 2) return;
    try {
      var key = "ekguru.search.recent";
      var list = JSON.parse(localStorage.getItem(key) || "[]");
      list = list.filter(function (x) { return x !== query; });
      list.unshift(query);
      localStorage.setItem(key, JSON.stringify(list.slice(0, 6)));
      paintRecent();
    } catch (e) { /* private mode, quota — search still works */ }
  }

  function recent() {
    try { return JSON.parse(localStorage.getItem("ekguru.search.recent") || "[]"); }
    catch (e) { return []; }
  }

  function paintRecent() {
    var host = doc.getElementById("search-recent");
    if (!host) return;
    var list = recent();
    if (!list.length) { host.innerHTML = ""; return; }
    host.innerHTML = '<span class="xp-recent-lbl">Recent:</span>' + list.map(function (t) {
      return '<a class="xp-chip" href="?q=' + encodeURIComponent(t) + '">' + esc(t) + "</a>";
    }).join(" ");
  }

  function paintSectionCounts() {
    if (!sf) return;
    Array.prototype.forEach.call(sf.querySelectorAll(".pill"), function (btn) {
      var s = btn.getAttribute("data-s") || "";
      if (!s) return;
      var n = SECTIONS[s];
      if (n && !btn.querySelector("small")) {
        var small = doc.createElement("small");
        small.textContent = " " + n;
        btn.appendChild(small);
      }
    });
  }

  /* ---------- driver ---------------------------------------------------- */

  var timer = null;

  function run(push) {
    var query = String(q.value || "").trim();
    state.q = query;
    state.section = state.section || "";

    if (push !== false) {
      try {
        var url = query ? "?q=" + encodeURIComponent(query) : location.pathname;
        history.replaceState(null, "", url);
      } catch (e) {}
    }

    if (!query) {
      res.innerHTML = "";
      if (q) q.setAttribute("aria-expanded", "false");
      sc.textContent = IDX
        ? "Type to search " + IDX.length + " pages"
        : "Type to search every page on EkGuru";
      say("");
      return;
    }

    sc.textContent = "Searching…";
    load().then(function (index) {
      var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
      var hits = search(index, query, state.section);
      render(hits, terms);
      /* One place writes the status line (updateCount) so the country and
         language the visitor picked are always named in it — otherwise the
         list is filtered by something the page does not mention. */
      if (hits.length) updateCount(hits.length);
      else sc.textContent = "Nothing matched “" + query + "”" +
        (state.section ? " in " + state.section : "") + describeFacets();
      remember(query);
    });
  }

  /* ---------- events ---------------------------------------------------- */

  if (q) {
    q.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { run(); }, 140);
    });
    q.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { q.value = ""; run(); return; }
      var rows = res.querySelectorAll(".xp-result");
      if (!rows.length) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        state.active = Math.max(0, Math.min(rows.length - 1,
          state.active + (e.key === "ArrowDown" ? 1 : -1)));
        rows.forEach(function (r, i) { r.setAttribute("aria-selected", i === state.active ? "true" : "false"); });
        var sel = rows[state.active];
        if (sel && sel.scrollIntoView) sel.scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter" && state.active > -1) {
        e.preventDefault();
        rows[state.active].click();
      }
    });
  }

  var goBtn = doc.getElementById("search-go");
  if (goBtn) {
    goBtn.addEventListener("click", function () {
      if (!q.value.trim()) { q.focus(); return; }
      run(true);
      if (res.firstChild && res.scrollIntoView) res.scrollIntoView({ block: "nearest", behavior: "smooth" });
    });
  }

  /* The two facet selects. Change is the only event that matters (a select
     has no "typing"), and both re-run the current query immediately so the
     result list never disagrees with the controls above it. */
  function bindFacets() {
    if (cf) cf.addEventListener("change", function () {
      state.country = cf.value || "";
      mirror();
      rerun();
    });
    if (lf) lf.addEventListener("change", function () {
      state.lang = lf.value || "";
      mirror();
      rerun();
    });
  }

  /* The URL carries ?q= already; the facet selections belong there too, so a
     narrowed search can be linked or bookmarked and ?c=…&l=… opens with the
     lists already set (see the boot block). */
  function mirror() {
    try {
      var params = new URLSearchParams(location.search);
      if (state.country) params.set("c", state.country); else params.delete("c");
      if (state.lang) params.set("l", state.lang); else params.delete("l");
      var qs = params.toString();
      history.replaceState(null, "", qs ? "?" + qs : location.pathname);
    } catch (e) {}
  }

  function rerun() {
    if (!IDX) return;
    var hits = search(IDX, state.q, state.section);
    render(hits, termsOf(state.q));
    updateCount(hits.length);
  }

  function termsOf(query) {
    return String(query || "").toLowerCase().split(/\s+/).filter(Boolean);
  }

  function describeFacets() {
    var bits = [];
    if (state.country) bits.push(pretty(state.country));
    if (state.lang) bits.push(languageLabel2(state.lang));
    return bits.length ? " · " + bits.join(" · ") : "";
  }

  function updateCount(shown) {
    if (!sc) return;
    sc.textContent = state.q
      ? shown + " result" + (shown === 1 ? "" : "s") + " for “" + state.q + "”" +
        (state.section ? " in " + state.section : "") + describeFacets() +
        " · " + IDX.length + " pages indexed"
      : (state.country || state.lang
          ? IDX.filter(matchesFacets).length + " pages" + describeFacets()
          : "Type to search " + IDX.length + " pages");
  }

  if (sf) {
    sf.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest(".pill") : null;
      if (!btn) return;
      state.section = btn.getAttribute("data-s") || "";
      Array.prototype.forEach.call(sf.querySelectorAll(".pill"), function (x) {
        x.setAttribute("aria-pressed", x === btn ? "true" : "false");
      });
      run(false);
    });
  }

  bindFacets();

  /* Fill both dropdowns immediately. load() used to run only when the visitor
     typed, which left an empty "Every country" list under the search box —
     the facets have to be there before the search, or they look broken. */
  load().then(function () { updateCount(0); });

  /* Section jumps: /search/?s=Tool opens the page already filtered. */
  try {
    var pre = new URLSearchParams(location.search);
    var preQ = pre.get("q");
    var preS = pre.get("s");
    if (preS && sf) {
      var match = sf.querySelector('.pill[data-s="' + preS.replace(/"/g, "") + '"]');
      if (match) {
        state.section = preS;
        Array.prototype.forEach.call(sf.querySelectorAll(".pill"), function (x) {
          x.setAttribute("aria-pressed", x === match ? "true" : "false");
        });
      }
    }
    var preC = pre.get("c"), preL = pre.get("l");
    if (preC && cf) { state.country = preC; cf.value = preC; }
    if (preL && lf) { state.lang = preL; lf.value = preL; }
    if (preQ && q) { q.value = preQ; run(false); }
    else if (preC || preL) load().then(function () { updateCount(0); });
  } catch (e) {}

  paintRecent();

  /* Search-page keyboard shortcut, offered on every page that loads
     js/experience.js too: "/" focuses this box. */
  doc.addEventListener("keydown", function (e) {
    if (e.key !== "/" || e.metaKey || e.ctrlKey || e.altKey) return;
    var tag = (e.target && e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || (e.target && e.target.isContentEditable)) return;
    if (!q) return;
    e.preventDefault();
    q.focus();
    q.select();
  });

  root.EkGuruSiteSearch = {
    run: run,
    focus: function () { if (q) q.focus(); },
    index: function () { return IDX; },
    hints: HINTS,
    popular: POPULAR
  };
})(window, document);
