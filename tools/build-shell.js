#!/usr/bin/env node
/* ==========================================================================
   EkGuru — THE SHELL: one header and one footer for every page
   --------------------------------------------------------------------------
   1,564 pages, and until this tool existed they carried two different site
   chromes and three different taglines:

       27 pages   the hand-written shell   (<header class="hdr"> + <footer class="ftr">)
    1,537 pages   the old plain wrapper     (<footer class="pw-ftr">, some with no header at all)

       js/site-config.js        One Student. One Guru. One Goal.
       the settings sheet       One Student. One Goal. One Guru.
       hand-written pages       one or the other, page by page

   This tool gives every page the same header and the same footer, with the
   tagline, the contact address and the "mode" line baked from the settings
   tab — the same source the rest of the site reads (tools/sheetsync.js writes
   the sheet into js/tutors/_overrides.js; this reads it back through
   tools/lib/site-data.js, so there is one value, not a fourth copy).

   WHAT IT DOES, IN ORDER
   ----------------------
     1. page already carries the shell (markers) → the block is rewritten
     2. page carries its own hand-written chrome    → that chrome is replaced
        in place (a second footer is removed, never stacked)
     3. page has no site chrome at all              → the shell is inserted

   The nine market pages keep their own translations: the labels come from
   js/i18n.js — the same file the page loads — so the header is right before
   JavaScript runs, and their own three pages (home, find-tutors, join) stay
   the targets of their links instead of the English ones.

   HOW IT STAYS HONEST
   -------------------
     · the block is wrapped in markers, so a rebuild replaces it instead of
       stacking a second copy; unbalanced markers refuse to run
     · the sheet chrome is held aside while the page's own chrome is removed,
       so the new header cannot be mistaken for an old one
     · relative links are computed per page depth, never guessed
     · `--check` exits 1 if any page is out of date (tools/build-all.py check
       runs it in the gate)

   Run:  node tools/build-shell.js [--check] [--verbose]
   ========================================================================== */

"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const { loadSite } = require("./lib/site-data");

const ROOT = path.resolve(__dirname, "..");
process.chdir(ROOT);

const SKIP_DIRS = new Set([".git", "node_modules", "images", "css", "js", "data",
  "reports", "docs", "templates", "research"]);
const SKIP_FILES = new Set(["googleb3b0e3defc1daa17.html"]);   // Google verification

const H_START = "<!-- ekguru:shell-header:start -->";
const H_END = "<!-- ekguru:shell-header:end -->";
const F_START = "<!-- ekguru:shell-footer:start -->";
const F_END = "<!-- ekguru:shell-footer:end -->";

/* Locales that have their own tree (ar/index.html, es/find-tutors.html …)
   and their own dictionary in js/i18n.js. */
const LOCALES = ["ar", "de", "es", "fr", "ja", "pt"];

const esc = (s) => String(s == null ? "" : s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
  .replace(/"/g, "&quot;");

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name) || e.name.startsWith(".")) continue;
      walk(path.join(dir, e.name), out);
    } else if (e.name.endsWith(".html") && !SKIP_FILES.has(e.name)) {
      out.push(path.join(dir, e.name));
    }
  }
  return out;
}

/* depth of a page inside the tree → "../" × n. Every link below is written
   relative to it, so the same markup works at / and at /answers/x/. */
const prefixFor = (file) => {
  const depth = file.split(path.sep).length - 1;
  return "../".repeat(depth);
};

/* --------------------------------------------------------------------------
   the labels
   -------------------------------------------------------------------------- */

/* js/i18n.js is a plain object literal assigned to window.EKGURU_I18N, so it
   can be read here without a browser — and reading it is the point: the
   translations in the shipped header are the translations in the dictionary,
   not a second copy that drifts from it. */
function loadI18n() {
  try {
    const src = fs.readFileSync("js/i18n.js", "utf8");
    const ctx = { window: {} };
    vm.runInNewContext(src, ctx, { filename: "js/i18n.js", timeout: 2000 });
    return ctx.window.EKGURU_I18N || {};
  } catch (e) {
    console.error("! could not read js/i18n.js (" + e.message + ") — market pages get English labels");
    return {};
  }
}

/* Every link in the chrome, once. `key` is the i18n key; `target` is the key
   into TARGETS below. */
const NAV = [
  ["Home", "nav.home", "home"],
  ["Find Tutors", "nav.tutors", "findTutors"],
  ["Courses", "nav.courses", "courses"],
  ["Learn", "nav.learn", "learn"],
  ["Support", "nav.support", "support"],
  ["Search", "nav.search", "search"],
];
const CTA = ["Find tutors", "nav.cta", "findTutors"];
const COLUMNS = [
  ["Site", "ftr.site", [
    ["Home", "nav.home", "home"],
    ["Find Tutors", "nav.tutors", "findTutors"],
    ["Become a tutor", "nav.join", "join"],
    ["All tutors — text directory", "ftr.tutors", "tutorDir"],
    ["Hindi tutors by location", "ftr.locations", "locations"],
    ["Courses", "nav.courses", "courses"],
    ["Courses by country", "ftr.bycountry", "byCountry"],
    ["Search the site", "ftr.search", "search"],
  ]],
  ["Learn Hindi", "ftr.learn", [
    ["Free guides", "ftr.guides", "guides"],
    ["Every topic, mapped", "ftr.topics", "topics"],
    ["Interactive tools", "ftr.tools", "tools"],
    ["Daily Hindi — 30 days", "ftr.daily", "daily"],
    ["Questions answered", "ftr.ask", "ask"],
    ["Short answers", "ftr.answers", "answers"],
    ["Countries & languages", "ftr.countries", "countries"],
  ]],
  ["Contact & legal", "ftr.legal", [
    ["Contact form", "ftr.contactForm", "contact"],
    ["EMAIL", "", "email"],
    ["About EkGuru", "ftr.about2", "about"],
    ["Privacy policy", "ftr.privacy", "privacy"],
    ["Terms of use", "ftr.terms", "terms"],
    ["Monetization disclosure", "ftr.monetization", "monetization"],
    ["Disclaimer", "ftr.disclaimer", "disclaimer"],
    ["Copyright", "ftr.copyright", "copyright"],
    ["Cookie policy", "ftr.cookies", "cookies"],
  ]],
];

const TARGETS = {
  home: "index.html", findTutors: "find-tutors.html", join: "join.html",
  courses: "courses/index.html", byCountry: "courses/by-country/index.html", learn: "learn/", support: "support/index.html",
  search: "search/", tutorDir: "tutor/", locations: "hindi-tutor/",
  guides: "learn/", topics: "hindi/", tools: "toolbox/", daily: "daily-hindi/",
  ask: "ask/", answers: "answers/", countries: "learn-hindi-by-country/",
  contact: "contact/", about: "about/", privacy: "privacy/",
  terms: "terms/", monetization: "monetization-disclosure/", disclaimer: "disclaimer/", copyright: "copyright/",
  cookies: "cookie-policy/",
};

/* A market page keeps its own three pages — a Spanish visitor lands on the
   Spanish home, books from the Spanish tutor list and applies on the Spanish
   join page — and links out to the English tree for everything else.

   These are relative to the market's own root, not to the page: /ar/ holds the
   Arabic home, tutor list and join page, and /ar/hindi/ is a page inside that
   market. Writing "find-tutors.html" from /ar/hindi/ pointed at
   /ar/hindi/find-tutors.html, which does not exist — 24 broken links, on
   every page of every market, since the day the shell went in. */
const LOCAL = { findTutors: "find-tutors.html", join: "join.html" };

/* --------------------------------------------------------------------------
   the blocks
   -------------------------------------------------------------------------- */

const localeOf = (file) => LOCALES.includes(file.split(path.sep)[0]) ? file.split(path.sep)[0] : "";

function labeller(loc, dict) {
  const d = (dict || {})[loc] || {};
  return function (english, key) {
    /* No dictionary entry is not a reason to break the shell: English is the
       site's default language. Only a locale page asks for a translation. */
    return loc ? (d[key] || english) : english;
  };
}

function anchor(href, english, key, label, loc) {
  const i18n = loc ? ` data-i18n="${key}"` : "";
  return `<a href="${esc(href)}"${i18n}>${esc(label)}</a>`;
}

/* js/main.js fills #lang-switch with the seven market links. Only the pages
   that load it get the empty div — on a page with no switcher it would be an
   8px gap in the mobile drawer. */
const LANGSWITCH = '      <div class="lang-wrap" id="lang-switch"></div>';

function headerHTML(p, shell, loc, dict, hasMain) {
  const L = labeller(loc, dict);
  /* l is the market's own root: one level up from the page for /ar/xx/, and
     the page's own directory for the market home itself. */
  const l = loc ? p.replace(/^\.\.\//, "") : p;
  const href = (target) => {
    if (!loc) return p + TARGETS[target];
    if (target === "home") return l;
    if (LOCAL[target]) return l + LOCAL[target];
    return p + TARGETS[target];
  };
  const nav = NAV.map(([en, key, target]) =>
    "      " + anchor(href(target), en, key, L(en, key), loc)).join("\n");
  return `${H_START}
<header class="hdr">
  <a class="skip" href="#main">${esc(L("Skip to content", "nav.skip"))}</a>
  <div class="hdr-in">
    <a class="logo" href="${esc(href("home"))}">
      <img class="logo-img" src="${esc(p)}images/logo.svg" width="38" height="38" alt="EkGuru">
      <span><span data-brand>EkGuru</span><small data-tagline>${esc(shell.tagline)}</small></span>
    </a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><span></span></button>
    <nav class="nav" aria-label="Main">
${nav}
      <a class="btn btn-primary btn-sm" href="${esc(href("findTutors"))}"${loc ? ' data-i18n="nav.cta"' : ""}>${esc(L(CTA[0], CTA[1]))}</a>
${hasMain ? LANGSWITCH + "\n" : ""}    </nav>
  </div>
</header>
<script src="${p}js/site-shell.js" defer></script>
<script src="${p}js/copywatch.js" defer></script>
${H_END}`;
}

function footerHTML(p, shell, loc, dict) {
  const L = labeller(loc, dict);
  const l = loc ? p.replace(/^\.\.\//, "") : p;
  const href = (target) => {
    if (!loc) return p + TARGETS[target];
    if (target === "home") return l;
    if (LOCAL[target]) return l + LOCAL[target];
    return p + TARGETS[target];
  };
  const mode = shell.mode
    ? ` · <span class="ftr-mode" data-mode>${esc(shell.mode)}</span>`
    : "";
  /* The address is a link in the legal column — from the settings sheet, not
     typed into the markup. */
  const renderLink = ([en, key, target]) => target === "email"
    ? `      <a href="mailto:${esc(shell.email)}">${esc(shell.email)}</a>`
    : "      " + anchor(href(target), en, key, L(en, key), loc);
  const cols = COLUMNS.map(([heading, hkey, links]) => {
    const hi = loc ? ` data-i18n="${hkey}"` : "";
    return `    <div>
      <h3${hi}>${esc(L(heading, hkey))}</h3>
${links.map(renderLink).join("\n")}
    </div>`;
  }).join("\n");
  return `${F_START}
<footer class="ftr">
  <div class="wrap ftr-in">
    <div>
      <a class="logo" href="${esc(href("home"))}">
        <img class="logo-img" src="${esc(p)}images/logo.svg" width="38" height="38" alt="EkGuru">
        <span><span data-brand>EkGuru</span><small data-tagline>${esc(shell.tagline)}</small></span>
      </a>
      <p style="margin-top:14px"${loc ? ' data-i18n="ftr.about"' : ""}>${esc(L("Online Hindi lessons with independent tutor profiles.", "ftr.about"))}</p>
    </div>
${cols}
  </div>
  <div class="wrap ftr-bot">
    <p class="ftr-founder">Written and maintained by Prakash in Jaipur, India.</p>
    <p>© <span data-year>${new Date().getFullYear()}</span> <span data-brand>EkGuru</span> — <span data-tagline>${esc(shell.tagline)}</span>${mode}</p>
  </div>
</footer>
${F_END}`;
}

/* --------------------------------------------------------------------------
   rewriting one page
   -------------------------------------------------------------------------- */

function between(text, start, end) {
  const i = text.indexOf(start);
  if (i === -1) return null;
  const j = text.indexOf(end, i);
  if (j === -1) return null;
  return { i, j: j + end.length, body: text.slice(i + start.length, j) };
}

function stripMarkers(body, start, end) {
  return body.split(start).join("").split(end).join("").replace(/^\n+|\n+$/g, "");
}

function replaceBetween(text, start, end, body) {
  const span = between(text, start, end);
  if (!span) return null;
  const inner = stripMarkers(body, start, end);
  /* start + body + end. Forgetting the end marker here is not cosmetic:
     the next run cannot find the block, so it appends a second header. */
  return text.slice(0, span.i) + start + "\n" + inner + "\n" + end + text.slice(span.j);
}

/* The hand-written chrome this tool replaces. Class-restricted on purpose:
   <footer> is a content element too — a testimonial citation
   (<blockquote><footer>— Student</footer></blockquote>) must survive, and on
   the tutor pages there are several of them. */
const OWN_HEADER = /<header[^>]*\bclass="[^"]*\bhdr\b[^"]*"[^>]*>[\s\S]*?<\/header>[ \t]*\n?/i;
const OWN_FOOTER = /<footer[^>]*\bclass="[^"]*(?:\bftr\b|\bpw-ftr\b|\bcourse-footer\b)[^"]*"[^>]*>[\s\S]*?<\/footer>[ \t]*\n?/i;

const HOLD_H = "\u0000ekguru-held-header\u0000";
const HOLD_F = "\u0000ekguru-held-footer\u0000";

/* Replace every unmarked match of `re`, keeping the page's own position for
   the first one. A second footer is removed rather than left stacked. */
function swapChrome(out, re, block, what) {
  let first = true, count = 0;
  for (;;) {
    const m = re.exec(out);
    if (!m) break;
    const inner = m[0];
    const tag = what === "header" ? /<header[\s>]/i : /<footer[\s>]/i;
    if (tag.test(inner.slice(1))) {
      throw new Error(`nested <${what}> inside the ${what} being replaced — ` +
        "fix the page by hand, then re-run");
    }
    out = out.slice(0, m.index) + (first ? block : "") + out.slice(m.index + m[0].length);
    first = false;
    count++;
  }
  return { out, count };
}

/* Pages that set their own body layout, and the Google verification file with
   no body at all: not wrapped, on purpose. */
const MAIN_SKIP = new Set(["admin.html", "googleb3b0e3defc1daa17.html"]);

function ensureMain(html, file) {
  if (MAIN_SKIP.has(file.replace(/^\.\//, ""))) return html;

  if (/<main\b/i.test(html)) {
    return html.replace(/<main\b(?![^>]*\bid=)/i, '<main id="main"');
  }

  const hEnd = html.indexOf(H_END);
  let from = hEnd >= 0 ? hEnd + H_END.length : -1;
  if (from < 0) {
    const m = html.match(/<\/header\s*>/i);
    if (m) from = m.index + m[0].length;
  }
  if (from < 0) {
    const m = html.match(/<body[^>]*>/i);
    if (m) from = m.index + m[0].length;
  }
  if (from < 0) return html;

  const fAt = html.indexOf(F_START);
  const to = fAt >= 0 ? fAt : html.lastIndexOf("</body>");
  if (to <= from) return html;

  return html.slice(0, from) + "\n<main id=\"main\">" +
    html.slice(from, to) + "</main>\n" + html.slice(to);
}

function rebuild(html, file, shell, dict) {
  if (!/<\/body>/i.test(html)) return null;

  /* A half-written block is worse than no block: with the start marker but
     no end marker the page keeps its old header forever and --check reports
     it up to date. Refuse loudly instead — this happened once, when an
     earlier revision of replaceBetween nested the markers, and the only
     reason it was caught is that the missing <script> was visible. */
  for (const [name, a, b] of [["header", H_START, H_END], ["footer", F_START, F_END]]) {
    const hasA = html.includes(a), hasB = html.includes(b);
    if (hasA !== hasB) {
      throw new Error(`${file}: ${name} markers are unbalanced ` +
        `(${hasA ? "start" : "end"} without ${hasA ? "end" : "start"}) — ` +
        "fix the page by hand, then re-run");
    }
  }

  const loc = localeOf(file);
  const p = prefixFor(file);
  const hasMain = /<script[^>]+js\/main\.js/.test(html);
  let out = html;
  let touched = false;
  const stats = { replacedHeader: 0, replacedFooter: 0, injectedHeader: 0, injectedFooter: 0 };

  /* 1. hold the existing shell blocks aside, so step 2 cannot see them.
     The second span is measured AFTER the first substitution: replacing a
     900-character header with a 22-character token moves every index behind
     it, and a stale index cuts into the middle of the footer — which is
     exactly the corruption this comment exists to prevent. */
  const hadHeader = between(out, H_START, H_END);
  if (hadHeader) out = out.slice(0, hadHeader.i) + HOLD_H + out.slice(hadHeader.j);
  const hadFooter = between(out, F_START, F_END);
  if (hadFooter) out = out.slice(0, hadFooter.i) + HOLD_F + out.slice(hadFooter.j);

  /* 2. remove the hand-written chrome (its position is kept for the first) */
  const head = swapChrome(out, OWN_HEADER, "", "header");
  out = head.out;
  stats.replacedHeader = head.count;
  const foot = swapChrome(out, OWN_FOOTER, "", "footer");
  out = foot.out;
  stats.replacedFooter = foot.count;

  /* 3. put the shell back — fresh markup at the old position, or a new one */
  if (out.includes(HOLD_H)) {
    out = out.split(HOLD_H).join(headerHTML(p, shell, loc, dict, hasMain));
    touched = true;
  } else {
    const m = out.match(/<body[^>]*>/i);
    /* after <body>, before anything else: the skip link and the page
       wrapper stay exactly where they were */
    const at = m ? m.index + m[0].length : out.indexOf("\n");
    out = out.slice(0, at) + "\n" + headerHTML(p, shell, loc, dict, hasMain) + out.slice(at);
    touched = true;
    stats.injectedHeader = 1;
  }

  if (out.includes(HOLD_F)) {
    out = out.split(HOLD_F).join(footerHTML(p, shell, loc, dict));
    touched = true;
  } else {
    const at = out.lastIndexOf("</body>");
    out = out.slice(0, at) + footerHTML(p, shell, loc, dict) + "\n" + out.slice(at);
    touched = true;
    stats.injectedFooter = 1;
  }

  /* 4. THE PAGE SKELETON — one <main id="main">, so the skip link in the
     header has somewhere to land. The shell header has carried
     <a class="skip" href="#main"> since v150 and only 30 of 1,564 pages had
     the target: pressing it did nothing on every other page. Rather than
     hand-place the landmark 1,500 times, wrap what is between the header and
     the footer — the content, bands and scripts — which is what the element
     means. Pages that already mark their own main (the v200 ones) keep it and
     only gain the id. */
  out = ensureMain(out, file);

  /* the pages that write their own chrome used to be the only ones with a
     hand-written header, and they were the only ones without copywatch */
  if (!/js\/copywatch\.js/.test(out)) {
    const anchorTag = out.match(/<script src="([^"]*js\/(?:experience|main)\.js)"[^>]*><\/script>/);
    if (anchorTag) {
      out = out.slice(0, anchorTag.index + anchorTag[0].length) +
        '\n<script src="' + anchorTag[1].replace(/js\/(experience|main)\.js$/, "js/copywatch.js") + '" defer></script>' +
        out.slice(anchorTag.index + anchorTag[0].length);
      touched = true;
    }
  }

  /* The tagline, one last time and unconditionally: this catches a page
     whose header was left alone because it was already right, and any
     hand-written <small data-tagline> outside the shell markers. */
  const aligned = out
    .replace(/(<span data-tagline>)[^<]*(<\/span>)/g, `$1${esc(shell.tagline)}$2`)
    .replace(/(<small data-tagline>)[^<]*(<\/small>)/g, `$1${esc(shell.tagline)}$2`);
  if (aligned !== out) { out = aligned; touched = true; }

  /* The comparison, not a `touched` flag: the shell is re-emitted on every
     pass to keep one code path, so "did anything change" is only knowable by
     looking at the result. Without this, every page is rewritten on every
     run and --check can never pass. */
  void touched;
  return out === html ? null : { html: out, stats };
}

/* --------------------------------------------------------------------------
   main
   -------------------------------------------------------------------------- */

function main() {
  const check = process.argv.includes("--check");
  const verbose = process.argv.includes("--verbose");
  const site = loadSite();
  const settings = site.settings || {};
  const config = site.site || {};
  const dict = loadI18n();

  const shell = {
    tagline: settings.tagline || config.tagline || "One Student. One Guru. One Goal.",
    mode: settings.mode || "",
    email: settings.email || config.email || "EkGuruLearning@gmail.com",
  };

  const pages = walk(".", []).sort();
  let written = 0, stale = 0, injected = 0, aligned = 0, oldChrome = 0;

  for (const file of pages) {
    const html = fs.readFileSync(file, "utf8");
    const res = rebuild(html, file, shell, dict);
    if (res === null) continue;
    const stats = res.stats;
    const hadOwn = stats.replacedHeader + stats.replacedFooter > 0;
    if (stats.injectedHeader) injected++;
    else aligned++;
    if (hadOwn) oldChrome++;
    if (check) {
      console.log("STALE " + file);
      stale++;
      continue;
    }
    fs.writeFileSync(file, res.html);
    written++;
    if (verbose) {
      console.log(`wrote ${file}` +
        (hadOwn ? ` (replaced ${stats.replacedHeader} header / ${stats.replacedFooter} footer block(s))` : ""));
    }
  }

  if (!written && !stale) {
    console.log(`ok    all ${pages.length} page(s) carry the same header and footer`);
  } else {
    console.log(`${check ? "stale: " : "updated: "} ${stale || written} page(s)` +
      ` (${injected} got the shell, ${aligned} refreshed` +
      (oldChrome ? `, ${oldChrome} had hand-written chrome replaced` : "") + ")");
  }
  console.log(`      tagline: "${shell.tagline}"  from ${settings.tagline ? "the settings sheet" : "js/site-config.js"}` +
    `  ·  mode: ${shell.mode || "(unset)"}` +
    `  ·  market pages: ${LOCALES.length} locales from js/i18n.js`);
  if (check && stale) process.exit(1);
}

main();
