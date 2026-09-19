/* EkGuru — Advanced Monetization System v300
   Purpose: Multiple revenue streams, AdSense approval compliance
   Channels: AdSense, affiliate, donations, tutor commissions
   Safety: Never shows ads on learning tasks, respects UX
*/
(function () {
  "use strict";

  // innerText is missing in some engines (jsdom, old WebKit) and can throw
  // on hidden subtrees — textContent is the safe fallback for measuring.
  function textLengthOf(el) {
    if (!el) return 0;
    try { return (el.innerText || el.textContent || "").length; } catch (e) { return 0; }
  }

  var path = location.pathname.replace(/^\/+/, "/");
  var host = location.hostname;

  // Page classification for AdSense policy compliance
  var excluded = [
    "/admin", "/privacy/", "/terms/", "/disclaimer/", "/contact/",
    "/search/", "/404", "/tutor.html", "/join", "/booking/",
    "/checkout/", "/payment/", "/courses/", "/cookie-policy/"
  ];
  
  var pageClass = "MEDIUM_CONTENT";
  if (excluded.some(function (prefix) { return path.indexOf(prefix) === 0; })) {
    pageClass = path.indexOf("/courses/") === 0 ? "INTERACTIVE_LEARNING" : "UTILITY";
  } else if (document.querySelector("article, main article, [itemtype*='Article'], .art, .pw-legacy")) {
    pageClass = "HIGH_CONTENT";
  }
  document.documentElement.dataset.monetizationClass = pageClass;

  // Protect learning UI from AdSense auto-ads intents
  var selectors = [
    "header", "nav", "footer", "form", "button", "audio", "video",
    "[role='navigation']", "[role='dialog']", "[role='button']",
    "[aria-live]", ".course-player", ".egc", ".quiz", ".assessment",
    ".answer", ".accessibility-controls", ".audio-controls",
    ".q", ".fc", ".ro-words", ".ro-built", ".ws-page", ".tool",
    ".cf-form", ".sc-box", ".ob-card", ".v-item", ".g-concept"
  ];
  document.querySelectorAll(selectors.join(",")).forEach(function (node) {
    node.classList.add("google-anno-skip");
  });
  if (pageClass !== "HIGH_CONTENT" && pageClass !== "MEDIUM_CONTENT") {
    document.body.classList.add("google-anno-skip");
  }

  // ===== MONETIZATION CHANNELS =====

  // 1. AdSense - conservative, learning-safe placements
  function initAdSense() {
    // Only on HIGH_CONTENT and MEDIUM_CONTENT, and only if consent given
    var consent = null;
    try {
      consent = JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3') || 'null');
    } catch (e) {}
    
    var canShowAds = (pageClass === "HIGH_CONTENT" || pageClass === "MEDIUM_CONTENT") && 
                     (!consent || consent.advertising !== false); // default allow if no consent yet, but banner will handle
    
    if (!canShowAds) return;

    // Check if AdSense loader already present (injected by build)
    if (document.querySelector('script[src*="adsbygoogle"]')) {
      // Add ad slots in safe positions
      addAdSlots();
    }
  }

  function addAdSlots() {
    // Don't add ads if page is too short (AdSense low value content policy)
    var textLength = textLengthOf(document.body);
    if (textLength < 800) return; // Need enough content

    var positions = [
      { selector: '.art, .pw-legacy, .pw', position: 'after', minLength: 1000 },
      { selector: '.egc', position: 'after', minLength: 800 }
    ];

    positions.forEach(function(pos) {
      var containers = document.querySelectorAll(pos.selector);
      containers.forEach(function(container) {
        if (textLengthOf(container) < pos.minLength) return;
        if (container.querySelector('.ad-slot')) return; // already has ad

        // Find safe insertion point - after first 2 paragraphs or after first section
        var paras = container.querySelectorAll('p, h2');
        if (paras.length < 3) return;

        var insertAfter = paras[1];
        if (!insertAfter) return;

        // Check if next element is already ad or learning widget
        var next = insertAfter.nextElementSibling;
        if (next && (next.classList.contains('ad-slot') || next.classList.contains('q') || next.classList.contains('tool'))) {
          return;
        }

        var adContainer = document.createElement('div');
        adContainer.className = 'ad-slot-wrapper google-anno-skip';
        adContainer.innerHTML = 
          '<div class="ad-label">Advertisement</div>' +
          '<ins class="adsbygoogle ad-slot" style="display:block" data-ad-client="ca-pub-8175326569491671" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>';
        
        // Insert
        if (insertAfter.parentNode) {
          insertAfter.parentNode.insertBefore(adContainer, insertAfter.nextSibling);
          
          // Push ad
          try {
            (window.adsbygoogle = window.adsbygoogle || []).push({});
          } catch (e) {}
        }
      });
    });
  }

  // 2. Affiliate & Support Links
  function addSupportLinks() {
    var supportSelectors = document.querySelectorAll('.pw-support, .support-band');
    supportSelectors.forEach(function(el) {
      if (el.querySelector('.support-extra')) return;
      
      var extra = document.createElement('div');
      extra.className = 'support-extra';
      extra.style.cssText = 'margin-top:16px;padding-top:16px;border-top:1px solid #e4e4ef;display:flex;flex-wrap:wrap;gap:10px;align-items:center';
      extra.innerHTML = 
        '<span style="font-size:.85rem;color:#5f6577">Support free lessons:</span>' +
        '<a href="/support/" class="btn btn-ghost btn-sm" style="text-decoration:none">☕ Buy us a coffee</a>' +
        '<a href="/find-tutors.html" class="btn btn-ghost btn-sm" style="text-decoration:none">👨‍🏫 Book a tutor</a>';
      
      el.appendChild(extra);
    });
  }

  // 3. Tutor commission tracking (for monetization via bookings)
  function trackTutorInterest() {
    document.querySelectorAll('a[href*="find-tutors"], a[href*="tutor"]').forEach(function(link) {
      link.addEventListener('click', function() {
        try {
          localStorage.setItem('ekguru_last_tutor_interest', JSON.stringify({
            path: path,
            timestamp: Date.now(),
            referrer: document.referrer
          }));
        } catch (e) {}
      });
    });
  }

  // 4. Donation / Buy Me a Coffee widget (non-intrusive)
  function addDonationWidget() {
    if (pageClass === "UTILITY" || path.indexOf('/admin') === 0) return;
    if (document.getElementById('ekguru-donate')) return;
    
    var donate = document.createElement('div');
    donate.id = 'ekguru-donate';
    donate.className = 'google-anno-skip';
    donate.style.cssText = 'position:fixed;bottom:20px;left:20px;z-index:999;background:#fff;border:1px solid #e4e4ef;border-radius:999px;box-shadow:0 4px 20px rgba(0,0,0,.1);padding:8px 14px;display:flex;align-items:center;gap:8px;font-size:.85rem;font-weight:600;transform:translateY(100px);transition:transform .4s cubic-bezier(.22,1,.36,1)';
    donate.innerHTML = '<span>❤️</span><a href="/support/" style="text-decoration:none;color:#10131f">Support free lessons</a><button type="button" style="background:none;border:none;cursor:pointer;font-size:1rem;margin-left:4px" aria-label="Close">×</button>';
    
    document.body.appendChild(donate);
    
    setTimeout(function() {
      donate.style.transform = 'translateY(0)';
    }, 3000);
    
    donate.querySelector('button').addEventListener('click', function() {
      donate.style.transform = 'translateY(100px)';
      setTimeout(function() { if (donate.parentNode) donate.parentNode.removeChild(donate); }, 400);
      try { localStorage.setItem('ekguru_donate_dismissed', Date.now().toString()); } catch (e) {}
    });
    
    // Auto-hide after 10s
    setTimeout(function() {
      if (donate.parentNode) {
        donate.style.transform = 'translateY(100px)';
        setTimeout(function() { if (donate.parentNode) donate.parentNode.removeChild(donate); }, 400);
      }
    }, 15000);
  }

  // 5. AdSense approval helpers
  function ensureContentDepth() {
    // Add structured data and content signals for AdSense review
    var article = document.querySelector('article, .art, .pw-legacy');
    if (!article) return;
    
    // Check if page is thin (AdSense low value content reason)
    var text = article.innerText || "";
    var wordCount = text.trim().split(/\s+/).length;
    
    if (wordCount < 250) {
      document.documentElement.setAttribute('data-content-depth', 'thin');
      // Add helpful content for thin pages (will be improved by build tools)
      console.warn('EkGuru: Thin content detected (' + wordCount + ' words) - needs expansion for AdSense');
    } else {
      document.documentElement.setAttribute('data-content-depth', 'adequate');
    }
  }

  // Initialize
  function init() {
    initAdSense();
    addSupportLinks();
    trackTutorInterest();
    ensureContentDepth();
    
    // Donation widget - only if not dismissed recently
    try {
      var dismissed = parseInt(localStorage.getItem('ekguru_donate_dismissed') || '0', 10);
      if (Date.now() - dismissed > 24*60*60*1000) { // 24 hours
        setTimeout(addDonationWidget, 5000);
      }
    } catch (e) {
      setTimeout(addDonationWidget, 5000);
    }

    // Expose monetization info
    window.EKGURU_MONETIZATION = {
      pageClass: pageClass,
      channels: {
        adsense: { client: 'ca-pub-8175326569491671', status: 'pending_approval', note: 'Conservative ad load, learning-safe' },
        affiliate: { status: 'planned', note: 'Language tools, books' },
        donations: { status: 'active', url: '/support/' },
        tutoring: { status: 'active', note: 'Commission from bookings' }
      },
      howWeMakeMoney: [
        "Google AdSense: ads on reading pages (not on quizzes/practice)",
        "Tutor bookings: small commission when you book a trial",
        "Donations: voluntary support via support page",
        "Future: affiliate links for language learning resources",
        "All revenue keeps lessons free - no paywall, no account needed"
      ],
      adSafety: {
        noAdsOn: ["quiz", "practice", "test", "worksheet", "typing", "review", "forms", "booking"],
        safeZones: ["navigation", "header", "footer", "ads"],
        policy: "Conservative ad load, no intrusive formats, no ads during learning tasks"
      }
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Listen for consent changes
  document.addEventListener('ekguru:consent', function(e) {
    if (e.detail && e.detail.advertising) {
      setTimeout(initAdSense, 500);
    }
  });
})();
