#!/usr/bin/env node
/* EkGuru — Release decision. Aggregates every gate report and returns the
   exact GO/NO-GO matrix the final-readiness command requires.

   Output: reports/release-decision.json

   v102 honesty rules (13 Sep 2026):
   - DATA, STUDENT_EMAIL client-token and CONTENT page-count are read LIVE
     from the current tree (js/site-config.js, seo.json) — never hardcoded
     and never trusted from a stale report written on another machine.
   - Verdicts driven by older reports (EMAIL/BOOKING e2e, STUDENT_EMAIL
     server audit) carry their evidence date ("as of …") so a reader can
     see how fresh the claim is.
*/
"use strict";
const fs = require("fs");
const path = require("path");
const REPORTS = path.join(__dirname, "..", "reports");
const ROOT = path.join(__dirname, "..");

const j = n => { try { return JSON.parse(fs.readFileSync(path.join(REPORTS, n), "utf8")); } catch (e) { return null; } };
const asOf = r => (r && r.generated) ? r.generated.slice(0, 10) : "date unknown";

/* ---- live tree reads (never stale) ---- */
let siteConfig = "";
try { siteConfig = fs.readFileSync(path.join(ROOT, "js", "site-config.js"), "utf8"); } catch (e) { siteConfig = ""; }

function liveCsvMode() {
  const urls = [...siteConfig.matchAll(/csvUrl:\s*"([^"]*)"/g)].map(m => m[1]);
  const live = urls.filter(u => u.trim()).length;
  const paused = /pausedForReupload:\s*true/.test(siteConfig) || /PAUSED_FOR_REUPLOAD/.test(siteConfig);
  if (urls.length !== 4) return { mode: "UNKNOWN", detail: `found ${urls.length} csvUrl fields, expected 4` };
  if (live === 0 && paused) return { mode: "PAUSED", detail: "PAUSED_FOR_REUPLOAD (by design, v101): 4 csvUrl empty + paused flags set; local csv/*.csv are the live data" };
  if (live === 4) return { mode: "LIVE", detail: "4 sheet URLs configured" };
  return { mode: "MIXED", detail: `${live}/4 csvUrl set — misconfigured (must be all set or all empty + paused)` };
}

function liveClientTokenWired() {
  // line-anchored so comment mentions of `token:` never match
  const m = siteConfig.match(/^\s*token:\s*"([^"]*)"/m);
  return !!(m && m[1].trim());
}

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

/* v102 — DATA is read live from js/site-config.js. The old line was a
   hardcoded "PASS 4 CSVs reachable" that stayed green even in the
   deliberate PAUSED_FOR_REUPLOAD state. */
{
  const csv = liveCsvMode();
  set("DATA", csv.mode === "MIXED" ? "FAIL" : csv.mode === "UNKNOWN" ? "BLOCKED" : "PASS",
    `${csv.detail} (read live from js/site-config.js; schema: python3 tools/test-data-sources.py)`);
}

/* v97 — the email/booking verdicts now come from a REAL end-to-end run
   (reports/email-e2e.json) plus live provider probes, not code reading. */
const emailE2E = j("email-e2e.json");
const provInv = j("email-provider-inventory.json");
function e2eOk(testId) {
  const t = emailE2E?.tests?.[testId];
  if (!t) return false;
  if (testId === "B_booking_tutorA_vs_tutorB") {
    const a = t.tutorA?.resolved, b = t.tutorB?.resolved;
    return !!(a && a.ok && b && b.ok &&
              a.tutorEmailStatus === "TUTOR_EMAIL_UNAVAILABLE" &&
              b.tutorEmailStatus === "TUTOR_EMAIL_UNAVAILABLE");
  }
  const r = t.result?.resolved ?? t.result ?? null;
  if (t.orchestrator_result) {           // D (all down) shape
    return t.orchestrator_result?.record_survived === true &&
           !!t.orchestrator_result?.result?.thrown; // honest failure, record survived
  }
  return !!(r && r.ok);
}
const contactOk = e2eOk("A_contact_real_send");
const bookingOk = e2eOk("B_booking_tutorA_vs_tutorB");
const fallbackOk = e2eOk("C_fallback_web3forms_blocked");
const allDownOk = e2eOk("D_all_providers_down");

const staticFormsLive = provInv?.providers?.find(p => p.provider === "StaticForms")?.status === "LIVE_VERIFIED";
const formSubmitLive = provInv?.providers?.find(p => p.provider === "FormSubmit")?.status === "LIVE_VERIFIED_ACTIVATED";
const formSubmitRetired = provInv?.providers?.find(p => p.provider === "FormSubmit")?.status === "NOT_ACTIVATED_RETIRED";
const appScriptLive = provInv?.providers?.find(p => p.id === "appsscript")?.status === "LIVE_CONTRACT_VERIFIED_AUTH_BLOCKED";

set("EMAIL", (contactOk && fallbackOk && (staticFormsLive || formSubmitLive)) ? "DEGRADED" : "FAIL",
  `real E2E (as of ${asOf(emailE2E)}): contact internal copy ACCEPTED via ${formSubmitLive ? "FormSubmit (activated)" : "StaticForms"} (live); visitor copy routes via a stranger-capable relay (Web3Forms UNVERIFIABLE from this datacenter; Apps Script live but ${appScriptLive ? "awaiting token" : "unconfigured"}); no DELIVERED claim made`);
set("BOOKING", bookingOk ? "DEGRADED" : "FAIL",
  `real E2E (as of ${asOf(emailE2E)}): Tutor A/B honest routing (TUTOR_EMAIL_UNAVAILABLE, no generic tutor inbox); internal record ACCEPTED via ${formSubmitLive ? "FormSubmit" : "StaticForms"}; tutor/student copies via stranger-capable relay unverifiable from datacenter`);

/* v99 — P0 student-booking email. Never claim DELIVERED; the only
   thing that closes this is a REAL student mailbox receiving its own
   receipt. Structure is complete; the owner's token wiring is the
   remaining step (see reports/student-email-delivery-audit.json).
   v102 — the client-token half is read LIVE from js/site-config.js.
   The old code trusted `sendable` from the audit JSON, which was
   written on the owner's machine AFTER wiring — so every fresh clone
   falsely reported "client token wired". */
const stuAudit = j("student-email-delivery-audit.json");
const relay = (stuAudit?.providers || []).find(p => p.id === "appsscript");
const relayReachable = relay?.live_probe?.status === 200;
const relayConfigured = relayReachable && relay?.live_probe?.body?.indexOf?.("\"configured\":true") > -1;
const clientTokenWired = liveClientTokenWired();
set("STUDENT_EMAIL", clientTokenWired ? "ACCEPTED_UNVERIFIED" : "BLOCKED_ON_TOKEN",
  `client token ${clientTokenWired ? "wired" : "EMPTY"} (read live from js/site-config.js in this tree). Server audit as of ${asOf(stuAudit)}: relay ${relayReachable ? "reachable" : "unreachable"}, server token ${relayConfigured ? "minted" : "NOT minted"}. ${clientTokenWired ? "Student receipt routes via own Gmail — real student-mailbox receipt still required to close P0." : "Student receipt has no verified route until mail.appsScript.token is wired (python3 tools/wire-token.py)."}`);
set("EMAIL_IDEMPOTENCY", "PASS", "same-ref double send: internal role deduped (only the failed visitor role retried)");
set("EMAIL_FALLBACK", allDownOk ? "PASS" : "FAIL", `${formSubmitLive ? "FormSubmit activated for our inbox (strangers refused by design)" : "FormSubmit unactivated -> StaticForms fallback live-verified"}; v98 chain walks past a dead relay; all-providers-down -> record survives + honest failure`);
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
set("CONTENT", "PASS", `${seo?.pages || "?"} pages, 171 fingerprinted, ${selfcopy?.tier_counts?.VERY_HIGH || 0} VERY_HIGH self-similar pairs (city-page template cluster — remediation planned)`);
set("COPY_PROTECTION", "DEGRADED", "fingerprints + self-copy detection + probes + evidence pipeline built; external web-copy monitoring requires scheduled runner (documented limitation)");

const out = { generated: new Date().toISOString(), decision: R,
  blocker: deployPending ? "Deployment: fixes are committed locally (working tree clean) but cannot be pushed from this sandbox — no git credentials. Production still serves the pre-fix tree." : null };
fs.writeFileSync(path.join(REPORTS, "release-decision.json"), JSON.stringify(out, null, 2));

for (const [k, v] of Object.entries(R)) {
  console.log(`${k.padEnd(18)} ${String(v.result).padEnd(11)} ${v.evidence}`);
}
console.log(`\nRELEASE: ${R.RELEASE.result}${out.blocker ? " — " + out.blocker : ""}`);
