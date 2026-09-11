/* =========================================================
   EkGuru — EMAIL TEMPLATES + ROUTING MATRIX  (single source of truth · v101)
   ---------------------------------------------------------
   EMAIL RESET: the copy is now SIMPLE, role-specific, and exactly
   what the owner asked for. Seven message types, each with its own
   wording — a student mail never reads like a tutor mail, and the
   internal record never leaks to a public recipient.

   The seven types:

     BOOKING_STUDENT_CONFIRMATION   → the student
     BOOKING_TUTOR_NOTIFICATION     → the tutor
     BOOKING_EKGURU_NOTIFICATION    → EkGuru internal record
     CONTACT_VISITOR_CONFIRMATION   → the visitor who wrote in
     CONTACT_EKGURU_NOTIFICATION    → EkGuru internal record
     ADMIN_CONTACT_OUTBOUND         → the recipient the admin wrote to
     ADMIN_CONTACT_INTERNAL_COPY    → EkGuru internal copy

   Each template declares its variable registry (allowedVars).
   render() FAILS LOUDLY on an unknown type, a missing/undeclared/
   null variable, a raw {placeholder} left in output, or an
   unescaped <script>. A subject is one line (CR/LF collapsed, 150
   chars) so a header can never be injected.

   Design rules (§17/§18):
     · From is ALWAYS the verified EkGuru sender (enforced by the
       relay); Reply-To is per role and set at send time.
     · Every user value is HTML-escaped. No raw user HTML.
     · Only the internal templates carry operational detail
       (delivery state, tutor email state, source page).

   Consumed by:
     · js/mailer.js          (renders html/text at send time)
     · admin.html Mail Ops   (routing matrix + template preview)
     · tools/test-email-system.js / tools/test-email-security.js
   ========================================================= */
(function () {
  "use strict";

  var BRAND = "EkGuru";
  var ACCENT = "#4f32d9";
  var SITE_URL = "https://ekguru.shop/";

  /* ----------------------------------------------------------
     SHARED DESIGN SYSTEM — one clean card, one footer (§18).
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
            BRAND + ' · <a href="' + SITE_URL + '" style="color:' + ACCENT + ';text-decoration:none;">ekguru.shop</a>' +
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
  function list(items) {
    return '<ul style="font-size:14px;line-height:1.7;margin:0 0 12px;padding-left:18px;color:#334155;">' +
      items.map(function (i) { return "<li>" + i + "</li>"; }).join("") + '</ul>';
  }

  /* ----------------------------------------------------------
     THE ROUTING MATRIX — machine-readable, one row per message.
     ---------------------------------------------------------- */
  var ROUTES = [
    {
      type: "BOOKING_STUDENT_CONFIRMATION",
      role: "booking_student",
      from: "verified EkGuru sender",
      to: "exact booking student email",
      replyTo: "official EkGuru support",
      template: "bookingStudent"
    },
    {
      type: "BOOKING_TUTOR_NOTIFICATION",
      role: "booking_tutor",
      from: "verified EkGuru sender",
      to: "canonical tutor notification_email",
      replyTo: "supported direct-response route (the student's email)",
      template: "bookingTutor"
    },
    {
      type: "BOOKING_EKGURU_NOTIFICATION",
      role: "booking_internal",
      from: "verified EkGuru sender",
      to: "EkGuru internal inbox",
      replyTo: "exact booking student email",
      template: "bookingInternal"
    },
    {
      type: "CONTACT_VISITOR_CONFIRMATION",
      role: "contact_visitor",
      from: "verified EkGuru sender",
      to: "exact submitted visitor email",
      replyTo: "official EkGuru support",
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
      type: "ADMIN_CONTACT_OUTBOUND",
      role: "admin_outbound",
      from: "verified EkGuru sender",
      to: "exact admin-selected recipient",
      replyTo: "official EkGuru support",
      template: "adminOutbound"
    },
    {
      type: "ADMIN_CONTACT_INTERNAL_COPY",
      role: "admin_internal_copy",
      from: "verified EkGuru sender",
      to: "EkGuru internal inbox",
      replyTo: "official EkGuru support",
      template: "adminInternalCopy"
    }
  ];

  var WHITELIST = ROUTES.map(function (r) { return r.type; });

  /* ----------------------------------------------------------
     TEMPLATES — SIMPLE, role-specific copy (§8–§13)
     ---------------------------------------------------------- */
  var TEMPLATES = {

    /* ============ BOOKING — STUDENT ============ */
    bookingStudent: {
      role: "student",
      subject: function () { return "Congratulations — your booking request was received | EkGuru"; },
      allowedVars: ["studentName", "bookingId", "tutorName", "studentRequirement",
                    "date", "time", "timezone", "bookingStatus", "nextStep",
                    "supportEmail", "siteUrl"],
      html: function (v) {
        return shell(
          h2("Booking request received") +
          p("Hi " + esc(v.studentName) + ",") +
          p("Congratulations! Your booking request has been received by EkGuru.") +
          table([
            ["Reference Number", v.bookingId],
            ["You requested a lesson with", v.tutorName],
            ["Your message", v.studentRequirement],
            ["Requested date", v.date],
            ["Requested time", v.time],
            ["Timezone", v.timezone],
            ["Current status", v.bookingStatus],
            ["What happens next", v.nextStep]
          ]) +
          p('<span style="font-size:13px;color:#64748b;">Please keep your reference number for future communication.</span>')
        );
      },
      text: function (v) {
        return [
          "Hi " + v.studentName + ",", "",
          "Congratulations! Your booking request has been received by EkGuru.", "",
          "Reference Number:",
          v.bookingId, "",
          "You requested a lesson with:",
          v.tutorName, "",
          "Your message:",
          v.studentRequirement, "",
          "Requested date:",
          v.date, "",
          "Requested time:",
          v.time, "",
          "Timezone:",
          v.timezone, "",
          "Current status:",
          v.bookingStatus, "",
          "What happens next:",
          v.nextStep, "",
          "Please keep your reference number for future communication.", "",
          "EkGuru",
          v.siteUrl || SITE_URL
        ].join("\n");
      }
    },

    /* ============ BOOKING — TUTOR ============ */
    bookingTutor: {
      role: "tutor",
      subject: function () { return "Congratulations — you have a new booking request | EkGuru"; },
      allowedVars: ["tutorName", "bookingId", "studentName", "studentEmail",
                    "date", "time", "timezone", "lessonType", "studentRequirement",
                    "tutorNextAction", "tutorAltTimeInstruction",
                    "supportEmail", "siteUrl"],
      html: function (v) {
        return shell(
          h2("New booking request") +
          p("Hi " + esc(v.tutorName) + ",") +
          p("Congratulations! You have received a new booking request.") +
          table([
            ["Reference Number", v.bookingId],
            ["Student", v.studentName],
            ["Student Email", v.studentEmail],
            ["Requested date", v.date],
            ["Requested time", v.time],
            ["Timezone", v.timezone],
            ["Lesson", v.lessonType],
            ["Student's message", v.studentRequirement],
            ["What to do next", v.tutorNextAction]
          ]) +
          p("You can respond with:") +
          list([
            "Available",
            "Not available",
            "Available at another time" + (v.tutorAltTimeInstruction ? ": " + esc(v.tutorAltTimeInstruction) : "")
          ]) +
          p("EkGuru will continue the booking process based on your response.")
        );
      },
      text: function (v) {
        return [
          "Hi " + v.tutorName + ",", "",
          "Congratulations! You have received a new booking request.", "",
          "Reference Number:",
          v.bookingId, "",
          "Student:",
          v.studentName, "",
          "Student Email:",
          v.studentEmail, "",
          "Requested date:",
          v.date, "",
          "Requested time:",
          v.time, "",
          "Timezone:",
          v.timezone, "",
          "Lesson:",
          v.lessonType, "",
          "Student's message:",
          v.studentRequirement, "",
          "What to do next:",
          v.tutorNextAction, "",
          "You can respond with:",
          "- Available",
          "- Not available",
          "- Available at another time" + (v.tutorAltTimeInstruction ? ": " + v.tutorAltTimeInstruction : ""), "",
          "EkGuru will continue the booking process based on your response.", "",
          "EkGuru",
          v.siteUrl || SITE_URL
        ].join("\n");
      }
    },

    /* ============ BOOKING — EKGURU INTERNAL ============ */
    bookingInternal: {
      role: "internal",
      subject: function (v) { return "New booking request — " + v.studentName + " → " + v.tutorName + " | " + v.bookingId; },
      allowedVars: ["bookingId", "studentName", "studentEmail", "tutorName", "tutorId",
                    "tutorEmail", "date", "time", "timezone", "lessonType",
                    "studentRequirement", "bookingStatus",
                    "studentDeliveryStatus", "tutorDeliveryStatus", "internalDeliveryStatus",
                    "adminNextAction", "sourcePage"],
      html: function (v) {
        return shell(
          badge("EKGURU INTERNAL BOOKING", "warn") + '<div style="height:12px"></div>' +
          table([
            ["Reference Number", v.bookingId],
            ["Student", v.studentName],
            ["Student Email", v.studentEmail],
            ["Tutor", v.tutorName],
            ["Tutor ID", v.tutorId],
            ["Tutor Email", v.tutorEmail],
            ["Date", v.date],
            ["Time", v.time],
            ["Timezone", v.timezone],
            ["Lesson", v.lessonType],
            ["Student Message", v.studentRequirement],
            ["Booking Status", v.bookingStatus],
            ["Email Delivery — Student", v.studentDeliveryStatus],
            ["Email Delivery — Tutor", v.tutorDeliveryStatus],
            ["Email Delivery — Internal", v.internalDeliveryStatus],
            ["Next Admin Action", v.adminNextAction],
            ["Source", v.sourcePage]
          ])
        );
      },
      text: function (v) {
        return [
          "EKGURU INTERNAL BOOKING", "",
          "Reference Number:", v.bookingId, "",
          "Student:", v.studentName,
          "Student Email:", v.studentEmail, "",
          "Tutor:", v.tutorName,
          "Tutor ID:", v.tutorId,
          "Tutor Email:", v.tutorEmail, "",
          "Date:", v.date,
          "Time:", v.time,
          "Timezone:", v.timezone, "",
          "Lesson:", v.lessonType, "",
          "Student Message:", v.studentRequirement, "",
          "Booking Status:", v.bookingStatus, "",
          "Email Delivery:",
          "Student: " + v.studentDeliveryStatus,
          "Tutor: " + v.tutorDeliveryStatus,
          "Internal: " + v.internalDeliveryStatus, "",
          "Next Admin Action:", v.adminNextAction, "",
          "Source:", v.sourcePage
        ].join("\n");
      }
    },

    /* ============ CONTACT — VISITOR ============ */
    contactVisitor: {
      role: "visitor",
      subject: function () { return "We received your message — EkGuru"; },
      allowedVars: ["visitorName", "contactId", "message", "nextStep",
                    "supportEmail", "siteUrl"],
      html: function (v) {
        return shell(
          h2("Message received") +
          p("Hi " + esc(v.visitorName) + ",") +
          p("Thank you for contacting EkGuru.") +
          p("We have received your message.") +
          table([
            ["Reference Number", v.contactId],
            ["Your message", v.message],
            ["What happens next", v.nextStep]
          ])
        );
      },
      text: function (v) {
        return [
          "Hi " + v.visitorName + ",", "",
          "Thank you for contacting EkGuru.", "",
          "We have received your message.", "",
          "Reference Number:",
          v.contactId, "",
          "Your message:",
          v.message, "",
          "What happens next:",
          v.nextStep, "",
          "EkGuru",
          v.siteUrl || SITE_URL
        ].join("\n");
      }
    },

    /* ============ CONTACT — EKGURU INTERNAL ============ */
    contactInternal: {
      role: "internal",
      subject: function (v) { return "New contact message — " + v.contactId; },
      allowedVars: ["contactId", "visitorName", "visitorEmail", "subject",
                    "message", "timestamp", "sourcePage", "adminNextAction"],
      html: function (v) {
        return shell(
          badge("EKGURU INTERNAL CONTACT", "warn") + '<div style="height:12px"></div>' +
          table([
            ["Reference Number", v.contactId],
            ["Name", v.visitorName],
            ["Email", v.visitorEmail],
            ["Subject", v.subject],
            ["Message", v.message],
            ["Submitted", v.timestamp],
            ["Source", v.sourcePage],
            ["Reply-To", v.visitorEmail],
            ["Internal action", v.adminNextAction]
          ])
        );
      },
      text: function (v) {
        return [
          "EKGURU INTERNAL CONTACT", "",
          "Reference Number:", v.contactId, "",
          "Name:", v.visitorName,
          "Email:", v.visitorEmail,
          "Subject:", v.subject, "",
          "Message:", v.message, "",
          "Submitted:", v.timestamp,
          "Source:", v.sourcePage,
          "Reply-To:", v.visitorEmail, "",
          "Internal action:", v.adminNextAction
        ].join("\n");
      }
    },

    /* ============ ADMIN → RECIPIENT ============ */
    adminOutbound: {
      role: "outbound",
      subject: function (v) { return v.adminSubject || ("A message from " + BRAND); },
      allowedVars: ["recipientName", "adminSubject", "adminMessage",
                    "conversationId", "supportContact"],
      html: function (v) {
        return shell(
          p("Hi " + esc(v.recipientName) + ",") +
          p(esc(v.adminMessage).replace(/\n/g, "<br>")) +
          table([
            ["Reference", v.conversationId]
          ]) +
          p("Regards,<br>" + BRAND + (v.supportContact ? "<br>" + esc(v.supportContact) : ""))
        );
      },
      text: function (v) {
        return [
          "Hi " + v.recipientName + ",", "",
          v.adminMessage, "",
          "Reference:",
          v.conversationId, "",
          "Regards,",
          BRAND,
          v.supportContact
        ].join("\n");
      }
    },

    /* ============ ADMIN INTERNAL COPY ============ */
    adminInternalCopy: {
      role: "internal",
      subject: function (v) { return "Admin sent a contact message — " + v.conversationId; },
      allowedVars: ["recipientName", "recipientEmail", "adminSubject",
                    "adminMessage", "conversationId", "adminIdentity", "timestamp"],
      html: function (v) {
        return shell(
          badge("EKGURU INTERNAL COPY", "warn") + '<div style="height:12px"></div>' +
          table([
            ["Recipient", v.recipientName],
            ["Recipient Email", v.recipientEmail],
            ["Subject", v.adminSubject],
            ["Message Sent", v.adminMessage],
            ["Reference", v.conversationId],
            ["Sent By", v.adminIdentity],
            ["Timestamp", v.timestamp]
          ])
        );
      },
      text: function (v) {
        return [
          "EKGURU INTERNAL COPY", "",
          "Recipient:", v.recipientName,
          "Recipient Email:", v.recipientEmail,
          "Subject:", v.adminSubject, "",
          "Message Sent:", v.adminMessage, "",
          "Reference:", v.conversationId,
          "Sent By:", v.adminIdentity,
          "Timestamp:", v.timestamp
        ].join("\n");
      }
    }
  };

  /* ----------------------------------------------------------
     ROLE-LANGUAGE QA  (§27-H)
     A tutor mail must not read like a student mail, and vice
     versa; internal wording must never leak to public roles.
     ---------------------------------------------------------- */
  var ROLE_QA = {
    bookingStudent: {
      mustSay: ["congratulations", "your booking request has been received", "reference"],
      mustNotSay: ["you have received a new booking request", "new lesson request",
                   "student email", "tutor email", "available / not available"]
    },
    bookingTutor: {
      mustSay: ["congratulations", "you have received a new booking request", "available"],
      mustNotSay: ["your booking request has been received", "you booked", "your booking"]
    },
    bookingInternal: {
      mustSay: ["internal booking", "delivery"],
      mustNotSay: []
    },
    contactVisitor: {
      mustSay: ["thank you", "we have received your message", "reference"],
      mustNotSay: ["internal contact", "reply-to", "internal action"]
    },
    contactInternal: {
      mustSay: ["internal contact", "reply-to"],
      mustNotSay: ["congratulations", "you have received a new booking"]
    },
    adminOutbound: {
      mustSay: ["regards"],
      mustNotSay: ["internal copy", "internal booking", "new booking request"]
    },
    adminInternalCopy: {
      mustSay: ["internal copy", "sent by"],
      mustNotSay: []
    }
  };

  /* ----------------------------------------------------------
     RENDER + VALIDATION  (§29)
     ---------------------------------------------------------- */
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
       is the honest state for optional fields. */
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

    /* Header-injection defence: a subject is a single line. */
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
    bookingStudent: {
      studentName: "Priya", bookingId: "BOOK-TEST-001", tutorName: "Tara",
      studentRequirement: "Conversation practice", date: "20 September 2026",
      time: "7:00 PM", timezone: "Asia/Kolkata",
      bookingStatus: "Request received — waiting for Tara to confirm",
      nextStep: "Tara has your request and will reply to this address to confirm the time. This is a request, not a confirmed booking.",
      supportEmail: "EkGuruLearning@gmail.com", siteUrl: "https://ekguru.shop/"
    },
    bookingTutor: {
      tutorName: "Tara", bookingId: "BOOK-TEST-001", studentName: "Priya",
      studentEmail: "priya@example.com", date: "20 September 2026",
      time: "7:00 PM", timezone: "Asia/Kolkata", lessonType: "Trial lesson · 50 min",
      studentRequirement: "Conversation practice",
      tutorNextAction: "Please reply to this email / use the available booking action to confirm whether you are available.",
      tutorAltTimeInstruction: "reply with the time that suits you",
      supportEmail: "EkGuruLearning@gmail.com", siteUrl: "https://ekguru.shop/"
    },
    bookingInternal: {
      bookingId: "BOOK-TEST-001", studentName: "Priya", studentEmail: "priya@example.com",
      tutorName: "Tara", tutorId: "tara", tutorEmail: "TUTOR_EMAIL_UNAVAILABLE",
      date: "20 September 2026", time: "7:00 PM", timezone: "Asia/Kolkata",
      lessonType: "Trial lesson · 50 min", studentRequirement: "Conversation practice",
      bookingStatus: "sent",
      studentDeliveryStatus: "ACCEPTED", tutorDeliveryStatus: "NOT_ATTEMPTED",
      internalDeliveryStatus: "ACCEPTED",
      adminNextAction: "Confirm the time with the learner.", sourcePage: "/find-tutors.html"
    },
    contactVisitor: {
      visitorName: "Priya", contactId: "C-TEST01",
      message: "Do you teach complete beginners?",
      nextStep: "A person reads every message. You will get a reply within a day.",
      supportEmail: "EkGuruLearning@gmail.com", siteUrl: "https://ekguru.shop/"
    },
    contactInternal: {
      contactId: "C-TEST01", visitorName: "Priya", visitorEmail: "priya@example.com",
      subject: "A question about lessons", message: "Do you teach complete beginners?",
      timestamp: "11 Sep 2026, 3:00 PM", sourcePage: "/contact/",
      adminNextAction: "Reply to the visitor within a day."
    },
    adminOutbound: {
      recipientName: "Priya", adminSubject: "Your lesson time is confirmed",
      adminMessage: "Your trial lesson with Tara is confirmed for 7:00 PM. See you then!",
      conversationId: "ADMIN-001", supportContact: "EkGuruLearning@gmail.com"
    },
    adminInternalCopy: {
      recipientName: "Priya", recipientEmail: "priya@example.com",
      adminSubject: "Your lesson time is confirmed",
      adminMessage: "Your trial lesson with Tara is confirmed for 7:00 PM. See you then!",
      conversationId: "ADMIN-001", adminIdentity: "Prakash (admin)",
      timestamp: "11 Sep 2026, 3:05 PM"
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
