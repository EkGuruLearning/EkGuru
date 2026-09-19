#!/usr/bin/env node
/* ==========================================================================
   EkGuru — ROSTER ROWS (the tutor lists baked into other pages)
   --------------------------------------------------------------------------
   Three pre-rendered shapes list the tutors, outside the home page and the
   profiles, and every one of them was hand-maintained and stale:

       div.tut         37 pages under hindi-tutor/   ("The tutors")
       div.t-item      tutor/index.html              (the tutor hub)
       article.lp-card the six translated find-tutors pages

   They all carried the same four tutors with the same two mistakes: the
   price inside the element text did not match the `data-usd` attribute for
   Tara and Shikha ($6 next to data-usd="8"), and a tutor added later — there
   is always one — would simply be missing from all 44 pages.

   This tool rewrites those blocks from the roster, in registry order. The
   surrounding page (headings, prose, filters, footer) is never touched: it
   finds the run of tutor blocks and replaces the run.

   Run:  node tools/build-roster-rows.js [--check]
         --check exits 1 if any page is out of date (CI/gate use)
   ========================================================================== */

"use strict";

const fs = require("fs");
const path = require("path");

const { loadSite } = require("./lib/site-data");

const ROOT = path.resolve(__dirname, "..");
process.chdir(ROOT);

const SKIP_DIRS = new Set([".git", "node_modules", "images", "css", "data", "reports", "docs"]);

const esc = (s) =>
  String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const exists = (p) => p && !/^https?:/i.test(p) && fs.existsSync(p);
const pretty = (n) => (Number.isInteger(Number(n)) ? "$" + Number(n) : "$" + Number(n).toFixed(2));

function walk(dir, out) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name) || entry.name.startsWith(".")) continue;
      walk(path.join(dir, entry.name), out);
    } else if (entry.name.endsWith(".html")) out.push(path.join(dir, entry.name));
  }
  return out;
}

/* --------------------------------------------------------------------------
   finding a block: `class="X" data-t-row="id"` … its matching close
   -------------------------------------------------------------------------- */

const KINDS = [
  { cls: "tut", tag: "div" },
  { cls: "t-item", tag: "div" },
  { cls: "lp-card", tag: "article" }
];

function findBlocks(html) {
  const blocks = [];
  for (const kind of KINDS) {
    const open = new RegExp(`<${kind.tag} class="${kind.cls}" data-t-row="([^"]+)"`, "g");
    for (let m = open.exec(html); m; m = open.exec(html)) {
      const start = m.index;
      /* walk the same tag name to the matching close — these blocks nest
         other divs (or are nested in them), so a lazy [\s\S]*? would stop
         at the first inner </div> */
      const tagRe = new RegExp(`<${kind.tag}\\b|</${kind.tag}>`, "g");
      tagRe.lastIndex = start;
      let depth = 0;
      let end = -1;
      for (let t = tagRe.exec(html); t; t = tagRe.exec(html)) {
        if (t[0][1] === "/") depth--;
        else depth++;
        if (depth === 0) {
          end = t.index + t[0].length;
          break;
        }
      }
      if (end === -1) continue;
      blocks.push({ kind: kind.cls, id: m[1], start, end });
    }
  }
  return blocks.sort((a, b) => a.start - b.start);
}

/* --------------------------------------------------------------------------
   renderers — each returns the block with the page's own indentation kept
   -------------------------------------------------------------------------- */

function imageFor(t, prefix) {
  const src = t.thumb || t.photo || "images/placeholder-tutor.jpg";
  if (/^https?:/i.test(src)) return { img: src, webp: "" };
  const base = src.replace(/\.(jpe?g|png|webp)$/i, "");
  const small = base + "-176.jpg";
  const webp = base + "-176.webp";
  return {
    img: prefix + (exists(small) ? small : src),
    webp: exists(webp) ? prefix + webp : ""
  };
}

function priceSpan(t, extra) {
  return (
    `<span data-usd="${t.priceUSD}" data-usd-mode="bare" data-t="${t.id}" data-f="priceUSD" data-fmt="money">` +
    `${pretty(t.priceUSD)}</span>` + (extra || "")
  );
}

function renderTut(t, prefix, indent) {
  const img = imageFor(t, prefix);
  const tail = t.trialAvailable
    ? "trial available"
    : t.reviewsCount
    ? `★ ${Number(t.rating).toFixed(1)} (${t.reviewsCount})`
    : t.badge
    ? esc(t.badge)
    : "lessons online";

  return `${indent}<div class="tut" data-t-row="${t.id}">
${indent}  <img src="${img.img}" alt="${esc(t.name)}" width="64" height="64" loading="lazy">
${indent}  <div>
${indent}    <b><a href="${prefix}tutor/${t.id}/"><span data-t="${t.id}" data-f="name">${esc(t.name)}</span></a></b>
${indent}    <small data-t="${t.id}" data-f="headline">${esc(t.headline || "")}</small><br>
${indent}    <small>${priceSpan(t)} · <span data-t="${t.id}" data-f="lessonLength">${esc(t.lessonLength || "50 min")}</span> · ${tail}</small>
${indent}  </div>
${indent}</div>`;
}

function renderTItem(t, prefix, indent) {
  const levels = (t.levels || []).join(", ");
  return `${indent}<div class="t-item" data-t-row="${t.id}">
${indent}  <h2><a href="${t.id}/"><span data-t="${t.id}" data-f="name">${esc(t.name)}</span></a></h2>
${indent}  <p data-t="${t.id}" data-f="headline">${esc(t.headline || "")}</p>
${indent}  <p><strong data-usd="${t.priceUSD}" data-t="${t.id}" data-f="priceUSD" data-fmt="money">${pretty(t.priceUSD)}</strong> per <span data-t="${t.id}" data-f="lessonLength">${esc(t.lessonLength || "50 min")}</span> · <span data-t="${t.id}" data-f="levels" data-fmt="list">${esc(levels)}</span> · <span data-t="${t.id}" data-f="city">${esc(t.city || t.country || "India")}</span></p>
${indent}  <p data-t="${t.id}" data-f="teaches" data-fmt="list">${esc((t.teaches || []).join(", "))}</p>
${indent}</div>`;
}

function renderLpCard(t, prefix, indent, tr) {
  const img = imageFor(t, prefix);
  const role = tr("card.tutor");
  const levels = (t.levels || []).join(", ");
  const rating = t.reviewsCount
    ? ` · ★ ${Number(t.rating).toFixed(1)} (${t.reviewsCount})`
    : t.trialAvailable
    ? ` · ${tr("pf.trial")}`
    : "";
  return `${indent}<article class="lp-card" data-t-row="${t.id}">
${indent}  <picture>
${img.webp ? `${indent}    <source srcset="${img.webp}" type="image/webp">\n` : ""}${indent}    <img src="${img.img}" alt="${esc(t.name + ", " + role)}" width="88" height="88" loading="lazy" decoding="async">
${indent}  </picture>
${indent}  <div>
${indent}    <h3><a href="${prefix}tutor/${t.id}/">${esc(t.name)}</a></h3>
${indent}    <p class="lp-headline">${esc(t.headline || "")}</p>
${indent}    <p class="lp-meta">
${indent}      <strong data-t="${t.id}" data-f="priceUSD" data-fmt="money" data-usd="${t.priceUSD}" data-usd-mode="bare">${pretty(t.priceUSD)}</strong> · ${esc(t.lessonLength || "50 min")} ·
${indent}      ${esc(levels)}${rating}
${indent}    </p>
${indent}    <p class="lp-teaches">${esc((t.teaches || []).join(" · "))}</p>
${indent}    <a class="btn btn-primary btn-sm" href="${prefix}tutor/${t.id}/">${esc(tr("hero.viewProfile"))}</a>
${indent}  </div>
${indent}</article>`;
}

/* --------------------------------------------------------------------------
   page copy that quotes the roster size
   --------------------------------------------------------------------------
   "See all 4 tutors" was true when there were four, and it silently became a
   lie the day a fifth arrived. A number inside a sentence goes stale; the
   generated pages drop it and let the list speak. */
function fixCopy(html) {
  return html
    .replace(/See all \d+ tutors?/gi, "See all Hindi tutors")
    .replace(/See all Hindi tutors tutors/gi, "See all Hindi tutors");
}

/* --------------------------------------------------------------------------
   rewriting one page
   -------------------------------------------------------------------------- */

function rebuild(html, roster, i18n, file) {
  const blocks = findBlocks(html);
  if (!blocks.length) return null;

  const lang = (html.match(/<html[^>]*\blang="([a-z-]{2,5})"/i) || [])[1] || "en";
  const dict = i18n[lang] || i18n.en || {};
  const tr = (key) => (dict[key] !== undefined ? dict[key] : (i18n.en || {})[key] || key);

  /* group adjacent blocks into runs — a run is one tutor list */
  const runs = [];
  for (const b of blocks.slice().sort((a, c) => a.start - c.start)) {
    const last = runs[runs.length - 1];
    if (last && last.kind === b.kind && html.slice(last.end, b.start).trim() === "") last.end = b.end;
    else runs.push({ kind: b.kind, start: b.start, end: b.end });
  }

  /* The replacement includes the line's own indentation, so the block that
     goes back in starts where the block that came out did. Without this the
     replacement is inserted after the old leading spaces and the markup
     walks right by four spaces on every build. */
  for (const run of runs) {
    const lineStart = html.lastIndexOf("\n", run.start) + 1;
    if (html.slice(lineStart, run.start).trim() === "") run.start = lineStart;
  }

  let out = html;
  /* back to front, so earlier offsets stay valid */
  for (const run of runs.reverse()) {
    /* the indentation of the line the run starts on (run.start is at the
       first non-space character of that line by now) */
    const indent = (html.slice(html.lastIndexOf("\n", run.start) + 1).match(/^[ \t]*/) || [""])[0];

    /* the page's own relative prefix, taken from the block being replaced */
    const sample = html.slice(run.start, run.end);
    const imgSample = /(?:src|srcset)="((?:\.\.\/)*)images\//.exec(sample);
    const linkSample = /href="((?:\.\.\/)*)tutor\//.exec(sample);
    const prefix = imgSample ? imgSample[1] : linkSample ? linkSample[1] : "";

    const render =
      run.kind === "tut" ? renderTut : run.kind === "t-item" ? renderTItem : renderLpCard;
    const body = roster
      .map((t) => (run.kind === "lp-card" ? render(t, prefix, indent, tr) : render(t, prefix, indent)))
      .join("\n");

    out = out.slice(0, run.start) + body + out.slice(run.end);
  }

  return fixCopy(out);
}

/* --------------------------------------------------------------------------
   main
   -------------------------------------------------------------------------- */

function main() {
  const check = process.argv.includes("--check");
  const site = loadSite();
  const roster = site.tutors;
  if (!roster.length) throw new Error("the tutor registry is empty");

  const pages = walk(".", []).sort();
  let touched = 0;
  let stale = 0;
  let seen = 0;

  for (const file of pages) {
    const html = fs.readFileSync(file, "utf8");
    const after = rebuild(html, roster, site.i18n, file);
    if (after === null) continue;
    seen++;
    if (after === html) continue;
    if (check) {
      console.log("STALE " + file);
      stale++;
      continue;
    }
    fs.writeFileSync(file, after);
    touched++;
    console.log("wrote " + file);
  }

  if (!touched && !stale) {
    console.log("ok    all " + seen + " page(s) with a tutor list already list all " + roster.length + " tutors");
  } else {
    console.log((check ? "stale: " : "updated: ") + (stale || touched) + " page(s)");
  }
  return check && stale ? 1 : 0;
}

process.exit(main());
