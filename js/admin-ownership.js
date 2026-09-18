/* =========================================================
   EkGuru — OWNERSHIP CHECK  (js/admin-ownership.js)
   ---------------------------------------------------------
   Prakash:

     "copyright only ekguru ke pass hi ye pata hona chahiye
      ki jo text apna hai vo apna hi ho ... admin mai agar
      koi sheet copy kar de to pata chal jaye ... ya hum
      check kar sake ki hai ki nahi copy."

   Two questions, one textarea:

     1. "ye text hamara hai?" — paste anything (a paragraph
        from another site, a row out of a sheet, a document
        somebody sent you) and this says which of our pages it
        came from, how much of it matches, and the fingerprint
        of that page as it was built.

     2. "koi hamara text utha kar le gaya?" — for the same
        answer in the other direction: search one of our pages
        on Google, and if it appears somewhere else without the
        source line, the fingerprint in this panel is the dated
        record that it was ours first.

   The corpus is data/copy-index.json, written by
   tools/build-copy-index.js: for every page, its title, its
   word count, a sha1 of its whole text, and up to 48 eight-word
   shingle hashes.

   Why shingles and not the whole page: nobody republishes nine
   hundred words unchanged. They lift two paragraphs. Eight
   words is the shortest run that is still specific — shorter
   and every page matches every page, longer and a single edited
   word breaks the match.

   Nothing leaves the browser. The index is a static file.
   ========================================================= */

(function () {
  "use strict";

  var INDEX_URL = "data/copy-index.json";
  var SHINGLE = 6;          // must match tools/build-copy-index.js
  var MIN_WORDS = 40;          // below this, a match is a coincidence
  var GOOD = 0.45;             // score that means "this is our text"
  var SOME = 0.15;             // "part of it is ours"

  var index = null;
  var loading = null;

  var $ = function (sel) { return document.querySelector(sel); };

  /* ---------------------------------------------------------
     hashing — must match tools/build-copy-index.js exactly, or
     nothing matches anything and the panel lies by saying
     "not ours" to our own text.
     --------------------------------------------------------- */
  function h32(word) {
    var h = 2166136261 >>> 0;
    for (var i = 0; i < word.length; i++) {
      h ^= word.charCodeAt(i);
      h = Math.imul(h, 16777619) >>> 0;
    }
    return h >>> 0;
  }

  function words(text) {
    return String(text).toLowerCase().replace(/\s+/g, " ").trim().split(" ").filter(Boolean);
  }

  function shinglesOf(list) {
    var wh = list.map(h32);
    var out = [];
    for (var i = 0; i + SHINGLE <= wh.length; i++) {
      var h = 0;
      for (var k = 0; k < SHINGLE; k++) h = (Math.imul(h, 31) + wh[i + k]) >>> 0;
      out.push(h);
    }
    if (out.length <= 160) return out;
    /* the same spread the builder uses, so a 900-word paste samples the
       same windows its page does */
    var step = out.length / 160, kept = [];
    for (var j = 0; j < 160; j++) kept.push(out[Math.floor(j * step)]);
    return kept;
  }

  function digest(text) {
    /* a short, stable fingerprint for a passage. Not a cryptographic sha1
       (that is the builder's, over the whole page); this only has to be
       stable enough to compare two pastes months apart. */
    var h1 = 2166136261 >>> 0, h2 = 5381 >>> 0;
    for (var i = 0; i < text.length; i++) {
      var c = text.charCodeAt(i);
      h1 ^= c; h1 = Math.imul(h1, 16777619) >>> 0;
      h2 = (Math.imul(h2, 33) + c) >>> 0;
    }
    return (h1.toString(16) + h2.toString(16)).slice(0, 16);
  }

  /* ---------------------------------------------------------
     the corpus
     --------------------------------------------------------- */
  function load() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    setStatus("Loading the site's fingerprints… (one static file, about a megabyte " +
      "compressed, cached after the first visit)");
    loading = fetch(INDEX_URL, { cache: "force-cache" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (j) {
        /* sets beat arrays for the containment test */
        j.pages.forEach(function (p) {
          var set = Object.create(null);
          for (var i = 0; i < p.s.length; i++) set[p.s[i]] = 1;
          p._set = set;
        });
        index = j;
        setStatus(index.pages.length + " page fingerprints, built " +
          index.generated.slice(0, 10) + " (" + index.shingle + "-word shingles).");
        return j;
      })
      .catch(function (e) {
        setStatus("Could not load " + INDEX_URL + " — " + e.message +
          ". Run: node tools/build-copy-index.js", true);
        loading = null;
        throw e;
      });
    return loading;
  }

  /* ---------------------------------------------------------
     the check
     --------------------------------------------------------- */
  /* ---------------------------------------------------------
     The score, and why it is not just "shared / total".

     Each page stores 160 windows out of `n` — a sample, so the
     raw overlap for a true match is only as big as the sample
     is dense (160/600 ≈ 0.27). Dividing by that density is
     what turns "some words overlap" into "this IS that page":
     a page pasted whole scores 1.00, a lifted paragraph scores
     0.4-0.8, unrelated text scores 0.00.

     The guard at the end is the other half: one shared window
     out of twenty is a common phrase, not a match, and it used
     to attribute 25-word pastes to the wrong page.
     --------------------------------------------------------- */
  function compare(text) {
    var w = words(text);
    if (w.length < SHINGLE) return { shingles: [], hits: [], words: w.length };
    var mine = shinglesOf(w);
    var guard = Math.max(2, Math.ceil(mine.length * 0.06));
    var hits = [];
    for (var i = 0; i < index.pages.length; i++) {
      var p = index.pages[i];
      var shared = 0;
      for (var j = 0; j < mine.length; j++) if (p._set[mine[j]]) shared++;
      if (shared < guard) continue;
      var density = Math.min(1, p.s.length / (p.n || p.s.length || 1));
      var coverage = density ? Math.min(1, (shared / mine.length) / density) : 0;
      var precision = shared / Math.min(mine.length, p.s.length || 1);
      var score = Math.max(coverage, precision);
      if (score > 0.05) hits.push({ page: p, score: score, shared: shared,
        coverage: coverage, precision: precision });
    }
    hits.sort(function (a, b) { return b.score - a.score; });
    return { shingles: mine, hits: hits.slice(0, 8), words: w.length };
  }

  /* ---------------------------------------------------------
     The verdict, and the trap it has to avoid.

     Half the site is generated from templates: 365 daily lessons,
     196 country funnels, 39 courses. A template sentence — "Day 7
     of 365 · today's word", the "how to use this page" block, a
     footer line — sits on hundreds of pages, and a matcher that
     only looks at the BEST hit answers "this is /daily-hindi/day-7/"
     for a sentence that is equally on all 365 of them. That is a
     wrong answer in the shape of a right one, and it is the kind
     of wrong answer a copyright record cannot afford.

     So the top hit is only a page when it is CLEARLY the top hit:
     if three or more pages match nearly as well, the honest answer
     is "this is shared template text", and the panel says that.
     --------------------------------------------------------- */
  function verdict(hits) {
    var best = hits && hits[0];
    if (!best) {
      return { cls: "warn", text:
        "Not found in EkGuru's own index. Either this text is not ours, or it " +
        "is shorter than " + SHINGLE + " words, or it has been rewritten. " +
        "Fingerprint this paste below and keep it: if the same text later shows " +
        "up on another site, ours is the dated copy." };
    }
    var NEAR = 0.8;
    var near = [];
    for (var i = 0; i < hits.length; i++) {
      if (i === 0 || hits[i].score >= best.score * NEAR) near.push(hits[i]);
    }
    if (near.length >= 3 && best.score >= SOME) {
      var names = near.slice(0, 3).map(function (h) { return "/" + h.page.u; }).join(", ");
      return { cls: "warn", text:
        "Shared text — this passage matches " + near.length + " or more EkGuru pages " +
        "about equally well (" + names + "). That is a template block: a lesson " +
        "template, a navigation or footer sentence, a " +
        "\u201chow to use this page\u201d paragraph. It is ours, but it cannot " +
        "identify one page — fingerprint the unique paragraph of the page instead, " +
        "and check which page the text was actually taken from." };
    }
    if (best.score >= GOOD) {
      return { cls: "ok", text:
        "This is EkGuru's own text — " + Math.round(best.score * 100) +
        "% match with /" + best.page.u + " (" + best.page.w + " words, " +
        best.shared + " shared windows). The page's fingerprint is " +
        best.page.sha + "; if this same passage appears on another site without " +
        "a link back, that record is what shows it was ours first." };
    }
    if (best.score >= SOME) {
      return { cls: "warn", text:
        "Partly ours — " + Math.round(best.score * 100) + "% match with /" +
        best.page.u + " (" + best.shared + " shared windows). A paragraph this " +
        "size usually means a passage was reused in a new page: check the two " +
        "say different things, or Google treats them as one page and drops one." };
    }
    return { cls: "warn", text:
      "Only " + Math.round(best.score * 100) + "% overlaps with /" + best.page.u +
      " — common phrasing, not copied text. Fingerprint the paste below and keep " +
      "it: if it shows up elsewhere later, this is the dated copy." };
  }

  /* ---------------------------------------------------------
     the panel
     --------------------------------------------------------- */
  function setStatus(msg, bad) {
    var el = $("#owStatus");
    if (!el) return;
    el.textContent = msg;
    el.className = bad ? "muted bad" : "muted";
  }

  function render(text) {
    var out = $("#owResult");
    var res = compare(text);
    var v = verdict(res.hits);
    var rows = res.hits.map(function (h) {
      return '<tr><td><a href="' + h.page.u + '" target="_blank" rel="noopener">' +
        (h.page.t || h.page.u) + "</a><br><small class=\"muted\">/" + h.page.u +
        "</small></td><td>" + Math.round(h.score * 100) + "%</td>" +
        "<td><code>" + h.page.sha + "</code><br><small class=\"muted\">" +
        h.page.w + " words</small></td></tr>";
    }).join("");

    out.innerHTML =
      '<p class="ow-verdict ' + v.cls + '">' + v.text + "</p>" +
      '<p class="muted">This paste: <b>' + res.words + "</b> words · windows <b>" +
      res.shingles.length + "</b> · fingerprint <code>" +
      digest(text) + "</code> · checked " + new Date().toISOString().slice(0, 10) + "</p>" +
      (rows
        ? '<table class="scroll"><tr><th>Closest page on the site</th><th>Match</th>' +
          "<th>Page fingerprint</th></tr>" + rows + "</table>"
        : "");
  }

  function run() {
    var box = $("#owText");
    if (!box) return;
    var text = box.value.trim();
    if (words(text).length < MIN_WORDS) {
      $("#owResult").innerHTML = '<p class="muted">Paste at least ' + MIN_WORDS +
        " words. Below that the answer is noise in both directions — measured on " +
        "this corpus: a 25-word paste can land on the wrong page, a 40-word one " +
        "does not.</p>";
      return;
    }
    load().then(function () { render(text); })
          .catch(function (e) { $("#owResult").innerHTML = '<p class="muted">' + e.message + "</p>"; });
  }

  function boot() {
    var card = $("#ownership");
    if (!card) return;
    setStatus("Press Check — the fingerprint file loads once.");
    card.addEventListener("click", function (e) {
      var t = e.target;
      if (t && t.id === "owRun") run();
      if (t && t.id === "owClear") {
        $("#owText").value = "";
        $("#owResult").innerHTML = "";
      }
    });
    /* Ctrl+Enter is how a paste-and-check gets done the second time */
    card.addEventListener("keydown", function (e) {
      if (e.target && e.target.id === "owText" && (e.ctrlKey || e.metaKey) && e.key === "Enter") run();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();

  /* ---------------------------------------------------------
     The matcher, exposed. tools/test-copy-index.mjs drives THIS
     code rather than a re-implementation of it — the whole point
     of the panel is that the builder and the browser agree on
     what a text fingerprint is, and two copies of the hashing
     cannot be trusted to stay in step.
     --------------------------------------------------------- */
  window.EkGuruOwnership = {
    load: load,
    compare: compare,
    digest: digest,
    shingle: SHINGLE,
    samples: 160,
    thresholds: { good: GOOD, some: SOME, minWords: MIN_WORDS }
  };
})();
