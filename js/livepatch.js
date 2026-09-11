/* =========================================================
   EkGuru — LIVE-PATCH THE PRE-RENDERED PAGES  (v65)
   ---------------------------------------------------------
   Prakash:

     "tara hi nahi, sabhi card mein change ho raha hai lekin andar
      nahi … jo cheezein sheet se change hoti hain unko fix mat karo
      chahe vo kitni bhi jagah ho … fix text mat karna kisi bhi
      database wale cheezon ka, vo change through value of sheet
      honi chahiye — card ya page kahin bhi ho"

   He is right, and the gap was bigger than the tutor pages.

   ═══════════════════════════════════════════════════════
   THE BUG
   ═══════════════════════════════════════════════════════

   Thirty-two published pages render tutor data as PLAIN TEXT,
   written into the HTML at build time:

     tutor/<id>/index.html    the pre-rendered profiles
     tutor/index.html         the text directory
     hindi-tutor/<place>/     24 city and country pages
     learn/, ask/, answers/   three hub pages

     (that third line is written without a star-slash on purpose —
      it would close this comment block, which is exactly the
      syntax error the first version of this file shipped with)

   None of them loaded js/sheet.js. Not one. So:

     · the home page card said $6      ← sheet, live
     · the profile behind it said $10  ← file, from the last build

   Change a price in the spreadsheet and the cards followed within
   a page view while thirty-two pages kept the old figure until the
   next deploy. Two numbers for one thing, which is worse than one
   wrong number — a visitor who notices stops trusting the price.

   ═══════════════════════════════════════════════════════
   WHY NOT JUST LOAD THE WHOLE STACK ON THOSE PAGES?
   ═══════════════════════════════════════════════════════

   Because they are deliberately cheap. A pre-rendered page is the
   canonical, crawlable, no-JavaScript-required version. Loading
   tutors-data, main.js, features.js and the rest onto twenty-four
   city pages would add roughly 90 KB to each for the sake of
   patching a handful of numbers, and would risk main.js trying to
   render a #tutor-list that is not there.

   So this file is small and does exactly one job: find the values
   the sheet owns, and update them in place. It needs only
   site-config, sheet.js and the generated overrides.

   ═══════════════════════════════════════════════════════
   HOW A VALUE IS FOUND
   ═══════════════════════════════════════════════════════

   The generators mark every sheet-owned value with data
   attributes:

     <strong data-t="sushila-g" data-f="priceUSD" data-usd="6">$6</strong>
     <p     data-t="sushila-g" data-f="headline">Friendly Hindi…</p>

   data-t   which tutor
   data-f   which field
   data-fmt optional shape: "money" | "years" | "lessons" | "list"

   Nothing is guessed from the text. A regex over rendered prose
   looking for "$6" would also rewrite a price inside a sentence
   about market rates, and would silently miss a value the moment
   the wording changed. An explicit marker cannot drift.

   ⚠️ If a page carries no markers, this file does nothing at all.
   That is the correct behaviour for a page with no tutor data on
   it, and it means adding the script everywhere is harmless.
   ========================================================= */

(function () {
  "use strict";

  function tutorsById() {
    var out = {};
    (window.EKGURU_TUTORS || []).forEach(function (t) { out[t.id] = t; });

    /* A page may not load tutors-data.js at all — the pre-rendered
       profiles do not. The sheet overrides are still there, and they
       are a complete picture of every value the sheet sets, so they
       work as the source on their own. */
    var O = window.EKGURU_SHEET_OVERRIDES || {};
    Object.keys(O).forEach(function (id) {
      out[id] = out[id] || {};
      Object.keys(O[id]).forEach(function (k) {
        if (out[id][k] === undefined) out[id][k] = O[id][k];
      });
    });

    /* And the LIVE sheet, fetched after the page loaded. These win
       over the baked-in overrides — that is the whole point: the
       overrides are the sheet as of the last build, these are the
       sheet as of thirty seconds ago. */
    var R = window.EKGURU_SHEET_RECORDS || {};
    Object.keys(R).forEach(function (id) {
      out[id] = out[id] || {};
      Object.keys(R[id]).forEach(function (k) {
        if (k.charAt(0) !== "_") out[id][k] = R[id][k];
      });
    });
    return out;
  }

  function money(n) {
    if (n == null || n === "") return "";
    try {
      if (window.EkGuruPrice && window.EkGuruPrice.price) return window.EkGuruPrice.price(n);
    } catch (e) {}
    var S = window.EKGURU_SITE || {};
    return (S.currency || "$") + n;
  }

  function format(val, fmt) {
    if (val == null) return null;
    switch (fmt) {
      case "money":   return money(val);
      case "years":   return val + "+ years";
      case "lessons": return val + (Number(val) === 1 ? " lesson" : " lessons");
      case "list":    return Array.isArray(val) ? val.join(", ") : String(val);
      case "rating":  return Number(val).toFixed(1);
      default:
        if (Array.isArray(val)) return val.join(", ");
        if (val && typeof val === "object") return null;   /* not printable */
        return String(val);
    }
  }

  function apply() {
    var T = tutorsById();
    var nodes = document.querySelectorAll("[data-t][data-f]");
    var changed = 0, hidden = 0;

    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var id = el.getAttribute("data-t");
      var field = el.getAttribute("data-f");
      var t = T[id];
      if (!t) continue;

      var raw = t[field];
      if (raw === undefined || raw === null || raw === "") continue;

      var text = format(raw, el.getAttribute("data-fmt"));
      if (text === null) continue;

      /* A price also carries data-usd, which js/pricing.js reads to
         convert into the visitor's currency. Update BOTH or the two
         disagree the moment the currency layer redraws — the
         attribute would still hold the old dollars. */
      if (el.hasAttribute("data-usd") && field === "priceUSD") {
        el.setAttribute("data-usd", String(raw));
      }

      if (el.textContent !== text) { el.textContent = text; changed++; }
    }

    /* =========================================================
       A HIDDEN TUTOR MUST VANISH FROM THESE PAGES TOO
       ---------------------------------------------------------
       active=no removes a tutor from the build, but the build only
       runs at deploy time. Until then their name is still sitting
       in the "other tutors" list on twenty-four city pages and in
       the text directory.

       Anything marked data-t-row is removed outright when that
       tutor is no longer in the live list. This only fires when
       the sheet has actually loaded — a network failure must not
       empty the page.
       ========================================================= */
    var info = window.EKGURU_SHEET_INFO;
    if (info && info.loaded) {
      var live = {};
      (window.EKGURU_TUTORS || []).forEach(function (t) { live[t.id] = 1; });

      /* Only trust this when we genuinely have a tutor list. On a
         pre-rendered page with only the overrides loaded,
         EKGURU_TUTORS is empty and removing "everyone not in it"
         would delete the whole page. */
      if (Object.keys(live).length) {
        var rows = document.querySelectorAll("[data-t-row]");
        for (var j = rows.length - 1; j >= 0; j--) {
          var rid = rows[j].getAttribute("data-t-row");
          if (!live[rid]) {
            rows[j].parentNode && rows[j].parentNode.removeChild(rows[j]);
            hidden++;
          }
        }
      }
    }

    if (changed || hidden) {
      /* Prices were just rewritten, so the currency layer has to
         redraw them or an Indian visitor sees dollars again. */
      try { if (window.EkGuruPrice && window.EkGuruPrice.redraw) window.EkGuruPrice.redraw(); } catch (e) {}
      try {
        window.dispatchEvent(new CustomEvent("ekguru:livepatch", {
          detail: { changed: changed, hidden: hidden }
        }));
      } catch (e) {}
    }
    return changed + hidden;
  }

  function run() { try { apply(); } catch (e) { /* never break a page over this */ } }

  /* The overrides are baked into the page, so patch immediately —
     that fixes the FIRST paint, before any network request. Then
     again when the live sheet lands with anything newer. */
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();

  window.addEventListener("ekguru:sheet", run);
  window.addEventListener("ekguru:reviews", run);
  window.addEventListener("ekguru:rates", run);
  window.addEventListener("ekguru:currency", run);

  window.EkGuruLivePatch = { apply: apply };
})();
