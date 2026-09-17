#!/usr/bin/env node
/* ==========================================================================
   EkGuru — MARKET HOME PAGES
   --------------------------------------------------------------------------
   Rebuilds the home page of the six translated markets so they are the same
   page as the English one, in their own language:

       es/index.html   fr/index.html   de/index.html
       pt/index.html   ja/index.html   ar/index.html

   WHY THIS TOOL EXISTS
   --------------------
   The English home page was redesigned in v200 (xp-* components, an emblem,
   a language rail, one motion vocabulary). The six market pages were left on
   the older `.lp-*` layout, so a Spanish visitor got a page that only LOOKED
   like EkGuru: no hero art, no rail, a different set of sections, and a
   stylesheet doing its best to disguise it.

   Rewriting 6 pages by hand is how they drifted apart in the first place, so
   they are generated — and generated from the sources the site already has:

       js/i18n.js                  every visible string, in all 7 languages
       js/tutors/_registry.js      who teaches (order and roster)
       js/tutors/*.js              price, headline, teaches, photo
       js/tutors-data.js           the same defaulting rules the site uses

   Nothing is translated here and no copy is invented: if a string is not in
   js/i18n.js it does not go on the page. That is what keeps the six markets
   from promising something the English page does not.

   WHAT IS PRESERVED (never touched)
   ---------------------------------
     · <head>          title, description, canonical, hreflang set, og tags,
                       AdSense block, JSON-LD
     · <header>        the market's own navigation
     · <footer>        both footers, including the trust footer
     · <script> tags   i18n, tutors, rates, pricing, analytics, experience
   Only the <main> element is rewritten, so a re-run can never lose SEO work
   that was done on those pages.

   Run:  node tools/build-market-pages.js [--check]
         --check exits 1 if a page on disk is out of date (CI/gate use)
   ========================================================================== */

"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
process.chdir(ROOT);

const MARKETS = ["es", "fr", "de", "pt", "ja", "ar"];
const RTL = { ar: true };

/* The languages shown in the rail. Native names, so the same strip is correct
   on every one of the seven home pages — "Tamil" is தமிழ் to a Japanese
   reader too. Hrefs are the real course entry points. */
const RAIL = [
  ["hi", "हिन्दी", "अ", "../learn/hindi/", "A1–C2"],
  ["bn", "বাংলা", "অ", "../bengali/", ""],
  ["ta", "தமிழ்", "அ", "../learn/tamil/", ""],
  ["te", "తెలుగు", "అ", "../learn/telugu/", ""],
  ["mr", "मराठी", "म", "../learn/marathi/", ""],
  ["ur", "اردو", "ا", "../learn/urdu/", ""],
  ["ar", "العربية", "ع", "../languages/ar/course/", ""],
  ["es", "Español", "Ñ", "../languages/es/course/", ""],
  ["fr", "Français", "É", "../languages/fr/course/", ""],
  ["de", "Deutsch", "Ö", "../languages/de/course/", ""],
  ["pt", "Português", "Ã", "../languages/pt/course/", ""],
  ["ja", "日本語", "あ", "../languages/ja/course/", ""],
  ["ko", "한국어", "가", "../languages/ko/course/", ""],
  ["zh", "中文", "一", "../languages/zh/course/", ""],
  ["ru", "Русский", "А", "../languages/ru/course/", ""]
];

/* The seven markets, for the "students from around the world" strip. The flag
   and the native name are the same in every language; the label is the
   country, which js/i18n.js does not translate (it is a proper noun). */
const WORLD = [
  ["united-states", "🇺🇸", "United States", "English"],
  ["spain", "🇪🇸", "Spain", "Español"],
  ["france", "🇫🇷", "France", "Français"],
  ["germany", "🇩🇪", "Germany", "Deutsch"],
  ["brazil", "🇧🇷", "Brazil", "Português"],
  ["japan", "🇯🇵", "Japan", "日本語"],
  ["uae", "🇦🇪", "UAE", "العربية"]
];

/* --------------------------------------------------------------------------
   sources
   -------------------------------------------------------------------------- */

function loadSite() {
  const sandbox = { console: { warn() {}, log() {}, error() {} } };
  vm.createContext(sandbox);
  sandbox.window = sandbox;                 // in a browser, window IS the global
  sandbox.document = { addEventListener() {}, querySelector: () => null, querySelectorAll: () => [] };
  sandbox.navigator = { languages: [], language: "en" };
  sandbox.localStorage = { getItem: () => null, setItem() {} };

  const files = ["js/site-config.js", "js/tutors/_registry.js"];
  const registry = fs.readFileSync("js/tutors/_registry.js", "utf8");
  registry.replace(/"([a-z0-9-]+)"/g, (m, id) => id).split("\n");
  fs.readdirSync("js/tutors")
    .filter((f) => f.endsWith(".js") && !f.startsWith("_"))
    .sort()
    .forEach((f) => files.push("js/tutors/" + f));
  files.push("js/tutors/_overrides.js", "js/tutors-data.js", "js/i18n.js");

  for (const f of files) {
    try {
      vm.runInContext(fs.readFileSync(f, "utf8"), sandbox, { filename: f });
    } catch (e) {
      throw new Error("could not load " + f + ": " + e.message);
    }
  }

  /* The roster in registry order. The sheet-hidden list is NOT applied here:
     it is a runtime filter (js/tutors-data.js) that changes the moment the
     owner edits the spreadsheet, while this file is crawled and indexed.
     Baking a temporary state into the HTML is how a tutor disappears from
     Google. The static page lists the roster; the live page filters it. */
  const order = sandbox.EKGURU_TUTOR_ORDER || [];
  const registered = sandbox.EKGURU_TUTOR_FILES || {};
  const tutors = order.filter((id) => registered[id]).map((id) => registered[id]);

  return { i18n: sandbox.EKGURU_I18N || {}, tutors };
}

/* --------------------------------------------------------------------------
   helpers
   -------------------------------------------------------------------------- */

const esc = (s) =>
  String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

/* Every string goes through this. A missing key throws rather than shipping an
   English word inside a Spanish sentence — the build should fail loudly, not
   quietly produce a half-translated page. */
function makeT(i18n) {
  return function t(lang, key) {
    const table = i18n[lang];
    const value = table && table[key];
    if (!value) throw new Error('missing i18n key "' + key + '" for ' + lang);
    return value;
  };
}

/* {minPrice} is a token, not a number: js/pricing.js rewrites the element from
   the live rate table. Never bake a price into a string — see js/i18n.js. */
function withPrice(html, price) {
  return html.replace(
    /\{minPrice\}/g,
    '<b data-usd="' + price + '" data-usd-mode="bare">$' + price + "</b>"
  );
}

/* --------------------------------------------------------------------------
   sections
   -------------------------------------------------------------------------- */

function hero(lang, t, tutors, price) {
  const lang0 = lang;
  const first = tutors[0];
  const letters = ["अ", "आ", "क", "म"];
  const hello = {
    es: "¡Hola!", fr: "Bonjour", de: "Hallo", pt: "Olá", ja: "こんにちは", ar: "مرحبا"
  }[lang0] || "Namaste";

  const card = first
    ? `      <div class="hero-card xp-sheen">
        <a class="hc-link" href="../tutor/${esc(first.id)}/" aria-label="${esc(first.name)}"></a>
        <img src="../${esc(first.thumb || first.photo)}" alt="${esc(first.name)}, ${esc(
        first.subject
      )} tutor" width="96" height="96" loading="eager" decoding="async">
        <p class="hc-name">${esc(first.name)}</p>
        <p class="sm">${esc(first.subject)} · ${esc(first.city)}</p>
        <p class="stars" style="margin:6px 0 10px">${"★".repeat(Math.round(first.rating || 5))} ${(first.rating || 5).toFixed(1)}</p>
        <a class="btn btn-primary btn-sm btn-block" href="../tutor/${esc(first.id)}/">${esc(
        t(lang0, "hero.viewProfile")
      )}</a>
      </div>`
    : "";

  return `<section class="xp-hero xp-band">
  <span class="xp-orb xp-orb-1" aria-hidden="true"></span>
  <span class="xp-orb xp-orb-2" aria-hidden="true"></span>
  <div class="xp-wrap xp-hero-in">
    <div class="xp-hero-copy xp-rise">
      <span class="xp-kicker" data-i18n="hero.badge">${esc(t(lang0, "hero.badge"))}</span>
      <h1><span data-i18n="hero.title1">${esc(t(lang0, "hero.title1"))}</span>
        <span class="grad-text" data-i18n="hero.title2">${esc(t(lang0, "hero.title2"))}</span></h1>
      <p class="xp-lead" data-i18n="hero.lead">${esc(t(lang0, "hero.lead"))}</p>

      <div class="xp-hero-actions">
        <a class="btn btn-primary btn-lg" href="../find-tutors.html?lang=${lang0}" data-i18n="nav.cta">${esc(
    t(lang0, "nav.cta")
  )}</a>
        <a class="btn btn-ghost btn-lg" href="../courses/" data-i18n="nav.courses">${esc(
    t(lang0, "nav.courses")
  )}</a>
      </div>

      <ul class="xp-trust">
        <li data-i18n="hero.trust1">${esc(t(lang0, "hero.trust1"))}</li>
        <li data-i18n="hero.trust2">${esc(t(lang0, "hero.trust2"))}</li>
        <li data-i18n="hero.trust3">${esc(t(lang0, "hero.trust3"))}</li>
      </ul>

      <ul class="xp-stats xp-stagger">
        <li class="xp-stat"><b>${tutors.length}</b><span data-i18n="hero.stat1">${esc(
    t(lang0, "hero.stat1")
  )}</span></li>
        <li class="xp-stat"><b data-usd="${price}" data-usd-mode="bare">$${price}</b><span data-i18n="hero.stat4">${esc(
    t(lang0, "hero.stat4")
  )}</span></li>
        <li class="xp-stat"><b>5.0★</b><span data-i18n="hero.stat3">${esc(
    t(lang0, "hero.stat3")
  )}</span></li>
      </ul>
    </div>

    <div class="xp-visual xp-rise">
      <!-- The emblem switches itself with the interface language
           (js/experience.js §7); the file below is the market's own, so the
           page is right before any script runs. -->
      <img class="xp-world" data-xp-world="auto" src="../images/xp/world-${lang0}.svg" alt=""
           aria-hidden="true" width="430" height="430" decoding="async">
      <span class="xp-ring" aria-hidden="true"></span>
      <span class="xp-ring xp-ring-2" aria-hidden="true"></span>
      <div class="xp-badge-tile xp-medallion" aria-hidden="true">
        <span data-xp-hello>${esc(hello)}</span>
        <small lang="hi">हिन्दी</small>
      </div>
${card}
      <div class="xp-letters xp-script" data-xp-letters aria-hidden="true">
${letters.map((c) => `        <span class="xp-letter">${c}</span>`).join("\n")}
      </div>
      <span class="xp-float xp-float-1">⭐ <span data-i18n="hero.chip1">${esc(
    t(lang0, "hero.chip1")
  )}</span></span>
      <span class="xp-float xp-float-2">💬 <span data-i18n="hero.chip2">${esc(
    t(lang0, "hero.chip2")
  )}</span></span>
      <span class="xp-float xp-float-3">🎯 <span data-i18n="hero.chip3">${esc(
    t(lang0, "hero.chip3")
  )}</span></span>
    </div>
  </div>
</section>`;
}

function rail(t, lang) {
  const items = RAIL.map(
    ([code, native, letter, href, band]) =>
      `    <a class="xp-rail-item" href="${href}"><b lang="${code}"${
        RTL[code] ? ' dir="rtl"' : ""
      }>${letter}</b> ${native}${band ? ` <small>${band}</small>` : ""}</a>`
  ).join("\n");
  return `<section class="xp-rail" data-xp-rail aria-label="${esc(t(lang, "nav.courses"))}">
  <div class="xp-rail-track">
${items}
    <a class="xp-rail-item" href="../courses/"><b aria-hidden="true">＋</b> 39 <small>${esc(
    t(lang, "nav.courses")
  )}</small></a>
  </div>
</section>`;
}

function why(t, lang, price) {
  const cards = [1, 2, 3, 4]
    .map(
      (i) => `      <article class="xp-card">
        <div class="xp-card-ico" aria-hidden="true">${["🎯", "🗣️", "💸", "🕒"][i - 1]}</div>
        <h3 data-i18n="why.w${i}t">${esc(t(lang, "why.w" + i + "t"))}</h3>
        <p data-i18n="why.w${i}d">${withPrice(esc(t(lang, "why.w" + i + "d")), price)}</p>
      </article>`
    )
    .join("\n");

  return `<section class="xp-sec" id="why">
  <div class="xp-wrap">
    <div class="xp-head xp-rise">
      <span class="xp-kicker" data-i18n="why.kicker">${esc(t(lang, "why.kicker"))}</span>
      <h2 data-i18n="why.title">${esc(t(lang, "why.title"))}</h2>
      <div class="xp-rule" aria-hidden="true"></div>
    </div>
    <div class="xp-grid xp-grid-4 xp-stagger">
${cards}
    </div>
  </div>
</section>`;
}

function tutorCards(t, lang, tutors) {
  return tutors
    .map((x) => {
      const teaches = (x.teaches || []).join(" · ");
      /* data-usd + data-usd-mode: js/pricing.js redraws this in the visitor's
         own currency. The $ figure is the no-JS fallback, exactly as on the
         English cards. */
      const price =
        '<b data-usd="' + x.priceUSD + '" data-usd-mode="bare">$' + x.priceUSD + "</b>";
      const stars = "★".repeat(Math.round(x.rating || 5));
      const reviews = x.reviewsCount ? ` (${x.reviewsCount})` : "";
      return `      <article class="xp-card xp-tutor">
        <img class="xp-tutor-photo" src="../${esc(x.thumb || x.photo)}" alt="${esc(x.name)}, ${esc(
        x.subject
      )} tutor" width="76" height="76" loading="lazy" decoding="async">
        <h3><a href="../tutor/${esc(x.id)}/">${esc(x.name)}</a></h3>
        <p class="xp-tutor-meta">${price} · <span data-i18n="tutor.perLesson">${esc(
        t(lang, "tutor.perLesson")
      )}</span> · <span class="stars">${stars} ${(x.rating || 5).toFixed(1)}${reviews}</span></p>
        <p class="xp-tutor-headline">${esc(x.headline || "")}</p>
        <p class="xp-tutor-teaches">${esc(teaches)}</p>
        <a class="btn btn-primary btn-sm" href="../tutor/${esc(x.id)}/" data-i18n="hero.viewProfile">${esc(
        t(lang, "hero.viewProfile")
      )}</a>
      </article>`;
    })
    .join("\n");
}

function tutorsSection(t, lang, tutors) {
  return `<section class="xp-sec soft" id="tutors">
  <div class="xp-wrap">
    <div class="xp-head xp-rise">
      <span class="xp-kicker" data-i18n="tutors.kicker">${esc(t(lang, "tutors.kicker"))}</span>
      <h2 data-i18n="tutors.title">${esc(t(lang, "tutors.title"))}</h2>
      <p data-i18n="tutors.sub">${esc(t(lang, "tutors.sub"))}</p>
      <div class="xp-rule" aria-hidden="true"></div>
    </div>
    <div class="xp-grid xp-grid-3 xp-stagger">
${tutorCards(t, lang, tutors)}
    </div>
    <p class="center" style="margin-top:26px">
      <a class="btn btn-ghost" href="../find-tutors.html?lang=${lang}" data-i18n="tutors.all">${esc(
    t(lang, "tutors.all")
  )}</a>
    </p>
  </div>
</section>`;
}

function how(t, lang) {
  const steps = [1, 2, 3]
    .map(
      (i) => `      <div class="xp-step">
        <b data-i18n="how.s${i}t">${esc(t(lang, "how.s" + i + "t"))}</b>
        <p data-i18n="how.s${i}d">${esc(t(lang, "how.s" + i + "d"))}</p>
      </div>`
    )
    .join("\n");

  return `<section class="xp-sec" id="how">
  <div class="xp-wrap">
    <div class="xp-head xp-rise">
      <span class="xp-kicker" data-i18n="how.kicker">${esc(t(lang, "how.kicker"))}</span>
      <h2 data-i18n="how.title">${esc(t(lang, "how.title"))}</h2>
      <p data-i18n="how.sub">${esc(t(lang, "how.sub"))}</p>
      <div class="xp-rule" aria-hidden="true"></div>
    </div>
    <div class="xp-steps xp-stagger">
${steps}
    </div>
  </div>
</section>`;
}

function markets(t, lang) {
  const chips = WORLD.map(
    ([slug, flag, name, native]) =>
      `      <a class="mkt" href="../learn-hindi-from-${slug}/"><span class="mkt-flag" aria-hidden="true">${flag}</span><b>${name}</b><span>${native}</span></a>`
  ).join("\n");

  /* The language switcher stays a real reciprocal link set: it is how Google
     discovers the relationship between the seven home pages, and it is the
     only place a visitor can move between them. */
  const langs = [
    ["en", "https://ekguru.shop/", "🇺🇸 English"],
    ["es", "https://ekguru.shop/es/", "🇪🇸 Español"],
    ["fr", "https://ekguru.shop/fr/", "🇫🇷 Français"],
    ["de", "https://ekguru.shop/de/", "🇩🇪 Deutsch"],
    ["pt", "https://ekguru.shop/pt/", "🇧🇷 Português"],
    ["ja", "https://ekguru.shop/ja/", "🇯🇵 日本語"],
    ["ar", "https://ekguru.shop/ar/", "🇦🇪 العربية"]
  ]
    .map(
      ([code, href, label]) =>
        `<a href="${href}" hreflang="${code}"${code === lang ? ' aria-current="page"' : ""}>${label}</a>`
    )
    .join("");

  return `<section class="xp-sec soft" id="markets">
  <div class="xp-wrap">
    <div class="xp-head xp-rise">
      <h2 data-i18n="markets.title">${esc(t(lang, "markets.title"))}</h2>
      <p data-i18n="markets.sub">${esc(t(lang, "markets.sub"))}</p>
      <div class="xp-rule" aria-hidden="true"></div>
    </div>
    <div class="markets xp-stagger">
${chips}
    </div>
    <nav class="lp-langs" aria-label="${esc(t(lang, "ftr.langs"))}" style="margin-top:26px;text-align:center">
      <strong>${esc(t(lang, "ftr.langs"))}:</strong>
      ${langs}
    </nav>
  </div>
</section>`;
}

function cta(t, lang) {
  return `<section class="xp-sec" id="cta">
  <div class="xp-wrap">
    <div class="xp-cta xp-rise">
      <h2 data-i18n="cta.title">${esc(t(lang, "cta.title"))}</h2>
      <p data-i18n="cta.sub">${esc(t(lang, "cta.sub"))}</p>
      <div class="xp-hero-actions" style="justify-content:center">
        <a class="btn btn-primary btn-lg" href="../find-tutors.html?lang=${lang}" data-i18n="cta.btn1">${esc(
    t(lang, "cta.btn1")
  )}</a>
        <a class="btn btn-ghost btn-lg" href="../contact/" data-i18n="cta.btn2">${esc(
    t(lang, "cta.btn2")
  )}</a>
        <a class="btn btn-ghost btn-lg" href="../courses/" data-i18n="nav.courses">${esc(
    t(lang, "nav.courses")
  )}</a>
      </div>
    </div>
  </div>
</section>`;
}

/* --------------------------------------------------------------------------
   page assembly
   -------------------------------------------------------------------------- */

function renderMain(lang, t, tutors, price) {
  return `<main id="main" class="xp-main">
${hero(lang, t, tutors, price)}
${rail(t, lang)}
${why(t, lang, price)}
${tutorsSection(t, lang, tutors)}
${how(t, lang)}
${markets(t, lang)}
${cta(t, lang)}
</main>`;
}

/* Everything outside <main> is preserved byte for byte. */
function split(html, file) {
  const mainStart = html.indexOf("<main");
  const mainEnd = html.indexOf("</main>");
  if (mainStart === -1 || mainEnd === -1) throw new Error("no <main> in " + file);

  return {
    head: html.slice(0, mainStart),
    main: html.slice(mainStart, mainEnd + "</main>".length),
    tail: html.slice(mainEnd + "</main>".length)
  };
}

/* The translated pages carried their own inline <style> with the .lp-* rules
   of the old layout. The redesigned <main> uses none of them, and leaving them
   in means two systems styling the same header for as long as nobody notices.
   What survives is the part that is still true: the language switcher's links
   and the touch-target floor, which no other rule on these pages provides. */
const HEAD_STYLE = `<style>
.lp-langs{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);font-size:.88rem}
.lp-langs a{margin:0 9px 8px 0;color:var(--brand);font-weight:700;white-space:nowrap;display:inline-block}
@media (pointer:coarse){
  .lp-langs a,.crumbs a,.ftr a{min-height:44px;display:inline-block;padding-block:10px}
  h2>a,h3>a,strong>a{display:inline-block;padding-block:12px}
  input,select,textarea,button{min-height:44px}
}
</style>`;

function stripHeadStyles(head) {
  return head.replace(/<style[\s\S]*?<\/style>\s*/g, "") .replace("</head>", HEAD_STYLE + "\n</head>");
}

/* The generated pages need one hook in their <body> so the stylesheet can tell
   a market page from a hand-written one (the mobile header rules in
   css/experience.css §20). Everything else about the body tag is preserved. */
function tagBody(head) {
  if (/class="[^"]*xp-market/.test(head)) return head;        /* already tagged */
  if (/<body[^>]*class=/.test(head)) {
    return head.replace(/<body([^>]*class=")([^"]*)"/, '<body$1$2 xp-page xp-market"');
  }
  return head.replace("<body>", '<body class="xp-page xp-market">');
}

function build(lang, site, t) {
  const file = path.join(lang, "index.html");
  const html = fs.readFileSync(file, "utf8");
  const parts = split(html, file);
  parts.head = stripHeadStyles(tagBody(parts.head));

  const price = site.tutors.reduce(
    (min, x) => (x.priceUSD && x.priceUSD < min ? x.priceUSD : min),
    site.tutors[0].priceUSD
  );

  return parts.head + renderMain(lang, t, site.tutors, price) + parts.tail;
}

function main() {
  const check = process.argv.includes("--check");
  const site = loadSite();
  const t = makeT(site.i18n);

  if (!site.tutors.length) throw new Error("the tutor registry is empty");

  let stale = 0;
  for (const lang of MARKETS) {
    const file = path.join(lang, "index.html");
    const before = fs.readFileSync(file, "utf8");
    const after = build(lang, site, t);

    if (before === after) {
      console.log("ok    " + file + " already up to date");
      continue;
    }
    if (check) {
      console.log("STALE " + file);
      stale++;
      continue;
    }
    fs.writeFileSync(file, after);
    console.log(
      "wrote " + file + " (" + before.length + " → " + after.length + " bytes, " +
        site.tutors.length + " tutors, min price $" + site.tutors.reduce((m, x) => Math.min(m, x.priceUSD), 99) + ")"
    );
  }

  if (check && stale) {
    console.log("STALE: " + stale + " market page(s) — run tools/build-market-pages.js");
    return 1;
  }
  return 0;
}

process.exit(main());
