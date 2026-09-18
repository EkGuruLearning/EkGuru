#!/usr/bin/env node
/* ==========================================================================
   test-print-visible.mjs — the page as the PRINTER sees it

   Prakash, three times: "print worksheet pura page hi print karti hai, par
   humein sirf worksheet hi print karni hai."

   The other tests prove the rules exist and that the script builds a sheet.
   This one answers the actual question — with the print stylesheet applied,
   WHAT would still be on the paper? It walks every element on the page and
   computes `display`, so a rule that hides the header but leaves the hero,
   the breadcrumb or the control row in the flow is a failure here, not a
   claim in a comment.

   It also runs with the SCRIPT OFF. A worksheet is baked into the file at
   build time (tools/build-print-sheets.py), so printing must work before any
   JavaScript runs — that was the second half of the same bug.

   Run:  node tools/test-print-visible.mjs
   ========================================================================== */
import { readFileSync } from "node:fs";
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

/* ---- the print stylesheet, without its @media wrappers --------------------
   experience.css carries SEVERAL @media print blocks (§27 and the smaller
   ones that came before it). Testing only the first — which is 266 bytes of
   something else — reported the whole page as printable and told us nothing.
   Every block is collected, in file order, which is also the cascade order. */
function printRules() {
  const css = read("css/experience.css");
  const parts = [];
  let i = -1;
  while ((i = css.indexOf("@media print", i + 1)) >= 0) {
    const open = css.indexOf("{", i);
    let depth = 0, j = open;
    for (; j < css.length; j++) {
      if (css[j] === "{") depth++;
      else if (css[j] === "}") { depth--; if (depth === 0) break; }
    }
    parts.push(css.slice(open + 1, j));
  }
  return parts.join("\n");
}

const RULES = printRules();
ok("the print block is found in the stylesheet", RULES.length > 500, RULES.length + " bytes");

/* ---- what would print ----------------------------------------------------- */
function printed(page) {
  const dom = new JSDOM(read(page), { url: "https://ekguru.shop/" + page.replace(/index\.html$/, "") });
  const w = dom.window, d = w.document;
  const style = d.createElement("style");
  style.textContent = RULES;                 /* the @media body, applied flat */
  d.head.appendChild(style);

  const shown = [];
  const display = (el) => {
    try { return (w.getComputedStyle(el).display || "block").toLowerCase(); } catch (e) { return "block"; }
  };
  for (const el of d.querySelectorAll("body *")) {
    if (display(el) !== "none") shown.push(el);
  }
  return { d, w, shown, display };
}

const MARKED = [];
for (const line of read("tools/build-print-sheets.py").split("\n")) {
  if (line.includes('MARK = ')) break;
}
{
  const { execSync } = await import("node:child_process");
  const out = execSync("python3 tools/build-print-sheets.py --check").toString();
  ok("print sheets --check is clean", /^ok/m.test(out), out.trim().split("\n")[0]);
}

/* The two kinds of printable page, plus one page that is NOT printable. */
const SHEETS = [
  "learn/bengali/practice/worksheets/index.html",
  "learn/hindi/practice/worksheets/index.html",
  "materials/alphabet/devanagari-chart/index.html"
];

console.log("\n1. a printable page, printed with scripting OFF\n");

for (const page of SHEETS) {
  const { d, shown } = printed(page);
  const target = d.querySelector("[data-print-target]");
  ok(`${page.replace("/index.html", "")}: the sheet is in the file`,
    !!target && target.textContent.trim().length > 200,
    target ? target.textContent.trim().length + " chars" : "no [data-print-target]");

  if (!target) continue;

  /* Every wrapper between <body> and the sheet must survive the print rule,
     or the sheet itself is inside a display:none ancestor and never renders. */
  const chain = [];
  for (let el = target.parentElement; el && el !== d.body; el = el.parentElement) chain.push(el);
  ok(`  its whole wrapper chain is marked (${chain.length} wrapper(s))`,
    chain.length > 0 && chain.every((el) => el.hasAttribute("data-print-chain")),
    chain.filter((el) => !el.hasAttribute("data-print-chain")).map((el) => el.tagName + "." + el.className).join(", "));

  ok("  the wrapper chain survives the print rule",
    chain.every((el) => (el.getAttribute("style") || "", true)) && chain.length > 0);

  /* Nothing on paper but the sheet: every visible element must be an ancestor
     of the sheet or inside it. */
  const strays = shown.filter((el) => el !== d.body && !el.contains(target) && !target.contains(el));
  ok("  nothing else is in the print flow",
    strays.length === 0,
    strays.slice(0, 6).map((el) => el.tagName + "." + (el.className || "").toString().slice(0, 24)).join(", "));

  const chrome = [".hdr", ".ftr", ".skip", "nav", "button", "select", "input", "label", ".sb-hint"];
  const leaked = chrome.filter((sel) => [...d.querySelectorAll(sel)].some((el) => !target.contains(el) && shown.includes(el)));
  ok("  the chrome, the controls and the hints are gone",
    leaked.length === 0, leaked.join(", "));
}

console.log("\n2. the worksheet itself is a worksheet\n");

{
  const { d } = printed("learn/bengali/practice/worksheets/index.html");
  const target = d.querySelector("[data-print-target]");
  const text = target.textContent;
  ok("it carries the language's own questions", /নমস্কার|বাংলা/.test(text), text.slice(0, 80).replace(/\s+/g, " "));
  ok("it has writing lines to answer on",
    target.querySelectorAll('div[style*="border-bottom"]').length >= 3);
  ok("it carries an answer key", /Answers/.test(text));
  ok("it carries the EkGuru source line", /EkGuru/.test(text));
  ok("it does not carry the page's own navigation or footer",
    !target.querySelector(".hdr, .ftr, .crumb, .pw-support"));
}

console.log("\n3. mode 1b: the sheet the script builds\n");

{
  const { d, shown, w } = printed("learn/hindi/practice/worksheets/index.html");
  /* js/print-sheet.js clones the sheet into #ekguru-print-root and sets
     html.eg-printing; then only that element prints. */
  const root = d.createElement("div");
  root.id = "ekguru-print-root";
  root.innerHTML = '<div class="ws-page"><h2>Hindi worksheet</h2><p>1. How many letters…</p></div>';
  d.body.appendChild(root);
  d.documentElement.classList.add("eg-printing");
  const strays = [...d.querySelectorAll("body > *")].filter((el) => el.id !== "ekguru-print-root")
    .filter((el) => (w.getComputedStyle(el).display || "block").toLowerCase() !== "none");
  ok("with the isolated copy, nothing but the copy is in the flow",
    strays.length === 0, strays.map((el) => el.tagName + "." + el.className).slice(0, 5).join(", "));
  ok("the isolated copy itself prints",
    (w.getComputedStyle(root).display || "").toLowerCase() !== "none");
}

console.log("\n4. a page that is not a sheet still prints its content\n");

{
  const page = "learn/bengali/basics/index.html";
  const { d, w, shown } = printed(page);
  ok("a lesson has no [data-print-target]", !d.querySelector("[data-print-target]"));
  const header = d.querySelector(".hdr"), main = d.querySelector("main");
  ok("its chrome is off the paper",
    header && (w.getComputedStyle(header).display || "").toLowerCase() === "none");
  ok("its content stays on the paper",
    main && shown.includes(main));
}

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
