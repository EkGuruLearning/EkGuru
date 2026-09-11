/* =========================================================
   EkGuru — EMAIL TEMPLATES + ROUTING MATRIX  (single source of truth · v100)
   ---------------------------------------------------------
   The one place that knows WHAT the site emails. Five message
   types, each with:
     · a declared variable registry (allowedVars) — rendering
       fails on a missing/undeclared/null variable or a raw
       {placeholder} left in the output, so a broken template
       cannot ship silently;
     · a subject(), an HTML body and a plain-text body;
     · a role-language contract (see roleqa below) so a student
       mail can never read like a tutor mail.

   Design rules:
     · From is ALWAYS the verified EkGuru sender; Reply-To is set
       per role at send time — never in the template.
     · Every user-controlled value is HTML-escaped. No raw user
       HTML, no secrets, no internal notes in visitor-facing mail.
     · BOOKING_EKGURU_NOTIFICATION is the only template that may
       carry operational detail (provider, delivery state) and it
       is internal-only.

   This file is consumed by:
     · js/mailer.js          (renders html/text at send time)
     · js/admin-mail-ops.js  (template preview + health)
     · tools/test-email-system.js (role-language + registry tests)
   ========================================================= */
(function () {
  "use strict";

  var BRAND = "EkGuru";
  var ACCENT = "#4f32d9";

  /* ----------------------------------------------------------
     SHARED DESIGN SYSTEM — one card layout, one footer.
     ---------------------------------------------------------- */
  function shell(inner) {
    return (
      '<div style="background:#f5f6f8;padding:24px 12px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#0f172a;">' +
        '<table role="presentation" width="100%" style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:12px;border:1px solid #e5e7eb;border-collapse:separate;border-spacing:0;">' +
          '<tr><td style="padding:22px 24px 6px;">' +
            '<div style="font-weight:800;letter-spacing:.06em;color:' + ACCENT + ';font-size:13px;">' + BRAND + '</div>' +
          '</td></tr>' +
          '<tr><td style="padding:6px 24px 18px;">' + inner + '</td></tr>' +
          '<tr><td style="padding:14px 24px;border-top:1px solid #eef0f3;color:#94a3b8;font-size:12px;line-height:1.6;">' +
            BRAND + ' · <a href="https://ekguru.shop/" style="color:' + ACCENT + ';text-decoration:none;">ekguru.shop</a>' +
          '</td></tr>' +
        '</table>' +
      '</div>'
    );
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function badge(text, tone) {
    var bg = tone === "ok" ? "#eef7f0" : tone === "warn" ? "#fff8e6" : "#eef0ff";
    var fg = tone === "ok" ? "#12532a" : tone === "warn" ? "#8a5a00" : "#3b2fa8";
    return '<span style="display:inline-block;background:' + bg + ';color:' + fg +
      ';font-size:11px;font-weight:700;letter-spacing:.05em;padding:3px 10px;border-radius:999px;">' +
      esc(text) + '</span>';
  }

  function row(label, value) {
    if (value == null || value === "") return "";
    return '<tr><td style="padding:7px 0;color:#64748b;font-size:12px;white-space:nowrap;vertical-align:top;width:150px;">' +
      esc(label) + '</td><td style="padding:7px 0 7px 12px;color:#0f172a;font-size:14px;white-space:pre-wrap;">' +
      esc(value) + '</td></tr>';
  }

  function table(rows) {
    var inner = [];
    rows.forEach(function (r) { var h = row(r[0], r[1]); if (h) inner.push(h); });
    return '<table role="presentation" width="100%" style="border-collapse:collapse;">' +
      inner.join("") + '</table>';
  }

  function h2(t) { return '<h2 style="font-size:17px;margin:0 0 12px;font-weight:700;">' + esc(t) + '</h2>'; }
  function p(t) { return '<p style="font-size:14px;line-height:1.7;margin:0 0 12px;color:#334155;">' + t + '</p>'; }

  /* ----------------------------------------------------------
     THE ROUTING MATRIX — machine-readable, one row per message.
     ---------------------------------------------------------- */
  var ROUTES = [
    {
      type: "CONTACT_VISITOR_CONFIRMATION",
      role: "contact_visitor",
      from: "verified EkGuru sender",
      to: "exact submitted visitor email",
      replyTo: "official support address",
      template: "contactVisitor"
    },
    {
      type: "CONTACT_EKGURU_NOTIFICATION",
      role: "contact_internal",
      from: "verified EkGuru sender",
      to: "EkGuru internal inbox",
      replyTo: "exact visitor email",
      template: "contactInternal"
    },
    {
      type: "BOOKING_STUDENT_CONFIRMATION",
      role: "booking_student",
      from: "verified EkGuru sender",
      to: "exact booking student email",
      replyTo: "official support address",
      template: "bookingStudent"
    },
    {
      type: "BOOKING_TUTOR_NOTIFICATION",
      role: "booking_tutor",
      from: "verified EkGuru sender",
      to: "canonical tutor notification email",
      replyTo: "exact booking student email (tutor confirms the time)",
      template: "bookingTutor"
    },
    {
      type: "BOOKING_EKGURU_NOTIFICATION",
      role: "booking_internal",
      from: "verified EkGuru sender",
      to: "EkGuru internal inbox",
      replyTo: "exact booking student email (staff can reply to the learner)",
      template: "bookingInternal"
    }
  ];

  var WHITELIST = ROUTES.map(function (r) { return r.type; });

  /* ----------------------------------------------------------
     TEMPLATES
     ---------------------------------------------------------- */
  var TEMPLATES = {

    /* ============ CONTACT — VISITOR CONFIRMATION ============ */
    contactVisitor: {
      role: "visitor",
      subject: function (v) { return "We received your message — " + v.contactId + " | EkGuru"; },
      allowedVars: ["visitorName", "contactId", "nextStep", "supportEmail", "siteUrl"],
      html: function (v) {
        return shell(
          h2("Message received") +
          p("Hi " + esc(v.visitorName) + ",") +
          p("Thank you for contacting EkGuru. We received your message and will review it.") +
          table([
            ["Reference", v.contactId],
            ["Next step", v.nextStep]
          ]) +
          p('<span style="font-size:13px;color:#64748b;">If you need to follow up, reply to this email or write to ' +
            esc(v.supportEmail) + " quoting " + esc(v.contactId) + ".</span>")
        );
      },
      text: function (v) {
        return [
          "EKGURU", "Message received", "",
          "Hi " + v.visitorName + ",",
          "", "Thank you for contacting EkGuru. We received your message and will review it.", "",
          "Reference: " + v.contactId,
          "Next step: " + v.nextStep, "",
          v.supportEmail + " · " + v.siteUrl
        ].join("\n");
      }
    },

    /* ============ CONTACT — EKGURU INTERNAL ============ */
    contactInternal: {
      role: "internal",
      subject: function (v) {
        return (v.urgent ? "[!! " + String(v.category).toUpperCase() + "] " : "") +
          "New contact request — " + v.category + " — " + v.contactId;
      },
      allowedVars: ["visitorName", "visitorEmail", "category", "subject", "message",
                    "timestamp", "sourcePage", "contactId", "supportEmail", "siteUrl",
                    "urgent", "actionNeeded"],
      html: function (v) {
        return shell(
          badge("NEW CONTACT REQUEST", "warn") +
          '<div style="height:12px"></div>' +
          table([
            ["Reference", v.contactId],
            ["Visitor", v.visitorName],
            ["Visitor email", v.visitorEmail],
            ["Category", v.category],
            ["Subject", v.subject],
            ["Received", v.timestamp],
            ["Source page", v.sourcePage],
            ["Message", v.message],
            /* Only present when it matters (a report or privacy
               request) — omitted otherwise, so it is not noise on
               the other topics. */
            ["Action needed", v.actionNeeded]
          ]) +
          p('<span style="font-size:13px;color:#64748b;">Reply directly to this email — the visitor\'s address is on the Reply-To line.</span>')
        );
      },
      text: function (v) {
        return [
          "NEW CONTACT REQUEST — " + v.contactId, "",
          "Reference: " + v.contactId,
          "Visitor: " + v.visitorName + " <" + v.visitorEmail + ">",
          "Category: " + v.category,
          "Subject: " + v.subject,
          "Received: " + v.timestamp,
          "Source: " + v.sourcePage, "",
          "Message:", v.message, "",
          (v.actionNeeded ? "ACTION NEEDED: " + v.actionNeeded + "\n" : ""),
          "Reply directly to this email to answer the visitor."
        ].join("\n");
      }
    },

    /* ============ BOOKING — STUDENT CONFIRMATION ============ */
    bookingStudent: {
      role: "student",
      subject: function (v) { return "Booking request received — " + v.tutorName + " | EkGuru"; },
      allowedVars: ["studentName", "bookingId", "tutorName", "date", "time", "timezone",
                    "lessonType", "studentRequirement", "bookingStatus", "nextStep",
                    "supportEmail", "siteUrl"],
      html: function (v) {
        return shell(
          h2("Booking request received") +
          p("Hi " + esc(v.studentName) + ", we've received your request to learn with " + esc(v.tutorName) + ".") +
          badge(v.bookingStatus, "ok") + '<div style="height:12px"></div>' +
          table([
            ["Booking ID", v.bookingId],
            ["Tutor", v.tutorName],
            ["Date", v.date],
            ["Time", v.time],
            ["Timezone", v.timezone],
            ["Lesson", v.lessonType],
            ["Your requirement", v.studentRequirement]
          ]) +
          p("<b>What happens next</b><br>" + esc(v.nextStep)) +
          p('<span style="font-size:13px;color:#64748b;">Need help? Reply to this email or write to ' +
            esc(v.supportEmail) + " quoting " + esc(v.bookingId) + ".</span>")
        );
      },
      text: function (v) {
        return [
          "EKGURU", "Booking request received", "",
          "Hi " + v.studentName + ", we've received your request to learn with " + v.tutorName + ".", "",
          "Booking ID: " + v.bookingId,
          "Tutor: " + v.tutorName,
          "Date: " + v.date,
          "Time: " + v.time,
          "Timezone: " + v.timezone,
          "Lesson: " + v.lessonType,
          "Your requirement: " + v.studentRequirement,
          "Status: " + v.bookingStatus, "",
          "What happens next: " + v.nextStep, "",
          "Need help? " + v.supportEmail + " · " + v.siteUrl
        ].join("\n");
      }
    },

    /* ============ BOOKING — TUTOR NOTIFICATION ============ */
    bookingTutor: {
      role: "tutor",
      subject: function (v) { return "New lesson request — " + v.studentName + " — " + v.date + " | EkGuru"; },
      allowedVars: ["tutorName", "bookingId", "studentName", "date", "time", "timezone",
                    "lessonType", "studentRequirement", "bookingStatus", "tutorNextAction",
                    "supportEmail", "siteUrl"],
      html: function (v) {
        return shell(
          h2("New lesson request") +
          p("Hi " + esc(v.tutorName) + ", a learner has requested a lesson with you.") +
          badge("NEW REQUEST", "warn") + '<div style="height:12px"></div>' +
          table([
            ["Booking ID", v.bookingId],
            ["Learner", v.studentName],
            ["Requested date", v.date],
            ["Requested time", v.time],
            ["Timezone", v.timezone],
            ["Lesson type", v.lessonType],
            ["Learner requirement", v.studentRequirement],
            ["Status", v.bookingStatus]
          ]) +
          p("<b>Your next action</b><br>" + esc(v.tutorNextAction))
        );
      },
      text: function (v) {
        return [
          "EKGURU", "New lesson request", "",
          "Hi " + v.tutorName + ", a learner has requested a lesson with you.", "",
          "Booking ID: " + v.bookingId,
          "Learner: " + v.studentName,
          "Requested date: " + v.date,
          "Requested time: " + v.time,
          "Timezone: " + v.timezone,
          "Lesson type: " + v.lessonType,
          "Learner requirement: " + v.studentRequirement,
          "Status: " + v.bookingStatus, "",
          "Your next action: " + v.tutorNextAction, "",
          v.supportEmail + " · " + v.siteUrl
        ].join("\n");
      }
    },

    /* ============ BOOKING — EKGURU INTERNAL ============ */
    bookingInternal: {
      role: "internal",
      subject: function (v) { return "New booking request — " + v.studentName + " → " + v.tutorName + " — " + v.bookingId; },
      allowedVars: ["bookingId", "status", "createdAt", "studentName", "studentEmail",
                    "tutorName", "tutorId", "tutorEmailState", "date", "time", "timezone",
                    "lessonType", "studentRequirement", "sourcePage",
                    "studentDeliveryState", "tutorDeliveryState", "internalDeliveryState",
                    "provider", "lastError", "nextAction", "supportEmail", "siteUrl"],
      html: function (v) {
        return shell(
          h2("New booking request") +
          badge(v.status || "REQUEST RECEIVED", "ok") + '<div style="height:12px"></div>' +
          table([
            ["Booking ID", v.bookingId],
            ["Created", v.createdAt],
            ["Student", v.studentName + " <" + v.studentEmail + ">"],
            ["Tutor", v.tutorName + " (" + v.tutorId + ")"],
            ["Tutor email state", v.tutorEmailState],
            ["Date", v.date],
            ["Time", v.time],
            ["Timezone", v.timezone],
            ["Lesson", v.lessonType],
            ["Requirement", v.studentRequirement],
            ["Source", v.sourcePage],
            ["Student delivery", v.studentDeliveryState],
            ["Tutor delivery", v.tutorDeliveryState],
            ["Internal delivery", v.internalDeliveryState],
            ["Provider", v.provider],
            ["Last error", v.lastError],
            ["Next action", v.nextAction]
          ])
        );
      },
      text: function (v) {
        return [
          "NEW BOOKING REQUEST — " + v.bookingId, "",
          "Booking ID: " + v.bookingId,
          "Status: " + v.status,
          "Created: " + v.createdAt,
          "Student: " + v.studentName + " <" + v.studentEmail + ">",
          "Tutor: " + v.tutorName + " (" + v.tutorId + ")",
          "Tutor email state: " + v.tutorEmailState,
          "Date: " + v.date,
          "Time: " + v.time,
          "Timezone: " + v.timezone,
          "Lesson: " + v.lessonType,
          "Requirement: " + v.studentRequirement,
          "Source: " + v.sourcePage,
          "Student delivery: " + v.studentDeliveryState,
          "Tutor delivery: " + v.tutorDeliveryState,
          "Internal delivery: " + v.internalDeliveryState,
          "Provider: " + v.provider,
          "Last error: " + v.lastError,
          "Next action: " + v.nextAction
        ].join("\n");
      }
    }
  };

  /* ----------------------------------------------------------
     ROLE-LANGUAGE CONTRACT  (§30)
     Automated semantic tests assert these.
     ---------------------------------------------------------- */
  var ROLE_QA = {
    contactVisitor: {
      mustSay: ["message received", "reference"],
      mustNotSay: ["new lesson request", "you booked", "internal", "provider"]
    },
    contactInternal: {
      mustSay: ["visitor", "message"],
      mustNotSay: ["you booked", "your booking id"]
    },
    bookingStudent: {
      mustSay: ["your request", "what happens next"],
      mustNotSay: ["new lesson request for you", "tutor's private", "your next action as the tutor"]
    },
    bookingTutor: {
      mustSay: ["new lesson request", "learner"],
      mustNotSay: ["you booked", "your booking request was received"]
    },
    bookingInternal: {
      mustSay: ["delivery"],
      mustNotSay: []
    }
  };

  /* ----------------------------------------------------------
     RENDER + VALIDATION  (§29)
     ---------------------------------------------------------- */
  /* A message can be addressed by its contractual type
     ("BOOKING_TUTOR_NOTIFICATION" — the value the Apps Script relay
     whitelists) or by its short template key ("bookingTutor"). Both
     resolve to the same template. */
  function resolveTemplate(type) {
    if (TEMPLATES[type]) return { key: type, t: TEMPLATES[type] };
    for (var i = 0; i < ROUTES.length; i++) {
      if (ROUTES[i].type === type) {
        var tk = ROUTES[i].template;
        return TEMPLATES[tk] ? { key: tk, t: TEMPLATES[tk] } : null;
      }
    }
    return null;
  }

  function render(type, vars) {
    var found = resolveTemplate(type);
    if (!found) return { ok: false, errors: ["unknown message type: " + type] };
    var t = found.t;
    vars = vars || {};
    var errors = [];

    /* undeclared variables */
    Object.keys(vars).forEach(function (k) {
      if (t.allowedVars.indexOf(k) === -1) errors.push("undeclared variable: " + k);
    });

    /* required variables — a declared var must not be null/undefined.
       An empty string is allowed: it renders as an omitted row, which
       is the honest state for fields like lastError. */
    t.allowedVars.forEach(function (k) {
      if (vars[k] == null) errors.push("missing variable: " + k);
    });

    if (errors.length) return { ok: false, errors: errors };

    var out = {};
    try {
      out.subject = t.subject(vars);
      out.html = t.html(vars);
      out.text = t.text(vars);
    } catch (e) {
      return { ok: false, errors: ["render threw: " + e.message] };
    }

    /* Header-injection defence: a subject is a single line. Any
       control character a user could smuggle into a name/date is
       collapsed to a space and the line is capped, so a newline can
       never inject a Bcc:/From: header. */
    out.subject = String(out.subject || "").replace(/[\r\n\t]+/g, " ").slice(0, 150);

    /* no raw {placeholder} may survive into output */
    ["subject", "html", "text"].forEach(function (k) {
      if (/\{[A-Za-z_]+\}/.test(out[k])) {
        errors.push("raw placeholder left in " + k + ": " + (out[k].match(/\{[A-Za-z_]+\}/) || [])[0]);
      }
    });

    /* HTML must be escaped — a literal <script> in a user value is a fail */
    ["html"].forEach(function (k) {
      if (/<script/i.test(out[k])) errors.push("unescaped script in " + k);
    });

    return { ok: errors.length === 0, errors: errors, subject: out.subject, html: out.html, text: out.text, template: found.key };
  }

  /* Fixtures for preview — never real customer data. */
  var FIXTURES = {
    contactVisitor: {
      visitorName: "Priya", contactId: "C-TEST01", nextStep: "We will reply within one working day.",
      supportEmail: "EkGuruLearning@gmail.com", siteUrl: "https://ekguru.shop/"
    },
    contactInternal: {
      visitorName: "Priya", visitorEmail: "priya@example.com", category: "General",
      subject: "A question about lessons", message: "Do you teach complete beginners?",
      timestamp: "11 Sep 2026, 3:00 PM", sourcePage: "/contact/", contactId: "C-TEST01",
      supportEmail: "EkGuruLearning@gmail.com", siteUrl: "https://ekguru.shop/",
      urgent: false, actionNeeded: ""
    },
    bookingStudent: {
      studentName: "Priya", bookingId: "EK-TEST01", tutorName: "Tara", date: "20 September 2026",
      time: "7:00 PM", timezone: "Asia/Kolkata", lessonType: "Trial lesson",
      studentRequirement: "Conversation practice", bookingStatus: "Request received",
      nextStep: "Tara has your request and will reply to confirm the time. This is a request, not a confirmed booking.",
      supportEmail: "EkGuruLearning@gmail.com", siteUrl: "https://ekguru.shop/"
    },
    bookingTutor: {
      tutorName: "Tara", bookingId: "EK-TEST01", studentName: "Priya", date: "20 September 2026",
      time: "7:00 PM", timezone: "Asia/Kolkata", lessonType: "Trial lesson",
      studentRequirement: "Conversation practice", bookingStatus: "Request received",
      tutorNextAction: "Reply to this email to confirm the time with the learner.",
      supportEmail: "EkGuruLearning@gmail.com", siteUrl: "https://ekguru.shop/"
    },
    bookingInternal: {
      bookingId: "EK-TEST01", status: "sent", createdAt: "2026-09-11T10:00:00Z",
      studentName: "Priya", studentEmail: "priya@example.com", tutorName: "Tara", tutorId: "tara",
      tutorEmailState: "ACTIVE+VALID", date: "20 September 2026", time: "7:00 PM",
      timezone: "Asia/Kolkata", lessonType: "Trial lesson", studentRequirement: "Conversation practice",
      sourcePage: "/find-tutors.html", studentDeliveryState: "ACCEPTED",
      tutorDeliveryState: "ACCEPTED", internalDeliveryState: "ACCEPTED",
      provider: "Google Apps Script", lastError: "", nextAction: "Confirm the time with the tutor.",
      supportEmail: "EkGuruLearning@gmail.com", siteUrl: "https://ekguru.shop/"
    }
  };

  window.EKGURU_EMAIL = {
    ROUTES: ROUTES,
    WHITELIST: WHITELIST,
    TEMPLATES: TEMPLATES,
    ROLE_QA: ROLE_QA,
    FIXTURES: FIXTURES,
    render: render,
    esc: esc
  };
})();
