# EkGuru design system (v200 — the experience layer)

**Status:** live on `/`, `/support/`, `/courses/`, `/search/` and the six
translated home pages. Every other page inherits the same look through the
bundled stylesheet and needs no markup change.

## The one idea

EkGuru ships one page per market. Before v200 all of them looked the same:
the same violet, the same shapes, the same motion — and a visitor on `/ar/`
read right-to-left text next to a left-to-right drawing.

The experience layer makes the interface speak the visitor's language:

| Layer | What changes per language | Where it lives |
|---|---|---|
| Palette | primary / secondary / accent per language family | `css/experience.css` §2 |
| Motif | one repeating geometry per family, drawn in CSS | §2, applied in §4 |
| Script | type scale, line-height and font stack per writing system | §3 |
| Motion | entrance accent per writing system | §22 |
| Artwork | a drawn emblem per market (`images/xp/world-*.svg`) | §21 + `tools/build-world-art.py` |
| Copy | every string, in seven languages | `js/i18n.js` |

## Rules that must not be broken

1. **Nothing hides without JavaScript.** `html.xp-anim` is added by
   `js/experience.js` only when it can actually reveal. No JS, or a broken
   script, and the page is complete and readable.
2. **Every animation is cancelled** by `@media (prefers-reduced-motion: reduce)`.
3. **Interactive targets stay ≥ 44px** on `@media (pointer: coarse)`.
4. **Logical properties only** (`inline-start`, `margin-inline`, …) so RTL
   needs no separate stylesheet.
5. **Generator-written class names are contractual** — `.m-card`,
   `.course-card`, `.egc`, `.tcard`, `.mkt`, `.reveal`, `.stagger`. Restyle
   them, never rename them.
6. **No price is ever typed into a string.** Use the `{minPrice}` token or a
   `data-usd` element; `js/pricing.js` fills it from the live rate table.

## Components

All of them live in `css/experience.css` and are plain classes — no build step
for a new page:

* **Shell** — `.xp-main`, `.xp-wrap`, `.xp-band`, `.xp-orb`, `.xp-sec(.soft)`,
  `.xp-head`, `.xp-kicker`, `.xp-rule`
* **Hero** — `.xp-hero`, `.xp-hero-copy`, `.xp-visual`, `.xp-ring`,
  `.xp-medallion`, `.xp-letters`/`.xp-letter`, `.xp-float`, `.hero-card`
* **Search** — `.xp-searchbox`, `.xp-searchbar`, `.xp-search-hint`, `.xp-kbd`
* **Rail** — `.xp-rail`, `.xp-rail-track`, `.xp-rail-item`
* **Cards** — `.xp-grid(-2/-3/-4)`, `.xp-card`, `.xp-card-ico`, `.xp-card-link`,
  `.xp-steps`/`.xp-step`, `.xp-quote`, `.xp-stat`, `.xp-cta`, `.xp-tutor*`
* **Artwork** — `.xp-world`, `.xp-world-hero`, `.xp-world-herochip`,
  `.xp-world-bleed`, `.xp-world-inline`
* **Motion hooks** — `.xp-rise`, `.xp-stagger`, `.reveal` (all opt-in via JS),
  `.xp-sheen`

## The header on a phone

The six translated pages carry their own header and deliberately do not load
`js/main.js` (it expects to run from the site root). Until v200 that left them
with no burger: at 390px four links and a pill-button wrapped into two ragged
rows and the booking button was clipped off the right edge.

Each of those headers now carries a `.burger`, and `js/experience.js` §11 wires
the drawer — the same panel the English pages get from `main.js`, from the same
shell stylesheet. The two can never fight: if `main.js` has already bound the
header it gives the nav an `id`, and §11 then returns without touching it.

Below 1200px the nav is a drawer on every page. Between 1201 and 1300px it is
at its tightest, so §20b trims the link gap by 4px rather than let the first
link slide under the logo.

Gate: `node tools/check-header-pages.mjs --url http://127.0.0.1:8080`
(puppeteer-core; `--ld-library-path` if the browser lives outside the loader
path) — 8 pages × 12 widths, no overlap, no viewport overflow, drawer opens
and closes with the right ARIA state.

## The artwork

```html
<img class="xp-world" data-xp-world="auto" src="../images/xp/world-es.svg"
     alt="" aria-hidden="true" width="430" height="430" decoding="async">
```

* `data-xp-world="auto"` — follow the interface language (home pages).
* `data-xp-world="ja"` / `"hi"` / `"multi"` — this page belongs to one world
  and keeps it (support/ is about Hindi lessons whoever is reading;
  courses/ and search/ span every language).
* The static `src` is always correct on its own, so a crawler and a no-JS
  visitor see the right emblem.

Emblems are drawn by `tools/build-world-art.py` from the palettes in
`css/experience.css` — the stylesheet is the source of truth, so the drawing
can never drift from the colours the page uses.

## Pages, and what writes them

| Page | Source | Tool |
|---|---|---|
| `/` | hand-written | — |
| `/support/` | hand-written | — |
| `/search/` | hand-written (`js/site-search.js` is the engine) | — |
| `/courses/` | catalogue in `data/courses/index.json` | `tools/build-course-hub.py` |
| `/es/ /fr/ /de/ /pt/ /ja/ /ar/` | `js/i18n.js` + `js/tutors/*` | `tools/build-market-pages.js` |
| `/search/` country + language lists | `search-index.json` | `js/site-search.js` §facets |
| `tutor/<id>/` + `sitemap-tutors.xml`, `sitemap.xml`, `feed.xml` | `js/tutors/<id>.js` + `_registry.js` | `tools/build-tutor-pages.js` |
| the tutor grid on `/`, and the six market grids | `js/tutors/*` | `tools/build-home-tutors.js` |
| the `<script>` tags that load the tutors | `js/tutors/_registry.js` | `tools/langsync.js` |
| `hindi-tutor/*`, `tutor/`, `*/find-tutors.html` | `js/tutors/*` | `tools/build-roster-rows.js` |
| the header and footer on **every** page | the settings tab (tagline, email, mode) | `tools/build-shell.js` |
| `/terms/ /privacy/ /disclaimer/ /copyright/` contents card + clause ids | the page's own headings | `tools/build-legal-pages.py` |

The market pages are generated because six hand-edited copies is exactly how
they drifted apart before. The generator rewrites **only `<main>`** — head,
header, footers and script tags are preserved byte for byte, so SEO work on
those pages can never be lost by a rebuild.

## One header, one footer, on every page

Every page — hand-written, generated, quiz, worksheet, country funnel, 404 —
carries the same `header.hdr` and `footer.ftr`, wrapped in
`ekguru:shell-header` / `ekguru:shell-footer` markers and written by
`tools/build-shell.js`. Before it existed there were three different taglines
in three different places and ~1,500 pages with no header at all.

- **The values come from the settings tab**, not from the markup: the tagline,
  the contact address and the "mode" line are read through
  `tools/lib/site-data.js` (which reads what `tools/sheetsync.js` wrote).
  Change the tagline in the spreadsheet, re-run the build, and every page and
  every printed footer follows — `js/site-shell.js` re-applies the same value
  at runtime when a live copy is on the page.
- **The market pages are translated, not English with a different `lang`.**
  The six locales take their labels from `js/i18n.js` — the same dictionary
  they already load — and keep their own three pages (home, find-tutors,
  join) as the targets of the nav.
- **One owner of the drawer.** The shell page carries `js/site-shell.js`, the
  hand-written pages carry `js/main.js`, and both want the same burger.
  `window.EKGURU_DRAWER` is the handshake: first one to bind claims it, the
  other stands down. Two handlers on one button is not cosmetic — one click
  opens the drawer and closes it again, which is the "3 lines open karte hi
  bug" report. `tools/test-shell-drawer.mjs` drives the real file in a DOM and
  fails if a click stops opening the menu.
- **The scroll lock is the v74 rule** in both files: remember `scrollY`, pin
  the body with `top:-<offset>px`, restore with `behavior:"auto"`. Anything
  else reads as the jump the lock exists to remove.
- `--check` fails if any page is out of date, and the write is idempotent by
  comparison (not by a "touched" flag), so a second run changes nothing.

## Country and language in search

`/search/` answers three questions that used to be one: what kind of page
(section pills, generated by `tools/build-search-index.py`), **which country**
(196 country funnels plus the city tutor pages) and **which language** (the
"for speakers" guides, the starter packs and the translated Hindi guides).
Both dropdowns are built at load from `search-index.json`, so a new funnel or
pack appears in them with no edit, and the three filters combine.

The language list exists because the site spells a language three ways — the
guide says `japanese`, the starter pack says `ja`, the market says `ja/hindi`.
They are merged into one English name learned from the index itself, so
"Japanese" appears once with all seven of its pages rather than twice with
half. `tools/test-search-facets.mjs` holds that line.

## The document pages (legal, and the long tail)

Terms, privacy, disclaimer and copyright arrive with one question and no
patience for a wall of prose, so `tools/build-legal-pages.py` gives every
clause an `id`, builds the **On this page** contents card from those headings
and marks the block `.xp-doc`. It never touches a word: the tool compares the
prose before and after and refuses to write if they differ, because legal
wording is the last thing a build script should rewrite to suit a stylesheet.

The 974 older pages (country funnels, answers, lessons, worksheets) still carry
their own 2024 markup and their own inline `<style>`, which loads *after*
`style.min.css` and therefore wins. They keep their layout deliberately — the
design system reaches them through `css/experience.css` §23 instead, with the
two properties those pages never set: an anchor that lands below the sticky
header (`scroll-margin-top`) and the redesigned focus ring.

## Build / check loop

```bash
python3 tools/build-all.py check            # every generator's --check + the DOM test
```

That one command is the gate. It runs, in order:

```bash
python3 tools/bundle-experience-css.py --check   # css/experience.css → css/style.min.css
python3 tools/build-world-art.py   --check       # the nine market emblems
python3 tools/build-course-hub.py  --check       # /courses/ + the home teaser
node    tools/langsync.js          --check       # tutor <script> tags, all 23 pages
node    tools/build-tutor-pages.js --check       # profiles + sitemaps + feed
node    tools/build-home-tutors.js --check       # the home page's tutor grid
node    tools/build-market-pages.js --check      # the six market home pages
node    tools/build-roster-rows.js --check       # 44 more pages that list tutors
node    tools/test-experience-dom.mjs            # DOM smoke test (needs: npm i jsdom)
node    tools/test-search-facets.mjs             # country + language dropdowns
node    tools/test-shell-drawer.mjs              # one owner of the menu button
node    tools/test-copy-index.mjs                # the ownership matcher
node    tools/build-shell.js            --check  # header + footer on 1,563 pages
node    tools/build-copy-index.js       --check  # ownership fingerprints
python3 tools/build-legal-pages.py      --check  # legal contents cards
```

Without `check` the same chain writes instead of comparing — `python3
tools/build-all.py` runs it as the last phase of the full rebuild (phase 12),
after the injectors, so nothing can overwrite a generated block. `node
tools/gate.js` runs the five tutor generators a second time as the
`tutor-roster` check, so a deploy where one page still lists four tutors fails.

`css/style.min.css` carries the whole layer, so the ~1,500 pages that only link
the stylesheet — country funnels, lessons, tools, guides — re-tint and
re-motif with no HTML edit at all. **Always re-run the bundler after editing
`css/experience.css`**; `--check` exits 1 when the bundle is stale.

## Adding a language

1. Add the locale to `EKGURU_MARKETS` in `js/site-config.js`.
2. Copy a block in `js/i18n.js` and translate the values.
3. Add a palette block in `css/experience.css` §2 (`--xp-a/b/c`, `--xp-motif`,
   `--world-*`) and, if the writing system is not Latin, its rhythm in §3.
4. `python3 tools/build-world-art.py` (add the code to `LANG_SELECTOR`).
5. `python3 tools/bundle-experience-css.py`.

`js/experience.js` picks the rest up from `html[lang]` — palette, motif,
script rhythm, motion accent and page copy.
