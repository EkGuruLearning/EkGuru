# Re-submitting EkGuru to AdSense — what to send, and what to say

Written 18 September 2026, after the review of 14 September. This is the packet
for the *next* submission: what Google said, what was actually wrong, what has
changed since, and the exact steps at the console. It is a checklist and an
honest record, not a promise of approval — approval is Google's decision alone.

Publisher ID: `pub-8175326569491671` · ads.txt seller: the same, `DIRECT`,
certification authority `f08c47fec0942fa0`.

---

## 1 · What the email actually said

> "Your site is not ready to show ads yet: your site needs some small changes
> before it can be approved." — with the standard note about **insufficient
> content** and **low content quality**.

Two things follow from that wording, and they shaped every round since:

- "small changes" is boilerplate. The two named problems are not small, and
  treating them as small is how a site gets rejected twice.
- **Insufficient content** and **low content quality** are different complaints.
  A site can have 1,500 pages and still be rejected if most of them are thin,
  templated, or written by a robot with nothing to say.

## 2 · What was actually wrong here

Found by auditing the repository rather than guessing:

| Finding | Then | Now |
|---|---|---|
| Pages under 250 words | 89 | 2 — both `noindex` utility pages (404, a JS shell) |
| **Indexable** thin pages | 89 | **0** |
| Pages missing an `h1` | many | 0 (`test-page-skeleton`, 1,566 pages) |
| Canonicals pointing at the old GitHub Pages host | 546 | 0 |
| Languages reachable but with nothing in them ("coming soon" hubs) | yes | removed — a language appears only when real lessons exist |
| Duplicate intros across localised market pages | 6 pages | pages extended per locale |
| A band on 1,527 pages claiming "never an ad on the free material" | — | corrected: the practice is ad-free, the pages around it are not |

The audit that produces these numbers is `tools/audit-adsense-readiness.py`; the
machine-readable copy is `data/quality/adsense-readiness.json`.

## 3 · What the site is now

- **1,565 pages scanned**, 234 courses, **technical SEO PASS on all of them**
  (title, meta description, exactly one `h1`, canonical, main landmark).
- **0 indexable thin pages.** The two that remain short are deliberately short
  and `noindex` — a 404 that tries to be an article is filler.
- **Creative work, not filler:** 32 languages with their own practice, quiz and
  review engines; 352 level figures generated from the ladder; an eleven-rung
  level reference page (`/how-levels-work/`) that says plainly that CEFR has six
  levels and that the other five are half-steps; 32 tutor pages with real
  profiles; a cookie policy that names every cookie.
- **Ad policy enforced in code:** the loader is present on 1,442 pages, absent
  on 125 by policy — practice, quizzes, worksheets, review, the course player,
  legal pages, contact, admin.
- **ads.txt** is correct and the canonical domain is consistent everywhere.

## 4 · The account-side steps — these are not code, and they are not done

Do these at the AdSense console, in this order, before pressing "Request review":

1. **Privacy & messaging → GDPR message.** The site's own cookie notice is
   informational only and is *not* a consent mechanism; the repository says so
   out loud (docs/GOOGLE_MONETIZATION.md, `consent.status` in
   data/monetization/google-monetization.json). For EEA/UK/Switzerland traffic,
   configure Google's certified CMP (IAB TCF) before the review, or set the
   account to non-personalised ads in those regions.
2. **Site → verify ownership** for `ekguru.shop` (the Search Console meta tag is
   already on every page, so this should resolve on its own).
3. **ads.txt** should show as authorised (it can take days after a crawl).
4. **Auto ads: turn on in-page formats only** for the review. Leave vignettes,
   anchors, multiplex and ad intents off — they are off in this repository's
   policy too.
5. **Page exclusions in the account** must match the repository's list
   (`data/monetization/google-monetization.json` → `excluded_paths`): practice,
   quizzes, support, join, contact, legal, search, 404, tutor shell. The script
   is not loaded there, but the account setting is the second lock on the same
   door.
6. **Payment address and tax info**, or the account stays limited regardless.

## 5 · The request itself

When requesting review, one or two sentences is enough — Google's reviewers do
not act on prose, but a clear statement helps a human who opens the site:

> EkGuru is a free Hindi-learning site. Since the last review we have removed
> every thin indexable page, published 32 real language courses with practice
> and quizzes, corrected the site's own claims about advertising, and kept ads
> off every practice page by policy. The account-side consent configuration is
> in place. Requesting a new review.

## 6 · After approval — what this repository already forbids

- No ad during practice, a quiz, a worksheet, a typing drill or an exam attempt.
- No ad on support, join, contact, booking, legal pages or the admin console.
- No advertorial that looks like a lesson, no ad that imitates an EkGuru button.
- No growth in ad density without a written experiment
  (`docs/GOOGLE_AD_MANAGER_SCALE_PLAN.md`).

## 7 · How to check the site's own side, any time

```bash
python3 tools/audit-adsense-readiness.py          # content-quality numbers
python3 tools/audit-adsense-readiness.py --selftest   # the counter, on unspaced scripts
node tools/adsready.js --local                    # ads.txt, canonicals, sitemaps, legal pages
node tools/adsready.js                            # the same facts against the live site (needs network)
python3 tools/build-all.py check                  # every generator's gate + every test
```

`tools/adsready.js` writes `reports/adsready.json` (live) and
`reports/adsready-local.json` (repository mode). Neither tool predicts approval;
they exist so that a rejection is never a surprise about something the
repository could have caught.
