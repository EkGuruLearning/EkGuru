#!/usr/bin/env node
/* ==========================================================================
   test-ad-policy.mjs — the ad script is only where the matrix says it may be

   AdSense rejected this site once for low-value content. The second
   submission must not also fail for a policy reason: an ad unit on a quiz a
   learner is mid-way through, or on the page that explains the ad cookies.

   Auto ads place themselves, so the only promise that can actually be kept is
   "the loader is not in that page at all" — which is what this checks, for
   every page, against data/monetization/google-monetization.json.

   Run:  node tools/test-ad-policy.mjs
   ========================================================================== */
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
process.chdir(ROOT);

let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) { pass++; console.log("  PASS  " + name); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};

const mon = JSON.parse(readFileSync("data/monetization/google-monetization.json", "utf8"));
const policy = mon.ad_policy || {};
const CLASSES = policy.classes || {};
const ALLOWED = new Set(policy.loader_allowed || []);
const EXCLUDED = mon.excluded_paths || [];

/* Pages, by the same rule the tool walks by: no build output (reports/ holds
   email previews), and the Google site-verification file is not a page (it has
   no <html> at all). */
const EXEMPT = (p) => p.startsWith("reports/") || /^google[a-z0-9]+\.html$/.test(p);
const allHtml = execFileSync("git", ["ls-files", "*.html"], { encoding: "utf8" })
  .split("\n").filter(Boolean);
const files = allHtml.filter((p) => !EXEMPT(p));
const read = (p) => readFileSync(p, "utf8");

const globRe = (pattern) => {
  let rx = pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&");
  rx = rx.split("**").join("\u0001").split("*").join("[^/]*").split("\u0001").join(".*");
  return new RegExp("^" + rx + "/?$");
};
const url = (rel) => "/" + rel;
const excluded = (u) => EXCLUDED.some((p) =>
  p.endsWith("/") ? (u === p || u.startsWith(p)) : u === p);
const classify = (u, html = "") => {
  for (const pattern of (CLASSES.ADMIN || {}).match || []) { if (globRe(pattern).test(u)) return "ADMIN"; }
  if (/<meta\b(?=[^>]*\bname=["']robots["'])(?=[^>]*\bcontent=["'][^"']*noindex)/i.test(html)) return "RESEARCH_REQUIRED";
  for (const name of ["TRANSACTIONAL", "UTILITY", "INTERACTIVE_LEARNING", "HIGH_CONTENT", "MEDIUM_CONTENT"]) {
    for (const pattern of (CLASSES[name] || {}).match || []) {
      if (pattern === "/" ? (u === "/" || u === "/index.html") : globRe(pattern).test(u)) return name;
    }
  }
  return "MEDIUM_CONTENT";
};

console.log("\n1. the policy is complete\n");

ok("every class the loader list names exists",
  [...ALLOWED].every((c) => c in CLASSES), [...ALLOWED].filter((c) => !(c in CLASSES)).join(", "));
ok("every route class has patterns; the noindex override is explicit",
  Object.entries(CLASSES).every(([n,c]) => Array.isArray(c.match) && (c.match.length || n === "RESEARCH_REQUIRED")));
ok("every class says why it exists",
  Object.values(CLASSES).every((c) => c.why));
ok("the interactive class may never load the loader",
  !ALLOWED.has("INTERACTIVE_LEARNING"));
ok("the legal pages are excluded twice over (class + excluded_paths)",
  ["/privacy/", "/terms/", "/disclaimer/", "/copyright/", "/cookie-policy/"]
    .every((p) => EXCLUDED.includes(p)) &&
  ["/privacy/", "/terms/", "/disclaimer/", "/copyright/", "/cookie-policy/"]
    .every((p) => classify(p) === "UTILITY"));
ok("money pages may not load the loader",
  ["/support/", "/join.html", "/contact/"].every((p) => !ALLOWED.has(classify(p))),
  ["/support/", "/join.html", "/contact/"].filter((p) => ALLOWED.has(classify(p))).join(", "));

console.log("\n2. every page agrees\n");

const rows = files.map((rel) => {
  const html = read(rel);
  const u = url(rel);
  const cls = classify(u, html);
  const m = html.match(/<html\b[^>]*data-ad-class="([^"]+)"/);
  return {
    rel, u, cls, declared: m && m[1],
    loader: /adsbygoogle\.js/.test(html),
    units: (html.match(/class="[^"]*adsbygoogle[^"]*"/g) || []).length,
    marks: (html.match(/ekguru:adsense:start/g) || []).length,
    may: ALLOWED.has(cls) && !excluded(u),
  };
});

const wrongClass = rows.filter((r) => r.declared !== r.cls);
ok(`every page states its own class (${rows.length} pages)`, wrongClass.length === 0,
  wrongClass.slice(0, 4).map((r) => `${r.rel}: ${r.declared} vs ${r.cls}`).join(", "));

const stray = rows.filter((r) => !r.may && r.loader);
ok("no page the policy excludes carries the ad loader", stray.length === 0,
  stray.slice(0, 6).map((r) => `${r.rel} (${r.cls})`).join(", "));

const strayUnits = rows.filter((r) => !r.may && r.units);
ok("no excluded page carries an ad unit", strayUnits.length === 0,
  strayUnits.slice(0, 6).map((r) => r.rel).join(", "));

const missing = rows.filter((r) => r.may && !r.loader);
ok(`every allowed page carries the loader (${rows.filter((r) => r.may).length} pages)`,
  missing.length === 0, missing.slice(0, 6).map((r) => r.rel).join(", "));

const double = rows.filter((r) => r.marks > 1);
ok("no page loads the account script twice", double.length === 0,
  double.slice(0, 6).map((r) => r.rel).join(", "));

const byClass = {};
for (const r of rows) byClass[r.cls] = (byClass[r.cls] || 0) + 1;
console.log("        classes: " + Object.entries(byClass).map(([c, n]) => `${c} ${n}`).join(", "));

console.log("\n3. the rest of the monetization setup\n");

ok("ads.txt names the publisher", read("ads.txt").includes(mon.publisher.ads_txt_id));
ok("the publisher id is configured but no loader is authorized while the runtime gate is closed",
  /^ca-pub-\d+$/.test(mon.publisher.adsense_client) && mon.runtime_gate.adsense_loader_enabled === false && rows.every((r) => !r.loader));
ok("robots.txt does not block AdsBot",
  !/User-agent:\s*AdsBot/i.test(read("robots.txt")));
ok("consent is a certified-CMP question, not a home-made banner",
  /certified/i.test(mon.consent.requirement) && /CMP/i.test(mon.consent.requirement));
ok("the local privacy UI cannot grant advertising consent",
  /ADVERTISING_AVAILABLE\s*=\s*false/.test(read("js/cookie-consent.js")) && /id=["']cc-advertising["'][^>]*disabled/.test(read("js/cookie-consent.js")));
ok("no page anywhere sets a cookie",
  files.every((f) => !/document\.cookie\s*=/.test(read(f))));

const scripts = ["js/analytics.js", "js/cookie-consent.js", "js/print-sheet.js", "js/copywatch.js"];
ok("no script sets a cookie either",
  scripts.every((f) => !/document\.cookie\s*=/.test(read(f))));

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
