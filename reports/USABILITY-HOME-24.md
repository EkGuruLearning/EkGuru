# Home page usability pass — 24 findings, root cause and fix

Page audited: `https://ekguru.shop/index.html` (served by `index.html`, generator-owned
regions only where a marker exists).
Branch: `arena/01a102f8-ekguru`.
Rules followed: generated pages are edited through their generator (R-5), Googlebot and a
human see the same content (R-1), noindex / canonical / domain untouched (R-7), runtime ad
flags stay OFF, WCAG 2.2 AA (R-9), every phase ships its own test.

New files: `tools/build-home-markets.py` (the server-rendered country grid),
`tools/test-usability-home.mjs` (the regression test for 1–24).

---

## 1–3 — 92 type sizes, 47 text colours, 29 corner values with no system

**Root cause.** The home page's two style layers (`<style id="critical">` in the document and
the home-owned rules of `css/experience.css`) had grown organically: 92 distinct `font-size`
values, 47 `color` values and 29 `border-radius` values, 8 of them one-off `clamp()` scales.
No file could answer "what is the type scale?", so every new block invented another value.

**Fix.** One declared scale, in both layers (`css/experience.css :root` and the `#critical`
`:root`): ten type steps `--xp-fs-3xs … --xp-fs-4xl` (.68 → 3.4 rem), four fluid steps
`--xp-fs-fluid-lg … -3xl` (folded in from the eight clamps), five radii + `--xp-pill` +
`--xp-circle` + the organic `--xp-blob`, and three text colours `--xp-ink`, `--xp-ink-2`,
`--xp-muted` that follow the theme (`var(--ink, …)`), plus `--xp-ink-on-brand` and
`--xp-accent-ink`. Every declaration in those layers now uses a token. The four fluid steps and
the two brand colours were **missing** from both layers after the first pass — the new regression
test caught it before it shipped (a `var()` to an undefined token resolves to `inherit`).

**Result.** 92 → 13 distinct type sizes, 47 → 13 colours, 29 → 11 corner values in the home
layers; the survivors are structural (`0`, `inherit`, `transparent`) or decorative
(`color-mix()` gradient stops).
**Verified by** `tools/test-usability-home.mjs` checks 1–3 (tokens declared in both layers; no
literal type size or corner value left in a home rule).

## 4 — a 26-character sentence inside a badge styled for 2-word labels

**Root cause.** `.xp-kicker` is an eyebrow label: uppercase, .12em letter-spacing. "100% Hindi ·
1-on-1 Online" was rendered with it, so a sentence was shouted in capitals and letter-spaced,
and the marketplace-style capital "Online" was wrong English.

**Fix.** A `.xp-kicker--badge` variant (no uppercase, .02em tracking, one size down) is applied
to the hero badge in `index.html` and in `tools/build-market-pages.js` for the locale homes; the
copy is sentence case in the HTML and in `js/i18n.js` (`hero.badge`).
**Verified by** check 4.

## 5 — the document outline jumped H1 → H3

**Root cause.** `js/visual-learning.js` injected `🌍 {country} Cultural Context` as an `<h3>`
immediately **after the `<h1>`**, so on the home page a level-3 heading sat between the headline
and the search box, and the outline read H1, H3, H2…

**Fix.** The block is a sibling section of the first `<h2>` of the article and carries an `<h2>`;
it is skipped entirely on a page with no `<h2>` to attach to. `js/visual-learning.js`.
**Verified by** check 5.

## 6 — the country "wall": ~100 unlabelled chips, no grouping, no links

**Root cause.** `js/country-marquee.js` replaced the section body with two continuous marquees of
`<button>` chips — 32 countries in data order, no regions, and no followable link, because chips
are not links. A crawler saw nothing at all.

**Fix.** The section is now server-rendered: 52 country links in 7 named regions
(`tools/build-home-markets.py`, markers `ekguru:home-markets`), each link going to that country's
page, each carrying its verified-language count. The chips become an enhancement *behind* that
grid. `js/country-marquee.js` keeps the static grid when it is present.
**Verified by** checks 6 and 12.

## 7 — the landing page's biggest graphic announced an absence (Critical)

**Root cause.** With no public tutor (U0 state) the hero card printed "No tutors are available
for booking right now." as its headline — the first feature-sized text a visitor read.

**Fix.** The card states the same truth in the order a visitor needs it: what is open first
("Free lessons, practice and courses are always open."), the booking status second, then the
free-course button. Generator `tools/build-home-tutors.js` and the JS repaint
`js/main.js renderHome()` produce identical markup.
**Verified by** check 7+22.

## 8 — a greeting floating between the badge and the H1

**Root cause.** `js/greeting.js` injects `.ekg-greeting-line` into the hero copy column, and
`css/experience.css` animates **every** `.xp-hero-copy > *` child, so the greeting appeared as a
third, differently-spaced row between the badge and the headline.

**Fix.** The pre-header is one bounded, left-aligned block: `.xp-hero-copy > .xp-kicker`,
`> .ekg-greeting-line` and `> h1` have explicit margins, and the RTL variant keeps the same
inline-start edge.
**Verified by** check 8.

## 9 — the section contradicted itself in one screen (Critical)

**Root cause.** Above the tutor grid, a filled "See all tutors + filters" button; below it,
"No tutors are available for booking right now." The page offered a door it had just said was
closed.

**Fix.** The button is generated from the roster (new marker pair
`ekguru:home-tutors-cta`, `tools/build-home-tutors.js`): with tutors it is the primary
"See all tutors + filters", with none it is a ghost "Browse the free courses →". `js/main.js
tutorsCtaHTML()` keeps a live repaint in step.
**Verified by** check 9.

## 10 — course cards with two different schemas

**Root cause.** `tools/build-course-hub.py` printed a country-chip row when the language had
country attributions and a single `<em>documented</em>` chip when it did not — so Spanish,
French, Japanese and Chinese advertised the word "documented" next to "complete A1–C2",
and the reader learned nothing.

**Fix.** One schema: chips only when there is something to name (four names + "+N more"),
no chip line at all otherwise. The level line above already carries the facts.
**Verified by** check 10.

## 11 — the empty state was a filled button plus a dotted link sentence

**Root cause.** `tools/lib/zero-state.js` and `js/main.js emptyTutorsHTML()` emitted
`<p class="t-empty-links">` with `·`-separated inline links that wrapped onto a second line,
while the stylesheet styled a `.t-empty-actions` row that no longer existed.

**Fix.** Both emitters (static + live) write `.t-empty-actions`: the primary course button, then
Learn / Courses / Daily Hindi as sibling ghost buttons in one wrapping row; the CSS owns the row.
**Verified by** check 11.

## 12 — the grid that only existed after JavaScript ran

**Root cause.** Same as 6: the only server-side content in the country section was a one-line
`<noscript>` fallback.

**Fix.** The grid is real HTML (52 links, 7 regions, inside `#markets`), the interactive rails sit
behind a labelled `<details>`, and the `<noscript>` line is gone because it is no longer needed.
**Verified by** checks 6, 12, 14.

## 13 — ~160 px of dead space between the markets section and the FAQ

**Root cause.** The markets section ended with its own `.xp-rule` margin and the FAQ section
opened with full `.xp-sec` padding, so two section paddings stacked into one visible gap.

**Fix.** `#markets-sec.xp-sec` and `#faq.xp-sec` own the seam (`padding-block` tightened in
`css/experience.css`), so the two blocks read as one group.
**Verified by** check 13.

## 14 — one orphan button explained the whole country section

**Root cause.** The only real link in the section was a bare "Country language research →" button
under the chip wall, with no heading and no sentence saying where it goes.

**Fix.** It is a closing block with an `<h3>`, a sentence and a button (`.xp-more`).
**Verified by** check 14.

## 15 — Appearance and Currency were two controls in two places

**Root cause.** The theme switch lived in a generated panel above the footer
(`tools/apply-ultra.py appearance_block`), the currency switch in the dark footer
(`js/features.js initCurrencySwitch`). One idea — "how the site works for me" — two locations,
two control styles.

**Fix.** The currency select is built into the Appearance panel: `settingsRow()` moves the
generated label into a `.eg-settings-row`, appends the currency select to it, and moves the two
policy links onto their own line; the footer remains the fallback for a page with no panel. Done
in JS on purpose: the panel exists on 2 687 pages and the control has always been JavaScript-only,
so this avoids rebuilding the whole site for one row.
**Verified by** check 15.

## 16 — the bottom nav cards did not look clickable

**Root cause.** `.eg-gn-list a` cards had a border and a hover colour change only; nothing in the
card said "this opens".

**Fix.** Every card carries a visible signifier (`b::after` " →") and lifts on hover/focus, with
`prefers-reduced-motion` honoured.
**Verified by** check 16.

## 17 — three different global navigations, and two of them duplicated an idea

**Root cause.** No generator owned the block: its header comment credited `tools/hublinks.js`, a
file that does not exist in this repository. Four phases had each appended their own card, so the
13 pages that carry the block shipped 10, 11 or 12 cards; the home page offered both "The free
guides" and "Learn languages", and `ask`, `answers` and `faq` all read as the same FAQ door.

**Fix.** `tools/build-phase7-pages.py` now owns the block end to end (`GLOBAL_NAV`,
`global_nav_html()`, `one_global_nav()`): one 13-card list, in one order, on all 13 pages, with
distinct labels (Ask a question · Short factual answers · Hindi learning FAQ · The free guides ·
Learn languages), and the stale generator note replaced.
**Verified by** check 17.

## 18 — the journal strip was an orphan link

**Root cause.** `hub_blocks()` emitted one sentence-link ("Learning journal and continue links on
this device") in the middle of the page, with no heading and no explanation of what is stored
where; on a first visit (no saved progress) that was all a reader saw.

**Fix.** A labelled panel: heading "Your learning journal", one sentence (saved in this browser
only, nothing uploaded, no account), and a real button to `/learn/progress/`. `js/retention.js`
still replaces the body with "Continue where you left off" once the device has progress.
**Verified by** check 18.

## 19 — three competing hero calls to action

**Root cause.** The hero carried "Find My Guru", "Free published courses" and the search bar's
"Find a tutor" — three buttons of equal weight, in two different vocabularies.

**Fix.** The search bar is the hero's one primary action; the block below it is a single ghost
door ("Free published courses").
**Verified by** check 19.

## 20 — "Find My Guru" vs "Find a tutor"

**Root cause.** Two names for the same destination (the tutor directory), one of them a
marketplace-ism that the rest of the site never uses.

**Fix.** The hero no longer renders "Find My Guru" (the i18n key and the tutors page keep their
own copy); the hero's tutor door is the search bar, which says "Find a tutor".
**Verified by** check 20.

## 21 — the language rail repeated the language section, more vaguely

**Root cause.** The rail under the hero listed 15 languages labelled "course" (or nothing), while
the published-packs section two screens down listed the same languages with their real state
("complete A1–C2", "A1 · A2 · B1 · B2 available"). Two answers to the same question, and the
first one was the less accurate.

**Fix.** The rail shows the same level bands as the section (in `index.html` and in the locale
rail table of `tools/build-market-pages.js`), and its label says what it is: a jump list.
**Verified by** check 21.

## 22 — a null hero visual (Critical)

**Root cause.** Same component as 7: on a page whose purpose is to find a tutor, the tutor card
showed a null state rather than the alternative that is actually open, so the hero's visual
answer to "what do I do here?" was "nothing".

**Fix.** The card leads with the free course (name line, sentence, primary button) and keeps the
honest booking sentence underneath — a filled, actionable card in both states.
**Verified by** check 7+22.

## 23 — a third primary call to action at the bottom

**Root cause.** The closing block offered "Browse tutors" (primary), "Email us" and
"Try a free course" (ghosts) — the fifth link to `/courses/` on one page, and a third
button-weight decision for the reader.

**Fix.** Two doors, one of them primary: "Browse tutors" and "Email us".
**Verified by** check 23.

## 24 — the currency listbox could paint over the page (Critical)

**Root cause.** `js/features.js` built the full listbox (≈60 `role="option"` buttons) in every
page and hid it with an `opacity:0; visibility:hidden` rule; a geometry-based audit reads that as
a 330 px column of currency rows sitting over the right-hand content, and any stylesheet failure
*shows* it. `scrollTo(sel, {block:"center"})` scrolled the document, not the menu, and Escape
closed the menu without syncing `aria-expanded` or returning focus.

**Fix.** The listbox ships `hidden` and empty; it is filled on first open (`fill()`), closed
state is `display:none !important` (`.cur-menu[hidden]`), the chosen row is scrolled inside
`.cur-menu-scroll` (`scrollTop`, never the page), `.cur-menu-scroll:empty` removes the stray bar,
and `close(returnFocus)` keeps `aria-expanded` true to the DOM and puts focus back on the button
when Escape closed it.
**Verified by** check 24.

---

## Gates run on this branch

| Gate | Result |
| --- | --- |
| `node tools/test-usability-home.mjs` | all checks passed (new) |
| `node tools/test-experience-dom.mjs` | all checks passed |
| `node tools/test-runtime-qa.mjs` | 142 passed, 0 failed |
| `node tools/test-browser-qa.mjs` | 26 passed, 0 failed |
| `node tools/test-theme-contrast.mjs` | 90 themes × 3 modes, 4 320 pairs, 0 problems |
| `node tools/test-course-levels.mjs` | 29 passed, 0 failed |
| `node tools/test-course-placeholders.mjs` | 7 passed, 0 failed |
| `node tools/test-ad-policy.mjs` | 22 passed, 0 failed |
| `node tools/test-voice.mjs` / `test-retention.mjs` / `test-learning-storage.mjs` / `test-learning-worker.mjs` | 26/26, 20/20, 10/10, 13/13 |
| `python3 tools/apply-ultra.py --check` | 0 pages stale |
| `python3 tools/test-ultra-integration.py` | 2 687 pages, 0 problems |
| `python3 tools/bundle-experience-css.py --check` | bundle current |
| `python3 tools/inject-ads.py --check` | 2 689 pages match the ad matrix (ads unchanged, runtime flags OFF) |
| `python3 tools/test-phase3-content.py` | PASS |
| `python3 tools/build-full-page-inventory.py` | 2 690 pages · 1 006 indexable · thin_indexable 0 · broken 0 |
| `python3 tools/audit-adsense-readiness.py` | 2 687 pages · 504 ad pages · 0 thin home |
| `node tools/build-home-tutors.js --check`, `python3 tools/build-course-hub.py --check`, `python3 tools/build-home-markets.py --check`, `node tools/build-shell.js --check` | current |
| `node tools/build-market-pages.js --check` | current (checked with ultra decoration stripped, as `build-all` does) |

Not runnable in this sandbox, unchanged by this pass: `tools/build-all.py` (its first step,
`tools/sheetsync.js`, needs the live Google Sheet), `tools/test-phase7c-stage6.py` (needs
Playwright + a browser download), and any real-Chromium overflow measurement. They run in CI.
