#!/usr/bin/env node
/* ==========================================================================
   test-print-sheet-dom.mjs — what the printer actually receives

   Prakash: "print worksheet pura page hi print karti hai, par humein sirf
   worksheet hi print karni hai."

   The stylesheet test (tools/test-print-sheets.mjs) proves the rules exist.
   This one runs the pages in jsdom and looks at the element the browser would
   print: build a worksheet, ask js/print-sheet.js for the printed copy, and
   check that the copy is the sheet — the questions, the watermark, the tagline
   — and not the header, the intro, the controls, the notes or the footer.

   Run:  node tools/test-print-sheet-dom.mjs
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

function open(page, scripts) {
  const dom = new JSDOM(read(page), {
    url: "https://ekguru.shop/" + page.replace(/index\.html$/, ""),
    runScripts: "outside-only"   // window.eval runs inside the page, not in Node
  });
  const w = dom.window;
  w.EKGURU_SHEET_SETTINGS = { tagline: "One Student. One Goal. One Guru." };
  for (const s of scripts) w.eval(read(s));
  /* jsdom is still on readyState "loading" at this point, and the tools boot
     on DOMContentLoaded. Fire it so the app mounts like it does in a browser. */
  w.document.dispatchEvent(new w.Event("DOMContentLoaded", { bubbles: true }));
  return dom;
}

console.log("\n1. a worksheet, printed from the page that builds it\n");

{
  const page = "learn/bengali/practice/worksheets/index.html";
  const dom = open(page, ["js/bengali-quiz-bank.js", "js/hindi-tools.js", "js/print-sheet.js"]);
  const w = dom.window, d = w.document;

  ok("the builder mounted", !!d.querySelector("#ws-app #w-make"));

  /* Nothing built yet: Ctrl+P must not print a page of controls, and must not
     print blank paper either — the script builds the worksheet the same way
     the Print button does. */
  const built = w.EKGURU_PRINT_SHEET.build();
  ok("printing before pressing Make builds a worksheet", built && !!d.querySelector(".ws-page"));

  const root = d.getElementById("ekguru-print-root");
  ok("the printed copy is one element (#ekguru-print-root)", !!root);
  ok("the page is marked as printing", d.documentElement.classList.contains("eg-printing"));
  ok("the printed copy is watermarked", root && root.getAttribute("data-watermark") === "EkGuru");

  const questions = root ? root.querySelectorAll(".ws-page p").length : 0;
  ok(`the questions are on the sheet (${questions} lines)`, questions >= 5);

  const text = root ? root.textContent : "";
  ok("the printed copy carries the tagline", /One Student\. One Goal\. One Guru\./.test(text));
  ok("the printed copy carries the source and the date",
    /ekguru\.shop/.test(text) && /printed \d{4}-\d{2}-\d{2}/.test(text));
  ok("the printed copy does not carry the site header",
    !root.querySelector(".hdr, .skip, .ftr"));
  ok("the printed copy does not carry the page around the sheet",
    !root.querySelector(".crumb, .sb-chapter, .lede, .note, .pw-support, .pw-next"));
  ok("no controls are printed", root.querySelectorAll("button, select, input").length === 0);

  w.EKGURU_PRINT_SHEET.clear();
  ok("after printing, the page is put back",
    !d.getElementById("ekguru-print-root") && !d.documentElement.classList.contains("eg-printing"));
  ok("the worksheet itself survives for the reader", !!d.querySelector("#ws-app .ws-page"));
}

console.log("\n2. a printable guide\n");

{
  const page = "materials/alphabet/devanagari-chart/index.html";
  const dom = open(page, ["js/print-sheet.js"]);
  const w = dom.window, d = w.document;
  w.EKGURU_PRINT_SHEET.build();
  const root = d.getElementById("ekguru-print-root");
  ok("the guide is cloned for print", !!root);
  const text = root ? root.textContent : "";
  ok("the guide's own heading prints", /Devanagari/.test(text));
  ok("the shell header does not", !root.querySelector(".hdr, .skip, .ftr"));
  ok("the Print button itself is not printed", root.querySelectorAll("button").length === 0);
  w.EKGURU_PRINT_SHEET.clear();
}

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
