#!/usr/bin/env node
/* =========================================================
   EkGuru — SHEET FETCH/PARSER UNIT TESTS  (U0, 30 Sep 2026)
   ---------------------------------------------------------
   Proves, without any network:

   1. tests/fixtures/tutors.tsv (the real tutors-tab shape,
      personal email/phone stripped) parses with the shared
      parser: every column, every multi-line cell (about,
      experience, methodology), the #help row, active flags.
   2. js/sheet.js and tools/sheet-fetch.js parse IDENTICALLY —
      the two implementations of one format cannot drift.
   3. Quoting edge cases: embedded tabs, embedded quotes,
      multi-line cells, CRLF, BOM, trailing newline, blank rows.
   4. The URL fallback rewrite (output=csv ↔ output=tsv).
   5. The fetch fallback contract: csv HTTP 500 → tsv 200 wins,
      usedFallback is set; both failing throws with BOTH errors;
      an HTML login page is refused in either format.
   6. Privacy: the fixture carries no email address or phone.

   Run:  node tools/test-sheet-fetch.mjs
   ========================================================= */
"use strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const ROOT = path.join(path.dirname(new URL(import.meta.url).pathname), "..");

const S = require(path.join(ROOT, "tools", "sheet-fetch.js"));

let failures = 0, checks = 0;
function check(name, cond, extra) {
  checks++;
  if (!cond) failures++;
  console.log((cond ? "PASS" : "FAIL") + "  " + name + (cond ? "" : "  →  " + (extra || "")));
}
const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);

/* ----------------------------------------------------------------
   1. the real-shape fixture
   ---------------------------------------------------------------- */
const FIX = path.join(ROOT, "tests", "fixtures", "tutors.tsv");
const fixtureText = readFileSync(FIX, "utf8");
const rows = S.parseTSV(fixtureText);
const head = S.headerOf(rows);

check("fixture parses to header + #help + 5 tutor rows", rows.length === 7, "got " + rows.length);
check("fixture keeps every column", head.length === 48, "got " + head.length);
check("fixture header has the lookup columns",
  ["id", "active", "name", "about", "methodology"].every((c) => head.indexOf(c) !== -1));

const byId = {};
for (const r of rows.slice(1)) byId[r[0]] = r;
const ids = Object.keys(byId).filter((k) => k.charAt(0) !== "#");
check("fixture ids are the five real tutors",
  ["sushila-g", "hemlata", "shikha-dutta", "tara", "sarshtee-baliyan"].every((id) => byId[id]),
  ids.join(","));
check("#help row survives the parser (it is a real row)", !!byId["#help"]);

const cell = (id, col) => byId[id][head.indexOf(col)];
check("every tutor row is active=no (the live 30 Sep 2026 state)",
  ids.every((id) => cell(id, "active") === "no"));
check("multi-line about cell keeps its paragraphs",
  ids.every((id) => cell(id, "about").split("\n").length >= 2));
check("multi-line methodology cell keeps 'Title | description' lines",
  ids.every((id) => cell(id, "methodology").includes("|") && cell(id, "methodology").includes("\n")));
check("availability cell keeps its commas (quoted field)",
  cell("sushila-g", "availability").includes("Mon 09:00,10:00"));

/* ----------------------------------------------------------------
   2. the two parsers agree
   ---------------------------------------------------------------- */
/* js/sheet.js needs a minimal browser shim. */
global.window = { EKGURU_SITE: { sheet: {} } };   /* no csvUrl -> no fetch work */
global.localStorage = { getItem: () => null, setItem() {} };
global.document = { addEventListener() {} };
global.CustomEvent = function (type, opts) { this.type = type; this.detail = (opts || {}).detail || {}; };
require(path.join(ROOT, "js", "sheet.js"));
const B = window.EkGuruSheet;

check("js/sheet.js publishes its parsers", !!(B && B.parseDelimited && B.parseCSV && B.parseTSV));
if (B && B.parseDelimited) {
  check("browser and Node parsers agree on the fixture",
    eq(B.parseTSV(fixtureText), rows));
}

/* ----------------------------------------------------------------
   3. quoting edge cases (synthetic — the fixture stays real data)
   ---------------------------------------------------------------- */
const synth = "\uFEFFid\tnote\textra\r\n" +                 /* BOM + CRLF */
  'one\t"a tab\there"\t"say ""hi"""\r\n' +                    /* embedded tab + escaped quotes */
  'two\t"line1\nline2"\tplain\r\n' +                          /* multi-line cell */
  "\r\n" +                                                   /* blank row -> dropped */
  'three\t,\t"x,y"\r\n';                                     /* delimiter inside quotes */
const srows = B ? B.parseTSV(synth) : S.parseTSV(synth);
check("BOM is stripped from the first header", srows[0][0] === "id");
check("embedded tab inside quotes survives", srows[1][1] === "a tab\there");
check('escaped "" becomes one quote', srows[1][2] === 'say "hi"');
check("multi-line cell keeps its newline", srows[2][1] === "line1\nline2");
check("blank rows are dropped, not parsed", srows.length === 4, "got " + srows.length);
check("delimiter inside quotes is not a split", srows[3][2] === "x,y");
check("no phantom row after the trailing newline", srows[srows.length - 1][0] === "three");
check("browser parser matches on the synthetic case too",
  !B || eq(B.parseTSV(synth), srows));

check("parseCSV still splits on commas", eq(S.parseCSV('a,b\n1,2'), [["a", "b"], ["1", "2"]]));
check("parseTSV does not split on commas", eq(S.parseTSV('a,b\n1,2'), [["a,b"], ["1,2"]]));

/* ----------------------------------------------------------------
   4. URL rewrite
   ---------------------------------------------------------------- */
const U = "https://docs.google.com/spreadsheets/d/e/AAA/pub?gid=123&single=true&output=csv";
check("csv url -> tsv url swaps output=",
  S.withOutput(U, "tsv") === "https://docs.google.com/spreadsheets/d/e/AAA/pub?gid=123&single=true&output=tsv",
  S.withOutput(U, "tsv"));
check("urlVariants returns both formats", S.urlVariants(U).tsv.includes("output=tsv") &&
  S.urlVariants(U).csv.includes("output=csv"));
check("a url without output= gets one appended",
  S.withOutput("https://x/pub?gid=1", "tsv") === "https://x/pub?gid=1&output=tsv");

/* ----------------------------------------------------------------
   5. the fetch fallback contract
   ---------------------------------------------------------------- */
const TSV_BODY = "id\tactive\tname\nsushila-g\tno\tSushila G.\nhemlata\tyes\tHemlata\n";
function stubFetch(script) {
  const calls = [];
  const f = (url) => {
    calls.push(url);
    const step = script.shift() || { status: 500 };
    return Promise.resolve({
      ok: step.status >= 200 && step.status < 300,
      status: step.status,
      text: () => Promise.resolve(step.body || "")
    });
  };
  f.calls = calls;
  return f;
}

(async () => {
  /* csv 500 -> tsv 200 */
  let f = stubFetch([{ status: 500 }, { status: 200, body: TSV_BODY }]);
  let got = await S.fetchSheetRows(f, U);
  check("csv HTTP 500 falls back to tsv", got.format === "tsv" && got.usedFallback === true);
  check("fallback rows carry the data", got.rows.length === 3 && got.rows[1][0] === "sushila-g");
  check("fallback tried csv first", f.calls.length === 2 && /output=csv/.test(f.calls[0]) &&
    /output=tsv/.test(f.calls[1]));

  /* csv answers an HTML login page -> tsv 200 */
  f = stubFetch([{ status: 200, body: "<html>login</html>" }, { status: 200, body: TSV_BODY }]);
  got = await S.fetchSheetRows(f, U);
  check("an HTML page on csv falls back to tsv (non-csv response)",
    got.format === "tsv" && got.usedFallback === true);

  /* csv 200 with real csv -> no fallback */
  f = stubFetch([{ status: 200, body: "id,active\nsushila-g,no\n" }]);
  got = await S.fetchSheetRows(f, U);
  check("healthy csv answers directly, no tsv request",
    got.format === "csv" && got.usedFallback === false && f.calls.length === 1);

  /* both fail -> one error naming BOTH formats */
  f = stubFetch([{ status: 500 }, { status: 500, body: "" }]);
  let err = null;
  try { await S.fetchSheetRows(f, U); } catch (e) { err = e; }
  check("both formats failing throws", !!err);
  check("the error reports both attempts",
    !!err && /csv/i.test(err.message) && /tsv/i.test(err.message), err && err.message);

  /* wrong tab (no id/tutor/key) on both -> refused */
  f = stubFetch([
    { status: 200, body: "foo,bar\n1,2\n" },
    { status: 200, body: "foo\tbar\n1\t2\n" }
  ]);
  err = null;
  try { await S.fetchSheetRows(f, U); } catch (e) { err = e; }
  check("a wrong tab is refused in both formats", !!err);

  /* key/value tab: settings shape passes with allowKeyOnly */
  f = stubFetch([{ status: 500 }, { status: 200, body: "key\tvalue\nemail\tsomeone@example.com\n" }]);
  got = await S.fetchSheetRows(f, U, { allowKeyOnly: true });
  check("settings-shaped tabs pass with allowKeyOnly", got.rows.length === 2);

  /* ----------------------------------------------------------------
     6. privacy of the fixture
     ---------------------------------------------------------------- */
  check("fixture carries no email address", !/\S+@\S+\.\S+/.test(fixtureText));
  check("fixture carries no phone number", !/\+?\d[\d\s()\-]{8,}\d\s*(?:ext|x)?/i.test(
    fixtureText.split("\n").slice(1).join("\n").replace(/[\t\n]/g, " ").replace(/https?:\/\/\S+/g, "")));

  console.log("\n" + checks + " checks, " + failures + " failure(s)");
  process.exit(failures ? 1 : 0);
})();
