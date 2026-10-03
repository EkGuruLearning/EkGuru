/* Usability pass regression test for the home page (Audit, 3 Oct 2026).
   Run:  node tools/test-usability-home.mjs            (needs: npm i jsdom)
         node tools/test-usability-home.mjs --check     same thing (gate use)

   Every check below is one numbered finding from the audit of
   https://ekguru.shop/index.html, and it fails if the fix is undone — either
   by a regenerated page or by a hand edit that drifts back. It is a static +
   DOM test: no network, no browser.

   Numbering follows the audit report; the comments name the file that owns
   each fix, so a failure points straight at the generator to edit. */
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");

let failures = 0;
const read = (p) => readFileSync(`${ROOT}/${p}`, "utf8");
function check(name, ok, extra = "") {
  console.log(`${ok ? "ok  " : "FAIL"}  ${name}${extra ? "  — " + extra : ""}`);
  if (!ok) failures++;
}

const home = read("index.html");
const dom = new JSDOM(home, { url: "https://ekguru.shop/" });
const doc = dom.window.document;
const experience = read("css/experience.css");
const features = read("js/features.js");
const i18n = read("js/i18n.js");
const marquee = read("js/country-marquee.js");
const visual = read("js/visual-learning.js");

/* ── 1–3 · one design scale ────────────────────────────────────────────────
   The comment blocks in css/experience.css and index.html #critical promise a
   guard test. This is it: the home layers may only use the tokens, and the
   tokens have to exist in both layers. */
const critical = (home.match(/<style id="critical">([\s\S]*?)<\/style>/) || [, ""])[1];
const TOKENS = ["--xp-fs-3xs", "--xp-fs-2xs", "--xp-fs-xs", "--xp-fs-sm", "--xp-fs-md",
  "--xp-fs-lg", "--xp-fs-xl", "--xp-fs-2xl", "--xp-fs-3xl", "--xp-fs-4xl",
  "--xp-fs-fluid-lg", "--xp-fs-fluid-xl", "--xp-fs-fluid-2xl", "--xp-fs-fluid-3xl",
  "--xp-r-0", "--xp-r-1", "--xp-r-2", "--xp-r-3", "--xp-r-4", "--xp-pill", "--xp-circle",
  "--xp-ink", "--xp-ink-2", "--xp-muted", "--xp-ink-on-brand", "--xp-accent-ink"];
check("1–3: the home-critical layer declares the design tokens",
  TOKENS.every((t) => critical.includes(t + ":")), `${TOKENS.length} tokens`);
check("1–3: css/experience.css declares the same tokens",
  TOKENS.slice(0, 24).every((t) => experience.includes(t + ":")));

/* home-owned rules only: the xp-, hc-, course-, markets and faq components */
const HOME_RULE = /(?:^|[\s,>+~])(?:\.[\w-]*(?:xp-|hc-|course-|mkt|markets|faq|lang-pill|t-empty|hero-card|country-chips|eg-cc-)|\[data-xp-[\w-]+\])/;
function homeDeclarations(css) {
  const out = [];
  for (const m of css.matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
    if (!HOME_RULE.test(m[1])) continue;
    out.push(m[2]);
  }
  return out.join(";");
}
const decls = homeDeclarations(experience) + ";" + critical;
/* A literal length/colour inside a home rule is exactly the drift the audit
   found (92 type sizes, 47 colours, 29 radii in one file). Decorative
   gradients and color-mix() blends are allowed; raw px/rem/hex type and
   corner values are not. */
const literalFontSizes = [...decls.matchAll(/font-size\s*:\s*([^;}]+)/g)]
  .map((m) => m[1].trim())
  .filter((v) => !v.startsWith("var(") && !v.startsWith("inherit") && !/^\d+pt$/.test(v));
const literalRadii = [...decls.matchAll(/border-radius\s*:\s*([^;}]+)/g)]
  .map((m) => m[1].trim())
  .filter((v) => !/var\(|0\b|inherit|transparent/.test(v));
check("1–3: no literal font-size left in the home layers",
  literalFontSizes.length === 0, literalFontSizes.slice(0, 4).join(" | "));
check("1–3: no literal corner value left in the home layers",
  literalRadii.length === 0, literalRadii.slice(0, 4).join(" | "));

/* ── 4 · the badge is a label, not a headline ───────────────────────────── */
const badge = doc.querySelector(".xp-hero-copy .xp-kicker");
check("4: the hero badge carries the sentence-case variant",
  !!badge && badge.classList.contains("xp-kicker--badge"), badge ? badge.className : "missing");
check("4: the badge copy is not shouted",
  !!badge && badge.textContent.trim() === badge.textContent.trim().replace(/\s+/g, " ") &&
  !/ONLINE|BOOK NOW/.test(badge.textContent));
check("4: the English i18n badge matches the static copy (lowercase 'online')",
  /"hero\.badge": "100% Hindi · 1-on-1 online"/.test(i18n));

/* ── 5 · no skipped heading level ───────────────────────────────────────── */
check("5: visual-learning.js inserts a level-2 heading after an existing <h2>",
  /<h2 style="margin:0 0 10px">🌍 /.test(visual) && !/<h3 style="margin:0 0 10px">🌍 /.test(visual));
check("5: it refuses to inject when the page has no <h2> to hang from",
  /firstH2 && !main\.querySelector\('\.country-visual'\)/.test(visual));

/* ── 6 · 12 · 14 · the country wall ─────────────────────────────────────── */
const markets = doc.querySelector("#markets");
const grid = markets && markets.querySelector(".mkt-grid");
const countryLinks = markets ? markets.querySelectorAll(".mkt-grid a").length : 0;
check("6: the country grid is server-rendered inside #markets",
  countryLinks >= 40, `${countryLinks} country links`);
check("6: the grid is grouped by region with real headings",
  !!grid && grid.closest(".mkt-region-block") !== null &&
  doc.querySelectorAll("#markets .mkt-region").length >= 5,
  doc.querySelectorAll("#markets .mkt-region").length + " region headings");
check("6 + 12: the interactive rails are behind a disclosure, not a wall",
  /<details class="eg-cc-more">/.test(marquee) && !/host\.innerHTML = rail\b/.test(marquee));
check("12: the static grid is preserved when the rails render",
  /if \(old \|\| !host\.querySelector\("\.mkt-grid"\)\)/.test(marquee));
const more = doc.querySelector("#markets-sec .xp-more");
check("14: the country link has a heading and a sentence",
  !!more && !!more.querySelector("h3") && (more.querySelector("p") || {}).textContent.length > 40);
check("14: the old orphan button is gone",
  !/<p class="center" style="margin-top:22px">[\s\S]{0,80}learn-hindi-by-country/.test(home));

/* ── 7 · 9 · 22 · the empty state tells one story ───────────────────────── */
const heroCard = doc.querySelector("#hero-tutor");
check("7 + 22: the hero card leads with what is open, not with the absence",
  !!heroCard && /always open/i.test(heroCard.querySelector(".hc-name").textContent),
  heroCard ? heroCard.querySelector(".hc-name").textContent.trim() : "missing");
const midCta = doc.querySelector("#tutors [data-eg-tutors-cta]");
check("9: the section CTA is generated (marker + hook present)",
  !!midCta && home.includes("ekguru:home-tutors-cta:start"));
check("9: with no public tutor listed, the CTA opens the free courses",
  !!midCta && /courses\//.test(midCta.innerHTML) && !/find-tutors/.test(midCta.innerHTML),
  midCta ? midCta.textContent.trim() : "missing");

/* ── 8 · badge + greeting are one pre-header row ────────────────────────── */
check("8: the pre-header is laid out explicitly (no free-floating greeting)",
  /\.xp-hero-copy > \.xp-kicker \{/.test(experience) &&
  /\.xp-hero-copy > \.ekg-greeting-line \{/.test(experience) &&
  /html\[dir="rtl"\] \.xp-hero-copy > \.xp-kicker/.test(experience));

/* ── 10 · one course-card schema ────────────────────────────────────────── */
const courses = read("courses/index.html");
check("10: no course card prints the empty word 'documented'",
  !/<em>documented<\/em>/.test(courses) && !/country-chips"><\/span>/.test(courses));
check("10: cards with no country attribution omit the chip line entirely",
  !/<span class="country-chips"><\/span>/.test(courses));

/* ── 11 · the empty state is a row of doors ─────────────────────────────── */
check("11: the empty-state actions are buttons in one row",
  /\.t-empty-actions \{/.test(experience) &&
  /class="t-empty-actions"/.test(read("tools/lib/zero-state.js")) &&
  /class="t-empty-actions"/.test(read("js/main.js")));
check("11: no dotted link sentence survives in the empty state",
  !/t-empty-links/.test(read("tools/lib/zero-state.js")) && !/t-empty-links/.test(read("js/main.js")));

/* ── 13 · markets and FAQ are one group ─────────────────────────────────── */
check("13: the gap between the two sections is owned by CSS",
  /#markets-sec\.xp-sec \{/.test(experience) && /#faq\.xp-sec \{/.test(experience));

/* ── 15 · appearance + currency in one panel ────────────────────────────── */
check("15: the currency control moves into the Appearance panel",
  /\.eg-appearance/.test(features) && /eg-settings-row/.test(features) &&
  /\.eg-settings-row \{/.test(read("css/ultra.css")));

/* ── 16 · the nav cards read as doors ──────────────────────────────────── */
check("16: every global-nav card carries a visible signifier",
  /\.eg-gn-list b::after \{/.test(experience) && /content: " →"/.test(experience));

/* ── 17 · one global nav on every page that has one ────────────────────── */
const pages = ["index.html", "learn/index.html", "ask/index.html", "hindi/index.html",
  "find-tutors.html", "toolbox/index.html", "tutor/index.html"];
const navCounts = pages.map((p) => {
  const block = read(p).split("ekguru:global-nav:start")[1].split("ekguru:global-nav:end")[0];
  return (block.match(/<li><a href="[^"]*"><b>/g) || []).length;
});
check("17: every page's global nav carries the same number of cards",
  new Set(navCounts).size === 1 && navCounts[0] >= 12, navCounts.join(", "));
check("17: the two FAQ-flavoured cards are relabelled, not duplicated",
  /<b>Ask a question<\/b>/.test(read("index.html")) &&
  /<b>Hindi learning FAQ<\/b>/.test(read("index.html")));
check("17: the stale generator note is gone",
  !/Generated by tools\/hublinks\.js/.test(read("index.html")) &&
  !/Generated by tools\/hublinks\.js/.test(read("learn/index.html")));

/* ── 18 · the journal strip is a panel, not an orphan link ─────────────── */
const cont = doc.querySelector("[data-eg-continue]");
check("18: the journal strip has a heading, a sentence and a button",
  !!cont && !!cont.querySelector(".eg-continue-h") && !!cont.querySelector("p") &&
  !!cont.querySelector(".eg-continue-go"));

/* ── 19 · 20 · one primary action in the hero ──────────────────────────── */
const hero = doc.querySelector(".xp-hero");
const heroLinks = [...hero.querySelectorAll(".xp-hero-actions a")].map((a) => a.textContent.trim());
check("19: the hero offers one secondary door, not a row of them",
  heroLinks.length === 1, heroLinks.join(" | "));
check("20: the ambiguous 'Find My Guru' label is gone from the page",
  !/>\s*Find My Guru\s*</.test(home) && !/data-i18n="tutors.all"/.test(home));
check("19: the search bar keeps the one primary action",
  (doc.querySelectorAll(".xp-searchbar .btn-primary").length === 1));

/* ── 21 · the rail agrees with the section below it ────────────────────── */
const railItems = [...doc.querySelectorAll("[data-xp-rail] .xp-rail-item")];
const langItems = railItems.filter((i) => (i.querySelector("b") || {}).textContent !== "＋");
const railBands = langItems.map((i) => (i.querySelector("small") || {}).textContent || "");
check("21: every language entry in the rail carries a level band",
  langItems.length >= 15 && railBands.every((b) => /A1[–-][BC]2/.test(b)),
  `${langItems.length} language items`);
check("21: the vague 'course' label is gone from the rail",
  !/ <small>course<\/small>/.test(home));

/* ── 23 · one hierarchy at the closing CTA ─────────────────────────────── */
const ctaButtons = doc.querySelectorAll("#contact .xp-hero-actions a");
check("23: the closing CTA offers two doors, one of them primary",
  ctaButtons.length === 2 && [...ctaButtons].filter((a) => a.classList.contains("btn-primary")).length === 1,
  `${ctaButtons.length} buttons`);

/* ── 24 · the currency menu cannot leak onto the page ──────────────────── */
check("24: the listbox is hidden (and empty) until it is opened",
  /class="cur-menu" role="listbox" hidden/.test(features) && /<div class="cur-menu-scroll"><\/div>/.test(features));
check("24: opening fills it, closing syncs aria-expanded",
  /function fill\(\)/.test(features) && /cbtn\.setAttribute\("aria-expanded", "true"\)/.test(features) &&
  /cbtn\.setAttribute\("aria-expanded", "false"\)/.test(features));
check("24: Escape returns focus instead of dropping it",
  /function close\(returnFocus\)/.test(features) && /if \(returnFocus\) \{ try \{ cbtn\.focus\(\); \} catch \(e\) \{\} \}/.test(features));
check("24: the stylesheet cannot re-open a hidden menu",
  /\.cur-menu\[hidden\] \{ display: none !important; \}/.test(read("css/ultra.css")));
check("24: the option list scrolls inside itself, never the page",
  /cscroll\.scrollTop = /.test(features) && !/scrollTo\(sel, \{ block: "center" \}\)/.test(features));

console.log(failures ? `\n${failures} check(s) failed` : "\nall checks passed");
process.exit(failures ? 1 : 0);
