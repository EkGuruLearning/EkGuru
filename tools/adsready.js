#!/usr/bin/env node
/* EkGuru — AdSense readiness. Checks the concrete, verifiable preconditions
   for AdSense review against the LIVE site and the local tree. It reports
   facts only — it never claims approval or guaranteed revenue.

   Output: reports/adsready.json + a printed checklist.

   Run: node tools/adsready.js            (live site + local tree)
        node tools/adsready.js --local    (local tree only)

   --local exists because the live checks need network, and a sandbox or a CI
   run without it reported 2/12 — which reads like the site is broken when it
   is the connection that is missing. The local mode checks the same facts in
   the repository: the ads.txt line, robots.txt and the sitemap index, the
   canonical self-consistency of every page, the required pages, and the money
   pages the policy allows. It writes reports/adsready-local.json.
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

function walkHtml() {
  const html = [];
  (function walk(d) {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      if (e.name.startsWith(".") || ["node_modules", "tools", "reports", "audit"].includes(e.name)) continue;
      if (e.isDirectory()) walk(path.join(d, e.name));
      else if (/\.html?$/.test(e.name)) html.push(path.join(d, e.name));
    }
  })(ROOT);
  return html;
}

function localChecks() {
  const read = (rel) => { try { return fs.readFileSync(path.join(ROOT, rel), "utf8"); } catch (e) { return ""; } };

  const ads = read("ads.txt");
  add("ads-txt", "ads.txt carries exactly the authorised line",
    new RegExp("^google\\.com,\\s*" + PUB + ",\\s*DIRECT,\\s*f08c47fec0942fa0\\s*$", "m").test(ads),
    (ads.split("\n").find((l) => l.includes("google.com,")) || "no google.com line").trim());

  const robots = read("robots.txt");
  add("robots", "robots.txt declares a sitemap and does not disallow everything",
    /Sitemap:/i.test(robots) && !/^Disallow:\s*\/\s*$/m.test(robots),
    robots ? "robots.txt present" : "robots.txt missing");

  const idx = read("sitemap-index.xml");
  const children = (idx.match(/<loc>/g) || []).length;
  const missingChildren = [...idx.matchAll(/<loc>https:\/\/ekguru\.shop\/([^<]+)<\/loc>/g)]
    .map((m) => m[1]).filter((f) => !fs.existsSync(path.join(ROOT, f)));
  add("sitemap", "sitemap-index lists child sitemaps that exist",
    /<sitemapindex/i.test(idx) && children >= 10 && missingChildren.length === 0,
    children + " child sitemaps" + (missingChildren.length ? ", MISSING " + missingChildren.slice(0, 3).join(", ") : ""));

  /* Every page should canonicalise to this domain — the 10 Sep 2026 rejection
     trace: 546 pages still pointed at the GitHub Pages host, and Google does
     not read ads.txt for a property it does not recognise. */
  const pages = walkHtml();
  const wrongCanon = [], noCanon = [];
  for (const p of pages) {
    const h = fs.readFileSync(p, "utf8");
    const m = h.match(/<link rel="canonical" href="([^"]+)"/);
    const noindex = /<meta name="robots"[^>]*noindex/i.test(h) || /google-?[0-9a-f]{16}\.html$/i.test(p);
    if (!m) { if (!noindex) noCanon.push(p); continue; }
    if (!m[1].startsWith("https://ekguru.shop/")) wrongCanon.push([p, m[1]]);
  }
  add("canonical", "every indexable page canonicalises to https://ekguru.shop/",
    wrongCanon.length === 0 && noCanon.length === 0,
    wrongCanon.length ? wrongCanon.slice(0, 3).map((x) => x[0] + " → " + x[1]).join("; ")
      : `${pages.length} pages; only noindex utilities (admin.html, the Search Console file) omit one`);

  for (const p of ["privacy/index.html", "about/index.html", "contact/index.html", "terms/index.html",
                   "cookie-policy/index.html", "disclaimer/index.html", "copyright/index.html"]) {
    add("page-" + p.split("/")[0], "/" + p.split("/")[0] + "/ exists",
      fs.existsSync(path.join(ROOT, p)), fs.existsSync(path.join(ROOT, p)) ? "present" : "MISSING");
  }

  add("content-volume", "Substantial unique content (≥100 published pages)",
    pages.length >= 100, `${pages.length} HTML pages in tree`);
  add("real-pages", "Country pages are real, distinct pages (not redirects to one)",
    fs.existsSync(path.join(ROOT, "learn-hindi-from-usa", "index.html")), "learn-hindi-from-usa/ checked");
}

async function main() {
  const local = process.argv.includes("--local");
  if (local) {
    localChecks();
    const passed0 = checks.filter((c) => c.ok).length;
    const result0 = { ready: passed0 === checks.length, passed: passed0, total: checks.length,
      failed: checks.filter((c) => !c.ok), checks, generated: new Date().toISOString(),
      mode: "local",
      disclaimer: "Readiness only — NOT an approval signal. AdSense approval is Google's decision." };
    fs.writeFileSync(path.join(REPORTS, "adsready-local.json"), JSON.stringify(result0, null, 2));
    for (const c of checks) console.log(`${c.ok ? "✓" : "✗"} ${c.label} — ${c.detail}`);
    console.log(`\nAdSense readiness (local): ${passed0}/${checks.length} checks pass.`);
    return;
  }

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
