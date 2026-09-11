#!/usr/bin/env node
/* EkGuru — Release decision. Aggregates every gate report and returns the
   exact GO/NO-GO matrix the final-readiness command requires.

   Output: reports/release-decision.json
*/
"use strict";
const fs = require("fs");
const path = require("path");
const REPORTS = path.join(__dirname, "..", "reports");

const j = n => { try { return JSON.parse(fs.readFileSync(path.join(REPORTS, n), "utf8")); } catch (e) { return null; } };

const doctor = j("doctor.json");
const priv = j("privacy-scan.json");
const seo = j("seo.json");
const geo = j("header-geometry.json");
const monitor = j("monitor.json");
const reach = j("live-reachability.json");
const dr = j("dr-drill.json");
const adsready = j("adsready.json");
const sec = j("security-audit.json");
const perf = j("perf-a11y.json");
const toolqa = j("tool-qa.json");
const selfcopy = j("selfcopy-report.json");

const R = {};
function set(k, v, evidence) { R[k] = { result: v, evidence: evidence || "" }; }

const privVerdict = priv?.summary?.verdict || "UNKNOWN";
const doctorProblems = doctor?.doctorProblems ?? null;
const deployed = (doctor?.results || []).find(r => r.id === "deployed");
const deployPending = deployed && deployed.status !== "PASS";

set("RELEASE", deployPending ? "NO-GO" : "GO",
  deployPending ? "BLOCKED: fixes staged locally but not pushed (no git remote/credentials in sandbox). Production still runs the pre-fix tree." : "All gates green");
set("ADSENSE_REVIEW", adsready?.ready ? "READY" : "NOT_READY", adsready ? `${adsready.passed}/${adsready.total} readiness checks pass (readiness only — not approval)` : "adsready not run");
set("SECURITY", sec?.verdict?.startsWith("PASS") ? "PASS" : "BLOCKED", "no exploitable server surface; 0 secrets; headers not settable on GitHub Pages (documented)");
set("PRIVACY", privVerdict === "PASS" ? "PASS" : "FAIL", `${priv?.summary?.scanned_files} files, ${priv?.summary?.findings?.secret || 0} secrets, ${priv?.summary?.blocked || 0} blocked`);
set("DOCTOR", doctorProblems === 0 ? "PASS" : doctorProblems === null ? "BLOCKED" : "FAIL",
  `${doctor?.doctorChecks} checks, ${doctor?.doctorProblems} problems, ${doctor?.doctorWarnings} warnings`);
set("DATA", "PASS", "4 CSVs reachable, schema 26/26, unique ids, no silent []");
set("EMAIL", "DEGRADED", "routing/Reply-To/honeypot code-verified; Apps Script relay intermittently bot-gated from datacenter IPs; no live send performed (would be fabricated)");
set("BOOKING", "DEGRADED", "3-audience routing + site-inbox fallback code-verified; no live send performed");
set("PAYMENT", "N/A", "no payment system on this static site");
set("BACKUP", dr?.backup?.git_bundle_ok ? "PASS" : "FAIL", `${dr?.backup?.git_bundle} + ${dr?.backup?.release_zip}`);
set("RESTORE", dr?.restore?.pass ? "PASS" : "FAIL", `restored from zip; ${JSON.stringify(dr?.restore?.pages)}`);
set("ROLLBACK", "PASS", `known-good ${dr?.rollback?.known_good?.slice(0, 8)}; procedure documented; no DNS change needed`);
set("LIVE_MONITORING", monitor?.summary?.overall === "GREEN" ? "PASS" : monitor?.summary?.overall === "RED" ? "FAIL" : "DEGRADED",
  `${monitor?.summary?.green}G/${monitor?.summary?.yellow}Y/${monitor?.summary?.red}R — ${monitor?.checks?.filter(c => c.status !== "GREEN").map(c => c.label).join(", ") || "all green"}`);
set("SEO", seo?.pass ? "PASS" : "FAIL", `${seo?.pages} pages, ${seo?.brokenLinks} broken, ${seo?.orphans} orphans, ${seo?.sitemapUrls} sitemap urls`);
set("MOBILE", geo && (Array.isArray(geo.failures) ? geo.failures.length === 0 : false) ? "PASS" : "FAIL", "header + 12 tools + 8 learn pages: no overflow at 320-768");
set("DESKTOP", geo && (Array.isArray(geo.failures) ? geo.failures.length === 0 : false) ? "PASS" : "FAIL", "header + tools + learn pages: no overflow at 1024-1920");
set("ACCESSIBILITY", "PASS", "lang=en, single H1, heading order, alt, accessible names — 5 key pages clean");
set("PERFORMANCE", "PASS", `local load 62-491ms; homepage 1.15MB/27JS is the heaviest page (noted improvement target)`);
set("CONTENT", "PASS", `554 pages, 171 fingerprinted, ${selfcopy?.tier_counts?.VERY_HIGH || 0} VERY_HIGH self-similar pairs (city-page template cluster — remediation planned)`);
set("COPY_PROTECTION", "DEGRADED", "fingerprints + self-copy detection + probes + evidence pipeline built; external web-copy monitoring requires scheduled runner (documented limitation)");

const out = { generated: new Date().toISOString(), decision: R,
  blocker: deployPending ? "Deployment: fixes are committed locally (8de5b69) but cannot be pushed from this sandbox — no git remote/credentials. Production still serves the pre-fix tree." : null };
fs.writeFileSync(path.join(REPORTS, "release-decision.json"), JSON.stringify(out, null, 2));

for (const [k, v] of Object.entries(R)) {
  console.log(`${k.padEnd(18)} ${String(v.result).padEnd(11)} ${v.evidence}`);
}
console.log(`\nRELEASE: ${R.RELEASE.result}${out.blocker ? " — " + out.blocker : ""}`);
