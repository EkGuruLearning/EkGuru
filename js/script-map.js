/* =========================================================
   EkGuru — DEVANAGARI → OTHER INDIC SCRIPTS
   ---------------------------------------------------------
   WHY THIS EXISTS

   js/translit.js already turns English into Devanagari and
   has been tested against real names. "My name in Punjabi
   writing" is a bigger search than people assume, and the
   answer is not a second transliteration engine — it is a
   script conversion of an answer that already exists.

   Every Indic script is the same abstract structure written
   in different shapes: independent vowels, consonants with an
   inherent "a", vowel signs (matras) that replace it, and a
   virama that cancels it. So one conversion table per script
   covers all of them, and it cannot drift from the Hindi
   engine, because it never re-implements it.

   ---------------------------------------------------------
   WHY NOT JUST ADD UP THE UNICODE OFFSETS

   Because the blocks are not laid out consistently. Gurmukhi
   is +0x100 from Devanagari for most letters, Gujarati +0x180,
   Telugu +0x300 — and then each block has holes exactly where
   that language does not distinguish two sounds that Hindi
   does. Devanagari has ऋ and ृ; Gurmukhi has neither. Tamil
   has no aspirated consonants at all, so ख घ छ झ ठ ढ थ ध फ भ
   have to be approximated, never offset.

   A blind offset writes unassigned codepoints — invisible
   boxes in the browser. So: offset only where the target
   codepoint is actually assigned, and fall back to an explicit
   decision everywhere else.
   ========================================================= */
(function (root) {
  "use strict";

  /* Codepoints each block actually assigns. Anything not listed
     is a hole and must not be produced by an offset. */
  var ASSIGNED = {
    gurmukhi: [
      [0x0a01, 0x0a03], [0x0a05, 0x0a0a], [0x0a0f, 0x0a10], [0x0a13, 0x0a28],
      [0x0a2a, 0x0a30], [0x0a32, 0x0a33], [0x0a35, 0x0a36], [0x0a38, 0x0a39],
      [0x0a3c, 0x0a3c], [0x0a3e, 0x0a42], [0x0a47, 0x0a48], [0x0a4b, 0x0a4d],
      [0x0a51, 0x0a51], [0x0a59, 0x0a5c], [0x0a5e, 0x0a5e], [0x0a66, 0x0a76]
    ],
    gujarati: [
      [0x0a81, 0x0a83], [0x0a85, 0x0a8d], [0x0a8f, 0x0a91], [0x0a93, 0x0aa8],
      [0x0aaa, 0x0ab0], [0x0ab2, 0x0ab3], [0x0ab5, 0x0ab9], [0x0abc, 0x0ac5],
      [0x0ac7, 0x0ac9], [0x0acb, 0x0acd], [0x0ad0, 0x0ad0], [0x0ae0, 0x0ae0],
      [0x0ae6, 0x0aef]
    ],
    bengali: [
      [0x0981, 0x0983], [0x0985, 0x098c], [0x098f, 0x0990], [0x0993, 0x09a8],
      [0x09aa, 0x09b0], [0x09b2, 0x09b2], [0x09b6, 0x09b9], [0x09bc, 0x09c4],
      [0x09c7, 0x09c8], [0x09cb, 0x09cd], [0x09ce, 0x09ce], [0x09dc, 0x09dd],
      [0x09df, 0x09df], [0x09e6, 0x09ef]
    ],
    telugu: [
      [0x0c00, 0x0c03], [0x0c05, 0x0c0c], [0x0c0e, 0x0c10], [0x0c12, 0x0c28],
      [0x0c2a, 0x0c39], [0x0c3d, 0x0c44], [0x0c46, 0x0c48], [0x0c4a, 0x0c4d],
      [0x0c55, 0x0c56], [0x0c58, 0x0c59], [0x0c60, 0x0c61], [0x0c66, 0x0c6f]
    ],
    kannada: [
      [0x0c80, 0x0c83], [0x0c85, 0x0c8c], [0x0c8e, 0x0c90], [0x0c92, 0x0ca8],
      [0x0caa, 0x0cb3], [0x0cb5, 0x0cb9], [0x0cbc, 0x0cc4], [0x0cc6, 0x0cc8],
      [0x0cca, 0x0ccd], [0x0cd5, 0x0cd6], [0x0cde, 0x0cde], [0x0ce0, 0x0ce1],
      [0x0ce6, 0x0cef]
    ],
    malayalam: [
      [0x0d00, 0x0d03], [0x0d05, 0x0d0c], [0x0d0e, 0x0d10], [0x0d12, 0x0d3a],
      [0x0d3d, 0x0d44], [0x0d46, 0x0d48], [0x0d4a, 0x0d4d], [0x0d57, 0x0d57],
      [0x0d60, 0x0d61], [0x0d66, 0x0d6f]
    ]
  };

  function assigned(script, cp) {
    var ranges = ASSIGNED[script];
    if (!ranges) return false;
    for (var i = 0; i < ranges.length; i++) {
      if (cp >= ranges[i][0] && cp <= ranges[i][1]) return true;
    }
    return false;
  }

  /* Block starts. The offset is a hypothesis; `assigned` decides. */
  var BLOCK = {
    gurmukhi: 0x0a00, gujarati: 0x0a80, bengali: 0x0980,
    telugu: 0x0c00, kannada: 0x0c80, malayalam: 0x0d00
  };

  /* Holes that need a decision, not an offset. Keyed by the
     Devanagari codepoint, valued per script. */
  var FIX = {
    /* ऋ — Gurmukhi, Telugu, Kannada, Malayalam, Bengali all have
       this vowel; only the offset differs, so it is handled by
       `assigned`. Nothing to fix here. */

    /* ृ vocalic-r matra. Gurmukhi writes the r AFTER the
       consonant as a rakar, which is exactly what ੍ + ਰ is.
       अमृत → ਅਮ੍ਰਿਤ. */
    "0x0943": { gurmukhi: "\u0a4d\u0a30\u0a3f", bengali: "\u09c3", gujarati: "\u0ac3",
                telugu: "\u0c43", kannada: "\u0cc3", malayalam: "\u0d43" },
    /* ॄ long vocalic r — no everyday equivalent; keep the short one. */
    "0x0944": { gurmukhi: "\u0a4d\u0a30\u0a40", bengali: "\u09c4", gujarati: "\u0ac4",
                telugu: "\u0c44", kannada: "\u0cc4", malayalam: "\u0d44" },
    /* ॅ candra-e (as in बैंक) — Gurmukhi has no candra; the
       nearest honest vowel sign is ੈ. */
    "0x0945": { gurmukhi: "\u0a48" },
    /* ॉ candra-o (John जॉन). Gurmukhi ੌ gives ਜੌਨ, which is how
       Punjabi actually writes John. */
    "0x0949": { gurmukhi: "\u0a4c" },
    /* ॆ / ॊ short e / short o — no Gurmukhi distinction. */
    "0x0946": { gurmukhi: "\u0a47" },
    "0x094a": { gurmukhi: "\u0a4b" },
    /* ऌ and ॢ, ॣ — not used in Indic names we serve. Drop. */
    "0x090c": { gurmukhi: "", bengali: "\u09e0", gujarati: "", telugu: "\u0c0c",
                kannada: "\u0c8c", malayalam: "\u0d0c" },
    "0x0962": { gurmukhi: "" },
    "0x0963": { gurmukhi: "" },
    /* Devanagari nukta consonants. Gurmukhi precomposes ਖ਼ ਗ਼ ਜ਼ ੜ ਫ਼,
       and has no letter for क़ ढ़ य़ — so those get base + nukta. */
    "0x0958": { gurmukhi: "\u0a15\u0a3c" },              /* क़ → ਕ਼ */
    "0x0959": { gurmukhi: "\u0a59" },                    /* ख़ → ਖ਼ */
    "0x095a": { gurmukhi: "\u0a5a" },                    /* ग़ → ਗ਼ */
    "0x095b": { gurmukhi: "\u0a5b" },                    /* ज़ → ਜ਼ */
    "0x095c": { gurmukhi: "\u0a5c" },                    /* ड़ → ੜ  */
    "0x095d": { gurmukhi: "\u0a22\u0a3c" },              /* ढ़ → ਢ਼ */
    "0x095e": { gurmukhi: "\u0a5e" },                    /* फ़ → ਫ਼ */
    "0x095f": { gurmukhi: "\u0a2f\u0a3c" },              /* य़ → ਯ਼ */
    /* Rare Devanagari letters used in loanwords; map to the base. */
    "0x0929": { gurmukhi: "\u0a28" },
    "0x0931": { gurmukhi: "\u0a30" },
    "0x0934": { gurmukhi: "\u0a32\u0a3c" },
    "0x0972": { gurmukhi: "\u0a05" },
    "0x0973": { gurmukhi: "\u0a06" },
    "0x0974": { gurmukhi: "\u0a07" },
    "0x0975": { gurmukhi: "\u0a0a" },
    "0x0976": { gurmukhi: "\u0a09" },
    "0x0977": { gurmukhi: "\u0a0a" },
    /* ॐ */
    "0x0950": { gurmukhi: "\u0a74", bengali: "\u0993\u0982",
                gujarati: "\u0ad0", telugu: "\u0c13\u0c02",
                kannada: "\u0c93\u0c82", malayalam: "\u0d13\u0d02" }
  };

  /* ------------------------------------------------------------------
     TAMIL is the one script that cannot be derived.
     Tamil has no voiced/voiceless distinction and no aspirates:
     one letter க covers ka, kha, ga, gha. So each Devanagari
     consonant must be *decided*, and the honest decision is the
     unaspirated voiceless letter Tamil speakers write.
     ------------------------------------------------------------------ */
  var TAMIL = {
    "\u0905": "\u0b85", "\u0906": "\u0b86", "\u0907": "\u0b87",
    "\u0908": "\u0b88", "\u0909": "\u0b89", "\u090a": "\u0b8a",
    "\u090b": "\u0b89\u0bb0\u0bcd", "\u090f": "\u0b8e", "\u0910": "\u0b90",
    "\u0913": "\u0b92", "\u0914": "\u0b94",
    "\u0915": "\u0b95", "\u0916": "\u0b95", "\u0917": "\u0b95",
    "\u0918": "\u0b95", "\u0919": "\u0b99",
    "\u091a": "\u0b9a", "\u091b": "\u0b9a", "\u091c": "\u0b9c",
    "\u091d": "\u0b9c", "\u091e": "\u0b9e",
    "\u091f": "\u0b9f", "\u0920": "\u0b9f", "\u0921": "\u0b9f",
    "\u0922": "\u0b9f", "\u0923": "\u0ba3",
    "\u0924": "\u0ba4", "\u0925": "\u0ba4", "\u0926": "\u0ba4",
    "\u0927": "\u0ba4", "\u0928": "\u0ba8",
    "\u092a": "\u0baa", "\u092b": "\u0baa", "\u092c": "\u0baa",
    "\u092d": "\u0baa", "\u092e": "\u0bae",
    "\u092f": "\u0baf", "\u0930": "\u0bb0", "\u0932": "\u0bb2",
    "\u0933": "\u0bb3", "\u0935": "\u0bb5",
    "\u0936": "\u0bb7", "\u0937": "\u0bb7", "\u0938": "\u0bb8",
    "\u0939": "\u0bb9",
    "\u0902": "\u0bae\u0bcd", "\u0903": "\u0b83", "\u0901": "\u0bae\u0bcd",
    "\u093e": "\u0bbe", "\u093f": "\u0bbf", "\u0940": "\u0bc0",
    "\u0941": "\u0bc1", "\u0942": "\u0bc2", "\u0943": "\u0bc1\u0bb0\u0bcd",
    "\u0947": "\u0bc7", "\u0948": "\u0bc8", "\u094b": "\u0bcb",
    "\u094c": "\u0bcc", "\u094d": "\u0bcd", "\u093c": ""
  };

  var NAMES = {
    gurmukhi: { en: "Punjabi (Gurmukhi)", native: "ਪੰਜਾਬੀ", script: "Gurmukhi" },
    gujarati: { en: "Gujarati", native: "ગુજરાતી", script: "Gujarati" },
    bengali: { en: "Bengali", native: "বাংলা", script: "Bengali" },
    telugu: { en: "Telugu", native: "తెలుగు", script: "Telugu" },
    kannada: { en: "Kannada", native: "ಕನ್ನಡ", script: "Kannada" },
    malayalam: { en: "Malayalam", native: "മലയാളം", script: "Malayalam" },
    tamil: { en: "Tamil", native: "தமிழ்", script: "Tamil" }
  };

  /* ------------------------------------------------------------------
     GURMUKHI ORTHOGRAPHY, which is not a codepoint question.

     Three things Punjabi does differently from Hindi, and a pure
     mapping gets all three wrong:

     1. NASAL. Hindi writes one anusvara ं everywhere. Gurmukhi
        uses tippi ੰ before a consonant and bindi ਂ at the end of a
        word. सिंह should not come out as ਸਿਂਹ.

     2. REPH. Hindi packs a preceding r into a mark over the next
        letter (र् + श = र्श). Punjabi writes the r as a full letter
        and does not stack it: ਅਰਸ਼, not ਅਰ੍ਸ਼. That is also why
        Punjabi is spelled the way it is — it avoids conjuncts.

     3. CLUSTERS. For the same reason, a virama between two ordinary
        consonants is usually dropped and the inherent a is spoken.
        It is kept before ਰ, ਯ and ਵ, where Gurmukhi genuinely has a
        subscript form (ਪ੍ਰ, ਸ੍ਯ, ਸ੍ਵ).
     ------------------------------------------------------------------ */
  var GUR_KEEP_HALANT = { "\u0a30": 1, "\u0a2f": 1, "\u0a35": 1 };
  var GUR_CONSONANT = /[\u0a15-\u0a28\u0a2a-\u0a30\u0a32-\u0a33\u0a35-\u0a36\u0a38-\u0a39\u0a59-\u0a5e]/;

  function gurmukhiOrthography(text) {
    var c = Array.from(String(text || ""));

    /* 1. anusvara → tippi before a consonant, bindi elsewhere */
    for (var i = 0; i < c.length; i++) {
      if (c[i] === "\u0a02" && i + 1 < c.length && GUR_CONSONANT.test(c[i + 1])) {
        c[i] = "\u0a70";
      }
    }

    /* 2 + 3. drop the virama before an ordinary consonant */
    var out = [];
    for (var j = 0; j < c.length; j++) {
      if (c[j] === "\u0a4d" && j + 1 < c.length &&
          GUR_CONSONANT.test(c[j + 1]) && !GUR_KEEP_HALANT[c[j + 1]]) {
        continue;
      }
      out.push(c[j]);
    }
    return out.join("");
  }

  function convertChar(ch, script) {
    if (script === "tamil") {
      return TAMIL.hasOwnProperty(ch) ? TAMIL[ch] : ch;
    }
    var key = "0x" + ch.codePointAt(0).toString(16).padStart(4, "0");
    var fix = FIX[key];
    if (fix && fix.hasOwnProperty(script)) return fix[script];

    var cp = ch.codePointAt(0);
    /* Only Devanagari gets translated. Anything else passes through,
       so a stray Latin letter or a space is left alone. */
    if (cp < 0x0900 || cp > 0x097f) return ch;

    var target = cp - 0x0900 + BLOCK[script];
    return assigned(script, target) ? String.fromCodePoint(target) : ch;
  }

  /**
   * Convert a Devanagari string into `script`.
   * Devanagari-only letters that have no counterpart are returned
   * unchanged rather than silently deleted, so a caller can see that
   * the conversion was partial (`complete: false`).
   */
  function fromDevanagari(text, script) {
    if (!BLOCK[script] && script !== "tamil") {
      throw new Error("Unknown script: " + script);
    }
    var out = "";
    var complete = true;
    var chars = Array.from(String(text || ""));
    for (var i = 0; i < chars.length; i++) {
      var ch = chars[i];
      var cp = ch.codePointAt(0);
      var conv = convertChar(ch, script);
      if (conv === ch && cp >= 0x0900 && cp <= 0x097f) complete = false;
      out += conv;
    }
    if (script === "gurmukhi") out = gurmukhiOrthography(out);
    return { text: out, script: script, complete: complete };
  }

  /** English → target script, using the Devanagari engine as the source. */
  function fromEnglish(text, script) {
    var engine = root.EkGuruTranslit;
    if (!engine) throw new Error("js/translit.js must load first");
    var dev = engine.transliterate(text);
    var r = fromDevanagari(dev.text, script);
    return {
      input: text,
      devanagari: dev.text,
      text: r.text,
      script: script,
      complete: r.complete,
      unknown: dev.unknown
    };
  }

  var API = {
    fromDevanagari: fromDevanagari,
    fromEnglish: fromEnglish,
    scripts: Object.keys(NAMES),
    names: NAMES,
    _assigned: assigned,
    _convertChar: convertChar
  };

  root.EkGuruScriptMap = API;
})(typeof window !== "undefined" ? window : globalThis);
