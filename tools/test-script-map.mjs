/* Correctness tests for the script conversion and the name list.

   Why a test and not just "it looked right": a wrong codepoint in a
   script map produces an invisible box or a letter that reads as a
   different name, and neither is visible in a screenshot review. The
   only way to know is to assert the exact string.

   Run: node tools/test-script-map.mjs
*/
import fs from "node:fs";
import assert from "node:assert/strict";

globalThis.window = globalThis;
new Function(fs.readFileSync(new URL("../js/translit.js", import.meta.url), "utf8"))();
new Function(fs.readFileSync(new URL("../js/script-map.js", import.meta.url), "utf8"))();

const { EkGuruScriptMap: M, EkGuruTranslit: T } = globalThis;
const NFC = (s) => s.normalize("NFC");

let pass = 0;
const fails = [];
function ok(name, actual, expected) {
  if (NFC(actual) === NFC(expected)) { pass++; return; }
  fails.push(`${name}: got ${JSON.stringify(actual)} (${[...actual].map(c => "U+" + c.codePointAt(0).toString(16)).join(" ")}) want ${JSON.stringify(expected)}`);
}

/* ---------------------------------------------------------------
   1. Curated spellings must survive the round trip.
   The name list is the answer for common names, so every entry has
   to be internally consistent: right script, right length, and no
   Devanagari leaking into a Gurmukhi field.
   --------------------------------------------------------------- */
const list = JSON.parse(fs.readFileSync(new URL("../data/names/names.json", import.meta.url), "utf8")).names;
assert.ok(list.length >= 100, "the curated list should cover at least 100 names");

/* ---------------------------------------------------------------
   Locale contract.
   ---------------------------------------------------------------
   `pa` and `hi` are OPTIONAL, and that is by design, not an oversight.
   tools/build-names-js.py copies a locale only `if n.get(k)`, and the JSON
   documents itself as "the forms these names are actually written in, in
   each script". A name with no Punjabi attestation (Ivan, George, Kenji,
   James, Paul, Mary) has ru/el/am/ar/ko/ja only. Writing a mechanical
   Gurmukhi spelling for it would be inventing a transliteration, which is
   exactly what the note above forbids.

   So every check below runs on the values that EXIST and is silent about
   the ones that do not. A present-but-wrong value is still a hard failure.
   --------------------------------------------------------------- */
const LOCALE_SCRIPTS = {
  pa: { label: "Gurmukhi",   lo: 0x0a00, hi: 0x0a7f },
  hi: { label: "Devanagari", lo: 0x0900, hi: 0x097f },
  ar: { label: "Arabic",     lo: 0x0600, hi: 0x06ff },
  el: { label: "Greek",      lo: 0x0370, hi: 0x03ff },
  ru: { label: "Cyrillic",   lo: 0x0400, hi: 0x04ff },
  ko: { label: "Hangul",     lo: 0xac00, hi: 0xd7a3 },
  ja: { label: "Japanese",   lo: 0x3040, hi: 0x30ff },
  am: { label: "Ethiopic",   lo: 0x1200, hi: 0x137f }
};

const has = (v) => typeof v === "string" && v.trim() !== "";

for (const n of list) {
  assert.ok(has(n.name), `an entry has no name: ${JSON.stringify(n)}`);

  for (const [key, spec] of Object.entries(LOCALE_SCRIPTS)) {
    const v = n[key];
    if (v === undefined) continue;      /* optional: absent is valid */
    assert.equal(typeof v, "string",
      `${n.name}: ${key} must be a string when present, got ${Array.isArray(v) ? "array" : typeof v}`);
    if (!has(v)) continue;              /* explicitly empty: no glyphs to check */
    for (const ch of v) {
      const cp = ch.codePointAt(0);
      assert.ok(cp >= spec.lo && cp <= spec.hi,
        `${n.name}: ${ch} (U+${cp.toString(16)}) in ${key} is not ${spec.label}`);
    }
    assert.equal(v.normalize("NFC"), v, `${n.name}: ${key} should be NFC`);
  }

  /* `also` is a list of alternative accepted spellings, all in the same
     script as `pa` — the field it annotates. */
  if (n.also !== undefined) {
    assert.ok(Array.isArray(n.also), `${n.name}: also must be an array`);
    for (const alt of n.also) {
      assert.ok(has(alt), `${n.name}: also contains an empty spelling`);
      for (const ch of alt) {
        const cp = ch.codePointAt(0);
        assert.ok(cp >= 0x0a00 && cp <= 0x0a7f, `${n.name}: ${ch} in also is not Gurmukhi`);
      }
    }
  }
}

/* Coverage floor, not a per-name demand: the list is meant to be mostly
   Punjabi, and a silent regression to 6 entries must not pass. */
const paCount = list.filter((n) => has(n.pa)).length;
assert.ok(paCount >= 100, `only ${paCount} of ${list.length} names have a Punjabi spelling`);
pass++;
ok("Singh is ਸਿੰਘ, not a mechanical ਸਿਂਹ", list.find(n => n.name === "Singh").pa, "ਸਿੰਘ");
ok("Amrit keeps the ri", list.find(n => n.name === "Amrit").pa, "ਅੰਮ੍ਰਿਤ");
ok("Arshdeep avoids the stack", list.find(n => n.name === "Arshdeep").pa, "ਅਰਸ਼ਦੀਪ");
ok("Kaur", list.find(n => n.name === "Kaur").pa, "ਕੌਰ");

/* ---------------------------------------------------------------
   2. The conversion itself, on Devanagari input.
   These are the cases where a blind codepoint offset is wrong:
   anusvara position, reph, vocalic r, and nukta letters.
   --------------------------------------------------------------- */
const G = [
  ["प्रिया", "ਪ੍ਰਿਯਾ"],
  ["राहुल", "ਰਾਹੁਲ"],
  ["सिमरन", "ਸਿਮਰਨ"],
  ["गुरप्रीत", "ਗੁਰਪ੍ਰੀਤ"],
  ["अमृत", "ਅਮ੍ਰਿਤ"],          // ृ → ੍ਰਿ
  ["हरप्रीत", "ਹਰਪ੍ਰੀਤ"],
  ["नवजोत", "ਨਵਜੋਤ"],
  ["कौर", "ਕੌਰ"],
  ["सिंह", "ਸਿੰਹ"],             // tippi before a consonant
  ["मनप्रीत", "ਮਨਪ੍ਰੀਤ"],
  ["अमन", "ਅਮਨ"],
  ["दीपक", "ਦੀਪਕ"],
  ["सुखदीप", "ਸੁਖਦੀਪ"],         // the cluster loses its halant
  ["अर्शदीप", "ਅਰਸ਼ਦੀਪ"],       // reph becomes a full ਰ
  ["जसमीत", "ਜਸਮੀਤ"],
  ["एकम", "ਏਕਮ"],
  ["जॉन", "ਜੌਨ"],               // ॉ → ੌ
  ["लवप्रीत", "ਲਵਪ੍ਰੀਤ"]
];
for (const [dev, want] of G) ok(`devanagari→gurmukhi ${dev}`, M.fromDevanagari(dev, "gurmukhi").text, want);

/* bindi at word end stays bindi */
ok("final nasal stays bindi", M.fromDevanagari("मैं", "gurmukhi").text, "ਮੈਂ");

/* nukta letters must not become unassigned codepoints */
for (const [dev] of [["ज़"], ["फ़"], ["ख़"], ["ग़"], ["ड़"], ["क़"]]) {
  const out = M.fromDevanagari(dev, "gurmukhi").text;
  for (const ch of out) {
    const cp = ch.codePointAt(0);
    assert.ok(cp >= 0x0a00 && cp <= 0x0a7f, `${dev} produced ${ch} (U+${cp.toString(16)}), outside Gurmukhi`);
  }
}
pass++;

/* ---------------------------------------------------------------
   3. No script may emit an unassigned codepoint.
   This is the failure mode that shows as a hollow box, and it is
   invisible to every other kind of review.
   --------------------------------------------------------------- */
const SAMPLE = ["प्रिया", "राहुल", "सिंह", "अमृत", "ज़फ़", "गुरप्रीत", "श्री", "क्षत्रिय", "ॐ", "अर्जुन"];
for (const script of M.scripts) {
  for (const dev of SAMPLE) {
    const out = M.fromDevanagari(dev, script);
    assert.equal(typeof out.text, "string");
    assert.ok(out.text.length > 0, `${script}: ${dev} produced nothing`);
    /* A conversion that could not place a letter says so rather than
       pretending, so `complete` must agree with the output. */
    if (!out.complete) {
      assert.ok(/[\u0900-\u097f]/.test(out.text), `${script}: ${dev} marked incomplete but kept no Devanagari`);
    }
  }
  pass++;
}

/* ---------------------------------------------------------------
   4. The English → script path, end to end.
   --------------------------------------------------------------- */
ok("John", M.fromEnglish("John", "gurmukhi").text, "ਜੌਨ");
ok("Sarah", M.fromEnglish("Sarah", "gurmukhi").text, "ਸਾਰਾ");
ok("empty input is empty, not a crash", M.fromEnglish("", "gurmukhi").text, "");

/* Latin text is passed through, never mangled */
ok("latin passes through", M.fromDevanagari("abc", "gurmukhi").text, "abc");

/* Every advertised script has a name card */
for (const s of M.scripts) {
  assert.ok(M.names[s] && M.names[s].en, `script ${s} has no display name`);
}
pass++;

/* ---------------------------------------------------------------
   5. The page itself: the tool, the license to index, and the
   curated table must all agree with the JSON.
   --------------------------------------------------------------- */
const page = fs.readFileSync(new URL("../name-in-punjabi/index.html", import.meta.url), "utf8");
assert.match(page, /data-script="gurmukhi"/, "the tool input must declare its script");
assert.match(page, /rel="canonical"\/>/, "canonical missing");
assert.match(page, /href="https:\/\/ekguru\.shop\/name-in-punjabi\/" rel="canonical"/, "canonical must be self");
assert.match(page, /content="index, follow/, "page is approved for indexing, so it must say index");
assert.match(page, /js\/script-map\.js/, "page must load the script map");
assert.match(page, /js\/name-in-script\.js/, "page must load the controller");
/* Only names WITH a Punjabi spelling can be required in the Punjabi table.
   `page.includes(undefined)` would coerce to the literal string "undefined"
   and pass vacuously, so the value is checked before the lookup. */
for (const n of list) {
  if (!has(n.pa)) continue;
  assert.ok(page.includes(n.pa), `curated table is missing ${n.name} (${n.pa})`);
}
pass++;

/* ---------------------------------------------------------------
   6. Locale contract regressions.
   The checks above run against live data, so they only exercise the
   optional-locale paths that today's file happens to contain. These
   cases pin the CONTRACT itself: absent, empty, malformed, valid.
   Without them the guard could be deleted and every test would still
   pass on a file where nobody ever omitted `pa`.
   --------------------------------------------------------------- */
{
  /* The same validator the loop above uses, extracted so it can be
     pointed at synthetic entries. */
  function validateEntry(n) {
    const errs = [];
    if (!has(n.name)) errs.push("no name");
    for (const [key, spec] of Object.entries(LOCALE_SCRIPTS)) {
      const v = n[key];
      if (v === undefined) continue;
      if (typeof v !== "string") { errs.push(`${key} not a string`); continue; }
      if (!has(v)) continue;
      for (const ch of v) {
        const cp = ch.codePointAt(0);
        if (cp < spec.lo || cp > spec.hi) errs.push(`${key}: ${ch} not ${spec.label}`);
      }
      if (v.normalize("NFC") !== v) errs.push(`${key} not NFC`);
    }
    return errs;
  }

  const cases = [
    /* name,                              entry,                                              expectErrors */
    ["MISSING pa is accepted",            { name: "Ivan", ru: "Иван", ja: "イヴァン" },       false],
    ["MISSING hi is accepted",            { name: "Ivan", pa: "ਇਵਾਨ", ru: "Иван" },          false],
    ["MISSING every locale is accepted",  { name: "Ivan" },                                  false],
    ["EMPTY pa is accepted, not crashed", { name: "Ivan", pa: "" },                          false],
    ["EMPTY hi is accepted",              { name: "Ivan", hi: "" },                          false],
    ["VALID pa is accepted",              { name: "Priya", pa: "ਪ੍ਰਿਯਾ" },                    false],
    ["VALID pa + also is accepted",       { name: "Amrit", pa: "ਅੰਮ੍ਰਿਤ", also: ["ਅੰਮ੍ਰਿਤ"] }, false],
    ["MALFORMED pa: Devanagari in pa",    { name: "Priya", pa: "प्रिया" },                   true],
    ["MALFORMED pa: latin in pa",         { name: "Priya", pa: "Priya" },                    true],
    ["MALFORMED hi: Gurmukhi in hi",      { name: "Priya", hi: "ਪ੍ਰਿਯਾ" },                    true],
    ["MALFORMED pa: array instead of str",{ name: "Priya", pa: ["ਪ੍ਰਿਯਾ"] },                  true],
    ["MALFORMED pa: number instead of str",{ name: "Priya", pa: 42 },                        true],
    /* Gurmukhi and Devanagari nukta letters are composition-excluded, so
       NFC leaves them alone and neither can produce a non-NFC string.
       Hangul can: decomposed Jamo U+110B U+1175 recompose to U+C774, which
       is how a mis-generated Korean field would arrive. */
    ["MALFORMED ko: non-NFC (decomposed Jamo)", { name: "Ivan", ko: "이반" }, true],
    ["MALFORMED ru: latin in ru",         { name: "Ivan", ru: "Ivan" },                      true],
    ["MALFORMED ko: arabic in ko",        { name: "Ivan", ko: "إيفان" },                     true],
    ["MALFORMED: no name at all",         { pa: "ਪ੍ਰਿਯਾ" },                                   true]
  ];

  for (const [label, entry, shouldFail] of cases) {
    const errs = validateEntry(entry);
    const failed = errs.length > 0;
    if (failed === shouldFail) { pass++; continue; }
    fails.push(`${label}: expected ${shouldFail ? "rejection" : "acceptance"}, got ${failed ? "rejection (" + errs[0] + ")" : "acceptance"}`);
  }

  /* The page-table guard must skip entries with no `pa` rather than
     search for the string "undefined". */
  const pageHas = (pg, v) => has(v) && pg.includes(v);
  if (!pageHas("<p>ਸਿੰਘ</p>", undefined)) pass++;
  else fails.push("page-table guard: undefined pa must never count as present");
  if (!pageHas("<p>undefined</p>", undefined)) pass++;
  else fails.push("page-table guard: undefined pa must not match the literal string 'undefined'");
  if (pageHas("<p>ਸਿੰਘ</p>", "ਸਿੰਘ")) pass++;
  else fails.push("page-table guard: a real pa value must be found in the page");
  if (!pageHas("<p>undefined</p>", "")) pass++;
  else fails.push("page-table guard: empty pa must never count as present");
}

const baseline = JSON.parse(fs.readFileSync(new URL("../data/quality/indexing-baseline.json", import.meta.url), "utf8"));
assert.ok(baseline.owner_approved_new_indexable?.["name-in-punjabi/index.html"],
  "a new indexable page must be in the owner-approved list");
pass++;

console.log(`${pass} passed, ${fails.length} failed`);
for (const f of fails) console.log("  FAIL " + f);
process.exit(fails.length ? 1 : 0);
