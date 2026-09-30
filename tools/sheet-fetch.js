#!/usr/bin/env node
/* =========================================================
   EkGuru — SHARED PUBLISHED-SHEET FETCH + PARSE
   ---------------------------------------------------------
   One implementation of "read a published Google Sheet tab" for
   every consumer: tools/sheetsync.js (build), the offline
   fixture path, tools/test-data-sources.py's Node siblings and
   the parser unit tests (tools/test-sheet-fetch.mjs).

   WHY THIS FILE EXISTS (30 Sep 2026)
   ----------------------------------
   Google's published-CSV endpoint went bad on the "EkGuru DB"
   workbook: every `pub?...&output=csv` URL answers HTTP 500
   while the SAME tab with `output=tsv` answers HTTP 200 with
   the data. Verified live on 30 Sep 2026 (all four tabs).

   So the order is fixed and lives HERE, once:

       1. try the URL with output=csv
       2. if that is non-200, or answers an HTML page, or the
          header has no usable id — retry the same URL with
          output=tsv
       3. if both fail, fail loudly with both errors

   js/sheet.js carries the same order for the browser (it cannot
   require this file); tools/test-sheet-fetch.mjs asserts the two
   implementations agree, row for row, on the real sheet shape.

   THE PARSER
   ----------
   Google's TSV export uses the same quoting rules as its CSV
   export — double quotes wrap fields that contain the delimiter,
   quotes or newlines, and `""` is a literal quote. Multi-line
   cells (about, bio, experience, methodology) therefore arrive
   intact. parseDelimited() handles both delimiters with one
   implementation so CSV and TSV can never drift apart.

   Rows that are entirely empty are dropped (the export's trailing
   newline must not become a phantom row).
   ========================================================= */
"use strict";

/* ---------- parsing ---------- */

/* Strip a UTF-8 BOM: Google's export carries one and it would
   otherwise glue itself to the first header name ("id" -> "id"
   with an invisible prefix, which breaks every column lookup). */
function stripBOM(text) {
  text = String(text == null ? "" : text);
  return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
}

/* The RFC-4180 state machine with an arbitrary delimiter.
   Handles: quoted fields, `""` escapes, newlines inside quotes,
   CRLF and LF, a trailing newline (no phantom row), and \r
   outside quotes (dropped, matching the historical parseCSV). */
function parseDelimited(text, delim) {
  text = stripBOM(text);
  const rows = [];
  let row = [], field = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i], next = text[i + 1];
    if (q) {
      if (c === '"' && next === '"') { field += '"'; i++; }
      else if (c === '"') q = false;
      else field += c;
    } else if (c === '"') q = true;
    else if (c === delim) { row.push(field); field = ""; }
    else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
    else if (c !== "\r") field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows.filter((r) => r.some((c) => String(c).trim()));
}

const parseCSV = (text) => parseDelimited(text, ",");
const parseTSV = (text) => parseDelimited(text, "\t");

/* Header row, normalised the way every consumer expects it. */
function headerOf(rows) {
  return (rows[0] || []).map((h) => String(h).trim().toLowerCase());
}

/* Records keyed by lowercase header. Tutor tabs keep rows that
   carry an `id` (or `tutor`, for the reviews tab — v104); the
   #help row and blank ids are dropped by the CALLER, because
   settings/support tabs are key/value shaped and want every row. */
function toRecords(rows) {
  if (rows.length < 2) return [];
  const head = headerOf(rows);
  return rows.slice(1).map((r) => {
    const o = {};
    head.forEach((h, i) => { if (h) o[h] = String(r[i] == null ? "" : r[i]).trim(); });
    return o;
  }).filter((o) => o.id || o.tutor);
}

/* ---------- URL variants ---------- */

/* The same tab, same publish token — only the export format
   changes. If the URL carries no `output=` parameter, one is
   appended (a hand-copied pubhtml link, for example). */
function withOutput(url, format) {
  const u = String(url || "");
  if (/[?&]output=/.test(u)) return u.replace(/([?&])output=[^&]*/, "$1output=" + format);
  return u + (u.indexOf("?") === -1 ? "?" : "&") + "output=" + format;
}

function urlVariants(url) {
  return { csv: withOutput(url, "csv"), tsv: withOutput(url, "tsv") };
}

/* A Sheet that is not published answers with an HTML login page.
   Parsing that as rows would silently produce garbage. */
function looksLikeHtml(text) {
  return /^\s*</.test(String(text == null ? "" : text));
}

/* ---------- fetching ---------- */

/* Try one format. Returns { ok, status, text } — never throws
   for network errors: the caller owns the fallback decision and
   the final error message. */
async function tryFetch(fetchImpl, url) {
  try {
    const res = await fetchImpl(url);
    const text = await res.text();
    return { ok: !!res.ok, status: res.status || (res.ok ? 200 : 0), text };
  } catch (e) {
    return { ok: false, status: 0, text: "", error: e.message || String(e) };
  }
}

/* The contract every consumer uses.

   Returns {
     rows,            the parsed rows (header + data)
     format,          "csv" | "tsv" — what actually answered
     url,             the URL that answered
     usedFallback,    true when CSV failed and TSV saved the day
     attempts: [{ format, url, ok, status, error? }]
   }
   Throws only when BOTH formats fail — with both errors in the
   message so CI logs show what happened on each side. */
async function fetchSheetRows(fetchImpl, url, opts) {
  const want = urlVariants(url);
  const order = (opts && opts.order) || ["csv", "tsv"];
  const attempts = [];

  for (const format of order) {
    const u = want[format];
    const r = await tryFetch(fetchImpl, u);
    attempts.push({ format, url: u, ok: r.ok, status: r.status, error: r.error });
    if (!r.ok) continue;
    if (looksLikeHtml(r.text)) {
      attempts[attempts.length - 1].error = "returned HTML, not " + format;
      continue;
    }
    const rows = parseDelimited(r.text, format === "tsv" ? "\t" : ",");
    const head = headerOf(rows);
    if (!head.length) {
      attempts[attempts.length - 1].error = "no header row";
      continue;
    }
    /* Schema sanity: a tutor/reviews tab must have id/tutor; a
       settings/support tab must have key. Anything else is a
       wrong tab or an empty sheet and must be loud, not silent.
       Callers that need key/value-only tabs pass
       { allowKeyOnly: true }. */
    const ok = head.indexOf("id") !== -1 || head.indexOf("tutor") !== -1 ||
      ((opts && opts.allowKeyOnly) && head.indexOf("key") !== -1);
    if (!ok) {
      attempts[attempts.length - 1].error = "header has no id/tutor/key column (got: " +
        head.slice(0, 6).join(",") + ")";
      continue;
    }
    return {
      rows, format, url: u,
      /* the raw export text, so a caller can feed the exact bytes to a
         second parser (tools/test-sheet-loader.js hands it to js/sheet.js)
         without a lossy rows -> text round trip */
      text: r.text,
      usedFallback: format !== order[0],
      attempts
    };
  }

  const detail = attempts.map((a) => a.format + " → HTTP " + a.status +
    (a.error ? " (" + a.error + ")" : "")).join("; ");
  throw new Error("published Sheet unreachable in every format: " + detail);
}

/* Same, but fetch-free: read a local export (tests/fixtures/, or
   a downloaded snapshot) instead of the network. The offline
   path for tools/sheetsync.js and the activation tests. */
function readLocalRows(text, format) {
  return parseDelimited(text, format === "tsv" ? "\t" : ",");
}

/* Pick csv/tsv purely from the file extension — used by the
   offline loader. */
function formatFromPath(p) {
  return /\.tsv$/i.test(String(p || "")) ? "tsv" : "csv";
}

module.exports = {
  parseDelimited, parseCSV, parseTSV,
  headerOf, toRecords,
  withOutput, urlVariants, looksLikeHtml,
  fetchSheetRows, readLocalRows, formatFromPath
};
