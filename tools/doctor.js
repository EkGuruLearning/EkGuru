#!/usr/bin/env node
/* EkGuru — DOCTOR. One command to run the whole health chain and leave the
   dashboard honest:

       node tools/doctor.js

   Runs, in order:
     1. node tools/seocheck.js          -> reports/seo.json
     2. node tools/privacy.js --sheets --live --json  -> reports/privacy-scan.json
     3. node tools/gate.js              -> reports/doctor.json
     4. node tools/adminstats.js        -> js/admin-stats.js

   The admin dashboard (admin.html) reads js/admin-stats.js, so after this
   command every health figure it shows is real and current.
*/
"use strict";
const { spawnSync } = require("child_process");
const path = require("path");
const TOOLS = path.join(__dirname);

const steps = [
  { label: "SEO check",        cmd: process.execPath, args: [path.join(TOOLS, "seocheck.js")] },
  { label: "Privacy scan",     cmd: process.execPath, args: [path.join(TOOLS, "privacy.js"), "--sheets", "--live", "--json"] },
  { label: "Doctor gate",      cmd: process.execPath, args: [path.join(TOOLS, "gate.js")] },
  { label: "Admin stats",      cmd: process.execPath, args: [path.join(TOOLS, "adminstats.js")] },
];

let failed = 0;
for (const s of steps) {
  console.log(`\n━━━ ${s.label} ━━━`);
  const r = spawnSync(s.cmd, s.args, { stdio: "inherit" });
  if (r.status !== 0) { failed++; console.log(`✗ ${s.label} exited ${r.status}`); }
}

console.log(`\n══════════════════════════════════════════`);
console.log(failed === 0 ? "Doctor complete — all steps ran." : `Doctor complete with ${failed} failing step(s).`);
console.log("Dashboard now reads js/admin-stats.js. See reports/ for evidence.");
