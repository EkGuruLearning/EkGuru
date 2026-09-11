#!/usr/bin/env node
/* EkGuru — the DOCTOR / build gate. One command that runs every health
   check the site must pass before a deploy is honest, and writes the
   verdict the admin dashboard displays.

   Output: reports/doctor.json
     { doctorProblems, doctorWarnings, doctorChecks, seoPass, privacyState,
       results: [ { id, label, status: PASS|WARN|FAIL, detail } ], generated }

   Run: node tools/gate.js   (or the whole chain: node tools/doctor.js)
*/
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const REPORTS = path.join(ROOT, "reports");
if (!fs.existsSync(REPORTS)) fs.mkdirSync(REPORTS, { recursive: true });

const read = p => { try { return fs.readFileSync(path.join(ROOT, p), "utf8"); } catch (e) { return null; } };
const readJson = p => { const t = read(p); if (!t) return null; try { return JSON.parse(t); } catch (e) { return null; } };

const results = [];
function check(id, label, ok, detail, warn) {
  const status = ok ? "PASS" : (warn ? "WARN" : "FAIL");
  results.push({ id, label, status, detail: detail || "" });
}

async function main() {
  /* 1 — config is live, not "soon" (local tree) */
  const cfg = read("js/site-config.js") || "";
  const live = /status\s*:\s*["']live["']/.test(cfg);
  check("status-live", "Site status is live (not Coming soon)", live,
    live ? "status:\"live\"" : "js/site-config.js still has status other than \"live\"");

  /* 1b — the PRODUCTION deployment serves this config (deployment freshness).
     Fails when the live site still serves an older tree than this one. */
  let liveStatus = "unknown";
  try {
    const r = await fetch("https://ekguru.shop/js/site-config.js");
    const t = await r.text();
    if (/status\s*:\s*["']soon["']/.test(t)) liveStatus = "soon";
    else if (/status\s*:\s*["']live["']/.test(t)) liveStatus = "live";
  } catch (e) { liveStatus = "unreachable"; }
  check("deployed", "Production serves the current tree", liveStatus === "live",
    liveStatus === "live" ? "live site-config.js status:\"live\"" :
      `live site-config.js status="${liveStatus}" (local is "live") — deploy pending`);

  /* 2 — privacy scan */
  const priv = readJson("reports/privacy-scan.json");
  const privState = priv ? (priv.summary?.verdict || "PASS") : "UNKNOWN";
  const privOk = privState === "PASS" && (priv.summary?.blocked || 0) === 0 && (priv.summary?.findings?.secret || 0) === 0;
  check("privacy", "Privacy/secret scan passes", privOk,
    `${privState} — ${priv?.summary?.findings?.secret || 0} secrets, ${priv?.summary?.findings?.sensitive || 0} sensitive, ${priv?.summary?.blocked || 0} blocked`,
    !priv);

  /* 3 — no personal emails in public tutor data */
  const overrides = read("js/tutors/_overrides.js") || "";
  const personalEmail = /\b(?:ckhadutta|hemlata\.hindi|sushila\.hindi|tara\.hindi)@gmail\.com\b/.test(overrides);
  check("no-personal-emails", "No personal tutor emails in public data", !personalEmail,
    personalEmail ? "a personal Gmail is published in js/tutors/_overrides.js" : "tutor emails route via site inbox/formKey");

  /* 4 — every tutor can receive bookings. Runtime fallback chain
     (js/sheet.js FIELDS.email + js/tutors-data.js): sheet email → formKey →
     hand-written file email → EKGURU_SITE.email (the site inbox). So a tutor
     is routable if it has email OR formKey, OR the site fallback exists. */
  const siteFallback = /email\s*:\s*"EkGuruLearning@gmail\.com"/.test(cfg);
  const sheetOver = overrides.match(/window\.EKGURU_SHEET_OVERRIDES\s*=\s*(\{[\s\S]*?\})\s*;\s*window\.EKGURU_SHEET_SETTINGS/) || [];
  let routable = 0, unroutable = [];
  if (sheetOver[1]) {
    try {
      const O = JSON.parse(sheetOver[1]);
      for (const [id, t] of Object.entries(O)) {
        if (t.email || t.formKey || siteFallback) routable++;
        else unroutable.push(id);
      }
    } catch (e) {}
  }
  check("booking-routing", "Every tutor can receive bookings", unroutable.length === 0 && routable > 0,
    unroutable.length ? `no route: ${unroutable.join(", ")}` : `${routable} tutor(s) routable${siteFallback ? " (site-inbox fallback)" : ""}`,
    routable === 0);

  /* 5 — header geometry */
  const geo = readJson("reports/header-geometry.json");
  const geoFails = Array.isArray(geo?.failures) ? geo.failures.length : -1;
  const geoWidths = geo?.evidence ? Object.keys(geo.evidence).length : 0;
  const geoOk = geoFails === 0 && geoWidths === 17;
  check("header-geometry", "Header geometry clean at 17 widths", geoOk,
    geo ? `${geoWidths} widths, ${geoFails} failures` : "reports/header-geometry.json missing — run tools/test-header-geometry.py",
    !geo);

  /* 6 — SEO */
  const seo = readJson("reports/seo.json");
  const seoPass = !!seo && seo.pass;
  check("seo", "No broken internal links", seoPass,
    seo ? `${seo.pages} pages, ${seo.brokenLinks} broken, ${seo.orphans} orphans` : "reports/seo.json missing — run node tools/seocheck.js",
    !seo);

  /* 7 — live: ads.txt publisher id */
  let adsOk = false, adsDetail = "not checked";
  try {
    const r = await fetch("https://ekguru.shop/ads.txt");
    const t = await r.text();
    adsOk = r.ok && /google\.com,\s*pub-8175326569491671,\s*DIRECT,\s*f08c47fec0942fa0/.test(t);
    adsDetail = r.status + (adsOk ? " — publisher id matches" : " — mismatch or missing");
  } catch (e) { adsDetail = "fetch failed"; }
  check("ads-txt", "ads.txt declares the correct publisher", adsOk, adsDetail);

  /* 8 — live: robots.txt safe + sitemap */
  let robotsOk = false, robotsDetail = "not checked";
  try {
    const r = await fetch("https://ekguru.shop/robots.txt");
    const t = await r.text();
    robotsOk = r.ok && /Sitemap:/i.test(t) && !/^Disallow:\s*\/\s*$/m.test(t);
    robotsDetail = r.status + (robotsOk ? " — sitemap declared, not all-blocked" : " — problem");
  } catch (e) { robotsDetail = "fetch failed"; }
  check("robots", "robots.txt safe and declares sitemap", robotsOk, robotsDetail);

  /* 9 — live: homepage canonical + old GitHub redirect */
  let canonOk = false, canonDetail = "not checked";
  try {
    const r = await fetch("https://ekguru.shop/");
    const t = await r.text();
    canonOk = r.ok && /rel="canonical"\s+href="https:\/\/ekguru\.shop\/"/.test(t);
    canonDetail = r.status + (canonOk ? " — canonical https://ekguru.shop/" : " — canonical missing");
  } catch (e) { canonDetail = "fetch failed"; }
  check("canonical", "Homepage canonical is https://ekguru.shop/", canonOk, canonDetail);

  /* 10 — sheet sanity: videoTitle must not contain methodology text */
  const sheetOk = !/\uD83D\uDC4D|Conversation first \|/.test(read("js/tutors/_overrides.js") || "") ||
    !/"videoTitle":\s*"[^"]*\|[^"]*"/.test(read("js/tutors/_overrides.js") || "");
  check("sheet-sanity", "Sheet values sanitised (no cross-column leakage)", sheetOk,
    sheetOk ? "videoTitle guard active" : "a multi-line / | value leaked into videoTitle");

  const problems = results.filter(r => r.status === "FAIL").length;
  const warnings = results.filter(r => r.status === "WARN").length;
  const doctor = {
    doctorProblems: problems,
    doctorWarnings: warnings,
    doctorChecks: results.length,
    seoPass,
    privacyState: privState,
    results,
    generated: new Date().toISOString(),
  };

  fs.writeFileSync(path.join(REPORTS, "doctor.json"), JSON.stringify(doctor, null, 2));

  for (const r of results) {
    const mark = r.status === "PASS" ? "✓" : (r.status === "WARN" ? "⚠" : "✗");
    console.log(`${mark} [${r.status}] ${r.label} — ${r.detail}`);
  }
  console.log(`\nDoctor: ${problems} problem(s), ${warnings} warning(s), ${results.length} checks. ${problems === 0 ? "PASS" : "FAIL"}`);
}

main().catch(e => { console.error("gate.js crashed:", e.message); process.exit(1); });
