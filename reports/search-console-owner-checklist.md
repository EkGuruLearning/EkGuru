# Google Search Console — Owner Checklist

Only you (the site owner) can perform these; they require your Google account.
Nothing here can be verified from this environment — do NOT mark them done until you see them in your own console.

1. **Verify property** — Search Console → Add property → `https://ekguru.shop` (domain property, DNS TXT) or URL-prefix. The file `googleb3b0e3defc1daa17.html` exists at the site root for URL-prefix verification.
2. **Submit sitemaps** — after pushing the Phase 2/3 build, submit:
   - `https://ekguru.shop/sitemap-index.xml` (and confirm it now lists **14** sitemap files including `sitemap-materials.xml`).
3. **Inspect key URLs** — run URL Inspection on `/`, `/learn/`, `/materials/`, `/faq/`, `/toolbox/`, `/learn/practice/`, one tutor page, and request indexing where "URL is not on Google".
4. **Check coverage** — Pages report → look for any "Crawled – currently not indexed" on real content pages (not on `search/` or `admin.html`, which are intentionally noindex/gated).
5. **Sitemap status** — confirm every submitted sitemap reports "Success" and that indexed counts grow (indexing is Google's decision and can take days/weeks — never claim it has happened until it appears here).
6. **Manual actions / security** — confirm zero manual actions and zero security issues.
7. **Core Web Vitals** — check the real-field LCP/INP/CLS once traffic exists.

Do not claim indexing, ranking, or traffic from anything except these console screens.
