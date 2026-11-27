#!/usr/bin/env node
/* =========================================================================
   SHEET-ONLY GURU BAKE  (17 Nov 2026)

   Owner rule: the Google Sheet is the source of truth and an approved guru
   is visible — on the FIRST paint too, not only after the browser manages
   to fetch Google's CSV endpoint (which answers HTTP 500 for stretches).

   tools/sheetsync.js therefore bakes every sheet row that says approved=yes
   (and is not active=no) into window.EKGURU_SHEET_TUTORS even when the id
   has no js/tutors/<id>.js file, and js/tutors-data.js appends those to the
   roster after the registry. This test pins the rule and its privacy edge:

     · approved=yes, unregistered          → baked, sheetOnly=true
     · approved blank, unregistered        → NOT baked (never written to git)
     · approved=yes but active=no          → NOT baked
     · approved=yes but no name            → NOT baked
     · notification_email / email          → never in the public file
     · an id that IS in the registry       → never duplicated by the bake
     · tools/lib/site-data.js (the build)  → sees the same roster the browser gets

   The test runs sheetsync --offline against a temp copy of tests/fixtures,
   then restores js/tutors/_overrides.js byte-for-byte.
   ========================================================================= */
import { readFileSync, writeFileSync, cpSync, rmSync, mkdtempSync } from "fs";
import { execFileSync } from "child_process";
import { join } from "path";
import { tmpdir } from "os";
import { createRequire } from "module";
import vm from "vm";

const ROOT = new URL(import.meta.url).pathname.replace(/\/tests\/[^/]+\/[^/]+$/, "");
const require = createRequire(import.meta.url);
const sheetFetch = require(join(ROOT, "tools", "sheet-fetch.js"));
const siteData = require(join(ROOT, "tools", "lib", "site-data.js"));

let passed = 0, failed = 0;
function check(name, cond, detail) {
  if (cond) { passed++; console.log("  ok    " + name); }
  else { failed++; console.log("  FAIL  " + name + (detail ? "  — " + detail : "")); }
}
function tsvEncode(rows) {
  return rows.map((r) => r.map((c) =>
    /[\t"\n\r]/.test(c) ? '"' + String(c).replace(/"/g, '""') + '"' : c
  ).join("\t")).join("\n") + "\n";
}

const OVERRIDES = join(ROOT, "js", "tutors", "_overrides.js");
const before = readFileSync(OVERRIDES, "utf8");

const PRIVATE_MAIL = "private.guru@example.net";
const PRIVATE_LEGACY = "legacy.inbox@example.net";

function fixtures() {
  const dir = mkdtempSync(join(tmpdir(), "ekguru-sheet-only-"));
  cpSync(join(ROOT, "tests", "fixtures"), dir, { recursive: true });
  const p = join(dir, "tutors.tsv");
  const rows = sheetFetch.parseTSV(readFileSync(p, "utf8"));
  const head = sheetFetch.headerOf(rows);
  if (head.indexOf("approved") === -1) { rows[0].push("approved"); head.push("approved"); }
  const col = (name) => head.indexOf(name.toLowerCase());
  const mk = (cells) => {
    const r = new Array(head.length).fill("");
    Object.keys(cells).forEach((k) => { if (col(k) > -1) r[col(k)] = cells[k]; });
    return r;
  };
  rows.push(mk({ id: "new-guru", active: "yes", name: "New Guru", subject: "Hindi", priceusd: "7",
    lessonlength: "50 min", headline: "Patient Hindi tutor", city: "Jaipur, India", country: "India",
    email: PRIVATE_LEGACY, notification_email: PRIVATE_MAIL, about: "Namaste, I teach Hindi.",
    approved: "yes" }));
  rows.push(mk({ id: "shy-guru", active: "yes", name: "Shy Guru", subject: "Hindi", priceusd: "5",
    notification_email: PRIVATE_MAIL, approved: "" }));
  rows.push(mk({ id: "gone-guru", active: "no", name: "Gone Guru", subject: "Hindi", priceusd: "5",
    approved: "yes" }));
  rows.push(mk({ id: "nameless-guru", active: "yes", name: "", subject: "Hindi", approved: "yes" }));
  rows.push(mk({ id: "Bad Id!", active: "yes", name: "Bad Id", subject: "Hindi", approved: "yes" }));
  /* a registry id flagged approved=yes must keep its normal (override) path */
  for (const r of rows) if (r[0] === "sushila-g") { r[col("active")] = "yes"; r[col("approved")] = "yes"; }
  writeFileSync(p, tsvEncode(rows));
  return dir;
}

try {
  const dir = fixtures();
  try {
    execFileSync("node", ["tools/sheetsync.js", "--offline", dir], { cwd: ROOT, stdio: "pipe" });
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }

  const out = readFileSync(OVERRIDES, "utf8");
  const sandbox = { window: {} }; sandbox.window = sandbox;
  vm.runInNewContext(out, sandbox);
  const baked = sandbox.EKGURU_SHEET_TUTORS || [];
  const ids = baked.map((t) => t.id);
  const over = sandbox.EKGURU_SHEET_OVERRIDES || {};

  console.log("sheetsync --offline (fixture + 5 unregistered rows)");
  check("EKGURU_SHEET_TUTORS is written", Array.isArray(sandbox.EKGURU_SHEET_TUTORS));
  check("approved=yes unregistered row IS baked", ids.includes("new-guru"), ids.join(","));
  check("approved blank unregistered row is NOT baked", !ids.includes("shy-guru"));
  check("approved=yes + active=no is NOT baked", !ids.includes("gone-guru"));
  check("approved=yes without a name is NOT baked", !ids.includes("nameless-guru"));
  check("unsafe id is NOT baked", !ids.some((i) => /bad/i.test(i)));
  check("registry id is NOT duplicated into the sheet-only list", !ids.includes("sushila-g"));
  check("registry id still goes through EKGURU_SHEET_OVERRIDES", !!over["sushila-g"]);
  const ng = baked.find((t) => t.id === "new-guru") || {};
  check("baked record carries sheetOnly=true", ng.sheetOnly === true);
  check("baked record has name/price/about from the sheet", ng.name === "New Guru" && ng.priceUSD === 7 && Array.isArray(ng.about));
  check("photo-less row gets the neutral placeholder + noPhoto", ng.noPhoto === true && /placeholder-tutor/.test(ng.photo || ""));
  check("notification_email is NOT in the public file", out.indexOf(PRIVATE_MAIL) === -1);
  check("legacy email is NOT in the public file", out.indexOf(PRIVATE_LEGACY) === -1);
  check("no baked record carries an email/notification_email key",
    baked.every((t) => !("email" in t) && !("notification_email" in t)));

  console.log("js/tutors-data.js + tools/lib/site-data.js");
  const site = siteData.loadSite();
  const roster = site.tutors.map((t) => t.id);
  check("the build roster includes the sheet-only guru", roster.includes("new-guru"), roster.join(","));
  check("the sheet-only guru is public (not hidden)", site.publicTutors.some((t) => t.id === "new-guru"));
  check("the sheet-only guru comes AFTER the registry", roster.indexOf("new-guru") > roster.indexOf("sushila-g"));
  check("no duplicate ids in the roster", new Set(roster).size === roster.length);
  const t = site.tutors.find((x) => x.id === "new-guru") || {};
  check("defaults applied (subject, lessonLength present)", !!t.subject && !!t.lessonLength);
  const siteMail = (site.site && site.site.email) || "";
  check("no whatsapp / private mail on the assembled sheet-only guru (email = site inbox fallback only)",
    !t.whatsapp && !t.notification_email && (!t.email || t.email === siteMail), JSON.stringify({ w: t.whatsapp, e: t.email }));
  check("sheetOnly flag survives assembly", t.sheetOnly === true);
} catch (e) {
  failed++;
  console.log("  FAIL  " + String(e.stack || e.message).slice(0, 1500));
} finally {
  writeFileSync(OVERRIDES, before);
  const restored = readFileSync(OVERRIDES, "utf8") === before;
  console.log("\njs/tutors/_overrides.js restored: " + (restored ? "byte-for-byte" : "MISMATCH"));
  if (!restored) failed++;
}

console.log("\n" + passed + " passed, " + failed + " failed");
process.exit(failed ? 1 : 0);
