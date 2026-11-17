#!/usr/bin/env node
/* =========================================================
   EkGuru — REAL-LIFE SHEET CYCLE TESTS  (16 Nov 2026)
   ---------------------------------------------------------
   Plays the owner's day with the production pages in jsdom:

     · the live profile page tutor/<id>/index.html and the roster
       page find-tutors.html load exactly as shipped
     · "Google" is a fake fetch that answers the published tab
       URLs with whatever the owner has in the sheet RIGHT NOW
     · every scenario is a real sequence a human performs:
         1. three live reviews                → 3 printed, 4.7 ★
         2. owner deletes EVERY review row    → "No reviews yet", 0 ★
            (header only — the #help row went too)
         3. owner deletes rows, keeps #help   → same honest zero
         4. owner writes ONE new review       → exactly that one, 5 ★
         5. owner hides it (status=hidden)    → gone again
         6. returning visitor with a warm
            localStorage cache sees the sheet,
            not yesterday's cache            → (the bug this file found)
         7. tutor active=no then active=yes   → roster hides / restores
         8. price edit in the sheet           → page follows

   Deterministic, no network. Run:
       node tools/test-real-life-sheet-cycle.mjs
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.resolve(import.meta.dirname, "..");

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log("PASS  " + name); }
  else { fail++; console.log("FAIL  " + name + (extra ? "  -- " + extra : "")); }
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* ---------- the sheet, as the owner sees it ---------- */
const REVIEW_HEAD = ["tutor", "name", "date", "stars", "text", "source", "status"];
const HELP_ROW = ["#help", "first name", "YYYY-MM-DD", "1 to 5", "what they wrote", "email / whatsapp / google", "live or hidden"];
const THREE = [
  ["sushila-g", "Riya", "2026-09-15", "5", "Sushila explains Hindi grammar very clearly. My daughter reads simple sentences now.", "whatsapp", "live"],
  ["sushila-g", "Aarav", "2026-09-28", "4", "Good conversational practice. I feel more confident speaking now.", "email", "live"],
  ["sushila-g", "Mei", "2026-10-02", "5", "Patient teacher, clear pronunciation, lessons are well structured.", "google", "live"]
];
const NEW_ONE = [["sushila-g", "Tomás", "2026-11-10", "5", "Booked through EkGuru, three lessons in and I can already introduce myself in Hindi.", "email", "live"]];

const TUTORS_TSV = fs.readFileSync(path.join(ROOT, "tests/fixtures/tutors.tsv"), "utf8");
/* Registry ids (approved tutors). The fixture sheet has NO row for some
   of them (deepika, utkarsh-upadhyay) — exactly the production shape. */
const REGISTRY = (fs.readFileSync(path.join(ROOT, "js/tutors/_registry.js"), "utf8").match(/"([a-z0-9-]+)"/g) || [])
  .map((x) => x.replace(/"/g, "")).filter((id) => fs.existsSync(path.join(ROOT, "js/tutors", id + ".js")));
/* 17 Nov 2026 — the sheet is the roster: approved=yes rows with no tutor
   file are baked into window.EKGURU_SHEET_TUTORS (js/tutors/_overrides.js).
   In production every one of them HAS a sheet row, so "the owner sets every
   row to active=no" must cover them too — otherwise the fixture, not the
   site, would be keeping them visible. */
const SHEET_BAKED = (() => {
  const ov = fs.readFileSync(path.join(ROOT, "js/tutors/_overrides.js"), "utf8");
  const m = /window\.EKGURU_SHEET_TUTORS\s*=\s*(\[[\s\S]*?\n\]);/.exec(ov);
  try { return m ? JSON.parse(m[1]).map((t) => t.id) : []; } catch (e) { return []; }
})();
const ALL_PUBLIC = Array.from(new Set(REGISTRY.concat(SHEET_BAKED)));
/* Quote-aware TSV: the fixture (like Google's TSV export) wraps a cell that
   holds a newline, tab or quote in double quotes and doubles inner quotes.
   Splitting on "\n" treated every continuation line of a tutor's bio as a
   row of its own, so dropping or editing a tutor left orphan lines that
   js/sheet.js then read as garbage ids. Parse records, mutate, re-encode. */
function parseTSV(text) {
  const rows = []; let row = [], cell = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; }
      else cell += c;
    } else if (c === '"' && cell === "") q = true;
    else if (c === "\t") { row.push(cell); cell = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(cell); rows.push(row); row = []; cell = "";
    } else cell += c;
  }
  if (cell !== "" || row.length) { row.push(cell); rows.push(row); }
  return rows.filter((r) => r.length > 1 || (r[0] || "").trim());
}
const tsvCell = (v) => (/[\t\n\r"]/.test(v) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v));
const TUTOR_ROWS = parseTSV(TUTORS_TSV);
function tutorsSheet(mut, opts) {
  opts = opts || {};
  const head = TUTOR_ROWS[0].slice();
  let rows = TUTOR_ROWS.slice(1).map((r) => { const c = r.slice(); while (c.length < head.length) c.push(""); return c; });
  if (opts.drop) rows = rows.filter((r) => !opts.drop.includes(r[0]));
  /* allNo: give EVERY public tutor a row that says active=no — the only
     way to hide an approved tutor (owner rule, 16 Nov 2026). */
  if (opts.allNo) {
    ALL_PUBLIC.forEach((id) => {
      if (rows.some((r) => r[0] === id)) return;
      const r = head.map(() => ""); r[0] = id; r[head.indexOf("active")] = "no"; r[head.indexOf("name")] = id;
      rows.push(r);
    });
    rows.forEach((r) => { if (r[0] !== "#help") r[head.indexOf("active")] = "no"; });
  }
  if (mut) rows.forEach((r) => mut(Object.fromEntries(head.map((h, i) => [h, r[i]])), r, head));
  return [head].concat(rows).map((r) => r.map(tsvCell).join("\t")).join("\n");
}
function setCell(row, cells, head, key, val) { const i = head.indexOf(key); if (i >= 0) cells[i] = val; }

const csv = (rows) => rows.map((r) => r.map((c) => '"' + String(c).replace(/"/g, '""') + '"').join(",")).join("\n");

/* "Google" — the Apps Script feed answers `?tab=reviews` with the public
   shape of reviews_pending (17 Nov 2026: ONE review tab, served only by
   the feed, apps-script/Unified.gs feedGet_). The old published `reviews`
   tab (gid 293675115) was deleted, so it answers 404 like the real one.
   The tutors tab still answers TSV (CSV 500s, as live). Anything else is
   offline. */
const FEED_EXEC = "https://script.google.com/macros/s/AKfycbTESTFEEDsushila/exec";
function makeGoogle(state) {
  const log = [];
  const fetch = (u) => {
    u = String(u);
    log.push(u);
    const resp = (body) => Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve(body) });
    const fail = (code) => Promise.resolve({ ok: false, status: code, text: () => Promise.resolve("") });
    if (u.indexOf(FEED_EXEC + "?tab=reviews") === 0) {   /* the feed */
      if (state.reviewsDown) return Promise.reject(new Error("offline"));
      return resp(csv([REVIEW_HEAD].concat(state.reviews)));
    }
    if (/gid=293675115/.test(u)) { log.push("DEAD_TAB"); return fail(404); }
    if (/gid=1631273256/.test(u)) {              /* tutors tab */
      if (state.tutorsDown) return Promise.reject(new Error("offline"));
      /* The real workbook answers HTTP 500 on output=csv and 200 on
         output=tsv (js/sheet.js carries that fallback). Serving the
         TSV verbatim also keeps the fixture's multi-line quoted bio
         cells intact — a naive CSV re-encode split them into junk rows. */
      if (/output=csv/.test(u)) return fail(500);
      return resp(tutorsSheet(state.tutorMut, { allNo: state.allNo, drop: state.drop }));
    }
    if (/live-sheets\/reviews\.csv/.test(u)) { log.push("SNAPSHOT"); return fail(404); }
    return Promise.reject(new Error("offline"));
  };
  return { fetch, log };
}

function resolveScript(src, pageRel) {
  if (src.startsWith("/")) return src.slice(1);
  if (/^https?:/.test(src)) return null;
  return path.normalize(path.join(path.dirname(pageRel), src));
}

const STORAGE = new Map();   /* survives across page loads, like a browser */
function fakeStorage() {
  return {
    getItem: (k) => (STORAGE.has(k) ? STORAGE.get(k) : null),
    setItem: (k, v) => STORAGE.set(k, String(v)),
    removeItem: (k) => STORAGE.delete(k),
    clear: () => STORAGE.clear(),
    key: (i) => Array.from(STORAGE.keys())[i] || null,
    get length() { return STORAGE.size; }
  };
}

async function loadPage(rel, url, google, { settle = 400 } = {}) {
  const html = fs.readFileSync(path.join(ROOT, rel), "utf8");
  const dom = new JSDOM(html, { url, runScripts: "outside-only", pretendToBeVisual: true });
  const win = dom.window;
  win.fetch = google.fetch;
  Object.defineProperty(win, "localStorage", { value: fakeStorage(), configurable: true });
  Object.defineProperty(win, "sessionStorage", { value: fakeStorage(), configurable: true });
  win.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
  win.matchMedia = win.matchMedia || ((q) => ({ matches: false, media: q, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} }));
  win.scrollTo = () => {};
  win.console = { log() {}, info() {}, warn() {}, error() {}, debug() {} };
  const errors = [];
  for (const s of [...win.document.querySelectorAll("script[src]")]) {
    const p = resolveScript(s.getAttribute("src"), rel);
    if (p === null) continue;
    const file = path.join(ROOT, p);
    if (!fs.existsSync(file)) continue;
    try { win.eval(fs.readFileSync(file, "utf8")); } catch (e) { errors.push(p + ": " + String(e && e.message).slice(0, 100)); }
    /* The owner has deployed the feed (js/site-config.js feed.url is the
       /exec address). Set it the moment the config is on the page, before
       js/reviews.js reads it — exactly what the deployed site does. */
    if (/js\/site-config\.js$/.test(p) && win.EKGURU_SITE) {
      win.EKGURU_SITE.feed = Object.assign({}, win.EKGURU_SITE.feed || {}, { url: FEED_EXEC, cacheSeconds: 30 });
    }
  }
  win.document.dispatchEvent(new win.Event("DOMContentLoaded", { bubbles: true }));
  win.dispatchEvent(new win.Event("load"));
  await sleep(settle);
  return { win, errors, close: () => dom.window.close() };
}

function profileReviews(win) {
  const host = win.document.querySelector('[data-eg-reviews][data-tutor="sushila-g"]');
  const cards = host ? host.querySelectorAll("article.rev") : [];
  const names = Array.from(cards).map((c) => c.querySelector("b").textContent.trim());
  const empty = host && /No reviews yet/.test(host.textContent);
  const f = (win.EKGURU_TUTOR_FILES || {})["sushila-g"] || {};
  return { count: cards.length, names, empty: !!empty, rating: f.rating || 0, reviewsCount: f.reviewsCount || 0 };
}

const PROFILE = "tutor/sushila-g/index.html";
const PROFILE_URL = "https://ekguru.shop/tutor/sushila-g/";

/* ================= 1. three live reviews ================= */
console.log("\n== 1. Three live reviews in the sheet ==");
STORAGE.clear();
{
  const g = makeGoogle({ reviews: [HELP_ROW].concat(THREE) });
  const { win, errors, close } = await loadPage(PROFILE, PROFILE_URL, g);
  const r = profileReviews(win);
  ok("profile page loads without script errors", errors.length === 0, errors.join(" | "));
  ok("three reviews printed", r.count === 3, JSON.stringify(r));
  ok("newest first (Mei, Aarav, Riya)", r.names.join(",") === "Mei,Aarav,Riya", r.names.join(","));
  ok("rating is the real average 4.7", r.rating === 4.7, String(r.rating));
  ok("the dead snapshot URL is NOT requested while the sheet answers", !g.log.includes("SNAPSHOT"));
  ok("cache written for the next visit", STORAGE.has("ekguru_reviews_v2"));
  close();
}

/* ====== 2. owner deletes EVERY row — header only remains ====== */
console.log("\n== 2. Owner deletes every review row (header only) ==");
{
  const g = makeGoogle({ reviews: [] });
  const { win, close } = await loadPage(PROFILE, PROFILE_URL, g);
  const r = profileReviews(win);
  ok("returning visitor sees NO reviews after the owner emptied the tab", r.count === 0 && r.empty, JSON.stringify(r));
  ok("rating back to 0 (no fabricated stars)", r.rating === 0 && r.reviewsCount === 0, JSON.stringify(r));
  ok("reviews loader reports the empty tab as loaded, not as an error", win.EKGURU_REVIEWS_INFO && win.EKGURU_REVIEWS_INFO.loaded === true, JSON.stringify(win.EKGURU_REVIEWS_INFO));
  ok("empty tab did NOT fall through to the dead snapshot", !g.log.includes("SNAPSHOT"));
  const cached = STORAGE.get("ekguru_reviews_v2");
  ok("localStorage cache now holds the empty sheet (no zombie reviews for tomorrow)", cached && JSON.parse(cached).recs.length === 0, String(cached).slice(0, 120));
  close();
}

/* ====== 2b. first-time visitor, cold cache, empty tab ====== */
console.log("\n== 2b. Brand-new visitor, cold cache, empty tab ==");
STORAGE.clear();
{
  const g = makeGoogle({ reviews: [] });
  const { win, close } = await loadPage(PROFILE, PROFILE_URL, g);
  const r = profileReviews(win);
  ok("cold visitor: honest 'No reviews yet'", r.count === 0 && r.empty, JSON.stringify(r));
  close();
}

/* ====== 3. rows deleted, #help row kept ====== */
console.log("\n== 3. Owner deletes the reviews but keeps the #help row ==");
STORAGE.clear();
{
  const g = makeGoogle({ reviews: [HELP_ROW] });
  const { win, close } = await loadPage(PROFILE, PROFILE_URL, g);
  const r = profileReviews(win);
  ok("help row alone publishes nothing", r.count === 0 && r.empty, JSON.stringify(r));
  close();
}

/* ====== 4. owner writes ONE new review ====== */
console.log("\n== 4. Owner writes one new review ==");
{
  const g = makeGoogle({ reviews: [HELP_ROW].concat(NEW_ONE) });
  const { win, close } = await loadPage(PROFILE, PROFILE_URL, g);
  const r = profileReviews(win);
  ok("exactly the new review is printed", r.count === 1 && r.names[0] === "Tomás", JSON.stringify(r));
  ok("rating 5.0 from one 5★ review", r.rating === 5 && r.reviewsCount === 1, JSON.stringify(r));
  const txt = win.document.querySelector('[data-eg-reviews] .rev-text').textContent;
  ok("review text is printed verbatim (accents survive)", /introduce myself in Hindi/.test(txt) && r.names[0] === "Tomás");
  close();
}

/* ====== 5. owner hides it ====== */
console.log("\n== 5. Owner sets status=hidden on that review ==");
{
  const hidden = NEW_ONE.map((r) => r.slice(0, 6).concat(["hidden"]));
  const g = makeGoogle({ reviews: [HELP_ROW].concat(hidden) });
  const { win, close } = await loadPage(PROFILE, PROFILE_URL, g);
  const r = profileReviews(win);
  ok("hidden review disappears from the page", r.count === 0 && r.empty, JSON.stringify(r));
  ok("hidden review no longer feeds the rating", r.rating === 0, String(r.rating));
  close();
}

/* ====== 6. warm cache, then the sheet empties, Google answers ====== */
console.log("\n== 6. Warm cache from yesterday, owner emptied the tab overnight ==");
STORAGE.clear();
{
  const g1 = makeGoogle({ reviews: [HELP_ROW].concat(THREE) });
  const p1 = await loadPage(PROFILE, PROFILE_URL, g1);
  ok("day 1: three reviews cached", profileReviews(p1.win).count === 3);
  p1.close();
  const g2 = makeGoogle({ reviews: [] });
  const p2 = await loadPage(PROFILE, PROFILE_URL, g2);
  const r = profileReviews(p2.win);
  ok("day 2: the page shows the SHEET (0), not yesterday's cache (3)", r.count === 0 && r.empty, JSON.stringify(r));
  p2.close();
}

/* ====== 6b. warm cache, Google unreachable: cache is the best we have ====== */
console.log("\n== 6b. Warm cache, Google unreachable ==");
STORAGE.clear();
{
  const g1 = makeGoogle({ reviews: [HELP_ROW].concat(THREE) });
  (await loadPage(PROFILE, PROFILE_URL, g1)).close();
  const g2 = makeGoogle({ reviews: [], reviewsDown: true });
  const p2 = await loadPage(PROFILE, PROFILE_URL, g2);
  const r = profileReviews(p2.win);
  ok("offline: the last good copy still paints (3)", r.count === 3, JSON.stringify(r));
  ok("offline: loader reports loaded:false honestly", p2.win.EKGURU_REVIEWS_INFO && p2.win.EKGURU_REVIEWS_INFO.loaded === false);
  p2.close();
}

/* ====== 7. roster: tutor active=no / active=yes ====== */
console.log("\n== 7. Roster page: owner flips sushila-g active=yes, then no ==");
STORAGE.clear();
const ROSTER = "find-tutors.html", ROSTER_URL = "https://ekguru.shop/find-tutors.html";
function rosterIds(win) {
  return (win.EKGURU_TUTORS || []).map((t) => t.id);
}
{
  const g = makeGoogle({ reviews: [HELP_ROW].concat(THREE), tutorMut: (o, cells, head) => { if (o.id === "sushila-g") setCell(o, cells, head, "active", "yes"); } });
  const { win, errors, close } = await loadPage(ROSTER, ROSTER_URL, g, { settle: 900 });
  ok("roster page loads without script errors", errors.length === 0, errors.join(" | "));
  const ids = rosterIds(win);
  ok("active=yes: sushila-g is on the public roster", ids.includes("sushila-g"), ids.join(","));
  const t = (win.EKGURU_TUTORS || []).find((x) => x.id === "sushila-g") || {};
  ok("roster card carries the sheet's reviews (3, 4.7★)", t.reviewsCount === 3 && t.rating === 4.7, JSON.stringify({ c: t.reviewsCount, r: t.rating }));
  close();
}
{
  const g = makeGoogle({ reviews: [HELP_ROW].concat(THREE), tutorMut: (o, cells, head) => { if (o.id === "sushila-g") setCell(o, cells, head, "active", "no"); } });
  const { win, close } = await loadPage(ROSTER, ROSTER_URL, g, { settle: 900 });
  const ids = rosterIds(win);
  ok("active=no: sushila-g is hidden from the public roster", !ids.includes("sushila-g"), ids.join(","));
  close();
}

/* ====== 8. price edit ====== */
console.log("\n== 8. Owner changes the price 6 -> 9 ==");
STORAGE.clear();
{
  const g = makeGoogle({ reviews: [HELP_ROW], tutorMut: (o, cells, head) => { if (o.id === "sushila-g") { setCell(o, cells, head, "active", "yes"); setCell(o, cells, head, "priceUSD", "9"); } } });
  const { win, close } = await loadPage(PROFILE, PROFILE_URL, g, { settle: 900 });
  const el = win.document.querySelector('[data-t="sushila-g"][data-f="priceUSD"]');
  ok("profile price cell follows the sheet", el && /9/.test(el.textContent) && !/\b6\b/.test(el.textContent), el && el.textContent);
  close();
}

/* ====== 9. owner empties the TUTORS tab (header only) ====== */
console.log("\n== 9. Owner empties the tutors tab (header only) -> approved tutors show, no overrides ==");
STORAGE.clear();
{
  /* day 1: sushila-g public */
  const g1 = makeGoogle({ reviews: [HELP_ROW], tutorMut: (o, cells, head) => { if (o.id === "sushila-g") setCell(o, cells, head, "active", "yes"); } });
  const p1 = await loadPage(ROSTER, ROSTER_URL, g1, { settle: 900 });
  ok("day 1: sushila-g on the roster", rosterIds(p1.win).includes("sushila-g"));
  p1.close();
  /* day 2: the tab is a lone header */
  const g2 = makeGoogle({ reviews: [HELP_ROW], tutorMut: null });
  g2.fetch = ((orig) => (u) => (/gid=1631273256/.test(String(u))
    ? Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve(TUTORS_TSV.split("\n")[0].split("\t").join(/output=tsv/.test(String(u)) ? "\t" : ",")) })
    : orig(u)))(g2.fetch);
  const p2 = await loadPage(ROSTER, ROSTER_URL, g2, { settle: 900 });
  ok("day 2: header-only tutors tab -> no script errors", p2.errors.length === 0, p2.errors.join(" | "));
  ok("day 2: every approved (registry) tutor shows with file values — nobody is hidden without an active=no row", REGISTRY.every((id) => rosterIds(p2.win).includes(id)), rosterIds(p2.win).join(","));
  ok("day 2: loader reports loaded:true with 0 rows", p2.win.EKGURU_SHEET_INFO && p2.win.EKGURU_SHEET_INFO.loaded === true && p2.win.EKGURU_SHEET_INFO.rows === 0, JSON.stringify(p2.win.EKGURU_SHEET_INFO));
  p2.close();
}

/* ====== 10. EVERY tutor profile: write one -> shows, delete -> gone ====== */
console.log("\n== 10. Every tutor profile with a review section: write -> shows, delete -> gone ==");
const allTutors = fs.readdirSync(path.join(ROOT, "tutor")).filter((id) => {
  const f = path.join(ROOT, "tutor", id, "index.html");
  return fs.existsSync(f) && /data-eg-reviews/.test(fs.readFileSync(f, "utf8"));
});
ok("at least 4 tutor profiles carry a review section", allTutors.length >= 4, allTutors.join(","));
for (const id of allTutors) {
  STORAGE.clear();
  const rel = "tutor/" + id + "/index.html", url = "https://ekguru.shop/tutor/" + id + "/";
  const one = [[id, "Student " + id.slice(0, 3), "2026-11-12", "4", "Clear, patient lessons — booked through EkGuru and happy to recommend " + id + ".", "email", "live"]];
  const host = (win) => win.document.querySelector('[data-eg-reviews][data-tutor="' + id + '"]');
  const g1 = makeGoogle({ reviews: [HELP_ROW].concat(one) });
  const p1 = await loadPage(rel, url, g1);
  const h1 = host(p1.win);
  ok(id + ": new review shows (1 card, 4★)", h1 && h1.querySelectorAll("article.rev").length === 1 && /★★★★☆/.test(h1.textContent), h1 && h1.textContent.slice(0, 80));
  ok(id + ": no script errors", p1.errors.length === 0, p1.errors.join(" | "));
  p1.close();
  const g2 = makeGoogle({ reviews: [] });
  const p2 = await loadPage(rel, url, g2);
  const h2 = host(p2.win);
  ok(id + ": after delete-all the same visitor sees 'No reviews yet'", h2 && h2.querySelectorAll("article.rev").length === 0 && /No reviews yet/.test(h2.textContent), h2 && h2.textContent.slice(0, 80));
  p2.close();
}

/* ====== 11. Translated rosters follow the sheet too ====== */
console.log("\n== 11. es/fr/de/pt/ja/ar find-tutors: all tutors active=no -> no cards, honest zero state; one active -> only that card ==");
const EXPECT_EMPTY = { es: /no hay tutores/i, fr: /Aucun tuteur/i, de: /keine Tutoren/i, pt: /Nenhum tutor/i, ja: /講師はいません/, ar: /لا يوجد معلّمون/ };
for (const lang of Object.keys(EXPECT_EMPTY)) {
  const rel = lang + "/find-tutors.html", url = "https://ekguru.shop/" + lang + "/find-tutors.html";
  if (!fs.existsSync(path.join(ROOT, rel))) { ok(lang + " roster page exists", false); continue; }
  STORAGE.clear();
  /* every approved tutor has a row saying active=no */
  const gAll = makeGoogle({ reviews: [], allNo: true });
  const pA = await loadPage(rel, url, gAll, { settle: 1200 });
  const cardsA = pA.win.document.querySelectorAll("[data-t-row]");
  const grid = pA.win.document.querySelector(".lp-cards");
  ok(lang + ": every tutor active=no -> zero tutor cards on the translated roster", cardsA.length === 0, Array.from(cardsA).map((c) => c.getAttribute("data-t-row")).join(","));
  ok(lang + ": the empty grid says so in " + lang, grid && EXPECT_EMPTY[lang].test(grid.textContent), grid && grid.textContent.replace(/\s+/g, " ").slice(0, 100));
  ok(lang + ": zero state links to the free course (../learn/hindi/)", grid && !!grid.querySelector('a[href="../learn/hindi/"]'));
  ok(lang + ": no script errors", pA.errors.length === 0, pA.errors.join(" | "));
  pA.close();
  STORAGE.clear();
  const gOne = makeGoogle({ reviews: [], allNo: true, tutorMut: (o, cells, head) => { if (o.id === "sushila-g") setCell(o, cells, head, "active", "yes"); } });
  const pB = await loadPage(rel, url, gOne, { settle: 1200 });
  const idsB = Array.from(pB.win.document.querySelectorAll("[data-t-row]")).map((c) => c.getAttribute("data-t-row"));
  ok(lang + ": sushila-g active=yes -> exactly her card remains, no zero state", idsB.join(",") === "sushila-g" && !pB.win.document.querySelector("[data-eg-empty]"), idsB.join(","));
  pB.close();
}

/* ====== 12. List-less pages (city page, text directory, profile "other tutors") follow the same rule ====== */
console.log("\n== 12. City page / text directory / profile 'other tutors': only active=no removes; offline never empties ==");
for (const [rel, url] of [["hindi-tutor/worldwide/index.html", "https://ekguru.shop/hindi-tutor/worldwide/"], ["tutor/index.html", "https://ekguru.shop/tutor/"], ["tutor/sushila-g/index.html", PROFILE_URL]]) {
  const rowsOf = (d) => Array.from(d.querySelectorAll("[data-t-row]")).filter((e) => e.style.display !== "none").map((e) => e.getAttribute("data-t-row"));
  STORAGE.clear();
  let p = await loadPage(rel, url, makeGoogle({ reviews: [], allNo: true }), { settle: 1200 });
  ok(rel + ": every tutor active=no -> no tutor rows remain", rowsOf(p.win.document).length === 0, rowsOf(p.win.document).join(","));
  ok(rel + ": the emptied list says so", !!p.win.document.querySelector("[data-eg-empty]"));
  ok(rel + ": no script errors", p.errors.length === 0, p.errors.join(" | "));
  p.close();
  STORAGE.clear();
  p = await loadPage(rel, url, makeGoogle({ reviews: [], allNo: true, tutorMut: (o, c, h) => { if (o.id === "sushila-g" || o.id === "shikha-dutta") setCell(o, c, h, "active", "yes"); } }), { settle: 1200 });
  const want = rel.includes("sushila-g") ? "shikha-dutta" : "sushila-g,shikha-dutta";
  ok(rel + ": two active -> exactly those rows, in sheet order", rowsOf(p.win.document).join(",") === want, rowsOf(p.win.document).join(","));
  p.close();
  STORAGE.clear();
  p = await loadPage(rel, url, makeGoogle({ reviews: [], tutorsDown: true }), { settle: 1200 });
  ok(rel + ": Google unreachable -> the page is NOT emptied", rowsOf(p.win.document).length >= 1 && !p.win.document.querySelector("[data-eg-empty]"), rowsOf(p.win.document).join(","));
  p.close();
}

/* ====== 13. OWNER RULE: approved tutor with NO sheet row is visible ====== */
console.log("\n== 13. Approved (registry) tutor with no sheet row at all -> visible everywhere; active=no row -> hidden ==");
{
  const noRow = REGISTRY.filter((id) => !TUTOR_ROWS.some((r) => r[0] === id));
  ok("the fixture really lacks rows for some approved tutors (production shape)", noRow.length >= 1, noRow.join(","));
  STORAGE.clear();
  /* sheet: only sushila-g active=yes; shikha-dutta + pinky-kumari rows REMOVED */
  const g = makeGoogle({ reviews: [], drop: ["shikha-dutta", "pinky-kumari"], tutorMut: (o, c, h) => { if (o.id === "sushila-g") setCell(o, c, h, "active", "yes"); } });
  const pR = await loadPage(ROSTER, ROSTER_URL, g, { settle: 1200 });
  const ids = rosterIds(pR.win);
  ok("English roster: sushila-g (active=yes) is public", ids.includes("sushila-g"), ids.join(","));
  ok("English roster: approved tutors WITHOUT a row (shikha-dutta, pinky-kumari, " + noRow.join(", ") + ") are public too", ["shikha-dutta", "pinky-kumari"].concat(noRow).every((id) => ids.includes(id)), ids.join(","));
  ok("English roster: sheet-only drafts (hemlata, tara, sarshtee-baliyan) stay off it", !["hemlata", "tara", "sarshtee-baliyan"].some((id) => ids.includes(id)), ids.join(","));
  ok("English roster: no script errors", pR.errors.length === 0, pR.errors.join(" | "));
  pR.close();
  for (const [rel, url] of [["es/find-tutors.html", "https://ekguru.shop/es/find-tutors.html"], ["hindi-tutor/worldwide/index.html", "https://ekguru.shop/hindi-tutor/worldwide/"], ["tutor/index.html", "https://ekguru.shop/tutor/"]]) {
    STORAGE.clear();
    const p = await loadPage(rel, url, g, { settle: 1200 });
    const rows = Array.from(p.win.document.querySelectorAll("[data-t-row]")).filter((e) => e.style.display !== "none").map((e) => e.getAttribute("data-t-row"));
    ok(rel + ": row-less approved tutors keep their card/line", ["shikha-dutta"].concat(noRow).every((id) => rows.includes(id)), rows.join(","));
    ok(rel + ": no zero state while tutors are visible", !p.win.document.querySelector("[data-eg-empty]"));
    p.close();
  }
  /* and the opposite: give deepika a row that says active=no -> gone */
  STORAGE.clear();
  const gNo = makeGoogle({ reviews: [], allNo: true, tutorMut: (o, c, h) => { if (o.id !== "deepika") setCell(o, c, h, "active", "yes"); } });
  const p2 = await loadPage(ROSTER, ROSTER_URL, gNo, { settle: 1200 });
  const ids2 = rosterIds(p2.win);
  ok("a row with active=no hides exactly that tutor (deepika)", !ids2.includes("deepika") && ids2.includes("utkarsh-upadhyay") && ids2.includes("sushila-g"), ids2.join(","));
  p2.close();
  /* tutor.html?id=<approved, no row> is a full bookable profile; ?id=<active=no> says closed, never "does not exist" */
  STORAGE.clear();
  const p3 = await loadPage("tutor.html", "https://ekguru.shop/tutor.html?id=deepika", g, { settle: 1200 });
  ok("tutor.html?id=deepika (approved, no row): full profile with Book buttons", p3.win.document.querySelectorAll("[data-book]").length >= 1 && /Deepika/.test(p3.win.document.querySelector("main").textContent));
  p3.close();
  STORAGE.clear();
  const p4 = await loadPage("tutor.html", "https://ekguru.shop/tutor.html?id=deepika", gNo, { settle: 1200 });
  const main4 = p4.win.document.querySelector("main").textContent;
  ok("tutor.html?id=deepika (active=no row): says bookings closed, NOT 'does not exist'", !/does not exist|not found/i.test(main4) && p4.win.document.querySelectorAll("[data-book]").length === 0, main4.replace(/\s+/g, " ").slice(0, 120));
  p4.close();
}

/* ====== 14. THE OWNER'S SHEET, 17 Nov 2026, through the real Unified.gs ====== */
console.log("\n== 14. reviews_pending as the owner has it today -> Unified.gs (vm) -> the live profile page ==");
{
  /* The exact rows of the `reviews_pending` tab on 17 Nov 2026 (contact
     e-mails replaced by placeholders — the feed strips that column anyway):
     three rejected rows, ONE approved row whose lesson_date is blank, so
     the feed falls back to the form timestamp (a real Date cell displayed
     day-first by the en_GB workbook). */
  const vm = require("node:vm");
  const DISPLAY = [
    ["timestamp", "reference", "status", "tutor_id", "reviewer_name", "stars", "text", "lesson_date", "contact_email", "booking_id", "notes"],
    ["04/11/2026 08:52:16", "EG-ZAVQPJ", "rejected", "sushila-g", "mnnm", "1", ",b;", "2026-11-04", "a@example.com", "", ""],
    ["04/11/2026 10:30:42", "EG-J4C9QM", "rejected", "pinky-kumari", "prakaash", "5", "MST HAI BHAI KYA PDHATI hi yrr yr", "2026-11-04", "", "", ""],
    ["04/11/2026 10:30:42", "EG-J4C9QM", "rejected", "pinky-kumari", "prakaash", "5", "good", "2026-11-04", "", "", ""],
    ["16/11/2026 11:24:13", "EG-CXHT9D", "approved", "sushila-g", "akg", "4", "good", "", "", "EK-VRX96M", ""]
  ];
  const RAW = DISPLAY.map((r, i) => (i ? [new Date(2026, 10, Number(r[0].slice(0, 2)), Number(r[0].slice(11, 13)), Number(r[0].slice(14, 16)))].concat(r.slice(1)) : r));
  function runUnified(source) {
    const ctx = {
      console: { log() {}, warn() {}, error() {} },
      SpreadsheetApp: { getActive: () => ({ getSheets: () => [{ getName: () => "reviews_pending", getSheetId: () => 176535552, getDataRange: () => ({ getDisplayValues: () => DISPLAY, getValues: () => RAW.map((r) => r.slice()) }) }] }) },
      CacheService: { getScriptCache: () => ({ get: () => null, put() {}, removeAll() {} }) },
      ContentService: { MimeType: { CSV: "CSV", JSON: "JSON" }, createTextOutput: (t) => ({ text: t, setMimeType() { return this; }, getContent() { return this.text; } }) },
      ScriptApp: { getProjectTriggers: () => [] },
      Utilities: { formatDate: (d) => d.toISOString().slice(0, 10) },
      Session: { getScriptTimeZone: () => "Asia/Kolkata" },
      PropertiesService: { getScriptProperties: () => ({ getProperty: () => null }) }
    };
    vm.createContext(ctx);
    vm.runInContext(source, ctx);
    return ctx.doGet({ parameter: { tab: "reviews" } }).getContent();
  }
  const repoCsv = runUnified(fs.readFileSync(path.join(ROOT, "apps-script/Unified.gs"), "utf8"));
  ok("Unified.gs (repo) publishes exactly the ONE approved row, dated 2026-11-16", /^sushila-g,akg,2026-11-16,4,good,/m.test(repoCsv) && !/pinky-kumari|EG-|example\.com|EK-VRX96M/.test(repoCsv), repoCsv);
  /* the still-deployed 2.1.0 build emitted the month/day swapped */
  const oldCsv = repoCsv.replace("2026-11-16", "2026-16-11");
  /* and the sheet's own word, should a row ever reach the browser unmapped */
  const approvedCsv = repoCsv.replace(/,live(\r?\n|$)/, ",approved$1");
  for (const [label, body] of [["repo 2.1.1 feed", repoCsv], ["deployed 2.1.0 feed (2026-16-11)", oldCsv], ["status=approved spelled as in the sheet", approvedCsv]]) {
    STORAGE.clear();
    const g = makeGoogle({ reviews: [], tutorMut: (o, c, h) => { if (o.id === "sushila-g") setCell(o, c, h, "active", "yes"); } });
    const real = g.fetch;
    g.fetch = (u) => (String(u).indexOf(FEED_EXEC + "?tab=reviews") === 0 ? Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve(body) }) : real(u));
    const p = await loadPage(PROFILE, PROFILE_URL, g, { settle: 1200 });
    const r = profileReviews(p.win);
    ok(label + ": sushila-g's profile prints akg's 4-star review and nothing else", r.count === 1 && r.names[0] === "akg" && r.rating === 4, JSON.stringify(r));
    ok(label + ": the printed date reads 16 Nov 2026", /16 Nov 2026|2026-11-16|Nov 16, 2026/.test(p.win.document.querySelector('[data-eg-reviews][data-tutor="sushila-g"]').textContent), p.win.document.querySelector('[data-eg-reviews][data-tutor="sushila-g"]').textContent.replace(/\s+/g, " ").slice(0, 200));
    ok(label + ": no script errors", p.errors.length === 0, p.errors.join(" | "));
    p.close();
    /* pinky-kumari: both her rows are rejected -> honest zero */
    STORAGE.clear();
    const pk = await loadPage("tutor/pinky-kumari/index.html", "https://ekguru.shop/tutor/pinky-kumari/", g, { settle: 1200 });
    const host = pk.win.document.querySelector('[data-eg-reviews][data-tutor="pinky-kumari"]');
    ok(label + ": pinky-kumari (rejected rows only) shows no review cards", host && host.querySelectorAll("article.rev").length === 0 && !/prakaash|MST HAI/.test(pk.win.document.body.textContent), host ? host.textContent.replace(/\s+/g, " ").slice(0, 120) : "no host");
    pk.close();
    /* ?reviews=debug — the owner's self-check box says what happened */
    STORAGE.clear();
    const dbg = await loadPage(PROFILE, PROFILE_URL + "?reviews=debug", g, { settle: 1200 });
    const box = dbg.win.document.getElementById("ekguru-reviews-debug");
    ok(label + ": ?reviews=debug prints the self-check (feed answered, 1 row, 1 published on sushila-g)", box && /answered\s*: yes/.test(box.textContent) && /rows received\s*: 1/.test(box.textContent) && /published\s*: 1 review\(s\) on sushila-g/.test(box.textContent), box ? box.textContent : "no box");
    dbg.close();
    /* the dynamic profile tutor.html?id=sushila-g (js/main.js) must agree */
    STORAGE.clear();
    const dyn = await loadPage("tutor.html", "https://ekguru.shop/tutor.html?id=sushila-g", g, { settle: 1500 });
    const dynMain = dyn.win.document.querySelector("main") ? dyn.win.document.querySelector("main").textContent : "";
    ok(label + ": tutor.html?id=sushila-g shows akg's review with a 4.0 rating", /akg/.test(dynMain) && /4\.0/.test(dynMain) && !/prakaash/.test(dynMain), dynMain.replace(/\s+/g, " ").slice(0, 160));
    dyn.close();
  }
}

console.log("\n" + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
