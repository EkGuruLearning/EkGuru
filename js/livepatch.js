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
    var knownVisible = {};
    if (info && info.loaded) {
      var live = {};
      (window.EKGURU_TUTORS || []).forEach(function (t) { live[t.id] = 1; });
      Object.keys(live).forEach(function (id) { knownVisible[id] = 1; });

      /* v130 — pages WITHOUT tutors-data.js (city pages, the text
         directory) have no EKGURU_TUTORS, so the removal below was
         dead code on exactly the pages it was written for: hidden
         tutors stood in every "other tutors" list forever. On such
         pages, remove only ids POSITIVELY known hidden — the baked
         list plus live hidden stubs — never "everyone not in an
         empty list". A file-only tutor with no sheet row keeps
         their place, matching js/sheet.js. Still gated on real
         data: empty records means the fetch failed, and a failed
         fetch must never empty the page. */
      var hideSet = null;
      if (!Object.keys(live).length) {
        var RR = window.EKGURU_SHEET_RECORDS || {};
        var RH = window.EKGURU_SHEET_HIDDEN || [];
        if (Object.keys(RR).length) {
          hideSet = {};
          Object.keys(RR).forEach(function (id) {
            if (RR[id] && RR[id]._hiddenBySheet) hideSet[id] = 1;
            else knownVisible[id] = 1;
          });
          /* Baked ids yield to live full records: reactivated since
             the build means visible, not hidden. */
          RH.forEach(function (id) {
            if (!(RR[id] && !RR[id]._hiddenBySheet)) hideSet[id] = 1;
          });
        }
      }

      /* Only trust this when we genuinely have a tutor list. On a
         pre-rendered page with only the overrides loaded,
         EKGURU_TUTORS is empty and removing "everyone not in it"
         would delete the whole page. */
      if (Object.keys(live).length || hideSet) {
        var rows = document.querySelectorAll("[data-t-row]");
        for (var j = rows.length - 1; j >= 0; j--) {
          var rid = rows[j].getAttribute("data-t-row");
          var gone = hideSet ? !!hideSet[rid] : !live[rid];
          if (gone) {
            rows[j].parentNode && rows[j].parentNode.removeChild(rows[j]);
            hidden++;
          } else if (rows[j].getAttribute("data-baked-hide")) {
            /* Reactivated since the build: lift the first-paint
               concealment below. */
            rows[j].removeAttribute("data-baked-hide");
            rows[j].style.display = "";
          }
        }
      }
    }

    /* v130 — FIRST-PAINT CONCEALMENT, REVERSIBLE. The baked hidden
       list is the sheet as of the last build. Conceal (never remove)
       those rows immediately so unavailable tutors don't flash on
       static pages; when the live sheet lands, rows it confirms
       hidden are removed outright above, and rows it revives are
       shown again. Runs on baked data alone — no network wait. */
    var RH0 = window.EKGURU_SHEET_HIDDEN || [];
    if (RH0.length) {
      var pre = document.querySelectorAll("[data-t-row]");
      for (var h = 0; h < pre.length; h++) {
        var pid = pre[h].getAttribute("data-t-row");
        /* Live knowledge wins: never re-conceal a tutor the sheet
           currently shows as visible. */
        if (knownVisible[pid]) continue;
        if (RH0.indexOf(pid) > -1 &&
            !pre[h].getAttribute("data-baked-hide")) {
          pre[h].setAttribute("data-baked-hide", "1");
          pre[h].style.display = "none";
        }
      }
    }

    /* v130 — a hidden tutor's OWN profile must say so. /tutor/<id>/
       is pre-rendered and fully bookable; the card that led here is
       gone, but the URL still resolves (bookmarks, Google). When
       the sheet says hidden, say so honestly at the top and point
       the booking buttons at the live tutor list. Runs on baked
       data too, so the first paint is already honest. */
    try { profileHidden(info); } catch (e) { /* never break a page over this */ }

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

  /* v130 — see the note at the call site in apply(). */
  var UNAVAIL_TEXT = {
    en: ["Currently unavailable", "This tutor is not taking new students right now.", "See available tutors"],
    de: ["Derzeit nicht verfügbar", "Diese Lehrkraft nimmt derzeit keine neuen Schüler auf.", "Verfügbare Lehrkräfte"],
    fr: ["Indisponible pour le moment", "Ce tuteur n'accepte pas de nouveaux élèves pour l'instant.", "Voir les tuteurs disponibles"],
    es: ["No disponible actualmente", "Este tutor no acepta nuevos estudiantes por ahora.", "Ver tutores disponibles"],
    pt: ["Indisponível no momento", "Este tutor não está aceitando novos alunos agora.", "Ver tutores disponíveis"],
    ja: ["現在受付停止中", "この講師は現在新規生徒を受け付けていません。", "受付中の講師を見る"],
    ar: ["غير متاح حالياً", "هذا المعلم لا يقبل طلاباً جدداً في الوقت الحالي.", "عرض المعلمين المتاحين"]
  };

  function profileHidden(info) {
    /* Only pre-rendered profiles: /tutor/<id>/. The /tutor/ directory
       has no id, and tutor.html?id= is rendered by js/main.js. */
    var m = /\/tutor\/([a-z0-9-]+)\//i.exec(location.pathname + "/");
    if (!m) return;
    var id = m[1].toLowerCase();
    if (id === "tutor") return;

    var isHidden = (window.EKGURU_SHEET_HIDDEN || []).indexOf(id) > -1;
    /* The live sheet OVERRULES a stale baked list either way: a
       tutor the sheet now shows as visible gets the banner lifted,
       and one it newly hides gets it — all without a rebuild. */
    if (info && info.loaded) {
      var rec = (window.EKGURU_SHEET_RECORDS || {})[id];
      if (rec) isHidden = !!rec._hiddenBySheet;
    }

    var banner = document.getElementById("ekguru-unavail");
    var ctas = document.querySelectorAll('a[href*="tutor.html?id=' + id + '"]');

    if (!isHidden) {
      /* Reactivated since the build (or never hidden): lift a stale
         banner and restore the original booking links. */
      if (banner && banner.parentNode) banner.parentNode.removeChild(banner);
      for (var r = 0; r < ctas.length; r++) {
        if (ctas[r].getAttribute("data-orig-href")) {
          ctas[r].setAttribute("href", ctas[r].getAttribute("data-orig-href"));
          ctas[r].removeAttribute("data-orig-href");
        }
      }
      return;
    }

    var lang = (document.documentElement.getAttribute("lang") || "en").slice(0, 2);
    var tx = UNAVAIL_TEXT[lang] || UNAVAIL_TEXT.en;
    var name = id;
    try {
      var h1 = document.querySelector("main h1");
      if (h1 && h1.textContent) name = h1.textContent.trim().split("\n")[0].trim() || id;
    } catch (e) {}

    var listHref = location.pathname.replace(/\/tutor\/[^/]+\/.*$/, "/find-tutors.html");
    if (listHref === location.pathname) listHref = null;

    if (!banner) {
      banner = document.createElement("div");
      banner.id = "ekguru-unavail";
      banner.setAttribute("role", "status");
      banner.setAttribute("style", "margin:16px 0;padding:14px 16px;border:2px solid #b45309;border-radius:12px;background:#fffbeb;color:#451a03;");
      var host = document.querySelector("main") || document.body;
      host.insertBefore(banner, host.firstChild);
    }
    banner.innerHTML = "";
    var b1 = document.createElement("p");
    b1.setAttribute("style", "margin:0 0 4px;font-weight:700;font-size:1.05rem;");
    b1.textContent = "\u23F8\uFE0F " + name + " — " + tx[0];
    var b2 = document.createElement("p");
    b2.setAttribute("style", "margin:0 0 10px;");
    b2.textContent = tx[1];
    banner.appendChild(b1);
    banner.appendChild(b2);
    if (listHref) {
      var btn = document.createElement("a");
      btn.setAttribute("href", listHref);
      btn.setAttribute("class", "btn btn-primary");
      btn.textContent = tx[2] + " \u2192";
      banner.appendChild(btn);
    }

    /* Point every "book with <hidden>" button at the live list. The
       original href is kept so reactivation restores it. */
    if (listHref) {
      for (var c = 0; c < ctas.length; c++) {
        if (!ctas[c].getAttribute("data-orig-href")) {
          ctas[c].setAttribute("data-orig-href", ctas[c].getAttribute("href") || "");
        }
        ctas[c].setAttribute("href", listHref);
      }
    }
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
