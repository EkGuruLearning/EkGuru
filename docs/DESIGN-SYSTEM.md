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

The market pages are generated because six hand-edited copies is exactly how
they drifted apart before. The generator rewrites **only `<main>`** — head,
header, footers and script tags are preserved byte for byte, so SEO work on
those pages can never be lost by a rebuild.

## Build / check loop

```bash
python3 tools/build-world-art.py            # redraw the emblems (--check in CI)
python3 tools/build-course-hub.py           # /courses/ + the home teaser (--check)
python3 tools/bundle-experience-css.py      # css/experience.css → css/style.min.css (--check)
node    tools/build-market-pages.js         # the six market home pages (--check)
node    tools/test-experience-dom.mjs       # DOM smoke test (needs: npm i jsdom)
```

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
