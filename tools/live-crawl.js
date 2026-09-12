#!/usr/bin/env node
/* EkGuru — LIVE reachability + URL inventory. Walks the local tree, maps
   every HTML page to its production URL, then requests each one against
   https://ekguru.shop/ and records the HTTP status.

   Outputs:
     reports/url-inventory.json     { base, total, urls[], generated }
     reports/live-reachability.json { total, ok, redirects, missing, results[], generated }

   Run: node tools/live-crawl.js   (uses ~10 concurrent requests)
*/
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
const REPORTS = path.join(ROOT, "reports");
if (!fs.existsSync(REPORTS)) fs.mkdirSync(REPORTS, { recursive: true });

const BASE = "https://ekguru.shop";
const CONC = 10;

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".") && e.name !== ".nojekyll") continue;
    if (["node_modules", "tools", "reports", "audit", ".git"].includes(e.name)) continue;
    if (e.isDirectory()) walk(path.join(dir, e.name), out);
    else if (/\.html?$/.test(e.name)) out.push(path.join(dir, e.name));
  }
  return out;
}

const files = walk(ROOT, []);
const rel = p => path.relative(ROOT, p).split(path.sep).join("/");
const urls = files.map(f => {
  const r = rel(f);
  if (r === "index.html") return BASE + "/";
  if (r === "admin.html") return BASE + "/admin.html";
  return BASE + "/" + r.replace(/index\.html$/, "");
});

/* include non-HTML deploy-critical paths */
const extras = [
  BASE + "/robots.txt", BASE + "/ads.txt", BASE + "/sitemap-index.xml",
  BASE + "/js/site-config.js", BASE + "/js/sheet.js", BASE + "/js/mailer.js",
  BASE + "/js/tutors/_overrides.js", BASE + "/css/style.min.css",
  BASE + "/images/sushila.jpg", BASE + "/images/placeholder-tutor.jpg",
];

const inventory = { base: BASE, totalHtml: urls.length, urls: [...urls, ...extras], generated: new Date().toISOString() };
fs.writeFileSync(path.join(REPORTS, "url-inventory.json"), JSON.stringify(inventory, null, 2));

async function main() {
  const results = [];
  const queue = [...urls, ...extras];
  let i = 0;
  async function worker() {
    while (i < queue.length) {
      const u = queue[i++];
      try {
        const ctrl = new AbortController();
        const to = setTimeout(() => ctrl.abort(), 20000);
        const r = await fetch(u, { redirect: "follow", signal: ctrl.signal });
        clearTimeout(to);
        const final = r.url;
        const redirect = final !== u ? final : null;
        results.push({ url: u, status: r.status, ok: r.status === 200, redirect });
      } catch (e) {
        results.push({ url: u, status: 0, ok: false, error: String(e.message || e) });
      }
      if (results.length % 100 === 0) process.stderr.write(`  ${results.length}/${queue.length}\n`);
    }
  }
  await Promise.all(Array.from({ length: CONC }, worker));

  results.sort((a, b) => (a.url < b.url ? -1 : 1));
  const ok = results.filter(r => r.ok).length;
  const redirects = results.filter(r => r.redirect).length;
  const missing = results.filter(r => !r.ok);
  const report = {
    total: results.length, ok, redirects, missing: missing.length,
    results, generated: new Date().toISOString(),
  };
  fs.writeFileSync(path.join(REPORTS, "live-reachability.json"), JSON.stringify(report, null, 2));

  console.log(`Live reachability: ${ok}/${results.length} OK, ${redirects} redirects, ${missing.length} not-200`);
  for (const m of missing) console.log(`  ✗ ${m.url} → ${m.status || m.error}`);
  console.log(`  (details in reports/live-reachability.json and reports/url-inventory.json)`);
}

main().catch(e => { console.error("live-crawl crashed:", e.message); process.exit(1); });
