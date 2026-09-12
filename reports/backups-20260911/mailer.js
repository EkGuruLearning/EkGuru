/* =========================================================
   EkGuru — MAILER
   ---------------------------------------------------------
   WHAT THIS FILE DOES
   ---------------------------------------------------------
   When a student presses "Send booking request" in the booking
   box, this file actually SENDS a real email. Three people get
   it, from one single press:

       1. THE TUTOR      → their own personal inbox
                           (js/tutors/<name>.js  →  email: "...")
       2. EKGURU         → EkGuruLearning@gmail.com  (our copy)
                           (js/site-config.js  →  email: "...")
       3. THE STUDENT    → the address they typed in the form,
                           so they have a record of their request

   There is no server and no database anywhere in EkGuru, so the
   sending is done by a free form-to-email relay (FormSubmit).
   The browser posts the booking details to it and it delivers
   the mail. Nothing is stored by us.

   ---------------------------------------------------------
   ⚠️  ONE-TIME ACTIVATION — READ THIS
   ---------------------------------------------------------
   FormSubmit will not send mail to an address until the owner of
   that address has clicked an activation link ONCE. So:

     · The very FIRST booking request sent to a tutor will not
       reach them. Instead FormSubmit emails that tutor a
       "Activate Form" link. Once they click it, every request
       from then on arrives normally, forever.

     · Do this yourself before launch rather than letting a real
       student trigger it. Open  tools/mail-activate.html  in a
       browser and press the button next to each tutor. Then ask
       each tutor to click the activation link in their inbox.

     · EkGuruLearning@gmail.com must be activated too — it is on
       the list in that page.

   ---------------------------------------------------------
   IF YOU EVER WANT TO SWITCH THIS OFF
   ---------------------------------------------------------
   In js/site-config.js set   mail: { enabled: false }
   The booking box then goes back to the old behaviour: it opens
   the student's own email app with the message pre-written.
   Nothing breaks either way.
   ========================================================= */

(function () {
  "use strict";

  var SITE = window.EKGURU_SITE || {};
  var CFG = SITE.mail || {};

  /* The relay endpoint. FormSubmit accepts either a plain email
     address or a random alias string, e.g.
       https://formsubmit.co/ajax/xxxxxxxxxxxxxxxxx
     The alias hides the address from spam bots. See
     tools/mail-activate.html for how to get one.               */
  var ENDPOINT = "https://formsubmit.co/ajax/";

  /* =========================================================
     TWO PROVIDERS, AND WHY
     ---------------------------------------------------------
     FormSubmit puts "Your friends from, FormSubmit Team" and a
     sponsor advert at the bottom of every email it sends. There
     is no setting to remove it — I checked their documentation
     and their templates page. It is how the free tier is paid
     for, and it is not something code on our side can strip,
     because the footer is added by their server after we hand
     over the message.

     Web3Forms does not brand its emails on the free tier. It
     allows 250 submissions a month, needs no account beyond an
     access key emailed to you, and works from a static page.
     That is comfortably more than four tutors will receive.

     So: put a Web3Forms access key in js/site-config.js and
     every email goes out unbranded, from EkGuru, with a link
     back to the site and Prakash's name at the bottom. Leave it
     blank and FormSubmit continues exactly as before, branding
     and all — nothing breaks either way.

         js/site-config.js
           mail: { web3formsKey: "your-access-key-here" }

     Get a key free at https://web3forms.com — enter your email,
     it arrives in one message. No signup, no card.
     ========================================================= */
  var W3F_ENDPOINT = "https://api.web3forms.com/submit";

  /* =========================================================
     THE PROVIDER CHAIN  (v55)
     ---------------------------------------------------------
     Prakash asked for more free relays that need no per-address
     activation, all falling back to one another.

     WHAT WAS SURVEYED, and why most were rejected:

       Web3Forms    ✓ no activation, 250/mo, unbranded.
       FormSubmit   ✓ works, but EVERY recipient address must be
                      activated once by clicking a link. Shikha's
                      still is not, which is exactly the problem.
       Formspree    ✗ free tier is 50/mo AND requires you to
                      create a form in their dashboard first.
       StaticForms  ✓ free, unlimited, no dashboard — you request
                      an access key by email and use it forever.
       Getform      ✗ 50/mo, dashboard-created endpoint.
       Formcarry    ✗ 100/mo, dashboard-created endpoint.
       Basin        ✗ 100/mo, dashboard-created endpoint.
       EmailJS      ✗ needs a template built in their UI plus a
                      connected Gmail account — more setup, not less.

     So the ones that genuinely need no per-recipient activation
     are Web3Forms and StaticForms. Both are wired here. Anything
     that needs a dashboard-built endpoint was deliberately left
     out: it moves work onto Prakash rather than off him.

     HOW THE CHAIN BEHAVES

       1. try each ENABLED provider in order
       2. a quota refusal marks that provider spent for the month
          and moves straight to the next one, resending the same
          message — the student never sees a failure
       3. FormSubmit is always last, because it is the only one
          that can bounce for an unactivated address
       4. if every provider refuses, the booking falls back to the
          student's own email app, exactly as before

     Adding another provider later is one entry in this array.
     ========================================================= */
  /* BUG FOUND v59 — WRONG DOMAIN.

     This said api.staticforms.XYZ. The service Prakash actually
     signed up to is api.staticforms.DEV. Both hostnames answer, so
     it would never have failed loudly — it would simply have sent
     his mail through a different company's relay than the one his
     key belongs to. Verified 8 Sep 2026 against the real key:
     .dev returns {"success":true,"id":"…"}. */
  var STATIC_ENDPOINT = "https://api.staticforms.dev/submit";

  /* =========================================================
     v95 — EMAILJS. THE ONE PRAKASH ASKED FOR.
     ---------------------------------------------------------
     "koi aisa free provider hai kya jo form active nahi
      karvata? to vo implement karo"

     Yes, and this is it. Surveyed 12 relays live on 11 Sep 2026;
     this was the only new one that both answers a browser and
     needs no per-recipient step.

         Origin: https://ekguru.shop
         → 400, access-control-allow-origin: *

     WHY IT IS DIFFERENT FROM EVERY OTHER OPTION

       FormSubmit   refuses any address whose owner has not
                    clicked an activation link. A student never
                    will. This is the wall.
       StaticForms  ignores the recipient entirely and delivers
                    wherever the key was registered.
       Formspark / Formbold / Herotofu / Pageclip / Formester
                    all need a form created in a dashboard, per
                    endpoint. We cannot create one per student.
       Resend       needs a SECRET key. A static site cannot hold
                    a secret — it would be readable in the page
                    source and anyone could send mail as us.

     EmailJS takes the recipient from template_params, and the
     TEMPLATE is created once by the account owner. No activation,
     no dashboard entry per recipient, and the public key is
     designed to ship in the browser — that is what their own
     CDN-hosted SDK does.

     FREE TIER: 200 emails a month. Smaller than Web3Forms' 250,
     which is exactly why it sits BELOW it in the chain. It is a
     second stranger-capable relay, not a replacement — and a
     second one is the whole point, because until now losing
     Web3Forms meant losing the student receipt entirely.

     SETUP, once, about five minutes:
       1. emailjs.com → sign up free
       2. add an email service (Gmail works)
       3. create a template whose To field is {{to_email}}
          and whose body uses {{subject}} and {{message}}
       4. copy the service id, template id and PUBLIC key into
          js/site-config.js under mail.emailjs

     Leave it empty and nothing changes — enabled() is false and
     the provider drops out of the chain entirely.
     ========================================================= */
  var EMAILJS_ENDPOINT = "https://api.emailjs.com/api/v1.0/email/send";

  /* =========================================================
     v96 — GOOGLE APPS SCRIPT. THE RELAY WE OWN.
     ---------------------------------------------------------
     Prakash, five times now and still the same sentence:

       "koi aisa free provider hai kya jo form active nahi
        karvata? … aisa karvana jo kabhi active form na karvaye"

     Every hosted relay surveyed (12 of them, live, 11 Sep 2026)
     falls into one of three buckets:

       · needs the recipient to click an activation link
             FormSubmit
       · ignores the recipient and delivers to the key owner
             StaticForms
       · needs a form built in a dashboard, one per endpoint
             Formspark Formbold Herotofu Formester Pageclip
             Sheetmonkey Formcarry Basin Getform

     Only Web3Forms and EmailJS escape all three, and BOTH are
     metered. So the honest answer to "unlimited, never asks for
     activation" was, until today, "does not exist as a hosted
     service".

     IT EXISTS IF WE STOP RENTING AND START OWNING.

     A Google Apps Script Web App is a URL that runs code in
     Prakash's own Google account. MailApp.sendEmail() there
     sends from HIS Gmail, so:

       · no activation, ever — Gmail does not ask a stranger for
         permission before delivering to them
       · no dashboard entry per recipient — the recipient is an
         argument
       · free, permanently. 100 recipients/day on a consumer
         Gmail = ~3,000 a month, which is 12× Web3Forms' 250 and
         more than the other four put together
       · WE write the email body. Every other relay imposes its
         own layout; this one sends exactly the HTML we hand it.
         That is the direct answer to "sab ko alag format jana
         chahiye" — the format stops being the relay's choice.
       · it can CC, it can BCC, it can set a real Reply-To

     ⚠️ THE CORS TRAP, AND WHY THE HEADER BELOW IS NOT A TYPO.
     Apps Script Web Apps do NOT answer the OPTIONS preflight.
     Send `Content-Type: application/json` and the browser fires
     a preflight, gets no CORS headers back, and the request dies
     before it ever reaches Google — a failure that looks exactly
     like the script being broken and costs an afternoon.

     The fix is to make the request SIMPLE, so no preflight
     happens at all. A simple POST is one whose Content-Type is
     text/plain, application/x-www-form-urlencoded, or
     multipart/form-data. We send the JSON as text/plain and
     JSON.parse it inside doPost(). Verified as the standard
     workaround across a decade of reports.

     That is why post() reads `active.contentType` instead of
     hardcoding application/json. A relay's wire format is the
     relay's property to declare — the same rule as cannotCC and
     canAddressStrangers, and for the same reason.

     SETUP: tools/apps-script-mailer.gs is the whole script, and
     tools/APPS-SCRIPT-SETUP.md is the click-by-click. Five
     minutes, once. Leave mail.appsScript.url empty and this
     provider drops out of the chain and nothing changes.
     ========================================================= */

  var PROVIDERS = [
    {
      /* FIRST IN THE CHAIN ON PURPOSE. It is free, it is the
         largest allowance of the five, it can reach a stranger,
         and it is the only one whose email body we control. Every
         other relay is now a fallback behind it rather than the
         front line. If it is not configured, enabled() is false
         and the chain is exactly what it was in v95. */
      id: "appsscript",
      label: "Google Apps Script (your own Gmail)",
      branded: false,
      quotaNote: "about 100 recipients a day from a free Gmail account",
      /* NOT metered in the sense the others are. There IS a daily
         cap, but it is a per-day cap that resets by itself, not a
         monthly allowance that strands us on the 28th. Marking it
         metered:false is what lets ownInboxRelay() prefer it and
         keeps the paid quotas for the messages only they can
         carry. A daily refusal still marks it spent for the month
         via the normal quota path — see the note in post(). */
      metered: false,
      ignoresRecipient: false,
      /* It is Gmail. Of course it can CC. */
      cannotCC: false,
      /* THE WHOLE POINT. No activation link, ever. */
      canAddressStrangers: true,
      /* ⚠️ text/plain, NOT application/json — see the long note
         above. A JSON content-type triggers a CORS preflight that
         Apps Script cannot answer. */
      contentType: "text/plain;charset=utf-8",
      /* Apps Script answers a 302 to googleusercontent before the
         real body; fetch follows it by default, but say so. */
      redirect: "follow",
      url: function () {
        return String((CFG.appsScript || {}).url || "").trim();
      },
      enabled: function () {
        var u = this.url();
        /* Only a real deployed Web App URL counts. A half-pasted
           value is a dead relay that silently eats every message,
           which is precisely the "second-key-here" bug of v94 in
           a new costume — so validate the SHAPE, not just the
           emptiness. */
        return /^https:\/\/script\.google\.com\/macros\/s\/[\w-]+\/exec/.test(u);
      },
      build: function (to, payload) {
        var body = {};
        for (var k in payload) {
          if (k === "_subject" || k === "_template" || k === "_captcha" ||
              k === "_cc" || k === "email") continue;
          if (payload[k] !== undefined && payload[k] !== null && payload[k] !== "") {
            body[k] = payload[k];
          }
        }
        return {
          url: this.url(),
          body: {
            /* A shared secret, so a stranger who finds the URL in
               our page source cannot use our Gmail as an open
               relay. It is NOT a security boundary — anything in
               a static page is public — but it stops a drive-by,
               and doPost() also refuses any recipient outside the
               allow-list it is given. Documented honestly in the
               setup guide rather than described as encryption. */
            token: String((CFG.appsScript || {}).token || ""),
            to: to,
            subject: payload._subject || "EkGuru",
            replyTo: payload.email || SITE.email || "",
            cc: payload._cc || "",
            fromName: SITE.brand || "EkGuru",
            /* The labelled rows, in order, exactly as every other
               provider receives them. doPost() renders them as a
               table — OUR table, in OUR wording. */
            rows: body
          }
        };
      }
    },
    {
      id: "web3forms",
      label: "Web3Forms",
      branded: false,
      quotaNote: "250 emails a month",
      /* METERED. 250 a month, and when they are gone they are gone
         until the 1st. Read by ownInboxRelay() below: anything
         addressed to an inbox WE own must never be paid for out of
         this budget, because our own inbox is already activated on
         the free unlimited relay. See v86. */
      metered: true,
      /* It honours the `to` field, so it can deliver to a named
         third party. StaticForms cannot — see there. */
      ignoresRecipient: false,
      /* =========================================================
         ⚠️ WEB3FORMS CANNOT CC ON THE FREE PLAN         (v79)
         ---------------------------------------------------------
         THIS IS WHY THE STUDENT NEVER GOT THEIR EMAIL.

         Prakash: "maine dekha ki student ke paas mail hi nahi
         ja raha."

         He is right, and the cause is documented by Web3Forms
         themselves — `ccemail` is listed under PRO FEATURES:

           web3forms.com/blog/working-contact-forms-jamstack-
           websites-api        "Add CC Emails (Pro)"
           github.com/surjithctly/web3forms-docs
           /getting-started/pro-features/add-cc-email.md
             "Heads Up! This is a PRO feature. You must have an
              active membership to use this feature."

         Two things made this invisible for months:

           1. The free API does not REJECT a cc field. It returns
              {"success":true} and silently drops it. So every
              log, every test that checked the response, and the
              confirmation screen all said the receipt was sent.
              It never was.

           2. The field name was wrong anyway — this code sent
              `cc`, and Web3Forms' field is `ccemail`. Even on Pro
              it would have done nothing.

         A response that says success while dropping a recipient
         is the worst possible failure mode, and it is exactly the
         "a timeout is NOT a pass" lesson in a new costume.

         THE FIX, which is what Prakash asked for:
         a message that needs a CC is not sent through Web3Forms
         at all. `cannotCC: true` below is read by pick() and by
         chain(), which route those jobs to FormSubmit instead —
         free, unlimited, and CC works. Web3Forms keeps the jobs
         it is genuinely better at: the single-recipient, unbranded
         ones.
         ========================================================= */
      cannotCC: true,
      /* =========================================================
         ...BUT IT CAN ADDRESS A STRANGER, AND IT IS THE ONLY ONE
         ---------------------------------------------------------
         The other side of the coin, and the reason this provider
         is still worth its 250/month limit.

         Web3Forms takes a `to` and delivers to it with NO
         activation step, because the ACCOUNT is verified by the
         access key rather than the recipient being verified
         individually. FormSubmit is the opposite: free and
         unlimited, but it refuses any address whose owner has not
         clicked an activation link.

         Probed against the live endpoint on 10 Sep 2026, with a
         browser Origin header so it was not the file:// path:

           POST formsubmit.co/ajax/never-a-real-person@example.com
           → {"success":"false","message":"This form needs
              Activation..."}

         A visitor filling in the contact form is by definition an
         address we have never seen. So their receipt can only be
         DELIVERED by a relay that does not demand activation.

         This flag is what routes it. See contact() — it is a
         capability, so adding a fourth relay later needs no edit
         anywhere else. */
      canAddressStrangers: true,
      /* =========================================================
         v87 — MORE THAN ONE ACCESS KEY
         ---------------------------------------------------------
         Prakash: "admin se kisi ko bhi unlimited mail bhej saku,
         bina kisi dikkat ke."

         Web3Forms' free tier is 250 a month PER ACCOUNT, and an
         account is just an email address plus a key that arrives
         by return. So the honest way to raise the ceiling without
         paying is to hold several keys and move to the next one
         when a key is spent.

         `web3formsKeys: []` in site-config takes any number.
         `web3formsKey: ""` still works and is treated as the
         first entry, so nothing breaks and no migration is
         needed. Three keys is 750 a month; six is 1,500.

         Each key is metered SEPARATELY in localStorage, because
         they are separate accounts with separate quotas. Marking
         the provider spent when one key is exhausted would throw
         away the other two — which is precisely the bug this
         replaces. See activeKey() and markKeySpent().

         ⚠️ These keys are public by design. Anyone can read them
         in the page source. That is true of every static-site
         form relay and is why the keys are rate-limited by the
         provider rather than kept secret. Do NOT put anything
         here that would be damaging to leak. */
      /* ═══════════════════════════════════════════════════════
         v94 — A KEY MUST LOOK LIKE A KEY
         ───────────────────────────────────────────────────────
         Found on the LIVE site, 11 Sep 2026. site-config had:

             web3formsKeys: [
               "second-key-here",
               "third-key-here",
             ]

         Those are the PLACEHOLDERS from the v87 comment, with
         the comment markers removed. Somebody uncommented the
         example instead of pasting real keys — an easy and
         completely understandable mistake.

         What it did was worse than doing nothing:

           · the dashboard reported "3 keys · 750 emails/month"
           · the real ceiling was still 250
           · and when the real key hits its limit, the chain
             moves to "second-key-here", Web3Forms answers
             "Invalid Access Key", and that is NOT a quota
             message — so it is not caught by the quota
             fallback. The send fails outright.

         Reproduced: with the real key exhausted, a student's
         booking receipt failed with "Invalid Access Key" while
         the dashboard still showed two keys remaining.

         A Web3Forms access key is a UUID. Anything that is not
         one cannot be a key, so it is dropped here — before it
         can be counted, displayed or tried. The dashboard then
         shows the truth, and the failure mode disappears
         because the bad value never enters the chain.

         ⚠️ Deliberately NOT silent: a rejected value is logged
         once, with its own text, so the cause is visible in the
         console rather than being a mysterious "why is it still
         250?".
         ═══════════════════════════════════════════════════════ */
      keys: function () {
        var out = [], bad = [];
        var VALID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

        function take(k, where) {
          k = String(k == null ? "" : k).trim();
          if (!k) return;
          if (!VALID.test(k)) { bad.push(k + "  (" + where + ")"); return; }
          if (out.indexOf(k) === -1) out.push(k);
        }

        take(CFG.web3formsKey, "mail.web3formsKey");
        (CFG.web3formsKeys || []).forEach(function (k) {
          take(k, "mail.web3formsKeys");
        });

        if (bad.length && !this._warned) {
          this._warned = true;
          if (window.console && console.warn) {
            console.warn("[EkGuru] " + bad.length + " Web3Forms value(s) ignored — " +
              "an access key is a UUID like 995dfc7d-31cc-4403-9c63-56a1d50cd9d9. " +
              "Get real keys free at web3forms.com and paste them into " +
              "mail.web3formsKeys in js/site-config.js. Ignored: " + bad.join(", "));
          }
        }
        return out;
      },
      /* The first key that has not hit its own monthly limit. */
      activeKey: function () {
        var all = this.keys();
        for (var i = 0; i < all.length; i++) {
          if (!spent("web3forms:" + all[i])) return all[i];
        }
        return null;
      },
      /* Enabled while ANY key is still usable. A provider whose
         keys are all spent must drop out of the chain, or every
         send burns a request discovering that again. */
      enabled: function () { return !!this.activeKey(); },
      build: function (to, payload) {
        var body = {};
        for (var k in payload) body[k] = payload[k];
        var key = this.activeKey() || this.keys()[0] || "";
        body.access_key = key;
        /* Remembered so the response handler can mark the right
           KEY spent rather than the whole provider. */
        body.__ekguruKey = key;
        body.subject = payload._subject || "EkGuru";
        body.from_name = (SITE.brand || "EkGuru");
        if (to && to.indexOf("@") > -1) body.to = to;
        /* The correct field name is `ccemail`, not `cc` — and it is
           Pro-only regardless. It is set here so that IF the account
           is ever upgraded this path is already right, but pick()
           will not send a CC job here in the first place. */
        if (payload._cc) body.ccemail = payload._cc;
        delete body._subject; delete body._template;
        delete body._captcha; delete body._cc;
        /* Internal bookkeeping, never sent over the wire. Read off
           the built body by post() before the fetch. */
        var usedKey = body.__ekguruKey; delete body.__ekguruKey;
        return { url: W3F_ENDPOINT, body: body, key: usedKey };
      }
    },
    {
      id: "emailjs",
      label: "EmailJS",
      branded: false,
      quotaNote: "200 emails a month, and no per-recipient activation",
      metered: true,
      ignoresRecipient: false,
      /* No CC on the free tier — the recipient is a single
         template field. Same shape as Web3Forms. */
      cannotCC: true,
      /* THE PROPERTY THAT MATTERS. No activation link, no
         dashboard entry per recipient: the address is a template
         parameter. This is the second relay that can reach a
         stranger, and before v95 there was only one. */
      canAddressStrangers: true,
      enabled: function () {
        var c = CFG.emailjs || {};
        return !!(String(c.serviceId || "").trim() &&
                  String(c.templateId || "").trim() &&
                  String(c.publicKey || "").trim());
      },
      build: function (to, payload) {
        var c = CFG.emailjs || {};
        /* Flatten our labelled rows into one readable block. Their
           template has a fixed shape, so everything that is not a
           named field goes into {{message}} rather than being
           silently dropped — which is what StaticForms taught us. */
        var lines = [];
        for (var k in payload) {
          if (k.charAt(0) === "_" || k === "email") continue;
          if (payload[k]) lines.push(k + ": " + payload[k]);
        }
        return {
          url: EMAILJS_ENDPOINT,
          body: {
            service_id: String(c.serviceId).trim(),
            template_id: String(c.templateId).trim(),
            user_id: String(c.publicKey).trim(),
            template_params: {
              to_email: to,
              from_name: (SITE.brand || "EkGuru"),
              reply_to: payload.email || SITE.email || "",
              subject: payload._subject || "EkGuru",
              message: lines.join("\n")
            }
          }
        };
      }
    },
    {
      id: "staticforms",
      label: "StaticForms",
      branded: false,
      quotaNote: "no monthly cap",
      /* Not metered — but it ignores the recipient entirely and
         delivers wherever the KEY is registered, so it is only ever
         a floor, never a choice. */
      metered: false,
      ignoresRecipient: true,
      /* It cannot honour a recipient at all (see below), so it
         certainly cannot honour a CC. Same flag, same routing. */
      cannotCC: true,
      /* And for the same reason it cannot address a stranger: it
         delivers to whichever address the KEY was registered with
         and silently ignores the recipient you pass. */
      canAddressStrangers: false,
      /* Get a key free at staticforms.dev — enter an email, the key
         arrives immediately, no account and no dashboard.

         ⚠️ IMPORTANT LIMITATION, verified 8 Sep 2026:
         StaticForms delivers to the address the KEY was registered
         with. It ignores any recipient you pass — omitting `email`
         entirely still returns success. So it cannot send a tutor
         their own copy; everything lands in EkGuru's inbox.

         That is fine as a FALLBACK — a booking reaching Prakash is
         infinitely better than a booking failing — but it is the
         reason StaticForms sits below Web3Forms in the chain rather
         than above it, and the reason the message it sends says
         plainly at the top who it was meant for. */
      enabled: function () { return !!(CFG.staticFormsKey && String(CFG.staticFormsKey).trim()); },
      build: function (to, payload) {
        /* StaticForms uses its own field names and flattens
           everything else into the message body, so the long
           formatted text we already build is passed as `message`. */
        var lines = [];
        for (var k in payload) {
          if (k.charAt(0) === "_" || k === "message") continue;
          if (payload[k]) lines.push(k + ": " + payload[k]);
        }
        /* Because StaticForms cannot honour a recipient, the intended
           address is written into the first line of the message. If
           this arrives in EkGuru's inbox instead of the tutor's, it
           still says who to forward it to — an email that reaches
           the wrong inbox with no addressee is nearly useless. */
        var header = "FOR: " + to +
          "\n(sent via the backup mail relay, which can only deliver to " +
          "the EkGuru inbox — please forward)\n\n";

        return {
          url: STATIC_ENDPOINT,
          body: {
            accessKey: String(CFG.staticFormsKey).trim(),
            subject: (payload._subject || "EkGuru booking"),
            replyTo: payload["Student email"] || (SITE.email || ""),
            name: (SITE.brand || "EkGuru"),
            email: to,
            honeypot: "",
            message: header + (payload.message || "") +
              (lines.length ? "\n\n" + lines.join("\n") : "")
          }
        };
      }
    },
    {
      id: "formsubmit",
      label: "FormSubmit",
      branded: true,
      quotaNote: "unlimited and free forever, but each address must be activated once",
      /* FREE AND UNLIMITED. This is the relay every message
         addressed to one of OUR OWN inboxes must use — see
         ownInboxRelay(). Our inboxes are activated once and forever,
         so the activation caveat that makes this relay useless for
         strangers does not apply to us at all. */
      metered: false,
      ignoresRecipient: false,
      /* =========================================================
         THE ONLY FREE RELAY THAT ACTUALLY DELIVERS A CC   (v79)
         ---------------------------------------------------------
         Prakash: "web3 jo paid aur only limited hai wo use karo
         student copy mein aur tutor ko send karne mein record ke
         liye; contact ke liye formsubmit free wala use karo jo
         unlimited hai."

         The instinct is right and the reasoning is worth writing
         down, because it is the opposite of what the chain did:

           Web3Forms   250/month, unbranded, single recipient only.
                       A metered resource. Spend it where the
                       polish is worth it and no CC is needed.
           FormSubmit  free forever, no monthly cap, `_cc` works.
                       Branded footer. Spend it where volume and
                       CC matter more than a footer.

         So `_cc` in a payload now ROUTES the message, rather than
         being a field that may or may not survive. See pick().

         The activation caveat is unchanged and is the reason the
         student is a CC on a post to OUR inbox rather than a post
         addressed at them: FormSubmit will not deliver to an
         address whose owner has never clicked an activation link,
         and a stranger never has. A CC needs no activation.
         ========================================================= */
      cannotCC: false,
      /* ⚠️ IT CANNOT REACH SOMEBODY WE HAVE NEVER MAILED BEFORE.
         Every recipient address must be activated once by its
         owner clicking a link. That is fine for our own two
         inboxes — activated once, forever — and impossible for a
         visitor who has just filled in the contact form.

         Re-verified against the live endpoint on 10 Sep 2026:
         posting to a fresh address returns
           {"success":"false","message":"This form needs Activation..."}
         and, worse, emails an activation link to a person who did
         not ask for one.

         A CC has no such requirement, which is why the student's
         booking receipt rides as a CC here. But a message
         ADDRESSED to a stranger must go via Web3Forms. */
      canAddressStrangers: false,
      /* Always available — it is the floor of the chain. */
      enabled: function () { return true; },
      build: function (to, payload) {
        return { url: endpointFor(to), body: payload };
      }
    }
  ];

  /* Which providers are usable right now, in order, skipping any
     that have already hit their monthly limit. */
  function chain() {
    return PROVIDERS.filter(function (p) {
      return p.enabled() && !spent(p.id);
    });
  }

  /* =========================================================
     pick(payload) — THE RIGHT RELAY FOR *THIS* MESSAGE   (v79)
     ---------------------------------------------------------
     Until v79 there was one chain for everything, and the first
     usable provider won regardless of what the message needed.
     That is how the student's receipt vanished: it carried a
     _cc, Web3Forms was first, Web3Forms drops cc on the free
     plan, and it answers success anyway.

     Choosing per MESSAGE rather than per SITE is the fix, and it
     is also what Prakash asked for in plain terms — spend the
     metered, unbranded relay where it helps, and use the free
     unlimited one where CC or volume matters.

       needs a CC   → only relays that can actually deliver one
       everything   → the normal chain, best first
       else

     A capability, never a hardcoded provider name. Add a fourth
     relay tomorrow, set cannotCC on it correctly, and this
     function needs no edit. Naming providers here is how you get
     the fourteen-hardcoded-values problem this project keeps
     rediscovering.

     If NOTHING can CC — every capable relay spent — we do not
     drop the recipient silently, which is the whole bug. We fall
     back to the best available and mark the payload so send()
     posts a SEPARATE message to that person instead. Degraded,
     visible, and nobody is quietly left out.
     ========================================================= */
  function pick(payload) {
    var usable = chain();
    if (!usable.length) usable = [PROVIDERS[PROVIDERS.length - 1]];

    if (payload && payload._cc) {
      var canCC = usable.filter(function (p) { return !p.cannotCC; });
      if (canCC.length) return canCC[0];
      /* Nobody can. Caller must split the message. */
      return null;
    }
    return usable[0];
  }

  /* =========================================================
     v86 — OUR OWN INBOX IS NEVER PAID FOR
     ---------------------------------------------------------
     Prakash: "jo mail EkGuruLearning@gmail.com ko aaye vo free
     wale se hi aana chahiye — record wali aur contact wali."

     He is right, and it is not only a preference — it is the
     single biggest waste in the mail budget.

     WHAT WAS HAPPENING (v81–v85)
     Web3Forms sits first in the chain, so pick() handed it every
     payload that carried no _cc. That included the two messages
     addressed to OUR OWN inbox:

         [record] <ref> — student → tutor      (every booking)
         the booking record when the tutor has no personal
         address, which is 3 tutors out of 4

     Both were burning the 250-a-month metered quota to deliver
     mail to an address that FormSubmit can reach for free,
     forever, with no cap.

     WHY IT IS SAFE, AND WHY IT IS ONLY SAFE FOR *US*
     FormSubmit refuses any recipient whose owner has not clicked
     an activation link. That is what makes it useless for a
     student or a fresh tutor. It is completely irrelevant for
     EkGuruLearning@gmail.com, which was activated once, in v49,
     and stays activated forever. So for our own inbox FormSubmit
     is strictly better: same delivery, zero cost, no cap.

     THE ARITHMETIC
     A booking used to spend 3 Web3Forms sends (tutor, record,
     student receipt). With 3 of the 4 tutors routing to our own
     inbox, one of those was doubly wasteful. Now:

         tutor has own address   → 2 metered (tutor + student)
         tutor routes to us      → 1 metered (student only)

     Roughly 83 bookings a month became 125–250. The receipt to
     the student is the one thing only Web3Forms can do, and now
     it gets the whole budget.

     ⚠️ CAPABILITY, NOT A NAME. This picks "cheapest relay that
     can actually deliver to an address we control" — it does not
     say "formsubmit". Add a fourth free relay tomorrow with
     metered:false and it is used with no edit here. Writing a
     provider id into logic is the hardcoded-value problem this
     project has now rediscovered fifteen times.
     ========================================================= */

  /* Every inbox EkGuru itself owns and has activated. Anything in
     this list can be reached by the free unlimited relay. */
  function ourInboxes() {
    var list = [];
    if (isEmail(SITE.email)) list.push(String(SITE.email).toLowerCase());
    (CFG.alwaysCc || []).forEach(function (a) {
      if (isEmail(a)) list.push(String(a).toLowerCase());
    });
    return list;
  }

  function isOurs(addr) {
    if (!addr) return false;
    return ourInboxes().indexOf(String(addr).toLowerCase()) > -1;
  }

  /* The relay to use for a message addressed to one of our own
     inboxes: free, uncapped, and able to honour a recipient.
     Returns null if none is usable right now, in which case the
     caller falls through to the normal chain — a preference is a
     preference, never a requirement, and mail must never be lost
     because the cheap route is unavailable. */
  function ownInboxRelay() {
    return chain().filter(function (p) {
      return !p.metered && !p.ignoresRecipient;
    })[0] || null;
  }

  /* postOwn(to, payload) — post to an address WE own, preferring
     the free relay. Falls back to post() untouched. Every retry,
     timeout, throttle and quota rule stays in post(). */
  function postOwn(to, payload) {
    /* A payload carrying a _cc still has to go somewhere that can
       CC; pick() knows that rule, so do not override it here. The
       free relay can CC anyway, but that is its property to
       declare, not ours to assume. */
    var free = ownInboxRelay();
    if (!free) return post(to, payload);
    if (payload && payload._cc && free.cannotCC) return post(to, payload);
    return postVia(free, to, payload);
  }

  /* Can any usable relay deliver a CC at all right now? The
     confirmation screen asks, so it can tell the truth about
     whether the student's copy went out. */
  function ccPossible() {
    return chain().some(function (p) { return !p.cannotCC; });
  }

  /* =========================================================
     PROVIDER CHOICE, AND THE QUOTA FALLBACK  (v54)
     ---------------------------------------------------------
     Web3Forms' free tier is 250 emails a month. One booking sends
     three (tutor, EkGuru, student receipt), so the ceiling is
     roughly 83 bookings a month — far more than four tutors will
     see, but not infinite.

     THE QUESTION THAT PROMPTED THIS: "limit reach karne pr
     automatic change ho jayega na?" The answer, before this
     change, was NO. useWeb3Forms() returned true whenever a key
     existed, so once the quota ran out every send would fail and
     the student would be told their booking could not be sent —
     with a perfectly good FormSubmit path sitting unused.

     Now: the first time Web3Forms refuses for a quota reason we
     record it and switch to FormSubmit for the rest of the month.
     The only visible difference is that their footer comes back.
     A booking is never lost because of a billing limit.

     The flag is stored per-month, so it clears itself on the 1st
     without anyone having to remember. It lives in localStorage,
     which means it is per-browser — imperfect, but a static site
     has nowhere else to put it, and the worst case is one extra
     failed attempt per visitor rather than a lost booking.
     ========================================================= */
  /* v55: the quota store is now PER PROVIDER, because there is more
     than one metered relay in the chain. It was a single flag when
     only Web3Forms had a limit.

     Stored as "<provider>:<year>-<month>", so a spent provider frees
     itself on the 1st with nobody having to remember. localStorage
     means it is per-browser — imperfect, but a static site has
     nowhere else, and the worst case is one wasted attempt per
     visitor rather than a lost booking. */
  var QUOTA_KEY = "ekguru_mail_quota_v2";

  function thisMonth() {
    var d = new Date();
    return d.getUTCFullYear() + "-" + (d.getUTCMonth() + 1);
  }
  function quotaMap() {
    try { return JSON.parse(localStorage.getItem(QUOTA_KEY) || "{}") || {}; }
    catch (e) { return {}; }
  }
  function spent(id) {
    return quotaMap()[id] === thisMonth();
  }
  function markSpent(id, label) {
    try {
      var m = quotaMap();
      m[id] = thisMonth();
      localStorage.setItem(QUOTA_KEY, JSON.stringify(m));
      if (window.console && console.warn) {
        console.warn("[EkGuru] " + (label || id) + " has hit its monthly limit. " +
          "Falling back to the next provider until the 1st. No booking is lost.");
      }
    } catch (e) {}
  }
  /* Exposed so the dashboard can show the real state, and so you can
     clear it by hand after upgrading mid-month. */
  /* =========================================================
     BUG FOUND v87 — quotaState() WENT BLIND WHEN KEYS BECAME
     PER-KEY, AND IT WENT BLIND SILENTLY
     ---------------------------------------------------------
     Two faults, both introduced by multi-key support, both
     caught by tools/test-integrations.js:

       "the spent relay is recorded"   FAIL  spent: []
       "provider() now reports the fallback"  FAIL  StaticForms

     FAULT 1 — SPENT WAS ONLY EVER CHECKED PROVIDER-WIDE.
     It read m[p.id]. v87 stopped writing that key: an exhausted
     Web3Forms account is now recorded as "web3forms:<key>" so
     one dead key does not retire two live ones. So the map had
     the information and this function was looking in the wrong
     place. It reported an exhausted relay as available and the
     dashboard said everything was fine.

     FAULT 2 — enabled() NOW RETURNS FALSE WHEN EVERY KEY IS
     SPENT, and the `if (!p.enabled()) return` above then skipped
     the provider entirely. So a relay that had just burned
     through all its quota vanished from BOTH lists rather than
     appearing in `spent`. The dashboard could not tell "out of
     quota" apart from "never configured" — which is precisely
     the distinction v54 added this function to make.

     The fix separates the three states that actually exist and
     that the dashboard needs to tell apart:

       not configured  no key at all — nothing to report
       spent           configured, but nothing left this month
       available       configured and usable right now

     A provider is spent when it is marked spent as a whole OR
     when it has keys and every one of them is spent. Asking
     `configured` rather than `enabled` is what keeps an
     exhausted relay visible.
     ========================================================= */
  function quotaState() {
    var m = quotaMap(), out = { month: thisMonth(), spent: [], available: [] };
    PROVIDERS.forEach(function (p) {
      var keys = p.keys ? p.keys() : null;

      /* Configured means "a key exists", not "a key is usable".
         enabled() means the second thing, and using it here is
         what made an exhausted relay disappear. */
      var configured = keys ? keys.length > 0 : p.enabled();
      if (!configured) return;

      var providerSpent = m[p.id] === out.month;
      var allKeysSpent = keys && keys.length > 0 && keys.every(function (k) {
        return spent(p.id + ":" + k);
      });

      (providerSpent || allKeysSpent ? out.spent : out.available).push(p.label);
    });
    out.exhausted = out.available.length === 0;
    return out;
  }
  function clearQuota() {
    try { localStorage.removeItem(QUOTA_KEY); } catch (e) {}
  }

  function hasWeb3Key() {
    return !!(CFG.web3formsKey && String(CFG.web3formsKey).trim());
  }
  /* Kept for the existing call sites and tests. It now means
     "is Web3Forms the provider that would be used right now",
     which is the same question it always answered. */
  function useWeb3Forms() {
    var c = chain();
    return c.length > 0 && c[0].id === "web3forms";
  }

  /* An "email link" alias looks like a short word, e.g. "yuxuse",
     and lives under a different path: /ajax/el/<alias> rather than
     /ajax/<address>. Detect which one we were given.

     ⚠️ Tested 08/09/2026: the /el/ alias endpoint replies with an
     empty {"message":""} instead of {"success":"true"} and the
     submission does NOT appear in the archive. The plain address
     endpoint answers {"success":"true"} and does deliver. So the
     alias is not used for sending — see ALIAS NOTE in
     tools/mail-activate.html. This helper exists so the code is
     ready if FormSubmit fixes it. */
  function isAlias(v) {
    return !!v && v.indexOf("@") === -1 && /^[a-z0-9]{4,20}$/i.test(v);
  }
  function endpointFor(target) {
    return isAlias(target)
      ? "https://formsubmit.co/ajax/el/" + encodeURIComponent(target)
      : ENDPOINT + encodeURIComponent(target);
  }

  function isEmail(v) {
    return !!v && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(v).trim());
  }

  /* Where the tutor's copy should go.
     A tutor file may set  formKey: "abc123..."  to use a hidden
     alias instead of publishing their raw address. If they have
     not, we use their email. If they have neither, EkGuru's
     address is used so a request is never simply lost.          */
  function tutorTarget(tutor) {
    if (tutor && tutor.formKey) return String(tutor.formKey).trim();
    if (tutor && isEmail(tutor.email)) return String(tutor.email).trim();
    if (CFG.siteKey) return String(CFG.siteKey).trim();
    return isEmail(SITE.email) ? SITE.email : "";
  }

  /* Everyone who should receive a copy, minus the main recipient
     so nobody is mailed twice.                                   */
  function copyList(tutor, studentEmail) {
    var main = tutorTarget(tutor).toLowerCase();
    var out = [];

    if (CFG.copyToSite !== false && isEmail(SITE.email) &&
        SITE.email.toLowerCase() !== main) out.push(SITE.email);

    if (CFG.copyToStudent !== false && isEmail(studentEmail) &&
        studentEmail.toLowerCase() !== main) out.push(studentEmail);

    /* Any extra addresses you want on every booking — an ops
       inbox, a co-founder, a spreadsheet-by-email service.
       js/site-config.js  →  mail: { alwaysCc: ["x@y.com"] }     */
    (CFG.alwaysCc || []).forEach(function (e) {
      if (isEmail(e) && e.toLowerCase() !== main) out.push(e);
    });

    /* de-duplicate, case-insensitively */
    var seen = {}, uniq = [];
    out.forEach(function (e) {
      var k = e.toLowerCase();
      if (!seen[k]) { seen[k] = 1; uniq.push(e); }
    });
    return uniq;
  }


  /* =========================================================
     post() — ONE request to ONE recipient, at MODULE scope   (v78)
     ---------------------------------------------------------
     WHY IT MOVED.

     Until v78 this function was declared INSIDE Mail.send(), so
     the only thing on the whole site that could use the provider
     chain — with its quota fallback, its throttle detection and
     its retry/backoff — was a booking. Everything else (the
     admin composer, and now the contact form) had to hand-roll
     its own fetch, and every hand-rolled copy drifted: compose()
     still only knows about Web3Forms and FormSubmit, and had no
     retry at all.

     Hoisting it here is a pure move — the body is unchanged —
     and it means the contact form gets, for free:

       · quota fallback between providers
       · the FormSubmit throttle workaround (its throttle reply
         is worded identically to its file:// error, see below)
       · 3 retries with backoff, and a 15s abort

     Do NOT put this back inside send(). A second copy of retry
     logic is a second place for it to be wrong.
     ========================================================= */
  /* ---------------------------------------------------------
     Send each copy as its OWN request.
     ---------------------------------------------------------
     One request per recipient, with no CC field anywhere. That
     is what keeps the three audiences separate: nobody's address
     appears in anyone else's headers, and each person receives
     only the version written for them.
     --------------------------------------------------------- */
  /* postVia(provider, to, payload) — force ONE relay, keeping every
     retry, timeout, throttle and quota rule that post() already has.
     A second copy of that logic is a second place for it to be
     wrong, which is why this is a parameter and not a new function
     body. post(to, payload) is simply postVia(null, ...). */
  function postVia(forced, to, payload, attempt) {
    return post(to, payload, attempt, forced);
  }

  function post(to, payload, attempt, forced) {
    attempt = attempt || 0;
    var ctrl = null, timer = null;
    try { ctrl = new AbortController(); } catch (e) {}
    if (ctrl) timer = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, 15000);

    /* v55: the provider is whichever is first in the chain right
       now. Captured here, before the request, because the
       response handler may mark it spent — asking again down
       there would give the wrong answer.

       v79: chosen for THIS payload rather than for the site. A
       message carrying a _cc must go to a relay that can actually
       deliver one, or the CC'd person is silently dropped and the
       relay still answers success. That is the bug that hid the
       student's receipt for months. */
    var active = forced || pick(payload);

    /* =========================================================
       v86 — THE LAST LINE OF DEFENCE
       ---------------------------------------------------------
       Every KNOWN caller that mails our own inbox now goes through
       postOwn(). This catches the one that gets added next year and
       forgets. If nobody forced a provider, the chosen one is
       metered, the recipient is an address we own, and a free relay
       that honours recipients is available — switch. Nothing about
       the message changes; only who carries it.

       It is deliberately NOT applied when `forced` is set: a caller
       that names a relay has a reason (compose() must avoid a relay
       that ignores the recipient), and silently overriding an
       explicit choice is how you get a bug nobody can find.
       ========================================================= */
    if (!forced && active && active.metered && isOurs(to)) {
      var freeRoute = ownInboxRelay();
      if (freeRoute && !(payload && payload._cc && freeRoute.cannotCC)) {
        active = freeRoute;
      }
    }

    if (!active) {
      /* pick() returns null only when a CC is required and no
         usable relay can do it. Rather than send it anyway and
         lose the recipient in silence, say so — send() catches
         this and posts the person their own separate message. */
      return Promise.resolve({
        to: to, ok: false, needsSplit: true,
        ccTarget: payload._cc,
        payload: payload,
        error: "No available relay can deliver a copy to a second address."
      });
    }
    var built = active.build(to, payload);
    var url = built.url, body = built.body;
    var usedW3F = active.id === "web3forms";
    /* v87 — WHICH KEY, not just which provider. Web3Forms can hold
       several access keys, each with its own 250/month. A quota
       refusal must retire ONE key, not the whole relay, or two
       perfectly good keys are thrown away with the exhausted one. */
    var usedKey = built.key || null;

    /* ⚠️ v96 — THE CONTENT TYPE IS THE RELAY'S PROPERTY, NOT OURS.

       This line was hardcoded to application/json for five
       versions and it was right for all four relays that existed
       then. It is WRONG for a Google Apps Script Web App, and
       wrong in the most expensive way: an application/json POST
       is a "non-simple" request, so the browser fires an OPTIONS
       preflight first. Apps Script Web Apps do not answer OPTIONS
       at all. The preflight fails, the real POST is never sent,
       and the console reports a CORS error that looks exactly
       like a broken script or a bad deployment.

       Sending the same JSON as text/plain makes the request
       simple, no preflight happens, and doPost() JSON.parses it
       on the other side. Declared per provider so the next relay
       with its own wire format needs no edit here — the same rule
       that cannotCC and canAddressStrangers already follow, and
       the same lesson this project has now learned sixteen times:
       a value that belongs to one provider must not be written
       into shared logic. */
    var ctype = active.contentType || "application/json";
    var headers = { "Content-Type": ctype };
    /* Only ask for JSON back when we are speaking JSON. Adding an
       Accept header to a text/plain POST re-triggers the preflight
       we just went to the trouble of avoiding — Accept is only a
       "simple" header for a narrow set of values, and
       application/json is not one of them. */
    if (ctype.indexOf("json") > -1) headers["Accept"] = "application/json";

    return fetch(url, {
      method: "POST",
      headers: headers,
      redirect: active.redirect || "follow",
      body: JSON.stringify(body),
      signal: ctrl ? ctrl.signal : undefined
    }).then(function (res) {
      if (timer) clearTimeout(timer);
      /* ⚠️ v95 — NOT EVERY RELAY ANSWERS IN JSON.
         EmailJS returns the plain text "OK" with HTTP 200. Calling
         res.json() on that throws, the catch turns it into {}, and
         {} has no success field — so a delivered email would have
         been reported as a failure, and the chain would have moved
         on and sent it AGAIN through the next relay.

         A relay that answers success while we read it as failure is
         the mirror of the v79 Web3Forms CC bug, and it produces
         duplicate mail rather than missing mail. Read the body as
         text first, then try to parse it. */
      /* ⚠️ v95 — READ THE BODY IN WHICHEVER WAY THIS RESPONSE
         SUPPORTS, NOT THE WAY THE NEWEST RELAY HAPPENS TO NEED.

         The first version of this called res.text() only. That is
         correct for EmailJS, which answers the plain string "OK",
         and it broke everything else: several test stubs — and
         any Response-like object that implements json() but not
         text() — threw, the catch turned it into {}, and a
         DELIVERED email was read as a failure.

         The damage was not "a message went missing". It was
         worse: post() saw a failure, retried, and the tutor got
         the SAME booking twice while the student got nothing.
         Reproduced by tools/test-delivery.js within minutes —
         "shared inbox not mailed twice :: 2".

         That is the mirror of the v79 Web3Forms CC bug. There a
         relay reported success while dropping a recipient; here
         we reported failure on a success and sent it again.
         Duplicate mail is the failure mode people notice, and
         the one that makes a booking look broken.

         So: prefer text() when it exists, fall back to json(),
         and treat an unreadable body as empty rather than as an
         error. Every relay's success is then recognised whatever
         shape it arrives in. */
      var readBody = typeof res.text === "function"
        ? res.text().then(function (raw) {
            var parsed = {};
            try { parsed = JSON.parse(raw); } catch (e) { parsed = {}; }
            /* EmailJS: HTTP 200 with the literal body "OK". */
            if (res.ok && typeof raw === "string" &&
                raw.trim().toUpperCase() === "OK") {
              parsed = { success: "true" };
            }
            return parsed;
          })
        : (typeof res.json === "function" ? res.json() : Promise.resolve({}));

      return readBody.catch(function () { return {}; }).then(function (json) {
        /* Only an explicit success counts. The alias endpoint
           returns {"message":""} with no success field and drops
           the submission, so an empty reply is never "sent".
           FormSubmit answers success:"true" as a string,
           Web3Forms answers success:true as a boolean. */
        /* v81 — carry the CC back to the caller. Without it, send()
           cannot tell a receipt that reached the student as a CC
           from one that failed, and the confirmation screen would
           claim an email that never arrived. */
        if (res.ok && json && String(json.success) === "true") {
          return { to: to, ok: true, ccTo: payload._cc || null };
        }

        var why = (json && json.message) ? json.message :
          "The mail relay gave no confirmation.";

        /* =========================================================
           THE MISLEADING THROTTLE MESSAGE
           ---------------------------------------------------------
           When FormSubmit throttles a burst it does NOT say so. It
           replies:

             "Make sure you open this page through a web server,
              FormSubmit will not work in pages browsed as HTML files"

           which is the same message it sends a genuine file:// page.
           Measured 08/09/2026: 12 requests fired at once, all 12 came
           back with that text; the same requests sent one at a time
           all succeeded.

           A real booking sends two or three emails together, which is
           enough to trip it. That is what produced "We could not send
           that just now" on a booking that was otherwise perfectly
           fine.

           So: if we are plainly not on file://, treat that message as
           a throttle and retry with a short backoff rather than
           telling the student their booking failed.
           ========================================================= */
        /* A Web3Forms quota refusal. Their wording has varied, so
           match the concepts rather than one exact sentence:
           "limit", "quota", "upgrade", "plan". Only treated as a
           quota problem when Web3Forms was actually the provider
           for THIS request — FormSubmit's throttle text also
           contains the word "limit". */
        /* A quota refusal from whichever relay just answered.
           Wording varies between providers, so match the concepts
           rather than one sentence. Only a metered provider can
           hit a quota — FormSubmit's throttle text also contains
           the word "limit", which is why the branded floor of the
           chain is excluded. */
        var quotaHit = active.id !== "formsubmit" &&
          /quota|limit exceeded|monthly limit|upgrade|pro plan|submission limit|exceeded/i.test(why);

        /* v94 — AN INVALID KEY IS ALSO A DEAD KEY.
           The quota test above catches "you have used your 250".
           It does not catch "this key is not real", which is a
           different message and was falling straight through to
           a hard failure — the send died instead of moving to
           the next key.

           keys() now rejects a non-UUID before it is ever tried,
           so this should be unreachable. It stays because a key
           can also be REVOKED at the provider, which produces
           the same answer and must behave the same way: retire
           it, move on, never lose the message. */
        var authDead = active.id !== "formsubmit" &&
          /invalid access key|invalid api key|access key.*invalid|unauthorized|forbidden/i.test(why);
        if (authDead) quotaHit = true;

        if (quotaHit) {
          if (usedKey) {
            /* Retire this KEY. The provider stays in the chain
               while any of its other keys are unspent — enabled()
               asks activeKey(), so the next attempt picks up the
               next key with no other change. */
            markSpent(active.id + ":" + usedKey,
              active.label + " key ..." + String(usedKey).slice(-6));
          } else {
            markSpent(active.id, active.label);
          }
          /* Do not fail. Send the SAME message again immediately;
             chain() will now pick the next provider — or the next
             KEY on the same provider — because this one is marked
             spent. The student sees nothing.

             ⚠️ v95 — THE RETRY BUDGET WAS COUNTED IN PROVIDERS,
             NOT IN ATTEMPTS THAT CAN ACTUALLY SUCCEED.

             It was PROVIDERS.length + 1, which was 4. That was
             fine when Web3Forms had one key. With five keys and
             four providers the real number of distinct routes is
             nine, so the budget ran out on the fifth try and the
             send failed while three good keys and EmailJS were
             still untouched.

             Reproduced: all five Web3Forms keys spent, EmailJS
             configured and working, and compose() still threw
             "monthly submission limit" — it never reached EmailJS.

             Count the routes that exist instead: every provider,
             plus one per extra key it holds. */
          var routes = 0;
          PROVIDERS.forEach(function (p) {
            routes += p.keys ? Math.max(1, p.keys().length) : 1;
          });
          if (attempt < routes + 1) return post(to, payload, attempt + 1, forced);
        }

        var throttled = /web server/i.test(why) &&
                        location && location.protocol !== "file:";
        var rateLimited = /rate limit|too many/i.test(why);

        if ((throttled || rateLimited) && attempt < 3) {
          var wait = 700 * Math.pow(2, attempt);   /* 700ms, 1.4s, 2.8s */
          return new Promise(function (r) { setTimeout(r, wait); })
            .then(function () { return post(to, payload, attempt + 1, forced); });
        }

        if (throttled) {
          why = "The mail service is busy. Please try again in a minute.";
        }
        return { to: to, ok: false, error: why };
      });
    }).catch(function (err) {
      if (timer) clearTimeout(timer);
      var msg = err && err.message ? err.message : String(err);
      /* A dropped connection is worth one retry too. */
      if (attempt < 2 && !/abort/i.test(msg)) {
        return new Promise(function (r) { setTimeout(r, 800 * (attempt + 1)); })
          .then(function () { return post(to, payload, attempt + 1, forced); });
      }
      return { to: to, ok: false, error: msg };
    });
  }


  var Mail = {

    /* Is real sending switched on and usable in this browser? */
    available: function () {
      return CFG.enabled !== false &&
             typeof window.fetch === "function" &&
             !!tutorTarget(null);
    },

    /* Who would be mailed — used by the confirmation screen so
       the student can see exactly where their request went.     */
    recipients: function (tutor, studentEmail) {
      return {
        to: tutorTarget(tutor),
        cc: copyList(tutor, studentEmail)
      };
    },

    /* ---------------------------------------------------------
       send(data) -> Promise
       data = {
         tutor,          the tutor object
         name,           student's name
         email,          student's email
         level, timezone, goal,
         slot,           chosen time, already formatted
         price,          "$8" or "$8 (about ₹664)"
         message,        the full plain-text message
         pageUrl         which page they booked from
       }
       Resolves on success, rejects with an Error otherwise.
       --------------------------------------------------------- */
    send: function (data) {
      var tutor = data.tutor || {};
      var target = tutorTarget(tutor);

      if (CFG.enabled === false) {
        return Promise.reject(new Error("Mail sending is switched off in site-config.js"));
      }
      if (!target) {
        return Promise.reject(new Error("No recipient address configured"));
      }
      if (typeof window.fetch !== "function") {
        return Promise.reject(new Error("This browser cannot send in the background"));
      }

      var cc = copyList(tutor, data.email);

      /* Every key below becomes a labelled row in the email the
         tutor receives, in this order. Rename a key and the label
         in the email changes with it.                            */
      /* =========================================================
         THREE AUDIENCES, THREE DIFFERENT EMAILS
         ---------------------------------------------------------
         This used to be ONE email CC'd to all three people, which
         meant the student received the tutor's full working copy:
         the tutor's private inbox address, the platform notes, the
         internal distribution list. That is a privacy problem, and
         it is not information a student needs.

         Now each recipient gets a message written for them, and
         each is sent separately so no address is disclosed to
         anyone else. No CC is used anywhere.

           TUTOR     everything they need to teach and reply —
                     the student's name, email, level, goal, the
                     requested time. This is the working copy.

           EKGURU    everything, plus the operational detail: which
                     page it came from, the distribution list, the
                     tutor's inbox. This is the record.

           STUDENT   only what is theirs: their reference, who they
                     booked, when, what it costs, what happens next.
                     They do NOT see the tutor's private inbox, nor
                     any internal note.

         The reference is identical in all three, so any of you can
         match them up without any of you seeing the others' detail.
         ========================================================= */
      var now = new Date();
      var ref = data.ref || "";
      var lesson = tutor.lessonLength || "50 min";
      var when = data.slot || "a time still to be agreed";
      var studentName = data.name || "A student";
      var tutorName = tutor.name || "the tutor";
      var brand = SITE.brand || "EkGuru";

      /* Who is actually being written to, kept private per copy. */
      /* Our own sign-off, on every email. FormSubmit adds theirs
         underneath on the free tier; with a Web3Forms key set, this
         is the only footer the reader sees. */
      var founder = (SITE.founder && SITE.founder.name) || "Prakash";
      var signOff =
        (SITE.brand || "EkGuru") + " — " + (SITE.tagline || "") + "\n" +
        (SITE.baseUrl || "") + "\n" +
        founder + ", founder" +
        ((SITE.founder && SITE.founder.linkedin) ? " — " + SITE.founder.linkedin : "") + "\n" +
        (SITE.email || "");

      var studentLine = studentName + (data.email ? " <" + data.email + ">" : "");
      var tutorLine = tutorName + (target.indexOf("@") > -1 ? " <" + target + ">" : "");

      var copies = cc.map(function (a) {
        if (data.email && a.toLowerCase() === String(data.email).toLowerCase())
          return studentName + " <" + a + "> (their own copy)";
        if (SITE.email && a.toLowerCase() === String(SITE.email).toLowerCase())
          return brand + " <" + a + "> (platform copy)";
        return a;
      });

      /* ---------- 1. THE TUTOR'S COPY — the working copy ---------- */
      function tutorBody() {
        return {
          _subject: "Booking request " + ref + " — " + studentName +
                    (data.slot ? " — " + data.slot : ""),
          _template: "table",
          _captcha: "false",

          "Reference": ref || "(none)",
          "WHO SENT THIS": studentLine,
          "SENT TO": "you",
          "WHAT WAS REQUESTED": "A " + lesson + " Hindi lesson with you at " +
                    when + " for " + (data.price || "the listed price"),
          "SENT WHEN": now.toUTCString() +
                    (data.timezone ? "   (student's timezone: " + data.timezone + ")" : ""),

          "Student name": studentName,
          "Student email": data.email || "",
          "Student level": data.level || "",
          "Student timezone": data.timezone || "",
          "Student goal": data.goal || "",
          "Requested time": when,
          "Lesson": lesson + " · " + (data.price || ""),
          "Full message": data.message || "",

          "What happens next":
            "Reply to " + (data.email || "the student") + " to confirm the time. " +
            brand + " keeps a copy for its records. Quote reference " +
            (ref || "above") + " in any reply.",

          "—": signOff,

          /* Reply goes straight back to the student */
          email: data.email || SITE.email || ""
        };
      }

      /* ---------- 2. EKGURU'S COPY — the full record ---------- */
      function siteBody() {
        return {
          _subject: "[record] " + ref + " — " + studentName + " → " + tutorName +
                    (data.slot ? " — " + data.slot : ""),
          _template: "table",
          _captcha: "false",

          "Reference": ref || "(none)",
          "WHO SENT THIS": studentLine,
          "SENT TO": tutorLine,
          "COPIES SENT SEPARATELY TO": copies.length ? copies.join("  |  ") : "(none)",
          "WHAT WAS REQUESTED": "A " + lesson + " Hindi lesson with " + tutorName +
                    " at " + when + " for " + (data.price || "the listed price"),
          "SENT WHEN": now.toUTCString() +
                    (data.timezone ? "   (student's timezone: " + data.timezone + ")" : ""),

          "Tutor": tutorName,
          "Tutor inbox": target,
          "Student name": studentName,
          "Student email": data.email || "",
          "Student level": data.level || "",
          "Student timezone": data.timezone || "",
          "Student goal": data.goal || "",
          "Requested time": when,
          "Lesson": lesson + " · " + (data.price || ""),
          "Booked from": data.pageUrl || (location && location.href) || "",
          "Sent via": brand + " booking form — " + (SITE.baseUrl || ""),
          "Full message": data.message || "",
          "—": signOff,

          email: data.email || SITE.email || ""
        };
      }

      /* ---------- 3. THE STUDENT'S RECEIPT — only what is theirs ----------
         Deliberately omits: the tutor's inbox address, the page URL,
         the distribution list, and every internal note. A student
         has no need for any of it, and publishing a tutor's private
         address to every person who books is not acceptable. */
      function studentBody() {
        return {
          _subject: "Your booking request " + ref + " with " + tutorName +
                    (data.slot ? " — " + data.slot : ""),
          _template: "table",
          _captcha: "false",

          "Your reference": ref || "(none)",
          "You booked": tutorName,
          "You asked for": "A " + lesson + " Hindi lesson at " + when +
                    " for " + (data.price || "the listed price"),
          "You sent it": now.toUTCString(),
          "Your name": studentName,
          "Your email": data.email || "",
          "Your level": data.level || "",
          "Your goal": data.goal || "",

          "What happens next":
            tutorName + " has your request and will reply to this address to " +
            "confirm the time. This is a request, not a confirmed booking. " +
            "If you hear nothing within a day, check your spam folder or write " +
            "to " + (SITE.email || "us") + " quoting " + (ref || "your reference") + ".",

          "—": signOff,

          /* Replies from the student come to EkGuru, not to the tutor's
             private inbox, so the address is never disclosed. */
          email: SITE.email || ""
        };
      }

      /* post() now lives at module scope — see the note above it. */

      /* =========================================================
         WHY THE STUDENT'S COPY IS A CC AND NOT ITS OWN REQUEST
         ---------------------------------------------------------
         v32 posted a separate request to the student's address so
         each audience got its own message. That was wrong, and it
         broke real bookings.

         FormSubmit will not send to an address until the OWNER of
         that address has clicked an "Activate Form" link. That is
         fine for our two fixed inboxes — they are activated once
         and never again. But a student is a stranger whose address
         we have never seen before. Posting to it made FormSubmit
         email THEM an activation link instead of their receipt, and
         demand they authorise a service they have never heard of.

         Verified 08/09/2026 against two unseen addresses:
             POST /ajax/somerandomstudent99@gmail.com
             -> "This form needs Activation..."
         Every single student would have hit this. No receipt would
         ever have arrived.

         The _cc field has no such requirement: it rides along on a
         message sent to an already-activated inbox. So the student
         is CC'd on their own receipt, which is sent TO our own
         activated address.

         Privacy is still preserved, because the receipt they are
         copied on is the student-safe body — it carries no tutor
         inbox, no page URL and no internal notes. That was the
         actual point of v32 and it is unchanged.
         ========================================================= */

      var ourInbox = (CFG.siteKey || SITE.email);
      var targetIsUs = isEmail(SITE.email) &&
                       SITE.email.toLowerCase() === String(target).toLowerCase();

      /* When a tutor has not yet given us a personal address, their
         bookings come to our inbox — so `target` and our inbox are
         the same place. Sending both the tutor copy and the record
         would arrive as two near-identical emails.

         Hemlata's booking showed the other half of this: you saw
         the tutor's working copy, not the operational record, so
         the page URL and the distribution list were missing. The
         record is the more complete of the two, so when they are
         the same inbox we send THAT one, once.

         The tutor copy is the primary either way: if it fails the
         booking failed. */
      /* v86 — anything addressed to an inbox WE own goes through
         the free unlimited relay, not the metered one. See
         ownInboxRelay(). `targetIsUs` is exactly the case where a
         tutor has no personal address yet, which is 3 of our 4
         tutors, so this is the common path, not the edge case. */
      var jobs = [function () {
        return targetIsUs
          ? postOwn(target, siteBody())      /* our inbox — free relay */
          : post(target, tutorBody());       /* a real tutor address   */
      }];

      if (CFG.copyToSite !== false && isEmail(SITE.email) && !targetIsUs) {
        /* THE RECORD. Prakash: "record wali free wale se hi aani
           chahiye." It is addressed to us, so it costs nothing. */
        jobs.push(function () { return postOwn(ourInbox, siteBody()); });
      }

      /* =========================================================
         v81 — THE STUDENT'S RECEIPT IS ADDRESSED TO THE STUDENT
         ---------------------------------------------------------
         Prakash: "sabhi ke liye fix karo."

         He asked for the contact form's copy to go to the sender
         rather than arriving in our inbox as a CC. The booking
         receipt had exactly the same shape and the same problem,
         so it gets exactly the same fix — one rule, both flows,
         rather than the contact form quietly behaving better than
         the booking form.

         WAS:  post → EkGuruLearning@gmail.com,  CC: the student
               subject "[student copy] ..."
               Delivered to US. The student saw it only because
               they were CC'd on a message addressed to somebody
               else, which threads oddly and trips some spam
               filters.

         NOW:  post → the student, addressed TO them, no CC.
               Nothing about our inbox is in their headers.

         WHY IT COULD NOT BE DONE BEFORE, AND CAN NOW
         FormSubmit refuses any recipient whose owner has not
         clicked an activation link, and a student is by definition
         an address we have never mailed. Re-probed against the
         live endpoint on 10 Sep 2026 with a browser Origin header:

           POST /ajax/never-a-real-person@example.com
           → {"success":"false","message":"This form needs Activation..."}

         Web3Forms has no such step — the ACCOUNT is verified by
         the access key, not the recipient. So the receipt goes
         there, chosen by the canAddressStrangers capability rather
         than by a hardcoded provider name.

         The fallback is the old path, unchanged: if Web3Forms is
         spent for the month or unconfigured, the receipt reverts
         to our inbox with the student CC'd. Worse, but never lost. */
      var studentTo = (CFG.copyToStudent !== false && isEmail(data.email) &&
                       String(data.email).toLowerCase() !== String(target).toLowerCase())
                       ? data.email : null;

      if (studentTo) {
        jobs.push(function () {
          var direct = PROVIDERS.filter(function (p) {
            return p.enabled() && !spent(p.id) && p.canAddressStrangers;
          })[0];

          if (direct) {
            /* Their own message. The "[student copy]" prefix is
               dropped: it existed only to distinguish the message
               in OUR inbox, and it is meaningless — faintly
               insulting, even — on the copy the student receives. */
            return postVia(direct, studentTo, studentBody());
          }

          /* No relay can reach a stranger. Old path. */
          if (!isEmail(SITE.email)) return Promise.resolve({ to: studentTo, ok: false,
            error: "No configured route to the student" });
          var receipt = studentBody();
          receipt._cc = studentTo;
          receipt._subject = "[student copy] " + receipt._subject;
          /* Addressed to us, CC'd to them. Ours, so free relay —
             and the free relay is also the only one that can
             actually deliver the CC. Both rules point the same way. */
          return postOwn(ourInbox, receipt);
        });
      }

      /* Any extra operational inboxes get the full record. These are
         addresses you control, so you can activate them once. */
      (CFG.alwaysCc || []).forEach(function (extra) {
        if (isEmail(extra) && extra.toLowerCase() !== String(target).toLowerCase()) {
          /* These are addresses YOU control and activated, so they
             are ours and they are free. */
          jobs.push(function () { return postOwn(extra, siteBody()); });
        }
      });

      /* =========================================================
         ONE AT A TIME, NOT ALL AT ONCE
         ---------------------------------------------------------
         Promise.all fired every email simultaneously, which is
         exactly the burst that trips FormSubmit's throttle. Running
         them in sequence with a small gap costs the student about
         half a second and removes the failure entirely.
         ========================================================= */
      function runSequential(list, i, out) {
        i = i || 0; out = out || [];
        if (i >= list.length) return Promise.resolve(out);
        return list[i]().then(function (r) {
          /* v79 — THE CC FALLBACK.
             post() returns needsSplit when the message required a
             CC and no usable relay could deliver one. Rather than
             drop that person in silence — which is precisely the
             bug that hid the student's receipt — send them their
             own message directly. It is a worse path (a stranger's
             address may not be activated with FormSubmit) but a
             visible one: if it fails, it fails loudly and lands in
             `failed`, instead of reporting success. */
          if (r && r.needsSplit && r.ccTarget) {
            var direct = r.payload || {};
            delete direct._cc;
            return post(r.ccTarget, direct).then(function (r2) {
              out.push(r2);
              if (i + 1 >= list.length) return out;
              return new Promise(function (res) { setTimeout(res, 250); })
                .then(function () { return runSequential(list, i + 1, out); });
            });
          }
          out.push(r);
          if (i + 1 >= list.length) return out;
          return new Promise(function (res) { setTimeout(res, 250); })
            .then(function () { return runSequential(list, i + 1, out); });
        });
      }

      return runSequential(jobs).then(function (results) {
        var primary = results[0];
        if (!primary.ok) throw new Error(primary.error);

        var delivered = results.filter(function (r) { return r.ok; }).map(function (r) { return r.to; });
        var failed = results.filter(function (r) { return !r.ok; });

        return {
          ok: true,
          to: target,
          /* Everyone who actually received something, for the
             confirmation screen and the ledger. The student is a CC
             recipient rather than a POST target, so they have to be
             added explicitly — leaving them out made the receipt say
             "a copy also went to: EkGuru" and omit the student's own
             copy, which was the one they most needed to see. */
          /* Everyone who actually received something, for the
             confirmation screen and the ledger.

             v81: the student is now usually a DIRECT recipient
             rather than a CC, so they appear in `delivered` on
             their own. The old code inferred their presence from
             "did a post to our inbox succeed", which after this
             change would have reported them as having received a
             copy when the direct send had in fact failed — the
             screen lying to a student about an email that never
             arrived. The fallback path still CCs them, so both
             cases are handled explicitly and neither is guessed. */
          cc: (function () {
            var out = [], seenAddr = {};
            delivered.forEach(function (a) {
              if (a === target) return;
              var k = String(a).toLowerCase();
              if (!seenAddr[k]) { seenAddr[k] = 1; out.push(a); }
            });
            /* The CC fallback: the receipt went to our inbox with
               the student CC'd, so they are not in `delivered`
               under their own address. Only claim it if THAT
               specific job succeeded. */
            if (studentTo && !seenAddr[String(studentTo).toLowerCase()]) {
              var ccDelivered = results.some(function (r) {
                return r.ok && r.ccTo &&
                  String(r.ccTo).toLowerCase() === String(studentTo).toLowerCase();
              });
              if (ccDelivered) {
                seenAddr[String(studentTo).toLowerCase()] = 1;
                out.push(studentTo);
              }
            }
            return out;
          })(),
          failed: failed.map(function (r) { return { to: r.to, error: r.error }; }),
          ref: data.ref || "",
          from: studentLine,
          toLabel: tutorLine,
          copies: copies,
          sentAt: now.toISOString(),
          subject: tutorBody()._subject,
          separate: true
        };
      });
    },

    /* =========================================================
       CONTACT — the website's own contact form              (v78)
       ---------------------------------------------------------
       WHAT PRAKASH ASKED FOR

         "ek contact jisme website se hi direct contact kar le,
          direct mail aa jaye static ke through … manually to
          contact form fill kare aur send. Uski mail id, uska
          naam, uska message — jo hum usko reply kar sake."

       So: a real form on the site. Not a mailto:. A mailto: is
       not a contact form — it hands the visitor a job (open a
       mail client, retype everything) and about half of them
       simply leave. Every "tell us" link on the site used to be
       exactly that, on 460 pages.

       WHAT THIS SENDS — TWO EMAILS, DELIBERATELY

         1. TO EKGURU   the message itself, with the sender's name
                        and address in a labelled row AND in the
                        reply-to header, so hitting Reply in Gmail
                        goes straight back to the visitor. That is
                        the whole point of "hum usko reply kar
                        sake" — it must work with one keypress, not
                        with copy-paste.

         2. TO THE VISITOR   a short acknowledgement containing
                        their own reference and a copy of what they
                        wrote. Costs one extra relay call and
                        removes the "did that send?" email that
                        otherwise follows every silent form.

       The acknowledgement is a CC on a post addressed to OUR OWN
       inbox, never a post addressed to the visitor. Same reason
       the booking receipt is: FormSubmit refuses to deliver to an
       address whose owner has not clicked an activation link, and
       a stranger never has. Posting straight at them produced a
       bounce AND an activation email to a person who did not ask
       for one. (Recorded here because it has been rediscovered
       twice.)

       WHY IT IS NOT compose()
       compose() is the admin dashboard's tool: it takes a
       recipient, and it only knows two of the three providers. A
       public form must never take a recipient from the page —
       that is an open relay, and spam bots find those in days.
       contact() has NO recipient parameter at all. It always
       sends to SITE.email (or CFG.siteKey), full stop.

         EkGuruMail.contact({ name, email, subject, message,
                              topic, pageUrl, ref })
       ========================================================= */
    contact: function (data) {
      data = data || {};

      if (CFG.enabled === false) {
        return Promise.reject(new Error("Mail sending is switched off in site-config.js"));
      }
      if (typeof window.fetch !== "function") {
        return Promise.reject(new Error("This browser cannot send in the background"));
      }
      if (!data.name || !String(data.name).trim()) {
        return Promise.reject(new Error("Please tell us your name"));
      }
      if (!isEmail(data.email)) {
        return Promise.reject(new Error("Please enter an email address we can reply to"));
      }
      if (!data.message || String(data.message).trim().length < 10) {
        return Promise.reject(new Error("Please write a little more so we can help"));
      }

      /* The honeypot. A field hidden from people and filled in by
         bots; if it has anything in it we resolve as if we sent,
         so the bot learns nothing, and send nothing at all. */
      if (data.hp && String(data.hp).trim()) {
        return Promise.resolve({ ok: true, ref: data.ref || "", ignored: true });
      }

      var brand = SITE.brand || "EkGuru";
      var ourInbox = (CFG.siteKey && String(CFG.siteKey).trim()) ||
                     (isEmail(SITE.email) ? SITE.email : "");
      if (!ourInbox) {
        return Promise.reject(new Error("No contact address is configured"));
      }

      var now = new Date();
      var ref = data.ref || ("C-" + now.getTime().toString(36).toUpperCase().slice(-6));
      var who = String(data.name).trim();
      var from = String(data.email).trim();
      var topic = String(data.topic || "General").trim();
      var subj = String(data.subject || "").trim() ||
                 (topic + " — message from " + who);
      var body = String(data.message).trim();

      var founder = (SITE.founder && SITE.founder.name) || "Prakash";
      var signOff =
        brand + " — " + (SITE.tagline || "") + "\n" +
        (SITE.baseUrl || "") + "\n" +
        founder + ", founder" +
        ((SITE.founder && SITE.founder.linkedin) ? " — " + SITE.founder.linkedin : "") + "\n" +
        (SITE.email || "");

      /* =========================================================
         v80 — A COMPLAINT ABOUT A TUTOR IS NOT ORDINARY POST
         ---------------------------------------------------------
         Prakash: "student report kar sake … phir hum usko hide
         aur suspend aur delete kar denge."

         A report has to be visible in the inbox at a glance, or
         it sits behind nine questions about prices and is answered
         on Thursday. So the subject is marked, and the marker is
         the first thing in it — Gmail truncates subject lines on a
         phone and the end is what gets cut.

         Derived from a list, not from an `if (topic === "Report")`
         — a hardcoded topic name in logic is the same class of
         bug as a hardcoded provider name, and this project has
         shipped fourteen of those. */
      var URGENT = ["Report", "Privacy"];
      var isUrgent = URGENT.indexOf(topic) > -1;
      var tag = isUrgent ? "[!! " + topic.toUpperCase() + "] " : "[contact] ";

      /* ---------- 1. our copy — the one that must be replyable ---------- */
      var mine = {
        _subject: tag + ref + " — " + topic + " — " + who,
        _template: "table",
        _captcha: "false",

        "Reference": ref,
        "Their name": who,
        "Their email": from,
        "Topic": topic,
        "Subject": subj,
        "Message": body,
        "Sent": now.toUTCString(),
        "Sent from page": data.pageUrl || (typeof location !== "undefined" ? location.href : ""),
        "Their language": data.lang || "",
        "How to answer": "Just press Reply — this email's reply-to is " + from + ".",
        /* Only present when it matters, so it is not noise on the
           other seven topics. */
        "ACTION NEEDED": isUrgent
          ? (topic === "Report"
              ? "This is a report about a tutor or a lesson. Read it today. " +
                "The Tutors tab in the dashboard can hide, suspend or remove a " +
                "tutor immediately — a hidden tutor disappears from the site on " +
                "the visitor's next page load, with no deploy."
              : "This is a privacy or data request. There are legal time limits " +
                "on answering one: 30 days under GDPR.")
          : undefined,
        "—": signOff,

        /* Both relays use `email` as the reply-to. This single line
           is what makes "hum usko reply kar sake" true. It is NOT
           the recipient — the recipient is the URL/access key. A
           previous version set this to SITE.email, which made every
           reply come back to ourselves. */
        email: from
      };

      /* ---------- 2. their acknowledgement ---------- */
      var theirs = {
        _subject: "[copy] We have your message — " + ref,
        _template: "table",
        _captcha: "false",

        "Your reference": ref,
        "We received": now.toUTCString(),
        "You wrote": body,
        "About": topic,
        "What happens next": isUrgent && topic === "Report"
          ? "Thank you for telling us — that took effort and it matters. " +
            "A person is reading this today, not a system. We will reply at " +
            from + ". Nothing you have written is shared with the tutor: we " +
            "look into it ourselves first, and we can remove a tutor from the " +
            "site immediately if we need to. Your reference is " + ref + "."
          : "A person reads every message. You will get a reply at " + from +
            ", usually within a day. If it is urgent, reply to this email and " +
            "quote " + ref + ". This is an acknowledgement, not an answer.",
        "—": signOff,
        _cc: from,
        email: SITE.email || ourInbox
      };

      /* =========================================================
         v79 — CONTACT GOES THROUGH THE FREE UNLIMITED RELAY
         ---------------------------------------------------------
         Prakash: "contact ke liye formsubmit free wala use karo
         jo unlimited hai."

         Both reasons hold:

           VOLUME. A public contact form is the one surface a
           stranger can submit repeatedly. Web3Forms' free tier is
           250 emails a month and every contact costs two. Burning
           a metered relay on unsolicited mail would starve the
           BOOKINGS, which are the ones that earn money.

           CC. The visitor's acknowledgement is a CC, and
           Web3Forms drops CCs on the free plan while answering
           success. pick() already routes any _cc payload away
           from it — the acknowledgement below would go to
           FormSubmit regardless. This makes it explicit for OUR
           copy too, so the whole conversation arrives from one
           sender and threads together in the visitor's client.

         Set mail.contactProvider in js/site-config.js to override.
         Never hardcoded to an id here — a provider name written
         into logic is the fourteen-hardcoded-values problem, and
         a relay that disappears would take the contact form with
         it. Unknown or unavailable value simply falls back to the
         normal chain rather than failing. */
      var wanted = String(CFG.contactProvider || "formsubmit").toLowerCase();
      function preferContact(payload) {
        var p = PROVIDERS.filter(function (x) {
          return x.id === wanted && x.enabled() && !spent(x.id);
        })[0];
        /* Unknown id, disabled, or spent for the month: fall back to
           the normal chain rather than failing. A preference is a
           preference, not a requirement. */
        /* v86: the fallback is postOwn, not post. This address is
           ours, so even when the named preference is unavailable
           the message must not be paid for out of the metered
           quota if a free relay exists. post() only as the floor. */
        if (!p) return postOwn(ourInbox, payload);
        /* v86 — a METERED preference is refused for our own inbox.
           contactProvider is a knob, and a knob set to "web3forms"
           would quietly spend the booking budget on contact-form
           mail addressed to an inbox the free relay reaches for
           nothing. Prakash asked for exactly this: "contact wali
           bhi free wale se". If the preference is free, it is
           honoured; if it is metered and a free route exists, the
           free route wins. */
        if (p.metered && ownInboxRelay()) return postOwn(ourInbox, payload);
        /* postVia keeps every retry, timeout and quota rule in
           post() rather than duplicating them here — a second copy
           of retry logic is a second place for it to be wrong. */
        return postVia(p, ourInbox, payload);
      }

      /* =========================================================
         v81 — THE SENDER'S COPY GOES TO THE SENDER
         ---------------------------------------------------------
         Prakash: "contact karta hai koi to uska dono mere paas hi
         aa raha hai — record aur copy dono EkGuruLearning@gmail.com
         par hi aa raha hai. Isko ek ko EkGuruLearning par aur copy
         sender means contact karne wale ki mail par jana chahiye."

         He is exactly right, and the cause is a design decision
         from v78 that was correct then and is wrong now.

         WHAT WAS HAPPENING
             mail 1  →  EkGuruLearning@gmail.com   (the message)
             mail 2  →  EkGuruLearning@gmail.com   CC: the sender

         Two emails, both DELIVERED to us. The sender only saw
         theirs because they were CC'd — and a CC on a message
         addressed to somebody else is a strange thing to receive.
         In Gmail it threads under our address, and some clients
         file it as spam because the To: header names nobody the
         recipient knows.

         WHY IT WAS BUILT THAT WAY
         FormSubmit refuses to deliver to an address whose owner
         has never clicked an activation link, and a stranger never
         has. Verified again today against the live endpoint, with
         a browser Origin header so it was not the file:// path:

             POST /ajax/never-a-real-person@example.com
             → {"success":"false","message":"This form needs
                Activation. We've sent you an email containing an
                'Activate Form' link."}

         So posting AT the visitor genuinely does not work on
         FormSubmit. That much of the v78 reasoning still holds.

         WHAT CHANGED
         Web3Forms does not have that restriction — it takes a `to`
         and delivers to it, no activation, because the account is
         already verified by the access key. It is metered (250 a
         month) and it cannot CC on the free plan, but a receipt
         addressed to one person needs no CC at all.

         So the two halves of the split are now chosen by what each
         relay can actually do:

             OUR copy      → FormSubmit   free, unlimited, and we
                                          are an activated address
             SENDER's copy → Web3Forms    delivers to a stranger,
                                          addressed TO them

         That is also the answer to the other half of his message —
         "jab tak fallback nahi hoti Web3 wali, tab tak usko use":
         keep using the metered relay where it is the only one that
         works, and fall back to the free one when it runs out.
         chain() already skips a provider marked spent, so if
         Web3Forms hits its 250 the sender's copy reverts to the
         old CC-through-our-inbox path automatically. Degraded, not
         lost — and the student still hears from us.

         ⚠️ DO NOT "simplify" this back to one relay. The two
         messages have genuinely different requirements: ours needs
         unlimited volume, theirs needs delivery to an unverified
         stranger. No single free relay does both.
         ========================================================= */

      /* Which relay can address a stranger directly? A CAPABILITY,
         declared per provider, never a hardcoded id — a provider
         name written into logic is the fourteen-hardcoded-values
         problem this project keeps rediscovering. */
      function directToStranger() {
        return PROVIDERS.filter(function (p) {
          return p.enabled() && !spent(p.id) && p.canAddressStrangers;
        })[0] || null;
      }

      var jobs = [function () { return preferContact(mine); }];

      if (CFG.copyToStudent !== false) {
        jobs.push(function () {
          var direct = directToStranger();

          if (direct) {
            /* Addressed TO them. No CC, so nothing about our inbox
               appears in their headers, and it threads in their
               client as a message from EkGuru — which is what it
               is. */
            var own = {};
            for (var k in theirs) {
              if (k !== "_cc") own[k] = theirs[k];
            }
            /* The subject loses "[copy]": it is not a copy of
               anything from their point of view, it is their
               receipt. The marker existed only because the message
               used to land in OUR inbox and needed distinguishing
               there. */
            own._subject = "We have your message — " + ref;
            return postVia(direct, from, own);
          }

          /* NO relay can reach a stranger right now — Web3Forms
             spent for the month, or no key configured. Fall back to
             the old path rather than dropping the receipt: posted
             to our activated inbox with them CC'd. They still get
             it; it just looks less tidy and costs us a duplicate.
             A worse copy beats no copy. */
          return preferContact(theirs);
        });
      }
      (CFG.alwaysCc || []).forEach(function (extra) {
        if (isEmail(extra) && extra.toLowerCase() !== String(ourInbox).toLowerCase()) {
          jobs.push(function () { return postOwn(extra, mine); });
        }
      });

      /* Sequential, 250ms apart — Promise.all is the exact burst
         that trips FormSubmit's throttle (see post()). */
      function run(list, i, out) {
        i = i || 0; out = out || [];
        if (i >= list.length) return Promise.resolve(out);
        return list[i]().then(function (r) {
          out.push(r);
          if (i + 1 >= list.length) return out;
          return new Promise(function (res) { setTimeout(res, 250); })
            .then(function () { return run(list, i + 1, out); });
        });
      }

      return run(jobs).then(function (results) {
        /* Only the FIRST job matters for success. If our own copy
           arrived, the message is not lost, and a failed
           acknowledgement must never be reported to the visitor as
           a failed message — they would send it again. */
        var primary = results[0];
        if (!primary.ok) throw new Error(primary.error);
        return {
          ok: true,
          ref: ref,
          to: ourInbox,
          acknowledged: !!(results[1] && results[1].ok),
          sentAt: now.toISOString()
        };
      });
    },

    /* A mailto: as the LAST resort — if every relay refuses, the
       visitor still gets their words carried into their own mail
       app instead of losing them. Built here so the form and the
       tests agree on exactly one version of it. */
    contactMailto: function (data) {
      data = data || {};
      var to = isEmail(SITE.email) ? SITE.email : "";
      var lines = [
        "Name: " + (data.name || ""),
        "Email: " + (data.email || ""),
        "Topic: " + (data.topic || "General"),
        "",
        (data.message || ""),
        "",
        "(sent from " + (data.pageUrl || "") + ")"
      ];
      return "mailto:" + to +
        "?subject=" + encodeURIComponent(data.subject || ("Message from " + (data.name || "a visitor"))) +
        "&body=" + encodeURIComponent(lines.join("\n"));
    },

    /* =========================================================
       COMPOSE — send a message from the admin dashboard
       ---------------------------------------------------------
       Write to any tutor, any student, or a typed address,
       without leaving the dashboard and without opening a mail
       client. Uses the same relay as booking emails.

         EkGuruMail.compose({ to, subject, message, replyTo })

       The tutor's address is never shown to the browser doing
       the sending beyond what the dashboard already knows, and
       nothing is stored anywhere.
       ========================================================= */
    compose: function (data) {
      if (CFG.enabled === false) {
        return Promise.reject(new Error("Mail sending is switched off in site-config.js"));
      }
      if (!isEmail(data.to)) return Promise.reject(new Error("A valid recipient is required"));
      if (!data.message || !String(data.message).trim()) {
        return Promise.reject(new Error("The message is empty"));
      }
      if (typeof window.fetch !== "function") {
        return Promise.reject(new Error("This browser cannot send in the background"));
      }

      var brand = SITE.brand || "EkGuru";
      var founder = (SITE.founder && SITE.founder.name) || "Prakash";
      var sign =
        brand + " — " + (SITE.tagline || "") + "\n" +
        (SITE.baseUrl || "") + "\n" +
        founder + ", founder" +
        ((SITE.founder && SITE.founder.linkedin) ? " — " + SITE.founder.linkedin : "") + "\n" +
        (SITE.email || "");

      /* =========================================================
         v80 — TWO BUGS PRAKASH FOUND IN THIS FUNCTION
         ---------------------------------------------------------
         He wrote:

           "jo contact hai vo only record send kar raha hai, to ke
            paas nahi karta sent … aur admin se agar koi mail jati
            hai to vo record nahi aaye, vo to ke paas hi jaye. Only
            record ka kya kaam? Admin to apan hai, apne ko kya
            matlab record se — vo to unke liye hai."

         Both halves are real defects, and they are opposites.

         BUG 1 — THE ADMIN REPLY DID NOT REACH THE PERSON.
         This built a body with a "To" ROW — a line of text inside
         the email saying who it was for — and then posted it
         through whichever relay was first in the chain. With a
         Web3Forms key set, that is Web3Forms, and on the free plan
         Web3Forms delivers to the address the ACCESS KEY is
         registered to. Which is EkGuru's own inbox.

         So pressing "Send reply" in the dashboard produced an
         email addressed to EkGuru, containing a line that said
         "To: student@example.com", and the student got nothing.
         It reported success every time, because the relay
         genuinely did accept and deliver it — to the wrong person.
         Exactly the same shape as the CC bug in v79: a relay
         answering success while dropping the recipient.

         BUG 2 — IT SENT US A COPY WE DID NOT NEED.
         Prakash is right that a "record" of a message HE typed,
         in HIS dashboard, sent to HIS inbox, is noise. The point
         of a record is to know what happened when you were not
         there. You were there — you wrote it.

         THE FIX:
           · route through a relay that can actually address a
             third party (FormSubmit — the same reason the
             student's booking receipt moved there in v79)
           · the recipient is the RECIPIENT, not a row of text
           · no copy to ourselves at all
           · reply-to is EkGuru, so their answer comes back
         ========================================================= */
      var payload = {
        _subject: data.subject || ("A message from " + brand),
        _template: "table",
        _captcha: "false",
        "Message": data.message,
        "Sent": new Date().toUTCString(),
        "—": sign,
        /* Their reply comes to us. This is the one address that
           SHOULD be ours in this message. */
        email: data.replyTo || SITE.email || ""
      };

      var target = data.to;

      /* =========================================================
         v86 — TWO BUGS IN THE RELAY CHOICE FOR AN ADMIN REPLY
         ---------------------------------------------------------
         BUG A — THE WRONG CAPABILITY WAS BEING ASKED ABOUT.
         This filtered on `!p.cannotCC`. That asks "can this relay
         carry a CC?" — a question this message never poses, since
         an admin reply has one recipient and no CC. The question
         it MEANT to ask is "will this relay honour the recipient I
         give it, or deliver wherever its key points?" That is
         `ignoresRecipient`, which is what StaticForms sets.

         It happened to select the right relay today only because
         StaticForms sets BOTH flags. Add a fourth relay tomorrow
         that honours a recipient but cannot CC and this would have
         silently refused to use it. A filter that gets the right
         answer from the wrong question is a bug waiting for a new
         provider.

         BUG B — AN ADMIN REPLY TO A NEW ADDRESS FAILED.
         FormSubmit is free and correct for anyone you have already
         corresponded with — which is the normal case, and why it
         is preferred. But it refuses an address whose owner has
         never clicked an activation link, and the dashboard lets
         you type ANY address. Writing to somebody for the first
         time returned "This form needs Activation", the dashboard
         showed that raw message, and the reply was simply not
         sent. Web3Forms could have carried it — the ACCOUNT is
         verified by the access key, so it needs no activation —
         but nothing ever tried it.

         Now: prefer the free relay, and if it comes back with an
         activation refusal, retry through one that can address a
         stranger. Cost stays at zero for every ordinary reply and
         only a genuinely new correspondent spends one of the 250.
         ========================================================= */

      /* Relays that will actually deliver to the address we name,
         cheapest first — free before metered. A CAPABILITY sort,
         so a new provider needs no edit here. */
      var usable = chain().filter(function (p) { return !p.ignoresRecipient; });
      var free = usable.filter(function (p) { return !p.metered; });
      var paid = usable.filter(function (p) { return p.metered; });
      var order = free.concat(paid);
      if (!order.length) order = [PROVIDERS[PROVIDERS.length - 1]];

      /* Does this failure mean "the recipient is not activated"
         rather than "the message was bad"? Only that one refusal
         is worth spending a metered send on; anything else is a
         real error and must surface. */
      function needsActivation(msg) {
        return /activat/i.test(String(msg || ""));
      }

      function attemptWith(i) {
        var relay = order[i];
        return postVia(relay, target, payload).then(function (r) {
          if (r.ok) return { ok: true, to: target, via: relay.label };

          var another = order[i + 1];

          /* ⚠️ v95 — QUOTA ALSO HAS TO MOVE ON, NOT ONLY ACTIVATION.
             This advanced to the next relay when the error said
             "needs Activation" and for no other reason. So when
             Web3Forms answered "monthly submission limit" —
             the commonest failure there is — compose() stopped
             dead, even with EmailJS configured and ready one
             position further down the list.

             Reproduced with all five keys spent: the reply failed
             while a working relay sat untried.

             post() already retries a quota refusal internally by
             marking the key spent, but once EVERY key on that
             provider is gone it returns the error, and this is
             where the next PROVIDER has to be tried. */
          var moveOn = needsActivation(r.error) ||
            /quota|limit|exceeded|upgrade|invalid access key|unauthorized/i.test(r.error || "");

          if (another && moveOn) {
            /* Only reached for a correspondent we have never
               mailed. Logged so the reason a metered send was
               spent is visible rather than mysterious. */
            if (window.console && console.info) {
              console.info("[EkGuru] " + relay.label + " could not deliver (" +
                (r.error || "refused") + "); retrying through " + another.label + ".");
            }
            return attemptWith(i + 1);
          }

          /* ═══════════════════════════════════════════════════════
             v94 — THE LAST RESORT compose() DID NOT HAVE
             ───────────────────────────────────────────────────────
             Reproduced 11 Sep 2026: with the metered key spent and
             the free relay refusing an unactivated stranger, this
             threw "You have reached your monthly submission limit"
             and the message was simply lost.

             send() has had a fallback for this since v79 — the
             student's receipt reverts to arriving in EkGuru's
             inbox with the person CC'd, which is worse but never
             lost. compose() never got the same treatment, so an
             admin reply on the 250th day of the month failed
             outright.

             Every other path in this file follows one rule:
             DEGRADED, NEVER LOST. This makes compose() follow it
             too. The reply lands in our own inbox, addressed to
             us, with the intended recipient CC'd and named at the
             top, so it can be forwarded in one click.

             Only attempted once, and only when there is a real
             inbox to fall back to. */
          if (isEmail(SITE.email) &&
              String(target).toLowerCase() !== String(SITE.email).toLowerCase()) {
            var copy = {};
            for (var k in payload) copy[k] = payload[k];
            copy._subject = "[could not deliver] " + (payload._subject || "");
            copy._cc = target;
            copy["COULD NOT SEND DIRECTLY TO"] = target;
            copy["WHY"] = r.error || "the relay refused";
            copy["WHAT TO DO"] = "Forward this to " + target +
              ", or reply to it — they are CC'd.";

            return postOwn(SITE.email, copy).then(function (r2) {
              if (r2.ok) {
                return { ok: true, to: SITE.email, via: "fallback",
                         degraded: true, intended: target,
                         note: "Could not reach " + target + " directly (" +
                               (r.error || "relay refused") +
                               "). Sent to your own inbox with them CC'd." };
              }
              throw new Error(r.error || "The mail relay gave no confirmation.");
            });
          }

          throw new Error(r.error || "The mail relay gave no confirmation.");
        });
      }

      return attemptWith(0);
    },

    /* Which provider is in use, for the dashboard to display.
       v54: reports the quota fallback too, so the Integrations panel
       can say "Web3Forms, but the monthly quota ran out" instead of
       silently showing FormSubmit and looking like the key was never
       configured. */
    provider: function () {
      var c = chain();
      var active = c[0] || PROVIDERS[PROVIDERS.length - 1];
      var q = quotaState();
      return {
        name: active.label,
        id: active.id,
        branded: !!active.branded,
        /* True when a better provider exists but is spent for the
           month — the dashboard says so instead of looking like the
           key was never configured. */
        fallback: q.spent.length > 0,
        spent: q.spent,
        available: q.available,
        chain: c.map(function (p) { return p.label; }),
        month: q.month
      };
    },

    /* Every provider the site knows about, for the dashboard to list
       with its real state. */
    providers: function () {
      return PROVIDERS.map(function (p) {
        /* v87 — the dashboard needs the CAPABILITIES, not just the
           name. Before this it could only print a label, so the
           "which relay carries which message" table was written by
           hand in admin.html and could drift from the code. Now it
           is rendered from what the providers actually declare. */
        var keys = p.keys ? p.keys() : [];
        return {
          id: p.id, label: p.label, branded: !!p.branded,
          note: p.quotaNote,
          configured: p.enabled(),
          spent: spent(p.id),
          /* Capabilities — the four questions routing asks. */
          metered: !!p.metered,
          cannotCC: !!p.cannotCC,
          canAddressStrangers: !!p.canAddressStrangers,
          ignoresRecipient: !!p.ignoresRecipient,
          /* Multi-key relays report each key separately, redacted.
             A key is public in the page source anyway, but there is
             no reason to print it in full on a dashboard someone
             may screenshot. */
          keys: keys.map(function (k) {
            return {
              tail: "..." + String(k).slice(-6),
              spent: spent("web3forms:" + k)
            };
          }),
          keysTotal: keys.length,
          keysLeft: keys.filter(function (k) {
            return !spent("web3forms:" + k);
          }).length,
          /* v94 — values that were configured but are not usable.
             The dashboard shows these, because a key you think you
             have and do not is worse than one you know is missing:
             the ceiling looks higher than it is until the day it
             matters. */
          keysIgnored: (function () {
            if (!p.keys) return [];
            var VALID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
            var raw = [].concat(CFG.web3formsKey || [], CFG.web3formsKeys || []);
            return raw.map(function (k) { return String(k == null ? "" : k).trim(); })
                      .filter(function (k) { return k && !VALID.test(k); });
          })()
        };
      });
    },

    /* =========================================================
       v87 — bulkSend(list, message, onProgress)
       ---------------------------------------------------------
       Prakash: "admin page se kisi ko bhi unlimited... jo jo mail
       provider hai unse mail send kar sake bina kisi dikkat ke."

       Sends the same message to many recipients, one at a time,
       choosing the cheapest relay that can reach EACH one. This
       is not a loop around compose(): the routing differs per
       recipient, and that is the whole point.

         · an address we own      → free relay, costs nothing
         · someone already mailed → free relay, costs nothing
         · a stranger             → metered relay, one send
                                    (only relay that can, and only
                                     if the free one refuses)

       WHY ONE AT A TIME AND NOT Promise.all
       FormSubmit throttles a burst and, worse, answers the
       throttle with "Make sure you open this page through a web
       server" — a message that looks like a completely different
       fault. Measured 08/09/2026: 12 simultaneous requests all
       failed; the same 12 sent in sequence all succeeded. The gap
       costs a few seconds and removes the failure.

       onProgress({ index, total, to, ok, via, error }) is called
       after each one so the dashboard can show a live list rather
       than freezing until the end. A single failure never stops
       the run — the remaining recipients still get their message,
       and the failures are returned for retry.
       ========================================================= */
    bulkSend: function (list, message, onProgress) {
      var self = this;
      var targets = (list || []).map(function (x) {
        return typeof x === "string" ? { to: x } : x;
      }).filter(function (x) { return isEmail(x.to); });

      if (!targets.length) {
        return Promise.reject(new Error("No valid recipients"));
      }
      if (!message || !message.message || !String(message.message).trim()) {
        return Promise.reject(new Error("The message is empty"));
      }

      var results = [];
      function step(i) {
        if (i >= targets.length) {
          return Promise.resolve({
            ok: results.every(function (r) { return r.ok; }),
            sent: results.filter(function (r) { return r.ok; }).length,
            failed: results.filter(function (r) { return !r.ok; }),
            results: results
          });
        }
        var t = targets[i];

        /* Per-recipient substitution. {{name}} in the subject or
           body becomes that person's name, so a bulk message can
           still be addressed to a human. Missing name falls back
           to "there" rather than printing an empty gap or the
           literal token. */
        function fill(str) {
          return String(str || "").replace(/\{\{\s*name\s*\}\}/g, t.name || "there");
        }

        return self.compose({
          to: t.to,
          subject: fill(message.subject),
          message: fill(message.message),
          replyTo: message.replyTo
        }).then(function (r) {
          var row = { to: t.to, name: t.name || "", ok: true, via: r.via };
          results.push(row);
          if (onProgress) onProgress({ index: i, total: targets.length, row: row });
          return row;
        }, function (e) {
          var row = { to: t.to, name: t.name || "", ok: false,
                      error: e && e.message ? e.message : String(e) };
          results.push(row);
          if (onProgress) onProgress({ index: i, total: targets.length, row: row });
          return row;
        }).then(function () {
          if (i + 1 >= targets.length) return step(i + 1);
          /* 400ms between sends. Enough to stay under every free
             relay's burst limit, short enough that fifty
             recipients take twenty seconds rather than minutes. */
          return new Promise(function (res) { setTimeout(res, 400); })
            .then(function () { return step(i + 1); });
        });
      }
      return step(0);
    },

    /* Quota controls, for the dashboard. clearQuota() exists so you
       can switch straight back after upgrading, without waiting for
       the 1st of the month. */
    quota: quotaState,
    clearQuota: clearQuota
  };

  window.EkGuruMail = Mail;
})();
