#!/usr/bin/env node
/* ==========================================================================
   test-level-visuals.mjs — the ladder, the figures, and the strip

   Prakash: "visuals har language pe honi chahiye, aur level ke hisab se umar
   badalni chahiye — chhote level pe bachche, master level pe buzurg."

   That is a claim about 352 files, so it is tested like one:

     · the ladder is the honest one — six CEFR levels and five half-steps,
       ages rising with the rungs, every age inside its own age band
     · every figure named in the manifest exists, parses as XML, states its
       level and its age, and the age really does rise rung by rung
     · every language hub carries the strip exactly once, inside <main>, with
       eleven images whose paths resolve from that page and whose alt text
       names the level — and the strip points at /how-levels-work/
     · the strip's stylesheet lives in css/experience.css and reached
       css/style.min.css (editing the source without re-bundling fails here)
     · two languages do not get the same picture: the theme is real

   Run:  node tools/test-level-visuals.mjs
   ========================================================================== */
import { readFileSync, existsSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) { pass++; console.log("  PASS  " + name); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};
const read = (p) => readFileSync(p, "utf8");

const levels = JSON.parse(read("data/levels.json"));
const manifest = JSON.parse(read("data/visuals.json"));
const RUNGS = levels.rungs;

console.log("\n1. the ladder is honest about itself\n");

{
  const labels = RUNGS.map((r) => r.label);
  ok("eleven rungs, each with a label, a name, an age and a stage",
    RUNGS.length === 11 && RUNGS.every((r) => r.label && r.name && r.age && r.stage),
    String(RUNGS.length));

  const real = ["A1", "A2", "B1", "B2", "C1", "C2"];
  ok("the six CEFR levels are all there",
    real.every((l) => labels.includes(l)), labels.join(" "));

  ok("the other five are written with a plus, not invented numbers",
    labels.filter((l) => !real.includes(l)).sort().join(",") === "A1+,A2+,B1+,B2+,C1+",
    labels.filter((l) => !real.includes(l)).join(" "));

  ok("no A3, B3, C3, C4 or C5 is claimed anywhere in the ladder",
    !RUNGS.some((r) => /^([ABC])[3-9]$/.test(r.label)));

  ok("the note says out loud that CEFR has six levels, not eleven",
    /six/i.test(levels.note) && /no A3/i.test(levels.note));

  const ages = RUNGS.map((r) => r.age);
  ok("the age rises with every rung, all the way to an elder",
    ages.every((a, i) => i === 0 || a > ages[i - 1]) && ages[0] < 12 && ages[ages.length - 1] > 70,
    ages.join(" → "));

  const bands = levels.age_bands;
  const outside = RUNGS.filter((r) => {
    const b = bands[r.stage];
    return !b || r.age < b.ages[0] || r.age > b.ages[1];
  });
  ok("every age sits inside the band its stage declares",
    outside.length === 0, outside.map((r) => r.label + "=" + r.age).join(", "));

  ok("a low level is a child and the top level is an elder",
    RUNGS[0].stage === "child" && RUNGS[RUNGS.length - 1].stage === "elder");
}

console.log("\n2. every figure exists, parses, and grows up\n");

{
  const langs = Object.keys(manifest.languages);
  ok("the manifest covers every language the site teaches",
    langs.length >= 30, String(langs.length));
  ok("there is one figure per language per rung",
    Object.keys(manifest.figures).length === langs.length * RUNGS.length,
    Object.keys(manifest.figures).length + " vs " + langs.length * RUNGS.length);

  const missing = [], broken = [], wrongAge = [], wrongLevel = [];
  const ages = {};
  for (const code of langs) {
    let previous = 0;
    for (const r of RUNGS) {
      const f = manifest.figures[code + "-" + r.id];
      if (!f || !existsSync(f.path)) { missing.push(code + "-" + r.id); continue; }
      const svg = read(f.path);
      try {
        const doc = new JSDOM(svg, { contentType: "image/svg+xml" }).window.document;
        if (!doc.documentElement || doc.documentElement.nodeName === "parsererror") throw new Error("parsererror");
      } catch (e) { broken.push(f.path); continue; }
      if (!svg.includes("age " + r.age + "<")) wrongAge.push(f.path);
      if (!svg.includes(">" + r.label + "<")) wrongLevel.push(f.path);
      ages[code] = (ages[code] || []).concat(r.age);
      if (r.age <= previous) broken.push(f.path + " (age not rising)");
      previous = r.age;
    }
  }
  ok("no figure is missing", missing.length === 0, missing.slice(0, 4).join(", "));
  ok("every figure is well-formed SVG", broken.length === 0, broken.slice(0, 4).join(", "));
  ok("every figure says the age of its level", wrongAge.length === 0, wrongAge.slice(0, 4).join(", "));
  ok("every figure is labelled with its level", wrongLevel.length === 0, wrongLevel.slice(0, 4).join(", "));
  ok("the figures of a language are the same person growing older, rung by rung",
    Object.values(ages).every((a) => a.every((v, i) => i === 0 || v > a[i - 1])));

  ok("every figure carries alt text that names the level and the language",
    Object.entries(manifest.figures).every(([k, f]) =>
      f.alt && f.alt.includes(f.label) && f.alt.includes(f.language_name)), "");

  /* Two languages must not look identical: the theme is per language, and a
     page should look like the language it teaches. */
  const hi = read(manifest.figures["hi-b1"].path), ar = read(manifest.figures["ar-b1"].path);
  const colour = (svg) => (svg.match(/stop-color="(#[0-9a-f]{6})"/i) || [])[1];
  ok("two languages get two different themes",
    colour(hi) && colour(ar) && colour(hi) !== colour(ar), colour(hi) + " vs " + colour(ar));
}

console.log("\n3. the strip is on the page, once, and it resolves\n");

{
  const bad = [];
  let hubs = 0, images = 0;
  for (const [code, info] of Object.entries(manifest.languages)) {
    const page = info.url;
    if (!existsSync(page)) { bad.push(code + ": no hub page"); continue; }
    hubs++;
    const html = read(page);
    const starts = html.split("<!-- ekguru:level-visuals:start -->").length - 1;
    const ends = html.split("<!-- ekguru:level-visuals:end -->").length - 1;
    if (starts !== 1 || ends !== 1) { bad.push(code + ": markers " + starts + "/" + ends); continue; }
    const at = html.indexOf("<!-- ekguru:level-visuals:start -->");
    if (!(html.indexOf("<main") < at && at < html.indexOf("</main>"))) {
      bad.push(code + ": strip is outside <main>"); continue;
    }
    const block = html.slice(at, html.indexOf("<!-- ekguru:level-visuals:end -->"));
    const srcs = [...block.matchAll(/<img src="([^"]+)"/g)].map((m) => m[1]);
    if (srcs.length !== RUNGS.length) { bad.push(code + ": " + srcs.length + " images"); continue; }
    const dir = path.dirname(page);
    for (const src of srcs) {
      images++;
      if (!existsSync(path.normalize(path.join(dir, src)))) bad.push(code + ": " + src + " does not resolve");
    }
    for (const r of RUNGS) {
      if (!block.includes("<b>" + r.label + "</b>")) bad.push(code + ": caption missing " + r.label);
    }
    const depth = page.split("/").length - 1;
    if (!block.includes('href="' + "../".repeat(depth) + 'how-levels-work/"')) {
      bad.push(code + ": strip does not link to how-levels-work");
    }
    const alts = [...block.matchAll(/alt="([^"]*)"/g)].map((m) => m[1]);
    if (alts.length !== RUNGS.length) bad.push(code + ": " + alts.length + " alt texts");
  }
  ok("every language in the manifest has a hub with one strip inside <main>",
    bad.filter((b) => /no hub|markers|outside/.test(b)).length === 0, bad.slice(0, 4).join("; "));
  ok("every strip has eleven images and eleven captions",
    bad.filter((b) => /images|alt texts|caption/.test(b)).length === 0, bad.slice(0, 4).join("; "));
  ok("every image path resolves from the page it is written on",
    bad.filter((b) => /resolve/.test(b)).length === 0, bad.slice(0, 4).join("; "));
  ok("every strip links to the page that explains the ladder",
    bad.filter((b) => /how-levels-work/.test(b)).length === 0, bad.slice(0, 4).join("; "));
  ok("32 hubs, 352 figures on the pages",
    hubs === Object.keys(manifest.languages).length && images === hubs * RUNGS.length,
    hubs + " hubs, " + images + " images");
}

console.log("\n4. /how-levels-work/ exists and answers the question\n");

{
  const page = "how-levels-work/index.html";
  ok("the page the strips link to exists", existsSync(page));
  const html = read(page);
  const dom = new JSDOM(html).window.document;
  ok("it has exactly one h1", dom.querySelectorAll("h1").length === 1);
  ok("it says in plain words that CEFR has no A3, C3, C4 or C5",
    /no A3/i.test(html) && /C4/i.test(html) && /six/i.test(html));
  const rows = dom.querySelectorAll("table.lv tbody tr");
  ok("the table lists all eleven rungs with the hours",
    rows.length === 11 && [...rows].every((tr) => tr.children.length === 4),
    String(rows.length));
  ok("every rung label appears in the table",
    RUNGS.every((r) => [...rows].some((tr) => tr.children[0].textContent.trim() === r.label)));
  const figs = [...dom.querySelectorAll("figure.lv-fig img")].map((i) => i.getAttribute("src"));
  ok("its own figures resolve",
    figs.length === 6 && figs.every((s) => existsSync(path.normalize(path.join("how-levels-work", s)))),
    figs.length + " figures");
  const ld = dom.querySelector('script[type="application/ld+json"]');
  const graph = ld ? JSON.parse(ld.textContent)["@graph"] : [];
  ok("it carries FAQ structured data for the questions it answers",
    graph.some((g) => g["@type"] === "FAQPage") && graph.some((g) => g["@type"] === "Article"));
  ok("it is classified but carries no ad loader while the release gate is closed",
    /data-ad-class="/.test(html) && !/adsbygoogle\.js/.test(html));
  ok("no page links to it from the strip of a language that has no hub",
    Object.values(manifest.languages).every((l) => existsSync(l.url)));
}

console.log("\n5. the stylesheet that draws the strip is bundled\n");

{
  const css = read("css/experience.css");
  const min = read("css/style.min.css");
  ok("the strip's rules live in css/experience.css",
    /\.lv-strip\s*\{/.test(css) && /\.lv-fig\s*\{/.test(css) && /\.lv-fig img/.test(css));
  ok("the bundle carries them, so the page is styled on first paint",
    /\.lv-strip\{/.test(min) && /\.lv-fig\{/.test(min));
  ok("the strip styles come before the print rules (print stays the last word)",
    css.indexOf(".lv-strip {") < css.indexOf("TWO RULES, IN THIS ORDER"));
  ok("the images keep their aspect ratio, so nothing shifts as they load",
    /\.lv-fig img[^}]*height:\s*auto/.test(css));
}

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
