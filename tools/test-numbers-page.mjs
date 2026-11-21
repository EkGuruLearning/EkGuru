/* Numbers page: does the table, the data and the tool all tell one story?

   Three things can silently disagree here:
     · data/numbers/*.json  — the source
     · js/numbers-data.js   — what the tool reads (generated)
     · the visible table    — what Google indexes (generated from the same file)

   Any two of those drifting means the page contradicts itself, and the
   visitor has no way to tell which spelling to trust. So: assert all three.

   Run: node tools/test-numbers-page.mjs
*/
import { JSDOM } from "jsdom";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname);
const data = JSON.parse(fs.readFileSync(path.join(root, "data/numbers/punjabi.json"), "utf8"));
const page = fs.readFileSync(path.join(root, "numbers-in-punjabi/index.html"), "utf8");

const fails = [];
let pass = 0;
const ok = (cond, msg) => { if (cond) pass++; else fails.push(msg); };

/* ---------------- 1. the data itself ---------------- */
const ns = data.numbers.map((x) => x.n);
ok(ns.length === 101, `expected 101 entries (0-100), got ${ns.length}`);
ok(ns.every((n, i) => n === i), "numbers must run 0..100 in order with no gaps");

const words = new Set();
for (const x of data.numbers) {
  for (const ch of x.word) {
    const cp = ch.codePointAt(0);
    ok(cp >= 0x0a00 && cp <= 0x0a7f, `${x.n}: ${ch} is not Gurmukhi`);
  }
  ok(!words.has(x.word), `${x.n}: ${x.word} is used twice — two numbers cannot share a word`);
  words.add(x.word);
  ok(/^[a-z\u1e6d\u1e37\u1e45\u1e47\u1e0d\u1e5b\u1e0c\u1e0b\u1e33\u1e0a\u1e0e\u00f1\u1e63]+$/i.test(x.roman.replace(/ /g, "")),
     `${x.n}: roman "${x.roman}" has unexpected characters`);
}

/* ---------------- 2. generated JS agrees ---------------- */
const dom = new JSDOM(page, {
  url: "https://ekguru.shop/numbers-in-punjabi/",
  runScripts: "outside-only",
  pretendToBeVisual: true
});
const { window } = dom;
for (const f of ["js/numbers-data.js", "js/numbers-tool.js"]) {
  window.eval(fs.readFileSync(path.join(root, f), "utf8"));
}
const lib = window.EkGuruNumbers;
ok(!!lib, "js/numbers-data.js did not define EkGuruNumbers");

for (const x of data.numbers) {
  const hit = lib.word(x.n, "pa");
  ok(hit && hit.w === x.word, `${x.n}: tool says ${hit && hit.w}, data says ${x.word}`);
  const gur = lib.digits(x.n, "pa");
  const want = String(x.n).split("").map((d) => data.numerals[+d]).join("");
  ok(gur === want, `${x.n}: digits ${gur} != ${want}`);
}

/* ---------------- 3. the visible table agrees ---------------- */
for (const x of data.numbers) {
  const gur = String(x.n).split("").map((d) => data.numerals[+d]).join("");
  ok(page.includes(`>${x.word}<`), `the table is missing ${x.n} (${x.word})`);
  ok(page.includes(`>${gur}<`), `the table is missing the Gurmukhi digit for ${x.n} (${gur})`);
}
ok((page.match(/<tr id="n/g) || []).length === 101, "the table must have one row per number 0-100");

/* ---------------- 4. the page is honest about itself ---------------- */
ok(/rel="canonical"/.test(page), "canonical missing");
ok(page.includes('href="https://ekguru.shop/numbers-in-punjabi/" rel="canonical"'), "canonical must be self");
ok(/content="index, follow/.test(page), "page is approved for indexing, so it must say index");
ok(page.includes("numbers-data.js") && page.includes("numbers-tool.js"), "the page must load the numbers modules");
ok(!page.includes("name-in-script.js"), "the page must not load the name tool");

const baseline = JSON.parse(fs.readFileSync(path.join(root, "data/quality/indexing-baseline.json"), "utf8"));
ok(!!baseline.owner_approved_new_indexable?.["numbers-in-punjabi/index.html"],
   "a new indexable page must be in the owner-approved list");

/* ---------------- 5. the tool actually answers ---------------- */
const input = window.document.getElementById("numIn");
const out = window.document.getElementById("out");
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
await wait(30); // let the controller's ready() run before dispatching

async function type(value) {
  input.value = value;
  input.dispatchEvent(new window.Event("input"));
  await wait(140);
  return {
    big: out.querySelector(".big")?.textContent ?? "",
    rom: out.querySelector(".rom")?.textContent ?? ""
  };
}

for (const [value, word] of [["25", "ਪੰਝੀ"], ["49", "ਉਣਿੰਜਾ"], ["100", "ਸੌ"], ["0", "ਸਿਫ਼ਰ"], ["99", "ਨੜਿੰਨਵੇਂ"]]) {
  const r = await type(value);
  ok(r.rom.includes(word), `typing ${value} did not produce ${word} (got ${JSON.stringify(r.rom)})`);
  /* and the answer must be the number that was typed, not the last one */
  ok(r.rom.includes(value) || value === "0", `typing ${value} echoed the wrong number (${JSON.stringify(r.rom)})`);
}

/* garbage in, a useful message out — not a crash and not a wrong answer */
{
  const r = await type("abc");
  ok(r.big === "?", `letters should ask for numbers, got ${JSON.stringify(r.big)}`);
}

/* beyond the table it must still write the digits, and admit the limit */
{
  const r = await type("1234");
  ok(r.big === "੧੨੩੪", `1234 should render as Gurmukhi digits, got ${JSON.stringify(r.big)}`);
  ok(/built from the parts/i.test(r.rom), "beyond 100 the page must say the word is not given");
}

console.log(`${pass} passed, ${fails.length} failed`);
for (const f of fails) console.log("  FAIL " + f);
process.exit(fails.length ? 1 : 0);
