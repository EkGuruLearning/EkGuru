# EkGuru demand vs coverage

Tracked markets: **106** · indexable: **53** · frozen by noindex: **51** · no page: **44**

**66.0%** of tracked demand has a page Google can rank. **32.7%** is written but frozen behind `noindex`.

## Starving — high demand, page exists, cannot rank

| market | demand | quality state |
| --- | --- | --- |
| australia | 58 | RESEARCH_REQUIRED |

## Opportunity — no page at all

france (16), italy (15), ireland (15), mauritius (14), sweden (13), norway (12), kenya (12), fiji (12), china (12), denmark (11), switzerland (11), nigeria (11), belgium (10), guyana (10), trinidad-and-tobago (10), austria (9), portugal (9), tanzania (9), south-korea (9), uganda (8)

## India — states with no page

25 states/UTs have no page. 11 city pages exist and serve 11 states; the rest are reachable through the nearest city page, which the hub now states explicitly.

## What to do today

1. Approve a `noindex → index` flip for the top 3 starving markets, then run `python3 tools/build-sitemaps.py` and resubmit `sitemap-index.xml`.
2. Add one city page for the largest uncovered state (see the hub note).
3. Check Search Console → Performance → Countries against the `live` list; a live market with zero impressions is a content problem, not a ranking one.
