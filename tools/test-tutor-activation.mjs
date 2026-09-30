#!/usr/bin/env node
/* ============================================================
   U0 RE-ACTIVATION TEST (30 Sep 2026)
   ============================================================
   One tutor row, two states, everything in between proven:

     active=no   -> hidden: profile noindex + booking surfaces off +
                    absent from sitemap-tutors.xml / sitemap.xml /
                    feed.xml / llms.txt / manifest shortcuts / 404.html /
                    find-tutors + tutor/index ItemLists / home + market cards
     active=yes  -> THE FULL RESTORE: indexable + booking CTAs + Person
                    JSON-LD + listings back everywhere

   Both directions are owned by the GENERATORS (Golden Rule R-5), so the
   test drives the real ones against a fixture row that it flips:

     tools/sheetsync.js --offline <tmp fixtures>   (hidden set + Policy)
     tools/build-tutor-pages.js                    (profiles + every roster
                                                    surface listed above)
     tools/build-home-tutors.js / build-market-pages.js (cards)

   The test snapshots every file it touches and restores them byte-for-byte
   in a finally block — the working tree ends exactly as it started.

   Run:  node tools/test-tutor-activation.mjs
   ============================================================ */
"use strict";
import { readFileSync, writeFileSync, mkdirSync, cpSync, rmSync, mkdtempSync } from "fs";
import { execFileSync } from "child_process";
import { join, dirname } from "path";
import { tmpdir } from "os";
import { createRequire } from "module";

const ROOT = new URL(import.meta.url).pathname.replace(/\/tools\/[^/]+$/, "");
const require = createRequire(import.meta.url);
const siteData = require(join(ROOT, "tools", "lib", "site-data.js"));

let passed = 0, failed = 0;
function check(name, cond, detail) {
  if (cond) { passed++; console.log("  ok    " + name); }
  else { failed++; console.log("  FAIL  " + name + (detail ? "  — " + detail : "")); }
}

const FLIP_ID = "sushila-g"; /* in the reviewed registry AND in the fixture tab */
const sheetFetch = require(join(ROOT, "tools", "sheet-fetch.js"));

function tsvEncode(rows) {
  return rows.map((r) => r.map((c) =>
    /[\t"\n\r]/.test(c) ? '"' + String(c).replace(/"/g, '""') + '"' : c
  ).join("\t")).join("\n") + "\n";
}

/* ---------- files any phase may touch (snapshot + restore) ---------- */
const TOUCHED = [
  "js/tutors/_overrides.js",
  "tutor/sushila-g/index.html", "tutor/shikha-dutta/index.html",
  "sitemap-tutors.xml", "sitemap.xml", "feed.xml",
  "find-tutors.html", "tutor/index.html",
  "llms.txt", "manifest.webmanifest", "404.html",
  "index.html",
  "es/index.html", "fr/index.html", "de/index.html", "pt/index.html",
  "ja/index.html", "ar/index.html"
];
const snapshot = new Map();
for (const f of TOUCHED) {
  try { snapshot.set(f, readFileSync(join(ROOT, f), "utf8")); }
  catch { snapshot.set(f, null); }
}

function run(cmd, args) {
  try {
    execFileSync(cmd, args, { cwd: ROOT, stdio: "pipe" });
  } catch (e) {
    throw new Error(cmd + " " + args.join(" ") + " failed:\n" +
      String(e.stderr || e.message).slice(-1500));
  }
}

function buildFixtures(activeYes) {
  const dir = mkdtempSync(join(tmpdir(), "ekguru-activation-"));
  cpSync(join(ROOT, "tests", "fixtures"), dir, { recursive: true });
  const p = join(dir, "tutors.tsv");
  if (activeYes) {
    /* flip ONLY the target row's active cell — through the shared parser,
       because the about/bio cells are multi-line (a line-based edit would
       miss the active column on the row's LAST physical line) */
    const rows = sheetFetch.parseTSV(readFileSync(p, "utf8"));
    const head = sheetFetch.headerOf(rows);
    const ai = head.indexOf("active");
    let flips = 0;
    for (const r of rows) {
      if (r[0] === FLIP_ID && ai > -1 && r[ai] === "no") { r[ai] = "yes"; flips++; }
    }
    if (flips !== 1) throw new Error("fixture flip failed: " + flips + " rows flipped");
    writeFileSync(p, tsvEncode(rows));
  }
  return dir;
}

function phase(activeYes) {
  const fixdir = buildFixtures(activeYes);
  try {
    run("node", ["tools/sheetsync.js", "--offline", fixdir]);
    run("node", ["tools/build-tutor-pages.js"]);
    run("node", ["tools/build-home-tutors.js"]);
    run("node", ["tools/build-market-pages.js"]);
    return siteData.loadSite();
  } finally {
    rmSync(fixdir, { recursive: true, force: true });
  }
}

function head(html) { return html.slice(0, html.indexOf("</head>")); }

try {
  /* =====================================================
     PHASE 1 — active=yes for FLIP_ID (the restore)
     ===================================================== */
  console.log("\n[phase 1] fixture row " + FLIP_ID + " flipped to active=yes");
  const site1 = phase(true);

  check("publicTutors contains " + FLIP_ID,
    site1.publicTutors.some((t) => t.id === FLIP_ID),
    "got " + site1.publicTutors.map((t) => t.id).join(","));
  check("the other rows stay hidden (shikha-dutta not public)",
    !site1.publicTutors.some((t) => t.id === "shikha-dutta"));

  const prof1 = readFileSync(join(ROOT, "tutor", FLIP_ID, "index.html"), "utf8");
  check("profile is indexable again", /content="index, follow/.test(head(prof1)));
  check("profile has no noindex", !/noindex/.test(head(prof1)));
  check("profile carries Person JSON-LD again", /"@type":\s*"Person"/.test(prof1));
  check("profile booking CTAs return (tutor.html?id=" + FLIP_ID + ")",
    new RegExp("tutor\\.html\\?id=" + FLIP_ID).test(prof1));
  check("profile has no hidden-notice markers", !/data-eg-hidden/.test(prof1));

  const sitemapT = readFileSync(join(ROOT, "sitemap-tutors.xml"), "utf8");
  check("sitemap-tutors.xml lists the profile", sitemapT.includes("/tutor/" + FLIP_ID + "/"));
  const sitemap = readFileSync(join(ROOT, "sitemap.xml"), "utf8");
  check("sitemap.xml lists the profile", sitemap.includes("/tutor/" + FLIP_ID + "/"));
  const feed = readFileSync(join(ROOT, "feed.xml"), "utf8");
  check("feed.xml carries the profile item", feed.includes("/tutor/" + FLIP_ID + "/"));

  const llms1 = readFileSync(join(ROOT, "llms.txt"), "utf8");
  check("llms.txt: Tutors listed: 1", /- Tutors listed: 1\n/.test(llms1));
  check("llms.txt: the tutor line is back", llms1.includes("ekguru.shop/tutor/" + FLIP_ID + "/"));
  const man1 = JSON.parse(readFileSync(join(ROOT, "manifest.webmanifest"), "utf8"));
  check("manifest: Book with shortcut returns",
    man1.shortcuts.some((s) => s.url.includes("id=" + FLIP_ID)));
  const f4041 = readFileSync(join(ROOT, "404.html"), "utf8");
  check("404.html links the profile again", f4041.includes("tutor/" + FLIP_ID + "/"));

  const ft1 = readFileSync(join(ROOT, "find-tutors.html"), "utf8");
  const list1 = JSON.parse(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/.exec(ft1)[1]);
  const itemList1 = (list1["@graph"] || []).find((n) => n["@type"] === "ItemList") || list1;
  check("find-tutors ItemList has 1 item again",
    itemList1.numberOfItems === 1 && JSON.stringify(itemList1.itemListElement).includes(FLIP_ID),
    "numberOfItems=" + itemList1.numberOfItems);

  const home1 = readFileSync(join(ROOT, "index.html"), "utf8");
  check("home card returns", home1.includes("tutor/" + FLIP_ID + "/"));
  check("home hero card shows the tutor again", /id="hero-tutor"[\s\S]{0,600}tutor\//.test(home1));
  check("home empty state gone", !/eg-empty|data-t-empty/.test(home1));
  const ar1 = readFileSync(join(ROOT, "ar", "index.html"), "utf8");
  check("market card returns (ar)", ar1.includes("tutor/" + FLIP_ID + "/"));

  /* =====================================================
     PHASE 2 — back to active=no (the zero state)
     ===================================================== */
  console.log("\n[phase 2] fixture row " + FLIP_ID + " back to active=no");
  const site2 = phase(false);

  check("publicTutors is empty again",
    site2.publicTutors.length === 0,
    "got " + site2.publicTutors.map((t) => t.id).join(","));

  const prof2 = readFileSync(join(ROOT, "tutor", FLIP_ID, "index.html"), "utf8");
  check("profile is noindex again", /<meta name="robots" content="noindex, follow">/.test(head(prof2)));
  check("profile drops Person JSON-LD (WebPage only)", /"@type":\s*"WebPage"/.test(prof2) && !/"@type":\s*"Person"/.test(prof2));
  check("booking surfaces off — no tutor.html?id anywhere", !/tutor\.html\?id=/.test(prof2));
  check("honest closed notice present", /data-eg-hidden="notice"/.test(prof2) && /data-eg-hidden="booking"/.test(prof2));
  check("free-course CTA instead", /learn\/hindi\//.test(prof2));

  const sitemapT2 = readFileSync(join(ROOT, "sitemap-tutors.xml"), "utf8");
  check("sitemap-tutors.xml has no profile URL", !/tutor\/[a-z0-9-]+\//.test(sitemapT2));
  const sitemap2 = readFileSync(join(ROOT, "sitemap.xml"), "utf8");
  check("sitemap.xml has no tutor profile URL", !sitemap2.includes("/tutor/" + FLIP_ID + "/"));
  const feed2 = readFileSync(join(ROOT, "feed.xml"), "utf8");
  check("feed.xml has no tutor item", !feed2.includes("/tutor/" + FLIP_ID + "/"));

  const llms2 = readFileSync(join(ROOT, "llms.txt"), "utf8");
  check("llms.txt: Tutors listed: 0", /- Tutors listed: 0\n/.test(llms2));
  check("llms.txt: no per-lesson price claim", !/from \$[\d.]+ per lesson/.test(llms2));
  check("llms.txt: no trial line", !/- Trial lessons:/.test(llms2));
  check("llms.txt: no price-range line", !/- Price range:/.test(llms2));
  check("llms.txt: no per-tutor link (the /tutor/ directory page may stay)",
    !/ekguru\.shop\/tutor\/[a-z0-9-]+\//.test(llms2));
  const man2 = JSON.parse(readFileSync(join(ROOT, "manifest.webmanifest"), "utf8"));
  check("manifest: no tutor shortcuts", !man2.shortcuts.some((s) => s.url.includes("tutor.html?id=")));
  check("manifest: free-course shortcut instead", man2.shortcuts.some((s) => s.url.includes("learn/hindi")));
  const f4042 = readFileSync(join(ROOT, "404.html"), "utf8");
  check("404.html has no tutor link", !f4042.includes("tutor/" + FLIP_ID + "/"));
  check("404.html: free course door", f4042.includes('href="learn/hindi/"'));

  const ft2 = readFileSync(join(ROOT, "find-tutors.html"), "utf8");
  const list2 = JSON.parse(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/.exec(ft2)[1]);
  const itemList2 = (list2["@graph"] || []).find((n) => n["@type"] === "ItemList") || list2;
  check("find-tutors ItemList is empty (numberOfItems 0)",
    itemList2.numberOfItems === 0 && itemList2.itemListElement.length === 0,
    "numberOfItems=" + itemList2.numberOfItems);
  const ti2 = readFileSync(join(ROOT, "tutor", "index.html"), "utf8");
  check("tutor/index ItemList is empty", !ti2.includes("tutor/" + FLIP_ID + "/"));

  const home2 = readFileSync(join(ROOT, "index.html"), "utf8");
  check("home: no tutor card", !home2.includes("tutor/" + FLIP_ID + "/"));
  check("home: hero card is the empty state",
    /id="hero-tutor" data-eg-empty="1"/.test(home2) && !/id="hero-tutor"[\s\S]*?tutor\/[a-z0-9-]+\//.test(home2));
  check("home: empty state present", /eg-empty|data-t-empty|emptyTutors|t-empty/.test(home2));
  check("home: free-course CTA", home2.includes("learn/hindi/"));
  const ar2 = readFileSync(join(ROOT, "ar", "index.html"), "utf8");
  check("market (ar): no tutor card", !ar2.includes("tutor/" + FLIP_ID + "/"));
  check("market (ar): free course link", ar2.includes("learn/hindi/"));

} finally {
  /* byte-for-byte restore of everything the phases touched */
  for (const [f, bytes] of snapshot) {
    const p = join(ROOT, f);
    if (bytes === null) { try { rmSync(p); } catch {} }
    else writeFileSync(p, bytes);
  }
  const restored = TOUCHED.every((f) => {
    try { return readFileSync(join(ROOT, f), "utf8") === snapshot.get(f); }
    catch { return snapshot.get(f) === null; }
  });
  console.log("\nworking tree restored: " + (restored ? "byte-for-byte" : "MISMATCH — inspect " + TOUCHED.join(", ")));
  if (!restored) failed++;
}

console.log("\n" + passed + " passed, " + failed + " failed");
process.exit(failed ? 1 : 0);
