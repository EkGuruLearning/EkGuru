/* =========================================================
   EkGuru — CONSENT CENTER  (v4)

   The compact center the site must carry instead of a
   full-width banner:

     [ Accept all ]  [ Reject — essential only ]  [ Customize ]
     …with the Privacy Policy linked in the text, and two
     OPTIONAL categories (functional, analytics) that are
     OFF until the visitor chooses them.

   Honest by construction:

   · No cookie is set anywhere on the site — the choice lives
     in localStorage, so "Reject" really means essential only.
   · No certification claims. EkGuru is NOT a certified consent
     platform, and that is said out loud instead of implied:
     because it is not, Google ads here are never personalized.
   · No emoji, no fake urgency, no "99% of visitors accepted".
   · The center is compact and centered at the bottom: it never
     covers the page's controls, closes on a choice or Escape,
     and can be reopened any time from the footer ("Cookie
     preferences").

   Storage is kept where js/monetization.js reads it
   (ekguru_cookie_consent_v3, same field names) and the choice
     is announced on <html data-consent> and as an
   ekguru:consent event, exactly like the previous version.

   Country/culture detection (data-country, data-culture) is
   preserved: css/experience.css and js/course-player.js read
   those attributes.
   ========================================================= */
(function () {
  "use strict";
  if (typeof window === "undefined" || !window.document) return;

  var CONSENT_KEY = "ekguru_cookie_consent_v3";  /* monetization.js reads it */
  var DATE_KEY = "ekguru_consent_date_v3";
  var COUNTRY_KEY = "ekguru_country";

  var CATEGORIES = [
    { id: "functional", name: "Functional",
      desc: "Remembers your language, lesson progress and offline saves. Stored on this device only." },
    { id: "analytics", name: "Analytics",
      desc: "Anonymous page and search counts, so we know which lessons help. No names, no IP tracking, no profiles." }
  ];

  /* ---------------------------------------------------------
     storage
     --------------------------------------------------------- */
  function readConsent() {
    try {
      var raw = localStorage.getItem(CONSENT_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  function writeConsent(consent) {
    try {
      localStorage.setItem(CONSENT_KEY, JSON.stringify(consent));
      localStorage.setItem(DATE_KEY, new Date().toISOString());
    } catch (e) {}
    try { document.documentElement.setAttribute("data-consent", JSON.stringify(consent)); } catch (e) {}
    try { document.dispatchEvent(new CustomEvent("ekguru:consent", { detail: consent })); } catch (e) {}
  }

  function makeConsent(opts) {
    return {
      necessary: true,
      functional: !!opts.functional,
      analytics: !!opts.analytics,
      advertising: !!opts.advertising,
      timestamp: Date.now()
    };
  }

  /* ---------------------------------------------------------
     the center
     --------------------------------------------------------- */
  var center = null;

  function buildCenter() {
    var el = document.createElement("div");
    el.id = "ekguru-consent";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", "Cookie preferences");
    el.hidden = true;

    var rows = CATEGORIES.map(function (c) {
      return '<label class="cc-row"><input type="checkbox" id="cc-' + c.id + '">' +
        '<span><b>' + c.name + "</b> — " + c.desc + "</span></label>";
    }).join("");

    el.innerHTML =
      '<div class="cc-in">' +
        '<p class="cc-text">EkGuru keeps a small amount of data on this device so the site works. ' +
        "Functional and analytics storage are optional, and off until you choose them. " +
        "Ads may appear to keep lessons free — and they are never personalized, because EkGuru " +
        'is not a certified consent platform and personalization needs one. ' +
        '<a href="/cookie-policy/">Cookie policy</a> · <a href="/privacy/">Privacy Policy</a></p>' +
        '<div class="cc-actions">' +
          '<button type="button" class="cc-btn cc-accept" id="cc-accept">Accept all</button>' +
          '<button type="button" class="cc-btn cc-reject" id="cc-reject">Reject — essential only</button>' +
          '<button type="button" class="cc-btn cc-customize" id="cc-customize" aria-expanded="false" aria-controls="cc-custom">Customize</button>' +
        "</div>" +
        '<div class="cc-custom" id="cc-custom" hidden>' +
          rows +
          '<p class="cc-note">Necessary storage is always on — it is how the site works. ' +
          "Advertising: because EkGuru is not a certified consent platform, Google ads here are " +
          "not personalized. Declining removes the ad slots from the page entirely.</p>" +
          '<div class="cc-custom-actions">' +
            '<button type="button" class="cc-btn cc-accept" id="cc-save">Save preferences</button>' +
            '<button type="button" class="cc-btn cc-reject" id="cc-cancel">Cancel</button>' +
          "</div>" +
        "</div>" +
      "</div>";

    document.body.appendChild(el);

    el.querySelector("#cc-accept").addEventListener("click", function () {
      writeConsent(makeConsent({ functional: true, analytics: true, advertising: true }));
      hideCenter();
    });
    el.querySelector("#cc-reject").addEventListener("click", function () {
      writeConsent(makeConsent({}));  /* essential only */
      hideCenter();
    });
    el.querySelector("#cc-customize").addEventListener("click", function () {
      var panel = el.querySelector("#cc-custom");
      var open = panel.hidden;
      panel.hidden = !open;
      this.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) {
        /* restore the recorded choice into the toggles, or nothing */
        var c = readConsent();
        el.querySelector("#cc-functional").checked = !!(c && c.functional);
        el.querySelector("#cc-analytics").checked = !!(c && c.analytics);
        var first = el.querySelector("#cc-functional");
        if (first) { try { first.focus(); } catch (e) {} }
      }
    });
    el.querySelector("#cc-save").addEventListener("click", function () {
      writeConsent(makeConsent({
        functional: el.querySelector("#cc-functional").checked,
        analytics: el.querySelector("#cc-analytics").checked,
        advertising: false  /* not personalized, and the visitor chose minimal */
      }));
      hideCenter();
    });
    el.querySelector("#cc-cancel").addEventListener("click", function () {
      el.querySelector("#cc-custom").hidden = true;
      el.querySelector("#cc-customize").setAttribute("aria-expanded", "false");
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && center && !center.hidden) hideCenter();
    });

    return el;
  }

  function showCenter() {
    if (!center) center = buildCenter();
    center.hidden = false;
    var accept = center.querySelector("#cc-accept");
    if (accept) { try { accept.focus(); } catch (e) {} }
  }

  function hideCenter() {
    if (center) center.hidden = true;
  }

  /* the footer's "Cookie preferences" link reopens the center */
  document.addEventListener("click", function (e) {
    var t = e.target && e.target.closest ? e.target.closest("[data-ekguru-consent-open]") : null;
    if (t) { e.preventDefault(); showCenter(); }
  }, true);

  /* ---------------------------------------------------------
     boot
     --------------------------------------------------------- */
  function init() {
    var consent = readConsent();
    if (consent) {
      writeConsent(consent);  /* re-apply data-consent + event for this load */
    } else {
      setTimeout(showCenter, 600);
    }
  }

  /* ---------------------------------------------------------
     country / culture detection — preserved from v300;
     css/experience.css and js/course-player.js read these.
     --------------------------------------------------------- */
  (function () {
    var path = String(location.pathname || "").toLowerCase();
    var aliases = {
      india: "IN", bharat: "IN", nepal: "NP", bangladesh: "BD", pakistan: "PK", srilanka: "LK",
      "sri-lanka": "LK", indonesia: "ID", "timor-leste": "TL", greece: "GR", cyprus: "CY",
      albania: "AL", "south-africa": "ZA", namibia: "NA", somalia: "SO", djibouti: "DJ",
      ethiopia: "ET", kenya: "KE", netherlands: "NL", belgium: "BE", suriname: "SR",
      iran: "IR", "united-arab-emirates": "AE", uae: "AE", "saudi-arabia": "SA",
      andorra: "AD", spain: "ES", france: "FR", haiti: "HT", canada: "CA",
      "united-states": "US", usa: "US", australia: "AU", "new-zealand": "NZ",
      japan: "JP", china: "CN", singapore: "SG", malaysia: "MY", turkey: "TR",
      germany: "DE", austria: "AT", switzerland: "CH", brazil: "BR", portugal: "PT",
      mexico: "MX", argentina: "AR", "united-kingdom": "GB", uk: "GB"
    };
    var code = "";
    Object.keys(aliases).some(function (slug) {
      if (new RegExp("(?:^|/|-)" + slug + "(?:/|-|$)").test(path)) { code = aliases[slug]; return true; }
      return false;
    });
    if (!code) {
      try {
        var locale = String(localStorage.getItem(COUNTRY_KEY) || navigator.language || "");
        var match = locale.match(/[-_]([A-Za-z]{2})$/); if (match) code = match[1].toUpperCase();
      } catch (e) {}
    }
    var culture = {
      IN: "south-asia", NP: "south-asia", BD: "south-asia", PK: "south-asia", LK: "south-asia",
      AE: "gulf", SA: "gulf", IR: "persian", ET: "horn", DJ: "horn", SO: "horn", KE: "east-africa",
      ZA: "southern-africa", NA: "southern-africa", ID: "southeast-asia", TL: "southeast-asia",
      MY: "southeast-asia", SG: "southeast-asia", JP: "japan", CN: "east-asia",
      GR: "mediterranean", CY: "mediterranean", AL: "balkans", ES: "mediterranean",
      FR: "western-europe", NL: "western-europe", BE: "western-europe", DE: "western-europe",
      AT: "western-europe", CH: "western-europe", AD: "mediterranean", SR: "caribbean",
      HT: "caribbean", BR: "latin-america", MX: "latin-america", AR: "latin-america"
    };
    if (code) document.documentElement.setAttribute("data-country", code);
    document.documentElement.setAttribute("data-culture", culture[code] || "global");
  })();

  window.EKGURU_COOKIES = {
    getConsent: readConsent,
    hasConsent: function () { var c = readConsent(); return !!(c && c.timestamp); },
    setConsent: writeConsent,
    showBanner: showCenter,
    showCenter: showCenter,
    categories: CATEGORIES
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
