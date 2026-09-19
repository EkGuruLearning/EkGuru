/* =========================================================
   EkGuru — ONE LEDGER FOR EVERY MESSAGE THE SITE SENDS
   ---------------------------------------------------------
   Prakash: "admin mein saare reference number … record aana
   chahiye … jisko bheje uske paas jana chahiye mail."

   ═══════════════════════════════════════════════════════
   THE GAP THIS CLOSES
   ═══════════════════════════════════════════════════════

   Bookings were written to js/store.js and are searchable in the
   dashboard by name, email, tutor or reference.

   Contact-form messages were not written anywhere at all.

   A visitor filling in the contact form gets a reference —
   C-4K2P9X — printed on screen and quoted in both emails. Then
   they write back three days later saying "any news on C-4K2P9X?"
   and the dashboard has never heard of it. The reference was
   real, it was just never recorded.

   Same for admin replies and bulk sends: they went out and left
   no trace, so there was no way to answer "did we ever reply to
   this person?"

   This is the single ledger. Every message with a reference lands
   here, whatever kind it is, and the dashboard can look any of
   them up.

   ═══════════════════════════════════════════════════════
   WHAT THIS IS NOT
   ═══════════════════════════════════════════════════════

   ⚠️ IT IS PER-BROWSER. localStorage is the only storage a
   static site has. A booking made on a visitor's phone is
   written to THEIR browser, not to yours — you will never see it
   here. What you see is what happened in THIS browser.

   That is a real limitation and the dashboard says so plainly
   rather than presenting this as a complete record. The complete
   record is the email in EkGuruLearning@gmail.com: every booking
   sends a [record] copy and every contact sends its own, and
   those are the ones that survive a cleared cache.

   This ledger exists so that a reference can be LOOKED UP
   quickly, not so it can replace the inbox.

   ⚠️ NO PERSONAL DATA LEAVES THE DEVICE. Nothing here is
   uploaded anywhere. tools/privacy.js checks that.
   ========================================================= */

(function () {
  "use strict";

  var KEY = "ekguru_ledger_v1";
  var CAP = 500;           /* keep the newest 500; localStorage is ~5 MB */

  /* Every kind of message the site can send. The `ref` prefix is
     what tells them apart at a glance in the dashboard and in an
     inbox search. */
  var KINDS = {
    booking: { label: "Booking request", prefix: "EK-" },
    contact: { label: "Contact message", prefix: "C-" },
    reply:   { label: "Admin reply",     prefix: "R-" },
    bulk:    { label: "Bulk message",    prefix: "B-" },
    report:  { label: "Report",          prefix: "!-" }
  };

  function readAll() {
    try {
      var raw = localStorage.getItem(KEY);
      var v = raw ? JSON.parse(raw) : [];
      return Object.prototype.toString.call(v) === "[object Array]" ? v : [];
    } catch (e) { return []; }
  }

  function writeAll(list) {
    try {
      /* Trim oldest first. A quota error here must never break a
         send — the message has already gone out; this is only the
         note about it. */
      if (list.length > CAP) list = list.slice(list.length - CAP);
      localStorage.setItem(KEY, JSON.stringify(list));
      return true;
    } catch (e) {
      /* Storage full or blocked (private mode). Drop half and try
         once; if that fails too, give up silently. */
      try {
        localStorage.setItem(KEY, JSON.stringify(list.slice(Math.floor(list.length / 2))));
        return true;
      } catch (e2) { return false; }
    }
  }

  /* A reference a human can read out over the phone. Deliberately
     avoids 0/O and 1/I — this gets dictated, and those get heard
     wrong. Matches the shape js/store.js already uses. */
  var ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  function makeRef(kind) {
    var p = (KINDS[kind] || {}).prefix || "X-";
    var s = "";
    try {
      var a = new Uint32Array(6);
      (window.crypto || window.msCrypto).getRandomValues(a);
      for (var i = 0; i < 6; i++) s += ALPHABET[a[i] % ALPHABET.length];
    } catch (e) {
      for (var j = 0; j < 6; j++) {
        s += ALPHABET[Math.floor(Math.random() * ALPHABET.length)];
      }
    }
    return p + s;
  }

  var Ledger = {

    KINDS: KINDS,
    makeRef: makeRef,

    /* Record one message.

       add({ kind, ref, to, name, email, subject, summary,
             tutor, tutorId, via, ok, error, recipients })

       `recipients` is the list of everyone this one action mailed
       — a booking is three people — so the dashboard can answer
       "who actually received something?" without guessing. */
    add: function (m) {
      m = m || {};
      var kind = KINDS[m.kind] ? m.kind : "contact";
      var rec = {
        ref: m.ref || makeRef(kind),
        kind: kind,
        at: new Date().toISOString(),
        name: m.name || "",
        email: m.email || "",
        subject: m.subject || "",
        /* A short human line, not the whole message. The full text
           is in the email; this is an index, not an archive. */
        summary: String(m.summary || m.message || "").slice(0, 240),
        tutor: m.tutor || "",
        tutorId: m.tutorId || "",
        topic: m.topic || "",
        /* Who it went to, and by which relay — this is what makes
           "did the student actually get their copy?" answerable. */
        recipients: (m.recipients || []).map(function (r) {
          return {
            role: r.role || "",         /* tutor | student | ekguru | sender */
            to: r.to || "",
            via: r.via || "",           /* Web3Forms | FormSubmit | … */
            ok: r.ok !== false,
            error: r.error || ""
          };
        }),
        ok: m.ok !== false,
        error: m.error || "",
        /* v100 — a message can be recorded BEFORE it is sent
           (status "sending") and filled in afterwards, so a crash
           mid-send still leaves a durable trace. */
        status: m.status || (m.ok !== false ? "sent" : "failed"),
        /* v97 — the honest per-role delivery state (ACCEPTED, FAILED,
           TUTOR_EMAIL_UNAVAILABLE, …) copied from the mailer result,
           so the record room can answer "was the tutor notified?" */
        tutorEmailStatus: m.tutorEmailStatus || "",
        emailStates: m.emailStates || {},
        page: m.page || (typeof location !== "undefined" ? location.href : ""),
        lang: (typeof document !== "undefined" &&
               document.documentElement.getAttribute("lang")) || "en"
      };
      var all = readAll();
      all.push(rec);
      writeAll(all);
      return rec;
    },

    /* v100 — fill in a record by reference (upsert semantics for
       fields that arrive later, e.g. the send outcome). Returns the
       patched record, or null when there is nothing to patch. */
    update: function (ref, patch) {
      if (!ref) return null;
      var all = readAll(), hit = null;
      all.forEach(function (r) {
        if (String(r.ref) === String(ref)) {
          for (var k in patch) r[k] = patch[k];
          hit = r;
        }
      });
      if (hit) writeAll(all);
      return hit;
    },

    /* Newest first — that is the order anybody wants to read it. */
    all: function () { return readAll().slice().reverse(); },

    of: function (kind) {
      return readAll().filter(function (r) { return r.kind === kind; }).reverse();
    },

    /* THE LOOKUP THIS FILE EXISTS FOR.
       Case- and whitespace-insensitive, and it also matches a bare
       code without its prefix — somebody reading a reference off a
       screen will not always include the "C-". */
    find: function (ref) {
      if (!ref) return null;
      var q = String(ref).trim().toUpperCase().replace(/\s+/g, "");
      var bare = q.replace(/^[A-Z!]+-/, "");
      var all = readAll();
      for (var i = all.length - 1; i >= 0; i--) {
        var r = String(all[i].ref || "").toUpperCase();
        if (r === q || r.replace(/^[A-Z!]+-/, "") === bare) return all[i];
      }
      return null;
    },

    /* Free-text search across everything a person might remember:
       the reference, a name, an address, a tutor, the subject. */
    search: function (q) {
      if (!q) return this.all();
      var s = String(q).trim().toLowerCase();
      return readAll().filter(function (r) {
        return [r.ref, r.name, r.email, r.tutor, r.subject, r.topic, r.summary]
          .join(" ").toLowerCase().indexOf(s) > -1;
      }).reverse();
    },

    /* Anything that did not fully succeed — the list worth acting
       on. A booking where the student's copy failed is still a
       booking, and it needs a human to send that copy by hand. */
    problems: function () {
      return readAll().filter(function (r) {
        return !r.ok || (r.recipients || []).some(function (x) { return !x.ok; });
      }).reverse();
    },

    counts: function () {
      var out = { total: 0, failed: 0 };
      Object.keys(KINDS).forEach(function (k) { out[k] = 0; });
      readAll().forEach(function (r) {
        out.total++;
        if (out[r.kind] != null) out[r.kind]++;
        if (!r.ok) out.failed++;
      });
      return out;
    },

    /* For the dashboard's export button. CSV rather than JSON
       because it opens in a spreadsheet, which is where this
       actually gets used. */
    csv: function () {
      var q = function (v) {
        return '"' + String(v == null ? "" : v).replace(/"/g, '""') + '"';
      };
      var rows = [["reference", "kind", "when", "name", "email", "tutor",
                   "subject", "recipients", "delivered", "ok", "error"].join(",")];
      readAll().slice().reverse().forEach(function (r) {
        rows.push([
          r.ref, (KINDS[r.kind] || {}).label || r.kind, r.at, r.name, r.email,
          r.tutor, r.subject,
          (r.recipients || []).map(function (x) { return x.role + ":" + x.to; }).join(" | "),
          (r.recipients || []).filter(function (x) { return x.ok; }).length +
            "/" + (r.recipients || []).length,
          r.ok ? "yes" : "no", r.error
        ].map(q).join(","));
      });
      return rows.join("\n");
    },

    clear: function () {
      try { localStorage.removeItem(KEY); return true; } catch (e) { return false; }
    }
  };

  window.EkGuruLedger = Ledger;
})();
