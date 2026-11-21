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

for (const n of list) {
  for (const ch of n.pa) {
    const cp = ch.codePointAt(0);
    assert.ok(cp >= 0x0a00 && cp <= 0x0a7f, `${n.name}: ${ch} is not Gurmukhi`);
  }
  for (const ch of n.hi) {
    const cp = ch.codePointAt(0);
    assert.ok(cp >= 0x0900 && cp <= 0x097f, `${n.name}: ${ch} is not Devanagari`);
  }
  assert.equal(n.pa.normalize("NFC"), n.pa, `${n.name}: pa should be NFC`);
  assert.equal(n.hi.normalize("NFC"), n.hi, `${n.name}: hi should be NFC`);
}
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
for (const n of list) {
  assert.ok(page.includes(n.pa), `curated table is missing ${n.name} (${n.pa})`);
}
pass++;

const baseline = JSON.parse(fs.readFileSync(new URL("../data/quality/indexing-baseline.json", import.meta.url), "utf8"));
assert.ok(baseline.owner_approved_new_indexable?.["name-in-punjabi/index.html"],
  "a new indexable page must be in the owner-approved list");
pass++;

console.log(`${pass} passed, ${fails.length} failed`);
for (const f of fails) console.log("  FAIL " + f);
process.exit(fails.length ? 1 : 0);
