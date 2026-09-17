/* =========================================================
   EkGuru — ADMIN GATE
   ---------------------------------------------------------
   READ THIS FIRST — WHAT THIS CAN AND CANNOT DO

   EkGuru has no server. Every file in the repository is public
   the moment it is pushed, and anyone can read the source.
   That is a fact of GitHub Pages, not something code can undo.

   So this gate is HONEST about what it is:

     ✅ It stops a curious visitor, a search engine, or someone
        who guessed /admin.html from seeing the dashboard.
     ✅ It stops shoulder-surfing and casual snooping.
     ✅ The passcode is never stored in the repo — only a hash
        of it is, so reading the source does not reveal it.

     ❌ It is NOT real security. A determined person who reads
        the source can see the hash and could brute-force a
        weak passcode offline. Use a long one.
     ❌ It cannot protect data that is already public. Tutor
        emails are in js/tutors/*.js because the site needs
        them to send bookings — the gate does not hide those.

   WHAT IS ACTUALLY BEHIND THE GATE
   Student booking records live in YOUR browser's local storage.
   They are not on GitHub and not in the repo. Nobody opening
   admin.html on their own machine can see them — I tested this,
   a second browser shows zero bookings. The gate exists so that
   the dashboard, your business email and the API-key controls
   are not simply on display.

   ---------------------------------------------------------
   HOW TO SET YOUR PASSCODE

   1. Open admin.html. With no passcode set, it will offer to
      create one. Type a long phrase you will remember.
   2. It prints a line like:
          PASSCODE_HASH: "a1b2c3…"
   3. Paste that value into js/site-config.js under
          admin: { passcodeHash: "…" }
   4. Push. From then on the dashboard asks for the phrase.

   To change it, clear the field in site-config.js and repeat.
   ========================================================= */

(function () {
  "use strict";

  var S = window.EKGURU_SITE || {};
  var CFG = S.admin || {};
  var SESSION_KEY = "ekguru_admin_ok";
  var ATTEMPT_KEY = "ekguru_admin_tries";
  var MAX_TRIES = 5;
  var LOCKOUT_MS = 10 * 60 * 1000;      // ten minutes after 5 wrong tries

  /* SHA-256 via the browser's own crypto. Salted with a fixed
     string so a stolen hash cannot be looked up in a rainbow
     table of common passwords. */
  var SALT = "EkGuru/admin/v1/";

  function sha256(text) {
    if (!window.crypto || !window.crypto.subtle) {
      return Promise.reject(new Error("This browser cannot hash securely. Use a modern browser over https."));
    }
    var data = new TextEncoder().encode(SALT + text);
    return window.crypto.subtle.digest("SHA-256", data).then(function (buf) {
      return Array.prototype.map.call(new Uint8Array(buf), function (b) {
        return ("00" + b.toString(16)).slice(-2);
      }).join("");
    });
  }

  function tries() {
    try {
      var r = JSON.parse(localStorage.getItem(ATTEMPT_KEY) || "{}");
      if (r.until && Date.now() > r.until) return { n: 0 };
      return r;
    } catch (e) { return { n: 0 }; }
  }
  function bumpTries() {
    var r = tries();
    r.n = (r.n || 0) + 1;
    if (r.n >= MAX_TRIES) r.until = Date.now() + LOCKOUT_MS;
    try { localStorage.setItem(ATTEMPT_KEY, JSON.stringify(r)); } catch (e) {}
    return r;
  }
  function clearTries() {
    try { localStorage.removeItem(ATTEMPT_KEY); } catch (e) {}
  }

  /* The unlock lasts for the tab only, so closing it re-locks. */
  function unlocked() {
    try { return sessionStorage.getItem(SESSION_KEY) === "1"; } catch (e) { return false; }
  }
  function markUnlocked() {
    try { sessionStorage.setItem(SESSION_KEY, "1"); } catch (e) {}
  }

  function screen(inner) {
    var el = document.createElement("div");
    el.id = "ekg-gate";
    el.innerHTML =
      '<div class="gate-box">' +
        '<div class="gate-logo" aria-hidden="true">🔒</div>' + inner +
      "</div>";
    return el;
  }

  var CSS =
    "#ekg-gate{position:fixed;inset:0;z-index:99999;background:#0f1222;color:#fff;" +
      "display:flex;align-items:center;justify-content:center;padding:24px;" +
      "font:16px/1.6 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}" +
    ".gate-box{max-width:440px;width:100%;text-align:center}" +
    ".gate-logo{font-size:2.6rem;margin-bottom:14px}" +
    ".gate-box h1{font-size:1.35rem;margin:0 0 8px}" +
    ".gate-box p{color:#c2c6da;font-size:.93rem;margin:0 0 18px}" +
    ".gate-box input{width:100%;font:inherit;padding:12px 14px;border-radius:10px;" +
      "border:1px solid #2a2f4a;background:#171a2e;color:#fff;margin-bottom:10px}" +
    ".gate-box button{width:100%;font:inherit;font-weight:700;padding:12px;border:0;" +
      "border-radius:10px;background:#e0682a;color:#fff;cursor:pointer}" +
    ".gate-box button:disabled{opacity:.5;cursor:default}" +
    ".gate-err{color:#fca5a5;font-size:.88rem;margin-top:12px;min-height:1.2em}" +
    ".gate-hash{margin-top:16px;padding:12px;border-radius:10px;background:#171a2e;" +
      "border:1px solid #2a2f4a;font-family:ui-monospace,Menlo,monospace;" +
      "font-size:.76rem;word-break:break-all;text-align:left;color:#93c5fd}" +
    ".gate-note{font-size:.8rem;color:#8b90a8;margin-top:14px;line-height:1.5}" +
    ".gate-link{background:none;border:0;color:#93c5fd;text-decoration:underline;" +
      "cursor:pointer;font:inherit;padding:4px 0;width:auto}";

  function injectCss() {
    var st = document.createElement("style");
    st.textContent = CSS;
    document.head.appendChild(st);
  }

  /* The gate now runs from <head>, so document.body does not exist
     yet. Attaching the screen must wait for it. Previously this file
     called document.body.appendChild directly, which is why moving
     the gate earlier was not enough on its own. */
  function attach(el, onReady) {
    function go() {
      document.body.appendChild(el);
      if (onReady) onReady();
    }
    if (document.body) go();
    else document.addEventListener("DOMContentLoaded", go);
  }

  /* ---------------------------------------------------------
     No passcode configured yet -> help them create one.
     --------------------------------------------------------- */
  function setupScreen() {
    var g = screen(
      "<h1>Set an admin passcode</h1>" +
      "<p>No passcode is configured, so this dashboard is currently open to anyone with the link. " +
      "Choose a long phrase, then paste the generated line into <b>js/site-config.js</b>.</p>" +
      '<input type="password" id="gate-new" placeholder="a long phrase you will remember" autocomplete="new-password">' +
      '<button id="gate-make" type="button">Generate the hash</button>' +
      '<div class="gate-err" id="gate-err"></div>' +
      '<div class="gate-hash" id="gate-out" hidden></div>' +
      '<p class="gate-note">The phrase itself is never saved anywhere. Only this hash goes into the repo, ' +
      "so reading the source does not reveal your passcode. It is a lock on the door, not a vault — " +
      "use something long.</p>"
    );
    var inp, err, out;
    attach(g, function () {
      inp = g.querySelector("#gate-new");
      err = g.querySelector("#gate-err");
      out = g.querySelector("#gate-out");
      g.querySelector("#gate-make").addEventListener("click", make);
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") make(); });
      inp.focus();
    });

    function make() {
      var v = inp.value;
      if (v.length < 8) { err.textContent = "Please use at least 8 characters — longer is better."; return; }
      err.textContent = "";
      sha256(v).then(function (h) {
        out.hidden = false;
        out.textContent = 'admin: { passcodeHash: "' + h + '" }';
        err.textContent = "Copy that line into js/site-config.js, then reload.";
      }).catch(function (e) { err.textContent = e.message; });
    }
  }

  /* ---------------------------------------------------------
     Passcode configured -> ask for it.
     --------------------------------------------------------- */
  function lockScreen(hash) {
    var t = tries();
    var locked = t.until && Date.now() < t.until;
    var mins = locked ? Math.ceil((t.until - Date.now()) / 60000) : 0;

    var g = screen(
      "<h1>EkGuru admin</h1>" +
      "<p>This dashboard is private. Enter the passcode to continue.</p>" +
      '<input type="password" id="gate-pw" placeholder="passcode" autocomplete="current-password"' +
        (locked ? " disabled" : "") + ">" +
      '<button id="gate-go" type="button"' + (locked ? " disabled" : "") + ">Unlock</button>" +
      '<div class="gate-err" id="gate-err">' +
        (locked ? "Too many attempts. Try again in " + mins + " minute" + (mins === 1 ? "" : "s") +
                  "." : "") + "</div>" +
      (locked
        ? '<p class="gate-note">Locked yourself out? You own this site — clear the lockout below.' +
          '<br><button type="button" id="gate-reset" class="gate-link">Reset the attempt counter</button></p>'
        : "") +
      '<p class="gate-note">Booking records are stored in the browser you are using now — ' +
      'this laptop, this browser profile. The archive tab pulls the complete list from the ' +
      'server, from every device.</p>'
    );
    var inp, err, btn;
    attach(g, function () {
      inp = g.querySelector("#gate-pw");
      err = g.querySelector("#gate-err");
      btn = g.querySelector("#gate-go");
      btn.addEventListener("click", attempt);
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") attempt(); });
      if (!locked) inp.focus();

      /* An owner locked out of their own dashboard is an annoyance,
         not a security feature — anyone who can press this could
         equally clear the browser's storage by hand. It exists so
         you are not left waiting ten minutes on your own site. */
      var reset = g.querySelector("#gate-reset");
      if (reset) reset.addEventListener("click", function () {
        clearTries();
        location.reload();
      });

      /* When the lockout expires, unlock the form without a reload. */
      if (locked) {
        var iv = setInterval(function () {
          var t2 = tries();
          if (!t2.until || Date.now() >= t2.until) {
            clearInterval(iv);
            inp.disabled = false; btn.disabled = false;
            err.textContent = "";
            var note = g.querySelector(".gate-link");
            if (note && note.parentNode) note.parentNode.style.display = "none";
            inp.focus();
          } else {
            var m2 = Math.ceil((t2.until - Date.now()) / 60000);
            err.textContent = "Too many attempts. Try again in " + m2 +
              " minute" + (m2 === 1 ? "" : "s") + ".";
          }
        }, 5000);
      }
    });

    function attempt() {
      var t2 = tries();
      if (t2.until && Date.now() < t2.until) {
        err.textContent = "Too many attempts. Try again in a few minutes.";
        return;
      }
      btn.disabled = true;
      sha256(inp.value).then(function (h) {
        if (h === hash) {
          clearTries();
          markUnlocked();
          g.parentNode.removeChild(g);
          window.dispatchEvent(new CustomEvent("ekguru:unlocked"));
        } else {
          var r = bumpTries();
          btn.disabled = false;
          inp.value = "";
          err.textContent = r.until
            ? "Too many attempts. Locked for ten minutes."
            : "Wrong passcode. " + (MAX_TRIES - r.n) + " attempt(s) left.";
        }
      }).catch(function (e) { btn.disabled = false; err.textContent = e.message; });
    }
  }

  /* ---------------------------------------------------------
     Run
     --------------------------------------------------------- */
  window.EkGuruGate = {
    /* Returns true when the page may render its contents. */
    check: function () {
      injectCss();
      var hash = (CFG.passcodeHash || "").trim();
      if (!hash) { setupScreen(); return false; }
      if (unlocked()) return true;
      lockScreen(hash);
      return false;
    },
    lock: function () {
      try { sessionStorage.removeItem(SESSION_KEY); } catch (e) {}
      location.reload();
    }
  };
})();
