/* =========================================================
   EkGuru — GENERIC AFFILIATE ENGINE (skeleton, inactive)
   ---------------------------------------------------------
   Purpose: one honest place for future affiliate links.

   This file ships INACTIVE. There is no approved affiliate
   program on EkGuru today, and this engine cannot create one:

     · data/affiliate-programs.json contains zero programs.
     · activation_master_switch is false.
     · With no APPROVED + enabled program, scan() below
       NEUTRALISES any element marked data-affiliate instead of
       monetising it — an author cannot accidentally publish a
       tracking link by adding attributes to an anchor.

   What an active setup would do (all of it, never a subset):
     1. read the registry (fetch data/affiliate-programs.json)
     2. for <a data-affiliate="slug"> anchors whose slug is
        APPROVED+enabled, on an allowed page class, on an
        allowed placement:
          - append the program's tracking parameters
          - force rel="sponsored nofollow noopener"
          - inject the program's disclosure_text beside the link
        if the page is excluded or the program is not approved,
        strip the data-affiliate marker and leave a plain link.
     3. record an aggregate outbound-click event through the
        site's existing analytics ONLY when analytics consent
        was granted (js/cookie-consent.js owns that state);
        otherwise record nothing. No personal data, ever.

   Page-class policy mirrors the ad policy: affiliate links never
   appear on INTERACTIVE_LEARNING, UTILITY, TRANSACTIONAL,
   ACCOUNT, ADMIN, CONTACT, BOOKING, PAYMENT, ERROR, SEARCH,
   PLACEHOLDER, RESEARCH_REQUIRED or INCOMPLETE surfaces.
   ========================================================= */
(function (root) {
  "use strict";

  var REGISTRY_URL = "/data/affiliate-programs.json";
  var EXCLUDED_CLASSES = {
    INTERACTIVE_LEARNING: true, UTILITY: true, TRANSACTIONAL: true,
    ACCOUNT: true, ADMIN: true, CONTACT: true, BOOKING: true,
    PAYMENT: true, ERROR: true, SEARCH: true, PLACEHOLDER: true,
    RESEARCH_REQUIRED: true, INCOMPLETE: true
  };

  function pageClass() {
    var c = document.documentElement.getAttribute("data-ad-class");
    return c || "MEDIUM_CONTENT";
  }

  function analyticsAllowed() {
    try {
      var raw = localStorage.getItem("ekguru_cookie_consent_v3");
      if (!raw) return false;
      var c = JSON.parse(raw);
      return !!(c && c.analytics === true);
    } catch (e) { return false; }
  }

  function trackOutbound(slug, href) {
    /* Aggregate only, consent-gated, personal-data-free. */
    if (!analyticsAllowed()) return;
    try {
      if (root.goatcounter && typeof root.goatcounter.count === "function") {
        root.goatcounter.count({
          path: "/outbound/" + encodeURIComponent(slug),
          title: "affiliate-click",
          event: true
        });
      }
    } catch (e) { /* tracking is best-effort and never blocks navigation */ }
    void href;
  }

  function neutralise(anchor) {
    /* The honest default: not approved => not an affiliate link. */
    anchor.removeAttribute("data-affiliate");
  }

  function activate(anchor, program) {
    var url;
    try { url = new URL(anchor.href, location.href); } catch (e) { neutralise(anchor); return; }
    if (program.tracking_id) {
      /* The parameter name comes from the program entry; we never
         guess one. If none is declared, the link stays plain. */
      (program.tracking_params || []).forEach(function (p) {
        url.searchParams.set(p.name, p.value);
      });
      anchor.href = url.toString();
    }
    anchor.setAttribute("rel", "sponsored nofollow noopener");
    /* Disclosure: required, beside the link, program-specific text. */
    if (!anchor.parentNode.querySelector(".affiliate-disclosure")) {
      var d = document.createElement("small");
      d.className = "affiliate-disclosure";
      d.style.display = "block";
      d.textContent = program.disclosure_text ||
        "This is an affiliate link: EkGuru may earn a commission at no extra cost to you.";
      anchor.parentNode.insertBefore(d, anchor.nextSibling);
    }
    anchor.addEventListener("click", function () {
      trackOutbound(program.slug, anchor.href);
    }, { passive: true });
  }

  function loadRegistry() {
    return fetch(REGISTRY_URL, { credentials: "same-origin" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
  }

  function scan(scope) {
    if (EXCLUDED_CLASSES[pageClass()]) return Promise.resolve(0);
    var anchors = Array.prototype.slice.call(
      (scope || document).querySelectorAll("a[data-affiliate]"));
    if (!anchors.length) return Promise.resolve(0);
    return loadRegistry().then(function (registry) {
      var masterOn = !!(registry && registry.global_rules &&
                        registry.global_rules.activation_master_switch === true);
      var programs = (registry && Array.isArray(registry.programs)) ? registry.programs : [];
      var activated = 0;
      anchors.forEach(function (a) {
        var slug = a.getAttribute("data-affiliate");
        var program = null;
        for (var i = 0; i < programs.length; i++) {
          var p = programs[i];
          if (p && p.slug === slug && p.enabled === true &&
              p.approval_status === "APPROVED" &&
              p.owner_status === "APPROVED") { program = p; break; }
        }
        if (!masterOn || !program) { neutralise(a); return; }
        if (Array.isArray(program.allowed_placements) &&
            program.allowed_placements.indexOf(location.pathname) === -1) {
          neutralise(a); return;
        }
        activate(a, program); activated++;
      });
      return activated;
    });
  }

  root.EkGuruAffiliate = {
    scan: scan,
    /* Deliberately NOT auto-run: wiring this script into a page is an
       editorial decision made per page when the first APPROVED program
       exists. Until then, no page ships this file. */
    _internals: { pageClass: pageClass, analyticsAllowed: analyticsAllowed }
  };
})(window);
