# What Else Can Be Built — GitHub Pages (Static, Client-Side Only)

_Generated 2026-09-12T05:40:51Z. Every item below works on the existing architecture: static HTML +
client-side JavaScript + Google Sheets (via published CSV) + the Apps Script mail relay.
Nothing here invents a server._

## Can be built (client-side only)

1. **Spaced-repetition deck builder** — the flashcard tool already runs client-side. Extend it into
   a full SRS (Leitner/box) system with localStorage, building on the honest review lab that exists.
2. **Per-phrase computer-voice playback** — the listening lab already uses the browser
   SpeechSynthesis API. Reuse it to add "play this phrase" buttons on every lesson, labelled
   "computer voice, not a native speaker" (no fake native audio).
3. **Offline "read later" queue + full offline lessons** — a service worker already caches the site.
   Add an offline mode that pre-downloads a chosen path's lessons and lets learners study without data.
4. **Personal "My Hindi" progress dashboard** — path checkboxes already persist in localStorage.
   Add one dashboard page showing progress across paths, practice streaks and review due counts
   (all stored locally, no account).
5. **Typing/transliteration trainer** — the Devanagari typing tutor exists. Add a "type what you hear
   in Roman letters → see Devanagari" mode to build Roman→Devanagari confidence (§10).
6. **Practice quiz generator** — the practice engine already scores runs. Add a "make me a 10-question
   quiz from topic X" mode assembled from the practice bank (honest "practice score", never a certificate).
7. **Printable worksheet generator** — the materials are print-formatted. Add client-side "generate a
   worksheet from these 20 items" using print CSS (no PDF server needed).
8. **Sheets-driven content freshness** — the live-sheets CSVs already drive tutors/settings. Use the
   same pipe to let the owner update lesson metadata, prices and FAQs by editing a Google Sheet.
9. **Fuzzy search + Roman/Devanagari search** — search is client-side over search-index.json. Add
   tolerant matching and let "namaste" match "नमस्ते" and vice versa.
10. **Short daily-practice widget on the hub** — embed the existing 5/10/20-question daily lab
    directly into the Learn Hindi hub page.

## Cannot be built statically (would need a backend — state it, don't fake it)

- Real user accounts, cloud-synced progress, or server-side scoring/certificates.
- Live chat or real-time booking — booking already routes through the honest Apps Script/Calendly
  relay; that is the correct boundary.
- User-submitted content or comments (no server to moderate it).
- Server-side A/B testing or server analytics beyond the existing privacy-respecting setup.

## Recommended next build (highest value, lowest risk)

Per-phrase computer-voice playback (item 2) + the "My Hindi" dashboard (item 4): both reuse existing
mechanisms, both directly serve the learner journey, and both are fully static.
