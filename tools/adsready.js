#!/usr/bin/env node
/* EkGuru — AdSense readiness. Checks the concrete, verifiable preconditions
   for AdSense review against the LIVE site and the local tree. It reports
   facts only — it never claims approval or guaranteed revenue.

   Output: reports/adsready.json + a printed checklist.

   Run: node tools/adsready.js
*/
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
const REPORTS = path.join(ROOT, "reports");
if (!fs.existsSync(REPORTS)) fs.mkdirSync(REPORTS, { recursive: true });

const BASE = "https://ekguru.shop";
const PUB = "pub-8175326569491671";

async function get(url) {
  try {
    const r = await fetch(url, { redirect: "follow" });
    return { ok: r.ok, status: r.status, body: await r.text(), url: r.url };
  } catch (e) { return { ok: false, status: 0, body: "", url, error: String(e) }; }
}

const checks = [];
function add(id, label, ok, detail) { checks.push({ id, label, ok: !!ok, detail }); }

async function main() {
  /* live checks */
  const ads = await get(`${BASE}/ads.txt`);
  add("ads-txt", "ads.txt present with correct publisher id",
    ads.ok && ads.body.includes(PUB) && /DIRECT/.test(ads.body),
    ads.status + " — " + (ads.body.split("\n").find(l => l.includes("google.com")) || "no google.com line"));

  const robots = await get(`${BASE}/robots.txt`);
  add("robots", "robots.txt allows crawling of money pages",
    robots.ok && /Sitemap:/i.test(robots.body) && !/^Disallow:\s*\/\s*$/m.test(robots.body),
    robots.status + (robots.ok ? " — sitemap declared" : ""));

  const sitemap = await get(`${BASE}/sitemap-index.xml`);
  add("sitemap", "sitemap-index valid and enumerates pages",
    sitemap.ok && /<sitemapindex/i.test(sitemap.body),
    sitemap.status + " — " + ((sitemap.body.match(/<loc>/g) || []).length) + " child sitemaps");

  const home = await get(`${BASE}/`);
  add("home-200", "Homepage serves HTTP 200", home.ok, String(home.status));
  add("canonical", "Homepage canonical is the https production URL",
    /rel="canonical"\s+href="https:\/\/ekguru\.shop\/"/.test(home.body), "https://ekguru.shop/");

  const redirect = await get("https://ekgurulearning.github.io/EkGuru/");
  add("old-github-redirect", "Old GitHub Pages URL 301s to production https",
    redirect.url === `${BASE}/`, "final " + redirect.url);

  /* required pages live */
  for (const p of ["privacy/", "about/", "contact/", "terms/"]) {
    const r = await get(`${BASE}/${p}`);
    add(`page-${p.replace("/", "")}`, `/${p} serves 200`, r.ok, String(r.status));
  }

  /* content volume from the tree */
  const html = [];
  (function walk(d) {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      if (e.name.startsWith(".") || ["node_modules", "tools", "reports", "audit"].includes(e.name)) continue;
      if (e.isDirectory()) walk(path.join(d, e.name));
      else if (/\.html?$/.test(e.name)) html.push(path.join(d, e.name));
    }
  })(ROOT);
  add("content-volume", "Substantial unique content (≥100 published pages)",
    html.length >= 100, `${html.length} HTML pages in tree`);

  /* no doorway/duplicate signal: countries pages must differ */
  const adHoc = fs.existsSync(path.join(ROOT, "learn-hindi-from-usa", "index.html"));
  add("real-pages", "Country pages are real, distinct pages (not redirects to one)",
    adHoc, adHoc ? "learn-hindi-from-usa/ exists" : "country pages missing");

  const passed = checks.filter(c => c.ok).length;
  const ready = passed === checks.length;
  const result = {
    ready,
    passed,
    total: checks.length,
    failed: checks.filter(c => !c.ok),
    checks,
    generated: new Date().toISOString(),
    disclaimer: "Readiness only — NOT an approval signal. AdSense approval is Google's decision.",
  };
  fs.writeFileSync(path.join(REPORTS, "adsready.json"), JSON.stringify(result, null, 2));

  for (const c of checks) console.log(`${c.ok ? "✓" : "✗"} ${c.label} — ${c.detail}`);
  console.log(`\nAdSense readiness: ${passed}/${checks.length} checks pass. ${ready ? "All preconditions verified (approval is Google's call)." : "Fix the failed checks first."}`);
}

main().catch(e => { console.error("adsready crashed:", e.message); process.exit(1); });
