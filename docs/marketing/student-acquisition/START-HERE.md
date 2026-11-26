# EkGuru — real student acquisition: findings and first campaign

## Bottom line

Website improvements are not a distribution campaign. Passing CI, successful deployment and a valid sitemap do not prove Google indexing, rankings, human visits or bookings. The exact reason for low traffic is still unverified because actual Search Console performance and authenticated analytics reports were not available in this review.

**Do not buy/scrape 100,000–2,000,000 personal email addresses or send to the account's maximum limit.** Public availability, a tutor application, a contact-form submission and permission to receive student marketing are different things.

This package contains five researched organisational/resource-page prospects, not a student email database. No campaign emails have been sent in this audit.

## 1. What was actually checked

| Check | Observed result | What this does / does not prove |
|---|---|---|
| Connected Gmail | Connection enabled; mailbox profile read successfully | Gmail can be reviewed; this is not proof of campaign consent or available sending quota |
| Learner/newsletter/analytics mailbox search | 14 matching messages; no next page for that specific query | Search covered selected terms, not every possible learner or subscription in the business |
| Enquiry/contact/subscription mailbox search | 11 matching messages; no next page for that specific query | Includes overlap with the first search, applications and apparent test messages; do not add the counts |
| Four contact-message bodies reviewed | Three clearly teaching-related; one ambiguous pay-related question | None of these four establishes student marketing permission |
| Other search previews | Multiple tutor applications; one incomplete lesson-enquiry template from an address also associated with the connected Sheets owner's account | Applications are supply, not student demand; the template is not a verified learner lead |
| Confirmed opted-in student recipients from reviewed evidence | **0 verified so far** | Not a claim that the entire business has zero learners; broader first-party consent records could change this |
| Google Sheets discovery | Two spreadsheets returned, both named for unrelated stores; no next page | No EkGuru consent/subscriber sheet found in this connected account; unrelated customer data was not opened or repurposed |
| Site analytics configuration | `js/site-config.js`: GoatCounter provider, site `ekguru`; Google Analytics is not configured there | Configuration does not prove requests are arriving or expose visitor counts |
| GoatCounter dashboard fetch | Redirected to sign-in at https://ekguru.goatcounter.com/user/new | Visitor/referrer/country statistics were not available; no login was bypassed |
| Analytics runtime | `js/analytics.js` allows counting without a stored choice but honours explicit opt-out, DNT/GPC and owner exclusion | Existing comments disagree with parts of the configuration commentary; this review follows runtime code, not historical traffic numbers in comments |
| Existing distribution materials | Social posts, three short videos, captions, tutor share kit and 30-day checklist already exist under `docs/marketing/growth-distribution-2026-11/` | Ready-to-publish files are not proof they were published or generated visits |
| Old outreach tracker | Contains an explicitly labelled example university row | It is not an actual contacted prospect or evidence of a live backlink |

Private email addresses and message bodies are deliberately not copied into this report or CSV. Prior replies to Sabitha, Neha and Neelam must not be resent as new campaign mail.

## 2. What may be blocking growth — and how to tell

| Signal | Likely next investigation | Action |
|---|---|---|
| Few Google impressions | Indexing, relevance, demand and authority | Inspect homepage + core Hindi guide, review Pages report, compare queries/pages over time |
| Impressions but few clicks | Search position, intent fit, title/snippet | Improve one already-impressed page; compare like-for-like queries and positions |
| Search clicks but low analytics count | Opt-outs, blockers, tracking delivery, report scope | Compare dates/timezones and recording behaviour; do not call all missing visits lost traffic |
| Visits but few lesson starts | Landing page/offer clarity or audience mismatch | Promote one specific useful lesson, not a giant general directory |
| Lesson starts but few tutor enquiries | Trust, tutor fit, pricing/timezone visibility or CTA friction | Test the route from one lesson to a relevant tutor and message enquiry |
| Tutor enquiries but no confirmed bookings | Response speed, availability, pricing and follow-through | Log outcomes separately; an email/WhatsApp click is not a confirmed booking |

**Most actionable finding today:** existing mailbox results skew towards teachers joining rather than students seeking lessons. That suggests reviewing audience and distribution, but does not establish that positioning alone caused low traffic.

### Data needed to identify the actual bottleneck

1. **GoatCounter:** last 28 days Pages, Referrers/Campaigns and Countries, plus the preceding 28-day comparison where available. A screenshot/export is sufficient; keep the dashboard private. Do not share passwords or API tokens.
2. **Search Console:** Search results, last 3 months: clicks, impressions, CTR, position, Queries, Pages and Countries; plus Pages/Indexing summary and homepage live URL inspection result. Redact account details if desired.
3. **Distribution evidence:** URLs of posts already published, dates, channels and any clicks/enquiries attributable to them.

Do not infer Google index coverage from a `site:` query or prescribe turning off security controls without a reproducible blocked-fetch result. Previous SEO consolidation and PR #77's practice fix are already merged/deployed; older checklists calling for their merge are historical, not current blockers.

## 3. First prospect list: five relevant organisations/resource pages

See `ORGANISATION-PROSPECTS.csv`. These are resource-distribution prospects, **not identified individual learners**, and their audience size/deliverability is unknown.

| Priority | Prospect | Verified fit and route | Send status |
|---|---|---|---|
| 1 | Omniglot | Hindi resources page explicitly invites new-link suggestions; its Contact page is linked. Contact address is displayed as an image, not extracted or guessed here. https://www.omniglot.com/links/hindi.htm | Not sent; verify the intended contact route and prior correspondence first |
| 2 | Open Culture | Free-language collection; Contact page explicitly invites link suggestions and offers a form. The fallback email was masked in fetched text; not guessed. https://www.openculture.com/contact | Not sent; manual contact form route available, submission not performed |
| 3 | SALTA | South Asian Language Resource Sites page explicitly invites site additions. A designated resource-submission contact still needs to be established; do not harvest faculty emails elsewhere on the page. https://mysalta.org/south-asian-language-resource-sites/ | Not sent; route verification pending |
| 4 | Gratis Global | Dedicated Hindi resource directory fetched successfully. No invitation/contact route verified in this review. https://gratisglobal.com/learn-hindi-free/ | Research only; no campaign send eligibility established |
| 5 | Zabaan | Hindi/Urdu learning resource collection fetched successfully. Also a language provider, so partnership fit is uncertain; no submission invitation verified. https://www.zabaan.com/free-stuff-sample-lessons/ | Research only; lower-priority potential collaborator |

These pages were fetched during this audit. A fetched page establishes relevance/existence, not endorsement, guaranteed acceptance, audience size or marketing permission. Asia Options was not included: its article appeared in search but fetching failed. SOAS was not included as a verified prospect because only a search result was inspected.

## 4. Campaign 01 — one useful resource, not a mass mailing

**Offer:** free beginner Hindi practice. Start with people already looking for Hindi resources. A travel-Hindi variant can be tested after the first channel is measured.

**Primary destination:** https://ekguru.shop/learn/hindi/

**Secondary destinations, only when relevant:**
- Travel Hindi: https://ekguru.shop/learn/hindi/travel/
- Script practice: https://ekguru.shop/hindi/alphabet/
- Tutor discovery: https://ekguru.shop/find-tutors.html

Do not call tutor lessons free. Do not imply native-speaker review, certification, guaranteed progress or tutor verification without evidence. Say you run EkGuru when recommending it.

### A. One-to-one invited editorial submission — draft, NOT SENT

**Subject:** Resource suggestion for your Hindi learning links: EkGuru

Hello,

I run EkGuru, a Hindi learning website. Your resource page invites suggestions, so I would like to submit our free beginner Hindi materials for your editorial consideration:

https://ekguru.shop/learn/hindi/

The site offers Hindi lessons and browser-based practice, including a Devanagari section:
https://ekguru.shop/hindi/alphabet/

EkGuru also has a separate directory of independent tutors; tutor lessons are not part of the free-materials offer. Please review the materials and include them only if they meet your standards. We are not requesting access to your subscriber or student contact list.

Thank you for considering the suggestion.
Team EkGuru

**Execution gate:** use only a route that actually invites submissions; personalise the reference to the relevant page, check Sent for previous contact, and record the result. Do not send this draft to all five organisations automatically. Do not enrol editors in a promotional sequence. Do not invent an address, success status or follow-up schedule.

### B. Community post — draft, NOT PUBLISHED

Read each community's current rules and obtain moderator permission where needed. Do not mass-DM members.

> Learning Hindi for a trip to India? Start with one useful question: “यह कितने का है?” (Yeh kitne ka hai? — How much is this?). Practise it slowly, then try changing the item you are asking about.
>
> Disclosure: I run EkGuru. We have free Hindi lessons and practice at https://ekguru.shop/learn/hindi/travel/?ref=community-travel-pilot . Independent tutor lessons are separate. If resource links are not allowed here, I am happy to keep the discussion to the phrases.

Have a Hindi-speaking tutor review any newly recorded pronunciation before publication. Prefer answering an existing relevant question over creating a promotional thread.

### C. Tutor/creator collaboration

Ask existing participating tutors, through the established relationship, if they want to record one 20–40 second phrase demonstration and share their own public profile. This is optional collaboration, not student marketing permission. Do not email all applicants a student newsletter or promise them bookings.

Use existing assets rather than generating another large pack:
- `../growth-distribution-2026-11/03_shorts_reels_pack/`
- `../growth-distribution-2026-11/02_official_profile_first_3_posts/`
- `../growth-distribution-2026-11/01_tutor_whatsapp_kit/`

## 5. Permission-based student email — launch blockers

No student promotional send is ready from the evidence reviewed. Before launching:

- Find/collect a real opt-in record: email, source, exact consent text/version, timestamp, purpose and status.
- Keep tutor applicants, service enquiries, confirmed subscribers and test records separate.
- A learner enquiry can receive a relevant response; it is not permission for an ongoing newsletter.
- Use a working unsubscribe/suppression mechanism, not a placeholder “unsubscribe here” sentence.
- Verify sender setup and applicable provider requirements in the intended sending service; no quota or deliverability guarantee is made here.
- Keep recipient lists private, deduplicate and suppress unsubscribed/bounced/complaining addresses before every send.
- Pilot with eligible recipients; stop and investigate delivery complaints. Do not rotate accounts to evade limits.

A proper opt-in flow and email service would require selecting a provider, supplying organisation/sender details through its normal UI, and testing subscribe/confirm/unsubscribe end to end. This report does not pretend that infrastructure is already installed.

## 6. Next seven days — measurable actions

These are proposed work targets, not traffic promises or actions already performed.

| Day | Action | Evidence to record |
|---|---|---|
| 1 | Export analytics/Search Console; choose beginner Hindi as the single pilot offer | Baseline and date range |
| 2 | Complete one invited resource submission through an established contact route | Actual sent ID/submission confirmation, not a draft |
| 3 | Publish existing Short #1 on an owned account and link the matching lesson | Public post URL and campaign/ref code |
| 4 | Give two genuinely useful replies to current learner questions, following community rules | Discussion URLs; no unsolicited DMs |
| 5 | Publish a tutor-reviewed travel phrase Short and invite one optional tutor collaboration | Post URL and collaborator confirmation |
| 6 | Complete a second invited resource submission; respond to genuine incoming enquiries | Confirmation and outcome |
| 7 | Compare attributable visits, lesson activity, tutor contacts and actual bookings | Keep “not measured” distinct from zero |

Do not spend on ads without an explicit budget, market and conversion definition. If paid acquisition is later approved, a small search-intent pilot can be considered; it is not configured or running now.

### Success measurement

Track: published/submitted items → attributable human visits → learning activity → tutor enquiries → confirmed bookings.

Use distinct `ref` values per published placement. Verify that the chosen attribution field appears in the real analytics report before relying on it. Do not put names or email addresses in campaign URLs. Link clicks are not bookings, requests are not necessarily people, and draft files are not campaigns run.

## 7. Follow-up engineering fixes

Two reproducible defects were found while continuing the audit:

1. **Join form styling was actually missing**, not merely an obsolete assertion: `css/join-wizard.css` exists but `join.html` did not load it. Restored the stylesheet link. The computed-style test now derives that dependency from the real page instead of injecting an assumed file, which had masked the production omission. Mobile/desktop browser regressions were added.
2. **Analytics rejection was destructive:** replacing GoatCounter's `count()` with a no-op stopped events permanently even after acceptance. A reversible per-call guard now honours saved opt-out/DNT/GPC/owner exclusion, including a late script-load race. Reacceptance resumes without reinjecting the counter or duplicating a pageview. Manual startup retains visibility gating and provider click binding.

Local verification: full `npm test` passed after restoring the stylesheet; analytics lifecycle tests cover reject/reaccept, late load, saved choices, DNT/GPC/owner exclusion, hidden pages and blocked provider; existing consent/ad release tests passed; public-surface gate passed (41 checks). CI/browser/deployment status must be recorded from the subsequent run, not inferred from these local results.

These defects affect presentation and measurement. They are **not established as the cause of low traffic**. The authenticated analytics/indexing exports are still needed; no marketing sends, bookings or traffic increase are claimed.

## 8. Completion status

**Done:** bounded first-party audience audit; analytics configuration review; five relevant organisational prospects researched; editorial/community drafts and launch gates prepared; reusable existing assets identified.

**Not done:** a lakh-scale personal-contact database; promotional sends; contact-form submissions; social publishing; an installed newsletter flow; access to authenticated traffic/indexing reports; verification of domain-wide email deliverability; proof of new traffic or bookings.

**Next input needed from owner:** GoatCounter and Search Console screenshots/exports, plus any actual student opt-in list with consent evidence. No passwords, OTPs or tokens in chat.
