# Real-life test report — 16 Nov 2026

Branch `arena/0804a520-ekguru` (on top of `main` @ `e9c3a0d`). Round 1: `91ccff8`; round 2 (translated rosters / list-less pages / cache honesty): see latest commit.

Scope: poori site ko real users / tutors ki tarah chalaya — booking, review
likhna, review delete karna, saare delete karna, naya likhna, tutor
active/inactive — har flow jsdom mein actual page + actual JS + fake Google
Sheet feed ke saath. Jo bhi toota, fix kiya aur test CI mein lock kiya.

> Note: production Google Sheet sandbox se reachable nahi thi (no internet),
> isliye har test ek fake sheet feed ke against chala, jo exact wahi TSV/CSV
> shape return karta hai jo Google deta hai. Apps Script (`Intake.gs`) ko bhi
> fake `SpreadsheetApp` ke saath run kiya — browser ne jo payload bheja, wahi
> verbatim server ko diya.

---

## Bugs found & fixed

| # | Kahan | Kya galat tha (user ko kya dikhta) | Fix |
|---|-------|-------------------------------------|-----|
| 1 | `js/reviews.js`, `js/sheet.js` | **Saare reviews delete karne par purane reviews dikhte rehte the.** Header-only (khali) reviews tab ko loader "broken" samajh kar throw karta tha aur cache wala purana data dikhata tha. Same bug tutors tab par: saare tutors hatao to roster purana rehta. | Valid header + 0 rows = "zero reviews" (cache clear, "No reviews yet"). Tutors tab bhi same. |
| 2 | `js/site-config.js` | Offline fallback `live-sheets/reviews.csv` ko point karta tha — **woh file kabhi exist nahi ki** (git history check ki). Har offline reader ko ek dead 404 fetch. | `fallbackCsvUrl: ""`; offline par localStorage cache serve hota hai. |
| 3 | `tools/test-intake-real-life.mjs` | Test pass hone ke baad bhi process hang (jsdom timers) → CI step kabhi khatam nahi hota. | Final PASS ke baad `process.exit(0)`. |
| 4 | `apps-script/Intake.gs`, `Unified.gs`, `js/intake.js` | **Review gate bahut strict tha.** Student ne booking ref `ek-ab2cd3` ya `EK AB2CD3` type kiya (lowercase / space / en-dash / bina dash) → review refuse. Aur agar galti se form receipt `EG-…` daala to confusing error. | `intakeNormRef_()` dono taraf: uppercase, unicode dash → `-`, spaces/underscore hatao, `EK` prefix normalise. Gate dono sides normalise karke compare karta hai; sheet mein canonical `EK-XXXXXX` store hota hai. `EG-` par saaf message: "That is a form reference (EG-…). The booking reference starts with EK- and is on your booking confirmation." |
| 5 | `tools/build-tutor-pages.js`, `tutor/deepika/`, `tutor/utkarsh-upadhyay/` | **Deepika aur Utkarsh ke profile par "Student reviews" section hamesha "Loading reviews…" par atka rehta tha** — `js/reviews.js` + `js/reviews-display.js` script tags sirf 3 profiles par haath se add hue the, in 2 par bhool gaye. Naya approved review yahan kabhi nahi dikhta. | Builder ab har profile par jahan `data-eg-reviews` section hai, dono scripts inject karta hai (store.js ke baad). Dono pages rebuild. `build-tutor-pages.js --check` clean. |

| 6 | `js/livepatch.js`, `js/sheet.js` | **PRODUCTION mein aaj live:** jab sheet mein *saare* tutors `active=no` hain (abhi ka state), English `find-tutors.html` 0 cards dikhata hai lekin `es/ fr/ de/ pt/ ja/ ar/find-tutors.html` par **paanchon tutor cards "Ver perfil" ke saath dikhte rehte the**. livepatch "EKGURU_TUTORS khali = page par tutor data nahi" maan leta tha, jabki data tha par sab hidden. | `sheet.js` ab `EKGURU_SHEET_HIDDEN_LIVE` (har hidden id) publish karta hai; livepatch use karta hai. Khali grid par page ki bhasha mein wahi zero-state ("Ahora no hay tutores disponibles…" + free-course CTA) jo generators/main.js dete hain. |
| 7 | `js/livepatch.js`, `js/sheet.js` | English roster aur baaki pages (city pages, directory, profile "other tutors") **bina sheet row wale approved tutors ko alag-alag treat karte the** (roster hide, baaki show). | Owner rule ke mutabik ab sab jagah ek hi rule: approved = visible, sirf `active=no` row hide karti hai; `active=no` par khali hui list mein honest zero-state. Offline / fetch fail par page kabhi khali nahi hota (test #12). |
| 8 | `js/reviews.js` | Offline visitor cache se reviews paint karta tha, lekin tutors tab land hote hi `EKGURU_REVIEWS_INFO.loaded` wapas `true` ho jata tha — admin ko "live" dikhta jabki cache tha. | `LAST_ERROR` yaad rakha jata hai; re-apply par `loaded:false, fromCache:true` barkarar. |

Chhoti cleanups: `tools/adminstats.js` stale `reviews.csv` entry, `site-config.js`
comment, `apps-script/UNIFIED-SETUP.md` mein ref-normalisation note.

---

## Real-life scenarios jo ab automated hain

### `tools/test-real-life-sheet-cycle.mjs` — 47/47 PASS
1. Sheet mein 3 live reviews → profile par 3 cards, 4.7★ average.
2. Owner saare delete karta hai → wahi visitor dobara aata hai → **0 cards, "No reviews yet"** (pehle bug #1 ki wajah se purane 3 dikhte the).
3. Owner naya 1 review likhta hai → sirf 1 naya card.
4. `status=hidden` kar do → card gayab.
5. Offline + warm cache → copy dikhti rehti hai (koi blank page nahi).
6. Tutor `active=no` → roster se gayab, booking band; `active=yes` → wapas.
7. Sheet mein price badlo → card aur profile dono follow karte hain.
8. Header-only tab (tutors/reviews/settings) → koi crash nahi.
9. **Har tutor profile (deepika, pinky-kumari, shikha-dutta, sushila-g, utkarsh-upadhyay): naya review likho → dikhe; saare delete → gaye.** (Yahi bug #5 pakda.)

10. **es/fr/de/pt/ja/ar rosters**: sab `active=no` → 0 cards + apni bhasha mein zero-state + `../learn/hindi/` CTA; sirf sushila `yes` → sirf uska card, koi zero-state nahi.
11. **City page / text directory / profile "other tutors"**: sab no → rows gaye + honest line; 2 active → exactly wahi 2 sheet order mein; **Google unreachable → page khali nahi hota**.

12. **Approved tutor bina sheet row ke** → har jagah visible; `active=no` row → sirf wahi hidden; `tutor.html?id=` closed vs not-found sahi.

(Total ab **106/106**.)

### `tools/test-real-life-booking-review.mjs` — 38/38 PASS
Ek student "Asha Verma" ka poora safar:
1. `find-tutors.html` par Sushila G. ka card (active=yes) → profile link.
2. `tutor.html?id=sushila-g` → Book → modal → slot chuno → form bharo → Send.
3. Exactly 1 row private sheet ko gayi, fresh `EK-XXXXXX` ref, sahi tutor/student/slot/WhatsApp/consent; `source_page` mein koi query string nahi; **email sheet row ke BAAD gayi, pehle kabhi nahi**; owner inbox ko koi mail nahi; receipt mein wahi EK- ref + "keep it for your review"; tutor ka private email receipt par nahi; browser ledger mein booking "sent".
4. Kuch din baad profile par review form: ref sloppy type kiya (`ek-ab2cd3` style) → canonical bheja gaya, thank-you dikha, form reset, button re-enabled.
5. `Intake.gs` ko browser ka exact booking payload aur review payload diya → dono accept; review `reviews_pending` mein gaya, kabhi live `reviews` tab mein nahi.

### `tools/test-reviews-fallback.js` — rewritten, PASS
Feed → cache → offline chain; dead CSV fallback hat gaya.

### `tools/test-intake.js` — typed-variant gate cases add
`ek-ab2cd3`, `EK AB2CD3`, `EKAB2CD3`, en-dash, padded spaces → sab accept, canonical store; galat ref → refuse.

---

## Regression (sab green after fixes)

| Suite | Result |
|-------|--------|
| test-sheet-apply.js | PASS |
| test-live-feed.js | PASS |
| test-intake.js | PASS |
| test-sheetsync-policy.js | PASS |
| test-sheet-fetch.mjs | PASS |
| test-tutor-activation.mjs | 39/39 |
| test-reviews-fallback.js | PASS |
| test-intake-real-life.mjs | PASS, exit 0 |
| test-real-life-sheet-cycle.mjs | 106/106 |
| test-real-life-booking-review.mjs | 38/38 |
| test-mail-flow.mjs | PASS |
| test-no-competitor-attribution.js / test-tutor-claims.js | PASS |
| test-browser-qa.mjs | 26/26 |
| test-runtime-qa.mjs | 142/142 |
| test-googlebot-parity.mjs | PASS (no cloaking) |
| `npm test` (razorpay-api, browser-qa, runtime-qa, apps-script, payment-e2e, live-payment-contract) | all PASS |
| test-data-sources.py (offline fixtures) | 21/21 |
| test-appscript-health.py | OK |
| `python3 tools/build-all.py check` | ✔ generated layers current |
| test-sheet-loader.js | FAIL **only because** it fetches the live Google Sheet and the sandbox has no internet — same failure on untouched `main`; runs fine in GitHub CI. |

CI: `.github/workflows/ci.yml` mein naya step "Real-life sheet cycle" — chaaron
naye/rewritten suites ab har PR par chalenge.

---

## Deploy ke liye owner ko kya karna hai

1. **Apps Script**: `apps-script/Unified.gs` (ya `Intake.gs`, jo deployed hai) ka
   naya text paste karo → Save → *Deploy → Manage deployments → Edit → New
   version* (URL same rehta hai). Bina iske server-side ref normalisation
   (bug #4) live nahi hogi — client side wala fix GitHub Pages ke saath turant
   live ho jayega.
2. GitHub Pages: branch merge hote hi `js/*`, `tutor/deepika/`,
   `tutor/utkarsh-upadhyay/` live.
3. Ek baar real check: kisi tutor ko `active=yes` karo, apni booking karo,
   receipt ka EK- ref lowercase mein review form mein daalo → `reviews_pending`
   mein canonical uppercase ref dikhna chahiye.

## Owner rule (16 Nov 2026): approved tutor = visible
Owner: *"jo tutor approved hai unko approved maan kar visible karna."* Implemented:
- **Approved = `js/tutors/_registry.js` mein hona.** Sheet mein row na ho to bhi tutor file values ke saath visible aur bookable hai (English roster, translated rosters, city pages, directory, `tutor.html?id=`).
- **Hide sirf explicit `active=no` row se.** (`js/sheet.js` pehle "no row = hidden" karta tha — build ke ulta; ab dono same.)
- Khali tutors tab (sirf header) = koi override nahi, sab approved tutors file values ke saath.
- Sheet-only drafts (registry ke bahar, e.g. hemlata/tara/sarshtee) pehle ki tarah roster par nahi aate jab tak `approved=yes` + real photo na ho.
- BUG #9 saath mein fixed: `tutor.html?id=<active=no tutor>` "This profile does not exist" bolta tha — ab "bookings closed" (file-backed hidden ids ab `EKGURU_SHEET_HIDDEN_LIVE` se pata chalte hain).
- Test #13 (14 checks) is rule ko lock karta hai; suite ab **106/106**.

## Jo nahi badla (jaan-boojh kar)
- `INTAKE_VERSION` 1.2.0 hi hai (tests isse assert karte hain).
- Production mein abhi bhi 0 public tutors (sab `active=no`) — yeh sheet ka
  decision hai, code ka nahi.
