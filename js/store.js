/* =========================================================
   EkGuru — BOOKING LEDGER
   ---------------------------------------------------------
   HONEST ANSWER FIRST

   GitHub does not have a built-in database. GitHub Pages
   serves files and nothing else — no server, no SQL, no
   storage you can write to from a visitor's browser. Anyone
   who tells you otherwise is selling something. So "GitHub ka
   inbuilt database" does not exist and cannot be added.

   What DOES exist is a real database you are already writing
   to without realising it, plus one you own outright. Together
   they give you everything a small booking database needs.

   ---------------------------------------------------------
   THE THREE LAYERS

   1. FORMSUBMIT ARCHIVE  — a real server-side database
      Every booking request sent through js/mailer.js is
      already being stored by FormSubmit, timestamped, for 30
      days. It has a read API, it allows cross-origin reads, so
      admin.html can list every booking you ever received.
      Free. Nothing to set up beyond asking for a key once.
      Limits: 30 day retention, 5 reads per day.

   2. THIS FILE — the browser's own ledger
      Every booking is also written to localStorage on the
      device that made it. Two uses:
        · the student sees their own booking history
        · on YOUR machine, opening admin.html shows every
          booking you have personally tested or taken
      It is per-device, so it is a convenience, not the record.

   3. THE EXPORT — the copy you actually own
      admin.html can pour layers 1 and 2 into a CSV or JSON
      file. Do that once a month and the 30-day limit stops
      mattering. That file is yours, forever, in a spreadsheet.

   ---------------------------------------------------------
   WHAT THIS IS NOT

   It is not multi-user, it does not sync between devices, and
   layer 2 disappears if the visitor clears their browser. If
   EkGuru ever needs real accounts and a shared database, the
   honest answer is that GitHub Pages is the wrong host for
   that and you would move to something with a backend. Until
   then, this covers a booking business genuinely well.
   ========================================================= */

(function () {
  "use strict";

  var KEY = "ekguru_bookings_v1";
  var LIMIT = 500;                 // plenty; keeps localStorage small

  /* =========================================================
     ACTIVITY LOG
     ---------------------------------------------------------
     Bookings are the outcome. This records the steps that lead
     to one, so the dashboard can show what people actually do:
     which tutors get looked at, who opens the booking box and
     abandons it, what visitors search for and find nothing.

     Stored in the visitor's own browser, exactly like the
     booking ledger, and never sent anywhere. On YOUR machine
     it shows your own activity; the real value is the pattern
     it captures per session, which the dashboard summarises.

     Deliberately NOT recorded: anything typed into the booking
     form, IP addresses, anything that identifies a person.
     Only which page, which tutor, and which action.
     ========================================================= */
  var LOG_KEY = "ekguru_activity_v1";
  var LOG_LIMIT = 800;

  function readAll() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return [];
      var a = JSON.parse(raw);
      return Array.isArray(a) ? a : [];
    } catch (e) { return []; }
  }

  function writeAll(list) {
    try {
      localStorage.setItem(KEY, JSON.stringify(list.slice(-LIMIT)));
      return true;
    } catch (e) {
      /* Quota full or private browsing. A booking must never fail
         because the diary is full, so this is swallowed. */
      return false;
    }
  }

  /* A short readable id, e.g. EK-8F3K2Q. Not a security token —
     just something a student can quote in an email. */
  function makeRef() {
    var A = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";   // no I,O,0,1
    var s = "";
    for (var i = 0; i < 6; i++) s += A.charAt(Math.floor(Math.random() * A.length));
    return "EK-" + s;
  }

  /* ---------- activity ---------- */
  function readLog() {
    try {
      var raw = localStorage.getItem(LOG_KEY);
      var a = raw ? JSON.parse(raw) : [];
      return Array.isArray(a) ? a : [];
    } catch (e) { return []; }
  }
  function writeLog(list) {
    try { localStorage.setItem(LOG_KEY, JSON.stringify(list.slice(-LOG_LIMIT))); return true; }
    catch (e) { return false; }
  }

  /* One id per browser session, so the dashboard can count
     visits rather than clicks. Not a tracking cookie: it lives
     in sessionStorage and dies when the tab closes. */
  function sessionId() {
    try {
      var v = sessionStorage.getItem("ekguru_sid");
      if (!v) {
        v = "s" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
        sessionStorage.setItem("ekguru_sid", v);
      }
      return v;
    } catch (e) { return "s0"; }
  }

  var Store = {

    /* Exposed so a booking can be given its reference BEFORE the
       email goes out, rather than after. */
    makeRef: makeRef,


    /* Write one booking. Returns the stored record, including
       its reference, so the confirmation screen can show it. */
    add: function (b) {
      var rec = {
        /* The caller may supply a reference it has already shown the
           student or written into an email. Only mint a new one when
           there is none, so the email, the screen and this ledger all
           quote the same code. */
        ref: b.ref || makeRef(),
        at: new Date().toISOString(),
        tutorId: b.tutorId || "",
        tutor: b.tutor || "",
        name: b.name || "",
        email: b.email || "",
        level: b.level || "",
        timezone: b.timezone || "",
        goal: b.goal || "",
        slot: b.slot || "",
        priceUSD: b.priceUSD == null ? "" : b.priceUSD,
        priceShown: b.priceShown || "",
        lang: (document.documentElement.getAttribute("lang") || "en"),
        page: b.page || (location && location.href) || "",
        status: b.status || "sent",       // sent | failed
        delivered: b.delivered || []      // which inboxes it reached
      };
      var all = readAll();
      all.push(rec);
      writeAll(all);
      return rec;
    },

    /* Everything on this device, newest first. */
    all: function () {
      return readAll().slice().reverse();
    },

    /* Just this student's own history, for a "your bookings" list. */
    mine: function (email) {
      if (!email) return [];
      var e = String(email).toLowerCase();
      return readAll().filter(function (r) {
        return String(r.email).toLowerCase() === e;
      }).reverse();
    },

    byTutor: function (id) {
      return readAll().filter(function (r) { return r.tutorId === id; }).reverse();
    },

    count: function () { return readAll().length; },

    /* Mark a record after the fact, e.g. the tutor confirmed. */
    update: function (ref, patch) {
      var all = readAll(), hit = false;
      all.forEach(function (r) {
        if (r.ref === ref) { for (var k in patch) r[k] = patch[k]; hit = true; }
      });
      if (hit) writeAll(all);
      return hit;
    },

    remove: function (ref) {
      var all = readAll();
      var out = all.filter(function (r) { return r.ref !== ref; });
      writeAll(out);
      return all.length - out.length;
    },

    clear: function () {
      try { localStorage.removeItem(KEY); } catch (e) {}
    },

    /* =========================================================
       ACTIVITY
       ========================================================= */

    /* track("view_tutor", { tutor: "shikha-dutta" })
       Never throws — a logging failure must not break the site. */
    track: function (event, detail) {
      try {
        var all = readLog();
        var last = all[all.length - 1];
        var now = Date.now();

        /* collapse an identical event fired twice within 2s */
        if (last && last.e === event && now - Date.parse(last.at) < 2000 &&
            JSON.stringify(last.d || {}) === JSON.stringify(detail || {})) return null;

        var rec = {
          at: new Date(now).toISOString(),
          e: event,
          d: detail || {},
          sid: sessionId(),
          lang: (document.documentElement.getAttribute("lang") || "en"),
          page: (location && location.pathname) || ""
        };
        all.push(rec);
        writeLog(all);
        return rec;
      } catch (e) { return null; }
    },

    activity: function () { return readLog().slice().reverse(); },
    activityCount: function () { return readLog().length; },
    clearActivity: function () { try { localStorage.removeItem(LOG_KEY); } catch (e) {} },

    /* A plain summary for the dashboard. */
    summary: function () {
      var log = readLog(), out = {
        events: log.length, sessions: {}, byEvent: {}, tutorViews: {},
        searches: {}, noResults: {}, languages: {}, days: {}
      };
      log.forEach(function (r) {
        out.sessions[r.sid] = 1;
        out.byEvent[r.e] = (out.byEvent[r.e] || 0) + 1;
        out.languages[r.lang] = (out.languages[r.lang] || 0) + 1;
        out.days[String(r.at).slice(0, 10)] = (out.days[String(r.at).slice(0, 10)] || 0) + 1;
        var d = r.d || {};
        if (d.tutor) out.tutorViews[d.tutor] = (out.tutorViews[d.tutor] || 0) + 1;
        if (r.e === "search" && d.q) out.searches[d.q] = (out.searches[d.q] || 0) + 1;
        if (r.e === "search_empty" && d.q) out.noResults[d.q] = (out.noResults[d.q] || 0) + 1;
      });
      out.sessionCount = Object.keys(out.sessions).length;

      /* ---------- traffic ----------
         Where visitors came from and which pages they landed on.
         Referrer is the hostname only — never the full URL, which
         can carry someone's search terms or private path. */
      out.referrers = {}; out.landing = {}; out.sessionFirst = {};
      var seenSession = {};
      log.forEach(function (r) {
        if (r.e !== "page_view") return;
        var d = r.d || {};
        var host = d.ref || "direct";
        /* our own pages are not a traffic source */
        if (host && host.indexOf("ekgurulearning") > -1) host = "internal";
        out.referrers[host] = (out.referrers[host] || 0) + 1;
        var path = d.path || "/";
        out.landing[path] = (out.landing[path] || 0) + 1;
        /* the first page of each session is the true landing page */
        if (!seenSession[r.sid]) {
          seenSession[r.sid] = 1;
          out.sessionFirst[path] = (out.sessionFirst[path] || 0) + 1;
        }
      });

      /* Group referrers into something readable. */
      out.channels = { "Search engines": 0, "Social": 0, "Direct or typed": 0, "Other sites": 0 };
      Object.keys(out.referrers).forEach(function (h) {
        var n = out.referrers[h];
        if (h === "internal") return;
        if (h === "direct" || !h) out.channels["Direct or typed"] += n;
        else if (/google|bing|duckduckgo|yahoo|yandex|baidu|ecosia|brave/i.test(h))
          out.channels["Search engines"] += n;
        else if (/facebook|instagram|twitter|x\.com|linkedin|reddit|whatsapp|t\.co|youtube|pinterest|telegram/i.test(h))
          out.channels["Social"] += n;
        else out.channels["Other sites"] += n;
      });

      /* A simple per-day series for the last 30 days, so the
         dashboard can draw a trend rather than a single number. */
      out.daily = [];
      for (var i = 29; i >= 0; i--) {
        var dt = new Date(Date.now() - i * 86400000).toISOString().slice(0, 10);
        out.daily.push({ day: dt, n: out.days[dt] || 0 });
      }

      /* How many who opened the booking box went on to send it. */
      var opened = out.byEvent.booking_open || 0;
      var sentN = out.byEvent.booking_sent || 0;
      out.conversion = opened ? Math.round((sentN / opened) * 100) : null;
      return out;
    },

    /* =========================================================
       BUSINESS SUMMARY
       ---------------------------------------------------------
       The dashboard had counters but nothing that answered the
       questions an owner actually has: which tutor is earning,
       what is still unanswered, how much is at stake this month.
       ========================================================= */
    business: function () {
      var all = readAll();
      var now = new Date();
      var monthKey = now.toISOString().slice(0, 7);
      var weekAgo = Date.now() - 7 * 86400000;

      var out = {
        total: all.length, sent: 0, failed: 0, confirmed: 0, declined: 0, pending: 0,
        revenue: 0, revenueMonth: 0, potential: 0,
        byTutor: {}, byLevel: {}, byMonth: {}, students: {}, repeat: 0,
        thisWeek: 0, lastWeek: 0, avgPrice: 0, needsReply: []
      };

      all.forEach(function (r) {
        var price = Number(r.priceUSD) || 0;
        var t = new Date(r.at).getTime();
        var mk = String(r.at).slice(0, 7);

        if (r.status === "failed") out.failed++;
        else out.sent++;
        if (r.status === "confirmed") { out.confirmed++; out.revenue += price; }
        else if (r.status === "declined") out.declined++;
        else if (r.status === "sent") out.pending++;

        if (r.status === "confirmed" && mk === monthKey) out.revenueMonth += price;
        if (r.status !== "failed") out.potential += price;

        if (!out.byTutor[r.tutor]) out.byTutor[r.tutor] =
          { name: r.tutor, id: r.tutorId, total: 0, confirmed: 0, pending: 0, revenue: 0 };
        var bt = out.byTutor[r.tutor];
        bt.total++;
        if (r.status === "confirmed") { bt.confirmed++; bt.revenue += price; }
        if (r.status === "sent") bt.pending++;

        if (r.level) out.byLevel[r.level] = (out.byLevel[r.level] || 0) + 1;
        out.byMonth[mk] = (out.byMonth[mk] || 0) + 1;

        var em = String(r.email || "").toLowerCase();
        if (em) {
          out.students[em] = (out.students[em] || 0) + 1;
          if (out.students[em] === 2) out.repeat++;
        }

        if (t >= weekAgo) out.thisWeek++;
        else if (t >= weekAgo - 7 * 86400000) out.lastWeek++;

        /* anything still "sent" after 48 hours has not been answered */
        if (r.status === "sent" && Date.now() - t > 48 * 3600000) out.needsReply.push(r);
      });

      out.uniqueStudents = Object.keys(out.students).length;
      out.avgPrice = out.total ? (out.potential / out.total) : 0;
      out.confirmRate = out.sent ? Math.round((out.confirmed / out.sent) * 100) : null;
      out.tutorList = Object.keys(out.byTutor)
        .map(function (k) { return out.byTutor[k]; })
        .sort(function (a, b) { return b.total - a.total; });
      return out;
    },

    activityCSV: function () {
      var rows = readLog().slice().reverse();
      var cols = ["at", "e", "sid", "lang", "page", "detail"];
      function cell(v) {
        if (v == null) v = "";
        v = String(v);
        if (/^[=+\-@\t\r]/.test(v)) v = "'" + v;
        return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
      }
      var out = [cols.join(",")];
      rows.forEach(function (r) {
        out.push([r.at, r.e, r.sid, r.lang, r.page,
                  JSON.stringify(r.d || {})].map(cell).join(","));
      });
      return "\uFEFF" + out.join("\r\n");
    },

    /* ---------- Export: the copy you actually own ---------- */

    toJSON: function (rows) {
      return JSON.stringify(rows || Store.all(), null, 2);
    },

    toCSV: function (rows) {
      rows = rows || Store.all();
      var cols = ["ref", "at", "tutor", "tutorId", "name", "email", "level",
                  "timezone", "slot", "priceUSD", "priceShown", "goal",
                  "lang", "status", "page"];
      function cell(v) {
        if (v == null) v = "";
        v = String(v);

        /* CSV INJECTION GUARD
           A student types their own name and goal. If either begins
           with = + - @ or a tab, Excel and Google Sheets treat the
           cell as a FORMULA when the export is opened. A name like
             =cmd|'/c calc'!A1
           can run a command on the machine that opens the file.
           This is a real, documented attack on exported CSVs.

           Prefixing a single quote makes the cell literal text in
           both Excel and Sheets, and the quote is not displayed. */
        if (/^[=+\-@\t\r]/.test(v)) v = "'" + v;

        /* Excel and Sheets both need this exact quoting */
        return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
      }
      var out = [cols.join(",")];
      rows.forEach(function (r) {
        out.push(cols.map(function (c) { return cell(r[c]); }).join(","));
      });
      /* BOM so Excel opens UTF-8 names and ₹ symbols correctly */
      return "\uFEFF" + out.join("\r\n");
    },

    download: function (filename, text, mime) {
      try {
        var blob = new Blob([text], { type: (mime || "text/plain") + ";charset=utf-8" });
        var url = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url; a.download = filename;
        document.body.appendChild(a); a.click();
        document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
        return true;
      } catch (e) { return false; }
    },

    /* ---------- Import, so an export can be merged back ---------- */
    importJSON: function (text) {
      var incoming;
      try { incoming = JSON.parse(text); } catch (e) { return { ok: false, error: "not valid JSON" }; }
      if (!Array.isArray(incoming)) return { ok: false, error: "expected a list of bookings" };
      var all = readAll();
      var have = {};
      all.forEach(function (r) { have[r.ref] = 1; });
      var added = 0;
      incoming.forEach(function (r) {
        if (r && r.ref && !have[r.ref]) { all.push(r); have[r.ref] = 1; added++; }
      });
      all.sort(function (a, b) { return String(a.at).localeCompare(String(b.at)); });
      writeAll(all);
      return { ok: true, added: added, total: all.length };
    }
  };

  /* Every page view, logged once on load. Placed here rather than
     in main.js because the pre-rendered and translated pages do not
     load main.js — and those are exactly the pages arriving from
     search, so leaving them out would have skewed everything. */
  (function () {
    function logView() {
      try {
        Store.track("page_view", {
          path: (location.pathname || "").replace(/\/EkGuru\//, "/"),
          ref: document.referrer ? (function () {
            try { return new URL(document.referrer).hostname; } catch (e) { return ""; }
          })() : "direct"
        });
      } catch (e) {}
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", logView);
    } else logView();
  })();

  window.EkGuruStore = Store;
})();
