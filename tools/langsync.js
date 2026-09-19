#!/usr/bin/env node
/* ==========================================================================
   EkGuru — TUTOR SCRIPT SYNC
   --------------------------------------------------------------------------
   Gives every page that loads the tutor registry a <script> tag for every
   tutor in it — English pages, the six translated markets, join.html,
   find-tutors.html, admin.html, all of them, in the registry's order.

   WHY THIS TOOL EXISTS
   --------------------
   js/tutors/_registry.js and js/tutors-data.js both warn about this by name:

       "It used to say 'add a <script> line to each HTML page by hand'.
        That is how Shikha Dutta ended up missing from all six language
        pages — the hand edit was done for English and forgotten for the
        rest. Never edit those script tags yourself; run langsync."

   That tool was never in the repository, so the warning pointed at nothing
   and the mistake was still available to everyone. This is that tool, and it
   does exactly one job: the script tags. Their cards, profiles, JSON-LD and
   sitemap entries are written by tools/build-tutor-pages.js,
   tools/build-market-pages.js and tools/build-home-tutors.js.

   The tag is inserted relative to the registry tag already on the page, so a
   page two levels deep gets ../../js/tutors/… and the root page gets
   js/tutors/… — never a path that works on one page and 404s on the next.

   Run:  node tools/langsync.js [--check]
         --check exits 1 if any page is missing a tag (CI/gate use)
   ========================================================================== */

"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
process.chdir(ROOT);

const SKIP_DIRS = new Set([".git", "node_modules", "images", "css", "data", "reports", "docs"]);

/* The registry is a plain list of ids — read it without running it. */
function readRegistry() {
  const src = fs.readFileSync("js/tutors/_registry.js", "utf8");
  const m = /window\.EKGURU_TUTOR_ORDER\s*=\s*\[([\s\S]*?)\]/.exec(src);
  if (!m) throw new Error("could not read window.EKGURU_TUTOR_ORDER from js/tutors/_registry.js");
  return (m[1].match(/"([a-z0-9-]+)"/g) || []).map((s) => s.replace(/"/g, ""));
}

function walk(dir, out) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name) || entry.name.startsWith(".")) continue;
      walk(path.join(dir, entry.name), out);
    } else if (entry.name.endsWith(".html")) {
      out.push(path.join(dir, entry.name));
    }
  }
  return out;
}

/* Pages do not agree on `defer`: the English pages use it, the six market
   pages load these scripts plainly. The new tag copies whatever the page
   already does, so a sync never changes how a page loads its scripts. */
const REGISTRY_TAG = /(<script src="((?:\.\.\/)*js\/tutors\/)_registry\.js"( defer)?><\/script>)/;
const TUTOR_TAG = (prefix, id, defer) => `<script src="${prefix}${id}.js"${defer || ""}></script>`;

function sync(html, ids, file) {
  const reg = REGISTRY_TAG.exec(html);
  if (!reg) return null;                       // page does not use tutors at all
  const prefix = reg[2];                       // "js/tutors/" or "../../js/tutors/"
  const defer = reg[3] || "";                  // "" or " defer"

  const has = (id) => new RegExp('<script src="' + prefix + id + '\\.js"(?: defer)?></script>').test(html);
  const missing = ids.filter((id) => !has(id));
  if (!missing.length) return html;

  /* Insert after the last tutor tag already present, so a page that already
     lists three of five gets the two new ones at the end — not in the middle
     of a hand-written block; if the page has none at all, right after the
     registry tag, which is where the first one always lived. */
  const tagRe = new RegExp('<script src="' + prefix + '[a-z0-9-]+\\.js"(?: defer)?><\\/script>', "g");
  let at = -1;
  for (let m = tagRe.exec(html); m; m = tagRe.exec(html)) at = m.index + m[0].length;
  if (at === -1) at = reg.index + reg[1].length;

  const block = "\n" + missing.map((id) => TUTOR_TAG(prefix, id, defer)).join("\n");
  return html.slice(0, at) + block + html.slice(at);
}

function main() {
  const check = process.argv.includes("--check");
  const ids = readRegistry();
  if (!ids.length) throw new Error("the registry lists no tutors");

  const pages = walk(".", []).sort();
  let touched = 0;
  let stale = 0;

  for (const file of pages) {
    const html = fs.readFileSync(file, "utf8");
    const after = sync(html, ids, file);
    if (after === null || after === html) {
      if (after === null) continue;
      continue;
    }
    if (check) {
      console.log("STALE " + file);
      stale++;
      continue;
    }
    fs.writeFileSync(file, after);
    touched++;
    console.log("wrote " + file);
  }

  const withRegistry = pages.filter((p) => REGISTRY_TAG.test(fs.readFileSync(p, "utf8"))).length;
  if (!touched && !stale) {
    console.log("ok    all " + withRegistry + " tutor-aware page(s) carry all " + ids.length + " tutor tags");
  } else {
    console.log((check ? "stale: " : "updated: ") + (stale || touched) + " page(s)");
  }
  return check && stale ? 1 : 0;
}

process.exit(main());
