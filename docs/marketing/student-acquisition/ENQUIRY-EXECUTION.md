# Existing enquiries: execution checkpoint

This continues `START-HERE.md`; it does not replace its audience/permission rules.
Private recipient details and provider message IDs are kept only in an ignored
local evidence ledger, not in this public repository or deploy set.

## What was actually done

- Ran a focused learner-intent mailbox search: 14 results, no next page.
- Broadened to enquiries, contact messages, students, booking and course terms:
  32 results, no next page. These overlap the first search; **do not add them**.
  This is complete for the queries used, not a claim of exhaustive business-wide
  audience coverage. Results included tutor applications, test/owner bookings,
  form notifications and a prior non-test-labelled lesson request.
- Read the relevant contact submissions: several wanted to **teach**, not learn.
  An ambiguous earnings question was not classified as a learner lead.
- Read the earlier non-test-labelled booking request and paired automated
  notification. The notification's subject said “confirmed” but its body said
  “Request received” and awaited tutor confirmation. Neither is evidence that a
  lesson took place or that the requester is a verified paying student.
- Checked all available Sent/incoming/spam/trash matches for that recipient and
  request reference before sending. Only the two original form notifications
  were returned; no manual response or opt-out was found in that search.
- **Sent one relevant, one-off service follow-up**, then fetched the sent message
  and verified its `SENT` label, recipient and body. It asks whether help is still
  needed with the old request and requests a current goal/timezone/time only if
  the person chooses to reply. It makes no booking, availability or payment claim.
  It explicitly says this is not a newsletter and allows no further contact.

**Sent count: 1. Promotional campaign sends: 0. Delivery/read/reply/booking
outcome: not established. Do not resend this follow-up automatically.**

Previous messages to Sabitha, Neha and Neelam were not resent. Applicants and
unrelated store/customer contacts were not repurposed as student subscribers.
No email addresses were scraped, purchased or added to a newsletter sequence.

## Website changes in the accompanying release

- Align About and the Learn library around **free multilingual self-study,
  Hindi as the main path, and separate optional independent Hindi tutoring**.
- Remove blanket full/complete-course promises from the Learn introduction and
  make review limitations explicit, without hiding existing editorial notices.
- Replace conflicting Hindi-only/duplicate Learn structured data with one
  CollectionPage and an ItemList matching the visible language cards/URLs.
- Add a shared optional speaking-help next step on the Learn and Hindi hubs:
  choose a goal, compare profiles/prices/availability, confirm directly, and keep
  learning for free if no suitable tutor is listed. A click/request is not a
  confirmed booking. No newsletter signup, payment collection or popup added.
- Remove typed names from name-tool share analytics labels while preserving
  the visitor-requested share link. Count only the script, not the typed name.

Automated tests cover the static offer/schema and real share handlers. Browser
journeys cover the help CTA at mobile/desktop widths. These are functional
checks, **not native-speaker review or evidence of increased traffic**.

## Next evidence / action

1. Wait for a reply to the service follow-up; do not infer interest from sending
   it, and honour any no-contact request before another action.
2. Supply private GoatCounter 28-day and Search Console 3-month exports to identify
   the actual traffic/conversion bottleneck. No passwords, OTPs or API tokens.
3. Launch Campaign 01 only through a verified invited resource-submission route
   or with genuinely opted-in learners; do not convert this service enquiry into
   newsletter permission. Other roadmap campaigns are not reported as executed.
4. Certified CMP/account approval remains a separate owner gate. No advertising
   runtime flags or account settings were enabled by this work.
