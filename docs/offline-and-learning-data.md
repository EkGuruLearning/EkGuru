# On-device learning, compatibility and offline limits

The v1 journal (`ekguru:learning:v1`) and per-language review decks (`ekguru:srs:<code>:v1`) live on this
device and origin only. A preview host and the live site are different origins. Use the explicit learning
JSON export/import to move **only** the journal and typed language decks. Booking, payment, contact and
consent storage are never included. The original Hindi deck (`ekguru:hindi:v1:review`) and the older path/lesson
logs keep their keys; they are not deleted or silently turned into XP.

## Backups and storage safety

* Export/import are bounded to 2 MiB and validated field by field. Import **replaces** the journal and typed
  decks after explicit confirmation; unknown fields, versions, URLs or cross-language cards are rejected without
  writing anything.
* Import marks the legacy Hindi migration “done”, so a removed or import-replaced card cannot come back from the
  original deck. Copying the original deck again is an explicit, confirmed recovery (`EkGuruSRS.copyLegacyDeck()`).
* A corrupt, unreadable or future-version saved journal/deck is **preserved**: automatic tracking cannot overwrite
  it, a verified export is refused, and only a validated backup replaces it.
* Browser storage and the Cache API are not transactional. Quota failures trigger a rollback attempt and no
  success claim; this is not a crash-proof transaction guarantee.

## What the numbers mean

Completion is a self-report (20 XP once per lesson URL). A review credits 5 XP once per card per day. XP,
badges and streaks are activity records, not fluency, pronunciation or a CEFR certificate. Spoken
self-reports and listening items without a matching voice are unscored. Streak dates use local calendar days;
one optional freeze per calendar week can bridge a missed yesterday without inventing activity. Active time is
approximate. Practice with no known level is stored as “legacy”, never relabelled as A1.

The starting-point check adapts over 5–10 recognition questions that already exist in the level data. It is not a
validated assessment and native/editorial review is still pending.

## Offline snapshots

Only an explicit manifest can download a level: ≤40 same-origin public files, ≤3 MiB per level, and ≤200 pinned
entries / 25 MiB in total, all-or-nothing with a rollback attempt. Pages, scripts and styles are network-first so a
removal reaches users; images are cache-first. Private, API, payment, contact, join, support, credential, query,
remote and unknown-data routes cannot be cached. POST and authenticated requests are not intercepted. Browsers may
evict storage. A saved level is a reading snapshot; whether voices work offline depends on the device.

## Reminders

Notifications start disabled and permission is requested only from the Enable button. The time reminder works only
while an EkGuru page is open; it is not background Web Push and creates no subscription. Disabling is one action.
Real closed-page Web Push would need an owner-run service and a privacy decision; it is deliberately not simulated.
