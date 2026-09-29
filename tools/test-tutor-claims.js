#!/usr/bin/env node
/* Site-level tutor claims gate (AdSense plan D-22 / S-29, 29 Sep 2026).

   EkGuru does not verify tutors' first language, and every tutor page says
   so ("EkGuru has not independently verified every statement"). A site-level
   sentence that calls all tutors "native speakers" or "verified" therefore
   contradicts the site's own disclosure. Tutor-provided headlines (e.g. a
   tutor describing herself as a "Native Hindi Tutor") are the tutor's own,
   attributed statement and are NOT checked here.

   Scans every public .html file plus feed.xml and llms.txt.
   Exit 0 = clean, 1 = a site-level claim came back. */
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
const SKIP = new Set([".git", "node_modules", "reports", "docs", "data", "tools", "tests", "Arena latest command  arena"]);
const BANNED = [
  /tutors are native hindi speakers/i,
  /lessons with native speakers/i,
  /you get a native speaker/i,
  /verified native hindi tutors/i,
  /local currency, native tutors/i,
  /will i actually speak with a native speaker/i,
];
const files = [];
(function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    if (e.isDirectory()) { if (!SKIP.has(e.name)) walk(path.join(d, e.name)); }
    else if (e.name.endsWith(".html")) files.push(path.join(d, e.name));
  }
})(ROOT);
files.push(path.join(ROOT, "feed.xml"), path.join(ROOT, "llms.txt"));
let bad = 0;
for (const f of files) {
  if (!fs.existsSync(f)) continue;
  const t = fs.readFileSync(f, "utf8").replace(/\s+/g, " ");
  for (const re of BANNED) {
    if (re.test(t)) { bad++; console.log(`FAIL  ${path.relative(ROOT, f)}  →  ${re}`); }
  }
}
console.log(bad ? `\n${bad} site-level tutor claim(s) found` : `PASS  no site-level native/verified tutor claims in ${files.length} files`);
process.exit(bad ? 1 : 0);
