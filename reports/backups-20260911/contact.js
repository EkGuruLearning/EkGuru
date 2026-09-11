/* =========================================================
   EkGuru — THE CONTACT FORM                              (v78)
   ---------------------------------------------------------
   WHAT PRAKASH ASKED FOR

     "ek contact jisme website se hi direct contact kar le,
      direct mail aa jaye static ke through … manually to
      contact form fill kare aur send kaam ho jaye. Uski mail
      id, uska naam, uska message — jo hum usko reply kar sake."

   Three fields minimum — name, email, message — sent from the
   page itself through the same static relay chain the booking
   form uses. No server. No database. Nothing stored anywhere.

   ---------------------------------------------------------
   WHY THE FORM MARKUP IS NOT BUILT BY THIS FILE
   ---------------------------------------------------------
   It is written into the page by tools/contactpage.js and by
   tools/contactform.js, as real HTML, before this script ever
   runs. Three reasons, all learned the hard way:

     1. A form that only exists after JavaScript runs is a form
        Google never sees and a form that does not exist for
        anyone whose script blocker ate this file.

     2. The <form> has a real `action` and `method` so it is a
        working form with this file entirely absent — it falls
        back to the visitor's own mail app (see NOJS below).
        That is worse UX, but it is never a dead button.

     3. v62's lesson: "_overrides.js applied to an empty array"
        — a script that builds the thing it also fills in can
        silently do neither. Markup first, behaviour second.

   This file only ADDS behaviour to markup that is already
   correct: intercept submit, validate inline, call
   EkGuruMail.contact(), swap in a confirmation.

   ---------------------------------------------------------
   THE HONEYPOT, AND WHY NOT A CAPTCHA
   ---------------------------------------------------------
   A captcha needs a third-party script, a consent story, and
   it punishes real people. The bots that scrape static sites
   fill in every field they find. So there is one extra field,
   hidden from people three different ways (off-screen,
   aria-hidden, tabindex -1, autocomplete off) and labelled as
   a trap in the markup. If it comes back filled we show the
   normal success screen and send nothing: a bot that is told
   it failed simply tries again from another address.

   Second line: a minimum dwell time. A human cannot read the
   page, type a name, an address and ten words in under three
   seconds. Anything faster is scripted.

   ---------------------------------------------------------
   NOJS — WHAT HAPPENS WITH THIS FILE MISSING
   ---------------------------------------------------------
   The <form> element carries action="mailto:..." so the
   browser composes the message in the visitor's mail app. It
   is clumsy — that is exactly why the JS path exists — but the
   message is never lost, and no button ever does nothing.
   ========================================================= */

(function () {
  "use strict";

  var SITE = window.EKGURU_SITE || {};

  function $(s, r) { return (r || document).querySelector(s); }
  function $all(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function isEmail(v) {
    return !!v && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(v).trim());
  }

  /* A short, human-readable reference. Shown to the visitor and
     put in the subject line of both emails, so a follow-up can be
     matched to a message without any database. Time-based, upper
     case, six characters — long enough not to collide in practice
     for a site this size, short enough to read down a phone. */
  function makeRef() {
    return "C-" + Date.now().toString(36).toUpperCase().slice(-6);
  }

  /* GoatCounter, wrapped. An analytics failure must never break a
     form submit — and GoatCounter is blocked by many ad-blockers,
     which is fine and expected. */
  function track(name) {
    try {
      if (window.goatcounter && window.goatcounter.count) {
        window.goatcounter.count({ path: "event/" + name, title: name, event: true });
      }
    } catch (e) {}
  }

  /* ---------------------------------------------------------
     Inline validation.
     Returns "" when the field is fine, or the message to show.
     Written as one function per rule so the contact form and
     the tests check the SAME rule — a test that reimplements
     the rule tests itself (v66 / v74).
     --------------------------------------------------------- */
  var RULES = {
    name: function (v) {
      v = String(v || "").trim();
      if (!v) return "Please tell us your name.";
      if (v.length < 2) return "That looks too short to be a name.";
      return "";
    },
    email: function (v) {
      v = String(v || "").trim();
      if (!v) return "We need an email address to reply to.";
      if (!isEmail(v)) return "That does not look like an email address.";
      return "";
    },
    message: function (v) {
      v = String(v || "").trim();
      if (!v) return "Please write your message.";
      if (v.length < 10) return "Please write a little more so we can actually help.";
      if (v.length > 4000) return "That is longer than the form can send. Please shorten it a little.";
      return "";
    }
  };

  function fieldError(form, key, msg) {
    var input = $('[name="' + key + '"]', form);
    var slot = $('[data-err-for="' + key + '"]', form);
    if (input) {
      input.setAttribute("aria-invalid", msg ? "true" : "false");
      if (msg) input.classList.add("cf-bad"); else input.classList.remove("cf-bad");
    }
    if (slot) {
      slot.textContent = msg || "";
      slot.hidden = !msg;
    }
    return !msg;
  }

  function validate(form) {
    var ok = true;
    Object.keys(RULES).forEach(function (k) {
      var el = $('[name="' + k + '"]', form);
      var msg = RULES[k](el ? el.value : "");
      if (!fieldError(form, k, msg)) ok = false;
    });
    return ok;
  }

  /* ---------------------------------------------------------
     The confirmation screen.
     Replaces the form rather than sitting above it, so nobody
     sends the same message twice wondering whether it worked.
     --------------------------------------------------------- */
  function showSent(host, res, data) {
    var ackLine = res.acknowledged
      ? "A copy has been sent to <b>" + esc(data.email) + "</b> so you have a record of it."
      : "We could not send you a copy, but your message did arrive with us.";

    host.innerHTML =
      '<div class="cf-done" role="status">' +
        '<div class="cf-tick" aria-hidden="true">✓</div>' +
        "<h2>Message sent</h2>" +
        "<p>Thank you, " + esc(String(data.name).split(" ")[0]) + ". " +
        "Your reference is <b class=\"cf-ref\">" + esc(res.ref) + "</b>.</p>" +
        "<p>" + ackLine + "</p>" +
        "<p class=\"cf-small\">A person reads every message — there is no bot answering " +
        "these. You will normally hear back within a day at " + esc(data.email) + ". " +
        "If nothing arrives, check your spam folder before writing again.</p>" +
        '<p><a class="btn btn-ghost" href="' + esc(host.getAttribute("data-home") || "./") + '">Back to the site</a></p>' +
      "</div>";
    host.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  /* Failure. The visitor's words are NEVER thrown away: the form
     stays exactly as they left it, and they are handed a mailto
     that already contains everything they typed. Losing a
     visitor's message because a third-party relay had a bad
     minute is not acceptable. */
  function showFail(form, err, data) {
    var box = $(".cf-err", form);
    if (!box) return;
    var href = (window.EkGuruMail && window.EkGuruMail.contactMailto)
      ? window.EkGuruMail.contactMailto(data)
      : "mailto:" + (SITE.email || "");
    box.innerHTML =
      "<b>That did not send.</b> " + esc(err && err.message ? err.message : String(err)) +
      "<br>Nothing you typed has been lost. " +
      '<a href="' + esc(href) + '">Send it from your own email app instead</a>' +
      " — everything is already filled in.";
    box.hidden = false;
    box.focus && box.focus();
  }

  /* ---------------------------------------------------------
     Wire one form.
     --------------------------------------------------------- */
  function initForm(form) {
    if (form.getAttribute("data-cf-ready") === "1") return;
    form.setAttribute("data-cf-ready", "1");

    var host = form.closest("[data-contact-host]") || form.parentNode;
    var openedAt = Date.now();
    var sending = false;

    /* Clear a field's error as soon as it becomes valid, rather
       than only on the next submit. An error message that stays
       on screen after you have fixed the thing is worse than no
       error message. */
    Object.keys(RULES).forEach(function (k) {
      var el = $('[name="' + k + '"]', form);
      if (!el) return;
      el.addEventListener("input", function () {
        if (el.getAttribute("aria-invalid") !== "true") return;
        if (!RULES[k](el.value)) fieldError(form, k, "");
      });
      el.addEventListener("blur", function () {
        if (el.value) fieldError(form, k, RULES[k](el.value));
      });
    });

    /* Live character count on the message. Not decoration: the
       relay has a size limit, and finding out at submit time
       that 4000 characters were too many is infuriating. */
    var msg = $('[name="message"]', form);
    var count = $(".cf-count", form);
    if (msg && count) {
      var paint = function () {
        var n = msg.value.length;
        count.textContent = n + " / 4000";
        count.classList.toggle("cf-count-hot", n > 3600);
      };
      msg.addEventListener("input", paint);
      paint();
    }

    form.addEventListener("submit", function (e) {
      /* Relay path only exists when there is a mailer with fetch.
         With neither, we let the browser do what the markup says
         — action="mailto:" — rather than swallowing the submit
         and leaving a dead button. */
      var canRelay = !!(window.EkGuruMail && window.EkGuruMail.contact &&
                        typeof window.fetch === "function");
      if (!canRelay) return;

      e.preventDefault();
      if (sending) return;

      var err = $(".cf-err", form);
      if (err) err.hidden = true;

      if (!validate(form)) {
        var first = $(".cf-bad", form);
        if (first) first.focus();
        track("contact_invalid");
        return;
      }

      var data = {
        name: $('[name="name"]', form).value.trim(),
        email: $('[name="email"]', form).value.trim(),
        topic: ($('[name="topic"]', form) || {}).value || "General",
        subject: (($('[name="subject"]', form) || {}).value || "").trim(),
        message: $('[name="message"]', form).value.trim(),
        hp: (($('[name="company"]', form) || {}).value || ""),
        pageUrl: (form.getAttribute("data-from") || location.href),
        lang: document.documentElement.getAttribute("lang") || "en",
        ref: makeRef()
      };

      /* Dwell-time trap — see the honeypot note at the top. A
         human has not read this page and typed all of that in
         three seconds. Treated exactly like the honeypot: looks
         successful, sends nothing. */
      if (Date.now() - openedAt < 3000) {
        track("contact_too_fast");
        showSent(host, { ok: true, ref: data.ref, acknowledged: false }, data);
        return;
      }

      sending = true;
      var btn = $(".cf-send", form);
      var label = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      track("contact_submit");

      window.EkGuruMail.contact(data).then(function (res) {
        track("contact_sent");
        /* ═══════════════════════════════════════════════════════
           v93 — WRITE IT DOWN.
           ───────────────────────────────────────────────────────
           A visitor gets a reference on screen and in both emails,
           then writes back three days later asking about C-4K2P9X
           — and the dashboard had never heard of it, because a
           contact submission was sent and then forgotten.

           Bookings were recorded; contacts were not. Same
           reference, same promise to the visitor, no record.
           Now every message lands in one ledger the dashboard can
           search. See js/ledger.js.

           Wrapped in try/catch on purpose: the message has already
           been delivered by this point. A storage failure — private
           mode, quota full — must never turn a successful send into
           an error the visitor sees. */
        try {
          if (window.EkGuruLedger) {
            window.EkGuruLedger.add({
              kind: data.topic === "Report" ? "report" : "contact",
              ref: res.ref,
              name: data.name,
              email: data.email,
              subject: data.subject,
              topic: data.topic,
              summary: data.message,
              ok: true,
              recipients: [
                { role: "ekguru", to: res.to || "", ok: true },
                /* The acknowledgement is best-effort by design: if
                   it failed the visitor still got through, and the
                   ledger records that honestly rather than claiming
                   both arrived. */
                { role: "sender", to: data.email, ok: res.acknowledged !== false }
              ]
            });
          }
        } catch (e3) {}
        showSent(host, res, data);
      }).catch(function (e2) {
        sending = false;
        if (btn) { btn.disabled = false; btn.textContent = label; }
        track("contact_failed");
        /* A failure is worth recording too — more so than a
           success. It is the list somebody has to act on. */
        try {
          if (window.EkGuruLedger) {
            window.EkGuruLedger.add({
              kind: "contact", name: data.name, email: data.email,
              subject: data.subject, topic: data.topic, summary: data.message,
              ok: false, error: (e2 && e2.message) || String(e2)
            });
          }
        } catch (e3) {}
        showFail(form, e2, data);
      });
    });
  }

  /* ---------------------------------------------------------
     Prefill from the URL.
     Every "tell us" / "report a spelling" link on the site now
     points here with ?topic=…&subject=…&from=… instead of
     opening a mail client. This reads them back so the visitor
     lands on a form that already knows why they came.

     Values are written with .value, never innerHTML — a query
     string is attacker-controlled and this is the exact shape
     of a reflected-XSS bug.
     --------------------------------------------------------- */
  function prefill(form) {
    var q;
    try { q = new URLSearchParams(location.search); } catch (e) { return; }

    var topic = q.get("topic");
    if (topic) {
      var sel = $('[name="topic"]', form);
      if (sel) {
        var found = false;
        $all("option", sel).forEach(function (o) {
          if (o.value.toLowerCase() === topic.toLowerCase()) { sel.value = o.value; found = true; }
        });
        /* An unknown topic is still information — keep it rather
           than silently dropping the visitor's context. */
        if (!found) {
          var o2 = document.createElement("option");
          o2.value = topic; o2.textContent = topic;
          sel.appendChild(o2); sel.value = topic;
        }
      }
    }

    var subject = q.get("subject");
    var sub = $('[name="subject"]', form);
    if (subject && sub) sub.value = subject;

    /* Where they came from, so a spelling report says which page
       the spelling is on. Recorded in a hidden field rather than
       the message box: it is ours, not theirs to edit or delete. */
    var from = q.get("from");
    if (from) form.setAttribute("data-from", from);

    /* A pre-written opening line for report-a-mistake links, so
       the visitor is not staring at an empty box. Only ever
       written into an EMPTY message field — never over anything
       a returning visitor has already typed. */
    var msgEl = $('[name="message"]', form);
    if (msgEl && !msgEl.value && q.get("about")) {
      msgEl.value = "About: " + q.get("about") + "\n\n";
      try { msgEl.setSelectionRange(msgEl.value.length, msgEl.value.length); } catch (e) {}
    }
  }

  function init() {
    $all("form.cf-form").forEach(function (f) {
      prefill(f);
      initForm(f);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  /* Exposed for tools/test-contact.js, and so the admin dashboard
     can reuse exactly the same validation rules rather than
     writing a second, drifting copy of them. */
  window.EkGuruContact = { RULES: RULES, validate: validate, makeRef: makeRef, init: init };
})();
