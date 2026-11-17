# EkGuru — free-listing & backlink outreach kit (17 Nov 2026)

**Why this file exists.** The owner asked for "1000+ free-promotion sites ko mail
bhejo". Bulk unsolicited e-mail from the EkGuru Gmail is not done by the agent:
it is spam under CAN-SPAM / GDPR, Gmail suspends accounts at ~500 sends/day, and
a new education brand's domain reputation is the one thing that cannot be
bought back. What *does* work for a site like this is (1) submitting to places
that exist to list sites, (2) answering real questions where Hindi learners
already are, and (3) giving people a reason to link (free printable sheets,
the 30-day course, the alphabet tools). Everything below is free.

Brand line to use everywhere (domain may change, the name will not):

> **EkGuru** — free Hindi lessons, Devanagari practice and verified online
> Hindi tutors. "One Student. One Goal. One Guru." · https://ekguru.shop

## 1. Submit once (directories / profiles — all free)

| Where | What to submit | Notes |
|---|---|---|
| Google Search Console + Bing Webmaster | sitemap.xml | Already generated; verify ownership, submit, request indexing of the home + `/learn/` hubs |
| Google Business Profile (service-area, Jaipur) | EkGuru, "Language school / Tutoring service" | Lets the brand appear in Maps/knowledge panel |
| Bing Places, Apple Business Connect | same | 10 min each |
| Crunchbase, Product Hunt (as a free tool launch), BetaList, AlternativeTo (alt. to Duolingo-Hindi), Indie Hackers | product page | One good launch post > 100 directory links |
| GitHub profile README (EkGuruLearning org) | link + description | Already a public org |
| Wikipedia / Wikidata | **do not** self-add; only once independent coverage exists | |
| Education directories: Class Central (free courses), Coursera-alternatives lists, OpenCulture "free language lessons" page (submit by e-mail to the editor), Omniglot links page (Hindi), Language-learning subreddit wikis | the free 30-day course + alphabet pages | Omniglot and OpenCulture are the two highest-value Hindi-learning links on the web |
| Tutor marketplaces that allow an external site in the bio (italki community, Preply blog comments are **not** allowed to be scraped — bios only) | tutors' own bios | Each tutor adds their EkGuru profile link to their own bios |
| Hindi diaspora: ISKCON temple newsletters, Hindi Sahitya Sabhas (UK, US, Canada, Germany, Netherlands, Gulf), Indian embassy culture-wing pages ("learn Hindi" resource lists) | one polite e-mail each, by a human | 40-60 targets, high intent; the country pages `/hindi-tutor/<country>/` are the landing pages |

## 2. Be where learners ask (no link-drops; answer, then cite)

- r/Hindi, r/languagelearning, r/IndianFood-adjacent culture threads, HiNative,
  Quora "how to learn Hindi" questions, Duolingo forum archives (read-only),
  Discord servers for Indian languages. Answer the question fully, link the
  exact EkGuru page that answers it (e.g. `/learn/hindi/foundation/aa-ki-matra/`).
- YouTube: the tutors' intro videos already exist; a 60-second "Devanagari in
  one minute" short per vowel, description linking to the matching page.

## 3. Give people a reason to link

- Printable worksheets (`/learn/<lang>/practice/worksheets/`) — teachers link
  printables. Add a "free for classrooms" line.
- The 30-day Daily Hindi course — pitch to "best free Hindi courses" roundups.
- Hindi alphabet stroke-order animations — unique; pitch to Omniglot, Wikibooks
  Hindi talk page, language-teacher blogs.

## 4. E-mail template (for a human to send, one at a time, 20–40/day max)

```
Subject: Free Hindi lessons + verified tutors — a resource for your readers

Namaste <name>,

I run EkGuru (ekguru.shop), a small free site for learning Hindi: a 30-day
beginner course, Devanagari practice with stroke animations, printable
worksheets, and a short list of verified online Hindi tutors.

Your page <URL of their resource list> lists Hindi-learning resources; if
EkGuru is useful to your readers, we'd be grateful for a mention. Everything
on the site is free and there is no sign-up wall.

Thank you for your time,
Prakash — EkGuru
EkGuruLearning@gmail.com
```

Rules: personalised first line, one e-mail, one follow-up after 10 days, never
a third. Keep a sheet tab `outreach` (date, site, contact, status) — the
Apps Script digest can report it weekly.

## 5. Before any of this (the owner's own order: "pehle bug fix")

- [x] All approved gurus visible on first paint (PR #53)
- [x] Dark-mode safety net
- [x] Merge PR #53 → main (merged 17 Nov 2026; #54 and #55 followed)
- [x] `apps-script/Unified.gs` deployed; its `/exec` URL is `feed.url` AND
      `intake.url` in `js/site-config.js` (reviews + roster live within 30 s)
      — still owner's: redeploy the repo's 2.1.1 as a *New version* of the
      same deployment (the live health endpoint reports 1.0.0)
- [x] Indexing for `/tutor/<id>/` decided: public gurus `index, follow`;
      a hidden guru (sheet `active=no`) or an unpublished draft is
      `noindex, follow` with booking off (PR #55, round 13)
- [ ] Owner: un-publish the `reviews_pending` tab from "File → Share →
      Publish to web" (its public CSV shows reviewer contact e-mails; the
      build reads approved reviews from the Apps Script feed since round 13)
- [ ] Owner: Cloudflare → Purge Everything after each merge, and the WAF
      skip rule for the `EkGuruGuard` user-agent (weekly live-guard is red
      only because Cloudflare challenges the probe)
