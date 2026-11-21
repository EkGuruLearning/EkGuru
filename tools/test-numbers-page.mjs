/* Numbers page: does the table, the data and the tool all tell one story?

   Three things can silently disagree here:
     · data/numbers/*.json  — the source
     · js/numbers-data.js   — what the tool reads (generated)
     · the visible table    — what Google indexes (generated from the same file)

   Any two of those drifting means the page contradicts itself, and the
   visitor has no way to tell which spelling to trust. So: assert all three.
   Runs per language, so a new data file gets full coverage for free.

   Run: node tools/test-numbers-page.mjs
*/
import { JSDOM } from "jsdom";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname);
const PAGE_SPECS = [
  { slug: "numbers-in-punjabi", file: "data/numbers/punjabi.json", lang: "pa",
    samples: [["25", "ਪੰਝੀ"], ["49", "ਉਣਿੰਜਾ"], ["100", "ਸੌ"], ["0", "ਸਿਫ਼ਰ"], ["99", "ਨੜਿੰਨਵੇਂ"]] },
  { slug: "numbers-in-marathi", file: "data/numbers/marathi.json", lang: "mr",
    samples: [["49", "एकोणपन्नास"], ["99", "नव्व्याण्णव"], ["100", "शंभर"], ["0", "शून्य"], ["75", "पंच्याहत्तर"]] },
];

const fails = [];
let pass = 0;
const ok = (cond, msg) => { if (cond) pass++; else fails.push(msg); };

for (const { slug, file, lang, samples } of PAGE_SPECS) {
  /* ---------------- 1. the data itself ---------------- */
  const data = JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
  const ns = data.numbers.map((x) => x.n);
  ok(ns.length === 101, `${slug}: expected 101 entries (0-100), got ${ns.length}`);
  ok(ns.every((n, i) => n === i), `${slug}: numbers must run 0..100 in order with no gaps`);
  ok(data.language === lang, `${slug}: data language must be ${lang}, got ${data.language}`);

  const words = new Set();
  for (const x of data.numbers) {
    for (const ch of x.word) {
      const cp = ch.codePointAt(0);
      /* Punjabi is Gurmukhi, Marathi is Devanagari — whatever the script,
         it must be that language's block, not a hole or ASCII. */
      ok(cp >= 0x0a00 && cp <= 0x0a7f || cp >= 0x0900 && cp <= 0x097f,
         `${slug} ${x.n}: ${ch} is not in a known Indic script`);
    }
    ok(!words.has(x.word), `${slug} ${x.n}: ${x.word} is used twice — two numbers cannot share a word`);
    words.add(x.word);
  }

  /* ---------------- 2. generated JS agrees ---------------- */
  const page = fs.readFileSync(path.join(root, `${slug}/index.html`), "utf8");
  const dom = new JSDOM(page, {
    url: `https://ekguru.shop/${slug}/`,
    runScripts: "outside-only",
    pretendToBeVisual: true
  });
  const { window } = dom;
  for (const f of ["js/numbers-data.js", "js/numbers-tool.js"]) {
    window.eval(fs.readFileSync(path.join(root, f), "utf8"));
  }
  const lib = window.EkGuruNumbers;
  ok(!!lib, `${slug}: js/numbers-data.js did not define EkGuruNumbers`);

  for (const x of data.numbers) {
    const hit = lib.word(x.n, lang);
    ok(hit && hit.w === x.word, `${slug} ${x.n}: tool says ${hit && hit.w}, data says ${x.word}`);
    const gur = lib.digits(x.n, lang);
    const want = String(x.n).split("").map((d) => data.numerals[+d]).join("");
    ok(gur === want, `${slug} ${x.n}: digits ${gur} != ${want}`);
  }

  /* ---------------- 3. the visible table agrees ---------------- */
  for (const x of data.numbers) {
    ok(page.includes(`>${x.word}<`), `${slug}: the table is missing ${x.n} (${x.word})`);
    const gur = String(x.n).split("").map((d) => data.numerals[+d]).join("");
    ok(page.includes(`>${gur}<`), `${slug}: the table is missing the digit for ${x.n} (${gur})`);
  }
  ok((page.match(/<tr id="n/g) || []).length === 101, `${slug}: the table must have one row per number 0-100`);

  /* ---------------- 4. the page is honest about itself ---------------- */
  ok(page.includes(`href="https://ekguru.shop/${slug}/" rel="canonical"`), `${slug}: canonical must be self`);
  ok(/content="index, follow/.test(page), `${slug}: approved for indexing, must say index`);
  ok(page.includes("numbers-data.js") && page.includes("numbers-tool.js"), `${slug}: must load the numbers modules`);
  ok(!page.includes("name-in-script.js"), `${slug}: must not load the name tool`);

  const baseline = JSON.parse(fs.readFileSync(path.join(root, "data/quality/indexing-baseline.json"), "utf8"));
  ok(!!baseline.owner_approved_new_indexable?.[`${slug}/index.html`],
     `${slug}: a new indexable page must be in the owner-approved list`);

  /* ---------------- 5. the tool actually answers ---------------- */
  const input = window.document.getElementById("numIn");
  const out = window.document.getElementById("out");
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

  for (const [value, word] of samples) {
    const r = await type(value);
    ok(r.rom.includes(word), `${slug}: typing ${value} did not produce ${word} (got ${JSON.stringify(r.rom)})`);
  }

  /* garbage in, a useful message out — not a crash and not a wrong answer */
  {
    const r = await type("abc");
    ok(r.big === "?", `${slug}: letters should ask for numbers, got ${JSON.stringify(r.big)}`);
  }

  /* beyond the table it must still write the digits, and admit the limit */
  {
    const r = await type("1234");
    const gur = String(1234).split("").map((d) => data.numerals[+d]).join("");
    ok(r.big === gur, `${slug}: 1234 should render as ${gur}, got ${JSON.stringify(r.big)}`);
    ok(/built from the parts/i.test(r.rom), `${slug}: beyond 100 the page must say the word is not given`);
  }
}

console.log(`${pass} passed, ${fails.length} failed`);
for (const f of fails) console.log("  FAIL " + f);
process.exit(fails.length ? 1 : 0);
