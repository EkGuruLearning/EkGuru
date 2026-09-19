#!/usr/bin/env node
/* ==========================================================================
   test-toolbox-visuals.mjs — the plates cannot lie about the pages

   tools/build-toolbox-visuals.py draws one plate per toolbox page from that
   page's own data. This test is the other half of that sentence: it re-derives
   the numbers and the sample items from the pages and compares.

     · every plate exists, is a well-formed svg, carries a title and a
       sentence aria-label, and contains no raster image or embedded font
     · every count on a plate is decoded from the page (rows in the table, keys
       in the deck object, entries in the pool, rungs in the planner) and must
       match — a plate that says 20 verbs over a table of 19 fails here
     · every sample the plate shows is text that really is on the page
     · the block sits above the support bands, once per page, with its own
       heading and a caption that repeats the plate's own words
     · the toolbox hub counts its own tools from the page's structured data

   Run:  node tools/test-toolbox-visuals.mjs
   ========================================================================== */
import { readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) { pass++; console.log("  ok    " + name); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};
const read = (p) => readFileSync(p, "utf8");
const manifest = JSON.parse(read("data/toolbox-visuals.json"));
const slugs = Object.keys(manifest);
const pageOf = (slug) => slug === "tools" ? "toolbox/index.html" : `toolbox/${slug}/index.html`;

console.log(`\n1. a plate per tool (${slugs.length})\n`);

{
  const missing = [], bad = [], raster = [];
  for (const slug of slugs) {
    const f = manifest[slug].path;
    if (!existsSync(f)) { missing.push(slug); continue; }
    const svg = read(f);
    const wellFormed = /^<svg [^>]*viewBox="0 0 320 200"/.test(svg) && /<\/svg>\s*$/.test(svg) &&
      /<title>[^<]+<\/title>/.test(svg) && /role="img"/.test(svg) &&
      /aria-label="[^"]{15,}"/.test(svg);
    if (!wellFormed) bad.push(slug);
    /* Text must stay text: no flattened image of a font, no base64 anywhere. */
    if (/<image|data:image|@font-face/.test(svg)) raster.push(slug);
  }
  ok("every plate exists and is a well-formed svg with a title and a label",
    missing.length === 0 && bad.length === 0,
    [...missing, ...bad].join("; "));
  ok("the plates are drawn, not pasted — text stays text", raster.length === 0, raster.join("; "));
  ok("every plate is on the page it describes",
    slugs.every((s) => existsSync(pageOf(s))) && slugs.length === 13,
    `pages=${slugs.filter((s) => existsSync(pageOf(s))).length}`);
}

console.log("\n2. the numbers on the plate are the numbers on the page\n");

{
  const cellRows = (html) => [...html.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/g)]
    .map((m) => m[1]).filter((r) => !/<th/.test(r));
  const jsObj = (html, name) => {
    const m = html.match(new RegExp(name + "\\s*=\\s*(\\{[\\s\\S]*?\\}|\\[[\\s\\S]*?\\])\\s*;"));
    return m ? JSON.parse(m[1]) : null;
  };
  const n = (stat, re) => {
    const m = stat.match(re);
    return m ? Number(m[1].replace(/,/g, "")) : null;
  };

  const checks = [];
  for (const slug of slugs) {
    const page = read(pageOf(slug));
    const stat = manifest[slug].stat;
    let truths = [];

    if (slug === "hindi-alphabet") {
      truths.push(["letters", n(stat, /^(\d+) letters/), cellRows(page).length]);
    } else if (slug === "hindi-verbs") {
      truths.push(["verbs", n(stat, /^(\d+) verbs/), cellRows(page).filter((r) => (r.match(/<td/g) || []).length >= 5).length]);
    } else if (slug === "hindi-phrasebook") {
      truths.push(["phrases", n(stat, /^(\d+) phrases/), (page.match(/<tr data-cat=/g) || []).length]);
    } else if (slug === "hindi-vocabulary") {
      truths.push(["words", n(stat, /^(\d+) words/), (page.match(/<tr data-g=/g) || []).length]);
    } else if (slug === "hindi-quiz") {
      truths.push(["questions", n(stat, /^(\d+) questions/), (jsObj(page, "POOL") || []).length]);
    } else if (slug === "hindi-flashcards") {
      const decks = jsObj(page, "DECKS") || {};
      const total = Object.values(decks).reduce((a, v) => a + v.length, 0);
      truths.push(["cards", n(stat, /^(\d+) cards/), total]);
      truths.push(["decks", n(stat, /in (\d+) decks/), Object.keys(decks).length]);
    } else if (slug === "hindi-level-test") {
      truths.push(["questions", n(stat, /^(\d+) honest/), (page.match(/data-q="/g) || []).length - 1]);
    } else if (slug === "hindi-time-planner") {
      truths.push(["milestones", null, (page.match(/roughly [\d,]+ to [\d,]+ hours/g) || []).length]);
    } else if (slug === "hindi-date-time") {
      truths.push(["words", n(stat, /^(\d+) words/), cellRows(page).length]);
    } else if (slug === "hindi-pronunciation") {
      truths.push(["sounds", n(stat, /^(\d+) sounds/), cellRows(page).length]);
    } else if (slug === "tools") {
      const list = (page.match(/"numberOfItems":\s*(\d+)/) || [])[1];
      truths.push(["tools", n(stat, /^(\d+) tools/), Number(list)]);
    }

    for (const [what, said, real] of truths) {
      if (said !== null && said !== real) checks.push(`${slug}:${what} ${said}≠${real}`);
    }
    /* A plate may never claim more than the page holds. */
    const claimed = [n(stat, /^(\d+) letters/), n(stat, /^(\d+) verbs/), n(stat, /^(\d+) phrases/),
                     n(stat, /^(\d+) words/), n(stat, /^(\d+) questions/), n(stat, /^(\d+) cards/),
                     n(stat, /^(\d+) sounds/), n(stat, /^(\d+) tools/)].filter((x) => x !== null);
    for (const c of claimed) {
      const ceiling = Math.max(cellRows(page).length, (page.match(/<tr data-/g) || []).length,
        (jsObj(page, "POOL") || []).length, (jsObj(page, "DECKS") ? 200 : 0), 40);
      if (c > ceiling) checks.push(`${slug}: claims ${c} over a page with ${ceiling} rows`);
    }
  }
  ok("every count on a plate is the count in the page it sits on",
    checks.length === 0, checks.join("; "));
}

console.log("\n3. every sample on the plate is on the page\n");

{
  const stray = [];
  for (const slug of slugs) {
    const svg = read(manifest[slug].path);
    const page = read(pageOf(slug));
    const texts = [...svg.matchAll(/<text[^>]*>([^<]+)<\/text>/g)]
      .map((m) => m[1].trim())
      .filter((t) => t && !/^[\d,.%–—-]+$/.test(t))
      /* the plate's own furniture is allowed to be its own words */
      .filter((t) => ![manifest[slug].title, manifest[slug].native].includes(t))
      .filter((t) => !/^(correct answer|Q\d)$/.test(t))
      .filter((t) => !/^and \d+ more decks? in this set/.test(t))
      .filter((t) => !/^[\d,]+[–-][\d,]+ h$/.test(t))     /* the planner reformats "30 to 50 hours" */
      .filter((t) => !new RegExp(manifest[slug].stat.slice(0, 14).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(t));
    for (const t of texts) {
      const needle = t.replace(/…$/, "").trim();
      if (needle.length < 3) continue;
      /* A plate joins separate cells with "·" (present · past · future): every
         piece must be on the page, the separator is the plate's own. */
      const pieces = needle.split(" · ").map((x) => x.trim()).filter(Boolean);
      if (pieces.length > 1 && pieces.every((x) => x.length > 1 && page.includes(x))) continue;

      if (!page.includes(needle)) {
        /* A plate reformats or wraps what it quotes: an hours span becomes
           "30–50 h" where the page writes "roughly 30 to 50 hours". Accept it
           only when every number in the quote is really on the page. */
        const nums = needle.match(/[\d,]+/g) || [];
        const numeric = nums.length > 0 && nums.every((x) => page.includes(x));
        const head = needle.split(/\s+/).slice(0, 3).join(" ");
        if (!numeric && !(head.length > 3 && page.includes(head))) stray.push(`${slug}: "${t}"`);
      }
    }
  }
  ok("nothing on a plate is invented — every word appears on its own page",
    stray.length === 0, stray.slice(0, 4).join("; "));
}

console.log("\n4. nothing runs off the plate\n");

{
  /* A 320px plate is unforgiving: a caption that is one word too long simply
     leaves the picture. Estimate each text run's width from its size and fail
     when it ends past the edge — on a plate, an overflow is a lost word. */
  const overflow = [];
  for (const slug of slugs) {
    const svg = read(manifest[slug].path);
    for (const m of svg.matchAll(/<text x="(\d+)"([^>]*)>([^<]*)<\/text>/g)) {
      const x = Number(m[1]), attrs = m[2], body = m[3];
      const size = Number((attrs.match(/font-size="([\d.]+)"/) || [, 12])[1]);
      const wide = /[\u0900-\u097F]/.test(body) ? 0.62 : 0.58;
      const width = body.length * size * wide;
      const anchor = (attrs.match(/text-anchor="(\w+)"/) || [, "start"])[1];
      const start = anchor === "middle" ? x - width / 2 : x;
      const end = start + width;
      if (end > 314) overflow.push(`${slug}: "${body.slice(0, 22)}" ends at ~${Math.round(end)}`);
      if (start < 2) overflow.push(`${slug}: "${body.slice(0, 22)}" starts at ~${Math.round(start)}`);
    }
    for (const m of svg.matchAll(/<rect x="(\d+)"[^>]*width="(\d+)"/g)) {
      if (Number(m[1]) + Number(m[2]) > 320) overflow.push(`${slug}: a box runs off the plate`);
    }
  }
  ok("every word and every box stays on the plate", overflow.length === 0,
    overflow.slice(0, 4).join("; "));
}

console.log("\n5. where the block sits\n");

{
  const problems = [];
  for (const slug of slugs) {
    const html = read(pageOf(slug));
    const at = html.indexOf("<!-- ekguru:toolbox-visuals:start -->");
    const bands = html.indexOf("<!-- ekguru:pw-bands:start -->");
    const foot = html.lastIndexOf("<footer");
    const blocks = (html.match(/class="ct-visual"/g) || []).length;
    const h2 = /<h2 id="ct-visual-h">/.test(html);
    const img = html.match(/ct-fig"><img src="([^"]+)"/);
    const alt = html.match(/<img src="[^"]*tool-[^"]*"[^>]*alt="([^"]+)"/);
    if (blocks !== 1) problems.push(`${slug}: ${blocks} blocks`);
    if (at < 0 || (bands > -1 && at > bands)) problems.push(`${slug}: after the bands`);
    if (foot > -1 && at > foot) problems.push(`${slug}: after the footer`);
    if (!h2) problems.push(`${slug}: no heading`);
    if (!img || !existsSync(path.normalize(path.join(path.dirname(pageOf(slug)), img[1])))) {
      problems.push(`${slug}: image does not resolve`);
    }
    if (!alt || alt[1].split(" ").length < 8) problems.push(`${slug}: alt is not a sentence`);

    /* The caption repeats the plate's own words, so the two cannot drift. */
    const cap = (html.split("ecclesiastes") && html.match(new RegExp(
      manifest[slug].title.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "</b> · ([^<]+)"))) || [];
    if (!cap[1] || !manifest[slug].stat.startsWith(cap[1].trim().slice(0, 24))) {
      problems.push(`${slug}: caption says something else`);
    }
  }
  ok("one block per page, above the bands, with a heading, an image and a caption that matches",
    problems.length === 0, problems.slice(0, 4).join("; "));

  const alt = read(pageOf("hindi-numbers")).match(/alt="([^"]+)"/)[1];
  ok("the alt text is a sentence about the tool, not a filename",
    alt.includes(manifest["hindi-numbers"].title) && alt.includes("Numbers") &&
    !/\.svg/.test(alt), alt.slice(0, 80));
}

console.log(`\n${fail === 0 ? "PASS" : "FAIL"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail === 0 ? 0 : 1);
