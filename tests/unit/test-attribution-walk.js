"use strict";
const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { walk } = require("../../tools/lib/attribution-walk");

const root = fs.mkdtempSync(path.join(os.tmpdir(), "ekguru-attribution-"));
try {
  const fixtures = ["index.html", "learn/hindi/index.html", "js/reader.js",
    "learn/A-Manually/public.html", "A-Manually/pack/preview.html",
    ".artifacts/pack/preview.html", "docs/notes.html"];
  for (const file of fixtures) {
    const target = path.join(root, file);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, "fixture");
  }
  assert.deepStrictEqual(walk(root).map(p => path.relative(root, p).split(path.sep).join("/")).sort(),
    ["index.html", "js/reader.js", "learn/A-Manually/public.html", "learn/hindi/index.html"].sort());
  console.log("PASS attribution walker: private root uploads excluded; public pages and JS retained");
} finally {
  fs.rmSync(root, { recursive: true, force: true });
}
