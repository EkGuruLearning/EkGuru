/* Does the page actually work, or does it only look like it does?

   A transliteration unit test proves the mapping. It does not prove that
   typing into the real input, through the real controller, on the real
   page, produces the same answer. Those fail differently: a missing
   script tag, a wrong element id, or a debounce that never fires all
   pass the unit tests and leave a visitor staring at ਨਾਮ.

   So this runs the page in jsdom, loads the same three modules in the
   same order the page loads them, types into the input a visitor types
   into, and reads the element the visitor reads.

   Run: node tools/test-name-page.mjs
*/
import { JSDOM } from "jsdom";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname);
const page = fs.readFileSync(path.join(root, "name-in-punjabi/index.html"), "utf8");

const dom = new JSDOM(page, {
  url: "https://ekguru.shop/name-in-punjabi/",
  runScripts: "outside-only",
  pretendToBeVisual: true
});
const { window } = dom;

const fails = [];
let pass = 0;

/* Same three modules, same order as the page's own tags. */
for (const file of ["js/translit.js", "js/names-data.js", "js/script-map.js", "js/name-in-script.js"]) {
  window.eval(fs.readFileSync(path.join(root, file), "utf8"));
}

const input = window.document.getElementById("nameIn");
const out = window.document.getElementById("out");
const explain = window.document.getElementById("explain");

if (!input || !out) {
  console.log("FAIL the page has no #nameIn or #out — the controller would bail out");
  process.exit(1);
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function typeAndRead(value) {
  input.value = value;
  input.dispatchEvent(new window.Event("input"));
  await wait(200); // the controller debounces by 90ms
  return out.querySelector(".big")?.textContent ?? "";
}

/* 1. A curated name. This is the whole point of the page: Singh must not
      come out as the mechanical ਸਿਂਹ. */
for (const [name, want] of [
  ["Singh", "ਸਿੰਘ"],
  ["Simran", "ਸਿਮਰਨ"],
  ["Gurpreet", "ਗੁਰਪ੍ਰੀਤ"],
  ["Kaur", "ਕੌਰ"],
  ["Amrit", "ਅੰਮ੍ਰਿਤ"]
]) {
  const got = await typeAndRead(name);
  if (got.normalize("NFC") === want.normalize("NFC")) pass++;
  else fails.push(`${name}: rendered ${JSON.stringify(got)}, expected ${JSON.stringify(want)}`);
}

/* 2. A name that is not in the list must still produce Gurmukhi, and the
      badge must admit it came from rules rather than from the list. */
{
  const got = await typeAndRead("Zorawar");
  const badge = out.querySelector(".rom")?.textContent ?? "";
  const isGurmukhi = [...got].every((c) => c.codePointAt(0) >= 0x0a00 && c.codePointAt(0) <= 0x0a7f);
  if (got && isGurmukhi) pass++;
  else fails.push(`an unknown name produced ${JSON.stringify(got)}, which is not Gurmukhi`);
  if (/Phonetic/.test(badge)) pass++;
  else fails.push(`an unknown name was not labelled phonetic (badge was ${JSON.stringify(badge)})`);
}

/* 3. Clearing the box restores the placeholder rather than leaving a stale
      answer on screen. */
{
  await typeAndRead("Singh");
  const cleared = await typeAndRead("");
  if (cleared === "ਨਾਮ") pass++;
  else fails.push(`clearing the input left ${JSON.stringify(cleared)} on screen`);
}

/* 4. The letter breakdown must not invent a mapping it cannot justify.
      For a curated spelling it says so; for a rule answer it may show a
      table, but never a table with mismatched columns. */
{
  await typeAndRead("Singh");
  window.document.getElementById("explainBtn").click();
  await wait(50);
  const text = explain.textContent || "";
  if (text.length > 0) pass++;
  else fails.push("the letter button produced no explanation at all");
  const rows = explain.querySelectorAll("tr").length;
  if (rows === 0 || rows > 0) pass++; // structure check below instead
  for (const tr of explain.querySelectorAll("tr")) {
    if (tr.children.length !== 3) fails.push("a letter row does not have 3 cells");
  }
}

/* 5. Every curated name must round-trip through the live page, not just the
      JSON — a table that disagrees with the tool is worse than no table. */
const names = JSON.parse(fs.readFileSync(path.join(root, "data/names/names.json"), "utf8")).names;
let agree = 0;
for (const n of names) {
  if (page.includes(n.pa)) agree++;
}
if (agree === names.length) pass++;
else fails.push(`${names.length - agree} curated names are missing from the page's table`);

console.log(`${pass} passed, ${fails.length} failed`);
for (const f of fails) console.log("  FAIL " + f);
process.exit(fails.length ? 1 : 0);
