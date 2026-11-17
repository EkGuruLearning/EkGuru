#!/usr/bin/env node
/* EkGuru — PUBLIC SURFACE GATE  (node tools/test-public-surface.mjs)

   The website is a public GitHub repo deployed to a public host, so the
   only real protection is "it is not in the public set". This gate builds
   the exact set tools/build-public-dist.py would publish and refuses:

     1. any private directory or file inside it (tools/, reports/, csv/ …)
     2. any e-mail address that is not the site's own public contact
        (tutor / student addresses must live ONLY in the Google Sheet)
     3. phone-number-looking strings in tutor data files
     4. any secret-shaped string (API keys, tokens, private keys)
     5. the retired sheet exports (live-sheets/, tutors-sheet.csv) in git
     6. js/tutors/*.js and the generated _overrides.js carrying a non-empty
        email / notification_email / formKey / phone value
     7. the public config pointing at a review CSV that holds contact
        columns (reviews_pending must never be published as a sheet)

   Exit 1 on any failure. Runs in CI (ci.yml) and tools/build-all.py check. */
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
let pass = 0, fail = 0;
function ok(cond, label, extra) {
  if (cond) { pass++; console.log("PASS  " + label); }
  else { fail++; console.log("FAIL  " + label + (extra ? "  ->  " + String(extra).slice(0, 300) : "")); }
}

/* ---- the public set ---- */
const out = fs.mkdtempSync(path.join(os.tmpdir(), "ekguru-public-"));
let built = "";
try {
  built = execFileSync("python3", [path.join(ROOT, "tools/build-public-dist.py"), "--check", "--out", out], { encoding: "utf8" });
  ok(/^ok\s+public deploy set/m.test(built), "build-public-dist --check passes (sitemap URLs + sw precache all present)", built);
} catch (e) {
  ok(false, "build-public-dist --check passes", (e.stdout || "") + (e.stderr || ""));
}

const PRIVATE_TOP = ["tools", "tests", "src", "reports", "docs", "research", "apps-script", "server", "csv", "live-sheets", ".github", "node_modules"];
for (const d of PRIVATE_TOP) ok(!fs.existsSync(path.join(out, d)), "public set has no /" + d + "/");
for (const f of ["package.json", "package-lock.json", "playwright.config.mjs", "FINAL_REPORT.md", "tutors-sheet.csv", ".gitignore"]) {
  ok(!fs.existsSync(path.join(out, f)), "public set has no /" + f);
}
for (const f of ["index.html", "CNAME", ".nojekyll", "robots.txt", "ads.txt", "sw.js", "js/site-config.js", "js/tutors/_overrides.js", "data/practice-flags.json", "tutor/sushila-g/index.html"]) {
  ok(fs.existsSync(path.join(out, f)), "public set keeps /" + f);
}

/* ---- walk the public set ---- */
const TEXT_EXT = new Set([".html", ".js", ".mjs", ".css", ".json", ".xml", ".txt", ".webmanifest", ".svg", ".csv", ".tsv", ".md"]);
const files = [];
(function walk(dir) {
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p);
    else if (TEXT_EXT.has(path.extname(name).toLowerCase())) files.push(p);
  }
})(out);

const PUBLIC_EMAILS = new Set([
  "ekgurulearning@gmail.com",          // the site's contact inbox (public by design)
  "support@ekguru.shop",               // public support alias
  "ekgurulearning+relay2@gmail.com",   // site relay (routing, not a person)
  "ekgurulearning+student-test@gmail.com", // documented test inbox
  "ops@ekguru.com",                    // operator mailbox named in legal pages
  "pw@ekguru.shop",                    // placeholder in the booking form copy
]);
const EMAIL_RE = /[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}/g;
const EXAMPLE_HOST = /(^|\.)(example|test|invalid|localhost)(\.|$)|\.local$|^x\.com$|^y\.com$|^b\.co$|attacker\./i;
const SECRET_PATTERNS = [
  [/\bAKIA[0-9A-Z]{16}\b/, "AWS access key"],
  [/\bAIza[0-9A-Za-z_-]{35}\b/, "Google API key"],
  [/\bsk-[A-Za-z0-9_-]{24,}\b/, "sk- style key"],
  [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, "private key block"],
  [/\brzp_live_[A-Za-z0-9]{10,}\b/, "Razorpay LIVE key id"],
  [/\bghp_[A-Za-z0-9]{30,}\b/, "GitHub token"],
  [/\bxox[baprs]-[A-Za-z0-9-]{10,}\b/, "Slack token"],
  [/EK_ADMIN_TOKEN\s*[:=]\s*["'][^"'\s]{8,}["']/, "admin token value"],
  [/MAILER_SHARED_TOKEN\s*[:=]\s*["'][^"'\s]{8,}["']/, "mailer token value"],
];

const strangeEmails = new Map();
const secrets = [];
for (const p of files) {
  const rel = path.relative(out, p).replace(/\\/g, "/");
  let txt;
  try { txt = fs.readFileSync(p, "utf8"); } catch (e) { continue; }
  for (const m of txt.matchAll(EMAIL_RE)) {
    const e = m[0].toLowerCase();
    const host = e.split("@")[1];
    if (PUBLIC_EMAILS.has(e)) continue;
    if (EXAMPLE_HOST.test(host)) continue;
    if (/\.(png|jpg|jpeg|svg|webp|css|js|json|html|md|xml)$/.test(e)) continue; // foo@2x.png style
    if (!strangeEmails.has(e)) strangeEmails.set(e, rel);
  }
  for (const [re, name] of SECRET_PATTERNS) {
    if (re.test(txt)) secrets.push(name + " in " + rel);
  }
}
/* A documented allowance: the three tutor template files carry a commented
   EXAMPLE address ("replace with HER address, e.g. …"). Those must stay
   empty in the live `email:` field — checked separately below. */
const TEMPLATE_EXAMPLES = new Set(["hemlata.hindi@gmail.com", "sushila.hindi@gmail.com", "tara.hindi@gmail.com", "somerandomstudent99@gmail.com", "nekgurulearning@gmail.com"]);
const leaks = [...strangeEmails].filter(([e]) => !TEMPLATE_EXAMPLES.has(e));
ok(leaks.length === 0, "no personal e-mail address anywhere in the public set", leaks.map(([e, f]) => e + " (" + f + ")").join(", "));
ok(secrets.length === 0, "no secret-shaped string in the public set", secrets.join(", "));

/* ---- tutor data: contact fields must be empty in every committed file ---- */
const tutorsDir = path.join(ROOT, "js/tutors");
const contactKeys = ["email", "notification_email", "notificationEmail", "formKey", "phone", "whatsapp", "mobile"];
const nonEmpty = [];
for (const f of fs.readdirSync(tutorsDir)) {
  if (!f.endsWith(".js")) continue;
  const txt = fs.readFileSync(path.join(tutorsDir, f), "utf8");
  for (const k of contactKeys) {
    const re = new RegExp('(?:^|[\\s,{])"?' + k + '"?\\s*:\\s*"([^"]*)"', "g");
    for (const m of txt.matchAll(re)) {
      const v = m[1].trim();
      if (!v) continue;
      if (PUBLIC_EMAILS.has(v.toLowerCase())) continue; // the site's own inbox (settings tab), not a person
      /* formKey is a FormSubmit alias (documented as safe to publish) — but a
         value with an @ is an address and never allowed. */
      if (k === "formKey" && !v.includes("@")) continue;
      nonEmpty.push(f + " " + k + "=" + v);
    }
  }
}
ok(nonEmpty.length === 0, "js/tutors/*.js (incl. generated _overrides.js) carry no email / phone / contact value", nonEmpty.join("; "));

const phoneRe = /(?:\+91[\s-]?)?\b[6-9]\d{4}[\s-]?\d{5}\b/;
const phoneHits = [];
for (const f of fs.readdirSync(tutorsDir)) {
  if (!f.endsWith(".js")) continue;
  const txt = fs.readFileSync(path.join(tutorsDir, f), "utf8").replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/[^\n]*/g, "");
  if (phoneRe.test(txt)) phoneHits.push(f);
}
ok(phoneHits.length === 0, "no Indian-mobile-looking number in tutor data", phoneHits.join(", "));

/* ---- retired exports are gone from git ---- */
const tracked = execFileSync("git", ["ls-files"], { cwd: ROOT, encoding: "utf8" }).split("\n");
ok(!tracked.some((f) => f.startsWith("live-sheets/")), "live-sheets/ is not tracked in git");
ok(!tracked.includes("tutors-sheet.csv"), "tutors-sheet.csv is not tracked in git");
ok(!tracked.some((f) => /\.local\.(csv|json)$/.test(f) || /deploy-secrets/.test(f)), "no *.local.csv / *.local.json / deploy-secrets file is tracked");

/* ---- public config never publishes the pending-review tab as a sheet ---- */
const cfg = fs.readFileSync(path.join(ROOT, "js/site-config.js"), "utf8");
const csvUrls = [...cfg.matchAll(/(?:csvUrl|fallbackCsvUrl|url)\s*:\s*"([^"]*)"/g)].map((m) => m[1]).filter(Boolean);
ok(!csvUrls.some((u) => /gid=176535552\b/.test(u)), "site-config never points a public CSV at reviews_pending (gid 176535552)", csvUrls.filter((u) => /176535552/.test(u)).join(", "));
const feedUrl = (cfg.match(/feed:\s*\{[\s\S]*?url:\s*"([^"]*)"/) || [])[1] || "";
ok(/^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(feedUrl), "feed.url is an Apps Script /exec (the only reader of the tutors tab; it strips private columns)", feedUrl);

/* ---- Apps Script: private columns are stripped, token comes from properties ---- */
const gs = fs.readFileSync(path.join(ROOT, "apps-script/Unified.gs"), "utf8");
ok(/FEED_PRIVATE_EXACT[\s\S]*notification_email/.test(gs) && /FEED_PRIVATE_PATTERN\s*=\s*\/.*phone/.test(gs), "Unified.gs strips notification_email / phone-like columns before the browser sees them");
ok(/getScriptProperties\(\)\.getProperty\("EK_ADMIN_TOKEN"\)/.test(gs) && !/EK_ADMIN_TOKEN\s*[:=]\s*"[^"]{6,}"/.test(gs), "Unified.gs admin token is read from Script Properties, never hard-coded");

/* ---- the workflow publishes _site, not the repo root ---- */
const wf = fs.readFileSync(path.join(ROOT, ".github/workflows/pages.yml"), "utf8");
ok(/build-public-dist\.py --out _site/.test(wf) && /upload-pages-artifact/.test(wf) && /path:\s*_site/.test(wf), "pages.yml uploads _site built by build-public-dist.py");

fs.rmSync(out, { recursive: true, force: true });
console.log("\n" + pass + " passed, " + fail + " failed");
if (fail) process.exit(1);
console.log("PUBLIC SURFACE GATE PASSED — the deploy set is the website only; no contact data, no secrets.");
