/* Time-and-days page: does the data, the generated JS and the visible table
   all tell one story, and does the tool return the right word?

   The tool's whole job is: visitor types an ENGLISH word, gets the target
   language's own script and real usage back. Three things can silently
   disagree here (the JSON, the generated JS, the visible table) and any two
   drifting means the page contradicts itself. So: assert all three, per
   language, and actually type into the real page.

   Run: node tests/regression/test-time-page.mjs
*/
import { JSDOM } from "jsdom";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("../..", import.meta.url).pathname);
const PAGE_SPECS = [
  { slug: "days-and-months-in-punjabi", file: "data/time/punjabi.json", lang: "pa",
    samples: [["Tuesday", "ਮੰਗਲਵਾਰ"], ["March", "ਮਾરਚ"], ["morning", "ਸਵੇਰ"],
              ["Saturday", "ਸ਼ਨਿੱਚਰਵਾਰ"], ["today", "ਅੱਜ"]] },
  { slug: "days-and-months-in-marathi", file: "data/time/marathi.json", lang: "mr",
    samples: [["Tuesday", "मंगळवार"], ["March", "मार्च"], ["morning", "सकाळ"],
              ["Saturday", "शनिवार"], ["today", "आज"]] },
  { slug: "days-and-months-in-gujarati", file: "data/time/gujarati.json", lang: "gu",
    samples: [["Tuesday", "મંગળવાર"], ["March", "માર્ચ"], ["morning", "સવાર"],
              ["Saturday", "શનિવાર"], ["today", "આજ"]] },
  { slug: "days-and-months-in-kannada", file: "data/time/kannada.json", lang: "kn",
    samples: [["Tuesday", "ಮಂಗಳವಾರ"], ["March", "ಮಾರ್ಚ್"], ["morning", "ಬೆಳಿಗ್ಗೆ"],
              ["Saturday", "ಶನಿವಾರ"], ["today", "ಇಂದು"]] },
  { slug: "days-and-months-in-telugu", file: "data/time/telugu.json", lang: "te",
    samples: [["Tuesday", "మంగళవారం"], ["March", "మార్చి"], ["morning", "ఉదయం"],
              ["Saturday", "శనివారం"], ["today", "నేడు"]] },
  { slug: "days-and-months-in-urdu", file: "data/time/urdu.json", lang: "ur",
    samples: [["Tuesday", "منگل"], ["March", "مارچ"], ["morning", "صبح"],
              ["Saturday", "ہفتہ"], ["today", "آج"]] },
];

/* The six scripts these pages use: Gurmukhi, Devanagari, Gujarati, Kannada,
   Telugu, and Perso-Arabic (Urdu). A word may contain a space when it is a
   multi-word phrase (e.g. Gujarati આવતી કાલ). */
const SCRIPTS = [
  [0x0a00, 0x0a7f], // Gurmukhi
  [0x0900, 0x097f], // Devanagari
  [0x0a80, 0x0aff], // Gujarati
  [0x0c80, 0x0cff], // Kannada
  [0x0c00, 0x0c7f], // Telugu
  [0x0600, 0x06ff], // Perso-Arabic
];
const inAnyScript = (cp) => SCRIPTS.some(([lo, hi]) => cp >= lo && cp <= hi);

const fails = [];
let pass = 0;
const ok = (cond, msg) => { if (cond) pass++; else fails.push(msg); };

/* gather every entry the tool must be able to answer, from the data */
function allEntries(d) {
  return [...d.days, ...d.months, ...d.desi_months, ...d.time_words];
}

for (const { slug, file, lang, samples } of PAGE_SPECS) {
  const data = JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
  ok(data.language === lang, `${slug}: data language must be ${lang}`);

  /* every word is in one of the known scripts (space allowed in multi-word phrases) */
  for (const e of allEntries(data)) {
    for (const ch of e.word) {
      const cp = ch.codePointAt(0);
      ok(cp === 0x20 || inAnyScript(cp),
         `${slug}: "${e.word}" (${e.en}) has a character outside a known script`);
    }
    ok(!!e.en, `${slug}: every entry needs an English key`);
  }
  /* some languages share one word for tomorrow/yesterday or after/before;
     that is intentional, not a bug. Just confirm the four entries exist. */
  const tw = Object.fromEntries(data.time_words.map((e) => [e.en, e.word]));
  for (const k of ["Tomorrow", "Yesterday", "Day after tomorrow", "Day before yesterday"]) {
    ok(k in tw, `${slug}: the time word "${k}" should be present`);
  }
  /* helper: expected word straight from the data, case-insensitive like the tool */
  const expect = (en) => {
    const e = allEntries(data).find((x) => x.en.toLowerCase() === en.toLowerCase());
    return e?.word;
  };

  const page = fs.readFileSync(path.join(root, `${slug}/index.html`), "utf8");
  const dom = new JSDOM(page, {
    url: `https://ekguru.shop/${slug}/`,
    runScripts: "outside-only",
    pretendToBeVisual: true
  });
  const { window } = dom;
  for (const f of ["js/time-data.js", "js/time-tool.js"]) {
    window.eval(fs.readFileSync(path.join(root, f), "utf8"));
  }
  const lib = window.EkGuruTime && window.EkGuruTime.langs[lang];
  ok(!!lib, `${slug}: js/time-data.js did not define EkGuruTime.langs.${lang}`);

  /* ---- the visible tables agree with the data ---- */
  for (const e of allEntries(data)) {
    ok(page.includes(`>${e.word}<`), `${slug}: the table is missing "${e.word}" (${e.en})`);
    ok(page.includes(`>${e.en}<`), `${slug}: the table is missing the English row ${e.en}`);
  }
  ok((page.match(/<tr><td class="en">/g) || []).length >= 7 + 12 + 15,
     `${slug}: should have at least the days+months+time tables`);

  /* ---- page honesty ---- */
  ok(page.includes(`href="https://ekguru.shop/${slug}/" rel="canonical"`), `${slug}: canonical must be self`);
  ok(/content="index, follow/.test(page), `${slug}: approved for indexing, must say index`);
  ok(page.includes("time-data.js") && page.includes("time-tool.js"), `${slug}: must load the time modules`);

  const baseline = JSON.parse(fs.readFileSync(path.join(root, "data/quality/indexing-baseline.json"), "utf8"));
  ok(!!baseline.owner_approved_new_indexable?.[`${slug}/index.html`],
     `${slug}: a new indexable page must be in the owner-approved list`);

  /* ---- the tool actually answers from English ---- */
  const input = window.document.getElementById("tIn");
  const out = window.document.getElementById("tOut");
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  await wait(30);

  async function type(value) {
    input.value = value;
    input.dispatchEvent(new window.Event("input"));
    await wait(140);
    return {
      big: out.querySelector(".big")?.textContent ?? "",
      rom: out.querySelector(".rom")?.textContent ?? ""
    };
  }

  for (const [value] of samples) {
    const r = await type(value);
    const want = expect(value);
    ok(r.big === want, `${slug}: typing "${value}" should give ${want}, got ${JSON.stringify(r.big)}`);
    ok(r.rom.toLowerCase().includes(value.toLowerCase()),
       `${slug}: the answer should echo the typed word "${value}" (got ${JSON.stringify(r.rom)})`);
  }

  /* case-insensitive: typed lowercase, key is uppercase */
  {
    const r = await type("tuesday");
    ok(r.big === expect("Tuesday"),
       `${slug}: lowercase "tuesday" should still match`);
  }

  /* unknown input: a hint, not a wrong answer and not a crash */
  {
    const r = await type("nonexistentday");
    ok(r.big === "?", `${slug}: unknown word should ask for a valid one, got ${JSON.stringify(r.big)}`);
    ok(/try a|did you mean/i.test(r.rom), `${slug}: unknown word should offer a hint`);
  }
}

console.log(`${pass} passed, ${fails.length} failed`);
for (const f of fails) console.log("  FAIL " + f);
process.exit(fails.length ? 1 : 0);
