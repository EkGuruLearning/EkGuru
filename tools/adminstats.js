#!/usr/bin/env node
/* EkGuru — regenerates js/admin-stats.js from the live reports.
   Reads the previous file (for the deeply-generated static datasets:
   countries, languages, pairs, tutors, sitemapUrls) and re-computes the
   health blocks (seo / privacy / gate) plus page counts from the current
   tree + reports. Contains NO secrets.

   Run: node tools/adminstats.js   (or the whole chain: node tools/doctor.js)
*/
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const REPORTS = path.join(ROOT, "reports");
const TARGET = path.join(ROOT, "js", "admin-stats.js");

const readJson = p => { try { return JSON.parse(fs.readFileSync(path.join(ROOT, p), "utf8")); } catch (e) { return null; } };

const seo = readJson("reports/seo.json");
const priv = readJson("reports/privacy-scan.json");
const gate = readJson("reports/doctor.json");

/* parse the previous file so we keep the static datasets */
const prevSrc = fs.readFileSync(TARGET, "utf8");
const m = /window\.EKGURU_ADMIN_STATS\s*=\s*(\{[\s\S]*\})\s*;?\s*$/.exec(prevSrc);
if (!m) { console.error("cannot parse existing admin-stats.js"); process.exit(1); }
const prev = JSON.parse(m[1]);

/* page counts from the tree */
function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".") && e.name !== ".nojekyll") continue;
    if (e.name === "node_modules" || e.name === "tools" || e.name === "reports" || e.name === "audit") continue;
    if (e.isDirectory()) walk(path.join(dir, e.name), out);
    else if (/\.html?$/.test(e.name)) out.push(path.join(dir, e.name));
  }
  return out;
}
const html = walk(ROOT, []);
const rel = p => path.relative(ROOT, p).split(path.sep).join("/");
const totalHtml = html.length;
const tutorProfiles = html.filter(f => /^tutor\/[^/]+\/index\.html$/.test(rel(f))).length;
const materials = html.filter(f => /^materials\/[^/]+\/index\.html$/.test(rel(f))).length;

/* privacy block (shape admin-repo.js expects) */
const privacyBlock = priv ? {
  state: priv.summary?.verdict || "PASS",
  fails: (priv.summary?.findings?.secret || 0) + (priv.summary?.findings?.sensitive || 0),
  blocked: priv.summary?.blocked || 0,
  note: `${priv.summary?.scanned_files} files scanned, ${priv.summary?.findings?.secret || 0} secrets`,
} : { state: "UNKNOWN", fails: 0, blocked: 0, note: "Run: node tools/privacy.js --sheets --live" };

/* seo block */
const seoBlock = seo ? {
  pass: seo.pass, critical: seo.critical, warnings: seo.warnings, pages: seo.pages,
  sitemapUrls: seo.sitemapUrls, sitemapFiles: seo.sitemapFiles,
  brokenLinks: seo.brokenLinks, orphans: seo.orphans,
} : prev.seo;

/* gate block */
const gateBlock = gate ? {
  doctorProblems: gate.doctorProblems,
  doctorWarnings: gate.doctorWarnings,
  doctorChecks: gate.doctorChecks,
  seoPass: gate.seoPass,
  privacyState: gate.privacyState,
} : prev.gate;

/* release block — current build identity, data-source state, and test evidence */
function releaseBlock() {
  let commit = "unknown", subject = "";
  try {
    const cp = require("child_process");
    commit = cp.execSync("git rev-parse HEAD", { cwd: ROOT }).toString().trim();
    subject = cp.execSync("git log -1 --format=%s", { cwd: ROOT }).toString().trim();
  } catch (e) { /* not a git checkout during build */ }
  const tests = {};
  ["test-sheet-apply.js", "adsready.js", "seocheck.js"].forEach(t => { tests[t] = null; });
  // pick up tool QA summary if present
  const qa = readJson("reports/tool-functional-qa.json");
  const idle = readJson("reports/idle-interaction-regression.json");
  return {
    commit, subject,
    buildTime: new Date().toISOString(),
    dataSourceStatus: "PAUSED_FOR_REUPLOAD",  // reflected from js/site-config.js at runtime
    toolQa: qa && qa.summary ? qa.summary : null,
    idleRegression: idle ? { refreshRequiredAnywhere: idle.refreshRequiredAnywhere } : null,
    sections: { totalHtml, tutorProfiles, materials },
  };
}

/* phase3 block — production/live/email/sheets evidence captured outside the
   local build. Read-only facts; the admin Release board renders them as a
   8-state ladder. Regenerate after any external verification changes. */
function phase3Block() {
  return {
    remote: {
      url: "https://github.com/ekgurulearning/EkGuru",
      mainHead: "ba859a9bb9b5ebd9826b94599179e5a0712f29db",
      mainSubject: "Initial commit (owner force-push, 2026-09-11)",
      localAhead: true,
      note: "Remote main is a squashed PRE-Phase-2 snapshot + the owner's live-sheets/ CSV exports. Local main is ~40 commits ahead; a push is non-fast-forward.",
    },
    live: {
      url: "https://ekguru.shop/",
      servesPhase2: false,
      materials: 404, faq: 404, recoveryJs: 404,
      swCache: "ekguru-v30-f10d5437",
      sitemaps: 13,
      note: "Production serves the pre-Phase-2 build (no /materials/, /faq/, recovery.js). Live-sheets/*.csv ARE publicly reachable on the live site.",
    },
    sheets: {
      runtime: "PAUSED_FOR_REUPLOAD",
      publishedUrlsSupplied: false,
      liveSheetsInRepo: ["content.csv", "reviews.csv", "settings.csv", "tutors.csv"],
      note: "Owner supplied live-sheets/ CSVs in the reset commit; six published Google-Sheet URLs are still required before runtime activation.",
    },
    email: {
      externalE2E: "BLOCKED_OWNER",
      tutorEmail: "TUTOR_EMAIL_UNAVAILABLE (blank in tutors.csv — via EkGuru fallback)",
      localTests: "system/security/routing PASS",
    },
  };
}

function phase4Block() {
  const gate = readJson("reports/learn-hindi-final-gate.json") || {};
  const build = readJson("reports/learn-hindi-build.json") || {};
  const arch = readJson("reports/learn-hindi-architecture.json") || {};
  const browser = readJson("reports/phase4-browser-gate.json") || {};
  return {
    hub: "/learn/hindi/",
    levels: build.levelsBuilt || [],
    levelsNotBuilt: build.levelsNotBuilt || [],
    topics: build.topicsBuilt || [],
    lessons: (arch.byType && arch.byType.lesson) || 0,
    materials: (arch.byType && arch.byType.material) || 0,
    practice: (arch.byType && arch.byType.practice) || 0,
    paths: (arch.byType && arch.byType.path) || 0,
    browser: browser.matrix ? `${browser.matrix.ok}/${browser.matrix.total}` : "not run",
    idleProblems: (browser.idle && browser.idle.problems) ? browser.idle.problems.length : null,
    gate: gate.overall || "NOT_RUN",
    green: gate.green, yellow: gate.yellow, red: gate.red,
  };
}

/* phase5 block — card clickability / interaction audit. Read-only facts from
   the Phase 5 evidence reports; rendered on the Release board. */
function phase5Block() {
  const inv = readJson("reports/phase5-interaction-inventory.json") || {};
  const click = readJson("reports/phase5-card-clickability.json") || {};
  const matrix = readJson("reports/phase5-browser-matrix.json") || {};
  const reg = readJson("reports/phase5-regression.json") || {};
  const fg = readJson("reports/phase5-final-gate.json") || {};
  return {
    verdict: fg.verdict || "NOT_RUN",
    cardsTotal: inv.totalCardInstances || 0,
    byPattern: inv.byPattern || {},
    titleOnly: (inv.byPattern && inv.byPattern["title-only-link"]) || 0,
    deadLinks: (fg.components && fg.components.staticInventory.deadLinks) || 0,
    deadButtons: (fg.components && fg.components.staticInventory.deadButtons) || 0,
    interactions: `${click.ok || 0}/${click.total || 0}`,
    matrix: `${matrix.ok || 0}/${matrix.total || 0}`,
    regression: `${reg.ok || 0}/${reg.total || 0}`,
    gapsBlocking: fg.gapsBlocking || 0,
  };
}

const out = {
  generated: new Date().toISOString(),
  sections: Object.assign({}, prev.sections, { totalHtml, tutorProfiles, materials }),
  countries: prev.countries,
  languages: prev.languages,
  pairs: prev.pairs,
  seo: seoBlock,
  privacy: privacyBlock,
  gate: gateBlock,
  tutors: prev.tutors,
  sitemapUrls: prev.sitemapUrls,
  release: releaseBlock(),
  phase3: phase3Block(),
  phase4: phase4Block(),
  phase5: phase5Block(),
};

const header =
`/* GENERATED by tools/adminstats.js — do not edit.
   Real numbers for admin.html, computed at build time from the
   same generators and validators that produce the site.
   Contains NO secrets and NO personal addresses: it is served
   publicly like every other file here.
   Regenerate: node tools/adminstats.js */
`;

fs.writeFileSync(TARGET, header + "window.EKGURU_ADMIN_STATS = " + JSON.stringify(out, null, 1) + ";\n");

console.log(`admin-stats.js regenerated`);
console.log(`  sections.totalHtml = ${totalHtml} (was ${prev.sections.totalHtml})`);
console.log(`  sections.tutorProfiles = ${tutorProfiles}`);
console.log(`  seo: ${seoBlock.pass ? "PASS" : "FAIL"} (${seoBlock.pages} pages, ${seoBlock.brokenLinks} broken, ${seoBlock.orphans} orphans)`);
console.log(`  privacy: ${privacyBlock.state} (${privacyBlock.fails} fails, ${privacyBlock.blocked} blocked)`);
console.log(`  gate: ${gateBlock.doctorProblems} problems, ${gateBlock.doctorWarnings} warnings, ${gateBlock.doctorChecks} checks`);
