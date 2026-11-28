/* EkGuru — Advanced Cookie Consent & Usage System v300
   Fixes: cookies usage explanation, AdSense compliance, GDPR
   Features: consent banner, preference center, gtag consent mode
   Monetization: supports AdSense, analytics, functional cookies
*/
(function () {
  "use strict";

  var CONSENT_KEY = "ekguru_cookie_consent_v3";
  var CONSENT_DATE_KEY = "ekguru_consent_date_v3";
  var COUNTRY_KEY = "ekguru_country";
  // A local preferences banner is not a Google-certified CMP/TCF deployment.
  // Advertising consent therefore remains unavailable and false until the
  // account-side certified flow is deployed and production-tested.
  var ADVERTISING_AVAILABLE = false;

  // Cookie categories explained
  var COOKIE_INFO = {
    necessary: {
      name: "Necessary",
      desc: "Basic static-page delivery and the record of your privacy choice. EkGuru has no login session.",
      examples: "Privacy choice in local storage; no EkGuru HTTP cookie",
      required: true
    },
    functional: {
      name: "Functional",
      desc: "Remembers your choices: language, theme, progress, offline saves.",
      examples: "ekguru_progress, language, theme, offline list",
      required: false
    },
    analytics: {
      name: "Analytics",
      desc: "Counts page views without cookies or personal data (GoatCounter): which pages help learners most, where people get stuck. On by default; switch it off here any time.",
      examples: "page views, search queries (anonymous)",
      required: false
    },
    advertising: {
      name: "Advertising",
      desc: "Currently disabled. A certified regional consent flow must be deployed before AdSense can be enabled.",
      examples: "No runtime ad units; review loader on eligible content pages",
      required: false
    }
  };

  var currentConsent = null;

  function readConsent() {
    try {
      var raw = localStorage.getItem(CONSENT_KEY);
      var consent = raw ? JSON.parse(raw) : null;
      if (!consent || Array.isArray(consent) || consent.necessary !== true ||
          !['functional', 'analytics', 'advertising'].every(function (key) { return typeof consent[key] === 'boolean'; }) ||
          !Number.isFinite(consent.timestamp) || consent.timestamp <= 0) return null;
      return consent;
    } catch (e) { return null; }
  }

  function writeConsent(consent) {
    var previous = currentConsent || readConsent();
    var requested = consent || defaultConsent();
    consent = {
      necessary: true, functional: requested.functional === true,
      analytics: requested.analytics === true,
      advertising: ADVERTISING_AVAILABLE && requested.advertising === true,
      timestamp: Date.now()
    };
    var saved = false, oldRecord, oldDate, captured = false;
    try {
      oldRecord = localStorage.getItem(CONSENT_KEY);
      oldDate = localStorage.getItem(CONSENT_DATE_KEY); captured = true;
      localStorage.setItem(CONSENT_KEY, JSON.stringify(consent));
      localStorage.setItem(CONSENT_DATE_KEY, new Date(consent.timestamp).toISOString());
      saved = true;
    } catch (e) {
      if (captured) try {
        if (oldRecord === null) localStorage.removeItem(CONSENT_KEY); else localStorage.setItem(CONSENT_KEY, oldRecord);
        if (oldDate === null) localStorage.removeItem(CONSENT_DATE_KEY); else localStorage.setItem(CONSENT_DATE_KEY, oldDate);
      } catch (ignored) {}
    }
    applyConsent(consent, previous);
    var notice = document.getElementById('ekguru-consent-storage-status');
    if (!saved) {
      if (!notice) {
        notice = document.createElement('p'); notice.id = 'ekguru-consent-storage-status';
        notice.setAttribute('role', 'status'); document.body.appendChild(notice);
      }
      notice.textContent = 'Privacy choices apply to this page, but this browser could not save them. You may be asked again on another page or visit.';
    } else if (notice) notice.remove();
    return saved;
  }

  function applyConsent(consent, previous) {
    // Restoring a saved choice must not rewrite its record or consent date.
    consent = Object.assign({}, consent, { advertising: ADVERTISING_AVAILABLE && consent.advertising === true });
    currentConsent = consent;
    // gtag consent mode
    try {
      if (window.gtag) {
        window.gtag('consent', 'update', {
          'ad_storage': consent.advertising ? 'granted' : 'denied',
          'ad_user_data': consent.advertising ? 'granted' : 'denied',
          'ad_personalization': consent.advertising ? 'granted' : 'denied',
          'analytics_storage': consent.analytics ? 'granted' : 'denied',
          'functionality_storage': consent.functional ? 'granted' : 'denied'
        });
      }
    } catch (e) {}
    // dataLayer for GTM
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'cookie_consent_update',
        consent: consent
      });
    } catch (e) {}
    document.documentElement.setAttribute('data-consent', JSON.stringify(consent));
    document.dispatchEvent(new CustomEvent('ekguru:consent', { detail: consent }));
    if (previous && previous.advertising && !consent.advertising) {
      document.querySelectorAll('.ad-slot-wrapper, ins.adsbygoogle').forEach(function (node) {
        if (node.parentNode) node.parentNode.removeChild(node);
      });
    }
  }

  function defaultConsent() {
    /* What is in force before any choice: local progress storage and the
       cookieless page counter (js/analytics.js, THE GATE). Advertising is
       never on. A saved record always replaces this. */
    return {
      necessary: true,
      functional: true,
      analytics: true,
      advertising: false,
      timestamp: Date.now()
    };
  }

  function hasConsent() {
    var c = readConsent();
    return !!(c && c.timestamp);
  }

  function ensureConsentStyle() {
    if (document.getElementById('ekguru-consent-style')) return;
    var link = document.createElement('link');
    link.id = 'ekguru-consent-style'; link.rel = 'stylesheet'; link.href = '/css/cookie-consent.css';
    document.head.appendChild(link);
  }

  function createBanner() {
    if (document.getElementById('ekguru-consent')) return;
    ensureConsentStyle();
    var banner = document.createElement('section');
    banner.id = 'ekguru-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-labelledby', 'consent-title');
    banner.setAttribute('aria-describedby', 'consent-description');
    banner.setAttribute('aria-live', 'polite');
    banner.innerHTML =
      '<div class="cc-top"><span class="cc-icon" aria-hidden="true">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.7 19 5.5v5.2c0 4.3-2.7 7.8-7 10.2-4.3-2.4-7-5.9-7-10.2V5.5z"/><path d="m9 11.5 2 2 4-4"/></svg></span>' +
        '<button type="button" class="cc-close" id="consent-close" aria-label="Close privacy notice without changing choices">&times;</button></div>' +
      '<p class="cc-eyebrow">Your privacy matters</p>' +
      '<h2 id="consent-title">Your space. Your choice.</h2>' +
      '<p class="cc-copy" id="consent-description">Learning preferences can stay on your device. <strong>Cookieless analytics is on by default</strong>; you can switch it off. Advertising is currently disabled.</p>' +
      '<p class="cc-links"><a href="/cookie-policy/">Cookie &amp; storage details</a> &nbsp;·&nbsp; <a href="/privacy/">Privacy policy</a></p>' +
      '<div class="consent-actions">' +
        '<button type="button" class="consent-btn consent-accept" id="consent-accept-all">Accept available</button>' +
        '<button type="button" class="consent-btn consent-reject" id="consent-reject">Only essential</button>' +
        '<button type="button" class="consent-settings" id="consent-customize" aria-expanded="false" aria-controls="consent-custom">Manage preferences</button>' +
      '</div>' +
      '<div id="consent-custom" hidden>' +
        '<h3 id="consent-custom-title" tabindex="-1">Privacy preferences</h3>' +
        '<p class="cc-intro">Choose what is available. You can return here any time.</p>' +
        '<label class="cc-option"><input type="checkbox" checked disabled> <span><strong>Necessary</strong><small>Records your privacy choice.</small></span></label>' +
        '<label class="cc-option"><input type="checkbox" id="cc-functional"> <span><strong>Functional</strong><small>Signals your functionality preference; learning progress and settings may still be stored on this device.</small></span></label>' +
        '<label class="cc-option"><input type="checkbox" id="cc-analytics"> <span><strong>Analytics</strong><small>Cookieless page counting. Untick to stop future counting.</small></span></label>' +
        '<label class="cc-option"><input type="checkbox" id="cc-advertising" disabled> <span><strong>Advertising</strong><small>Unavailable until a certified consent flow is deployed.</small></span></label>' +
        '<div class="cc-custom-actions"><button type="button" class="consent-btn consent-accept" id="consent-save-custom">Save preferences</button><button type="button" class="consent-btn consent-reject" id="consent-cancel-custom">Cancel</button></div>' +
      '</div>' +
      '<p class="cc-intro">Only essential stops analytics and keeps local learning storage available. Close without choosing leaves the current defaults in place.</p>';
    document.body.appendChild(banner);
    var launcher = document.getElementById('ekguru-cookie-settings');
    if (launcher) launcher.hidden = true;
    var saved = currentConsent || readConsent() || defaultConsent();
    banner.querySelector('#cc-functional').checked = saved.functional === true;
    banner.querySelector('#cc-analytics').checked = saved.analytics === true;
    banner.querySelector('#cc-advertising').checked = ADVERTISING_AVAILABLE && saved.advertising === true;
    requestAnimationFrame(function () { requestAnimationFrame(function () { banner.classList.add('show'); }); });

    function setCustom(open, moveFocus) {
      banner.querySelector('#consent-custom').hidden = !open;
      banner.querySelector('#consent-customize').setAttribute('aria-expanded', String(open));
      if (moveFocus) (open ? banner.querySelector('#consent-custom-title') : banner.querySelector('#consent-customize')).focus();
    }
    function dismiss() {
      var hadFocus = banner.contains(document.activeElement);
      banner.remove();
      var settings = document.getElementById('ekguru-cookie-settings');
      if (settings) { settings.hidden = false; if (hadFocus) settings.focus(); }
    }
    banner.querySelector('#consent-close').addEventListener('click', dismiss);
    banner.querySelector('#consent-accept-all').addEventListener('click', function () {
      writeConsent({ necessary: true, functional: true, analytics: true, advertising: false, timestamp: Date.now() });
      dismiss();
    });
    banner.querySelector('#consent-reject').addEventListener('click', function () {
      writeConsent({ necessary: true, functional: true, analytics: false, advertising: false, timestamp: Date.now() });
      dismiss();
    });
    banner.querySelector('#consent-customize').addEventListener('click', function () {
      setCustom(banner.querySelector('#consent-custom').hidden, true);
    });
    banner.querySelector('#consent-save-custom').addEventListener('click', function () {
      writeConsent({ necessary: true, functional: banner.querySelector('#cc-functional').checked,
        analytics: banner.querySelector('#cc-analytics').checked,
        advertising: banner.querySelector('#cc-advertising').checked, timestamp: Date.now() });
      dismiss();
    });
    banner.querySelector('#consent-cancel-custom').addEventListener('click', function () { setCustom(false, true); });
    banner._openPreferences = function () { setCustom(true, true); };
  }

  function ensureSettingsButton() {
    if (document.getElementById('ekguru-cookie-settings')) return;
    var button = document.createElement('button');
    button.type = 'button'; button.id = 'ekguru-cookie-settings';
    button.className = 'consent-settings'; button.textContent = 'Privacy settings';
    button.setAttribute('aria-haspopup', 'dialog');
    button.addEventListener('click', function () {
      createBanner();
      var dialog = document.getElementById('ekguru-consent');
      if (dialog) dialog._openPreferences();
    });
    document.body.appendChild(button);
  }

  function initConsentMode() {
    // Default deny for GDPR compliance until user consents
    try {
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      window.gtag = window.gtag || gtag;
      gtag('consent', 'default', {
        'ad_storage': 'denied',
        'ad_user_data': 'denied',
        'ad_personalization': 'denied',
        'analytics_storage': 'denied',
        'functionality_storage': 'granted',
        'security_storage': 'granted'
      });
      gtag('set', 'ads_data_redaction', true);
    } catch (e) {}
  }

  function init() {
    initConsentMode();
    ensureConsentStyle();
    ensureSettingsButton();
    
    var consent = readConsent();
    if (consent) {
      applyConsent(consent, null); // restore without renewing the saved date
    } else {
      // Show banner after short delay
      setTimeout(createBanner, 1200);
    }

    // Expose API
    window.EKGURU_COOKIES = {
      getConsent: readConsent,
      hasConsent: hasConsent,
      setConsent: writeConsent,
      showBanner: createBanner,
      withdrawOptional: function () {
        writeConsent({ necessary: true, functional: false, analytics: false, advertising: false, timestamp: Date.now() });
      },
      advertisingAvailable: ADVERTISING_AVAILABLE,
      info: COOKIE_INFO,
      // How cookies are used - for cookie-policy page
      usage: {
        essential: [
          "Remember the privacy choice itself in local storage",
          "Deliver the static page without an EkGuru login session"
        ],
        functional: [
          "Save lesson progress on your device (localStorage)",
          "Remember language preference (en, es, fr, de, pt, ja, ar)",
          "Remember country context",
          "Offline saved pages list",
          "Practice question history and mastery",
          "Quiz and test scores"
        ],
        analytics: [
          "Cookieless page views, on by default, off the moment you say so",
          "Page, referrer, approximate country and browser type",
          "No cross-site advertising identifier"
        ],
        advertising: [
          "Unavailable in this release",
          "Runtime ad units disabled; review loader already present on eligible content pages"
        ],
        howToUse: [
          "Necessary: records the privacy choice",
          "Functional: local progress and display preferences",
          "Analytics: cookieless page counts, switch off with Only essential or Customise",
          "Advertising: disabled and unavailable",
          "Change choices with the Privacy settings button"
        ],
        monetization: [
          "Optional one-time support uses a Razorpay-hosted link",
          "Google AdSense is disabled pending site and certified-consent readiness",
          "Affiliate tracking is disabled until a real programme relationship is configured",
          "Tutor-lesson payments are not collected by EkGuru in this release"
        ]
      }
    };

    document.documentElement.dataset.consentFramework = "ekguru-v3";
  }

  // Country detection (existing logic preserved)
  (function () {
    var path = String(location.pathname || "").toLowerCase();
    var aliases = {
      india:"IN",bharat:"IN",nepal:"NP",bangladesh:"BD",pakistan:"PK",srilanka:"LK",
      "sri-lanka":"LK",indonesia:"ID","timor-leste":"TL",greece:"GR",cyprus:"CY",
      albania:"AL","south-africa":"ZA",namibia:"NA",somalia:"SO",djibouti:"DJ",
      ethiopia:"ET",kenya:"KE",netherlands:"NL",belgium:"BE",suriname:"SR",
      iran:"IR","united-arab-emirates":"AE",uae:"AE","saudi-arabia":"SA",
      andorra:"AD",spain:"ES",france:"FR",haiti:"HT",canada:"CA",
      "united-states":"US",usa:"US",australia:"AU","new-zealand":"NZ",
      japan:"JP",china:"CN",singapore:"SG",malaysia:"MY",turkey:"TR",
      germany:"DE",austria:"AT",switzerland:"CH",brazil:"BR",portugal:"PT",
      mexico:"MX",argentina:"AR","united-kingdom":"GB",uk:"GB"
    };
    var code = "";
    Object.keys(aliases).some(function (slug) {
      if (new RegExp("(?:^|/|-)"+slug+"(?:/|-|$)").test(path)) { code = aliases[slug]; return true; }
      return false;
    });
    if (!code) {
      try {
        var locale = String(localStorage.getItem(COUNTRY_KEY) || navigator.language || "");
        var match = locale.match(/[-_]([A-Za-z]{2})$/); if (match) code = match[1].toUpperCase();
      } catch (e) {}
    }
    var culture = {
      IN:"south-asia",NP:"south-asia",BD:"south-asia",PK:"south-asia",LK:"south-asia",
      AE:"gulf",SA:"gulf",IR:"persian",ET:"horn",DJ:"horn",SO:"horn",KE:"east-africa",
      ZA:"southern-africa",NA:"southern-africa",ID:"southeast-asia",TL:"southeast-asia",
      MY:"southeast-asia",SG:"southeast-asia",JP:"japan",CN:"east-asia",
      GR:"mediterranean",CY:"mediterranean",AL:"balkans",ES:"mediterranean",
      FR:"western-europe",NL:"western-europe",BE:"western-europe",DE:"western-europe",
      AT:"western-europe",CH:"western-europe",AD:"mediterranean",SR:"caribbean",
      HT:"caribbean",BR:"latin-america",MX:"latin-america",AR:"latin-america"
    };
    if (code) document.documentElement.setAttribute("data-country", code);
    document.documentElement.setAttribute("data-culture", culture[code] || "global");
  })();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
