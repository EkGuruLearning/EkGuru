/* =========================================================
   EkGuru — MY HINDI PROGRESS  (v1)
   ---------------------------------------------------------
   Local, honest learning progress stored ONLY in this browser
   under ekguru:hindi:v1:progress. Nothing here implies an
   account, a server, cross-device sync, or certification.

   Tracks (all real, local metrics):
     · lessons opened
     · lessons marked complete (reversible)
     · quiz attempts + best score (from the topic quiz)
     · review deck size / due (read from EkGuruSRS)

   Never stores passwords, tokens or booking data.

   Mounts a reversible "Mark lesson complete" toggle on any page
   that carries data-lesson-slug, and (optionally) paints a
   #my-hindi host if present.

   Window API: window.EkGuruProgress
   ========================================================= */
(function () {
  "use strict";

  var KEY = "ekguru:hindi:v1:progress";
  var VERSION = 1;

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return { version: VERSION, opened: [], completed: {}, quizzes: {} };
      var o = JSON.parse(raw);
      if (o && o.version === VERSION) {
        o.opened = o.opened || []; o.completed = o.completed || {}; o.quizzes = o.quizzes || {};
        return o;
      }
      return { version: VERSION, opened: [], completed: {}, quizzes: {} };
    } catch (e) { return { version: VERSION, opened: [], completed: {}, quizzes: {} }; }
  }
  function write(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  var P = {
    version: VERSION,

    slug: function () {
      var el = document.querySelector("[data-lesson-slug]");
      return el ? el.getAttribute("data-lesson-slug") : null;
    },
    title: function () {
      var h = document.querySelector("h1");
      return h ? h.textContent.trim() : (document.title || "").split("|")[0].trim();
    },

    /* called on every lesson page load (auto-mounted) */
    recordOpen: function () {
      var s = this.slug();
      if (!s) return;
      var o = read();
      var t = this.title();
      o.opened = o.opened.filter(function (x) { return x.slug !== s; });
      o.opened.unshift({ slug: s, title: t, at: Date.now() });
      if (o.opened.length > 60) o.opened.length = 60;
      write(o);
    },

    completed: function () { return read().completed; },
    isComplete: function (s) { return !!read().completed[s || this.slug()]; },

    markComplete: function (s, on) {
      var slug = s || this.slug();
      if (!slug) return false;
      var o = read();
      if (on) o.completed[slug] = { title: this.title(), at: Date.now() };
      else delete o.completed[slug];
      write(o);
      return true;
    },

    recordQuiz: function (quizId, correct, total) {
      var o = read();
      var q = o.quizzes[quizId] || { attempts: 0, best: 0, last: 0 };
      q.attempts += 1;
      q.last = correct;
      q.best = Math.max(q.best || 0, correct);
      o.quizzes[quizId] = { attempts: q.attempts, best: q.best, last: q.last,
                            total: total, at: Date.now() };
      write(o);
      return q;
    },

    snapshot: function () {
      var o = read();
      var srs = window.EkGuruSRS || null;
      return {
        version: VERSION,
        lessonsOpened: o.opened.length,
        lessonsCompleted: Object.keys(o.completed).length,
        opened: o.opened.slice(0, 12),
        completed: o.completed,
        quizzes: o.quizzes,
        reviewCards: srs ? srs.count() : 0,
        reviewDue: srs ? srs.dueCount() : 0,
        pathsStarted: (function () {
          try {
            var m = JSON.parse(localStorage.getItem("ekguru_path_progress_v1") || "{}");
            return Object.keys(m).length;
          } catch (e) { return 0; }
        })()
      };
    },

    reset: function () {
      try { localStorage.removeItem(KEY); return true; } catch (e) { return false; }
    },
    exportJSON: function () {
      var o = read();
      o.exported_at = new Date().toISOString();
      o.kind = "ekguru-hindi-progress";
      return JSON.stringify(o, null, 2);
    },
    importJSON: function (text) {
      var incoming;
      try { incoming = JSON.parse(text); } catch (e) { return { ok: false, error: "Not valid JSON." }; }
      if (!incoming || incoming.kind !== "ekguru-hindi-progress" || incoming.version !== VERSION) {
        return { ok: false, error: "Not an EkGuru Hindi progress export (wrong kind or version)." };
      }
      var clean = { version: VERSION,
                    opened: Array.isArray(incoming.opened) ? incoming.opened.slice(0, 60) : [],
                    completed: incoming.completed && typeof incoming.completed === "object" ? incoming.completed : {},
                    quizzes: incoming.quizzes && typeof incoming.quizzes === "object" ? incoming.quizzes : {} };
      write(clean);
      return { ok: true, imported: Object.keys(clean.completed).length };
    },

    /* ---- Mark-complete toggle ---- */
    mountComplete: function () {
      var s = this.slug();
      var host = document.getElementById("lesson-complete");
      if (!s || !host) return;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn";
      var label = function () {
        var done = P.isComplete(s);
        btn.textContent = done ? "✓ Lesson complete — undo" : "Mark lesson complete";
        btn.setAttribute("aria-pressed", done ? "true" : "false");
      };
      label();
      btn.addEventListener("click", function () {
        P.markComplete(s, !P.isComplete(s));
        label();
      });
      var note = document.createElement("p");
      note.className = "muted";
      note.style.cssText = "font-size:.78rem;margin:6px 0 0";
      note.textContent = "Saved on this device only. Not a certificate — just your own checklist.";
      host.appendChild(btn);
      host.appendChild(note);
    }
  };

  window.EkGuruProgress = P;

  function boot() {
    P.recordOpen();
    P.mountComplete();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
