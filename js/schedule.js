/* =========================================================
   EkGuru — BUILT-IN CALENDAR
   ---------------------------------------------------------
   WHY THIS EXISTS

   The Integrations panel said "Calendar booking — off", and
   the only way to switch it on was for every tutor to create
   a cal.com account and paste a calLink. Four tutors, four
   sign-ups, none of which had happened. The feature had been
   sitting at "off" since v44.

   But the data needed for a calendar was ALREADY THERE. Every
   tutor file carries a real weekly availability grid:

       Mon: ["09:00","10:00","16:00","18:00","20:00"]
       Sun: []

   That is enough to show the next fourteen days of genuine
   free slots without any third party at all. So this file
   turns existing data into a working calendar, and cal.com
   stays available for any tutor who later wants automatic
   video links and reminders.

   ---------------------------------------------------------
   WHAT THIS DOES AND DOES NOT DO

   DOES
     · shows the next 14 days with real, per-day slots
     · converts every slot into the VISITOR'S timezone
     · hides slots that have already passed today
     · marks days the tutor does not teach
     · feeds the chosen slot straight into the booking form
     · offers an .ics download so the lesson lands in their
       own calendar app

   DOES NOT
     · know about lessons already booked. There is no server,
       so nothing can. A slot shown here is "the tutor
       normally teaches then", not "guaranteed free".

   That distinction is stated on the page. Pretending to have
   live availability we cannot have would produce double
   bookings and angry students, which is far worse than an
   honest label.

   ---------------------------------------------------------
   THE TIMEZONE PROBLEM — AND THE BUG IT CAUSED

   Tutor availability is stored in the TUTOR's local time.
   Sushila teaches at 20:00 IST. A student in London must be
   shown 15:30, not 20:00.

   The tutor's zone is stored as a display string:

       timezone: "IST (Asia/Kolkata)"

   That is written for humans, not for Date(). So the offset
   is parsed out of the "(GMT+5:30)" part. If it cannot be
   parsed we fall back to IST, because every current tutor is
   in India — and, critically, we then LABEL the times as the
   tutor's, rather than silently showing a wrong conversion.
   A wrong time confidently displayed is the worst outcome.
   ========================================================= */

(function (root) {
  "use strict";

  var DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var DAY_LONG = ["Sunday", "Monday", "Tuesday", "Wednesday",
                  "Thursday", "Friday", "Saturday"];
  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  /* How many days ahead to show. Two weeks is enough to find a
     slot and short enough that the list stays scannable. */
  var HORIZON = 14;

  /* Do not offer a slot that is less than this far away — a
     tutor cannot realistically answer a request for a lesson
     starting in ten minutes. */
  var MIN_NOTICE_HOURS = 3;

  /* ---------------------------------------------------------
     Parse "IST (Asia/Kolkata)" or "IST (GMT+5:30)" → 330 min.
     Also accepts "GMT-3", "UTC+05:30", "(GMT+0)".
     Returns null when it genuinely cannot tell, so the caller
     can fall back loudly rather than guess.

     v98 — the tutor timezone label is now "IST (Asia/Kolkata)"
     (the command's required display form). IANA names have no
     +/- inside them, so they are matched by name first; the GMT
     parser remains for any hand-written string.
     --------------------------------------------------------- */
  var IANA_OFFSET = {
    "Asia/Kolkata": 330, "Asia/Calcutta": 330,
    "Asia/Kathmandu": 345, "Asia/Dubai": 240,
    "Europe/London": 0, "America/New_York": -300,
    "America/Chicago": -360, "America/Denver": -420,
    "America/Los_Angeles": -480, "Australia/Sydney": 600
  };
  function offsetMinutes(tzString) {
    var s = String(tzString || "");
    var m = /([A-Za-z_]+\/[A-Za-z_]+)/.exec(s);
    if (m && IANA_OFFSET[m[1]] !== undefined) return IANA_OFFSET[m[1]];
    m = /(?:GMT|UTC)\s*([+-])\s*(\d{1,2})(?::?(\d{2}))?/i.exec(s);
    if (!m) return null;
    var sign = m[1] === "-" ? -1 : 1;
    var h = parseInt(m[2], 10) || 0;
    var mi = parseInt(m[3] || "0", 10) || 0;
    return sign * (h * 60 + mi);
  }

  /* The visitor's own offset, in the same units. getTimezoneOffset
     is inverted by definition — it returns minutes to ADD to local
     time to get UTC — so it is negated here once, on purpose. */
  function localOffsetMinutes(d) {
    return -(d || new Date()).getTimezoneOffset();
  }

  function visitorZoneName() {
    try {
      var z = Intl.DateTimeFormat().resolvedOptions().timeZone;
      if (z) return z;
    } catch (e) {}
    var off = localOffsetMinutes();
    var sign = off < 0 ? "-" : "+";
    off = Math.abs(off);
    return "GMT" + sign + Math.floor(off / 60) +
      (off % 60 ? ":" + String(off % 60).padStart(2, "0") : "");
  }

  function pad(n) { return n < 10 ? "0" + n : String(n); }

  /* ---------------------------------------------------------
     Build the real slot list.

     For each of the next HORIZON days we look up what the tutor
     teaches on that weekday IN THEIR OWN ZONE, then convert each
     slot to a real Date so it can be re-rendered in the
     visitor's zone. Converting per-slot rather than per-day
     matters: a 20:00 IST slot on Monday is Monday 06:30 in
     Los Angeles but a 23:00 IST slot is TUESDAY there, and a
     per-day conversion would put it on the wrong row.
     --------------------------------------------------------- */
  function slotsFor(tutor, opts) {
    opts = opts || {};
    var avail = (tutor && tutor.availability) || {};
    var tutorOff = offsetMinutes(tutor && tutor.timezone);
    var known = tutorOff !== null;
    if (!known) tutorOff = 330;          /* IST — every current tutor */

    var now = new Date();
    var earliest = now.getTime() + MIN_NOTICE_HOURS * 3600 * 1000;
    var out = [];

    /* Walk days in the TUTOR's calendar, not the visitor's, so we
       never miss or duplicate one either side of midnight. */
    for (var d = 0; d <= HORIZON; d++) {
      /* Midnight of this day, in the tutor's zone, as real UTC. */
      var base = new Date(now.getTime() + d * 86400000);
      var tutorMidnightUTC = Date.UTC(
        base.getUTCFullYear(), base.getUTCMonth(), base.getUTCDate()
      ) - tutorOff * 60000;

      var probe = new Date(tutorMidnightUTC + tutorOff * 60000);
      var dayName = DAYS[probe.getUTCDay()];
      var times = avail[dayName] || [];

      for (var i = 0; i < times.length; i++) {
        /* BUG FOUND v53 — "25:99" WAS ACCEPTED.

           The shape check /^\d{1,2}:\d{2}$/ only proves the entry
           LOOKS like a time. "25:99" passes it, and the arithmetic
           below then silently rolls it into the next day at 02:39 —
           a slot the tutor never offered, on a day they may not
           teach, presented to the student as real.

           A typo in a tutor file must never invent availability, so
           the numbers are range-checked too. Anything out of range
           is skipped exactly like unreadable text. */
        var hm = /^(\d{1,2}):(\d{2})$/.exec(String(times[i]).trim());
        if (!hm) continue;               /* unreadable entry, skip quietly */
        var hh = parseInt(hm[1], 10), mm = parseInt(hm[2], 10);
        if (!(hh >= 0 && hh <= 23 && mm >= 0 && mm <= 59)) continue;
        var when = new Date(tutorMidnightUTC + (hh * 60 + mm) * 60000);

        if (when.getTime() < earliest) continue;
        if (out.length >= 200) break;    /* sanity cap */

        out.push({
          date: when,
          tutorTime: (hh < 10 ? "0" + hh : String(hh)) + ":" +
                     (mm < 10 ? "0" + mm : String(mm)),
          zoneKnown: known
        });
      }
    }

    out.sort(function (a, b) { return a.date - b.date; });
    return { slots: out, zoneKnown: known, tutorOffset: tutorOff };
  }

  /* Group into days using the VISITOR's local calendar, because
     that is the calendar they are reading. When the visitor has
     SELECTED a timezone (offMin is a number), group using that
     zone's calendar instead of the browser's. */
  function inZone(d, offMin) {
    return typeof offMin === "number" ? new Date(d.getTime() + offMin * 60000) : null;
  }
  function groupByLocalDay(slots, offMin) {
    var map = {}, order = [];
    slots.forEach(function (s) {
      var z = inZone(s.date, offMin);
      var key = z
        ? z.getUTCFullYear() + "-" + pad(z.getUTCMonth() + 1) + "-" + pad(z.getUTCDate())
        : s.date.getFullYear() + "-" + pad(s.date.getMonth() + 1) + "-" + pad(s.date.getDate());
      if (!map[key]) { map[key] = { key: key, date: s.date, slots: [] }; order.push(key); }
      map[key].slots.push(s);
    });

    /* BUG FOUND v53 — SLOTS OUT OF ORDER ACROSS THE DATE LINE.

       slotsFor() sorts globally by absolute time, which is correct.
       But grouping by the VISITOR's calendar day reshuffles them:
       viewed from Los Angeles, a 16:00 IST slot lands at 03:30 the
       next local morning while a 10:00 IST slot from the FOLLOWING
       tutor-day lands at 21:30 that same local evening. Both fall in
       one local day, and they arrived in tutor order, so the column
       read 03:30, 05:30, 07:30, 21:30, 23:30 — plausible — but with
       other offsets it read 21:30 before 03:30, which looks broken.

       Sorting inside each day, after grouping, is the only place
       this can be fixed: before grouping we do not yet know which
       local day a slot belongs to.

       The day ORDER also has to be sorted, for the same reason. */
    order.sort();
    order.forEach(function (k) {
      map[k].slots.sort(function (a, b) { return a.date - b.date; });
      map[k].date = map[k].slots[0].date;
    });
    return order.map(function (k) { return map[k]; });
  }

  function dayLabel(d, offMin) {
    var z = inZone(new Date(), offMin);
    var t0 = z
      ? new Date(Date.UTC(z.getUTCFullYear(), z.getUTCMonth(), z.getUTCDate()))
      : new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
    var zd = inZone(d, offMin);
    var d0 = zd
      ? new Date(Date.UTC(zd.getUTCFullYear(), zd.getUTCMonth(), zd.getUTCDate()))
      : new Date(d.getFullYear(), d.getMonth(), d.getDate());
    var diff = Math.round((d0 - t0) / 86400000);
    if (diff === 0) return "Today";
    if (diff === 1) return "Tomorrow";
    return DAY_LONG[(zd ? zd.getUTCDay() : d.getDay())] + " " + (zd ? zd.getUTCDate() : d.getDate()) + " " + MON[(zd ? zd.getUTCMonth() : d.getMonth())];
  }

  function timeLabel(d, offMin) {
    if (typeof offMin === "number") {
      var u = new Date(d.getTime() + offMin * 60000);
      return pad(u.getUTCHours()) + ":" + pad(u.getUTCMinutes());
    }
    return pad(d.getHours()) + ":" + pad(d.getMinutes());
  }

  /* ---------------------------------------------------------
     .ics — so the lesson goes into their real calendar.

     Written by hand because the format is tiny and a library
     would be a third-party dependency for forty lines of text.
     CRLF line endings are REQUIRED by RFC 5545; Outlook rejects
     the file outright with plain \n, which is the classic way
     hand-rolled .ics files fail.
     --------------------------------------------------------- */
  function icsFor(tutor, slotDate, minutes) {
    minutes = minutes || 50;
    function z(d) {
      return d.getUTCFullYear() + pad(d.getUTCMonth() + 1) + pad(d.getUTCDate()) +
        "T" + pad(d.getUTCHours()) + pad(d.getUTCMinutes()) + "00Z";
    }
    var end = new Date(slotDate.getTime() + minutes * 60000);
    var site = (root.EKGURU_SITE || {});
    var name = (tutor && tutor.name) || "your tutor";
    /* Escape per RFC 5545: comma, semicolon and backslash are
       delimiters inside a property value. */
    function esc(s) {
      return String(s || "").replace(/\\/g, "\\\\")
        .replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n");
    }
    var lines = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//EkGuru//Hindi lessons//EN",
      "CALSCALE:GREGORIAN",
      "METHOD:PUBLISH",
      "BEGIN:VEVENT",
      "UID:" + z(slotDate) + "-" + (tutor && tutor.id || "lesson") + "@ekguru",
      "DTSTAMP:" + z(new Date()),
      "DTSTART:" + z(slotDate),
      "DTEND:" + z(end),
      "SUMMARY:" + esc("Hindi lesson with " + name),
      "DESCRIPTION:" + esc("A " + minutes + " minute one-to-one Hindi lesson booked through " +
        (site.brand || "EkGuru") + ". Your tutor will confirm by email."),
      "LOCATION:" + esc("Online"),
      "STATUS:TENTATIVE",
      "END:VEVENT",
      "END:VCALENDAR"
    ];
    return lines.join("\r\n");
  }

  function downloadIcs(tutor, slotDate, minutes) {
    var text = icsFor(tutor, slotDate, minutes);
    try {
      var blob = new Blob([text], { type: "text/calendar;charset=utf-8" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "hindi-lesson-" + ((tutor && tutor.id) || "ekguru") + ".ics";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      return true;
    } catch (e) {
      /* Older browsers, or a blocked blob URL. A data URI still
         works almost everywhere and is better than nothing. */
      try {
        window.open("data:text/calendar;charset=utf-8," + encodeURIComponent(text));
        return true;
      } catch (e2) { return false; }
    }
  }

  /* ---------------------------------------------------------
     Render into a container. Returns the number of slots shown
     so the caller can decide whether to display anything at all.
     --------------------------------------------------------- */
  function render(el, tutor, onPick, offMin, zoneLabel) {
    if (!el) return 0;
    var res = slotsFor(tutor);
    var days = groupByLocalDay(res.slots, offMin);

    if (!days.length) {
      el.innerHTML = '<p class="sched-none">' +
        (tutor && tutor.name ? tutor.name.split(" ")[0] : "This tutor") +
        ' has no set hours listed. Send a request with the time that suits you and ' +
        'they will reply.</p>';
      return 0;
    }

    var zone = zoneLabel || visitorZoneName();
    var html = '<p class="sched-zone">Times shown in <b>' + zone + '</b>' +
      (res.zoneKnown ? "" : " — the tutor's own timezone could not be read, so these may be off") +
      '.</p><div class="sched-days">';

    days.slice(0, 10).forEach(function (d) {
      html += '<div class="sched-day"><h4>' + dayLabel(d.date, offMin) + "</h4><div class='sched-slots'>";
      d.slots.forEach(function (s) {
        html += '<button type="button" class="sched-slot" data-iso="' +
          s.date.toISOString() + '">' + timeLabel(s.date, offMin) + "</button>";
      });
      html += "</div></div>";
    });
    html += "</div>";

    /* The honest caveat. Without a server we cannot know what is
       already booked, and saying so prevents the double-booking
       complaint that would otherwise be inevitable. */
    html += '<p class="sched-note">These are the hours ' +
      ((tutor && tutor.name) ? tutor.name.split(" ")[0] : "this tutor") +
      ' normally teaches. Your request confirms the exact time by email.</p>';

    el.innerHTML = html;

    el.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest(".sched-slot");
      if (!b) return;
      [].forEach.call(el.querySelectorAll(".sched-slot"), function (x) {
        x.classList.remove("on");
      });
      b.classList.add("on");
      var iso = b.getAttribute("data-iso");
      if (typeof onPick === "function") onPick(new Date(iso), b.textContent);
      /* Deliberately NOT firing an analytics event here. The caller
         in features.js logs slot_picked through track(), which
         reaches both the local ledger and analytics. Firing it in
         both places counted every choice twice. */
    });

    return res.slots.length;
  }

  var API = {
    slotsFor: slotsFor,
    groupByLocalDay: groupByLocalDay,
    render: render,
    icsFor: icsFor,
    downloadIcs: downloadIcs,
    offsetMinutes: offsetMinutes,
    visitorZoneName: visitorZoneName,
    HORIZON: HORIZON,
    MIN_NOTICE_HOURS: MIN_NOTICE_HOURS
  };

  if (typeof module !== "undefined" && module.exports) module.exports = API;
  root.EkGuruSchedule = API;

})(typeof window !== "undefined" ? window : globalThis);
