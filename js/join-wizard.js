/* =========================================================
   EkGuru — TUTOR APPLICATION WIZARD (join.html)
   ---------------------------------------------------------
   WHAT THIS IS
   A guided seven-step front end around the SAME intake endpoint
   js/intake.js already posts to (js/site-config.js -> intake.url,
   Apps Script "Unified.gs" -> "ApplicationIntake.gs"). It adds no
   backend, no second review system and no new status: it validates
   earlier and fills the applications row properly.

   WHAT IT DOES NOT DO
   · It never invents fields the backend would drop. Every answer
     a tutor gives maps to its own column in
     apps-script/ApplicationSchema.gs (see buildPayload below). An
     answer with no column is sent under its own name and stored in
     `details_json` by the server, never silently dropped.
   · It never sends a value the tutor did not choose. A <select>
     that opens on a real value would answer for them on every
     resubmission, so the optional ones open on an empty option.
   · It never claims an upload succeeded. There is no file
     storage in this architecture, so a photo is a LINK the tutor
     already hosts (Drive/YouTube), exactly as before. The
     preview is a local-only image preview of a URL that loads.
   · It never marks anything verified. Qualification text is
     labelled "as declared by the tutor".

   WITHOUT JAVASCRIPT
   join.html ships the form as real HTML with action=mailto and
   every step visible. If this file fails to load, a tutor can
   still send an application by email. Nothing is lost.
   ========================================================= */
(function () {
  "use strict";

  var DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  var MAX_NOTES = 500;
  /* There is deliberately NO minimum biography length. 150–250 words is
     ADVICE, shown by the counter under the box; what blocks the step is an
     empty introduction and nothing else. A tutor who writes one honest
     sentence must not be stopped by a number nobody told them was a rule. */

  /* ---------------------------------------------------------
     The contract with the backend.
     ---------------------------------------------------------
     Lengths come from js/join-schema.js (generated from
     apps-script/ApplicationSchema.gs), so the page and the server cannot
     disagree about a limit. These literals are only the fallback for the
     case where the schema file did not load — and in that case
     buildPayload() also switches to the old 13-column payload, so a
     missing script degrades to the previous behaviour rather than to an
     empty submission.
     --------------------------------------------------------- */
  var FALLBACK_LIMITS = {
    name: 80, email: 120, city: 80, country: 60,
    subject: 60, experience: 300, availability: 400,
    bio: 1500, photo_link: 300, video_link: 300,
    languages: 120, notes: 2000
  };
  function schemaLimits() {
    var S = window.EKGURU_APP_SCHEMA;
    var out = {};
    for (var k in FALLBACK_LIMITS) if (Object.prototype.hasOwnProperty.call(FALLBACK_LIMITS, k)) out[k] = FALLBACK_LIMITS[k];
    if (!S || !S.fields) return out;
    S.fields.forEach(function (f) {
      if (!f.src || !f.max) return;
      if (out[f.src] !== undefined) out[f.src] = f.max;
    });
    return out;
  }
  var LIMITS = schemaLimits();

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }
  function val(el) { return el ? String(el.value || "").trim() : ""; }
  function clip(s, n) {
    s = String(s || "").replace(/\s+/g, " ").trim();
    return s.length > n ? s.slice(0, n - 1).trim() + "…" : s;
  }
  function words(s) {
    s = String(s || "").trim();
    return s ? s.split(/\s+/).length : 0;
  }

  /* ---------------------------------------------------------
     Availability: the day rows are a small state machine.
     ---------------------------------------------------------
     A day row has three pieces: the tick box (the answer), the two
     time inputs (the detail) and the row itself (the visual state).

     The rule, in one place so it cannot drift:
        ticked   → row is NOT is-off, both time inputs enabled
        unticked → row IS is-off, both time inputs disabled

     A disabled time input is skipped by the browser's own form controls,
     cannot take focus and cannot be typed into — which is exactly why the
     row must be enabled the moment its box is ticked. An earlier build
     rendered every row with `is-off` and `disabled=""` and never undid
     it, so step 5 could not be completed at all.

     Clearing rule (documented, and deliberate): unticking a day KEEPS the
     times it already had. Re-ticking the same day brings the hours back, so
     a tutor who changes their mind twice does not re-type them; the values
     are never sent for an unticked day, because availabilitySlots() only
     reads ticked rows.
     --------------------------------------------------------- */
  function dayRow(root, day) {
    return $('[data-day="' + day + '"]', root);
  }

  function setDayState(row) {
    if (!row) return false;
    var on = $('input[type="checkbox"]', row);
    var live = !!(on && on.checked);
    if (row.classList) row.classList.toggle("is-off", !live);
    /* Per-control, not a blanket querySelectorAll on the row: the checkbox
       itself must NEVER be disabled, or the tutor could not undo the tick. */
    var times = row.querySelectorAll('input[type="time"]');
    for (var i = 0; i < times.length; i++) {
      times[i].disabled = !live;
      times[i].setAttribute("aria-disabled", live ? "false" : "true");
    }
    if (on) on.setAttribute("aria-expanded", live ? "true" : "false");
    return live;
  }

  /* Every row, every time a step is shown or a box changes. Cheap (7 rows). */
  function syncDayRows(root) {
    DAYS.forEach(function (d) { setDayState(dayRow(root, d)); });
  }

  /* The shared error line under the days block. Called when a day is ticked
     so "tick at least one day" disappears the instant it is true. */
  /* The days block's error line. It is a SIBLING of .jw-days, not a child —
     deliberate, so the message spans the full width under all seven rows
     instead of sitting inside the grid. One helper resolves it so the two
     callers cannot disagree about where it lives. */
  function dayGroupBox(root) {
    var block = $(".jw-days", root);
    if (!block) return null;
    var sib = block.nextElementSibling;
    if (sib && sib.classList && sib.classList.contains("jw-err")) return sib;
    return $(".jw-err", block) || null;
  }

  function clearDayGroupError(root) {
    var box = dayGroupBox(root);
    if (box) { box.textContent = ""; box.classList.remove("is-on"); }
  }

  /* The one sentence under the days block, rebuilt from every ticked day.
     Keeping it a joined list means a tutor who breaks two days sees both. */
  /* Show every error of a step: the days block's shared line FIRST (rebuilt
     from all ticked days), then each field's own message. Called from
     Continue, the progress chips and Submit so all three behave identically
     and none of them can leave a single-day sentence behind. */
  function paintErrors(form, stepEl, errors) {
    if (stepEl && stepEl.querySelector("[data-day]")) refreshDayErrors(form);
    (errors || []).forEach(function (e) {
      if (!e.el) return;
      if (e.el.closest && e.el.closest(".jw-day")) {
        /* Mark only. The shared line already carries every broken day. */
        e.el.setAttribute("aria-invalid", "true");
        return;
      }
      showError(e.el, e.msg);
    });
  }

  function refreshDayErrors(root) {
    var box = dayGroupBox(root);
    if (!box) return;
    var issues = availabilityIssues(root);
    if (!issues.length) {
      box.textContent = "";
      box.classList.remove("is-on");
      return;
    }
    box.textContent = issues.map(function (i) { return i.msg; }).join(" ");
    box.classList.add("is-on");
  }

  /* ---------------------------------------------------------
     Availability: build the sheet's own string format.
     The tutors tab / booking flow read "Mon-Fri 19:00,20:00; Sat
     10:00 | none = away". Producing that exact shape means an
     approved tutor's row can be copied across without retyping.
     --------------------------------------------------------- */
  function readAvailability(root) {
    var parts = [];
    var any = false;
    DAYS.forEach(function (d) {
      var row = $('[data-day="' + d + '"]', root);
      if (!row) return;
      var on = $('input[type="checkbox"]', row);
      if (!on || !on.checked) return;
      any = true;
      var from = val($('input[name$="-from"]', row));
      var to = val($('input[name$="-to"]', row));
      if (from && to) parts.push(d + " " + from + "-" + to);
      else if (from) parts.push(d + " " + from);
    });
    return { any: any, text: parts.join("; ") };
  }

  /* The full weekday name, because "Mon:" reads like a code and
     "Monday:" reads like a person. Used only in messages. */
  var DAY_NAME = {
    Mon: "Monday", Tue: "Tuesday", Wed: "Wednesday", Thu: "Thursday",
    Fri: "Friday", Sat: "Saturday", Sun: "Sunday"
  };

  /* Every problem with the ticked days, as { day, el, msg } — one entry per
     day, so the summary can list all of them and each click lands on the
     right row. Disabled (unticked) days are never checked: they are not an
     answer, so they cannot be wrong. */
  function availabilityIssues(root) {
    var out = [];
    DAYS.forEach(function (d) {
      var row = dayRow(root, d);
      if (!row) return;
      var on = $('input[type="checkbox"]', row);
      if (!on || !on.checked) return;
      var fromEl = $('input[name$="-from"]', row);
      var toEl = $('input[name$="-to"]', row);
      var from = val(fromEl);
      var to = val(toEl);
      var name = DAY_NAME[d] || d;
      if (!from && !to) {
        out.push({ day: d, el: fromEl, msg: name + ": Please select both a start time and an end time." });
        return;
      }
      if (!from) {
        out.push({ day: d, el: fromEl, msg: name + ": Please select a start time." });
        return;
      }
      if (!to) {
        out.push({ day: d, el: toEl, msg: name + ": Please select an end time." });
        return;
      }
      if (to <= from) {
        out.push({ day: d, el: toEl, msg: name + ": the end time must be after the start time." });
      }
    });
    return out;
  }

  /* The first problem, as the single sentence older callers expect. */
  function availabilityProblem(root) {
    var issues = availabilityIssues(root);
    return issues.length ? issues[0].msg : null;
  }

  /* ---------------------------------------------------------
     Validation. Runs against the LIVE fields of one step, so a
     tutor is told what is wrong on the step they are standing on
     rather than at the end.
     --------------------------------------------------------- */
  /* ---------------------------------------------------------
     Error help copy — one sentence per field that explains the FIX,
     not just the fault. Keyed by the control id so an addition to the
     form does not silently fall back to a generic sentence.
     --------------------------------------------------------- */
  var HELP_TEXT = {
    "jw-name": "Please enter your full legal name, for example “Neha Sharma”.",
    "jw-email": "Enter a valid email address, for example neha@example.com.",
    "jw-city": "Please enter the city you teach from.",
    "jw-country": "Please select or type your country.",
    "jw-price": "Enter a valid lesson price in whole US dollars, between 1 and 200.",
    "jw-tz": "Please select your timezone.",
    "jw-bio": "Please add your teaching introduction — who you teach and how.",
    "jw-years": "Please choose how long you have been teaching.",
    "jw-less-exp": "Tell us what you have taught so far, however small.",
    "jw-bed-detail": "Tell us which teaching qualification, in which subject and from where.",
    "jw-edu-qual": "Please choose your highest qualification.",
    "jw-edu-year": "Enter the year you completed it, for example 2018.",
    "jw-duration": "Please choose a lesson length.",
    "jw-trial": "Please choose your trial lesson preference."
  };

  function fieldError(el) {
    if (!el) return "";
    var v = val(el);
    var rule = el.getAttribute("data-rule") || "";
    var label = el.getAttribute("data-label") || "This field";
    var max = parseInt(el.getAttribute("maxlength") || "0", 10);
    var help = HELP_TEXT[el.id] || "";

    if (el.required && !v) {
      if (help) return help;
      if (el.tagName === "SELECT") return "Please choose " + label + ".";
      return "Please enter " + label + ".";
    }
    if (!v) return "";
    if (max && v.length > max) return label + " is too long (max " + max + " characters).";

    if (rule === "email" && !/^[^\s@<>"']+@[^\s@<>"']+\.[^\s@<>"']{2,}$/.test(v)) {
      return "That email does not look right — check for a typo.";
    }
    if (rule === "url" && !/^https:\/\/[^\s<>"']+$/.test(v)) {
      return "Must start with https://";
    }
    if (rule === "url-youtube" && !/^https:\/\/(www\.)?(youtube\.com|youtu\.be)\/[^\s<>"']+$/.test(v)) {
      return "Paste a YouTube link (youtube.com or youtu.be).";
    }
    if (rule === "url-image" && !/^https:\/\/[^\s<>"']+\.(jpg|jpeg|png|webp|gif)(\?[^\s<>"']*)?$/i.test(v) &&
        !/^https:\/\/(drive\.google\.com|images\.ekguru\.shop|ekguru\.shop)\/[^\s<>"']*$/i.test(v)) {
      return "Use a link that ends in .jpg/.png/.webp, or a Google Drive share link.";
    }
    if (rule === "price") {
      var n = Number(v);
      if (!isFinite(n) || n !== Math.round(n)) return "Use a whole dollar amount.";
      if (n < 1 || n > 200) return "Price must be between $1 and $200.";
    }
    if (rule === "phone") {
      /* The number itself is normalised at payload-build time (see
         normalisePhone) so the sheet holds the same digits the server would
         compute, not whatever spacing the tutor used. */
      /* Mirrors the server rule exactly: 7-15 digits, a leading "+" kept,
         no country code invented. */
      var digits = v.replace(/[^0-9]/g, "");
      if (/[^0-9+()\-.\s]/.test(v)) return "Use digits only, with an optional + for the country code.";
      if (digits.length < 7 || digits.length > 15) {
        return "That number should have 7 to 15 digits, including the country code.";
      }
      if (v.indexOf("+") > 0) return "Put the + at the start, e.g. +91 98765 43210.";
    }
    return "";
  }

  /* ---------------------------------------------------------
     Field state
     ---------------------------------------------------------
     One place that decides what a field looks like: normal, focused,
     valid, invalid, disabled. The class on the wrapper drives the circle
     tick in the CSS, and aria-invalid drives the colour — so the two
     signals never disagree, and colour is never the only one.
     --------------------------------------------------------- */
  function wrapperOf(el) {
    return el.closest(".jw-field") || el.closest(".jw-chipgroup") || el.parentNode;
  }

  function markValid(el, ok) {
    var field = wrapperOf(el);
    if (!field || !field.classList) return;
    field.classList.toggle("is-invalid", !ok);
    field.classList.toggle("is-valid", !!ok);
  }

  /* A day row's time inputs live inside .jw-slots, whose error box is the
     shared #jw-avail-e at the bottom of the days block — not a per-input
     .jw-err. Without this the per-day message had nowhere to appear and the
     applicant only saw a red border with no sentence. */
  function dayErrorBox(el) {
    var row = el.closest(".jw-day");
    if (!row) return null;
    var block = row.closest(".jw-days");
    if (!block) return null;
    var sib = block.nextElementSibling;
    if (sib && sib.classList && sib.classList.contains("jw-err")) return sib;
    return $(".jw-err", block) || null;
  }

  function showError(el, msg) {
    var field = wrapperOf(el);
    var box = field ? $(".jw-err", field) : null;
    if (!box && !el.closest(".jw-day")) box = dayErrorBox(el);
    /* A day's time input has no error box of its own. Its sentence is the
       SHARED line under the whole days block, which is rebuilt from every
       ticked day by refreshDayErrors() — writing one message here would
       replace the other broken days' messages with just this one. */
    if (!box && el.id) box = document.getElementById(el.id + "-e");
    if (msg) {
      el.setAttribute("aria-invalid", "true");
      if (box) {
        box.textContent = msg;
        box.classList.add("is-on");
        if (box.id && String(el.getAttribute("aria-describedby") || "").indexOf(box.id) === -1) {
          el.setAttribute("aria-describedby",
            ((el.getAttribute("aria-describedby") || "") + " " + box.id).trim());
        }
      }
      markValid(el, false);
    } else {
      el.removeAttribute("aria-invalid");
      if (box) { box.textContent = ""; box.classList.remove("is-on"); }
      markValid(el, !!val(el));
    }
  }

  /* ---------------------------------------------------------
     Step-wise validation
     ---------------------------------------------------------
     validateStep(form, i) is the ONLY thing that decides whether a step may
     be left. It returns { ok, errors:[{ el, label, msg }] } and it is used by
     Next, by the progress chips, by Submit, and by the tests.

     Rules it follows, because the brief is explicit about them:
       · optional fields never block;
       · a [data-when] field is checked ONLY while it is actually shown and
         enabled — a hidden conditional is never required;
       · chip groups are checked through data-need-min, not per checkbox;
       · availability is checked as a whole (at least one day, times in order);
       · the biography has NO minimum word count (the counter is advice).
     --------------------------------------------------------- */
  function stepLabel(stepEl) {
    var h = $("h2", stepEl);
    if (!h) return "This step";
    return String(h.textContent || "").replace(/[^\w\s&,'’\-]/g, "").trim() || "This step";
  }

  function fieldLabel(el) {
    var data = el.getAttribute("data-label");
    if (data) return data;
    var field = wrapperOf(el);
    var lab = field ? $("label", field) : null;
    if (lab) {
      var text = String(lab.textContent || "").replace(/\*/g, "").replace(/optional/gi, "").trim();
      if (text) return text.split("\n")[0].trim();
    }
    return el.name ? el.name.replace(/_/g, " ") : "This field";
  }

  /* Is this element inside a conditional block that is currently off? */
  function isHiddenConditional(el) {
    var box = el.closest("[data-when]");
    if (!box) return false;
    return box.hidden === true || el.disabled === true;
  }

  /* The consent sentences. Kept together so the wording the applicant reads
     and the wording the summary lists can never drift apart. */
  var CONSENT_MSG = "Please tick this box before submitting.";
  function CONSENT_MSG_FOR(el) {
    if (el && el.id === "jw-consent-data") {
      return "Please confirm that the details you have given are true, so we can review your application.";
    }
    if (el && el.id === "jw-consent-privacy") {
      return "Please agree that we may keep these details to review your application and reply to you.";
    }
    return CONSENT_MSG;
  }

  function validateStep(form, index) {
    var all = steps(form);
    var stepEl = all[index];
    if (!stepEl) return { ok: true, errors: [] };
    var errors = [];

    function add(el, label, msg) {
      errors.push({ el: el, label: label, msg: msg });
    }

    /* 1. single controls */
    $$("[name]", stepEl).forEach(function (el) {
      if (el.disabled) return;
      if (el.type === "checkbox" || el.type === "radio") {
        /* A lone required tick box. The day toggles are excluded because a
           day is an ANSWER, not a tick-to-continue: an unticked day is not
           wrong, it is simply not offered. The consent boxes are the
           opposite — an unticked one is the whole reason submit is blocked,
           so they get their own sentence naming the box. */
        if (el.required && el.closest(".jw-day") === null && !el.checked) {
          add(el, fieldLabel(el), CONSENT_MSG_FOR(el));
        }
        return;
      }
      if (isHiddenConditional(el)) return;
      if (!el.required && !val(el)) return;      /* empty optional: fine */
      var msg = fieldError(el);
      if (msg) add(el, fieldLabel(el), msg);
    });

    /* 2. chip groups (subjects / levels / methods) */
    $$("[data-need-min]", stepEl).forEach(function (grp) {
      var name = grp.getAttribute("data-need-min");
      var min = parseInt(grp.getAttribute("data-min") || "1", 10);
      if (checkedValues(form, name).length >= min) return;
      var first = $('input[name="' + name + '"]', grp);
      var label = grp.getAttribute("data-label") || fieldLabel(first) || "This choice";
      add(first, label, grp.getAttribute("data-msg") || "Select at least one option.");
    });

    /* 3. availability (a step 5 special: the day rows are not [name]ed
          as a unit, and the times need cross-checking) */
    if (stepEl.querySelector("[data-day]")) {
      var av = readAvailability(form);
      if (!av.any) {
        add($("[data-day] input[type='checkbox']", stepEl), "Availability",
          "Please tick at least one day you can teach.");
      } else {
        /* One error PER BROKEN DAY, each carrying the day's own time input as
           its focus target. Listing only the first problem made a tutor fix
           Monday, press Continue, and discover Tuesday was broken too. */
        var issues = availabilityIssues(form);
        issues.forEach(function (issue) {
          add(issue.el, issue.day, issue.msg);
        });
        /* The shared line under the days block lists EVERY broken day. It is
           refreshed here rather than only on input, so pressing Continue
           cannot leave a stale single-day sentence behind. */
        refreshDayErrors(form);
        if (!issues.length) refreshDayErrors(form);
      }
    }

    return { ok: errors.length === 0, errors: errors };
  }

  /* Every step, in order, answered without touching the DOM. Used by the
     progress chips and by the final check. */
  function stepState(form) {
    var all = steps(form);
    var out = [];
    for (var i = 0; i < all.length; i++) {
      var r = validateStep(form, i);
      out.push({ index: i, ok: r.ok, count: r.errors.length, errors: r.errors });
    }
    return out;
  }

  /* ---------------------------------------------------------
     The error summary at the top of a step
     --------------------------------------------------------- */
  function clearSummary(stepEl) {
    var box = $("[data-jw-summary]", stepEl);
    if (!box) return;
    box.hidden = true;
    var list = $("[data-jw-summary-list]", box);
    if (list) list.innerHTML = "";
    var title = $("[data-jw-summary-title]", box);
    if (title) title.textContent = "";
  }

  function renderSummary(form, stepEl, errors) {
    var box = $("[data-jw-summary]", stepEl);
    if (!box) return;
    /* A step can hold more than one summary slot (the status line); use the
       first real block. */
    var list = $("[data-jw-summary-list]", box);
    var title = $("[data-jw-summary-title]", box);
    if (!list || !errors.length) { clearSummary(stepEl); return; }

    var n = errors.length;
    title.textContent = "Please complete " + n + (n === 1 ? " item" : " items") + " before continuing.";

    list.innerHTML = "";
    errors.forEach(function (err) {
      var li = document.createElement("li");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = err.label + " — ";
      btn.setAttribute("data-jw-jump", "1");
      var span = document.createElement("span");
      span.textContent = err.msg;
      li.appendChild(btn);
      li.appendChild(span);
      btn.addEventListener("click", function () {
        focusField(form, err.el, err.msg);
      });
      list.appendChild(li);
    });

    box.hidden = false;
    /* Announce it, but do not steal focus from the field the tutor was in:
       role="alert" does the announcing. */
  }

  /* Show one field's error, scroll to it, focus it, and re-announce. */
  function focusField(form, el, msg) {
    if (!el) return;
    if (el.type === "checkbox" || el.type === "radio") {
      var group = el.closest(".jw-chipgroup") || el.closest("[data-need-min]") || wrapperOf(el);
      if (group) {
        var box = $(".jw-err", group.parentNode) || $(".jw-err", group);
        if (box && msg) { box.textContent = msg; box.classList.add("is-on"); }
        if (group.classList) group.classList.add("is-invalid");
      }
    } else if (el.closest(".jw-day")) {
      /* A day's time input: mark it invalid and focus it, but never touch the
         shared line — refreshDayErrors() owns that and already lists every
         broken day. */
      el.setAttribute("aria-invalid", "true");
      var dayRow = el.closest(".jw-day");
      if (dayRow && dayRow.classList) dayRow.classList.add("is-invalid");
    } else {
      showError(el, msg || fieldError(el));
    }
    try { el.scrollIntoView({ behavior: motion(), block: "center" }); } catch (e) {}
    try { el.focus({ preventScroll: true }); } catch (e2) { try { el.focus(); } catch (e3) {} }
    var field = wrapperOf(el);
    if (field && field.scrollIntoView) {
      try { field.scrollIntoView({ behavior: motion(), block: "center" }); } catch (e4) {}
    }
  }

  function motion() {
    try {
      return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ? "auto" : "smooth";
    } catch (e) { return "auto"; }
  }

  /* ---------------------------------------------------------
     Payload — built from the schema, not from a hand-written list.
     ---------------------------------------------------------
     apps-script/ApplicationSchema.gs (copied to js/join-schema.js by
     tools/build-join-schema.mjs) says which field lands in which column.
     Anything the page collects that has NO column is carried in `details`,
     which the server stores in details_json — the documented overflow
     bucket. That is the difference between this build and the last one:
     the last one collected five fields (`intro`, `other_langs`,
     `edu_extra`, `less_exp`, `bed_detail`) and then dropped them on the
     floor, with no error, so a tutor's words vanished.
     --------------------------------------------------------- */
  var SCHEMA = window.EKGURU_APP_SCHEMA || null;

  /* The ticked values of one checkbox group, in document order. */
  function checkedValues(form, groupName) {
    return $$('input[name="' + groupName + '"]:checked', form).map(function (el) {
      return String(el.value || "").trim();
    }).filter(Boolean);
  }

  /* Every control in the form, by its `name`, as the value a person typed.
     Grouped checkboxes (subjects, levels, methods) become arrays. A blank
     input is "" and is left out of the payload by the caller. */
  function collectNamed(form) {
    var out = {};
    $$("input, select, textarea", form).forEach(function (el) {
      if (!el.name || el.disabled) return;
      if (el.name === "website") return;           /* honeypot, never posted */
      if (el.name === "consent" || el.name === "consent_privacy") return;
      /* The day rows are MECHANICS, not answers: availabilitySlots() turns
         them into availability_slots. Without this they would also land in
         details_json as "day-mon: on", which is noise in the owner's row. */
      if (/^day-(mon|tue|wed|thu|fri|sat|sun)$/.test(el.name)) return;
      if (/^(mon|tue|wed|thu|fri|sat|sun)-(from|to)$/.test(el.name)) return;
      if (el.type === "checkbox") {
        if (/^(subjects|levels|methods|teachLangs)$/.test(el.name)) {
          if (el.checked && val(el)) (out[el.name] = out[el.name] || []).push(val(el));
          return;
        }
        if (!el.checked) return;
        out[el.name] = val(el) || "yes";
        return;
      }
      if (el.type === "radio") {
        if (el.checked) out[el.name] = val(el);
        return;
      }
      var v = val(el);
      if (v !== "") out[el.name] = v;
    });
    return out;
  }

  /* Day slots in the canonical shape the server validates: Monday first,
     {day, from, to}. Skipped days simply have no entry. */
  function availabilitySlots(form) {
    var slots = [];
    DAYS.forEach(function (d) {
      var row = $('[data-day="' + d + '"]', form);
      if (!row) return;
      var on = $('input[type="checkbox"]', row);
      if (!on || !on.checked) return;
      var from = val($('input[name="' + d.toLowerCase() + '-from"]', form));
      var to = val($('input[name="' + d.toLowerCase() + '-to"]', form));
      if (from && to) slots.push({ day: d, from: from, to: to });
    });
    return slots;
  }

  /* Digits only, with a leading "+" kept when the tutor typed one. This
     mirrors ApplicationIntake.gs exactly: no country code is ever invented,
     so 9876543210 stays 9876543210 and +919876543210 stays
     +919876543210. Storing the tidy form means the sheet does not collect
     three spellings of one number. */
  function normalisePhone(v) {
    var s = String(v == null ? "" : v).trim();
    if (!s) return "";
    var plus = /^\+/.test(s);
    var digits = s.replace(/[^0-9]/g, "");
    if (!digits) return "";
    return (plus ? "+" : "") + digits;
  }

  function buildPayload(form) {
    var typed = collectNamed(form);
    var slots = availabilitySlots(form);
    var consentData = $("#jw-consent-data", form);
    var consentPrivacy = $("#jw-consent-privacy", form);

    var payload = {};
    var details = {};
    var used = {};
    var fields = (SCHEMA && SCHEMA.fields) || [];

    /* 1. straight from the schema: payload key -> the column it belongs to */
    fields.forEach(function (f) {
      if (!f.src) return;                          /* server-owned column */
      if (SCHEMA.serverOnly.indexOf(f.col) !== -1) return;  /* never sent */
      var v = typed[f.src];
      if (v === undefined) return;
      if (Object.prototype.toString.call(v) === "[object Array]") {
        if (!v.length) return;
        payload[f.src] = v;
      } else if (String(v).trim() !== "") {
        payload[f.src] = String(v).trim();
      }
      used[f.src] = 1;
    });

    /* 2. the values the page DERIVES rather than reads off one control.
          These are the columns the old backend already had and that the
          public profile prints, so they must keep being filled even though
          the wizard collects the same facts as chips and selects. */
    var subjects = typed.subjects || [];
    var levels = typed.levels || [];
    var teachLangs = typed.teachLangs || [];

    if (subjects.length && !payload.subject) {
      payload.subject = clip(subjects.join(", "), LIMITS.subject);
    }
    var langBits = [];
    if (teachLangs.length) langBits.push(teachLangs.join(", "));
    if (typed.hindi_level) langBits.push("Hindi: " + typed.hindi_level);
    if (typed.english_level) langBits.push("English: " + typed.english_level);
    if (typed.other_langs) langBits.push(typed.other_langs);
    if (langBits.length) {
      payload.languages = clip(langBits.join(", "), LIMITS.languages);
    }
    var expBits = [];
    if (typed.years) expBits.push(typed.years);
    if (levels.length) expBits.push("Teaches: " + levels.join(", "));
    if (expBits.length) {
      payload.experience = clip(expBits.join(" \u00b7 "), LIMITS.experience);
    }

    /* The phone is normalised, not rewritten: the digits the tutor typed are
       the digits we store. */
    if (payload.whatsapp) {
      var cleanPhone = normalisePhone(payload.whatsapp);
      if (cleanPhone) payload.whatsapp = cleanPhone;
      else delete payload.whatsapp;
    }

    /* 3. the two things that are not simple named controls */
    if (slots.length) {
      payload.availability_slots = slots;
      payload.availability_meta = {
        days: slots.length,
        timezone: typed.timezone || "",
        format: "weekly-hours"
      };
    }
    /* NOTE: consent is a top-level flag on the request body, sent by
       js/intake.js from the same checkbox. Putting a copy inside `fields`
       made the server file it under details_json as noise. */

    /* 4. anything typed that the schema has no column for → details.
          This is the guard against silent loss, so it is deliberately
          computed from what was ACTUALLY typed, not from a list. */
    Object.keys(typed).forEach(function (k) {
      if (used[k]) return;
      var v = typed[k];
      if (Object.prototype.toString.call(v) === "[object Array]") {
        if (!v.length) return;
        details[k] = v.join(", ").slice(0, 300);
      } else if (String(v).trim() !== "") {
        details[k] = String(v).trim().slice(0, 300);
      }
    });
    if (Object.keys(details).length) payload.details = details;

    /* 5. an availability line even when only one day was filled, so the
          pre-existing `availability` column keeps its human value */
    if (slots.length && !payload.availability) {
      payload.availability = clip(
        slots.map(function (x) { return x.day + " " + x.from + "-" + x.to; }).join("; ") +
        (typed.timezone ? " | " + typed.timezone : ""),
        LIMITS.availability
      );
    }

    /* 6. consent — the server keeps its own copy; these two are what it
          records, and they are never trusted from the payload alone */
    var consentGiven = !!(consentData && consentData.checked);

    /* 7. If the schema file did not load (an old cached page, a blocked
          request), fall back to the 13 columns Intake.gs v1.2.0 accepts
          rather than posting an empty object and reporting success. The
          tutor must never be told "saved" by a payload with nothing in it. */
    if (!fields.length) {
      var legacy = {
        name: typed.name, email: typed.email, city: typed.city, country: typed.country,
        subject: clip((typed.subjects || []).join(", "), LIMITS.subject),
        experience: [typed.years, (typed.levels || []).length ? "Teaches: " + typed.levels.join(", ") : ""]
          .filter(Boolean).join(" \u00b7 "),
        rate_usd: typed.rate_usd,
        availability: payload.availability,
        bio: typed.bio,
        photo_link: typed.photo_link,
        video_link: typed.video_link,
        languages: clip([(typed.hindi_level ? "Hindi: " + typed.hindi_level : ""),
                         (typed.english_level ? "English: " + typed.english_level : "")]
                        .filter(Boolean).join(", "), LIMITS.languages),
        notes: clip(detailsToNotes(details), LIMITS.notes)
      };
      var out = {};
      Object.keys(legacy).forEach(function (k) {
        if (legacy[k] !== undefined && String(legacy[k]).trim() !== "") out[k] = legacy[k];
      });
      out.consent = consentGiven;
      return out;
    }
    return payload;
  }

  /* "label: value; label: value" — the note the old backend stored. */
  function detailsToNotes(details) {
    return Object.keys(details).map(function (k) {
      return k.replace(/_/g, " ") + ": " + details[k];
    }).join("; ");
  }

  /* ---------------------------------------------------------
     Preview + completion. Built from the same payload, so what a
     tutor previews is what gets posted — not a separate drawing
     of the form that could drift.
     --------------------------------------------------------- */
  function initials(name) {
    return String(name || "").trim().split(/\s+/).slice(0, 2)
      .map(function (w) { return w.charAt(0).toUpperCase(); }).join("") || "?";
  }

  function renderPreview(form) {
    var p = buildPayload(form);
    var head = $("[data-jw-pv-head]", form);
    if (head) {
      var av = $(".jw-preview-avatar", head);
      var photo = photoPreviewUrl(p.photo_link);
      if (photo) {
        av.style.backgroundImage = 'url("' + photo.replace(/"/g, "%22") + '")';
        av.textContent = "";
      } else {
        av.style.backgroundImage = "";
        av.textContent = initials(p.name);
      }
      var h3 = $("h3", head);
      if (h3) h3.textContent = val($('#jw-display', form)) || p.name || "Your name";
      var sub = $("p", head);
      if (sub) {
        sub.textContent = [p.city, p.country].filter(Boolean).join(", ") || "City, country";
      }
    }

    var map = {
      headline: val($('#jw-headline', form)),
      bio: p.bio,
      subject: p.subject,
      levels: checkedValues(form, "levels").join(", "),
      languages: p.languages,
      experience: p.experience,
      education: [val($('#jw-edu-qual', form)), val($('#jw-edu-inst', form)),
        val($('#jw-edu-year', form))].filter(Boolean).join(", "),
      video: p.video_link,
      /* No invented lesson length: an unpicked duration must read as "not
         chosen yet", not as the 50 min the server would default to. */
      price: p.rate_usd ? "$" + p.rate_usd + (val($('#jw-duration', form)) ? " / " + val($('#jw-duration', form)) : "") : "",
      availability: p.availability
    };
    /* Extra section: whatever the tutor chose to tell us on step 6. */
    map.extra = [val($("#jw-why", form)), val($("#jw-referral", form)),
      val($("#jw-contact-pref", form))].filter(Boolean).join(" · ");
    map.media = [p.photo_link ? "Photo added" : "", p.video_link ? "Video added" : ""]
      .filter(Boolean).join(" · ");

    Object.keys(map).forEach(function (k) {
      var dd = $('[data-jw-pv="' + k + '"]', form);
      if (!dd) return;
      var v = map[k];
      dd.textContent = v || "Not added yet";
      dd.classList.toggle("missing", !v);
    });

    /* Completion checklist. Required items block submission;
       optional ones are listed so a tutor can see what would make
       the profile stronger without being forced. */
    var required = [
      ["Full legal name", !!p.name],
      ["Email address", !!p.email],
      ["City and country", !!(p.city && p.country)],
      ["At least one subject", !!p.subject],
      /* no word minimum: the counter under the box is advice, not a rule */
      ["Your teaching introduction", !!p.bio],
      ["Price per lesson", !!p.rate_usd],
      ["Weekly availability", readAvailability(form).any && !availabilityProblem(form)],
      ["Consent", !!(form.querySelector('#jw-consent-data') || {}).checked]
    ];
    var optional = [
      ["Profile photo link", !!p.photo_link],
      ["Professional headline", !!val($('#jw-headline', form))],
      ["Introduction video", !!p.video_link],
      ["Qualification details", !!val($('#jw-edu-qual', form))]
    ];

    var list = $("[data-jw-checklist]", form);
    if (list) {
      list.innerHTML = "";
      required.concat(optional).forEach(function (row, i) {
        var li = document.createElement("li");
        var ok = row[1];
        var isOpt = i >= required.length;
        li.className = ok ? "ok" : (isOpt ? "" : "no");
        var mark = document.createElement("span");
        mark.className = "m";
        mark.textContent = ok ? "✓" : (isOpt ? "○" : "!");
        li.appendChild(mark);
        var txt = document.createElement("span");
        txt.textContent = row[0] + (isOpt ? " (optional)" : "");
        li.appendChild(txt);
        list.appendChild(li);
      });
    }

    var missing = required.filter(function (r) { return !r[1]; }).map(function (r) { return r[0]; });
    var done = required.length - missing.length;
    var pct = Math.round((done / required.length) * 100);

    /* The percentage is measured in STEPS, not in checklist rows: that is
       what the brief asks for ("completion percentage, completed and
       incomplete steps"), and it means a step counts only once its own
       validator passes — not once a box happens to have text in it. */
    var states = stepState(form);
    var doneSteps = states.filter(function (x) { return x.ok; }).length;
    var stepPct = Math.round((doneSteps / states.length) * 100);

    var pctEl = $("[data-jw-pct]", form);
    if (pctEl) pctEl.textContent = stepPct + "%";
    var pctBar = $("[data-jw-pctbar]", form);
    if (pctBar) pctBar.style.width = stepPct + "%";
    var pctTrack = $("[data-jw-pcttrack]", form);
    if (pctTrack) {
      pctTrack.setAttribute("role", "progressbar");
      pctTrack.setAttribute("aria-valuemin", "0");
      pctTrack.setAttribute("aria-valuemax", "100");
      pctTrack.setAttribute("aria-valuenow", String(stepPct));
      pctTrack.setAttribute("aria-valuetext", doneSteps + " of " + states.length +
        " steps complete");
    }

    /* Submit is enabled by VALIDATION, never by the checklist: if the seven
       step validators all pass, the application is submittable. */
    var allGood = states.every(function (x) { return x.ok; });
    var submit = $(".jw-submit", form);
    if (submit) submit.disabled = !allGood;
    return { payload: p, complete: allGood, pct: stepPct,
      doneSteps: doneSteps, totalSteps: states.length,
      missing: missing, stepErrors: states };
  }

  /* ---------------------------------------------------------
     Step machine
     --------------------------------------------------------- */
  function steps(form) { return $$(".jw-step", form); }

  function showStep(form, idx, opts) {
    opts = opts || {};
    var all = steps(form);
    if (!all.length) return;
    idx = Math.max(0, Math.min(all.length - 1, idx));

    all.forEach(function (s, i) {
      var active = i === idx;
      s.classList.toggle("is-active", active);
      s.hidden = !active;
    });

    /* Coming back to step 5 must show the day rows as they really are, not as
       the static markup left them. Cheap and idempotent. */
    if (all[idx] && all[idx].querySelector("[data-day]")) syncDayRows(form);

    var states = stepState(form);
    $$(".jw-steps li", form).forEach(function (li, i) {
      /* aria-current and the roving tabindex belong on the BUTTON inside the
         chip, not on the list item: the li is not an interactive element. */
      var chip = $("button", li);
      if (chip) {
        if (i === idx) chip.setAttribute("aria-current", "step");
        else chip.removeAttribute("aria-current");
        chip.tabIndex = i === idx ? 0 : -1;
      }
      li.classList.toggle("is-current", i === idx);
      /* DONE means "validated", not "visited": a step the tutor walked
         through with an empty name is not done, and a step they went back
         and broke stops being done. */
      li.classList.toggle("is-done", states[i] && states[i].ok);
      li.classList.toggle("is-error", !!(states[i] && !states[i].ok && i < idx));
      var state = $("[data-jw-stepstate]", li);
      if (state) {
        state.textContent = i === idx ? " current step"
          : (states[i] && states[i].ok) ? " completed"
          : (states[i] ? " " + states[i].count + " item(s) still needed" : "");
      }
    });

    var bar = $(".jw-bar i", form);
    if (bar) bar.style.width = ((idx + 1) / all.length * 100) + "%";
    var track = $("[data-jw-track]", form);
    if (track) {
      track.setAttribute("role", "progressbar");
      track.setAttribute("aria-valuemin", "0");
      track.setAttribute("aria-valuemax", String(all.length));
      track.setAttribute("aria-valuenow", String(idx + 1));
      track.setAttribute("aria-label", "Step " + (idx + 1) + " of " + all.length);
    }
    var label = $("[data-jw-steplabel]", form);
    if (label) label.textContent = "Step " + (idx + 1) + " of " + all.length;
    var name = $("[data-jw-stepname]", form);
    if (name) {
      var li = $$(".jw-steps li", form)[idx];
      name.textContent = li ? (li.getAttribute("data-step-name") || stepLabel(all[idx])) : stepLabel(all[idx]);
    }
    var doneCount = states.filter(function (x) { return x.ok; }).length;
    var note = $("[data-jw-progressnote]", form);
    if (note) {
      note.textContent = doneCount === 0
        ? "Nothing goes live until we have checked you"
        : doneCount + " of " + all.length + " steps complete";
    }

    var back = $(".jw-back", form);
    if (back) back.disabled = idx === 0;

    form.setAttribute("data-jw-step", String(idx));

    /* Focus the new step's heading so a screen reader announces the
       change of context instead of leaving focus on a dead button. */
    if (!opts.silent) {
      var h = $("h2", all[idx]);
      if (h) {
        h.setAttribute("tabindex", "-1");
        try { h.focus({ preventScroll: true }); } catch (e) { h.focus(); }
      }
      var card = $(".jw-card", form);
      if (card && !opts.noScroll) {
        var y = card.getBoundingClientRect().top + window.pageYOffset - 90;
        window.scrollTo({ top: y < 0 ? 0 : y, behavior: "smooth" });
      }
    }
  }

  /* data-when="years:Less than 1 year" -> true when that select (or the
     checkbox group with that name) holds that value. A blank value means
     "anything not empty". */
  function shouldShow(form, box) {
    var spec = String(box.getAttribute("data-when") || "");
    var cut = spec.indexOf(":");
    var name = cut === -1 ? spec : spec.slice(0, cut);
    var want = cut === -1 ? "" : spec.slice(cut + 1);
    var el = form.querySelector('[name="' + name + '"]');
    if (!el) return false;
    if (el.type === "checkbox") {
      var picked = checkedValues(form, name);
      return want ? picked.indexOf(want) !== -1 : picked.length > 0;
    }
    var v = val(el);
    return want ? v === want : !!v;
  }

  function syncConditionals(form) {
    $$("[data-when]", form).forEach(function (box) {
      var on = shouldShow(form, box);
      box.hidden = !on;
      $$("[name]", box).forEach(function (el) { el.disabled = !on; });
    });
  }

  /* ---------------------------------------------------------
     Submit. Delegates to js/intake.js — the same endpoint, the
     same consent + honeypot, the same reference reply. The only
     thing added is duplicate protection and a clearer message.
     --------------------------------------------------------- */
  function setStatus(form, text, kind) {
    var box = $("[data-jw-status]", form);
    if (!box) return;
    box.className = "jw-status is-on " + (kind === "ok" ? "is-ok" : kind === "err" ? "is-err" : "is-info");
    box.textContent = text;
  }

  function submitViaIntake(form, payload, done) {
    var api = window.EkGuruIntake;
    if (!api || !api.ready || !api.ready()) {
      done({ urlFallback: true });
      return;
    }
    var consentEl = $("#jw-consent-data", form);
    var honey = $('[name="website"]', form);
    api.submit("application", payload, !!(consentEl && consentEl.checked), honey ? val(honey) : "")
      .then(function (res) {
        if (res && res.ok) done({ ok: true, reference: res.reference });
        else if (res && res.fallback) done({ fallback: true, error: res.error });
        else done({ error: (res && res.error) || "We could not send that." });
      })
      .catch(function () { done({ fallback: true }); });
  }

  /* A self-contained mailto fallback. Used when the intake endpoint
     is off or unreachable, so an application is never silently
     lost — the tutor still gets a working email with everything in
     it, and is told plainly what happened. */
  function mailtoFallback(form, payload) {
    var lines = [
      "EkGuru tutor application",
      "",
      "Name: " + payload.name,
      "Email: " + payload.email,
      "City: " + payload.city,
      "Country: " + payload.country,
      "Teaches: " + payload.subject,
      "Price (USD / 50 min): " + (payload.rate_usd || ""),
      "Languages: " + payload.languages,
      "Availability: " + payload.availability,
      "Experience: " + payload.experience,
      "Photo: " + payload.photo_link,
      "Video: " + payload.video_link,
      "",
      "About me:",
      payload.bio,
      "",
      "Extra details:",
      payload.notes,
      "",
      "Consent: yes — EkGuru may keep these details to review this application."
    ];
    var href = "mailto:EkGuruLearning@gmail.com"
      + "?subject=" + encodeURIComponent("Tutor application — " + payload.name)
      + "&body=" + encodeURIComponent(lines.join("\n"));
    var a = document.createElement("a");
    a.href = href;
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { a.remove(); }, 1000);
  }

  function showDone(form, reference) {
    var shell = $(".jw-shell", form) || form;
    var card = $(".jw-card", form);
    /* The success block lives AFTER </form> on purpose: it is not an
       input and must never be posted. So look it up document-wide. */
    var done = document.querySelector("[data-jw-done]");
    steps(form).forEach(function (s) { s.hidden = true; s.classList.remove("is-active"); });
    var prog = $(".jw-progress", form);
    if (prog) prog.hidden = true;
    var nav = $(".jw-nav", form);
    if (nav) nav.hidden = true;
    var rail = $(".jw-rail");
    if (rail) rail.hidden = true;
    if (done) {
      done.hidden = false;
      var ref = $("[data-jw-ref]", done);
      if (ref) ref.textContent = reference || "—";
    } else if (card) {
      card.innerHTML = '<div class="jw-done"><div class="tick">✓</div>' +
        "<h2>Application received</h2>" +
        "<p>Your reference is <span class=\"jw-ref\" data-jw-ref>" + (reference || "—") + "</span></p>" +
        "<p class=\"muted\">We review every application by hand. You will get an email at the address you gave us, usually within a few days.</p></div>";
    }
    if (shell) shell.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  /* The bio counter is ADVICE. It counts words so a tutor can see whether
     they are in the useful range, and it never turns into a requirement —
     fieldError() only rejects an empty bio. */
  function updateWordCount(form) {
    var bio = $("#jw-bio", form);
    var out = $("[data-jw-wordcount]", form);
    if (!bio || !out) return;
    var n = words(val(bio));
    out.textContent = n === 1 ? "1 word" : n + " words";
    var hint = $("[data-jw-wordhint]", form);
    if (hint) {
      hint.textContent = n === 0 ? "Aim for 150–250 words — a few honest sentences is plenty to start."
        : n < 60 ? "Good start. Aim for 150–250 words so students can picture your lessons."
        : n <= 250 ? "That is a good length." : "That is long — students skim. 150–250 words works best.";
    }
  }

  /* ---------------------------------------------------------
     Photo preview — "is this the face I meant to send?"
     ---------------------------------------------------------
     A tutor pastes a Google Drive *share* link, which is a web PAGE, not
     an image. Putting that page URL into a CSS background loads nothing,
     so the earlier build showed an empty box even for a perfect photo.
     The link the browser needs is the drive file id rewritten to the
     direct-image host; js/sheet.js already owns that conversion for
     every tutor card on the site (EkGuruSheet.photoUrl), so the form
     calls it rather than keeping a second copy of the same regexes that
     could drift from the one the public pages use.
     --------------------------------------------------------- */
  function photoPreviewUrl(raw) {
    var v = String(raw == null ? "" : raw).trim();
    if (!v) return "";
    var S = window.EkGuruSheet;
    if (S && typeof S.photoUrl === "function") {
      var resolved = S.photoUrl(v);
      if (resolved) return String(resolved);
      /* photoUrl() returns null for a URL it will not vouch for. Fall
         through to the plain https check so a valid-but-unlisted host
         still previews instead of silently showing nothing. */
    }
    return /^https:\/\//i.test(v) ? v : "";
  }

  function updatePhotoPreview(form) {
    var input = $("#jw-photo", form);
    var box = $("[data-jw-photo-preview]", form);
    if (!input || !box) return;
    var raw = val(input);
    var src = raw && !fieldError(input) ? photoPreviewUrl(raw) : "";
    if (!src) {
      clearPhotoPreview(box);
      return;
    }
    box.style.backgroundImage = 'url("' + src.replace(/"/g, "%22") + '")';
    box.textContent = "";
    /* .has-img, not .has-image: this is the class css/join-wizard.css
       stylehooks (.jw-photo-preview.has-img). Keyboard and screen-reader
       users get the same information as the picture: the tile is
       labelled, so "it loaded" and "it is a photo of you" are announced
       rather than inferred from a colour. */
    box.classList.add("has-img");
    box.classList.remove("is-broken");
    box.setAttribute("role", "img");
    box.setAttribute("aria-label", "Preview of the photo you linked");
    probePhoto(src, form);
  }

  function clearPhotoPreview(box) {
    if (!box) return;
    box.style.backgroundImage = "";
    box.textContent = "🖼️";
    box.classList.remove("has-img", "is-broken");
    box.removeAttribute("role");
    box.removeAttribute("aria-label");
    box.setAttribute("aria-hidden", "true");
  }

  /* A URL can pass every check and still fail to load: the Drive file was
     made private again, or deleted. background-image gives no error event,
     so the tile is probed with an Image() once; a failure says so out loud
     rather than leaving the tutor staring at an empty square wondering
     whether their photo was received. */
  function probePhoto(url, form) {
    if (!url || typeof window.Image !== "function") return;
    var box = $("[data-jw-photo-preview]", form);
    if (!box) return;
    var stamp = box.getAttribute("data-jw-photo-src");
    if (stamp === url) return;                 /* already probed this URL */
    box.setAttribute("data-jw-photo-src", url);
    var img = new window.Image();
    img.onload = function () {
      if (box.getAttribute("data-jw-photo-src") !== url) return;
      box.classList.remove("is-broken");
    };
    img.onerror = function () {
      if (box.getAttribute("data-jw-photo-src") !== url) return;
      box.classList.remove("has-img");
      box.classList.add("is-broken");
      box.style.backgroundImage = "";
      box.textContent = "⚠️";
      box.setAttribute("role", "img");
      box.setAttribute("aria-label",
        "That link did not load a picture. In Google Drive, set sharing to Anyone with the link.");
    };
    img.src = url;
  }

  /* ---------------------------------------------------------
     Wiring
     --------------------------------------------------------- */
  function init() {
    var form = $("#jw-form");
    if (!form) return;

    /* ---------------------------------------------------------
       BOTH the wrapper and the form must be marked.
       ---------------------------------------------------------
       css/join-wizard.css gates the navigation on the OUTER wrapper:

           .jw:not(.jw-on) .jw-nav { display: none; }

       #jw-form carries the class `jw-form`, NOT `jw`, so it never matches
       that selector. Marking only the form left the wrapper permanently
       `.jw:not(.jw-on)`, and the nav strip — a descendant of BOTH — stayed
       display:none even though the wizard had initialised perfectly.

       That is why the buttons were invisible while every DOM-only test
       passed: the buttons existed, were enabled and were wired, and CSS
       painted them at zero height.

       The tests missed it because they only ever asserted DOM state. jsdom
       DOES resolve the cascade through getComputedStyle, so a
       display:none assertion was always possible — it just was not written.
       tools/test-join-css-visibility.mjs now does exactly that, and it
       fails if the outer wrapper loses this class.
       --------------------------------------------------------- */
    var root = form.closest(".jw") || document.getElementById("jw");
    if (root) root.classList.add("jw-on");

    /* Kept for compatibility with anything that looks at the form itself. */
    form.classList.add("jw-on");

    var total = steps(form).length;
    if (!total) return;
    var lastIndex = total - 1;

    /* The single door between steps. Re-rendering the preview here
       rather than inside showStep keeps showStep free of side effects
       and means every path — buttons, step chips, Edit links — gets a
       fresh preview. */
    function go(i, opts) {
      opts = opts || {};
      showStep(form, i, opts);
      if (i === lastIndex) renderPreview(form);
      toggleSubmit(i === lastIndex);
      /* Arriving at a step does not mean it is being "tried": no red
         summary until the tutor presses Continue. But a summary left over
         from an earlier attempt on THIS step must reflect the truth now. */
      var here = steps(form)[i];
      if (here && !opts.keepErrors) {
        var st = validateStep(form, i);
        if (st.ok) clearSummary(here);
      }
      /* Step 1 has nowhere to go back to, so Previous is genuinely disabled
         there and re-enabled everywhere else — including when the tutor
         comes back out of the review step. */
      var back = $(".jw-back", form);
      if (back) {
        back.disabled = i === 0;
        back.setAttribute("aria-disabled", i === 0 ? "true" : "false");
      }
      /* The hint under Submit is only meaningful on the review step, so it is
         refreshed there and cleared everywhere else. */
      if (i === lastIndex) {
        refreshSubmit();
      } else {
        var sh = $("[data-jw-submit-hint]", form);
        if (sh) sh.hidden = true;
      }
      if (!opts.silent) {
        var nameEl = $("[data-jw-stepname]", form);
        announce(form, "Step " + (i + 1) + " of " + total +
          (nameEl && nameEl.textContent ? " — " + nameEl.textContent : ""));
      }
    }

    /* Submit enablement is a pure function of the seven validators, never
       of the checklist (which would re-impose a word count). */
    /* The Submit button is NEVER disabled for "something is unanswered". A
       disabled button swallows the click, so the tutor gets no summary, no
       field error and no sentence — the form simply looks broken. It is
       disabled for exactly one reason: a submission is already in flight.
       Everything else is said out loud by validate-and-jump below. */
    function refreshSubmit() {
      var sb = $(".jw-submit", form);
      if (!sb) return false;
      var states = stepState(form);
      var allGood = states.every(function (x) { return x.ok; });
      sb.disabled = form.getAttribute("data-jw-sending") === "1";
      sb.setAttribute("aria-disabled", sb.disabled ? "true" : "false");
      /* The hint under the button tells the tutor what a click will do right
         now, so the outcome is never a surprise. */
      var hint = $("[data-jw-submit-hint]", form);
      if (hint) {
        var missing = states.filter(function (x) { return !x.ok; }).length;
        hint.textContent = allGood
          ? "Everything you need has been filled in."
          : (missing === 1 ? "1 step still needs an answer — Submit will take you there."
                           : missing + " steps still need an answer — Submit will take you there.");
        hint.hidden = false;
      }
      return allGood;
    }

    /* One polite live region for step changes, so the count and the step
       name are read out without hijacking focus. */
    function announce(scope, text) {
      var live = $("[data-jw-live]", scope) || $("[data-jw-live]");
      if (!live) return;
      live.textContent = "";
      setTimeout(function () { live.textContent = text; }, 40);
    }
    /* The forward control says what pressing it will actually do:
         steps 1-5  "Save & Next ->"        (validate, move on)
         step 6     "Preview Application ->" (the last step before review)
         step 7     hidden; Submit takes over
       A single button with one label for all seven steps made step 6 read
       the same as step 1, which hid the fact that the next screen is the
       final review. */
    var NEXT_LABEL = "Save & Next \u2192";
    var PREVIEW_LABEL = "Preview Application \u2192";

    function toggleSubmit(on) {
      var nx = $(".jw-next", form);
      var sb = $(".jw-submit", form);
      var hint = $(".jw-submit-hint", form);
      if (nx) {
        nx.hidden = !!on;
        if (!on) {
          var cur = parseInt(form.getAttribute("data-jw-step") || "0", 10);
          var label = (cur === lastIndex - 1) ? PREVIEW_LABEL : NEXT_LABEL;
          if (nx.textContent.trim() !== label) nx.textContent = label;
        }
      }
      if (sb) sb.hidden = !on;
      if (hint) hint.hidden = !on;
    }

    /* ---------------------------------------------------------
       Continue. Validates ONLY the step the tutor is standing on. If it is
       clean it advances; if it is not, nothing moves, the summary fills in,
       and focus lands on the first field that needs an answer.
       --------------------------------------------------------- */
    function advance() {
      var cur = parseInt(form.getAttribute("data-jw-step") || "0", 10);
      if (cur >= lastIndex) return;            /* the review step has no Next */
      var here = steps(form)[cur];
      var st = validateStep(form, cur);
      if (!st.ok) {
        /* Availability first: showError() deliberately leaves the days block's
           shared line alone, and refreshDayErrors() writes every broken day
           into it. Doing it before the field errors keeps the order readable
           in a screen reader. */
        paintErrors(form, here, st.errors);
        renderSummary(form, here, st.errors);
        var first = st.errors[0];
        if (first) focusField(form, first.el, first.msg);
        announce(form, "Please complete " + st.errors.length +
          (st.errors.length === 1 ? " item" : " items") + " on this step.");
        setStatus(form, "", "info");
        return;
      }
      clearSummary(here);
      setStatus(form, "", "info");
      go(cur + 1);
    }

    /* A double-tap must not skip a step or run two transitions. The lock is
       a flag, not a disabled state: disabling the button mid-click would
       swallow the click that is already on its way and make the control look
       broken to anyone tapping quickly. */
    function withStepLock(fn) {
      if (form.getAttribute("data-jw-lock") === "1") return;
      form.setAttribute("data-jw-lock", "1");
      try { fn(); } finally {
        setTimeout(function () { form.removeAttribute("data-jw-lock"); }, 80);
      }
    }

    var nextBtn = $(".jw-next", form);
    if (nextBtn) {
      nextBtn.addEventListener("click", function () { withStepLock(advance); });
    }

    /* --- progress chips. The <li> is not the control: each chip holds a
       real <button>, so Enter/Space work natively. Forward jumps still go
       through the same validation as Continue. --- */
    $$(".jw-steps button[data-jw-goto-step]", form).forEach(function (btn) {
      btn.addEventListener("click", function () {
        tryStep(parseInt(btn.getAttribute("data-jw-goto-step"), 10));
      });
      btn.addEventListener("keydown", function (ev) {
        var key = ev.key;
        var idx = parseInt(btn.getAttribute("data-jw-goto-step"), 10);
        var buttons = $$(".jw-steps button[data-jw-goto-step]", form);
        var move = null;
        if (key === "ArrowRight" || key === "ArrowDown") move = Math.min(buttons.length - 1, idx + 1);
        else if (key === "ArrowLeft" || key === "ArrowUp") move = Math.max(0, idx - 1);
        else if (key === "Home") move = 0;
        else if (key === "End") move = buttons.length - 1;
        if (move === null) return;
        ev.preventDefault();
        buttons.forEach(function (b) { b.tabIndex = -1; });
        buttons[move].tabIndex = 0;
        buttons[move].focus();
      });
    });

    function tryStep(i) {
      var cur = parseInt(form.getAttribute("data-jw-step") || "0", 10);
      if (i > cur) {
        /* Forward jumps are not a shortcut: the step the tutor is on has to
           validate first, and only the very next step may be entered. */
        var st = validateStep(form, cur);
        if (!st.ok) {
          var here = steps(form)[cur];
          paintErrors(form, here, st.errors);
          renderSummary(form, here, st.errors);
          if (st.errors[0]) focusField(form, st.errors[0].el, st.errors[0].msg);
          return;
        }
        if (i > cur + 1) return;
      }
      if (i >= 0 && i < steps(form).length) clearSummary(steps(form)[i]);
      go(i);
    }

    /* ---------------------------------------------------------
       Submit
       --------------------------------------------------------- */
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (form.getAttribute("data-jw-sending") === "1") return;  /* in flight */
      if (form.getAttribute("data-jw-sent") === "1") return;     /* already accepted */

        /* The final check is the whole form, run through the SAME seven
           validators the Next button uses — no second, subtly different set
           of rules for submission. If anything is wrong we jump to the
           earliest bad step, show its summary and stop. */
        var states = stepState(form);
        var bad = states.filter(function (x) { return !x.ok; });
        if (bad.length) {
          /* Mark EVERY bad step, not just the one we jump to: when the tutor
             then fixes step 1 and submits again, the remaining steps are
             already flagged in the progress bar instead of appearing one at a
             time, one round trip each. */
          bad.forEach(function (b) {
            var s = steps(form)[b.index];
            if (s) paintErrors(form, s, b.errors);
          });
          var target = bad[0].index;
          var errs = bad[0].errors;
          go(target, { keepErrors: true });
          var stepEl = steps(form)[target];
          renderSummary(form, stepEl, errs);
          setStatus(form, bad.length === 1
            ? "One step still needs an answer — it is open now."
            : "Please complete the items highlighted here and on " +
              (bad.length - 1) + " more " + (bad.length - 1 === 1 ? "step" : "steps") + ".", "err");
          if (errs[0]) focusField(form, errs[0].el, errs[0].msg);
          return;
        }

        /* Consent is validated by step 7's own validator above, so this is a
           belt-and-braces check rather than the only line of defence. It is
           written to be reachable: it says which box, where, and why. */
        var consent = $("#jw-consent-data", form);
        if (!consent || !consent.checked) {
          setStatus(form, "Please tick the box agreeing that your details are true before submitting.", "err");
          if (consent) { showError(consent, CONSENT_MSG); focusField(form, consent, CONSENT_MSG); }
          return;
        }

        var pv = renderPreview(form);
        var btn = $(".jw-submit", form);
        form.setAttribute("data-jw-sending", "1");
        if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
        setStatus(form, "Sending your application…", "info");

        submitViaIntake(form, pv.payload, function (res) {
          if (res.ok) {
            /* The submitted flag deliberately STAYS set: a second submit
               after "received" would create a duplicate application row,
               and the tutor has no way to know which one we reviewed. */
            form.setAttribute("data-jw-sent", "1");
            /* Success screen REPLACES the form: leaving a half-visible
               form under a "received" message invites a second submission
               and makes the tutor doubt the first one landed. */
            var shell = $(".jw-shell", form);
            if (shell) shell.hidden = true;
            showDone(form, res.reference);
            return;
          }
          /* Recoverable failure: unlock, restore the EXACT button label, and
             keep every answer the tutor typed. Nothing is cleared here. */
          form.removeAttribute("data-jw-sending");
          if (btn) { btn.disabled = false; btn.textContent = "Submit Application"; }

          if (res.fallback || res.urlFallback) {
            mailtoFallback(form, pv.payload);
            setStatus(form,
              "Our form service did not answer, so we opened an email to us with everything you typed — press Send in your mail app. " +
              "Your answers are all there; nothing was lost. If no mail window opened, write to EkGuruLearning@gmail.com.",
              "err");
            return;
          }
          setStatus(form, res.error || "We could not send that. Please try again, or email EkGuruLearning@gmail.com.", "err");
        });
      });

    /* ---------------------------------------------------------
       Previous — always available off step 1, never validates, never
       clears an answer. The step's own validation state is recomputed by
       showStep(), so a value the tutor breaks by going back shows up as an
       incomplete step instead of a stale tick.
       --------------------------------------------------------- */
    var backBtn = $(".jw-back", form);
    if (backBtn) {
      backBtn.addEventListener("click", function () {
        var cur = parseInt(form.getAttribute("data-jw-step") || "0", 10);
        if (cur === 0) return;
        go(cur - 1);
      });
    }

    /* ---------------------------------------------------------
       Live field state. While the tutor types, a field that ALREADY shows an
       error is re-checked on every keystroke, so the message disappears the
       moment the value becomes acceptable — no waiting for another Continue.
       Fields that are still clean are only validated on blur, so a half-typed
       email is not called invalid after the first character.
       --------------------------------------------------------- */
    function recheck(el) {
      if (!el || !el.name) return;
      if (el.type === "checkbox" || el.type === "radio") return;
      var touched = el.getAttribute("aria-invalid") === "true";
      if (touched) {
        var msg = fieldError(el);
        showError(el, msg);
        if (!msg) {
          var cur = parseInt(form.getAttribute("data-jw-step") || "0", 10);
          var stepEl = steps(form)[cur];
          if (stepEl) {
            var st = validateStep(form, cur);
            if (st.ok) clearSummary(stepEl); else renderSummary(form, stepEl, st.errors);
          }
        }
      }
    }

    form.addEventListener("input", function (ev) {
      var el = ev.target;
      if (!el || el.nodeName === "SELECT") return;
      recheck(el);
      if (el.id === "jw-bio") updateWordCount(form);
      if (el.id === "jw-photo") updatePhotoPreview(form);
      /* Typing a time fixes or breaks that day's slot — rebuild the sentence
         under the days block right away instead of waiting for Continue. */
      if (el.type === "time" && el.closest(".jw-day")) refreshDayErrors(form);
    });

    form.addEventListener("change", function (ev) {
      var el = ev.target;
      if (!el) return;
      /* A day tick switches that row's time inputs on or off. This is THE fix
         for "checking a day does not let me enter times": the row is put into
         its live state the moment the box changes, before any validation. */
      if (el.closest(".jw-day")) {
        var liveRow = setDayState(el.closest(".jw-day"));
        /* Ticking a day is an answer to "when can you teach?" — take the
           "tick at least one day" error away at once. Unticking the last day
           puts it back on the next check, not mid-edit. */
        if (liveRow) clearDayGroupError(form);
        if (liveRow) {
          var firstTime = $('input[type="time"]', el.closest(".jw-day"));
          if (firstTime && typeof firstTime.focus === "function") {
            try { firstTime.focus({ preventScroll: true }); } catch (e0) { try { firstTime.focus(); } catch (e1) {} }
          }
        }
      }
      /* Conditional blocks appear the instant their trigger is answered —
         before any validation runs, so the newly shown field is visible. */
      if (el.id === "jw-years" || el.id === "jw-edu-qual" || el.name === "subjects" ||
          el.name === "levels" || el.closest("[data-when]")) {
        syncConditionals(form);
      }
      /* Chip groups: clear their group error as soon as the minimum is met. */
      var grp = el.closest("[data-need-min]");
      if (grp) {
        var name = grp.getAttribute("data-need-min");
        var min = parseInt(grp.getAttribute("data-min") || "1", 10);
        if (checkedValues(form, name).length >= min) {
          var box = grp.parentNode ? $(".jw-err", grp.parentNode) : null;
          if (box) { box.textContent = ""; box.classList.remove("is-on"); }
          if (grp.classList) grp.classList.remove("is-invalid");
        }
      }
      recheck(el);
      var cur = parseInt(form.getAttribute("data-jw-step") || "0", 10);
      var stepEl = steps(form)[cur];
      if (stepEl && $("[data-jw-summary]:not([hidden])", stepEl)) {
        var st = validateStep(form, cur);
        if (st.ok) { clearSummary(stepEl); setStatus(form, "", "info"); }
        else renderSummary(form, stepEl, st.errors);
      }
      /* Progress and submit state follow every change, so the percentage
         and the tick marks never lag behind what is actually filled in. */
      showStep(form, cur, { silent: true });
      if (cur === lastIndex) {
        renderPreview(form);
        refreshSubmit();
      }
    });

    form.addEventListener("blur", function (ev) {
      var el = ev.target;
      if (el && el.name && el.getAttribute("aria-invalid") !== "true") {
        /* Only report on blur when the field is required and empty, or the
           tutor typed something that the rule rejects. */
        var msg = fieldError(el);
        if (msg && (el.required ? !!val(el) : true)) showError(el, msg);
      }
    }, true);

    /* Enter inside a text field means "Continue", not "submit an application
       I have not reviewed". Without this the browser's implicit submission
       fires the form's submit handler from step 1. */
    form.addEventListener("keydown", function (ev) {
      if (ev.key !== "Enter" || ev.shiftKey) return;
      var el = ev.target;
      if (!el || el.tagName === "TEXTAREA" || el.tagName === "BUTTON") return;
      var cur = parseInt(form.getAttribute("data-jw-step") || "0", 10);
      if (cur >= lastIndex) return;      /* on the review step, let Submit work */
      ev.preventDefault();
      withStepLock(advance);
    });

    /* Review-step Edit buttons: back to the right question, answers intact. */
    $$("[data-jw-goto]", form).forEach(function (btn) {
      btn.addEventListener("click", function () {
        tryStep(parseInt(btn.getAttribute("data-jw-goto"), 10));
      });
    });

    /* Browser-restored values (or a soft reload) can leave a conditional
       block out of sync with its trigger, so settle it once before the first
       paint rather than waiting for the tutor to touch the trigger again. */
    syncConditionals(form);
    /* Same for the day rows: a browser that restored a tick must come back
       with that row live and its time inputs usable. */
    syncDayRows(form);
    go(0, { silent: true });
    toggleSubmit(false);
    refreshSubmit();
    showStep(form, 0, { silent: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  /* Exposed for the tests: they assert the payload contract against
     Intake.gs's allow-list without needing a browser. */
  window.EkGuruJoinWizard = {
    buildPayload: buildPayload,
    fieldError: fieldError,
    readAvailability: readAvailability,
    availabilityProblem: availabilityProblem,
    limits: LIMITS
  };
})();
