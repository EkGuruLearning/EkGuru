/* =========================================================
   EkGuru — SITE CONFIG
   ---------------------------------------------------------
   Edit brand, contact and SEO settings here. Nothing else.
   ========================================================= */

window.EKGURU_SITE = {
  /* ---------- Brand ---------- */
  brand: "EkGuru",
  tagline: "One Student. One Guru. One Goal.",

  /* ---------- Live URL (used for canonical + sitemap + OG) ----------
     If you rename the repo, change this ONE line.

     ═══════════════════════════════════════════════════════
     v90 — MOVED TO THE CUSTOM DOMAIN, AND WHY IT MATTERED
     ═══════════════════════════════════════════════════════

     Prakash bought ekguru.shop, pointed it at GitHub Pages, and
     pushed v89. Everything worked: the site loaded, /privacy/
     returned 200, the ad loader was live, ads.txt served the
     correct publisher line at the domain root. AdSense still
     reported ads.txt as MISSING.

     ads.txt was never the problem. THIS LINE was.

     Every one of the 546 shipped pages still declared

         <link rel="canonical" href="https://ekgurulearning.github.io/EkGuru/...">

     A canonical tag is not a hint. It is the page telling Google
     "I am not the real version of myself — index that one
     instead." So Google, arriving at ekguru.shop, was told by
     every page to go somewhere else, and treated ekguru.shop as
     a duplicate. It does not read ads.txt for a domain it does
     not consider the property.

     Worse, the loop closed on itself:

         sitemap.xml lists  ekgurulearning.github.io/EkGuru/privacy/
         that URL 301s to   ekguru.shop/privacy/
         which canonicals   back to github.io

     Google followed a redirect to a page that pointed back at
     the URL it had just been redirected away from. Measured
     10 Sep 2026, all three legs confirmed by HTTP.

     3,245 URLs in sitemap.xml, 546 canonicals, robots.txt,
     feed.xml and llms.txt all named the old host. Changing this
     ONE line regenerates every one of them — which is exactly
     why the value lives here and is never written twice.

     ⚠️ The old host is NOT dead: GitHub 301s it to the domain
     permanently. Old links and any existing indexing carry over.
     ═══════════════════════════════════════════════════════ */
  baseUrl: "https://ekguru.shop/",

  /* ---------- Contact (REAL) ---------- */
  email: "EkGuruLearning@gmail.com",

  /* WhatsApp: leave "" to hide every WhatsApp button site-wide.
     Add a real number with country code to switch them all on,
     e.g. "+919876543210"                                              */
  whatsapp: "",

  /* =========================================================
     BOOKING EMAILS
     ---------------------------------------------------------
     When a student presses "Send booking request", one press
     sends one real email to three inboxes:

        the tutor      (js/tutors/<name>.js  →  email:)
        EkGuru         (the address above)
        the student    (whatever they typed in the form)

     enabled        false -> no mail is sent; the button falls
                    back to opening the student's own email app
                    with the message already written, exactly as
                    the site behaved before.
     copyToSite     EkGuru keeps a copy of every request.
     copyToStudent  the student gets their own receipt.
     alwaysCc       any extra inboxes, e.g. ["ops@ekguru.com"]
     siteKey        optional FormSubmit alias for EkGuru's inbox,
                    so the raw address is not in the page source.

     ⚠️ Each recipient address must be activated ONCE with the
     mail relay before it will receive anything. Open
     tools/mail-activate.html and follow the steps there.
     ========================================================= */
  mail: {
    enabled: true,

    /* ---------- REMOVING THE "FormSubmit Team" FOOTER ----------
       Every email FormSubmit sends carries their sign-off and a
       sponsor advert. There is no setting to remove it; it is how
       their free tier is funded, and it is added on their server
       after we hand the message over.

       Web3Forms does not brand free-tier emails. Paste an access
       key here and every booking email goes out unbranded, from
       EkGuru, with your own footer instead.

         1. go to https://web3forms.com
         2. enter EkGuruLearning@gmail.com
         3. the access key arrives by email — paste it below

       No account, no card. 250 emails a month, which is far more
       than four tutors will use. Leave it blank and FormSubmit
       keeps working exactly as it does now.                     */
    /* LIVE since v54. Verified 8 Sep 2026.
       The key is safe in public source — it only says "deliver to the
       inbox this key was registered with". It cannot read anything and
       cannot send anywhere else, which is why Web3Forms publishes it
       in their own client-side examples.

       Free tier: 250 emails a month. If that runs out mid-month the
       mailer AUTOMATICALLY falls back to FormSubmit for the rest of
       the month rather than failing — see FALLBACK in js/mailer.js.
       Nothing is lost, the only difference is their footer reappears. */
    web3formsKey: "5ad4a9a6-fcb2-445c-9764-cab8c99fadfa",

    /* ---------- MORE KEYS = A HIGHER FREE CEILING  (v87) ----------
       Web3Forms' free tier is 250 emails a month PER ACCOUNT, and
       an account is nothing more than an email address plus a key
       that arrives by return mail. So the honest way to raise the
       ceiling without paying is to hold several keys.

       Each key is metered SEPARATELY. When one is exhausted the
       mailer moves to the next automatically and says so in the
       Mail centre tab. All of them clear on the 1st.

           1 key  =   250 a month
           3 keys =   750 a month
           6 keys = 1,500 a month

       TO ADD ONE, and it takes about a minute:
         1. go to https://web3forms.com
         2. enter any address you control — a Gmail alias works,
            EkGuruLearning+relay2@gmail.com arrives in the same
            inbox and counts as a different account
         3. the key arrives immediately, no signup and no card
         4. paste it into the list below

       ⚠️ These keys are PUBLIC. They ship in the page source,
       which is unavoidable for a static site and is why the
       provider rate-limits them instead of treating them as
       secrets. Never put a credential here that would matter if
       it leaked. */
    /* ⚠️ REAL UUIDs ONLY. NOT THE WORDS BELOW.
       Found live on 11 Sep 2026: this array contained
       "second-key-here" and "third-key-here" — the example text
       from the comment above, with the comment markers removed.

       The dashboard then reported 750 emails a month against a
       real ceiling of 250, and when the genuine key hit its
       limit the chain tried "second-key-here", Web3Forms replied
       "Invalid Access Key", and the send FAILED — because that
       is an authentication error, not a quota error, so the
       quota fallback never ran.

       js/mailer.js now refuses anything that is not a UUID and
       says so in the console, so this cannot happen again. But
       an ignored key is still a key you thought you had.

       A real one looks exactly like the one above:
           995dfc7d-31cc-4403-9c63-56a1d50cd9d9

       Uncomment a line ONLY when you have pasted a real key
       into it. */
    web3formsKeys: [
      /* v95 — FIVE REAL KEYS, supplied by Prakash on 11 Sep 2026.
         He listed seven; two were the same UUID repeated, so the
         real count is five and the ceiling is 5 x 250 = 1,250 a
         month. Duplicates are dropped by js/mailer.js keys()
         anyway, but they are removed here so the file says the
         truth.

         The old key 995dfc7d-31cc-4403-9c63-56a1d50cd9d9 has been
         replaced by the first of these. It is kept out of the list
         deliberately: if it had been revoked or exhausted it would
         waste one attempt per send discovering that. */
      "abc520f5-f682-4225-9810-266bac004cd6",
      "50855e6f-ffcd-4956-b6b1-8802eb8840e1",
      "8d80b297-9f6d-42d3-8865-d4883e264021",
      "83fd80d7-9ab4-4116-9082-685433861376",
    ],

    /* ---------- EmailJS — THE RELAY THAT NEEDS NO ACTIVATION ----
       Prakash: "koi aisa free provider hai kya jo form active
       nahi karvata? to vo implement karo."

       Surveyed twelve relays live on 11 Sep 2026. This was the
       only new one that both answers a browser (CORS: *) and
       needs no per-recipient step:

         FormSubmit   every recipient must click an activation
                      link. A student never will.
         StaticForms  ignores the recipient completely.
         Formspark, Formbold, Herotofu, Pageclip, Formester
                      need a form created in a dashboard, one per
                      endpoint. We cannot make one per student.
         Resend       needs a SECRET key. A static site cannot
                      hold a secret — it would be in the page
                      source and anyone could send mail as us.

       EmailJS takes the recipient from a template parameter, and
       the template is created ONCE, by you.

       FREE: 200 emails a month. Below Web3Forms' 250, which is
       why it sits under it in the chain. It is a SECOND
       stranger-capable relay — until now there was exactly one,
       so losing it meant losing every student receipt.

       SETUP, about five minutes, once:
         1. emailjs.com → sign up (free)
         2. Email Services → add one (Gmail works)
         3. Email Templates → new template
              To      : {{to_email}}
              Subject : {{subject}}
              Reply-To: {{reply_to}}
              Body    : {{message}}
         4. Account → copy the PUBLIC key
         5. paste all three below

       ⚠️ The PUBLIC key only. EmailJS also shows a private key —
       that one must never appear here or anywhere in this repo.

       Leave these empty and nothing changes: the provider drops
       out of the chain entirely. */
    emailjs: {
      serviceId: "",
      templateId: "",
      publicKey: ""
    },

    /* ---------- THE RELAY YOU OWN (v96) ----------
       "koi aisa free provider hai kya jo form active nahi
        karvata … aisa karvana jo kabhi active form na karvaye"

       This is that, and it is the only honest answer.

       Twelve hosted relays were probed live. Every single one
       either asks the recipient to click an activation link, or
       ignores the recipient entirely, or needs a form built by
       hand in a dashboard for each endpoint. There is no hosted
       free service that does what you asked. There IS a way to
       stop renting one.

       A Google Apps Script Web App is a URL that runs inside
       YOUR Google account and sends from YOUR Gmail. Gmail never
       asks a stranger for permission before delivering to them,
       so the activation problem simply does not exist. It is
       free, it allows about 100 recipients a day (≈3,000 a month
       — twelve times Web3Forms), and — the part that matters for
       "sab ko alag format jana chahiye" — WE write the email
       body, so every message can have its own layout instead of
       the relay's.

       SETUP: tools/APPS-SCRIPT-SETUP.md, five minutes, once.
       Paste the two values it gives you below.

       Leave `url` empty and nothing at all changes: the provider
       drops out of the chain and the site behaves exactly as it
       did in v95. */
    appsScript: {
      /* Must look like
         https://script.google.com/macros/s/AKfy…/exec
         Anything else is rejected by the provider's enabled()
         check rather than silently eating your mail — the v94
         "second-key-here" lesson. */
      url: "",
      /* A shared word you invent, and paste into the script too.
         It stops a passer-by who reads the page source from using
         your Gmail as an open relay. It is NOT a secret — nothing
         in a static page ever is — which is why the script ALSO
         refuses any recipient it was not asked to allow. */
      token: ""
    },

    /* ---------- A SECOND FREE RELAY (optional) ----------
       StaticForms is the only other relay found that needs NO
       per-recipient activation and NO dashboard-built endpoint,
       which are the two things that make the others useless here.
       It has no monthly cap.

         1. go to https://staticforms.dev
         2. enter EkGuruLearning@gmail.com
         3. the access key arrives by email — paste it below

       Leave it blank and nothing changes. Fill it in and the chain
       becomes  Web3Forms → StaticForms → FormSubmit, so a booking
       survives two providers running out in the same month.

       Rejected, and why:
         Formspree  50/mo and needs a form built in their dashboard
         Getform    50/mo, dashboard endpoint
         Formcarry  100/mo, dashboard endpoint
         Basin      100/mo, dashboard endpoint
         EmailJS    needs a template plus a connected Gmail account
       Every one of those moves work onto you instead of off you. */
    /* LIVE since v59. Verified 8 Sep 2026 — a real POST to
       api.staticforms.dev/submit with this key returned
       {"success":true,"id":"fba519ee-…"}.

       Note it delivers only to the address the key is registered
       with, so it cannot copy a tutor directly. That is why it sits
       BELOW Web3Forms in the chain — see js/mailer.js. */
    staticFormsKey: "sf_cfb12602e030b67320c6f99e",
    copyToSite: true,
    copyToStudent: true,
    alwaysCc: [],
    siteKey: "",

    /* =========================================================
       WHICH RELAY SENDS WHAT  (v79)
       ---------------------------------------------------------
       Prakash: "web3 jo paid aur only limited hai wo use karo
       student copy mein aur tutor ko send karne mein record ke
       liye; contact ke liye formsubmit free wala use karo jo
       unlimited hai."

       The split, and why each way round:

         BOOKINGS  → the normal chain, Web3Forms first.
                     Low volume, high value, unbranded matters
                     when a stranger is deciding whether to trust
                     you with money. 250/month is plenty for four
                     tutors.

         CONTACT   → FormSubmit. Free forever, no monthly cap.
                     A public form is the one surface anyone can
                     submit repeatedly; metering it would starve
                     the bookings, which are the ones that earn.

         ANY CC    → FormSubmit, automatically, whatever this
                     setting says. Web3Forms drops `ccemail` on
                     the free plan AND STILL ANSWERS SUCCESS, so
                     the student's receipt vanished silently for
                     months. js/mailer.js pick() enforces this by
                     CAPABILITY, not by name.

         OUR OWN   → FormSubmit, automatically, whatever this
         INBOX       setting says. (v86) EkGuruLearning@gmail.com
                     was activated with FormSubmit once, in v49,
                     and stays activated forever — so every
                     message addressed to it is free and uncapped.
                     Setting this to "web3forms" will NOT buy what
                     is already free: js/mailer.js refuses a
                     METERED preference for an address we own.
                     The 250 belong to the messages no free relay
                     can carry — the student's receipt and the
                     contact sender's copy.

       Set to "" to use the normal chain for contact too. */
    contactProvider: "formsubmit"
  },

  /* ---------- Tutor application form ----------
     Paste your Google Form link here and every "Become a Tutor" button
     switches from email to the form automatically.
     Leave "" and the buttons keep opening a pre-filled email instead.
     Example: "https://forms.gle/AbCdEfGhIjKlMnOp"                       */
  applyFormUrl: "https://forms.gle/xtnT1mwuDvSKxn8F6",

  /* ---------- Social (leave "" to hide) ---------- */
  youtubeChannel: "https://www.youtube.com/@Sashi-e3s",
  facebook: "",
  instagram: "",

  /* ---------- Commerce ---------- */
  currency: "$",            // fallback symbol if conversion is off
  currencyCode: "USD",      // the canonical currency, used in Google schema

  /* =========================================================
     COUNTRY-AWARE PRICING
     ---------------------------------------------------------
     Shows prices in the visitor's own currency automatically,
     with no login and no server. Detection uses their browser
     timezone and language only, so nothing leaves their device.

     mode
       "currency"  same price, shown in their local money   ← default
       "regional"  different price per region (see `regional`)
       "off"       everyone sees plain USD

     showUsdAlso   append a quiet "($12)" so the real figure is
                   always visible next to the converted one

     rates         1 USD = how much. Update these every month or
                   two; approximate is fine, they are indicative.
     ========================================================= */
  pricing: {
    mode: "currency",
    showUsdAlso: true,
    allowManualSwitch: true,

    /* ---------- LIVE EXCHANGE RATES ----------
       true  -> js/rates.js fetches today's real rates once a day
                from open.er-api.com (free, no key, 166 currencies)
                and uses the table below only as a fallback.
       false -> the typed table below is used and nothing is fetched.

       Leave this on. The typed rates were 9% wrong on average when
       last checked, and 59% wrong for Argentina.                    */
    liveRates: true,

    /* ---------- FALLBACK RATES ----------
       These are only used if the live fetch fails, or if the visitor
       is offline, or if liveRates is false above. They do not need to
       be perfect any more, but refresh them once a year so the
       offline case stays reasonable. Last checked 08/09/2026.        */
    rates: {
      INR: 94.54,    EUR: 0.8604,  GBP: 0.7386,  JPY: 154.4,   AED: 3.6725,
      BRL: 5.1262,   CAD: 1.3812,  AUD: 1.3853,  NZD: 1.7003,  SGD: 1.2658,
      ZAR: 15.99,  MXN: 16.93,  PHP: 62.69,    MYR: 4.0456,   THB: 32.88,
      IDR: 17654, VND: 25969, KRW: 1345,  CNY: 6.7284,   HKD: 7.8403,
      SAR: 3.75,  QAR: 3.64,  KWD: 0.3086,  TRY: 48.46,    PLN: 3.7082,
      SEK: 9.5963,  NOK: 9.2696,  DKK: 6.4313,   CHF: 0.8092,  ILS: 3.0138,
      PKR: 277.7,   BDT: 123.0,   NPR: 151.3,   LKR: 328.1,   NGN: 1321,
      KES: 129.4,   EGP: 50.92,    MAD: 9.3872,   RUB: 86.24,    UAH: 44.49,
      CZK: 20.81,    HUF: 312.3,   RON: 4.5196,   ARS: 1511,   CLP: 933.5,
      COP: 3132,  PEN: 3.3552,   MUR: 46.88,    FJD: 2.2178,  GHS: 11.41
    },

    /* Only used when mode is "regional". A multiplier on the USD
       price, so 0.35 means an Indian student pays 35% of it.
       ⚠️ This changes what a tutor earns — agree it with them first. */
    regional: {
      IN: 0.35, PK: 0.35, BD: 0.35, NP: 0.35, LK: 0.4,
      BR: 0.5,  MX: 0.6,  AR: 0.4,  CO: 0.5,  PE: 0.55,
      ZA: 0.55, NG: 0.4,  KE: 0.45, EG: 0.4,  PH: 0.5,
      ID: 0.5,  VN: 0.5,  TH: 0.6,  TR: 0.5,  UA: 0.4,
      default: 1.0
    }
  },

  /* =========================================================
     ADMIN DASHBOARD
     ---------------------------------------------------------
     admin.html is a private tool. It is noindex and blocked in
     robots.txt, but GitHub Pages serves every file in the repo,
     so the URL is reachable by anyone who knows or guesses it.

     Set a passcode so it is not simply on display:
       1. Open admin.html — with this blank it offers to make one
       2. Type a long phrase, it prints a hash
       3. Paste the hash here
       4. Push

     Only the hash lives in the repo, never the phrase itself.

     ⚠️ Be clear-eyed about what this is: a lock on a door, not
     a vault. Anyone can read this file and see the hash, so a
     short passcode could be cracked offline. Use a long one.
     The student booking records are NOT in the repo — they live
     in your browser only — so this protects the dashboard, not
     a database.
     ========================================================= */
  admin: {
    /* Set 08/09/2026. This is a SHA-256 of your phrase plus a fixed
       salt — the phrase itself is not recoverable from it. Losing the
       phrase means generating a new hash, not reading this one. */
    passcodeHash: "97b0fd238329af05c922b1d20fddf165d0173f96012db4a51d215b147e2d6b9b"
  },

  /* =========================================================
     REAL SITE-WIDE ANALYTICS
     ---------------------------------------------------------
     The admin Activity tab counts one browser — yours. This
     counts everybody, which is what you actually need to know
     whether the SEO work is landing.

     provider  "goatcounter"  free, open source, start here
               "plausible"    nicer, ~$9/mo after a trial
               ""             nothing loads at all (default)

     site      goatcounter: your code, e.g. "ekguru", giving
                            ekguru.goatcounter.com
               plausible:   your domain

     Neither sets cookies or needs a consent banner. Google
     Analytics was deliberately not used — see js/analytics.js
     for the reasoning.

     SETUP: goatcounter.com → sign up → pick a code → paste it
     below → push. Free, two minutes.
     ========================================================= */
  analytics: {
    /* LIVE since v48. Prakash created the GoatCounter site on
       8 Sep 2026; verified reachable:
         https://ekguru.goatcounter.com/count   → 200
       Dashboard: https://ekguru.goatcounter.com/  (log in to see it)

       Your own visits are NOT counted — open the admin dashboard
       once on a browser, or run
         localStorage.setItem("ekguru_no_track","1")
       See js/analytics.js. No cookies, no consent banner needed. */
    provider: "goatcounter",
    site: "ekguru"
  },

  /* =========================================================
     GOOGLE ADSENSE  (v79)
     ---------------------------------------------------------
     Prakash: "muje isme google adsense monetization karvana hai
     jisse paise kama saku, to uske liye all requirement puri kar
     do."

     Everything AdSense checks for is now built:

       /privacy/      REQUIRED. Their own policy makes this a
                      contractual term, and a missing one is the
                      most common cause of a rejection that gets
                      reported as "low value content" instead.
       /about/        who runs the site, named, with a real link
       /contact/      built in v78
       /terms/  /disclaimer/
       ads.txt        at the domain root
       461 pages of original, hand-written material

     ═══════════════════════════════════════════════════════
     WHAT YOU STILL HAVE TO DO — IT CANNOT BE DONE FROM CODE
     ═══════════════════════════════════════════════════════

       1. Apply at adsense.google.com with this site's URL.
       2. Google gives you a publisher id: ca-pub-0000000000000000
       3. Paste it into `client` below and rebuild.

     That is the whole integration. Leave `client` empty and NO
     ad code is emitted anywhere — the site is exactly as it is
     today. Fill it in and every page gets the loader plus the
     verification meta tag.

     ⚠️ DO NOT paste a publisher id you have not been given.
     Shipping ad code before approval, or with a made-up id, is
     a policy violation on its own.

     ⚠️ ADSENSE WILL REJECT A SITE THAT IS NOT LIVE. Nothing in
     v71–v79 has been pushed. Applying before pushing means
     Google crawls a 404 for /privacy/, /about/ and /contact/ and
     rejects for exactly the reason this block was written to
     prevent. PUSH FIRST.
     ========================================================= */
  ads: {
    /* Your AdSense publisher id, e.g. "ca-pub-1234567890123456".
       Empty = no ad code anywhere.

       v88 — SET. Prakash supplied the ads.txt line on 10 Sep 2026:
           google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0
       which means the AdSense account exists and this id is real.
       The `ca-` prefix belongs on the CLIENT id used by the loader
       script; ads.txt uses the bare `pub-` form. tools/adsense.js
       strips it when writing ads.txt, so both come out correct from
       this one value — never write the id in two places. */
    client: "ca-pub-8175326569491671",

    /* Auto ads let Google place units itself. It is the right
       choice for a content site with 461 pages of varying shape:
       hand-placing slots on generated pages means editing eight
       generators, and a slot in the wrong place on a phone is an
       AdSense violation. */
    auto: true,

    /* Pages that must NEVER carry advertising, as path prefixes.
       Two different reasons, both of them policy:

         · The admin dashboard is not public content.
         · Ads ON a privacy policy or a contact form is, at best,
           a bad look while a human reviewer is reading it — and
           Google specifically dislikes ads that could be mistaken
           for page furniture on a form. The search page is
           noindex and is a utility, not content.

       Matched as a prefix against the path below baseUrl. */
    exclude: ["admin.html", "privacy/", "terms/", "disclaimer/",
              "contact/", "search/", "404.html",

              /* v88 — tutor.html is a JS SHELL, and that is an
                 AdSense policy problem the moment ads are switched on.

                 It exists so /tutor.html?id=hemlata still works for
                 old links; the real, pre-rendered profiles live at
                 /tutor/<id>/. It carries 107 visible words — the
                 header, the nav and the footer — and everything a
                 reader came for is written by JavaScript afterwards.

                 Google's policy names this directly: no ads on
                 pages "without publisher content", and screenshots
                 are taken with JS in an unknown state. A page that
                 is nav-plus-advert to a crawler is exactly the
                 "low value content" refusal reason, and it is
                 noindex anyway — so it can never earn from search.

                 There is nothing to gain and an approval to lose.
                 The four real /tutor/<id>/ pages keep their ads. */
              "tutor.html"]
  },

  /* =========================================================
     GOOGLE SHEET AS A LIVE DATA SOURCE
     ---------------------------------------------------------
     Edit prices, video links, availability and small
     corrections in a spreadsheet, and the live site picks them
     up within the hour. No file editing, no push.

     Right for: prices, video ids, bios, hiding a tutor.
     Not right for: adding a NEW tutor — that needs their page,
     schema and sitemap entry, so use tools/addtutor.js.

     SETUP: make a Sheet with an "id" column matching the files
     in js/tutors/, then File → Share → Publish to web → CSV,
     and paste the URL here. Full instructions in js/sheet.js.

     ⚠️ A published Sheet is public to anyone with the link.
     ========================================================= */
  /* =========================================================
     A SECOND SHEET — NEW PAGES FROM A SPREADSHEET  (v58)
     ---------------------------------------------------------
     Tab 1 (below) controls the four tutors. It cannot add a
     PAGE, and pages are what bring traffic — every one of the
     32 question pages so far needed a code change.

     This is tab 2. One row = one new page under /answers/,
     with QAPage schema, breadcrumbs and a sitemap entry.

     IT IS NOT A DOORWAY-PAGE MACHINE. The build refuses any
     row whose answer is under 200 characters, so it cannot be
     used to mass-produce thin pages even deliberately. That is
     the line between content Google rewards and content it
     penalises, and it is enforced in code rather than trusted
     to good intentions.

     SETUP:  node tools/contentsheet.js --template
             then add it as a second tab and publish that tab.
     ========================================================= */
  /* =========================================================
     A THIRD SHEET — REVIEWS  (v60)
     ---------------------------------------------------------
     One row per REVIEW, not per tutor, because a tutor has
     many. Add a row and it appears on their page within the
     hour, with the star rating and review count recalculated
     from the reviews themselves — so the number on the page
     can never drift away from the reviews printed under it.

     ⚠️ NEVER INVENT A REVIEW. Fake reviews are deceptive
     content under Google's review spam policy and illegal in
     the UK under the DMCC Act 2024. One fake risks every page
     on this site, not just the profile it sits on. The loader
     refuses obviously bad rows, but it cannot detect a
     plausible lie — that part is on you.

     SETUP:  node tools/makereviews.js
     ========================================================= */
  reviews: {
    /* LIVE — consolidated production workbook (see sheet tab).
       Verified 11 Sep 2026 — HTTP 200, correct header row. */
    csvUrl: "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=1290168568&single=true&output=csv",
    /* v62: 60 -> 5, same reason as the tutor sheet above. A review
       added in the morning could otherwise be invisible all
       afternoon to anyone who had loaded the page once. */
    cacheMinutes: 5,
    alwaysRevalidate: true
  },

  /* =========================================================
     SITE SETTINGS — A FOURTH TAB  (v69)
     ---------------------------------------------------------
     Prakash: "jaise mail id — isko sheet se karo, sheet mein
     change karte hi sabhi jagah change honi chahiye."

     He is right and it was a real gap. The tutor sheet controls
     every tutor; nothing controlled the SITE. The email address
     alone was baked into 85 published HTML files and into the
     JSON-LD of every tutor page — change it and you would have to
     rebuild and push before a single link moved.

     Two columns, key and value:

         key              value
         email            hello@example.com
         whatsapp         +919876543210   (or "none" to hide)
         youtubeChannel   https://youtube.com/@...
         applyFormUrl     https://forms.gle/...
         tagline          One Student. One Guru. One Goal.

     TO SWITCH ON:
       1. node tools/makesettings.js   → settings-sheet.csv
       2. add it as a fourth tab called "settings"
       3. File → Share → Publish to web → that tab → CSV
       4. paste the URL below

     Leave csvUrl blank and nothing is fetched; the values in this
     file are used exactly as they are today.

     ⚠️ A blank cell means "leave it alone", never "make it
     empty" — the same rule as the tutor sheet, because the
     alternative is one accidental deletion wiping the contact
     address off the whole site.

     ⚠️ Secrets are NOT settable here. The sheet is published to
     the web; the mail keys and the admin passcode stay in this
     file. So do baseUrl and brand — a typo in either renames the
     company or breaks every canonical URL at once. */
  settings: {
    /* LIVE — consolidated production workbook (see sheet tab).
       Verified 11 Sep 2026: HTTP 200, key/value shape. */
    csvUrl: "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=764031473&single=true&output=csv",
    cacheMinutes: 5,
    alwaysRevalidate: true,
    /* The address that is currently baked into the generated
       pages. js/settings.js rewrites any mailto: pointing here,
       which is what lets one sheet edit move 85 files' worth of
       links without each one being marked up. Update this when
       the built-in email above changes. */
    previousEmail: "EkGuruLearning@gmail.com"
  },

  content: {
    /* LIVE — consolidated production workbook (see sheet tab).
       Verified 11 Sep 2026 — HTTP 200, correct header row. */
    csvUrl: "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=2135319947&single=true&output=csv"
  },

  sheet: {
    /* LIVE since v54. Verified 8 Sep 2026 — returns HTTP 200 with all
       four tutors. Edit the Sheet and the site follows within the hour.

       A published Sheet is readable by anyone with the link, so the
       email column is deliberately left blank by tools/makesheet.js.
       A blank cell means "keep whatever the tutor file already says",
       so the Sheet can never wipe a real address either. */
    /* v63 — gid CHANGED from 415827901 to 2127621931.

       Prakash used File → Import → "Replace spreadsheet", which does
       not overwrite a tab: it DELETES every tab and creates new ones.
       A gid is permanent and never reused, so the old published URL
       pointed at a tab that no longer existed and Google answered
       HTTP 400 for it — while the reviews sheet, in the same account
       at the same minute, kept answering 200. That is how we knew it
       was the tab and not a throttle.

       ⚠️ NEXT TIME: Import → "Replace CURRENT sheet" (same tab, same
       gid, link keeps working) or just Ctrl+A, Delete, paste. Never
       "Replace spreadsheet".

       Verified 9 Sep 2026: HTTP 200, all 36 columns. */
    /* v97 — CONSOLIDATED TO THE SINGLE PRODUCTION WORKBOOK (11 Sep 2026).

       The four data tabs (tutors, reviews, settings, content) now live
       in ONE spreadsheet — the same workbook the master command lists —
       instead of four separate published spreadsheets. The previous
       tutor URL pointed at an OLDER copy of the tab: 36 columns, raw
       emails still exposed, and tara's row shifted (about/experience/
       methodology had landed in thumb/banner). The production tab has
       47 columns — including formKey, holiday, holidayUntil,
       holidayNote, specialities, badge, trialMinutes, packageDiscount,
       responseHours, intro, exams — emails blanked in favour of
       formKey, and tara's columns correct. js/sheet.js FIELDS already
       expected the 47-column schema, so the code and the config were
       out of step until this change.

       Verified 11 Sep 2026: HTTP 200, all 47 columns, 4 tutors. */
    csvUrl: "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=834026040&single=true&output=csv",
    /* v62 — WAS 60, AND THAT WAS THE BUG PRAKASH KEPT HITTING.
       A visitor's cached copy under an hour old BLOCKED the fetch
       entirely, so a price changed in the sheet stayed invisible for
       up to sixty minutes on a page that had already been loaded once
       — with a working connection and the right value one request
       away.

       Two changes together fix it. This number is now the age at
       which the cache is called stale, and js/sheet.js revalidates
       unconditionally regardless: the cached copy paints instantly so
       nothing feels slower, and a fresh fetch always runs behind it.

       Five minutes is also the honest floor. Google's own CDN caches
       a published sheet for roughly that long, so no amount of
       client-side eagerness beats it — see the note in the admin
       dashboard, which tells you the same thing rather than promising
       instant. */
    cacheMinutes: 5,

    /* Set to false to go back to the old behaviour: only fetch when
       the cache is older than cacheMinutes. There is no good reason
       to; it exists so the behaviour is a setting rather than a
       hardcoded decision buried in js/sheet.js. */
    alwaysRevalidate: true
  },

  /* =========================================================
     REAL CALENDAR BOOKING
     ---------------------------------------------------------
     Opt-in per tutor. Add  calLink: "username/50min"  to a
     tutor file and their profile shows a real Cal.com calendar
     — genuine free slots from their own calendar, instant
     confirmation, reminders, and a video link created for
     them. Free for individuals.

     A tutor without a calLink keeps the email request flow
     exactly as it is. Both work side by side.

     See js/calendar.js for the three-step tutor setup.
     ========================================================= */
  calendar: {
    brandColor: "#e0682a"
  },

  /* ---------- Founding year (for schema) ---------- */
  foundingYear: 2026,

  /* =========================================================
     FOUNDER — appears in Google's knowledge graph as the person
     behind EkGuru. Also powers the "Founder" credit in the footer.
     ========================================================= */
  founder: {
    name: "Prakash",
    displayName: "Prakash — MNIT Jaipur",
    title: "Founder & CEO, EkGuru",
    degree: "B.Tech, Computer Science & Engineering",
    college: "Malaviya National Institute of Technology Jaipur",
    collegeShort: "MNIT Jaipur",
    collegeUrl: "https://www.mnit.ac.in/",
    batch: "2022–2026",
    city: "Jaipur, Rajasthan, India",

    /* Birthplace — used only for local SEO signals and the founder schema.
       Nothing here is shown on the site beyond the footer credit line.     */
    birthplace: {
      hamlet: "Gothwal Ki Dhani",
      village: "Kolwa",
      district: "Dausa",
      state: "Rajasthan",
      country: "India",
      pincode: "303325",
      landmark: "Kolwa Railway Station"
    },
    /* The ONLY sentence written about the founder anywhere on the site. */
    bio: "Prakash — MNIT Jaipur, CSE 2022–2026 batch pass out.",
    email: "EkGuruLearning@gmail.com",
    linkedin: "https://www.linkedin.com/in/itstheprakash/",
    twitter: ""
  },

  /* =========================================================
     LAUNCH STATUS
     status: "live"    -> no badge
             "soon"    -> "Coming soon" pill in the header
             "beta"    -> "Beta" pill in the header
     ========================================================= */
  status: "live"
};

/* =========================================================
   The 7 major countries our students come from.
   Used for: language switcher, SEO hreflang, "students from" strip.
   ========================================================= */
window.EKGURU_MARKETS = [
  { code: "en", locale: "en-US", country: "United States", flag: "🇺🇸", label: "English",    dir: "ltr" },
  { code: "es", locale: "es-ES", country: "Spain",         flag: "🇪🇸", label: "Español",    dir: "ltr" },
  { code: "fr", locale: "fr-FR", country: "France",        flag: "🇫🇷", label: "Français",   dir: "ltr" },
  { code: "de", locale: "de-DE", country: "Germany",       flag: "🇩🇪", label: "Deutsch",    dir: "ltr" },
  { code: "pt", locale: "pt-BR", country: "Brazil",        flag: "🇧🇷", label: "Português",  dir: "ltr" },
  { code: "ja", locale: "ja-JP", country: "Japan",         flag: "🇯🇵", label: "日本語",       dir: "ltr" },
  { code: "ar", locale: "ar-AE", country: "UAE",           flag: "🇦🇪", label: "العربية",    dir: "rtl" }
];
