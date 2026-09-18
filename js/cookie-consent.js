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

  // Cookie categories explained
  var COOKIE_INFO = {
    necessary: {
      name: "Necessary",
      desc: "Essential for site to work: session, security, load balancing. No consent needed.",
      examples: "session_id, csrf_token, preferences",
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
      desc: "Helps us improve: which pages help learners most, where people get stuck. No personal data.",
      examples: "page views, search queries (anonymous)",
      required: false
    },
    advertising: {
      name: "Advertising",
      desc: "Supports free lessons: Google AdSense shows relevant ads. Personalized ads only with your consent.",
      examples: "Google AdSense cookies, ad personalization",
      required: false
    }
  };

  function readConsent() {
    try {
      var raw = localStorage.getItem(CONSENT_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  function writeConsent(consent) {
    try {
      localStorage.setItem(CONSENT_KEY, JSON.stringify(consent));
      localStorage.setItem(CONSENT_DATE_KEY, new Date().toISOString());
    } catch (e) {}
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
  }

  function defaultConsent() {
    return {
      necessary: true,
      functional: true,
      analytics: false,
      advertising: false,
      timestamp: Date.now()
    };
  }

  function hasConsent() {
    var c = readConsent();
    return !!(c && c.timestamp);
  }

  function createBanner() {
    if (document.getElementById('ekguru-consent')) return;
    
    var banner = document.createElement('div');
    banner.id = 'ekguru-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.setAttribute('aria-live', 'polite');
    
    var isSmall = window.innerWidth < 600;
    
    banner.innerHTML = 
      '<div class="consent-in">' +
        '<div class="consent-text">' +
          '<b>🍪 We use cookies to make learning better</b><br>' +
          '<span style="font-size:.88em">Essential cookies keep progress on your device. ' +
          'With your permission, we use analytics to improve lessons and advertising to keep everything free. ' +
          'Your data never leaves your device except for ads (Google) when you allow. ' +
          '<a href="/cookie-policy/" target="_blank">Learn how we use cookies</a> • ' +
          '<a href="/privacy/" target="_blank">Privacy policy</a></span>' +
          '<details style="margin-top:10px"><summary style="cursor:pointer;font-weight:700;font-size:.85em">⚙️ Cookie details</summary>' +
            '<div style="margin-top:10px;display:grid;gap:8px;font-size:.84em">' +
              '<div><b>🔒 Necessary (always on):</b> ' + COOKIE_INFO.necessary.desc + '<br><small>Examples: ' + COOKIE_INFO.necessary.examples + '</small></div>' +
              '<div><b>⚙️ Functional:</b> ' + COOKIE_INFO.functional.desc + '<br><small>Examples: ' + COOKIE_INFO.functional.examples + '</small></div>' +
              '<div><b>📊 Analytics:</b> ' + COOKIE_INFO.analytics.desc + '<br><small>Examples: ' + COOKIE_INFO.analytics.examples + '</small></div>' +
              '<div><b>💰 Advertising:</b> ' + COOKIE_INFO.advertising.desc + '<br><small>Examples: ' + COOKIE_INFO.advertising.examples + '</small></div>' +
            '</div>' +
          '</details>' +
        '</div>' +
        '<div class="consent-actions">' +
          '<button type="button" class="consent-btn consent-accept" id="consent-accept-all">✓ Accept all</button>' +
          '<button type="button" class="consent-btn consent-reject" id="consent-reject">✕ Only essential</button>' +
          '<button type="button" class="consent-settings" id="consent-customize">Customize</button>' +
        '</div>' +
      '</div>' +
      '<div id="consent-custom" style="display:none;max-width:1160px;margin:16px auto 0;padding:16px;border:1px solid #e4e4ef;border-radius:12px;background:#f8f7fd">' +
        '<h3 style="margin:0 0 12px;font-size:1rem">Customize cookies</h3>' +
        '<div style="display:grid;gap:12px">' +
          '<label style="display:flex;gap:10px;align-items:start"><input type="checkbox" checked disabled> <span><b>Necessary</b> — site cannot work without these</span></label>' +
          '<label style="display:flex;gap:10px;align-items:start"><input type="checkbox" id="cc-functional" checked> <span><b>Functional</b> — remembers progress, language, offline saves</span></label>' +
          '<label style="display:flex;gap:10px;align-items:start"><input type="checkbox" id="cc-analytics"> <span><b>Analytics</b> — helps us improve lessons (anonymous)</span></label>' +
          '<label style="display:flex;gap:10px;align-items:start"><input type="checkbox" id="cc-advertising"> <span><b>Advertising</b> — keeps lessons free via Google AdSense</span></label>' +
        '</div>' +
        '<div style="margin-top:16px;display:flex;gap:10px"><button type="button" class="consent-btn consent-accept" id="consent-save-custom">Save preferences</button><button type="button" class="consent-btn consent-reject" id="consent-cancel-custom">Cancel</button></div>' +
      '</div>';

    document.body.appendChild(banner);
    
    // Animate in
    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        banner.classList.add('show');
      });
    });

    // Handlers
    banner.querySelector('#consent-accept-all').addEventListener('click', function() {
      writeConsent({ necessary: true, functional: true, analytics: true, advertising: true, timestamp: Date.now() });
      banner.classList.remove('show');
      setTimeout(function() { if (banner.parentNode) banner.parentNode.removeChild(banner); }, 400);
    });

    banner.querySelector('#consent-reject').addEventListener('click', function() {
      writeConsent({ necessary: true, functional: true, analytics: false, advertising: false, timestamp: Date.now() });
      banner.classList.remove('show');
      setTimeout(function() { if (banner.parentNode) banner.parentNode.removeChild(banner); }, 400);
    });

    banner.querySelector('#consent-customize').addEventListener('click', function() {
      var custom = document.getElementById('consent-custom');
      custom.style.display = custom.style.display === 'none' ? 'block' : 'none';
    });

    banner.querySelector('#consent-save-custom').addEventListener('click', function() {
      var func = document.getElementById('cc-functional').checked;
      var anal = document.getElementById('cc-analytics').checked;
      var adv = document.getElementById('cc-advertising').checked;
      writeConsent({ necessary: true, functional: func, analytics: anal, advertising: adv, timestamp: Date.now() });
      banner.classList.remove('show');
      setTimeout(function() { if (banner.parentNode) banner.parentNode.removeChild(banner); }, 400);
    });

    banner.querySelector('#consent-cancel-custom').addEventListener('click', function() {
      document.getElementById('consent-custom').style.display = 'none';
    });
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
    
    var consent = readConsent();
    if (consent) {
      writeConsent(consent); // re-apply
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
      info: COOKIE_INFO,
      // How cookies are used - for cookie-policy page
      usage: {
        essential: [
          "Keep you logged in (no account system, but progress tracking)",
          "Security: prevent CSRF attacks",
          "Remember cookie consent choice itself"
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
          "Anonymous page views (which lessons are popular)",
          "Search queries (what learners look for)",
          "No personal data collected, no IP tracking",
          "Helps us improve content depth for AdSense approval"
        ],
        advertising: [
          "Google AdSense: shows ads to keep lessons free",
          "Ad personalization only if you consent",
          "Ad measurement: which ads support the site",
          "No ad on learning tasks (quiz, practice, typing)",
          "Safe zones: navigation, forms, course player excluded"
        ],
        howToUse: [
          "Essential: site won't work without - always on",
          "Functional: enables progress tracking, offline mode - recommended",
          "Analytics: helps us create better lessons - optional but helpful",
          "Advertising: keeps site free, supports creators - optional",
          "You can change anytime via footer link or cookie policy page"
        ],
        monetization: [
          "Google AdSense: main revenue - conservative ad load",
          "Affiliate links: language learning tools (future)",
          "Donations: Buy Me a Coffee, support page",
          "Tutor bookings: commission from trial lessons",
          "All monetization respects learning flow - no ads during quizzes"
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
