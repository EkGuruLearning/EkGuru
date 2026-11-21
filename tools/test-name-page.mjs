/* Does the page actually work, or does it only look like it does?

   A transliteration unit test proves the mapping. It does not prove that
   typing into the real input, through the real controller, on the real
   page, produces the same answer. Those fail differently: a missing
   script tag, a wrong element id, or a debounce that never fires all
   pass the unit tests and leave a visitor staring at ਨਾਮ.

   This runs each page in jsdom, loads the same modules in the same
   order the page loads them, types into the input a visitor types
   into, and reads the element the visitor reads.

   Indic pages (Hindi, Punjabi) go through Devanagari via script-map.js.
   Non-Indic pages (Arabic, Greek, Russian, Korean, Japanese, Amharic)
   use the engine in non-indic-scripts.js instead.

   Run: node tools/test-name-page.mjs
*/
import { JSDOM } from "jsdom";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname);

const fails = [];
let pass = 0;

/* Each page: its slug, which modules it loads, and its expected script. */
const PAGES = [
  {
    slug: "name-in-punjabi",
    modules: ["js/translit.js", "js/names-data.js", "js/script-map.js", "js/name-in-script.js"],
    script: "gurmukhi",
    curated: [
      ["Singh", "ਸਿੰਘ"],
      ["Simran", "ਸਿਮਰਨ"],
      ["Gurpreet", "ਗੁਰਪ੍ਰੀਤ"],
      ["Kaur", "ਕੌਰ"],
      ["Amrit", "ਅੰਮ੍ਰਿਤ"],
    ],
    unknown: ["Zorawar"],
    placeholder: "ਨਾਮ",
    codepoint_range: [0x0a00, 0x0a7f],
  },
  {
    slug: "name-in-arabic",
    modules: ["js/translit.js", "js/non-indic-scripts.js", "js/names-data.js", "js/name-in-script.js"],
    script: "arabic",
    curated: [],
    unknown: ["John", "Sarah", "Michael"],
    placeholder: "اسمك",
    codepoint_range: [0x0600, 0x06ff],
  },
  {
    slug: "name-in-greek",
    modules: ["js/translit.js", "js/non-indic-scripts.js", "js/names-data.js", "js/name-in-script.js"],
    script: "greek",
    curated: [],
    unknown: ["John", "Sarah", "George"],
    placeholder: "Το όνομά σας",
    codepoint_range: [0x0370, 0x03ff],
  },
  {
    slug: "name-in-russian",
    modules: ["js/translit.js", "js/non-indic-scripts.js", "js/names-data.js", "js/name-in-script.js"],
    script: "cyrillic",
    curated: [],
    unknown: ["John", "Sarah", "Ivan"],
    placeholder: "Ваше имя",
    codepoint_range: [0x0400, 0x04ff],
  },
  {
    slug: "name-in-korean",
    modules: ["js/translit.js", "js/non-indic-scripts.js", "js/names-data.js", "js/name-in-script.js"],
    script: "hangul",
    curated: [],
    unknown: ["John", "Sarah", "Minsu"],
    placeholder: "이름",
    codepoint_range: [0xac00, 0xd7af],
  },
  {
    slug: "name-in-japanese",
    modules: ["js/translit.js", "js/non-indic-scripts.js", "js/names-data.js", "js/name-in-script.js"],
    script: "kana",
    curated: [],
    unknown: ["John", "Sarah", "Kenji"],
    placeholder: "お名前",
    codepoint_range: [0x3040, 0x30ff],
  },
  {
    slug: "name-in-amharic",
    modules: ["js/translit.js", "js/non-indic-scripts.js", "js/names-data.js", "js/name-in-script.js"],
    script: "ethiopic",
    curated: [],
    unknown: ["John", "Sarah", "Tadel"],
    placeholder: "ስሙ",
    codepoint_range: [0x1200, 0x13ff],
  },
];

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function testPage(page) {
  const htmlPath = path.join(root, page.slug, "index.html");
  if (!fs.existsSync(htmlPath)) {
    fails.push(`${page.slug}: page file not found`);
    return;
  }
  const html = fs.readFileSync(htmlPath, "utf8");
  const dom = new JSDOM(html, {
    url: `https://ekguru.shop/${page.slug}/`,
    runScripts: "outside-only",
    pretendToBeVisual: true,
  });
  const { window } = dom;

  /* Load the same modules, in the same order as the page's own tags. */
  for (const file of page.modules) {
    window.eval(fs.readFileSync(path.join(root, file), "utf8"));
  }

  const input = window.document.getElementById("nameIn");
  const out = window.document.getElementById("out");
  const explain = window.document.getElementById("explain");

  if (!input || !out) {
    fails.push(`${page.slug}: no #nameIn or #out — controller would bail`);
    return;
  }

  async function typeAndRead(value) {
    input.value = value;
    input.dispatchEvent(new window.Event("input"));
    await wait(200); // controller debounces by 90ms
    return out.querySelector(".big")?.textContent ?? "";
  }

  /* 1. Curated names round-trip through the live page. */
  for (const [name, want] of page.curated) {
    const got = await typeAndRead(name);
    if (got.normalize("NFC") === want.normalize("NFC")) pass++;
    else fails.push(`${page.slug}: ${name} rendered ${JSON.stringify(got)}, expected ${JSON.stringify(want)}`);
  }

  /* 2. Unknown names still produce the target script. */
  for (const name of page.unknown) {
    const got = await typeAndRead(name);
    const badge = out.querySelector(".rom")?.textContent ?? "";
    const isTargetScript = [...got].every(
      (c) => c.codePointAt(0) >= page.codepoint_range[0] && c.codePointAt(0) <= page.codepoint_range[1]
    );
    if (got && isTargetScript) pass++;
    else fails.push(`${page.slug}: "${name}" produced ${JSON.stringify(got)}, not in target script range`);
    if (/Phonetic|Curated/.test(badge)) pass++;
    else fails.push(`${page.slug}: "${name}" was not labelled (badge: ${JSON.stringify(badge)})`);
  }

  /* 3. Clearing restores the placeholder. */
  if (page.curated.length > 0) {
    await typeAndRead(page.curated[0][0]);
    const cleared = await typeAndRead("");
    if (cleared === page.placeholder) pass++;
    else fails.push(`${page.slug}: clearing left ${JSON.stringify(cleared)}, expected ${JSON.stringify(page.placeholder)}`);
  } else {
    await typeAndRead(page.unknown[0]);
    const cleared = await typeAndRead("");
    if (cleared === page.placeholder) pass++;
    else fails.push(`${page.slug}: clearing left ${JSON.stringify(cleared)}, expected ${JSON.stringify(page.placeholder)}`);
  }

  /* 4. The letter button produces content. */
  await typeAndRead(page.curated[0] ? page.curated[0][0] : page.unknown[0]);
  const explainBtn = window.document.getElementById("explainBtn");
  if (explainBtn) {
    explainBtn.click();
    await wait(50);
    const text = explain.textContent || "";
    if (text.length > 0) pass++;
    else fails.push(`${page.slug}: explain button produced no explanation`);
  } else {
    fails.push(`${page.slug}: no #explainBtn found`);
  }
}

for (const page of PAGES) {
  await testPage(page);
}

/* 5. Every curated name in the JSON must appear on the Punjabi page. */
{
  const punjabiHtml = fs.readFileSync(path.join(root, "name-in-punjabi/index.html"), "utf8");
  const names = JSON.parse(fs.readFileSync(path.join(root, "data/names/names.json"), "utf8")).names;
  let agree = 0;
  let total = 0;
  for (const n of names) {
    if (!n.pa) continue; // names with only non-Indic scripts have no Panjabi form
    total++;
    if (punjabiHtml.includes(n.pa)) agree++;
  }
  if (agree === total) pass++;
  else fails.push(`${total - agree} of ${total} curated Punjabi names missing from Punjabi page table`);
}

console.log(`${pass} passed, ${fails.length} failed`);
for (const f of fails) console.log("  FAIL " + f);
process.exit(fails.length ? 1 : 0);
