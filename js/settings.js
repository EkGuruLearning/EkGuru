/* =========================================================
   EkGuru — SITE SETTINGS FROM A SHEET  (v69)
   ---------------------------------------------------------
   Prakash:

     "bug fix karo jaise koi cheez db mein ho or vo same cheez
      text form mein fixed ho jo change nahi hogi — jaise mail id.
      Isko sheet se karo, sheet mein change karte hi sabhi jagah
      change honi chahiye. Ye aise kaafi bugs hain, find karo,
      fix karo."

   ═══════════════════════════════════════════════════════
   THE BUG, AND IT IS THE SAME SHAPE AS THE PRICE ONE
   ═══════════════════════════════════════════════════════

   The tutor sheet controls every tutor. Nothing controls the
   SITE. The email address, the WhatsApp number, the YouTube
   channel, the application form link — all of them live in
   js/site-config.js and are then BAKED into the generated HTML.

   Counted, not guessed:

       EkGuruLearning@gmail.com   in 85 published HTML files
                                  and in the JSON-LD of every
                                  tutor page

   Change that address and you would have to rebuild and push to
   move it. Until then, 85 pages point at an inbox you no longer
   read — including the schema Google shows in search results,
   and the mailto on every "report a Hindi spelling" note.

   This is exactly the class of bug he is describing: a value that
   lives in one place conceptually, and in eighty-five places
   physically.

   ═══════════════════════════════════════════════════════
   HOW IT WORKS
   ═══════════════════════════════════════════════════════

   A fourth tab, two columns:

       key              value
       email            hello@example.com
       whatsapp         +919876543210
       youtubeChannel   https://youtube.com/@...
       applyFormUrl     https://forms.gle/...
       tagline          One Student. One Guru. One Goal.

   The BUILD reads it (tools/sheetsync.js) and writes the values
   into the generated pages, so a crawler sees them.

   The BROWSER reads it too (this file) and patches anything
   marked data-s="email" — so a change reaches a visitor on the
   next page view, without a deploy. Same two-halves design as
   the tutor data, for the same reason: one of them is what
   Google reads and the other is what a person sees.

   ⚠️ Unset keys change nothing. A blank cell is not "make it
   empty", it is "leave it alone" — the same rule as the tutor
   sheet, because the alternative is one accidental deletion
   wiping the site's contact address.
   ========================================================= */

(function (root) {
  "use strict";

  var S = root.EKGURU_SITE || {};
  var CFG = S.settings || {};
  var url = String(CFG.csvUrl || "").trim();

  var CACHE_KEY = "ekguru_settings_v1";
  var MAX_AGE = (Number(CFG.cacheMinutes) || 5) * 60 * 1000;

  /* ---------------------------------------------------------
     Which keys may be set, and how each is validated.

     An allow-list, because this sheet can change the address
     bookings are sent to. A typo must not silently redirect
     every enquiry into nowhere, and an unknown key must not be
     able to overwrite something structural like baseUrl.
     --------------------------------------------------------- */
  var FIELDS = {
    email: function (v) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? v : null;
    },
    /* A phone number is only published if it is a real one. The
       site hides every WhatsApp button when this is empty, which
       is the intended default — see js/tutors-data.js on why
       personal numbers are never published for tutors. */
    whatsapp: function (v) {
      if (/^(none|no|off|hide)$/i.test(v)) return "";
      return /^\+?[0-9][0-9\s-]{8,17}$/.test(v) ? v.replace(/[\s-]/g, "") : null;
    },
    youtubeChannel: function (v) {
      if (/^(none|no|off)$/i.test(v)) return "";
      return /^https:\/\/(www\.)?youtube\.com\//.test(v) ? v : null;
    },
    facebook: function (v) {
      if (/^(none|no|off)$/i.test(v)) return "";
      return /^https:\/\/(www\.)?facebook\.com\//.test(v) ? v : null;
    },
    instagram: function (v) {
      if (/^(none|no|off)$/i.test(v)) return "";
      return /^https:\/\/(www\.)?instagram\.com\//.test(v) ? v : null;
    },
    applyFormUrl: function (v) {
      if (/^(none|no|off)$/i.test(v)) return "";
      return /^https:\/\//.test(v) ? v : null;
    },
    tagline: function (v) { return v.length <= 90 ? v : null; },
    /* Deliberately NOT settable from the sheet:

         baseUrl     changing it breaks every canonical, the
                     sitemap and the schema at once, and it can
                     only change when the repo is renamed — which
                     is a code change anyway.
         brand       it is in the logo, the manifest and 130
                     titles; a spreadsheet typo would rename the
                     company on every page.
         passcodeHash, mail keys   secrets never go in a public
                     sheet, and this one is published to the web. */
    supportHours: function (v) { return v.length <= 60 ? v : null; }
  };

  function parseCSV(text) {
    var rows = [], row = [], field = "", q = false;
    text = String(text).replace(/^\uFEFF/, "");
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (q) {
        if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
        else if (c === '"') q = false;
        else field += c;
      } else if (c === '"') q = true;
      else if (c === ",") { row.push(field); field = ""; }
      else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
      else if (c !== "\r") field += c;
    }
    if (field.length || row.length) { row.push(field); rows.push(row); }
    return rows;
  }

  function toPairs(rows) {
    if (!rows.length) return {};
    var head = rows[0].map(function (h) { return String(h).trim().toLowerCase(); });
    var ki = head.indexOf("key"), vi = head.indexOf("value");
    if (ki === -1 || vi === -1) return {};
    var out = {};
    rows.slice(1).forEach(function (r) {
      var k = String(r[ki] || "").trim();
      var v = String(r[vi] || "").trim();
      /* The #help row, and blank cells that mean "leave it". */
      if (!k || k.charAt(0) === "#" || !v) return;
      out[k] = v;
    });
    return out;
  }

  function apply(pairs) {
    var changed = 0, refused = [];

    Object.keys(pairs).forEach(function (rawKey) {
      /* Case-insensitive: someone typing "Email" on a phone should
         not silently do nothing. Same lesson as the tutor sheet. */
      var key = Object.keys(FIELDS).filter(function (f) {
        return f.toLowerCase() === rawKey.toLowerCase();
      })[0];
      if (!key) { refused.push(rawKey + " (not a setting)"); return; }

      var val = FIELDS[key](pairs[rawKey]);
      if (val === null) { refused.push(rawKey + ' = "' + pairs[rawKey].slice(0, 24) + '"'); return; }
      if (S[key] === val) return;
      S[key] = val;
      changed++;
    });

    if (refused.length && root.console && console.warn) {
      console.warn("[EkGuru] settings refused: " + refused.join(", ") +
        ". The previous value was kept.");
    }

    root.EKGURU_SETTINGS_INFO = {
      loaded: true, changed: changed, refused: refused, at: new Date().toISOString()
    };
    return changed;
  }

  /* ---------------------------------------------------------
     Write the values into the page.

     Anything marked data-s="email" gets the text; an <a> also
     gets a matching href. This is the same mechanism as
     js/livepatch.js uses for tutor data, and it exists for the
     same reason: a generated page prints the value as plain text
     and cannot otherwise follow a change.
     --------------------------------------------------------- */
  function paint() {
    var n = 0;
    var nodes = document.querySelectorAll("[data-s]");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var key = el.getAttribute("data-s");
      var v = S[key];
      if (v === undefined || v === null || v === "") continue;

      if (el.tagName === "A") {
        var href = el.getAttribute("href") || "";
        if (key === "email") {
          /* Keep any ?subject= the page had — the spelling-report
             links carry the page title in it, and losing that
             makes every report say only "Hindi spelling". */
          var q = href.indexOf("?");
          el.setAttribute("href", "mailto:" + v + (q > -1 ? href.slice(q) : ""));
        } else if (/^https?:/.test(String(v))) {
          el.setAttribute("href", v);
        }
      }
      /* Only replace the text when the element IS the value, not
         when it merely links to it — "Contact us" must not turn
         into an email address. */
      if (el.hasAttribute("data-s-text") || el.textContent.indexOf("@") > -1 ||
          el.getAttribute("data-s-force") !== null) {
        if (el.textContent !== v) { el.textContent = v; n++; }
      }
    }

    /* Every plain mailto: to the OLD address, anywhere on the
       page. This is what makes an address change actually reach
       85 files' worth of links without each one being marked. */
    var old = CFG.previousEmail || "";
    if (S.email && old && old !== S.email) {
      var links = document.querySelectorAll('a[href^="mailto:"]');
      for (var j = 0; j < links.length; j++) {
        var h = links[j].getAttribute("href");
        if (h.indexOf(old) > -1) {
          links[j].setAttribute("href", h.replace(old, S.email));
          if (links[j].textContent.indexOf(old) > -1) {
            links[j].textContent = links[j].textContent.replace(old, S.email);
          }
          n++;
        }
      }
    }

    if (n) {
      try {
        root.dispatchEvent(new CustomEvent("ekguru:settings", { detail: { painted: n } }));
      } catch (e) {}
    }
    return n;
  }

  function readCache() {
    try {
      var raw = root.localStorage && root.localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var c = JSON.parse(raw);
      if (!c || !c.t || !c.pairs) return null;
      return { stale: Date.now() - c.t > MAX_AGE, pairs: c.pairs };
    } catch (e) { return null; }
  }
  function writeCache(pairs) {
    try {
      root.localStorage &&
        root.localStorage.setItem(CACHE_KEY, JSON.stringify({ t: Date.now(), pairs: pairs }));
    } catch (e) {}
  }

  function fetchSheet() {
    var ctrl = null, timer = null;
    try { ctrl = new AbortController(); } catch (e) {}
    if (ctrl) timer = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, 8000);

    return root.fetch(url, { signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { return r.ok ? r.text() : Promise.reject(new Error("HTTP " + r.status)); })
      .then(function (text) {
        if (timer) clearTimeout(timer);
        if (/^\s*</.test(text)) throw new Error("that URL returns a page, not CSV");
        var pairs = toPairs(parseCSV(text));
        if (!Object.keys(pairs).length) throw new Error("no key/value rows");
        writeCache(pairs);
        if (apply(pairs)) paint();
      })
      .catch(function (e) {
        if (timer) clearTimeout(timer);
        root.EKGURU_SETTINGS_INFO = { loaded: false, error: e.message };
        /* Silent by design in the console only — a settings sheet
           that will not load must never change anything, and the
           built-in values are already correct. */
        if (root.console && console.warn) {
          console.warn("[EkGuru] settings sheet not loaded: " + e.message +
            " — using the values in js/site-config.js.");
        }
      });
  }

  /* Paint immediately from whatever is configured, so a page that
     marks its email is correct before any network call. */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { paint(); });
  } else { paint(); }

  root.EkGuruSettings = {
    apply: apply, paint: paint,
    fields: function () { return Object.keys(FIELDS); },
    info: function () { return root.EKGURU_SETTINGS_INFO || { loaded: false }; },
    refresh: function () {
      try { root.localStorage && root.localStorage.removeItem(CACHE_KEY); } catch (e) {}
      return url ? fetchSheet() : Promise.resolve();
    }
  };

  if (!url || typeof root.fetch !== "function") return;

  var cached = readCache();
  if (cached) {
    if (apply(cached.pairs)) paint();
    if (cached.stale || CFG.alwaysRevalidate !== false) fetchSheet();
  } else {
    fetchSheet();
  }

})(typeof window !== "undefined" ? window : globalThis);
