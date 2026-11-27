# Search visibility: verified priorities, not a ranking guarantee

Audit date: 2026-11-24. Scope: current working tree and local server, not production or a Google account. The Hindi expansion and discovery fixes are on the active working branch; a branch push is not a live deployment. Earlier deployed technical fixes are documented separately in `docs/global-discovery-qa.md`.

## Findings against the proposed checklist

| Checklist topic | Repository evidence | Action |
|---|---|---|
| Missing sitemap / robots blocking public lessons | `robots.txt` advertises `https://ekguru.shop/sitemap-index.xml`. Generic and named Googlebot groups allow public content, excluding admin/build tools/search UI. Sitemap gate passes: 1,561 memberships, zero invalid entries. | Do not replace robots or resubmit through an invented account. Verify the sitemap's submitted/success status in the owner's Search Console. |
| Wrong canonicals / missing sitemap destinations | The current inventory has 1,561 **self-canonical indexable** pages. All pass the sitemap gate. Another 197 pages without a noindex directive point elsewhere canonically: 196 consolidated country phrase routes plus `/hindi/`, the topic-map alias. | Do not misreport those 197 deliberate aliases as missing indexable landing pages. Retain consolidation and canonical decisions. |
| Duplicate/missing metadata | Among those 1,561 self-canonical indexable pages: zero missing titles/descriptions, zero duplicate titles/descriptions, and every page has exactly one H1. One H1 text is shared by two Punjabi name pages; their titles and canonicals differ. | No evidence for blanket title rewriting. The overlapping Punjabi intent can receive a separate content review; shared H1 wording alone is not evidence of a Google penalty. |
| Broken internal discovery | `tools/discovery_integrity.py`: 3,016 public HTML files, 249,459 internal references, zero errors. Homepage already links to the Hindi hub, tutor directory and Daily Hindi. Hindi hub already links to the beginner, alphabet, speaking and grammar paths. | Preserve working navigation. Previous turns also added the new reading collection link from the Hindi hub and sentence lesson. Global navigation inlinks are not proof that contextual lesson links are sufficient or that Google has crawled them. |
| Practice-page metadata no longer described its content | Practice hub still advertised only typing, quiz and worksheets after the reading collection was added. | **Fixed in source generator and existing HTML**: title, H1, first paragraph and search/social descriptions now reflect words, sentences and paragraph reading while retaining the legacy tools. URL, canonical and robots unchanged. |
| New material expected to rank automatically | `/learn/hindi/foundation/swar/` is still intentionally `noindex, follow`, even with 3,293 added explanatory words. `/learn/hindi-speaking-practice-alone/` is also noindex. | These pages are not organic-search landing-page candidates under their current directives. Obtain editorial review and explicit selective publication approval before changing these decisions. Do not remove all noindex directives or treat added word count as approval. |

The 1,758 `indexable=true` count in the broad inventory means “no noindex directive”; it includes canonicalised aliases. It must not be presented as 1,758 independent eligible landing pages or as Google's indexed total. A passing repository check is not a production HTTP, Search Console or indexing result.

## Map search intent to existing pages first

Avoid creating another page for each phrase when an appropriate existing page already exists. No search-volume, ranking, competition or conversion evidence is asserted by this map.

| Search intent | Existing primary candidate | Current directive / next step |
|---|---|---|
| Learn Hindi online for beginners | `/learn/hindi/`, with `/learn/hindi/beginner/` as the beginner path | Both indexable/self-canonical; homepage already links to main hub. Distinguish broad navigation from beginner instruction. |
| How to learn Hindi online | `/learn/learn-hindi-online-guide/` | Indexable/self-canonical; review its 2026-specific advice when updating substance, not just the year. |
| Hindi alphabet / Devanagari practice | `/learn/hindi-alphabet-for-beginners/`, supported by `/toolbox/hindi-alphabet/` | Both indexable/self-canonical; keep explanatory guide and interactive-tool roles distinct. |
| Hindi speaking practice for beginners | `/learn/hindi/conversation/` | Indexable/self-canonical. The separate solo-speaking guide is noindex; do not silently publish or clone it. |
| Hindi grammar basics | `/hindi/grammar/`, supported by `/learn/paths/grammar-foundations/` and specific topic lessons | Indexable/self-canonical grammar landing page; strengthen explanation and worked examples rather than making another generic doorway. |
| Daily Hindi sentences with meaning | `/daily-hindi/` and its existing daily lessons | Indexable/self-canonical course. Hub is already linked from homepage. Assess individual lesson usefulness before requesting indexing of any held material. |
| Hindi words, sentences and reading practice | `/learn/hindi/practice/` | Indexable/self-canonical, existing URL; newly aligned metadata and introduction in this working tree. |

## Follow-up fix: contextual paths to phrase answers

A deeper incoming-link audit (distinct source pages with static anchors, not merely checking whether existing hrefs resolve) found **38 self-canonical indexable phrase answers with zero internal inlinks**. This does not contradict the earlier zero-broken-links result: a page can have no broken outgoing links and still have no incoming path.

Implemented on the existing `/ask/` hub: **39 existing phrase answers in five situation groups**, using each target's actual H1 as its link text. The 39th target already had an incoming link. The existing conversation landing page now links to this directory and three relevant practical answers, with a route into the existing rule-based practice tool. No new answer page, translated content, profile claim, script, storage or indexing decision was introduced.

- Source/regeneration: `tools/build-hindi-phrase-discovery.py` (`--check` is read-only), registered in the master build. The original Hindi topic renderer retains the conversation entry when regenerated.
- Regression: `tests/regression/test-hindi-phrase-discovery.py`, **5 tests PASS**: exact coverage of the 39 existing phrase-source entries, unique grouping, static incoming anchors, preserved metadata/schema, valid files/fragments, and legacy topic-renderer retention.
- Inventory after fix: **zero orphan phrase-answer targets**. Self-canonical indexable pages with no static inlinks fall **46 → 8**. The broader noindex-directive-only orphan count falls **242 → 204**, because it also includes the 196 intentionally canonicalised country aliases; that broader count is not 204 eligible orphan landing pages.
- At the phrase-fix checkpoint, eight self-canonical indexable orphans remained: `/hindi-classes/`, `/hindi-tutor-near-me/`, and the Amharic/Arabic/Greek/Japanese/Korean/Russian name pages. The follow-up below adds their contextual entry points; this checkpoint is retained to explain the counts.
- Discovery validation: **3,016 HTML files, 249,506 internal references, zero errors**. Sitemap gate still passes **1,561 memberships, zero invalid**, with no sitemap or robots changes.
- Chromium 158.0.8127.0: **320/390/1280px**, five groups/39 links, keyboard navigation from conversation to directory and an existing answer, no page exceptions or document overflow. JavaScript disabled: all 39 links visible. External requests blocked; local static server only. Inspected the 390px directory screenshot.
- Full `python3 tools/build-all.py check`: **PASS** after the fix and regenerated inventories. Excluded evidence: `.cache/phrase-discovery-build-check.log`, `.cache/phrase-discovery-qa/`, `.cache/hindi-pilot-qa/phrase-discovery-browser.cjs`.

These are working-tree fixes, not a live deployment, native editorial review or evidence of Google's indexing/ranking response.

## Follow-up: remaining eight contextual entry points

With the owner's instruction to continue fixes and push the working branch:

- The existing tutor directory now links contextually to `/hindi-classes/` and `/hindi-tutor-near-me/`. Wording explicitly describes online routes, not fabricated local centres, verified tutors or guaranteed availability. No booking form, pricing or tutor profile is changed.
- The existing Hindi-name tool now links to the six existing Amharic/Arabic/Greek/Japanese/Korean/Russian script guides. Wording explains spelling limitations and name-owner preference; no generated spelling is claimed official.
- Regeneration: `tools/build-contextual-entry-links.py`, bounded to two existing source pages/eight existing destinations, with read-only `--check`, registered in the master build.
- `tests/regression/test-contextual-entry-links.py`: **4 tests PASS**, covering bounded destinations, static/no-JS anchors, idempotence, unchanged title/H1/meta/canonical/schema and unchanged forms/code outside the insertion, plus recorded incoming paths in the regenerated inventory.
- Inventory now reports **0 self-canonical indexable pages with zero static inlinks**, down from 46 before the combined phrase/contextual fixes. The broad inventory still reports 196 no-noindex orphan aliases: the intentionally consolidated country phrase routes. Held/noindex pages are not counted as eligible landing pages and were not mass-published.
- Chromium 158.0.8127.0, local server: **320/390/1280px**, eight visible links, keyboard navigation to existing class/name destinations, no page exceptions or horizontal overflow. JavaScript disabled: all eight links visible. No forms submitted; external requests blocked. Excluded evidence: `.cache/contextual-entry-qa/` and `.cache/hindi-pilot-qa/contextual-entry-browser.cjs`.
- Full `python3 tools/build-all.py check`: **PASS** after these eight entry links and regenerated inventories. Excluded log: `.cache/contextual-entry-build-check.log`.
- This proves a static incoming path, not optimal crawl depth, contextual quality on every lesson, a production deployment or Google indexing/ranking.

## Prioritised next work

### P0 — collect Google-side evidence before diagnosing a Google-side cause

From the owner, request redacted screenshots or exports (no passwords/tokens):

1. **Search Console → Indexing → Pages**: counts and exclusion reasons with sample URLs. Not indexed is not automatically an error; redirects, alternate canonicals and intentionally noindex pages can be expected.
2. **Indexing → Sitemaps**: submitted sitemap URL, status and last-read information for `https://ekguru.shop/sitemap-index.xml`.
3. **URL Inspection** for the homepage, `/learn/hindi/`, and one important underperforming indexable lesson: crawl result, indexing status, user-declared versus Google-selected canonical, last crawl and any blocking reason.
4. For international targeting, **Performance → Search results**, a stated date range such as the last 28 days, split by queries/pages/countries. Do not infer country traffic from browser-language tests.

The `site:ekguru.shop` result estimate is not a dependable indexing census and is not required to proceed. Sitemap submission does not guarantee indexing. No Search Console account, submission or screenshots were accessed in this pass.

### P1 — validate production after an authorised release

Run the existing HTTP discovery gate against production where network access is available, checking status codes, final redirects, canonicals, robots meta and response headers. This sandbox's outbound access is restricted; no production crawl was attempted here. Existing local/browser checks cannot establish live host behaviour, CDN rules, Google's fetch results or live deployment of pending changes.

### P2 — editorial depth and selective publication

Continue the approved existing-page expansion in useful batches. The first Foundation batch has **1 of 10** chapters expanded; it is not 1,000 completed pages. Native-speaker review is pending. There is no universal SEO word-count minimum and no requirement that titles fit exactly 50–60 characters; clarity, distinct intent and accurate descriptions matter more than padding to an arbitrary count. Keep real examples, answer explanations and relevant next steps, not repeated keywords.

### P3 — trust and relevant outreach

Tutor qualifications, locations, teaching experience and reviews must come from verified tutor/owner records. Do not invent them to fill a schema. Add FAQs only when the answers are real, useful and visible; FAQ markup does not guarantee a Google rich result. No tutor profile was changed in this pass.

Relevant community participation and outreach can follow, but no directory submissions, guest posts, emails, paid backlinks or link packs were sent or purchased. Those actions require specific destinations, truthful material and separate owner direction. No worldwide ranking, traffic or AI-recommendation guarantee is made.

## Validation for the scoped practice fix

- Regression added to `tests/regression/test-hindi-learning-library.mjs`: title, single H1, natural first paragraph, matching descriptions/social title, self-canonical and retained indexability.
- `node tests/regression/test-hindi-learning-library.mjs`: **16 checks PASS**, including the new metadata/introduction contract and existing practice/voice/review behavior.
- `node tests/regression/test-seo-runtime.mjs`: **84 international runtime cases PASS**, plus static metadata/noindex guards.
- Real legacy `practice_hub()` regeneration verified semantic title/description and retained collection, with the decorated working page restored in `finally`. The generator can serialize an ampersand differently; metadata is compared as parsed text, not HTML entity bytes.
- Local HTTP discovery gate: **PASS, 1,561 sitemap URLs, 29 HTML samples, 54 probes**. Excluded evidence: `.cache/seo-checklist-http.json`. This was localhost, not production.
- Chromium 158.0.8127.0: updated practice title, canonical and retained indexability checked at 390/768/1280/1440px after runtime scripts, alongside existing keyboard/reading/no-JS/offline regressions. No local HTTP/page errors or document overflow in the tested cases. Device voice was simulated; no real pronunciation claim.
- `python3 tools/build-all.py check`: **PASS** after the fix and regenerated metadata/ownership/content inventories. Excluded log: `.cache/seo-checklist-build-check.log`.
- Generated report data is a local structural audit, not editorial approval.
