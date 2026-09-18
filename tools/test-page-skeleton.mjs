#!/usr/bin/env node
/* ==========================================================================
   test-page-skeleton.mjs — every page has one main, and the skip link lands

   The shell header has carried <a class="skip" href="#main"> since v150.
   Thirty of 1,564 pages had something with that id; on every other page the
   accessibility shortcut, and the landmark a screen reader jumps to, went
   nowhere. tools/build-shell.js now guarantees the skeleton — one
   <main id="main"> between the header and the footer — and this test is what
   keeps it there.

   Run:  node tools/test-page-skeleton.mjs
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

/* Two exceptions, both on purpose: the Google verification file has no body,
   and /admin.html sets its own body layout (and is noindex + disallowed). */
const EXEMPT = new Set(["admin.html", "googleb3b0e3defc1daa17.html"]);

console.log(`\n1. the skeleton (${pages.length} pages)\n`);

const missing = [], doubled = [], order = [], noId = [];
for (const p of pages) {
  if (EXEMPT.has(p)) continue;
  const h = read(p);
  const opens = (h.match(/<main\b/g) || []).length;
  const closes = (h.match(/<\/main>/g) || []).length;
  if (opens !== 1 || closes !== 1) { missing.push(`${p} (${opens}/${closes})`); continue; }
  const tag = (h.match(/<main\b[^>]*>/) || [""])[0];
  if (!/id="main"/.test(tag)) noId.push(p);
  const mi = h.indexOf("<main");
  const hi = h.indexOf("ekguru:shell-header:end");
  const fi = h.indexOf("ekguru:shell-footer:start");
  if (hi < 0 || fi < 0 || mi < hi || mi > fi) order.push(p);
}
ok("every page has exactly one <main>", missing.length === 0, missing.slice(0, 5).join(", "));
ok("every <main> carries id=\"main\", the skip link's target", noId.length === 0, noId.slice(0, 5).join(", "));
ok("every <main> sits between the shell header and the shell footer", order.length === 0, order.slice(0, 5).join(", "));
ok(`only the two documented pages are exempt (${pages.length - 2} checked)`,
  pages.filter((p) => !EXEMPT.has(p)).length === pages.length - 2);

console.log("\n2. the skip link\n");
const skip = pages.filter((p) => !EXEMPT.has(p)).filter((p) => !/class="skip"[^>]*href="#main"|href="#main"[^>]*class="skip"/.test(read(p)));
ok("every page links to #main from the header", skip.length === 0, skip.slice(0, 5).join(", "));
ok("the wrapper does not put the landmark inside the chrome", pages.every((p) => {
  const h = read(p);
  const mi = h.indexOf("<main");
  const ci = h.indexOf("</header>");
  return mi < 0 || ci < 0 || mi > ci;
}));

console.log("\n3. the pages that had their own main\n");
const v200 = ["index.html", "courses/index.html"];   // the two that already had a main with a class
ok("the pages that had their own main keep it, with the id",
  v200.every((p) => /<main[^>]*class="xp-main"[^>]*>/.test(read(p)) && /id="main"/.test(read(p))),
  v200.filter((p) => !/id="main"/.test(read(p))).join(", "));

console.log("\n4. print still treats main as content\n");
const css = read("css/experience.css");
const printBlock = css.slice(css.indexOf("27. PRINT — the sheet, not the website"));
ok("the print section exists after the page layer", printBlock.length > 0);
ok("main is flattened on paper, not hidden",
  /\n  \.pw, \.pw-legacy[^{]*\bmain\b[^{]*\{[^}]*max-width: none/.test(printBlock));
ok("the chrome is what gets hidden", /\.hdr, \.ftr/.test(printBlock));

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
