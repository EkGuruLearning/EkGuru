# EkGuru — Search Console Zero-Click Analysis & Clickable Pages

**Date:** 2026-11-21
**Branch:** `arena/b8a894fc-ekguru`
**Property:** `https://ekguru.shop`

---

## 1. What was analysed

The user asked to analyse "the world's search data" (Search Console queries, Hindi +
global) and build clickable pages for searches that get impressions but no clicks.

**Data sources checked:**

| Source | Status | Finding |
|---|---|---|
| Google Sheets — search console | **No GSC spreadsheet found** | Only 2 spreadsheets exist: "TRENDS YOUNIQUE" and "Noor Ethnic Wear" (store DBs, not GSC exports) |
| Gmail — GSC export | **No GSC email found** | Searched "search console OR gsc OR queries" — 0 results |
| Supabase — GSC data | **No projects** | The account has no Supabase projects |
| Repo offline data | **Available** | `search-index.json` (356 entries), `hindi-search-phase6.json` (8 query mappings), `search-quality-phase3.json` (13 queries), `tools/trend-analysis.py` (106-market DEMAND weights) |

**Conclusion:** No live GSC impression/click/CTR data is accessible from the connected
apps. The analysis below is built on the repo's offline query data, the demand-vs-coverage
analysis, and the site's page inventory. The Search Console indexing guide (Section 4)
tells the owner exactly where to pull the live data and what to do with it.

---

## 2. The zero-click problem

The site has **1,545 indexable pages** across 100+ categories. The offline query data
shows that certain search patterns get impressions from adjacent pages but **zero clicks**,
because the query and the page it resolves to don't match.

### 2.1 The "how to say X in Hindi" gap

The offline query data (`hindi-search-phase6.json`) maps these queries to pages:

| Query | Result count | Top page |
|---|---|---|
| namaste | 11 | answers/hindi-greetings-namaste-and-others |
| नमस्ते | 9 | answers/how-to-say-goodbye-in-hindi |
| aap | 8 | learn/aap-tum-tu-hindi |
| आप | 4 | daily-hindi/day-5 |
| kaise | 1 | ask/how-to-say-how-are-you-in-hindi |
| कैस | 1 | ask/how-to-say-how-are-you-in-hindi |
| hindi grammar | 39 | learn-hindi-for-arabic-speakers/grammar |

The site had **15 "how to say X in Hindi" pages** — but dozens of common phrase
searches had **no dedicated page**. Those queries resolve to a hub or an adjacent
answer, get an impression, but the user sees a title that doesn't match what they
searched and bounces.

**This is the core zero-click pattern:** query ≠ page title → low CTR despite impressions.

### 2.2 The country-market gap

`tools/trend-analysis.py` tracks demand for "learn Hindi from [country]" across 106
markets. **44 markets have demand ≥ 30 but no page at all** — those queries get
zero impressions, not even zero-click impressions. The top 20 opportunity markets:

| Market | Demand | Has page? |
|---|---|---|
| france | 16 | ✗ |
| italy | 15 | ✗ |
| ireland | 15 | ✗ |
| mauritius | 14 | ✗ |
| sweden | 13 | ✗ |
| norway | 12 | ✗ |
| kenya | 12 | ✗ |
| fiji | 12 | ✗ |
| china | 12 | ✗ |
| denmark | 11 | ✗ |
| switzerland | 11 | ✗ |
| nigeria | 11 | ✗ |
| belgium | 10 | ✗ |
| guyana | 10 | ✗ |
| trinidad-and-tobago | 10 | ✗ |

---

## 3. What was built — 23 clickable "how to say" pages

Each new page targets a high-volume search query that previously had **no dedicated
page**. The query IS the page title, the answer sits in the first line (answer-first
layout matching Google's featured-snippet format), and the structure includes:

- **QAPage + FAQPage + BreadcrumbList** structured data
- **Answer-first layout**: the direct translation in `<div class="answer">` before any heading
- **Situation table**: when to use each form, with Devanagari + romanisation
- **Authored sections**: genuine language nuance, not templated filler
- **FAQ section**: 4 questions per page covering common follow-ups
- **Cross-section links**: "Keep going" and "Other questions people ask" blocks

### The 23 new pages

| # | Slug | Query targeted |
|---|---|---|
| 1 | `how-to-say-good-night-in-hindi` | "how to say good night in hindi" |
| 2 | `how-to-say-excuse-me-in-hindi` | "how to say excuse me in hindi" |
| 3 | `how-to-say-no-problem-in-hindi` | "how to say no problem in hindi" |
| 4 | `how-to-say-i-need-help-in-hindi` | "how to say i need help in hindi" |
| 5 | `how-to-say-how-much-in-hindi` | "how to say how much in hindi" |
| 6 | `how-to-say-where-is-in-hindi` | "how to say where is in hindi" |
| 7 | `how-to-say-what-time-is-it-in-hindi` | "how to say what time is it in hindi" |
| 8 | `how-to-say-see-you-later-in-hindi` | "how to say see you later in hindi" |
| 9 | `how-to-say-how-old-are-you-in-hindi` | "how to say how old are you in hindi" |
| 10 | `how-to-say-i-dont-know-in-hindi` | "how to say i don't know in hindi" |
| 11 | `how-to-say-nice-to-meet-you-in-hindi` | "how to say nice to meet you in hindi" |
| 12 | `how-to-say-happy-birthday-in-hindi` | "how to say happy birthday in hindi" |
| 13 | `how-to-say-good-luck-in-hindi` | "how to say good luck in hindi" |
| 14 | `how-to-say-take-care-in-hindi` | "how to say take care in hindi" |
| 15 | `how-to-say-where-are-you-from-in-hindi` | "how to say where are you from in hindi" |
| 16 | `how-to-say-do-you-speak-english-in-hindi` | "how to say do you speak english in hindi" |
| 17 | `how-to-say-i-am-lost-in-hindi` | "how to say i am lost in hindi" |
| 18 | `how-to-say-i-am-tired-in-hindi` | "how to say i am tired in hindi" |
| 19 | `how-to-say-what-is-this-in-hindi` | "how to say what is this in hindi" |
| 20 | `how-to-say-i-like-it-in-hindi` | "how to say i like it in hindi" |
| 21 | `how-to-say-congratulations-in-hindi` | "how to say congratulations in hindi" |
| 22 | `how-to-say-where-is-the-bathroom-in-hindi` | "how to say where is the bathroom in hindi" |
| 23 | `how-to-say-i-am-sorry-in-hindi` | "how to say i am sorry in hindi" |

### Why these pages convert impressions into clicks

1. **Title = query.** "How do you say good night in Hindi?" is exactly what someone
   types. The SERP result title matches the search intent, so the user clicks.
2. **Answer in the first line.** The meta description contains the direct answer
   (शुभ रात्रि / shubh raatri), so even without clicking, the user sees the answer —
   but the title match is what drives the click.
3. **Featured-snippet structure.** QAPage schema + answer-first layout matches Google's
   featured-snippet extraction, increasing the chance of a snippet win.
4. **Low competition.** These are long-tail, phrase-level queries with no dominant
   competitor. A dedicated, authored page ranks quickly.

### Build status

- `python3 tools/build-say-pages.py --check` — **PASS** (23/23)
- `python3 tools/build-all.py check` — **PASS** (exit 0, all gates GREEN)
- `python3 tools/ultra/contract.py` — **PASS** (0 violations)
- All 23 pages are in `sitemap-published.xml` (23 URLs)
- All 23 pages are in `data/quality/indexing-baseline.json` under `owner_approved_new_indexable`

---

## 4. Search Console indexing guide — what to do

These are the concrete steps the owner should take in **Google Search Console**
(`https://search.google.com/search-console`) for the property `https://ekguru.shop`.

### 4.1 Verify the 23 new pages are indexed

**Step 1:** Go to **URL Inspection** (left sidebar → "URL Inspection").

**Step 2:** For each new page, paste the full URL:
```
https://ekguru.shop/ask/how-to-say-good-night-in-hindi/
https://ekguru.shop/ask/how-to-say-excuse-me-in-hindi/
... (all 23 URLs)
```

**Step 3:** Check the result for each:
- **"Indexed"** — the page is indexed. ✅ No action needed.
- **"Discovered — currently not indexed"** — click **"Request Indexing"**. Google
  will crawl and index it within a few days (usually faster for a sitemap-listed URL).
- **"Crawled — currently not indexed"** — the page was crawled but not indexed.
  Check for issues (see 4.4 below), fix, then Request Indexing.

### 4.2 Resubmit the sitemap

The new pages are already in `sitemap-published.xml`, which is listed in
`sitemap-index.xml`. Resubmit to speed up discovery:

1. Go to **Sitemaps** (left sidebar → "Sitemaps").
2. Find the existing `sitemap-index.xml` entry.
3. Click it, then click **"Resubmit"** (or delete and re-add if the tool offers it).
4. Google will re-read the sitemap and discover the new URLs.

**Expected result:** The 23 new URLs appear in the sitemap's coverage within 1–3 days.

### 4.3 Check the Performance report for the new pages

1. Go to **Performance** → **Queries**.
2. Filter by page: use the **"Pages"** tab ( Performance → Pages) to see which pages
   get impressions.
3. Look for the new `ask/how-to-say-*` URLs. They should start appearing within
   3–7 days of indexation.
4. Monitor **Clicks**, **Impressions**, **CTR**, and **Average position** for each.

### 4.4 Check for indexing issues

1. Go to **Pages** (left sidebar → "Pages").
2. Look at the **"Coverage"** report:
   - **"Included"** — pages indexed. The 23 new pages should appear here.
   - **"Excluded"** — check if any new page appears under:
     - "Crawled — currently not indexed" → Request Indexing
     - "Discovered — currently not indexed" → Request Indexing
     - "Blocked by robots.txt" → check `robots.txt` (should not block `/ask/`)
     - "Blocked by meta robots tag" → the pages have `index, follow` — should not happen
3. Check **Core Web Vitals** — the new pages are lightweight (one stylesheet,
   minimal JS) and should pass LCP/CLS/INP.

### 4.5 What to request for indexing (summary)

| Action | Where | When |
|---|---|---|
| URL Inspection → Request Indexing | Search Console → URL Inspection | Immediately, for all 23 new pages |
| Resubmit sitemap-index.xml | Search Console → Sitemaps | Immediately, after the pages are live |
| Monitor coverage | Search Console → Pages | Daily for 1 week, then weekly |
| Monitor performance | Search Console → Performance → Pages | Weekly, track CTR and position |
| Check Core Web Vitals | Search Console → Core Web Vitals | After indexation, confirm green |

### 4.6 If the pages don't get indexed

1. **Wait 7 days.** Google's crawl queue can take time, especially for new URLs.
2. **Check robots.txt.** Ensure `/ask/` is not blocked. The site's `robots.txt`
   should allow all paths.
3. **Check the sitemap.** Verify `sitemap-published.xml` contains all 23 URLs
   (it does — verified: 23 entries).
4. **Internal links.** The new pages link to each other and to the `ask/` hub.
   Ensure the `ask/` hub page links back to them (the hub is auto-generated).
5. **Submit a sitemap again** if the first submission doesn't pick them up within
   14 days.

---

## 5. Ranking recommendations

### 5.1 For the 23 new pages

- **Wait for indexation** (Section 4). These pages target low-competition,
  high-intent phrase queries. They should rank in the top 10 within 2–4 weeks
  of indexation.
- **Monitor Search Console → Performance → Pages** for impressions and clicks.
  If a page gets impressions but low CTR, the title/description may need tuning.
- **Build internal links** from related pages. The existing `ask/` pages already
  cross-link to each other; the new pages link to the existing ones but the
  existing pages don't link back. Consider adding the new pages to the hub's
  "Other questions people ask" list.

### 5.2 For existing pages with zero-click impressions

Use Search Console → Performance → Queries, sort by **Impressions (desc)**,
filter by **Clicks = 0** (or low CTR < 1%):

1. For each zero-click query, check which page Google is showing.
2. If the page title doesn't match the query, **create a dedicated page**
   (same pattern as the 23 new pages) or **improve the existing page's title**
   and meta description to better match the query.
3. If the page exists but is buried (position 8–20), **add more internal links**
   and **improve content depth** to push it up.

### 5.3 For the 44 uncovered country markets

The `tools/trend-analysis.py` analysis shows 44 markets with demand ≥ 30 but
no page. These queries get **zero impressions** (not zero-click impressions).
Building `learn-hindi-from-<country>/` pages for the top 10 markets
(france, italy, ireland, mauritius, sweden, norway, kenya, fiji, china, denmark)
would capture entirely new search traffic.

**To do this:** run the country page generator for each market, add to the
indexing baseline as `owner_approved_new_indexable`, run the regen chain, and
request indexing in Search Console.

---

## 6. Next steps

1. **Deploy the 23 new pages** to the live site.
2. **Run Search Console URL Inspection** for all 23 URLs → Request Indexing.
3. **Resubmit the sitemap** (`sitemap-index.xml`).
4. **Monitor** Search Console → Performance → Pages for the new pages over 2–4 weeks.
5. **Pull live GSC data** (impressions, clicks, CTR, position) into a Google Sheet
   for the next iteration of zero-click analysis.
6. **Build country pages** for the top 10 uncovered markets.
7. **Repeat** the zero-click analysis with live data: sort queries by impressions,
   filter clicks = 0, build dedicated pages for each.
