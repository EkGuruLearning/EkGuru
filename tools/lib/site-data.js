/* =========================================================
   EkGuru — shared site data loader (build side)
   ---------------------------------------------------------
   One loader for every generator that needs the tutor roster:
   the tutors come out exactly as the browser will see them.

   It runs the real files in a vm sandbox, in the real order:

       js/site-config.js          site constants
       js/tutors/_registry.js     who exists, and in what order
       js/tutors/<each>.js        the hand-written tutor files
       js/tutors/_overrides.js    the sheet as of the last sync
       js/tutors-data.js          the assembler: merges, defaults,
                                  strips unpublished phone numbers
       js/i18n.js                 every translated string

   ⚠️ Do not re-implement these transforms. The two tools that
   parsed the sheet independently are exactly how a $3 price sat
   on six pages for nine versions (see js/sheet.js v72 note).

   tools/build-market-pages.js and tools/build-tutor-pages.js both
   use this, so the six market home pages and the tutor profiles
   can never disagree about who exists or what they charge.
   ========================================================= */
"use strict";

const fs = require("fs");
const vm = require("vm");

/* options.overrides
     true  (default) — layer js/tutors/_overrides.js on top, exactly as
                       js/livepatch.js does in the browser. The overrides
                       ARE the sheet as of the last sync, and the pages on
                       the site already bake them (index.html's tutor cards
                       quote the sheet's $6, not Sushila's file's $3).
                       A generated page that ignored them would disagree
                       with the page next to it and with Google's cache.
     false           — the hand-written tutor files only. Used by the
                       checks that compare files with files.
   Nothing in the overrides can publish a phone number or a private
   address: tools/sheetsync.js writes neither (see its header). */
function loadSite(options) {
  const useOverrides = !options || options.overrides !== false;
  let hidden = [];

  const sandbox = { console: { warn() {}, log() {}, error() {} } };
  vm.createContext(sandbox);
  sandbox.window = sandbox;                 // in a browser, window IS the global
  sandbox.document = { addEventListener() {}, querySelector: () => null, querySelectorAll: () => [] };
  sandbox.navigator = { languages: [], language: "en" };
  sandbox.localStorage = { getItem: () => null, setItem() {} };

  const files = ["js/site-config.js", "js/tutors/_registry.js"];
  fs.readdirSync("js/tutors")
    .filter((f) => f.endsWith(".js") && !f.startsWith("_"))
    .sort()
    .forEach((f) => files.push("js/tutors/" + f));
  files.push("js/tutors/_overrides.js", "js/tutors-data.js", "js/i18n.js");

  for (const f of files) {
    if (f === "js/tutors-data.js") {
      /* _overrides.js has just set window.EKGURU_SHEET_HIDDEN. It is captured
         here and cleared for the duration of the assembler, so EVERY tutor
         gets the defaults and the contact fallbacks — a tutor the sheet
         currently hides still needs a complete object, or the moment the
         owner sets active=yes again half their page is missing. The list is
         handed back as `hidden`; deciding what to publish is the caller's
         job, and the pages themselves list the whole roster (see below). */
      hidden = (sandbox.EKGURU_SHEET_HIDDEN || []).slice();
      sandbox.EKGURU_SHEET_HIDDEN = [];
    }
    try {
      vm.runInContext(fs.readFileSync(f, "utf8"), sandbox, { filename: f });
    } catch (e) {
      throw new Error("could not load " + f + ": " + e.message);
    }
  }

  /* The roster in registry order. The sheet-hidden list is NOT applied here:
     it is a runtime filter (js/tutors-data.js) that changes the moment the
     owner edits the spreadsheet, while the generated pages are crawled and
     indexed. Baking a temporary state into the HTML is how a tutor disappears
     from Google. The static page lists the roster; the live page filters it. */
  const order = sandbox.EKGURU_TUTOR_ORDER || [];
  const registered = sandbox.EKGURU_TUTOR_FILES || {};
  const tutors = order.filter((id) => registered[id]).map((id) => registered[id]);
  const unlisted = Object.keys(registered).filter((id) => order.indexOf(id) === -1);

  /* The overlay runs AFTER js/tutors-data.js on purpose: that file has already
     merged the defaults and removed anything that must never be published, and
     this must not undo either. It only fills in values the sheet owns. */
  if (useOverrides) {
    const O = sandbox.EKGURU_SHEET_OVERRIDES || {};
    tutors.forEach((t) => {
      const row = O[t.id];
      if (!row) return;
      Object.keys(row).forEach((k) => {
        if (k === "whatsapp" || k === "email") return;   // never from the sheet
        t[k] = row[k];
      });
      t.__fromSheet = true;
    });
  }

  return {
    i18n: sandbox.EKGURU_I18N || {},
    tutors,
    unlisted,
    hidden,
    site: sandbox.EKGURU_SITE || {},
  };
}

module.exports = { loadSite };
