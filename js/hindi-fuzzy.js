/* =========================================================
   EkGuru — HINDI FUZZY MATCHING  (v1)
   ---------------------------------------------------------
   Small, dependency-free helpers shared by two features:

   1. Search (§16) — matching priority: exact → Unicode-normalised
      → curated Roman↔Devanagari mapping → lightweight fuzzy.
      Examples: "namaste" → नमस्ते, "aap" → आप, "kaise" → कैसे.
   2. Typing trainer (§11) — conservative normalisation of the
      learner's Devanagari input so harmless Unicode/space/punct
      differences are not marked wrong.

   The curated map is deliberately small and high-confidence; it
   is a helper, not a claim of universal transliteration.
   ========================================================= */
(function () {
  "use strict";

  var ROMAN2DEV = {
    "namaste": "नमस्ते", "namaskar": "नमस्कार", "namaskaar": "नमस्कार",
    "aap": "आप", "tum": "तुम", "tu": "तू",
    "kaise": "कैसे", "kaisa": "कैसा", "kaisi": "कैसी",
    "kya": "क्या", "haal": "हाल", "hai": "है", "hain": "हैं",
    "shukriya": "शुक्रिया", "dhanyavaad": "धन्यवाद", "dhanyavad": "धन्यवाद",
    "paani": "पानी", "roti": "रोटी", "chai": "चाय", "chaay": "चाय",
    "ghar": "घर", "dost": "दोस्त", "khaana": "खाना", "khana": "खाना",
    "pyaar": "प्यार", "pyar": "प्यार", "hindi": "हिन्दी", "hindee": "हिन्दी",
    "grammar": "व्याकरण", "numbers": "संख्या", "ginti": "गिनती",
    "ek": "एक", "do": "दो", "teen": "तीन", "sau": "सौ",
    "subah": "सुबह", "suprabhat": "सुप्रभात", "shaam": "शाम",
    "aaj": "आज", "kal": "कल", "daada": "दादा", "naana": "नाना",
    "chacha": "चाचा", "maama": "मामा", "bhookh": "भूख", "achchha": "अच्छा",
    "theek": "ठीक", "nahin": "नहीं", "haan": "हाँ", "jee": "जी",
    "main": "मैं", "hum": "हम", "woh": "वह", "pita": "पिता",
    "maata": "माता", "beta": "बेटा", "beti": "बेटी", "kitab": "किताब",
    "school": "स्कूल", "paisa": "पैसा", "paise": "पैसे", "kitna": "कितना",
    "kitne": "कितने", "phrasebook": "वाक्य", "vocabulary": "शब्दावली",
    "shabdkosh": "शब्दकोश"
  };

  var DEV2ROMAN = {};
  Object.keys(ROMAN2DEV).forEach(function (k) {
    var d = ROMAN2DEV[k];
    if (!DEV2ROMAN[d]) DEV2ROMAN[d] = k;
  });

  function norm(s) {
    try { return String(s == null ? "" : s).normalize("NFC").toLowerCase().trim(); }
    catch (e) { return String(s == null ? "" : s).toLowerCase().trim(); }
  }

  function stripNoise(s) {
    return norm(s)
      .replace(/[\u200b-\u200f\ufeff]/g, "")   // zero-width / bidi marks
      .replace(/[।॥,;:!?]/g, "")                 // danda + punctuation
      .replace(/\s+/g, " ");
  }

  /* Candidate forms of a query term, in matching-priority order. */
  function expand(term) {
    var out = [];
    var t = norm(term);
    if (!t) return out;
    out.push(t);                                 // 1 exact
    var s = stripNoise(t);
    if (s !== t) out.push(s);                    // 2 unicode/format normalised
    if (ROMAN2DEV[t]) out.push(norm(ROMAN2DEV[t]));        // 3 roman → devanagari
    if (DEV2ROMAN[t]) out.push(norm(DEV2ROMAN[t]));        // 3 devanagari → roman
    // 4 lightweight fuzzy: single transposition / one-edit for longer words
    if (t.length >= 5) {
      for (var i = 0; i < t.length - 1; i++) {
        out.push(t.slice(0, i) + t.charAt(i + 1) + t.charAt(i) + t.slice(i + 2));
      }
    }
    var seen = {};
    return out.filter(function (x) { if (seen[x]) return false; seen[x] = 1; return true; });
  }

  /* True if `needle` (a candidate form) is found inside `haystack`. */
  function hits(haystack, candidate) {
    return String(haystack).indexOf(candidate) > -1;
  }

  /* ---- typing trainer: conservative comparison (§11) ---- */
  function normSp(s) {
    // NFC + collapse whitespace, but KEEP punctuation (it is meaningful)
    var t = norm(s);
    return t.replace(/[\u200b-\u200f\ufeff]/g, "").replace(/\s+/g, " ");
  }
  function stripPunct(s) {
    return s.replace(/[\s,;:!?।॥\-'"“”‘’]+/g, "");
  }
  function compare(expected, actual) {
    var e = normSp(expected);
    var a = normSp(actual);
    if (!a) return { state: "empty" };
    if (e === a) return { state: "correct" };
    // minor-format: identical once spacing + punctuation are ignored
    if (stripPunct(e) === stripPunct(a)) return { state: "minor-format" };
    return { state: "incorrect" };
  }

  window.EkGuruFuzzy = {
    norm: norm,
    expand: expand,
    hits: hits,
    compare: compare,
    ROMAN2DEV: ROMAN2DEV,
    DEV2ROMAN: DEV2ROMAN
  };
})();
