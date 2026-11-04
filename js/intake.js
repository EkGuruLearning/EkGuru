/* =========================================================
   EkGuru — ONLINE FORMS (tutor application, review, sign-up, booking, contact)
   ---------------------------------------------------------
   Sends a form to the Intake web app (apps-script/Intake.gs)
   and shows the visitor a plain result. It never publishes
   anything. Every submission is a PENDING row for the owner
   to check first.

   EkGuru — ONLINE FORMS (tutor application, review, sign-up, booking, contact)
   (or not a real Apps Script /exec address), this file does
   nothing: the form's own mailto link still works, exactly as
   before. So it is safe to merge before the script is deployed.

   HOW A FORM OPTS IN
     <form data-intake="application"> … </form>
     data-intake is one of: application, review, signup, booking, contact.
     Inside the form, the server reads: name, email, … (the
     name attribute of each field must match the server's list).
     A field called "website" is the honeypot. Keep it hidden.

   WHAT THE VISITOR SEES
     Checking…  →  "Thank you. Your reference is EG-XXXXXX (booking:
     EK-XXXXXX).
     We reply by email within a few days."
     or the real reason (for example "that email does not look
     right"), or, if the form cannot be sent, the email option.
   ========================================================= */
(function () {
  "use strict";

  var S = (window.EKGURU_SITE || {});
  var KINDS = { application: 1, review: 1, signup: 1, booking: 1, contact: 1 };
  var TIMEOUT_MS = 15000;

  function intakeUrl() {
    var u = String((S.intake && S.intake.url) || "").trim();
    return /^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(u) ? u : "";
  }

  function ready() {
    return !!intakeUrl() && typeof window.fetch === "function";
  }

  /* Plain-English checks, the same rules as the server, so a typo is caught
     before the request leaves the browser. The server still decides. */
  function checkFields(kind, fields) {
    /* Length limits mirror apps-script/Intake.gs exactly. A field the
       client forgets to check here is not a soft warning: the server
       refuses the WHOLE submission, so (for example) a student goal of
       201 characters used to lose the entire booking. */
    var rules = {
      application: { name: 80, email: 120, subject: 60, bio: 1500 },
      review:      { tutor_id: 60, reviewer_name: 60, text: 800 },
      signup:      { email: 120 },
      booking:     { student_name: 60, student_email: 120, preferred_times_ist: 120,
                     student_whatsapp: 30, lesson: 60, price_usd: 12,
                     student_level: 60, student_goal: 200, student_timezone: 60,
                     source_page: 300, tutor_email: 120 },
      contact:     { name: 80, email: 120, subject: 120, topic: 60, message: 4000, page: 300 }
    }[kind];
    var required = {
      application: ["name", "email", "subject", "bio"],
      review:      ["tutor_id", "reviewer_name", "stars", "text", "booking_id"],
      signup:      ["email", "goal"],
      booking:     ["booking_ref", "tutor_id", "student_name", "student_email", "preferred_times_ist"],
      contact:     ["name", "email", "message"]
    }[kind];
    for (var i = 0; i < required.length; i++) {
      var v = String(fields[required[i]] == null ? "" : fields[required[i]]).trim();
      if (!v) return "Please fill in " + required[i].replace(/_/g, " ") + ".";
    }
    var keys = Object.keys(rules);
    for (var k = 0; k < keys.length; k++) {
      var val = String(fields[keys[k]] == null ? "" : fields[keys[k]]).trim();
      if (val.length > rules[keys[k]]) return keys[k].replace(/_/g, " ") + " is too long.";
    }
    /* The email field is NOT called "email" on every form: a booking
       sends student_email (and an optional tutor_email), a review an
       optional contact_email. Checking only fields.email meant a typo'd
       student address passed the browser and was refused by the server
       AFTER the whole booking submit — the sheet row was lost. */
    var emailFields = {
      application: [["email", true]],
      review:      [["contact_email", false]],
      signup:      [["email", true]],
      booking:     [["student_email", true], ["tutor_email", false]],
      contact:     [["email", true]]
    }[kind] || [];
    for (var e = 0; e < emailFields.length; e++) {
      var ev = String(fields[emailFields[e][0]] == null ? "" : fields[emailFields[e][0]]).trim();
      if (!ev && !emailFields[e][1]) continue;
      if (ev && !/^[^\s@<>"']+@[^\s@<>"']+\.[^\s@<>"']{2,}$/.test(ev)) {
        return "That email does not look right.";
      }
    }
    return "";
  }

  /* Send. Resolves { ok, reference } or { ok:false, error, fallback }. Never rejects. */
  function submit(kind, fields, consent, honeypot) {
    if (!KINDS[kind]) return Promise.resolve({ ok: false, error: "This form is not set up." });
    if (!ready()) return Promise.resolve({ ok: false, fallback: true, error: "Online sending is off right now." });
    var problem = checkFields(kind, fields || {});
    if (problem) return Promise.resolve({ ok: false, error: problem });
    if (consent !== true) return Promise.resolve({ ok: false, error: "Please tick the box so we can reply to you." });

    var body = JSON.stringify({
      kind: kind, consent: true, website: String(honeypot || ""), fields: fields || {}
    });
    var ctrl = typeof AbortController === "function" ? new AbortController() : null;
    var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, TIMEOUT_MS) : null;

    return window.fetch(intakeUrl(), {
      method: "POST",
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: body,
      signal: ctrl ? ctrl.signal : undefined,
      redirect: "follow"
    }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.text();
    }).then(function (t) {
      var j;
      try { j = JSON.parse(t); } catch (e) { throw new Error("not JSON"); }
      /* Success MUST carry the reference the server wrote into the
         sheet row. A bare {"ok":true} can also come from the health
         action or a wrong/old deployment answering the redirect;
         trusting it used to tell the student "saved" (and let the
         booking email go out) with no row in the sheet at all. */
      if (j && j.ok && String(j.reference || "").trim()) {
        return { ok: true, reference: String(j.reference), duplicate: j.duplicate === true };
      }
      if (j && j.ok) {
        return { ok: false, fallback: true, error: "The booking service replied without a confirmation reference, so this was not treated as saved." };
      }
      return { ok: false, error: String((j && j.error) || "We could not save that. Please email us instead.") };
    }).catch(function () {
      return { ok: false, fallback: true, error: "We could not reach the form just now. Please email us instead." };
    }).then(function (res) {
      if (timer) clearTimeout(timer);
      return res;
    });
  }

  function formFields(form) {
    var out = {};
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.disabled) return;
      if (el.type === "checkbox" || el.type === "radio") {
        if (!el.checked) return;
      }
      out[el.name] = el.value;
    });
    return out;
  }

  function showMessage(form, text, isError) {
    var box = form.querySelector("[data-intake-msg]");
    if (!box) {
      box = document.createElement("p");
      box.setAttribute("data-intake-msg", "");
      box.setAttribute("role", "status");
      form.appendChild(box);
    }
    box.textContent = text;
    box.style.color = isError ? "#b42318" : "#147a3d";
  }

  function wire(form) {
    if (form.__egIntake) return;
    form.__egIntake = true;
    form.addEventListener("submit", function (ev) {
      if (!ready()) return;          /* off: let the mailto / Google Form path run */
      ev.preventDefault();
      var kind = form.getAttribute("data-intake");
      var consentEl = form.querySelector('[name="consent"]');
      var honey = form.querySelector('[name="website"]');
      var button = form.querySelector('button[type="submit"],input[type="submit"]');
      if (button) button.disabled = true;
      showMessage(form, "Sending…", false);
      var fields = formFields(form);
      delete fields.consent;
      delete fields.website;
      submit(kind, fields, !!(consentEl && consentEl.checked), honey ? honey.value : "")
        .then(function (res) {
          if (button) button.disabled = false;
          if (res.ok) {
            form.reset();
            showMessage(form, "Thank you. Your reference is " + res.reference +
              ". We reply by email within a few days.", false);
          } else if (res.fallback) {
            showMessage(form, res.error + " You can also write to EkGuruLearning@gmail.com.", true);
          } else {
            showMessage(form, res.error, true);
          }
        });
    });
  }

  function init() {
    var forms = document.querySelectorAll("form[data-intake]");
    for (var i = 0; i < forms.length; i++) wire(forms[i]);
  }

  /* Re-wire forms injected after load (the profile review form is
     re-rendered on every sheet repaint — without this its submit
     falls back to a native mailto POST). Idempotent. */
  window.EkGuruIntake = { ready: ready, submit: submit, checkFields: checkFields, intakeUrl: intakeUrl, rewire: init };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
