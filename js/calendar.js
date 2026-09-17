/* =========================================================
   EkGuru — REAL CALENDAR BOOKING (Cal.com)
   ---------------------------------------------------------
   WHAT THIS ADDS, AND WHY IT IS BETTER

   Today a student picks a slot and EkGuru emails the tutor a
   request. The tutor then has to reply and agree it. That
   works, but it has real weaknesses:

     · the slot shown might already be taken — we cannot see
       the tutor's actual calendar
     · nobody gets a confirmed booking, only a request
     · no reminder before the lesson
     · no video link created automatically
     · if the tutor forgets to reply, the student hears nothing

   Cal.com fixes all of that on its free tier: it reads the
   tutor's real Google or Outlook calendar, offers only genuine
   free slots, confirms instantly, sends reminders, and creates
   the meeting link. Open source, free for individuals.

   ---------------------------------------------------------
   THIS IS OPT-IN, PER TUTOR

   A tutor who has not set up Cal.com keeps the existing email
   flow exactly as it is. Nothing changes for them. A tutor who
   has one gets a real calendar on their profile.

   Both can be true at the same time, which matters: you are
   not forcing four people to sign up for something before the
   site keeps working.

   ---------------------------------------------------------
   TO SWITCH ON FOR A TUTOR

     1. She signs up free at cal.com and picks a username
     2. She connects her Google Calendar and sets her hours
     3. She creates an event type, e.g. "50min"
     4. You add one line to her file in js/tutors/:

          calLink: "shikha/50min",

   That is all. Her profile then shows a real booking calendar
   instead of the request form.

   To turn it off again, blank the line.

   ---------------------------------------------------------
   PRIVACY

   Cal.com's embed script is only loaded on a page where a
   tutor actually has a calLink. No calLink anywhere on the
   page means no third-party request at all.
   ========================================================= */

(function () {
  "use strict";

  var S = window.EKGURU_SITE || {};
  var CFG = S.calendar || {};
  var loaded = false;

  function tutors() { return window.EKGURU_TUTORS || []; }

  /* Does any tutor on this page use a calendar? */
  function anyCalLink() {
    return tutors().some(function (t) { return t.calLink; });
  }

  /* The official Cal.com embed loader, added only when needed. */
  function loadCal() {
    if (loaded) return;
    loaded = true;
    (function (C, A, L) {
      var p = function (a, ar) { a.q.push(ar); };
      var d = C.document;
      C.Cal = C.Cal || function () {
        var cal = C.Cal, ar = arguments;
        if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; }
        if (ar[0] === L) {
          var api = function () { p(api, arguments); };
          var namespace = ar[1];
          api.q = api.q || [];
          if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); }
          else p(cal, ar);
          return;
        }
        p(cal, ar);
      };
    })(window, "https://app.cal.com/embed/embed.js", "init");

    try {
      window.Cal("init", { origin: "https://cal.com" });
      window.Cal("ui", {
        theme: "light",
        styles: { branding: { brandColor: CFG.brandColor || "#e0682a" } },
        hideEventTypeDetails: false,
        layout: "month_view"
      });
    } catch (e) {}
  }

  /* Open a tutor's calendar in a Cal.com overlay. */
  function open(tutor, prefill) {
    if (!tutor || !tutor.calLink) return false;
    loadCal();
    try {
      var cfg = { layout: "month_view" };
      if (prefill && prefill.name) cfg.name = prefill.name;
      if (prefill && prefill.email) cfg.email = prefill.email;
      if (prefill && prefill.notes) cfg.notes = prefill.notes;

      window.Cal("modal", { calLink: tutor.calLink, config: cfg });

      /* Recorded like any other booking step, so the funnel in the
         admin dashboard stays complete. */
      try { if (window.EkGuruStore) window.EkGuruStore.track("calendar_open", { tutor: tutor.id }); } catch (e) {}
      try { if (window.EkGuruAnalytics) window.EkGuruAnalytics.event("calendar-open", tutor.name); } catch (e) {}
      return true;
    } catch (e) {
      return false;
    }
  }

  /* Any button marked data-cal="<tutorId>" opens that calendar.
     main.js renders one on the profile of a tutor who has a
     calLink, in place of the email request button. */
  function init() {
    if (!anyCalLink()) return;      /* no calendar on this page, load nothing */

    document.addEventListener("click", function (e) {
      var b = e.target.closest("[data-cal]");
      if (!b) return;
      e.preventDefault();
      var id = b.getAttribute("data-cal");
      var t = tutors().filter(function (x) { return x.id === id; })[0];
      if (!open(t)) {
        /* If Cal.com cannot load — blocked, offline — fall back to
           the email request rather than leaving a dead button. */
        if (window.EkGuruBook) window.EkGuruBook(id);
      }
    });

    /* Warm the script once the page is idle, so the first click
       opens instantly rather than waiting on a download. */
    if ("requestIdleCallback" in window) {
      requestIdleCallback(loadCal, { timeout: 4000 });
    } else {
      setTimeout(loadCal, 3000);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else init();

  window.EkGuruCalendar = {
    open: open,
    /* Used by main.js to decide which button to render. */
    has: function (tutor) { return !!(tutor && tutor.calLink); },
    anyOnPage: anyCalLink
  };
})();
