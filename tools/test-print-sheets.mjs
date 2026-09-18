#!/usr/bin/env node
/* ==========================================================================
   test-print-sheets.mjs — what actually lands on paper

   Prakash, twice: "print worksheet pura page print karti hai, lekin hum
   only worksheet print karna hai", and the standing rule that a printed
   EkGuru sheet carries the watermark and the tagline.

   A browser is not available here, so this test does not screenshot. It
   checks the three things that decide the printed page:

     1. the print rules exist in css/experience.css (and reach the bundle)
     2. the chrome is in the hide list, the sheet is not
     3. the printable pages are marked, and only they are

   Run:  node tools/test-print-sheets.mjs
   ========================================================================== */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) { pass++; console.log("  PASS  " + name); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};

const read = (p) => fs.readFileSync(p, "utf8");
const css = read("css/experience.css");
const bundle = read("css/style.min.css");
const copywatch = read("js/copywatch.js");

/* The print section, on its own, so the assertions below read the rules and
   not the whole stylesheet. */
const i = css.indexOf("@media print");
ok("css/experience.css has a print section", i > -1);
const printCss = i > -1 ? css.slice(i) : "";

console.log("\n1. the rules exist\n");

ok("print section says what it is for (worksheet, only the sheet)",
  /only the sheet|only that sheet|sheet, not the website/i.test(css));
for (const sel of [".hdr", ".ftr", ".crumb", ".pw-support", ".pw-next",
                   ".adsbygoogle", "#ekguru-consent", ".sb-band", ".no-print"]) {
  ok(`print hides ${sel}`, printCss.includes(sel));
}
ok("print keeps the copy source stamp visible",
  /#ekguru-print-src\s*\{[^}]*display:\s*block\s*!important/.test(printCss));
ok("print does not hide #ekguru-print-src in the chrome list",
  !/\.hdr[^{]*\{[^}]*\}/.test("") && !/#ekguru-print-src[^{]*\{[^}]*display:\s*none/.test(printCss));

ok("sheet mode is driven by body[data-print=\"sheet\"]",
  /body\[data-print="sheet"\]/.test(printCss));
ok("sheet mode prints the marked target",
  /body\[data-print="sheet"\]\s*\[data-print-target\]/.test(printCss));
ok("sheet mode flattens the worksheet card",
  /body\[data-print="sheet"\]\s*\.ws-page/.test(printCss));
ok("sheet mode keeps the writing lines dark",
  /body\[data-print="sheet"\]\s*\.ws-page\s*div\[style\*="border-bottom"\]/.test(printCss));

ok("print rules reach the bundle", bundle.includes("body[data-print=\"sheet\"]"));
ok("bundle hides the chrome too", /@media print/.test(bundle) && bundle.includes("#ekguru-consent"));
ok("one @page margin for every page", /@page\s*\{[^}]*margin/.test(printCss));

console.log("\n2. the watermark and the tagline\n");

ok("copywatch stamps the print source", copywatch.includes("ekguru-print-src"));
ok("the stamp carries the live sheet tagline", /sheet\.tagline/.test(copywatch));
ok("the stamp carries the date and the brand",
  /printed " \+ new Date/.test(copywatch) && copywatch.includes("ekguru.shop"));
ok("the generated worksheet sheet is watermarked (.ws-page)",
  /\.ws-page/.test(copywatch.slice(copywatch.indexOf("stampSheets"), copywatch.indexOf("function boot"))));
ok("materials guides are watermarked (.art)",
  copywatch.slice(copywatch.indexOf("stampSheets"), copywatch.indexOf("function boot")).includes(".art"));
ok("the watermark rule exists and prints",
  /\[data-watermark\]::after/.test(css) && /\[data-watermark\]::after/.test(printCss));

console.log("\n3. which pages are sheets\n");

const SKIP = new Set([".git", "node_modules", "images", "css", "js", "data",
                      "reports", "docs", "templates", "research", "tools"]);
const pages = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { if (!SKIP.has(e.name) && !e.name.startsWith(".")) walk(p); }
    else if (e.name.endsWith(".html")) pages.push(p.replace(/^\.\//, ""));
  }
})(".");

const marked = pages.filter((p) => /<body[^>]*data-print="sheet"/.test(read(p)));
const worksheets = pages.filter((p) => p.includes("/practice/worksheets/"));
/* The guides carry their own Print button. materials/index.html is the hub
   that lists them — a listing is not a sheet, and must not be marked. */
const materials = pages.filter((p) => p.startsWith("materials/"));
const guides = materials.filter((p) => /window\.print\s*\(\s*\)/.test(read(p)));

ok(`every worksheet page is a sheet (${worksheets.length} pages)`,
  worksheets.length > 0 && worksheets.every((p) => marked.includes(p)),
  worksheets.filter((p) => !marked.includes(p)).join(", "));
ok(`every printed guide is a sheet (${guides.length} pages)`,
  guides.length > 0 && guides.every((p) => marked.includes(p)),
  guides.filter((p) => !marked.includes(p)).join(", "));
ok("the materials hub is a listing, not a sheet",
  materials.length > guides.length &&
  materials.filter((p) => !guides.includes(p)).every((p) => !marked.includes(p)));
ok("nothing else claims to be a sheet",
  marked.every((p) => worksheets.includes(p) || guides.includes(p)),
  marked.filter((p) => !worksheets.includes(p) && !guides.includes(p)).join(", "));
ok("every sheet names its target element",
  marked.every((p) => /data-print-target/.test(read(p))));
ok("a sheet target is one element, not the page",
  marked.every((p) => (read(p).match(/data-print-target/g) || []).length === 1));
ok("no sheet page prints the site header inside the target",
  marked.every((p) => !/<div class="art"[^>]*data-print-target[^>]*>[\s\S]*class="hdr"/.test(read(p))));

console.log("\n4. the worksheet page itself\n");

const ws = "learn/hindi/practice/worksheets/index.html";
const wsHtml = read(ws);
ok("the worksheet builder is present", wsHtml.includes('<div id="ws-app"'));
ok("the builder is the print target",
  /<div id="ws-app" data-print-target/.test(wsHtml));
ok("the controls are the only thing hidden around the sheet",
  /#ws-app > \*:not\(#w-sheet\)/.test(printCss));
ok("the sheet is built with a class the print layer knows",
  read("js/hindi-tools.js").includes('class="ws-page"'));
ok("the sheet carries the free-to-print line",
  /free to print and share/.test(read("js/hindi-tools.js")));

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
