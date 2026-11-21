/* =========================================================
   EkGuru — ENGLISH → NON-INDIC SCRIPTS
   ---------------------------------------------------------
   WHY THIS EXISTS

   The name tool (name-in-script.js) already writes English
   names in every Indic script by going through Devanagari:
   translit.js turns the English into Devanagari phonemes,
   then script-map.js converts codepoints to the target
   script. That works because every Indic script shares the
   same abugida structure and roughly the same phoneme
   inventory.

   Non-Indic scripts do NOT share that structure. Arabic is
   an abjad with diacritics that change meaning. Greek,
   Cyrillic, Hangul, Kana and Ethiopic each have their own
   phoneme inventory and their own orthographic rules. There
   is no common intermediate. So each one needs its own
   English-to-script phonetic mapping.

   This file provides that: one engine per non-Indic script,
   each with the same interface as script-map.js's fromEnglish:
   { text, script, complete, devanagari, input }.

   The `devanagari` field is populated by calling the existing
   translit.js engine, so the page can still show the
   Devanagari intermediate for comparison.

   Each engine works on SOUNDS, not letters, using a rules
   layer that fixes common English spelling traps before
   mapping. This is the same philosophy as translit.js.
   ========================================================= */
(function (root) {
  "use strict";

  /* Shared vowel set — every engine handles these as standalone vowels. */
  var VOWELS = { "a": true, "e": true, "i": true, "o": true, "u": true };

  /* ------------------------------------------------------------------
     Shared English preprocessing: normalise spelling traps.
     Called once in fromEnglish(); engines receive the cleaned string.
     ------------------------------------------------------------------ */
  function preprocess(word) {
    var w = word.toLowerCase();
    w = w.replace(/ph/g, "f");
    w = w.replace(/e$/, "");       // silent final e
    w = w.replace(/ck/g, "k");
    w = w.replace(/x/g, "ks");
    w = w.replace(/qu/g, "kw");
    w = w.replace(/tion/g, "shan");
    w = w.replace(/^wr/, "r");
    w = w.replace(/^kn/, "n");
    w = w.replace(/gh/g, "");
    w = w.replace(/ough/g, "uf");
    w = w.replace(/c(?=[ei])/g, "s");
    w = w.replace(/c/g, "k");
    w = w.replace(/(.)\1/g, "$1");
    return w;
  }

  /* ------------------------------------------------------------------
     ARABIC
     Abjad: consonants carry meaning, vowels are diacritics.
     We write with full diacritics (tashkeel) so the reading is
     unambiguous. Long vowels use alif/waw/ya.
     ------------------------------------------------------------------ */
  function arabicEngine(word) {
    var w = word;
    var out = "";
    var complete = true;
    var i = 0;
    while (i < w.length) {
      var ch = w[i];
      var next = w[i + 1] || "";
      var mapped = "";
      // Digraphs
      if (ch === "sh") { mapped = "ش"; i += 2; }
      else if (ch === "ch") { mapped = "تْش"; i += 2; complete = false; }
      else if (ch === "th") { mapped = "ث"; i += 2; }
      else if (ch === "dh") { mapped = "ذ"; i += 2; }
      else if (ch === "kh") { mapped = "خ"; i += 2; }
      else if (ch === "gh") { mapped = "غ"; i += 2; }
      else if (ch === "qu") { mapped = "قُ"; i += 2; }
      else {
        var c = arabicConsonant(ch);
        if (c) {
          mapped = c;
          if (VOWELS[next]) {
            var v = arabicVowel(next);
            if (v) { mapped += v; i += 2; }
            else { i += 1; }
          } else {
            i += 1;
          }
        } else if (VOWELS[ch]) {
          // Standalone vowel → long vowel
          mapped = arabicLongVowel(ch);
          i += 1;
        } else {
          complete = false;
          mapped = ch;
          i += 1;
        }
      }
      out += mapped;
    }
    return { text: out, complete: complete };
  }

  function arabicConsonant(ch) {
    var map = {
      "b": "ب", "p": "ب", "t": "ت", "d": "د",
      "j": "ج", "h": "ه", "k": "ك", "l": "ل", "m": "م",
      "n": "ن", "s": "س", "z": "ز", "r": "ر",
      "f": "ف", "v": "ف", "w": "و", "y": "ي", "g": "غ", "q": "ق"
    };
    return map[ch] || null;
  }

  function arabicVowel(ch) {
    var map = { "a": "َ", "e": "َ", "i": "ِ", "o": "ُ", "u": "ُ" };
    return map[ch] || null;
  }

  function arabicLongVowel(ch) {
    var map = { "a": "َا", "e": "َا", "i": "ِي", "o": "ُو", "u": "ُو" };
    return map[ch] || ch;
  }

  /* ------------------------------------------------------------------
     GREEK
     Full alphabet with diacritics. Modern Greek orthography.
     ------------------------------------------------------------------ */
  function greekEngine(word) {
    var w = word;
    var out = "";
    var complete = true;
    var i = 0;
    while (i < w.length) {
      var ch = w[i];
      var next = w[i + 1] || "";
      var mapped = "";
      if (ch === "ch") { mapped = "χ"; i += 2; }
      else if (ch === "th") { mapped = "θ"; i += 2; }
      else if (ch === "ph") { mapped = "φ"; i += 2; }
      else if (ch === "kh") { mapped = "χ"; i += 2; }
      else if (ch === "ps") { mapped = "ψ"; i += 2; }
      else {
        var c = greekConsonant(ch);
        if (c) {
          mapped = c;
          if (VOWELS[next]) {
            var v = greekVowel(next);
            if (v) { mapped += v; i += 2; }
            else { i += 1; }
          } else {
            i += 1;
          }
        } else if (VOWELS[ch]) {
          mapped = greekVowel(ch);
          i += 1;
        } else {
          complete = false;
          mapped = ch;
          i += 1;
        }
      }
      out += mapped;
    }
    return { text: out, complete: complete };
  }

  function greekConsonant(ch) {
    var map = {
      "b": "β", "p": "π", "t": "τ", "d": "δ",
      "g": "γ", "k": "κ", "l": "λ", "m": "μ", "n": "ν",
      "s": "σ", "z": "ζ", "r": "ρ", "h": "η", "f": "φ",
      "v": "β", "j": "γ", "w": "ω", "y": "υ"
    };
    return map[ch] || null;
  }

  function greekVowel(ch) {
    var map = { "a": "α", "e": "ε", "i": "ι", "o": "ο", "u": "υ" };
    return map[ch] || null;
  }

  /* ------------------------------------------------------------------
     CYRILLIC (covers Russian, Ukrainian, Kazakh)
     Each language has slight differences in a few letters, but the
     core mapping is shared. The caller passes a variant.
     ------------------------------------------------------------------ */
  function cyrillicEngine(word, variant) {
    var w = word;
    var out = "";
    var complete = true;
    var i = 0;
    while (i < w.length) {
      var ch = w[i];
      var next = w[i + 1] || "";
      var mapped = "";
      if (ch === "ch") { mapped = "ч"; i += 2; }
      else if (ch === "sh") { mapped = "ш"; i += 2; }
      else if (ch === "sch") { mapped = "щ"; i += 3; }
      else if (ch === "yu") { mapped = "ю"; i += 2; }
      else if (ch === "ya") { mapped = "я"; i += 2; }
      else if (ch === "ye") { mapped = "е"; i += 2; }
      else if (ch === "yo") { mapped = "ё"; i += 2; }
      else if (ch === "y") { mapped = "й"; i += 1; }
      else {
        var c = cyrillicConsonant(ch, variant);
        if (c) {
          mapped = c;
          if (VOWELS[next]) {
            var v = cyrillicVowel(next, variant);
            if (v) { mapped += v; i += 2; }
            else { i += 1; }
          } else {
            i += 1;
          }
        } else if (VOWELS[ch]) {
          mapped = cyrillicVowel(ch, variant);
          i += 1;
        } else {
          complete = false;
          mapped = ch;
          i += 1;
        }
      }
      out += mapped;
    }
    return { text: out, complete: complete };
  }

  function cyrillicConsonant(ch, variant) {
    var map = {
      "b": "б", "p": "п", "t": "т", "d": "д",
      "g": "г", "k": "к", "l": "л", "m": "м", "n": "н",
      "s": "с", "z": "з", "r": "р", "f": "ф", "v": "в",
      "c": "ц", "h": "х", "w": "в", "j": "й"
    };
    return map[ch] || null;
  }

  function cyrillicVowel(ch, variant) {
    var map = { "a": "а", "e": "е", "i": "и", "o": "о", "u": "у" };
    return map[ch] || null;
  }

  /* ------------------------------------------------------------------
     HANGUL (Korean)
     Syllabic blocks: each block = initial consonant + vowel +
     optional final consonant. The Unicode formula is:
       block = 0xAC00 + ((L - 0x1100) * 21 * 28) + ((V - 0x1161) * 28) + (T - 0x11A7)
     ------------------------------------------------------------------ */
  function hangulEngine(word) {
    var w = word;
    var out = "";
    var complete = true;
    var i = 0;
    while (i < w.length) {
      var ch = w[i];
      var next = w[i + 1] || "";
      var next2 = w[i + 2] || "";
      var cons = hangulConsonant(ch);
      if (cons) {
        if (VOWELS[next]) {
          var vow = hangulVowel(next);
          if (vow) {
            var fin = null;
            if (next2 && VOWELS[next2] === undefined && hangulConsonant(next2)) {
              fin = hangulFinal(next2);
            }
            out += hangulBlock(cons, vow, fin);
            i += (fin ? 3 : 2);
            continue;
          }
        }
        // Consonant without a following vowel — use ㅏ as filler
        // so the block is valid. Mark complete=false.
        out += hangulBlock(cons, 0x1161, null);
        complete = false;
        i += 1;
        continue;
      }
      // Standalone vowel
      var v = hangulVowel(ch);
      if (v) {
        out += hangulBlock(0x1100, v, null);
        i += 1;
        continue;
      }
      complete = false;
      out += ch;
      i += 1;
    }
    return { text: out, complete: complete };
  }

  /* Hangul Jamo lead consonants (U+1100..U+1112) */
  function hangulConsonant(ch) {
    var map = {
      "b": 0x1107, "p": 0x1108, "t": 0x1103, "d": 0x1103,
      "g": 0x1100, "k": 0x1100, "kh": 0x1111, "l": 0x1105,
      "m": 0x1106, "n": 0x1102, "s": 0x1109, "z": 0x1109,
      "r": 0x1105, "j": 0x110c, "ch": 0x110e, "sh": 0x110e,
      "h": 0x1112, "f": 0x1108, "v": 0x1107, "c": 0x110e,
      "w": 0x1107, "y": 0x110b
    };
    return map[ch] || null;
  }

  /* Hangul Jamo vowels (U+1161..U+1175) */
  function hangulVowel(ch) {
    var map = {
      "a": 0x1161, "e": 0x1165, "i": 0x1175, "o": 0x1169, "u": 0x116e,
      "ae": 0x1162, "eo": 0x1167, "eu": 0x1173, "ui": 0x1174,
      "y": 0x1175, "ye": 0x1166, "yo": 0x116d, "yu": 0x1172
    };
    return map[ch] || null;
  }

  /* Hangul Jamo tail consonants (U+11A7..U+11C2) */
  function hangulFinal(ch) {
    var map = {
      "k": 0x11a7, "g": 0x11a7, "t": 0x11ad, "d": 0x11ad, "l": 0x11ae,
      "m": 0x11b6, "n": 0x11ab, "ng": 0x11ab, "p": 0x11c0, "b": 0x11c0,
      "s": 0x11b9, "j": 0x11bc, "ch": 0x11bd, "sh": 0x11bd
    };
    return map[ch] || null;
  }

  function hangulBlock(cons, vow, fin) {
    var L = cons - 0x1100;
    var V = vow - 0x1161;
    var T = fin ? (fin - 0x11a7) : 0;
    var block = 0xac00 + (L * 21 * 28) + (V * 28) + T;
    return String.fromCodePoint(block);
  }

  /* ------------------------------------------------------------------
     KANA (Japanese)
     Hiragana for native words. Each syllable = one kana.
     ------------------------------------------------------------------ */
  function kanaEngine(word) {
    var w = word;
    var out = "";
    var complete = true;
    var i = 0;
    while (i < w.length) {
      var ch = w[i];
      var next = w[i + 1] || "";
      var mapped = "";
      if (ch === "ch") { mapped = "\u3061"; i += 2; }
      else if (ch === "sh") { mapped = "\u305b"; i += 2; }
      else if (ch === "ts") { mapped = "\u3064"; i += 2; }
      else if (ch === "ty") { mapped = "\u3058"; i += 2; }
      else if (ch === "dy") { mapped = "\u3065"; i += 2; }
      else if (ch === "gy") { mapped = "\u304e"; i += 2; }
      else if (ch === "ky") { mapped = "\u304d"; i += 2; }
      else if (ch === "py") { mapped = "\u3073"; i += 2; }
      else if (ch === "by") { mapped = "\u3070"; i += 2; }
      else if (ch === "my") { mapped = "\u307f"; i += 2; }
      else if (ch === "ry") { mapped = "\u3089"; i += 2; }
      else if (ch === "hy") { mapped = "\u308f"; i += 2; }
      else if (ch === "j") { mapped = "\u3058"; i += 1; }
      else if (ch === "w") { mapped = "\u308f"; i += 1; }
      else {
        var cons = kanaConsonant(ch);
        if (cons && next) {
          var vow = kanaVowel(next);
          if (vow) {
            mapped = kanaChar(cons + vow);
            i += 2;
          } else {
            mapped = kanaChar(cons + "a"); // fallback vowel 'a'
            complete = false;
            i += 1;
          }
        } else if (cons) {
          // Consonant at end of word with no following vowel
          mapped = kanaChar(cons + "a");
          complete = false;
          i += 1;
        } else if (VOWELS[ch]) {
          var v = kanaVowel(ch);
          if (v) {
            mapped = kanaChar(v);
            i += 1;
          } else {
            complete = false;
            mapped = ch;
            i += 1;
          }
        } else {
          complete = false;
          mapped = ch;
          i += 1;
        }
      }
      out += mapped;
    }
    return { text: out, complete: complete };
  }

  /* KANA lookup table: maps (consonant+vowel) string keys to hiragana. */
  var KANA_TABLE = {
    "ka": "\u304b", "ki": "\u304d", "ku": "\u304f", "ke": "\u3051", "ko": "\u3053",
    "ga": "\u304c", "gi": "\u304e", "gu": "\u3050", "ge": "\u3052", "go": "\u3054",
    "sa": "\u3055", "si": "\u3057", "su": "\u3059", "se": "\u305b", "so": "\u305d",
    "za": "\u3056", "zi": "\u3058", "zu": "\u305a", "ze": "\u305c", "zo": "\u305e",
    "ta": "\u3058", "ti": "\u3061", "tu": "\u3064", "te": "\u3066", "to": "\u3068",
    "da": "\u3060", "di": "\u3061", "du": "\u3065", "de": "\u3067", "do": "\u3069",
    "na": "\u306a", "ni": "\u306b", "nu": "\u306c", "ne": "\u306d", "no": "\u306e",
    "ha": "\u306f", "hi": "\u3072", "hu": "\u3075", "he": "\u3078", "ho": "\u307b",
    "ba": "\u3070", "bi": "\u3073", "bu": "\u3074", "be": "\u3076", "bo": "\u307b",
    "pa": "\u3071", "pi": "\u3074", "pu": "\u3077", "pe": "\u307a", "po": "\u307d",
    "ma": "\u307f", "mi": "\u3080", "mu": "\u3081", "me": "\u3082", "mo": "\u3083",
    "ya": "\u3084", "yi": "\u3084", "yu": "\u3085", "ye": "\u3084", "yo": "\u3086",
    "ra": "\u3089", "ri": "\u308a", "ru": "\u308b", "re": "\u308c", "ro": "\u308d",
    "wa": "\u308f", "wi": "\u308f", "wu": "\u308f", "we": "\u308f", "wo": "\u3092",
    "a": "\u3042", "i": "\u3044", "u": "\u3046", "e": "\u3048", "o": "\u304a"
  };

  function kanaConsonant(ch) {
    var map = {
      "k": "k", "g": "g", "s": "s", "z": "z", "t": "t", "d": "d",
      "n": "n", "h": "h", "b": "b", "p": "p", "m": "m", "y": "y",
      "r": "r", "w": "w", "j": "z"
    };
    return map[ch] || null;
  }

  function kanaVowel(ch) {
    return ch; // vowel character maps directly
  }

  function kanaChar(key) {
    return KANA_TABLE[key] || "\u3042";
  }


  /* ------------------------------------------------------------------
     ETHIOPIC (Amharic)
     An abugida: consonant-vowel units. Each syllable is a glyph.
     ------------------------------------------------------------------ */
  function ethiopicEngine(word) {
    var w = word;
    var out = "";
    var complete = true;
    var i = 0;
    while (i < w.length) {
      var ch = w[i];
      var next = w[i + 1] || "";
      var mapped = "";
      var cons = ethiopicConsonant(ch);
      if (cons && next) {
        var vow = ethiopicVowel(next);
        if (vow) {
          mapped = String.fromCodePoint(cons) + vow;
          i += 2;
        } else {
          mapped = String.fromCodePoint(cons);
          i += 1;
        }
      } else if (cons) {
        mapped = String.fromCodePoint(cons);
        i += 1;
      } else if (VOWELS[ch]) {
        // Standalone vowel — use the default vowel mark for 'a'
        mapped = "\u1220\u1240"; // consonant 'b' with 'a' vowel
        complete = false;
        i += 1;
      } else {
        complete = false;
        mapped = ch;
        i += 1;
      }
      out += mapped;
    }
    return { text: out, complete: complete };
  }

  function ethiopicConsonant(ch) {
    var map = {
      "b": 0x1220, "p": 0x1221, "t": 0x1222, "s": 0x1223,
      "k": 0x1224, "w": 0x1225, "z": 0x1226, "h": 0x1227,
      "m": 0x1228, "n": 0x1229, "l": 0x122a, "r": 0x122b,
      "y": 0x122c, "f": 0x122e, "v": 0x122e,
      "g": 0x1233, "j": 0x1234, "d": 0x1235, "ch": 0x1236,
      "x": 0x1237, "q": 0x1238, "c": 0x1239
    };
    return map[ch] || null;
  }

  function ethiopicVowel(ch) {
    var map = {
      "a": "\u1240", "u": "\u1241", "i": "\u1242", "e": "\u1243",
      "o": "\u1244"
    };
    return map[ch] || null;
  }

  /* ------------------------------------------------------------------
     Public API: same interface as EkGuruScriptMap.fromEnglish
     ------------------------------------------------------------------ */
  function fromEnglish(text, script, variant) {
    var engine = root.EkGuruTranslit;
    var devanagari = "";
    if (engine) {
      try { devanagari = engine.transliterate(text).text; } catch (e) {}
    }
    var w = preprocess(text.toLowerCase());
    var r;
    switch (script) {
      case "arabic": r = arabicEngine(w); break;
      case "greek": r = greekEngine(w); break;
      case "cyrillic": r = cyrillicEngine(w, variant || "ru"); break;
      case "hangul": r = hangulEngine(w); break;
      case "kana": r = kanaEngine(w); break;
      case "ethiopic": r = ethiopicEngine(w); break;
      default: r = { text: text, complete: false };
    }
    return {
      input: text,
      devanagari: devanagari,
      text: r.text,
      script: script,
      complete: r.complete
    };
  }

  var NAMES = {
    arabic: { en: "Arabic", native: "العربية" },
    greek: { en: "Greek", native: "Ελληνικά" },
    cyrillic: { en: "Cyrillic", native: "Кириллица" },
    hangul: { en: "Korean (Hangul)", native: "한글" },
    kana: { en: "Japanese (Kana)", native: "かな" },
    ethiopic: { en: "Amharic (Ethiopic)", native: "አማርኛ" }
  };

  var API = {
    fromEnglish: fromEnglish,
    scripts: Object.keys(NAMES),
    names: NAMES,
    _preprocess: preprocess
  };

  root.EkGuruNonIndic = API;
})(typeof window !== "undefined" ? window : globalThis);
