/* =========================================================
   EkGuru — production email templates
   Five public IDs + two admin extras. Missing fields are omitted.
   ========================================================= */
(function (root) {
  "use strict";

  var BRAND = "EkGuru";
  var ACCENT = "#4f32d9";
  var SITE_URL = "https://ekguru.shop/";
  var SUPPORT = "EkGuruLearning@gmail.com";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function present(v) {
    if (v == null) return false;
    var s = String(v).trim();
    if (!s) return false;
    if (/^(undefined|null|n\/a|na)$/i.test(s)) return false;
    return true;
  }
  function oneLine(s) {
    return String(s == null ? "" : s).replace(/[\r\n\t]+/g, " ").trim().slice(0, 150);
  }
  function fill(str, data) {
    return String(str).replace(/\{\{\s*([a-zA-Z0-9_]+)\s*\}\}/g, function (_, k) {
      return present(data[k]) ? String(data[k]) : "";
    }).replace(/\s{2,}/g, " ").replace(/\s+[—–-]\s*$/, "").trim();
  }
  function htmlToText(html) {
    return String(html || "")
      .replace(/<style[\s\S]*?<\/style>/gi, "")
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/<\/p>/gi, "\n")
      .replace(/<\/tr>/gi, "\n")
      .replace(/<\/h[1-6]>/gi, "\n")
      .replace(/<[^>]+>/g, " ")
      .replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&")
      .replace(/&quot;/g, "\"").replace(/&#39;/g, "'")
      .replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n")
      .replace(/[ \t]{2,}/g, " ").trim();
  }

  function shell(inner, preheader) {
    return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">' +
      '<meta name="viewport" content="width=device-width">' +
      "<title>" + esc(BRAND) + "</title></head>" +
      '<body style="margin:0;padding:0;background:#f6f4ff;font-family:Inter,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#10131f;">' +
      (present(preheader) ? '<div style="display:none;max-height:0;overflow:hidden;opacity:0">' + esc(preheader) + "</div>" : "") +
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f4ff;padding:24px 12px"><tr><td align="center">' +
      '<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#fff;border:1px solid #e4e4ef;border-radius:16px;overflow:hidden">' +
      '<tr><td style="padding:18px 24px;background:linear-gradient(135deg,#4f32d9,#8b5cf6);color:#fff">' +
      '<div style="font-weight:800;font-size:16px">EkGuru</div>' +
      '<div style="font-size:12px;opacity:.9">One Student. One Goal. One Guru.</div></td></tr>' +
      '<tr><td style="padding:28px 24px 12px">' + inner + "</td></tr>" +
      '<tr><td style="padding:8px 24px 24px;color:#5f6577;font-size:12px;line-height:1.55">' +
      "Sent by EkGuru because of a booking or form on " +
      '<a href="' + SITE_URL + '" style="color:' + ACCENT + '">ekguru.shop</a>.' +
      "</td></tr></table></td></tr></table></body></html>";
  }
  function h1(t) {
    return '<h1 style="margin:0 0 12px;font-size:22px;line-height:1.25">' + esc(t) + "</h1>";
  }
  function p(t) {
    if (!present(t)) return "";
    return '<p style="margin:0 0 14px;font-size:15px;line-height:1.65">' + esc(t) + "</p>";
  }
  function row(label, value) {
    if (!present(value)) return "";
    return '<tr><td style="padding:7px 0;color:#5f6577;font-size:13px;width:38%;vertical-align:top">' +
      esc(label) + '</td><td style="padding:7px 0;font-size:14px;font-weight:600">' +
      esc(value) + "</td></tr>";
  }
  function table(pairs) {
    var inner = "";
    (pairs || []).forEach(function (r) { inner += row(r[0], r[1]); });
    if (!inner) return "";
    return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:8px 0 18px;border-top:1px solid #e4e4ef;border-bottom:1px solid #e4e4ef">' +
      inner + "</table>";
  }
  function cta(href, label) {
    if (!present(href) || !present(label)) return "";
    return '<p style="margin:16px 0"><a href="' + esc(href) +
      '" style="display:inline-block;background:' + ACCENT +
      ';color:#fff;text-decoration:none;font-weight:700;padding:12px 18px;border-radius:999px">' +
      esc(label) + "</a></p>";
  }

  function norm(v) {
    v = v || {};
    var o = {};
    Object.keys(v).forEach(function (k) { o[k] = v[k]; });
    if (!present(o.sessionTitle) && present(o.lessonType)) o.sessionTitle = o.lessonType;
    if (!present(o.bookingDate) && present(o.date)) o.bookingDate = o.date;
    if (!present(o.bookingTime) && present(o.time)) o.bookingTime = o.time;
    if (!present(o.name) && present(o.studentName)) o.name = o.studentName;
    if (!present(o.name) && present(o.visitorName)) o.name = o.visitorName;
    if (!present(o.email) && present(o.studentEmail)) o.email = o.studentEmail;
    if (!present(o.email) && present(o.visitorEmail)) o.email = o.visitorEmail;
    if (!present(o.pageUrl) && present(o.sourcePage)) o.pageUrl = o.sourcePage;
    if (!present(o.bookingId) && present(o.contactId)) o.bookingId = o.contactId;
    if (!present(o.notes) && present(o.studentRequirement)) o.notes = o.studentRequirement;
    if (!present(o.subject) && present(o.adminSubject)) o.subject = o.adminSubject;
    if (!present(o.body) && present(o.adminMessage)) o.body = o.adminMessage;
    if (!present(o.to) && present(o.recipientEmail)) o.to = o.recipientEmail;
    return o;
  }

  var TEMPLATES = {
    booking_student_confirmation: {
      key: "bookingStudent",
      role: "student",
      subject: "Your EkGuru booking is confirmed — {{tutorName}}",
      allowedVars: ["studentName", "tutorName", "sessionTitle", "bookingDate", "bookingTime", "duration", "amount", "bookingId", "bookingUrl", "date", "time", "lessonType", "studentRequirement", "timezone", "bookingStatus", "nextStep", "supportEmail", "siteUrl"],
      html: function (v) {
        var who = present(v.studentName) ? "Hello " + v.studentName + "." : "Hello.";
        return shell(
          h1("Your booking is confirmed") +
          p(who) +
          p("This confirms your lesson" + (present(v.tutorName) ? " with " + v.tutorName : "") + " on EkGuru.") +
          table([
            ["Tutor", v.tutorName],
            ["Session", v.sessionTitle || v.lessonType],
            ["Date", v.bookingDate || v.date],
            ["Time", v.bookingTime || v.time],
            ["Duration", v.duration],
            ["Amount", v.amount],
            ["Your message", v.studentRequirement || v.notes],
            ["Booking ID", v.bookingId]
          ]) +
          cta(v.bookingUrl, "Open booking details") +
          p(v.nextStep) +
          p("If the time no longer works, reply to this email."),
          "Your EkGuru lesson is booked."
        );
      }
    },
    booking_tutor_notification: {
      key: "bookingTutor",
      role: "tutor",
      subject: "New booking on EkGuru — {{studentName}}",
      allowedVars: ["tutorName", "studentName", "studentEmail", "sessionTitle", "bookingDate", "bookingTime", "duration", "amount", "notes", "bookingId", "bookingUrl", "date", "time", "timezone", "lessonType", "studentRequirement", "tutorNextAction", "tutorAltTimeInstruction", "supportEmail", "siteUrl"],
      html: function (v) {
        return shell(
          h1("You have a new booking") +
          p("A student booked a lesson with you on EkGuru.") +
          table([
            ["Student", v.studentName],
            ["Student email", v.studentEmail],
            ["Session", v.sessionTitle || v.lessonType],
            ["Date", v.bookingDate || v.date],
            ["Time", v.bookingTime || v.time],
            ["Duration", v.duration],
            ["Amount", v.amount],
            ["Notes", v.notes || v.studentRequirement],
            ["Booking ID", v.bookingId]
          ]) +
          cta(v.bookingUrl, "Open booking") +
          p(v.tutorNextAction) +
          p("Please confirm the meeting link with the student if you have not already."),
          "New student booking on EkGuru."
        );
      }
    },
    booking_internal_record: {
      key: "bookingInternal",
      role: "internal",
      subject: "Booking record — {{tutorName}} ← {{studentName}} — {{bookingId}}",
      allowedVars: ["bookingId", "studentName", "studentEmail", "tutorName", "tutorId", "tutorEmail", "sessionTitle", "bookingDate", "bookingTime", "duration", "amount", "notes", "pageUrl", "date", "time", "timezone", "lessonType", "studentRequirement", "bookingStatus", "studentDeliveryStatus", "tutorDeliveryStatus", "internalDeliveryStatus", "adminNextAction", "sourcePage"],
      html: function (v) {
        return shell(
          h1("Internal booking record") +
          p("A booking was stored. This copy is for EkGuru operations — it is not a payment receipt.") +
          table([
            ["Booking ID", v.bookingId],
            ["Tutor", v.tutorName],
            ["Tutor ID", v.tutorId],
            ["Tutor email", v.tutorEmail],
            ["Student", v.studentName],
            ["Student email", v.studentEmail],
            ["Session", v.sessionTitle || v.lessonType],
            ["Date", v.bookingDate || v.date],
            ["Time", v.bookingTime || v.time],
            ["Duration", v.duration],
            ["Amount", v.amount],
            ["Notes", v.notes || v.studentRequirement],
            ["Status", v.bookingStatus],
            ["Page", v.pageUrl || v.sourcePage]
          ]),
          "Internal booking record."
        );
      }
    },
    contact_submitter_confirmation: {
      key: "contactVisitor",
      role: "submitter",
      subject: "We received your message — EkGuru",
      allowedVars: ["name", "visitorName", "topic", "message", "pageUrl", "contactId", "nextStep", "supportEmail", "siteUrl"],
      html: function (v) {
        var who = present(v.name || v.visitorName) ? "Hello " + (v.name || v.visitorName) + "." : "Hello.";
        return shell(
          h1("We received your message") +
          p(who) +
          p("Thanks for writing to EkGuru. A person will read this and reply to the email you gave us.") +
          table([
            ["Name", v.name || v.visitorName],
            ["Topic", v.topic],
            ["Reference", v.contactId],
            ["Page", v.pageUrl]
          ]) +
          (present(v.message) ? p("Your message:") + p(v.message) : "") +
          p(v.nextStep),
          "EkGuru received your message."
        );
      }
    },
    contact_internal_record: {
      key: "contactInternal",
      role: "internal",
      subject: "New contact message — {{name}}",
      allowedVars: ["name", "visitorName", "email", "visitorEmail", "topic", "subject", "message", "pageUrl", "userAgent", "contactId", "timestamp", "sourcePage", "adminNextAction"],
      html: function (v) {
        return shell(
          h1("New contact message") +
          table([
            ["Name", v.name || v.visitorName],
            ["Email", v.email || v.visitorEmail],
            ["Topic", v.topic],
            ["Subject", v.subject],
            ["Reference", v.contactId],
            ["Page", v.pageUrl || v.sourcePage],
            ["User agent", v.userAgent]
          ]) +
          (present(v.message) ? p("Message:") + p(v.message) : ""),
          "New contact form submission."
        );
      }
    },
    ADMIN_CONTACT_OUTBOUND: {
      key: "adminOutbound",
      role: "recipient",
      subject: "{{subject}}",
      allowedVars: ["recipientName", "adminSubject", "adminMessage", "conversationId", "supportContact", "subject", "body", "to"],
      html: function (v) {
        return shell(
          h1(present(v.adminSubject || v.subject) ? (v.adminSubject || v.subject) : "Message from EkGuru") +
          p(v.adminMessage || v.body) +
          table([["Reference", v.conversationId]]),
          present(v.adminSubject || v.subject) ? (v.adminSubject || v.subject) : "Message from EkGuru"
        );
      }
    },
    ADMIN_CONTACT_INTERNAL_COPY: {
      key: "adminInternalCopy",
      role: "internal",
      subject: "{{subject}}",
      allowedVars: ["recipientName", "recipientEmail", "adminSubject", "adminMessage", "conversationId", "adminIdentity", "timestamp", "subject", "body", "to"],
      html: function (v) {
        return shell(
          h1("Admin message copy") +
          table([
            ["To", v.recipientName],
            ["Recipient email", v.recipientEmail || v.to],
            ["Subject", v.adminSubject || v.subject],
            ["Sent by", v.adminIdentity],
            ["Reference", v.conversationId]
          ]) +
          p(v.adminMessage || v.body),
          "Copy of an admin message."
        );
      }
    }
  };

  var ALIAS = {
    bookingStudent: "booking_student_confirmation",
    bookingTutor: "booking_tutor_notification",
    bookingInternal: "booking_internal_record",
    contactVisitor: "contact_submitter_confirmation",
    contactInternal: "contact_internal_record",
    adminOutbound: "ADMIN_CONTACT_OUTBOUND",
    adminInternalCopy: "ADMIN_CONTACT_INTERNAL_COPY",
    BOOKING_STUDENT_CONFIRMATION: "booking_student_confirmation",
    BOOKING_TUTOR_NOTIFICATION: "booking_tutor_notification",
    BOOKING_EKGURU_NOTIFICATION: "booking_internal_record",
    BOOKING_INTERNAL_RECORD: "booking_internal_record",
    CONTACT_VISITOR_CONFIRMATION: "contact_submitter_confirmation",
    CONTACT_EKGURU_NOTIFICATION: "contact_internal_record",
    CONTACT_SUBMITTER_CONFIRMATION: "contact_submitter_confirmation",
    CONTACT_INTERNAL_RECORD: "contact_internal_record"
  };

  var PUBLIC_IDS = [
    "booking_student_confirmation",
    "booking_tutor_notification",
    "booking_internal_record",
    "contact_submitter_confirmation",
    "contact_internal_record"
  ];
  var WHITELIST = PUBLIC_IDS.concat(["ADMIN_CONTACT_OUTBOUND", "ADMIN_CONTACT_INTERNAL_COPY"]);

  var FIXTURES = {
    bookingStudent: {
      studentName: "Priya", tutorName: "Tara", sessionTitle: "Trial lesson",
      bookingDate: "20 September 2026", bookingTime: "19:00", duration: "50 min",
      bookingId: "EK-TEST-01", date: "20 September 2026", time: "19:00",
      lessonType: "Trial lesson", timezone: "Asia/Kolkata", bookingStatus: "Request received",
      nextStep: "Tara will reply to confirm the time.", studentRequirement: "Conversation practice",
      supportEmail: SUPPORT, siteUrl: SITE_URL
    },
    bookingTutor: {
      tutorName: "Tara", studentName: "Priya", studentEmail: "priya@example.com",
      sessionTitle: "Trial lesson", bookingDate: "20 September 2026", bookingTime: "19:00",
      bookingId: "EK-TEST-01", date: "20 September 2026", time: "19:00",
      timezone: "Asia/Kolkata", lessonType: "Trial lesson",
      studentRequirement: "Conversation practice",
      tutorNextAction: "Please reply to confirm whether you are available.",
      tutorAltTimeInstruction: "reply with the time that suits you",
      supportEmail: SUPPORT, siteUrl: SITE_URL
    },
    bookingInternal: {
      bookingId: "EK-TEST-01", studentName: "Priya", studentEmail: "priya@example.com",
      tutorName: "Tara", tutorId: "tara", tutorEmail: "tara@example.com",
      sessionTitle: "Trial lesson", bookingDate: "20 September 2026", bookingTime: "19:00",
      date: "20 September 2026", time: "19:00", timezone: "Asia/Kolkata",
      lessonType: "Trial lesson", studentRequirement: "Conversation practice",
      bookingStatus: "Request received", studentDeliveryStatus: "SENDING",
      tutorDeliveryStatus: "SENDING", internalDeliveryStatus: "SENDING",
      adminNextAction: "Confirm the time with the tutor.",
      sourcePage: "https://ekguru.shop/find-tutors.html"
    },
    contactVisitor: {
      name: "Aarav", visitorName: "Aarav", topic: "General",
      message: "Do you teach absolute beginners?",
      contactId: "C-TEST01", nextStep: "A person reads every message.",
      supportEmail: SUPPORT, siteUrl: SITE_URL, pageUrl: "https://ekguru.shop/contact/"
    },
    contactInternal: {
      name: "Aarav", visitorName: "Aarav", email: "aarav@example.com",
      visitorEmail: "aarav@example.com", topic: "General",
      subject: "Question about lessons", message: "Do you teach absolute beginners?",
      contactId: "C-TEST01", timestamp: "Sun, 20 Sep 2026 12:00:00 GMT",
      sourcePage: "https://ekguru.shop/contact/",
      adminNextAction: "Reply to the visitor within a day."
    },
    adminOutbound: {
      recipientName: "Priya", adminSubject: "Your lesson time is confirmed",
      adminMessage: "Your trial lesson with Tara is confirmed. See you then!",
      conversationId: "ADMIN-TEST01", supportContact: SUPPORT,
      subject: "Your lesson time is confirmed"
    },
    adminInternalCopy: {
      recipientName: "Priya", recipientEmail: "student@example.com",
      adminSubject: "Your lesson time is confirmed",
      adminMessage: "Your trial lesson with Tara is confirmed. See you then!",
      conversationId: "ADMIN-TEST01", adminIdentity: "admin dashboard",
      timestamp: "Sun, 20 Sep 2026 12:00:00 GMT",
      subject: "Your lesson time is confirmed"
    }
  };

  var ROLE_QA = {
    bookingStudent: {
      mustSay: ["booking is confirmed", "EkGuru"],
      mustNotSay: ["you have a new booking", "internal booking record", "TUTOR_EMAIL_UNAVAILABLE"]
    },
    bookingTutor: {
      mustSay: ["new booking", "student"],
      mustNotSay: ["your booking is confirmed", "internal booking record"]
    },
    bookingInternal: {
      mustSay: ["internal booking record"],
      mustNotSay: ["your booking is confirmed"]
    },
    contactVisitor: {
      mustSay: ["we received your message"],
      mustNotSay: ["new contact message", "user agent"]
    },
    contactInternal: {
      mustSay: ["new contact message"],
      mustNotSay: ["thanks for writing to ekguru"]
    },
    adminOutbound: { mustSay: ["ekguru"], mustNotSay: ["admin message copy"] },
    adminInternalCopy: { mustSay: ["admin message copy"], mustNotSay: [] }
  };

  function canonical(id) {
    id = String(id || "");
    return ALIAS[id] || id;
  }

  function render(id, data) {
    var key = canonical(id);
    var tpl = TEMPLATES[key];
    if (!tpl) return { ok: false, errors: ["unknown type " + id] };
    var v = norm(data);
    var subject = oneLine(fill(tpl.subject, v) || (present(v.adminSubject) ? v.adminSubject : "EkGuru"));
    var html = tpl.html(v);
    var text = htmlToText(html);
    return {
      ok: true,
      errors: [],
      subject: subject,
      html: html,
      text: text,
      template: tpl.key,
      id: key,
      audience: tpl.role
    };
  }

  var ROUTES = [
    { type: "booking_student_confirmation", role: "booking_student", template: "bookingStudent" },
    { type: "booking_tutor_notification", role: "booking_tutor", template: "bookingTutor" },
    { type: "booking_internal_record", role: "booking_internal", template: "bookingInternal" },
    { type: "contact_submitter_confirmation", role: "contact_submitter", template: "contactVisitor" },
    { type: "contact_internal_record", role: "contact_internal", template: "contactInternal" },
    { type: "ADMIN_CONTACT_OUTBOUND", role: "admin_outbound", template: "adminOutbound" },
    { type: "ADMIN_CONTACT_INTERNAL_COPY", role: "admin_internal_copy", template: "adminInternalCopy" }
  ];

  var api = {
    BRAND: BRAND,
    TEMPLATES: {
      bookingStudent: TEMPLATES.booking_student_confirmation,
      bookingTutor: TEMPLATES.booking_tutor_notification,
      bookingInternal: TEMPLATES.booking_internal_record,
      contactVisitor: TEMPLATES.contact_submitter_confirmation,
      contactInternal: TEMPLATES.contact_internal_record,
      adminOutbound: TEMPLATES.ADMIN_CONTACT_OUTBOUND,
      adminInternalCopy: TEMPLATES.ADMIN_CONTACT_INTERNAL_COPY
    },
    PUBLIC_IDS: PUBLIC_IDS,
    WHITELIST: WHITELIST,
    FIXTURES: FIXTURES,
    ROLE_QA: ROLE_QA,
    ROUTES: ROUTES,
    render: render,
    canonical: canonical,
    esc: esc,
    present: present
  };

  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.EKGURU_EMAIL = api;
  root.EkGuruEmailTemplates = api;
  if (typeof window !== "undefined") {
    window.EKGURU_EMAIL = api;
    window.EkGuruEmailTemplates = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : this);
