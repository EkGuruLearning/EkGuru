#!/usr/bin/env node
/* EkGuru — Sheets sync (build side). Regenerates js/tutors/_overrides.js
   from the LIVE production Google Sheets.

   This is the generator the repo has been missing (referenced in the
   _overrides.js header and in js/sheet.js comments). It ports the SAME
   FIELDS transforms as js/sheet.js so the two parsers agree — see
   tools/test-data-sources.py and tools/test-sheet-loader.js.

   Outputs:
     js/tutors/_overrides.js   window.EKGURU_SHEET_OVERRIDES  (tutors + reviews)
                               window.EKGURU_SHEET_SETTINGS   (from settings tab)

   Privacy rule (matches js/sheet.js): an `email` cell is only written
   when it is a valid address; the production sheet intentionally keeps
   tutor emails blank so enquiries route via the site inbox / formKey,
   so a regenerated file never leaks a personal address.

   Run: node tools/sheetsync.js
*/
"use strict";
const fs = require("fs");
const path = require("path");

const BASE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIman_Um2wQrj_3mXqqgq4k69zzmJHkhZ1TRoAnh2jcamhzoo-0VeTd55UieGMi6mEaTl3Zy84G44h/pub";
const SRC = {
  tutors:   `${BASE}?gid=1631273256&single=true&output=csv`,
  reviews:  `${BASE}?gid=298809212&single=true&output=csv`,
  settings: `${BASE}?gid=1658518385&single=true&output=csv`,
  support:  `${BASE}?gid=1041390059&single=true&output=csv`,
};

/* ---------- delimited-text parsing (shared, see tools/sheet-fetch.js) ----------
   v143 (30 Sep 2026): the parser and the CSV→TSV fallback now live in
   tools/sheet-fetch.js — one implementation for the build, the offline
   fixtures and the unit tests (tools/test-sheet-fetch.mjs asserts this file
   and js/sheet.js agree). Google's published-CSV endpoints for this workbook
   answer HTTP 500 while output=tsv answers 200; the fallback order is
   csv first, tsv second, and it is not configurable. */
const SHEET_FETCH = require("./sheet-fetch");
const parseCSV = SHEET_FETCH.parseCSV;

function toRecords(rows) {
  if (rows.length < 2) return [];
  const head = rows[0].map(h => String(h).trim().toLowerCase());
  return rows.slice(1).map(r => {
    const o = {};
    head.forEach((h, i) => { if (h) o[h] = (r[i] || "").trim(); });
    return o;
    /* v104 — reviews rows carry `tutor`, not `id`. The old filter dropped
       the entire reviews tab, so buildReviews() always got [] and every
       baked `reviews` array was empty (review text rendered nowhere). */
  }).filter(o => o.id || o.tutor);
}

/* ---------- FIELDS transforms — ported from js/sheet.js ---------- */
const isEmail = v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(v || ""));
const yes = v => /^(yes|true|1|y)$/i.test(String(v || ""));

function normalizePhoto(v) {
  v = String(v == null ? "" : v).trim();
  if (!v) return null;
  let m = /drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?[^#]*id=|d\/)([A-Za-z0-9_-]{10,})/.exec(v);
  if (m) return "https://lh3.googleusercontent.com/d/" + m[1] + "=w800";
  m = /^https:\/\/lh\d\.googleusercontent\.com\/d\/([A-Za-z0-9_-]{10,})/.exec(v);
  if (m) return "https://lh3.googleusercontent.com/d/" + m[1] + "=w800";
  if (/^https:\/\/[^\s]+\.(jpg|jpeg|png|webp|avif)(\?[^\s]*)?$/i.test(v)) return v;
  if (/^https:\/\/(i\.imgur\.com|i\.ibb\.co|res\.cloudinary\.com|images\.unsplash\.com|lh\d\.googleusercontent\.com|[a-z0-9-]+\.githubusercontent\.com|[a-z0-9-]+\.supabase\.co|[a-z0-9-]+\.r2\.dev|[a-z0-9-]+\.imagekit\.io)\//i.test(v)) return v;
  if (/^images\/[A-Za-z0-9._-]+\.(jpg|jpeg|png|webp|avif)$/i.test(v)) return v;
  return null;
}

function parseAvailability(v) {
  const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  if (/^(none|closed|away)$/i.test(String(v).trim())) return {};
  const out = {};
  String(v).split(";").forEach(part => {
    part = part.trim();
    if (!part) return;
    const m = /^([A-Za-z]{3})\s*(?:-\s*([A-Za-z]{3}))?\s+(.+)$/.exec(part);
    if (!m) return;
    const norm = d => DAYS.find(x => x.toLowerCase() === d.toLowerCase());
    const a = norm(m[1]), b = m[2] ? norm(m[2]) : null;
    if (!a) return;
    const days = b ? DAYS.slice(DAYS.indexOf(a), DAYS.indexOf(b) + 1) : [a];
    const times = m[3].split(",").map(t => t.trim()).filter(t => {
      const hm = /^(\d{1,2}):(\d{2})$/.exec(t);
      if (!hm) return false;
      const h = +hm[1], mi = +hm[2];
      return h >= 0 && h <= 23 && mi >= 0 && mi <= 59;
    }).map(t => {
      const hm = /^(\d{1,2}):(\d{2})$/.exec(t);
      return (hm[1].length === 1 ? "0" + hm[1] : hm[1]) + ":" + hm[2];
    });
    if (!times.length) return;
    days.forEach(d => { out[d] = (out[d] || []).concat(times); });
  });
  if (!Object.keys(out).length) return null;
  const full = {};
  DAYS.forEach(d => { full[d] = out[d] || []; });
  return full;
}

const num = (v, min, max) => {
  const n = Number(v);
  if (!isFinite(n)) return null;
  if (min !== undefined && n < min) return null;
  if (max !== undefined && n > max) return null;
  return n;
};

const list = (v, cap) => String(v || "").split(",").map(x => x.trim()).filter(Boolean).slice(0, cap || 999);

function buildTutor(r) {
  const t = { id: String(r.id || "").trim().toLowerCase() };
  const set = (key, val) => { if (val !== null && val !== undefined && val !== "") t[key] = val; };

  set("name", r.name);
  set("nickname", r.nickname);
  set("headline", r.headline);
  set("city", r.city);
  set("country", r.country);
  set("timezone", r.timezone);
  set("subject", r.subject);
  set("lessonLength", r.lessonlength || r["lessonlength"]);
  if (isEmail(r.email)) set("email", String(r.email).trim());
  /* v101 — canonical operational email (RESET §11). Written into the
     tutor file so the mailer's notification_email() resolves it even
     before the sheet is fetched; never rendered on a public page. */
  if (isEmail(r.notification_email || r["notification_email"])) set("notification_email", String(r.notification_email || r["notification_email"]).trim());
  if (r.formkey && r.formkey.indexOf("@") < 0 && /^[A-Za-z0-9_-]{6,64}$/.test(r.formkey)) set("formKey", r.formkey);
  set("priceUSD", num(r.priceusd || r["priceusd"], 1, 2000));
  set("experienceYears", num(r.experienceyears || r["experienceyears"]));
  /* =========================================================
     REPUTATION-METRIC POLICY  (27 Sep 2026 master audit)
     Mirrors the runtime gate in js/sheet.js — the two parsers
     must agree (tools/test-sheet-loader.js asserts that).
     The sheet's rating / reviewsCount / lessonsCount /
     superTutor / preplyUrl cells are the owner's records only;
     the site publishes:
       · rating + reviewsCount derived from SITE-NATIVE
         reviews (buildReviews below, marketplace rows gated)
       · lessonsCount 0 — EkGuru has no lesson-delivery ledger
       · superTutor false — no EkGuru record earns the label
       · no external-marketplace profile links
     Baking them from the sheet is exactly how the removed
     marketplace values (5.0 / 3 / 40) would come back on the
     next sync.
     ========================================================= */
  if (r.video && String(r.video).length === 11) set("youtubeId", r.video);
  if (yes(r.trialavailable || r["trialavailable"])) set("trialAvailable", true);
  if (yes(r.verified)) set("verified", true);
  if (/^[a-z0-9-]+\/[a-z0-9-]+$/i.test(r.callink || "")) set("calLink", r.callink);
  const photo = normalizePhoto(r.photo); if (photo) set("photo", photo);
  const thumb = normalizePhoto(r.thumb); if (thumb) set("thumb", thumb);
  if (/^(none|no|remove|clear)$/i.test(String(r.banner).trim())) set("banner", "");
  else { const b = normalizePhoto(r.banner); if (b) set("banner", b); }
  const vt = String(r.videotitle || r["videotitle"] || "").trim();
  if (vt && vt.length <= 90 && vt.indexOf("|") === -1 && !/[\r\n]/.test(vt)) set("videoTitle", vt);
  if (/^[\uD83C][\uDDE6-\uDDFF][\uD83C][\uDDE6-\uDDFF]$/.test(String(r.countryflag || "").trim())) set("countryFlag", String(r.countryflag).trim());
  const tags = list(r.tags); if (tags.length) set("tags", tags);
  const teaches = list(r.teaches); if (teaches.length) set("teaches", teaches);
  const LEVELS = ["Beginner", "Intermediate", "Advanced"];
  const levels = list(r.levels).map(x => LEVELS.find(l => l.toLowerCase() === x.toLowerCase())).filter(Boolean);
  if (levels.length) set("levels", levels);
  const speaks = list(r.speaks).map(p => {
    const bits = p.split(":");
    const lang = (bits[0] || "").trim();
    return lang ? { lang, level: (bits[1] || "Fluent").trim() } : null;
  }).filter(Boolean);
  if (speaks.length) set("speaks", speaks);
  const about = String(r.about || "").split(/\r?\n/).map(x => x.trim()).filter(Boolean);
  if (about.length) set("about", about);
  const exp = String(r.experience || "").split(/\r?\n/).map(x => x.trim()).filter(Boolean);
  if (exp.length) set("experience", exp);
  const meth = String(r.methodology || "").split(/\r?\n/).map(line => {
    line = line.trim(); if (!line) return null;
    const i = line.indexOf("|");
    if (i === -1) return { title: line, desc: "" };
    return { title: line.slice(0, i).trim(), desc: line.slice(i + 1).trim() };
  }).filter(Boolean);
  if (meth.length) set("methodology", meth);
  const avail = parseAvailability(r.availability || "");
  if (avail) set("availability", avail);
  return t;
}

/* External-marketplace gate — build side of the same policy the
   runtime enforces in js/reviews.js (27 Sep 2026 master audit).
   A review row sourced from preply/italki is content that belongs
   to that marketplace; it is never baked into _overrides.js and
   never feeds a rating. Site-native sources publish as before. */
const MARKETPLACE_SOURCES = ["preply", "italki"];

function buildReviews(reviewRows) {
  const byTutor = {};
  for (const r of reviewRows) {
    if (String(r.tutor || "").charAt(0) === "#") continue;
    if (String(r.status || "live").toLowerCase() !== "live") continue;
    const src = String(r.source || "").trim().toLowerCase();
    if (MARKETPLACE_SOURCES.indexOf(src) !== -1) {
      console.warn(`  !! review for "${r.tutor}" (${r.name || "?"}) has external-marketplace source "${src}" — skipped (site-native reviews only, 27 Sep 2026 policy).`);
      continue;
    }
    const stars = Number(r.stars);
    if (!isFinite(stars) || stars < 1 || stars > 5) continue;
    const text = String(r.text || "").trim();
    if (!text || text.length < 40) continue;
    if (r.date && (!/^\d{4}-\d{2}-\d{2}$/.test(r.date) || new Date(r.date).getTime() > Date.now() + 86400000)) continue;
    const tid = String(r.tutor).trim().toLowerCase();
    (byTutor[tid] = byTutor[tid] || []).push({
      name: String(r.name).trim(),
      date: r.date || "",
      stars,
      text
    });
  }
  Object.values(byTutor).forEach(l => l.sort((a, b) => (b.date || "").localeCompare(a.date || "")));
  return byTutor;
}

/* CSV first, TSV fallback — see tools/sheet-fetch.js. Throws only when
   both formats fail (with both errors in the message). */
async function fetchRows(url, opts) {
  return SHEET_FETCH.fetchSheetRows((u) => fetch(u), url, opts);
}

async function fetchCSV(url) {
  const { rows, format, usedFallback } = await fetchRows(url);
  if (usedFallback) console.warn(`  !! ${url.split("gid=")[1] || url} answered via output=${format} (csv endpoint down) — tsv fallback.`);
  return toRecords(rows);
}

/* Settings tab has key/value rows, not an id column. */
async function fetchSettings(url) {
  const { rows, format, usedFallback } = await fetchRows(url, { allowKeyOnly: true });
  if (usedFallback) console.warn(`  !! settings/support tab answered via output=${format} (csv endpoint down) — tsv fallback.`);
  const head = (rows[0] || []).map(h => String(h).trim().toLowerCase());
  const ki = head.indexOf("key"), vi = head.indexOf("value");
  if (ki === -1 || vi === -1) return [];
  return rows.slice(1).map(r => ({ key: (r[ki] || "").trim(), value: (r[vi] || "").trim() }))
    .filter(o => o.key);
}

/* ---------- offline mode (--offline <dir>) ----------
   Reads a saved export instead of the network:
       <dir>/tutors.tsv  reviews.tsv  settings.tsv  support.tsv
   (.csv works too). Used by tools/test-tutor-activation.mjs and by
   builds in a sandbox where docs.google.com is unreachable. The
   parsing path is the SAME code the network path uses. */
function offlineRows(dir, name) {
  for (const ext of [".tsv", ".csv"]) {
    const p = path.join(dir, name + ext);
    if (fs.existsSync(p)) {
      return { rows: SHEET_FETCH.readLocalRows(fs.readFileSync(p, "utf8"), ext.slice(1)), file: p };
    }
  }
  throw new Error(`offline sheet input missing: ${name}.tsv (or .csv) in ${dir}`);
}

function offlineAll(dir) {
  const t = offlineRows(dir, "tutors");
  const r = offlineRows(dir, "reviews");
  const s = offlineRows(dir, "settings");
  const u = offlineRows(dir, "support");
  console.log(`  offline inputs: ${[t, r, s, u].map(x => path.relative(process.cwd(), x.file)).join(", ")}`);
  return {
    tutors: toRecords(t.rows),
    reviews: toRecords(r.rows),
    settings: keyValues(s.rows),
    support: keyValues(u.rows)
  };
}

function keyValues(rows) {
  const head = (rows[0] || []).map(h => String(h).trim().toLowerCase());
  const ki = head.indexOf("key"), vi = head.indexOf("value");
  if (ki === -1 || vi === -1) return [];
  return rows.slice(1).map(r => ({ key: (r[ki] || "").trim(), value: (r[vi] || "").trim() }))
    .filter(o => o.key);
}

/* The policy functions above are unit-tested directly by
   tools/test-sheetsync-policy.js (build-side of the 27 Sep 2026
   reputation gate). Requiring this file must not run the sync —
   only running it as a CLI does. */
if (require.main === module) (async function main() {
  /* --offline <dir>: read a saved export (tests/fixtures/, a downloaded
     snapshot) instead of the network. Same parsers, same output. */
  const argv = process.argv.slice(2);
  const offIdx = argv.indexOf("--offline");
  let tutors, reviews, settings, support;
  if (offIdx > -1 && argv[offIdx + 1]) {
    const src = offlineAll(argv[offIdx + 1]);
    tutors = src.tutors; reviews = src.reviews; settings = src.settings; support = src.support;
  } else {
    [tutors, reviews, settings, support] = await Promise.all([
      fetchCSV(SRC.tutors), fetchCSV(SRC.reviews), fetchSettings(SRC.settings),
      fetchSettings(SRC.support),
    ]);
  }
  /* Support tab merges UNDER the main settings tab: on a conflict
     the main tab wins, so payments can only ADD keys. */
  const have = new Set(settings.map(s => String(s.key || "").toLowerCase()));
  for (const s of support) {
    const k = String(s.key || "").trim();
    if (k && !have.has(k.toLowerCase())) {
      settings.push({ key: k, value: s.value }); have.add(k.toLowerCase());
    }
  }

  const reviewMap = buildReviews(reviews);
  const overrides = {};
  const hidden = [];
  const HIDE_RE = /^(no|false|0|n|hidden)$/i;
  for (const row of tutors) {
    const id = String(row.id || "").trim().toLowerCase();
    if (!id || id.charAt(0) === "#") continue;   // the #help row
    /* v130 — active=no hides the tutor everywhere. No overrides are
       baked for them, and the id joins EKGURU_SHEET_HIDDEN so the
       FIRST paint — before the live sheet arrives — already excludes
       them. Before this, hidden tutors were baked with fresh data
       and flashed visible on every page load. */
    if (HIDE_RE.test(String(row.active || "yes").trim())) { hidden.push(id); continue; }
    /* The availability column holds time slots, not a switch. A bare
       "no" there parses to nothing and is silently ignored — which
       reads as "the sheet did nothing". Say so at build time. */
    if (/^(no|n|false|0)$/i.test(String(row.availability || "").trim())) {
      console.warn(`  !! "${id}": availability="${row.availability}" does nothing — to hide this tutor set active=no.`);
    }
    const t = buildTutor(row);
    if (!t.name) continue;                    // a tutor needs a name
    delete t.id;
    const revs = reviewMap[id] || [];
    if (revs.length) {
      t.reviews = revs;
      t.reviewsCount = revs.length;
      t.rating = revs.reduce((n, x) => n + x.stars, 0) / revs.length;
    } else {
      t.reviews = [];
      if (t.reviewsCount === undefined) t.reviewsCount = 0;
      if (t.rating === undefined) t.rating = 0;
    }
    overrides[id] = t;
  }

  const settingsObj = {};
  for (const s of settings) {
    const k = String(s.key || "").trim();
    const v = String(s.value || "").trim();
    if (!k || k.charAt(0) === "#" || !v) continue;
    settingsObj[k] = v;
  }

  const out =
`/* =========================================================
   EkGuru — SHEET OVERRIDES  (GENERATED — DO NOT EDIT)
   ---------------------------------------------------------
   Written by tools/sheetsync.js from the Google Sheet on
   ${new Date().toISOString()}.

   Loaded AFTER the hand-written tutor files, so the sheet
   wins. Delete this file and the site falls back to those
   files, which is exactly what happens when the sheet is
   unreachable.

   Edit the spreadsheet, not this file. Anything typed here
   is overwritten on the next build.

   Privacy: tutor emails are NOT written here. The production
   sheet keeps the email column blank (enquiries route via
   the site inbox or a formKey alias), so this file carries
   no personal addresses. Regenerate with:
       node tools/sheetsync.js
   ========================================================= */
window.EKGURU_SHEET_OVERRIDES = ${JSON.stringify(overrides, null, 2)};
window.EKGURU_SHEET_SETTINGS = ${JSON.stringify(settingsObj, null, 2)};
/* v130 — ids whose sheet row says active=no, as of this build.
   js/tutors-data.js excludes them from the first paint; the live
   sheet then corrects both ways at runtime. Keep this line AFTER
   SETTINGS: tools/gate.js expects OVERRIDES and SETTINGS adjacent. */
window.EKGURU_SHEET_HIDDEN = ${JSON.stringify(hidden)};
`;
  const target = path.join(__dirname, "..", "js", "tutors", "_overrides.js");
  fs.writeFileSync(target, out);
  console.log(`Wrote ${path.relative(process.cwd(), target)}`);
  console.log(`  tutors: ${Object.keys(overrides).join(", ")}`);
  console.log(`  hidden (active=no): ${hidden.join(", ") || "(none)"}`);
  console.log(`  settings: ${Object.keys(settingsObj).join(", ")}`);
  console.log(`  emails written: ${Object.values(overrides).filter(t => t.email).length}`);
})();

module.exports = { buildTutor, buildReviews, MARKETPLACE_SOURCES };
