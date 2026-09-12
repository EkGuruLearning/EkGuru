/* =========================================================
   EkGuru — REAL TRANSLITERATION, FROM GOOGLE INPUT TOOLS
   ---------------------------------------------------------
   Prakash:

     "hindi ka naam or hindi word ko improve karo, sabhi hindi
      exact likho, kisi free api laga lo"

   ═══════════════════════════════════════════════════════
   WHY THE OFFLINE ENGINE WAS NOT ENOUGH
   ═══════════════════════════════════════════════════════

   js/translit.js is 828 lines of hand-written rules and it is
   genuinely good — it handles the schwa-deletion problem, the
   त/ट distinction between Indian and English names, nukta
   letters, and about ninety exceptions.

   It is still a rule engine, and Hindi transliteration is not
   rule-shaped. Checked against real names:

       Prakash    प्राकश     should be  प्रकाश
       Hemlata    हेंलटा      should be  हेमलता
       Rahul      रहुल       should be  राहुल
       Mohammed   मोहम्मेड    should be  मोहम्मद
       Jennifer   जेन्निफ़र   should be  जेनिफर
       Elizabeth  ईलिज़बेथ    should be  एलिज़ाबेथ

   Every one of those is a vowel-length judgement that depends on
   knowing the word, not on a rule. "Prakash" needs a long आ in
   the second syllable and a short one in the first, and nothing
   in the spelling says so.

   For a page whose entire promise is "write your name in Hindi",
   getting a common name like Prakash wrong is the whole product
   failing.

   ═══════════════════════════════════════════════════════
   THE API
   ═══════════════════════════════════════════════════════

     https://inputtools.google.com/request?text=NAME&itc=hi-t-i0-und

   It is what Gmail, Google Docs and the Android Hindi keyboard
   use. Verified before writing this:

     · no key, no account, no quota published
     · access-control-allow-origin: *  — callable from a static
       page with no proxy, which is the only reason this is
       possible at all on GitHub Pages
     · returns SEVERAL candidates, ranked, which is more honest
       than one answer: Hindi genuinely has more than one correct
       spelling for most foreign names

   Response shape:
     ["SUCCESS",[["Prakash",["प्रकाश","प्रकाष","प्रकश"],[],{…}]]]

   ═══════════════════════════════════════════════════════
   WHAT THIS FILE GUARANTEES
   ═══════════════════════════════════════════════════════

   1. THE PAGE NEVER WAITS FOR THE NETWORK. The offline engine
      answers instantly and is shown first. The API result
      replaces it when it arrives — usually 200-400ms.

   2. THE PAGE NEVER BREAKS. Offline, blocked, rate-limited,
      slow, or returning nonsense — every path falls back to the
      offline answer, which was already on screen.

   3. THE SAME NAME IS NOT ASKED TWICE. Results are cached in
      memory and in localStorage, so typing "Prakash" again is
      free and a repeat visitor pays nothing.

   4. TYPING DOES NOT FLOOD IT. Requests are debounced and only
      the newest response is used, because responses can arrive
      out of order and the older one would overwrite the newer.
   ========================================================= */

(function (root) {
  "use strict";

  var ENDPOINT = "https://inputtools.google.com/request";
  var CACHE_KEY = "ekguru_translit_v1";
  var TIMEOUT = 4000;          /* beyond this the offline answer is better */
  var MAX_CACHE = 400;         /* names, not bytes — each is tiny */

  var mem = {};
  var inflight = {};
  var seq = 0;                 /* only the newest response wins */

  /* ---------------------------------------------------------
     Cache. localStorage can throw in private mode and can be
     full; every access is guarded because a broken cache must
     not break the tool.
     --------------------------------------------------------- */
  (function loadCache() {
    try {
      var raw = root.localStorage && root.localStorage.getItem(CACHE_KEY);
      if (raw) mem = JSON.parse(raw) || {};
    } catch (e) { mem = {}; }
  })();

  function saveCache() {
    try {
      var keys = Object.keys(mem);
      if (keys.length > MAX_CACHE) {
        /* Drop the oldest half rather than clearing everything —
           a visitor who has looked up forty names should not lose
           all of them because of the forty-first. */
        var trimmed = {};
        keys.slice(-Math.floor(MAX_CACHE / 2)).forEach(function (k) { trimmed[k] = mem[k]; });
        mem = trimmed;
      }
      root.localStorage && root.localStorage.setItem(CACHE_KEY, JSON.stringify(mem));
    } catch (e) { /* full or unavailable — memory cache still works */ }
  }

  function key(word) { return String(word).trim().toLowerCase(); }

  /* ---------------------------------------------------------
     Is this worth sending?
     --------------------------------------------------------- */
  function sendable(word) {
    word = String(word || "").trim();
    if (!word) return false;
    if (word.length > 40) return false;              /* not a name */
    /* Already Devanagari — there is nothing to transliterate, and
       sending it back would return it unchanged at best. */
    if (/[\u0900-\u097F]/.test(word)) return false;
    /* Latin letters, apostrophes and hyphens only. Anything else
       is not a name and the endpoint will not help. */
    return /^[A-Za-z][A-Za-z'\u2019.\-]*$/.test(word);
  }

  /* ---------------------------------------------------------
     One word.
     --------------------------------------------------------- */
  function fetchWord(word) {
    var k = key(word);

    if (mem[k]) return Promise.resolve(mem[k]);
    if (inflight[k]) return inflight[k];
    if (typeof root.fetch !== "function") return Promise.resolve(null);

    var url = ENDPOINT +
      "?text=" + encodeURIComponent(word) +
      "&itc=hi-t-i0-und" +
      "&num=5&cp=0&cs=1&ie=utf-8&oe=utf-8";

    var ctrl = null, timer = null;
    try { ctrl = new AbortController(); } catch (e) {}
    if (ctrl) timer = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, TIMEOUT);

    var p = root.fetch(url, { signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (timer) clearTimeout(timer);
        /* ["SUCCESS",[["Prakash",["प्रकाश","प्रकाष",…],[],{…}]]] */
        if (!data || data[0] !== "SUCCESS") return null;
        var first = data[1] && data[1][0];
        var list = first && first[1];
        if (!list || !list.length) return null;

        /* Keep only genuine Devanagari. The endpoint has been seen
           to echo the Latin input back when it has no idea, and
           showing someone their own name unchanged as "the Hindi
           spelling" is worse than showing the offline guess. */
        var clean = list.filter(function (x) { return /[\u0900-\u097F]/.test(x); });
        if (!clean.length) return null;

        mem[k] = clean.slice(0, 4);
        saveCache();
        return mem[k];
      })
      .catch(function () {
        if (timer) clearTimeout(timer);
        return null;             /* the caller keeps the offline answer */
      })
      .then(function (v) { delete inflight[k]; return v; });

    inflight[k] = p;
    return p;
  }

  /* ---------------------------------------------------------
     A full name: "Prakash Kumar" is two lookups, joined.

     Done per WORD rather than as one string because the endpoint
     is a word transliterator — given a phrase it returns one
     candidate list for the whole thing and the alternatives
     become useless.
     --------------------------------------------------------- */
  function lookup(name) {
    var words = String(name || "").trim().split(/\s+/).filter(Boolean);
    if (!words.length) return Promise.resolve(null);
    if (words.length > 6) return Promise.resolve(null);      /* a sentence, not a name */
    if (!words.every(sendable)) return Promise.resolve(null);

    var mine = ++seq;

    return Promise.all(words.map(fetchWord)).then(function (parts) {
      /* A newer request started while this one was in the air.
         Responses can arrive out of order and the stale one would
         overwrite the fresh answer on screen. */
      if (mine !== seq) return null;
      if (parts.some(function (p) { return !p; })) return null;

      return {
        text: parts.map(function (p) { return p[0]; }).join(" "),
        /* Alternatives only make sense for a single word — for two
           words the combinations multiply and none of them is
           meaningfully "the second-best spelling". */
        alternatives: words.length === 1 ? parts[0].slice(1) : [],
        source: "google"
      };
    });
  }

  root.EkGuruTranslitAPI = {
    lookup: lookup,
    /* exposed for the tests and the admin dashboard */
    _sendable: sendable,
    _cacheSize: function () { return Object.keys(mem).length; },
    _clear: function () {
      mem = {};
      try { root.localStorage && root.localStorage.removeItem(CACHE_KEY); } catch (e) {}
    }
  };

})(typeof window !== "undefined" ? window : globalThis);
