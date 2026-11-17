# Country SEO — status report (17 Nov 2026)

Report only. Nothing in this file changes indexation; the numbers are read
from the repository on the stated date and from the gates that
`python3 tools/build-all.py check` runs.

## What exists

| Page set | Pages | Indexable | Held (noindex) | Listed in |
|---|---|---|---|---|
| `learn-hindi-from-<country>/` (learner country pages) | 196 | **54** | 142 | `sitemap-published.xml` (54 URLs) |
| `hindi-tutor/<place>/` (tutor location pages: 13 Indian cities + 24 countries/cities abroad + worldwide) | 38 | **38** | 0 | `sitemap-places.xml` (38 URLs + hub) |
| `world-languages/<country>/` (research pages) | 194 | 0 | 194 | — (quarantined on purpose) |

Indexable learner-country pages (54): afghanistan, armenia, azerbaijan,
bahrain, bangladesh, bhutan, brunei, cambodia, canada, ethiopia, georgia,
haiti, india, indonesia, iran, iraq, israel, jordan, kazakhstan, kosovo,
kuwait, kyrgyzstan, laos, lebanon, malaysia, maldives, moldova, myanmar,
nepal, new-zealand, oman, pakistan, palestine, peru, philippines, poland,
qatar, romania, saudi-arabia, singapore, south-africa, sri-lanka, syria,
tajikistan, thailand, timor-leste, turkiye, turkmenistan, uae, uk, usa,
uzbekistan, vietnam, yemen.

## Why only 54 of 196 are indexable

The 196 pages were generated from one template. Nine paragraphs came out
word-for-word identical on every page and some were factually wrong for most
countries (a daylight-saving sentence printed for countries that do not
change their clocks). Publishing all 196 would be thin, duplicated content —
the exact pattern AdSense's "low value content" review and Google's helpful
content system penalise, and it would drag the 54 good pages down with it.

So the rule in `tools/apply-country-specifics.py` is: a country page is
indexable only when `data/content/country-specifics.json` holds verified,
country-specific facts for it (time-zone/DST, currency, script relationship
to Devanagari, a country-specific opening, FAQ answers). 54 countries have
that data today; the other 142 pages stay reachable but `noindex` until
their entry is written. `tools/quarantine-country-funnels.py` keeps the
held pages out of the sitemaps, and `build-all.py check` fails if a published
page still carries template text (`country specifics --check`, passing at
54/54 on 17 Nov 2026) or if a tutor-location page lacks its specifics
(`tutor location specifics --check`, 38/38).

## Verified on 17 Nov 2026

* 1,031 indexable pages site-wide; 0 titles over 65 characters; 0 duplicate
  titles (after PR #55).
* `sitemap-index.xml` lists 15 sitemaps; `sitemap-countries.xml` is an
  intentionally empty urlset (held set).
* Live checks that are NOT done here (they need the owner's Google account):
  Search Console coverage, indexing status, impressions. See
  `reports/search-console-owner-checklist.md`.

## How to publish more country pages (owner decision, no code change needed)

1. Add the country to `data/content/country-specifics.json` with real facts
   (zone, DST yes/no, currency code, script note, one local opening, FAQ
   answers). One entry ≈ 15 minutes with a reliable source open.
2. Run `python3 tools/apply-country-specifics.py` then
   `python3 tools/quarantine-country-funnels.py` (both idempotent), then
   `python3 tools/build-all.py check`.
3. Highest-value next entries by Hindi-learner demand and diaspora size:
   australia, germany, netherlands, france, italy, spain, japan, south-korea,
   mauritius, fiji, trinidad-and-tobago, guyana, suriname, kenya, tanzania,
   nigeria, ireland, sweden, norway, denmark.

No ranking, traffic or indexing result is claimed in this report.
