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
    /* U0 — a run may also be the generated EMPTY state (data-t-empty), so
       the block machinery can swap it back to rows the moment a tutor
       returns. Both markers count as one list slot. */
    const open = new RegExp(`<${kind.tag} class="${kind.cls}" data-t-(?:row|empty)="([^"]+)"`, "g");
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
      blocks.push({ kind: kind.cls, tag: kind.tag, id: m[1], start, end });
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
   U0 — THE "FIND A TUTOR" CTA, GENERATOR-OWNED
   -------------------------------------------------------------------------- */
/* While zero tutors are public, the conversion buttons in the three page
   families that sell tutor browsing (hindi-tutor/<city>, learn-hindi-from-*,
   answers/*) must not: they become "Start the free course" and point at the
   free Hindi course. Nav links ("Tutors", "Find Tutors") stay — they lead to
   find-tutors.html, which explains the state honestly.

   Both directions are generated, so the buttons come back word for word the
   moment a tutor row says active=yes. Never hand-edited (R-5). */
const RESTORE_LABEL = {
  "hindi-tutor/": "See all Hindi tutors",
  "learn-hindi-from-": "Find a Hindi Guru",
  "answers/": "Find a Hindi tutor"
};

function familyLabelOf(file) {
  if (file.indexOf("hindi-tutor/") === 0) return RESTORE_LABEL["hindi-tutor/"];
  if (file.indexOf("learn-hindi-from-") === 0) return RESTORE_LABEL["learn-hindi-from-"];
  return RESTORE_LABEL["answers/"];
}

/* Prefix is the page's relative path to the site root ("../../" etc.),
   derived from the page path itself — one level per directory. */
function prefixOf(file) {
  const depth = file.split("/").length - 1;
  return "../".repeat(depth);
}

function applyCta(html, prefix, familyLabel, zero) {
  if (zero) {
    /* zero public tutors: the selling button becomes the free-course CTA */
    return html.replace(
      /<a class="(btn[^"]*)"([^>]*href=")((?:\.\.\/)*find-tutors\.html[^"]*)("[^>]*>)(Find a Hindi Guru|See all Hindi tutors|Find a Hindi tutor)(<\/a>)/g,
      (m, cls, pre, href, mid, label, close) =>
        `<a class="${cls}"${pre}${prefix}learn/hindi/"${mid}Start the free course${close}`
    );
  }
  /* tutors are public again: the family's own words come back */
  return html.replace(
    /<a class="(btn[^"]*)"([^>]*href=")((?:\.\.\/)*learn-hindi\/")([^>]*>)Start the free course(<\/a>)/g,
    (m, cls, pre, href, mid, close) =>
      `<a class="${cls}"${pre}${prefix}find-tutors.html"${mid}${familyLabel}${close}`
  );
}

/* --------------------------------------------------------------------------
   rewriting one page
   -------------------------------------------------------------------------- */

/* U0 — the honest empty state in the exact slot the tutor rows used.
   Marked data-t-empty so the same machinery swaps the rows back in. */
function renderEmptyRun(kind, tag, prefix, indent, tr) {
  const { emptyTutorsBlock } = require("./lib/zero-state");
  return emptyTutorsBlock({
    prefix,
    lang: "en",
    t: (lang, key) => tr(key),
    tag,
    attrs: `class="${kind}" data-t-empty="${kind}" data-eg-empty="1"`
  }).split("\n").map((line, i) => (i === 0 ? line : indent + line)).join("\n");
}

function rebuild(html, roster, i18n, file, zero) {
  const blocks = findBlocks(html);

  const lang = (html.match(/<html[^>]*\blang="([a-z-]{2,5})"/i) || [])[1] || "en";
  const dict = i18n[lang] || i18n.en || {};
  const tr = (key) => (dict[key] !== undefined ? dict[key] : (i18n.en || {})[key] || key);

  let out = html;

  if (blocks.length) {
    /* group adjacent blocks into runs — a run is one tutor list */
    const runs = [];
    for (const b of blocks.slice().sort((a, c) => a.start - c.start)) {
      const last = runs[runs.length - 1];
      if (last && last.kind === b.kind && html.slice(last.end, b.start).trim() === "") last.end = b.end;
      else runs.push({ kind: b.kind, tag: b.tag, start: b.start, end: b.end });
    }

    /* The replacement includes the line's own indentation, so the block that
       goes back in starts where the block that came out did. Without this the
       replacement is inserted after the old leading spaces and the markup
       walks right by four spaces on every build. */
    for (const run of runs) {
      const lineStart = html.lastIndexOf("\n", run.start) + 1;
      if (html.slice(lineStart, run.start).trim() === "") run.start = lineStart;
    }

    /* back to front, so earlier offsets stay valid */
    for (const run of runs.reverse()) {
      /* the indentation of the line the run starts on (run.start is at the
         first non-space character of that line by now) */
      const indent = (html.slice(html.lastIndexOf("\n", run.start) + 1).match(/^[ \t]*/) || [""])[0];

      /* the page's own relative prefix, taken from the block being replaced;
         an already-empty block carries no links or images, so fall back to
         the page path itself (one level up per directory). */
      const sample = html.slice(run.start, run.end);
      const imgSample = /(?:src|srcset)="((?:\.\.\/)*)images\//.exec(sample);
      const linkSample = /href="((?:\.\.\/)*)tutor\//.exec(sample);
      const prefix = imgSample ? imgSample[1] : linkSample ? linkSample[1] : prefixOf(file);

      const render =
        run.kind === "tut" ? renderTut : run.kind === "t-item" ? renderTItem : renderLpCard;
      /* U0 — rows when someone is public, the honest empty state when not. */
      const body = roster.length
        ? roster
            .map((t) => (run.kind === "lp-card" ? render(t, prefix, indent, tr) : render(t, prefix, indent)))
            .join("\n")
        : renderEmptyRun(run.kind, run.tag, prefix, indent, tr);

      out = out.slice(0, run.start) + body + out.slice(run.end);
    }
    out = fixCopy(out);
  }

  /* The "Find a tutor" CTA swap runs on the three page families even when
     the page has no roster blocks at all (most learn-hindi-from-* and
     answers pages have none). Nowhere else — see familyLabelOf(). */
  const inFamily =
    file.indexOf("hindi-tutor/") === 0 ||
    file.indexOf("learn-hindi-from-") === 0 ||
    file.indexOf("answers/") === 0;
  const cta = inFamily ? applyCta(out, prefixOf(file), familyLabelOf(file), zero) : out;
  return cta === out && !blocks.length ? null : cta;
}

/* --------------------------------------------------------------------------
   main
   -------------------------------------------------------------------------- */

function main() {
  const check = process.argv.includes("--check");
  const site = loadSite();
  /* U0 — PUBLIC roster only (registry ∩ sheet active=yes); zero is a
     supported state and renders the honest empty state + free-course CTA. */
  const roster = site.publicTutors;
  const zero = roster.length === 0;

  const pages = walk(".", []).sort();
  let touched = 0;
  let stale = 0;
  let seen = 0;

  for (const file of pages) {
    const html = fs.readFileSync(file, "utf8");
    const after = rebuild(html, roster, site.i18n, file, zero);
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
    console.log("ok    all " + seen + " page(s) with a tutor list already list " +
      (zero ? "the zero-tutor empty state" : "all " + roster.length + " public tutors"));
  } else {
    console.log((check ? "stale: " : "updated: ") + (stale || touched) + " page(s)");
  }
  return check && stale ? 1 : 0;
}

process.exit(main());
