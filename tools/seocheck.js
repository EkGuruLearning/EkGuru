#!/usr/bin/env node
/* EkGuru — SEO checker (build side). Crawls the static tree, checks every
   internal link resolves, finds orphan pages, and verifies the sitemap.

   Output: reports/seo.json  { pass, critical, warnings, pages, sitemapUrls,
                              sitemapFiles, brokenLinks, orphans }

   Run: node tools/seocheck.js
*/
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const REPORTS = path.join(ROOT, "reports");
if (!fs.existsSync(REPORTS)) fs.mkdirSync(REPORTS, { recursive: true });

const SKIP_DIRS = new Set([".git", "node_modules", "reports", "tools", "audit"]);
const HTML = [];

function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".") && e.name !== ".nojekyll") continue;
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) walk(path.join(dir, e.name)); continue; }
    if (/\.html?$/.test(e.name)) HTML.push(path.join(dir, e.name));
  }
}
walk(ROOT);

function rel(p) { return path.relative(ROOT, p).split(path.sep).join("/"); }

/* every internal href -> target file (or null if external/hash/mailto) */
function resolveHref(fromDir, href) {
  href = href.trim();
  if (/^(https?:|mailto:|tel:|data:|javascript:|#|void)/i.test(href)) return null;
  if (href.startsWith("#")) return null;
  let clean = href.split("#")[0].split("?")[0];
  if (!clean || clean === "/") clean = "index.html";
  let p = clean.startsWith("/") ? path.join(ROOT, clean) : path.join(fromDir, clean);
  p = path.normalize(p);
  if (!path.extname(p)) p = path.join(p, "index.html");
  return p;
}

const broken = [];
const inbound = {};          // rel path -> count
const linkCount = { checked: 0 };

/* strip inline script/style so JS string-literal hrefs (built at runtime) are
   not mistaken for static links — e.g. admin's `'<a href="..' + r[0]` or
   `href="../daily-hindi/day-" + nextDay`. */
function stripDynamic(text) {
  return text
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, "");
}

/* system files that are intentionally not linked from any page */
const NON_ORPHAN = new Set(["404.html", "googleb3b0e3defc1daa17.html"]);

for (const file of HTML) {
  const text = stripDynamic(fs.readFileSync(file, "utf8"));
  const dir = path.dirname(file);
  const hrefs = [...text.matchAll(/\b(?:href|src)\s*=\s*["']([^"']+)["']/gi)].map(m => m[1]);
  for (const h of hrefs) {
    const target = resolveHref(dir, h);
    if (target === null) continue;
    linkCount.checked++;
    const r = rel(target);
    inbound[r] = (inbound[r] || 0) + 1;
    if (!fs.existsSync(target)) broken.push({ from: rel(file), to: h, target: r });
  }
}

const htmlSet = new Set(HTML.map(rel));

/* sitemap */
const sitemapUrls = [];
let sitemapFiles = 0;
try {
  const idx = fs.readFileSync(path.join(ROOT, "sitemap-index.xml"), "utf8");
  const files = [...idx.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
  sitemapFiles = files.length;
  for (const f of files) {
    const name = f.split("/").pop();
    const p = path.join(ROOT, name);
    if (!fs.existsSync(p)) continue;
    const xml = fs.readFileSync(p, "utf8");
    for (const m of xml.matchAll(/<loc>([^<]+)<\/loc>/g)) {
      const u = m[1];
      if (!sitemapUrls.includes(u)) sitemapUrls.push(u);
    }
  }
} catch (e) { /* no sitemap found */ }

/* orphans = html files with no inbound link, excluding index + admin + sitemap'd */
const orphanList = [];
for (const r of htmlSet) {
  if (r === "index.html" || r === "admin.html") continue;
  if (inbound[r]) continue;
  if (NON_ORPHAN.has(r.split("/").pop())) continue;
  const name = r.split("/").pop();
  if (sitemapUrls.some(u => u.includes("/" + name.replace(/index\.html$/, "")))) continue;
  orphanList.push(r);
}

const critical = broken.length;
const warnings = orphanList.length;
const pass = critical === 0;

const seo = {
  pass,
  critical,
  warnings,
  pages: HTML.length,
  sitemapUrls: sitemapUrls.length,
  sitemapFiles,
  brokenLinks: broken.length,
  orphans: orphanList.length,
  broken: broken.slice(0, 50),
  orphanPages: orphanList.slice(0, 50),
  generated: new Date().toISOString(),
};

fs.writeFileSync(path.join(REPORTS, "seo.json"), JSON.stringify(seo, null, 2));

console.log(`pages: ${seo.pages}`);
console.log(`links checked: ${linkCount.checked}`);
console.log(`broken internal links: ${seo.brokenLinks}`);
for (const b of broken) console.log(`  ✗ ${b.from} -> ${b.to}`);
console.log(`orphan pages: ${seo.orphans}`);
for (const o of orphanList) console.log(`  ? ${o}`);
console.log(`sitemap: ${sitemapFiles} files, ${seo.sitemapUrls} urls`);
console.log(seo.pass ? "SEO: PASS" : "SEO: FAIL");
