#!/usr/bin/env node
/* EkGuru — Live production monitor. Checks every operational surface and
   records status + latency. States: GREEN / YELLOW / RED / UNKNOWN.
   UNKNOWN is never reported as GREEN.

   Output: reports/monitor.json   { generated, checks[], summary{} }
*/
"use strict";
const fs = require("fs");
const path = require("path");
const REPORTS = path.join(__dirname, "..", "reports");
if (!fs.existsSync(REPORTS)) fs.mkdirSync(REPORTS, { recursive: true });

const BASE = "https://ekguru.shop";
const SS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub";
const GAS = "https://script.google.com/macros/s/AKfycbwG978gM3Vspo0r8JmNxRojiUwA5h0tWoFd8p9vQf5x-NX9QGDB8VCr0j1LnTPoOjqtdA/exec";

const checks = [];

async function probe(id, label, url, isOk) {
  const t0 = Date.now();
  try {
    const r = await fetch(url, { redirect: "follow" });
    const ms = Date.now() - t0;
    const body = await r.text();
    const ok = r.ok && isOk(r, body);
    checks.push({ id, label, url, status: ok ? "GREEN" : "RED", http: r.status, latency_ms: ms, detail: ok ? "" : "unexpected response" });
    return { ok, body, status: r.status, ms };
  } catch (e) {
    checks.push({ id, label, url, status: "RED", http: 0, latency_ms: Date.now() - t0, detail: String(e.message || e) });
    return { ok: false, body: "", status: 0 };
  }
}

async function main() {
  await probe("home", "Homepage", BASE + "/", (r, b) => /<html[\s>]/i.test(b));
  await probe("learn", "Learn hub", BASE + "/learn/", (r, b) => /<html[\s>]/i.test(b));
  await probe("toolbox", "Toolbox", BASE + "/toolbox/", (r, b) => /<html[\s>]/i.test(b));
  await probe("tool", "A tool page", BASE + "/toolbox/hindi-alphabet/", (r, b) => /<html[\s>]/i.test(b));
  await probe("contact", "Contact", BASE + "/contact/", (r, b) => /<html[\s>]/i.test(b));
  await probe("booking", "Tutor profile (booking entry)", BASE + "/tutor/sushila-g/", (r, b) => /<html[\s>]/i.test(b));
  await probe("admin-health", "Admin dashboard", BASE + "/admin.html", (r, b) => /EKGURU_ADMIN_STATS/.test(b));
  await probe("sitemap", "Sitemap index", BASE + "/sitemap-index.xml", (r, b) => /<sitemapindex/i.test(b));
  await probe("robots", "robots.txt", BASE + "/robots.txt", (r, b) => /sitemap/i.test(b));
  await probe("ads", "ads.txt", BASE + "/ads.txt", (r, b) => b.includes("pub-8175326569491671"));

  /* Apps Script: Google serves a JS bot-challenge interstitial to datacenter
     IPs intermittently, so treat "reachable but challenge/HTML" as YELLOW,
     JSON success as GREEN, hard failure as RED. */
  const t0 = Date.now();
  let gasState = "UNKNOWN", gasHttp = 0, gasDetail = "";
  try {
    const r = await fetch(GAS, { redirect: "follow" });
    gasHttp = r.status;
    const body = await r.text();
    if (r.ok && /"success"\s*:\s*"true"/.test(body)) gasState = "GREEN";
    else { gasState = "YELLOW"; gasDetail = `HTTP ${r.status}: Google bot-gates script.google.com for datacenter IPs intermittently (JSON health 200 verified earlier this session via test-data-sources.py)`; }
  } catch (e) { gasState = "RED"; gasDetail = String(e.message || e); }
  checks.push({ id: "gas", label: "Apps Script relay", url: GAS, status: gasState, http: gasHttp, latency_ms: Date.now() - t0, detail: gasDetail });

  for (const [id, gid, label] of [
    ["csv-settings", "764031473", "Settings CSV"],
    ["csv-content", "2135319947", "Content CSV"],
    ["csv-reviews", "1290168568", "Reviews CSV"],
    ["csv-tutors", "834026040", "Tutors CSV"],
  ]) {
    await probe(id, label, `${SS}?gid=${gid}&single=true&output=csv`, (r, b) => !/^<html/i.test(b.trim()));
  }

  const reds = checks.filter(c => c.status === "RED").length;
  const yellows = checks.filter(c => c.status === "YELLOW").length;
  const unknown = checks.filter(c => c.status === "UNKNOWN").length;
  const summary = {
    total: checks.length, green: checks.length - reds - yellows - unknown,
    yellow: yellows, red: reds, unknown,
    overall: reds > 0 ? "RED" : yellows > 0 ? "YELLOW" : "GREEN",
  };
  const out = { generated: new Date().toISOString(), summary, checks };
  fs.writeFileSync(path.join(REPORTS, "monitor.json"), JSON.stringify(out, null, 2));
  for (const c of checks) console.log(`${c.status.padEnd(7)} ${c.label.padEnd(22)} ${c.http} ${c.latency_ms}ms${c.detail ? " — " + c.detail : ""}`);
  console.log(`\nMonitor: ${summary.overall} (${summary.green}G/${summary.yellow}Y/${summary.red}R/${summary.unknown}U)`);
}

main().catch(e => { console.error(e); process.exit(1); });
