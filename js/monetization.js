/* EkGuru — release-safe funding UI
   Advertising and affiliates are globally disabled in this release.
   The only active funding route is the optional Razorpay-hosted support link.
*/
(function () {
  "use strict";

  var path = location.pathname.replace(/^\/+/, "/");
  var host = location.hostname;

  // Global release gate. Page eligibility is not authorization to load ads.
  // Keep false until a Google-certified CMP/TCF path and account-side site
  // status have both been verified in production.
  var ADS_RUNTIME_ENABLED = false;

  // Page classification for AdSense policy compliance
  var excluded = [
    "/admin", "/privacy/", "/terms/", "/disclaimer/", "/contact/",
    "/search/", "/404", "/tutor.html", "/join", "/booking/",
    "/checkout/", "/payment/", "/courses/", "/cookie-policy/"
  ];
  
  var declaredClass = document.documentElement.getAttribute("data-ad-class");
  var pageClass = declaredClass || "MEDIUM_CONTENT";
  if (excluded.some(function (prefix) { return path.indexOf(prefix) === 0; })) {
    pageClass = path.indexOf("/courses/") === 0 ? "INTERACTIVE_LEARNING" : "UTILITY";
  } else if (!declaredClass && document.querySelector("article, main article, [itemtype*='Article'], .art, .pw-legacy")) {
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
    // Fail closed globally. Consent is necessary but not sufficient: this
    // release also requires the certified CMP and account-side gate.
    if (!ADS_RUNTIME_ENABLED) return;
    // Only on HIGH_CONTENT and MEDIUM_CONTENT, and only if consent given
    var consent = null;
    try {
      consent = JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3') || 'null');
    } catch (e) {}
    
    var canShowAds = (pageClass === "HIGH_CONTENT" || pageClass === "MEDIUM_CONTENT") &&
                     (consent && consent.advertising === true); // default deny until explicit advertising consent
    
    if (!canShowAds) return;

    // Check if AdSense loader already present (injected by build)
    if (document.querySelector('script[src*="adsbygoogle"]')) {
      // Add ad slots in safe positions
      addAdSlots();
    }
  }

  function addAdSlots() {
    // Deliberately empty. A future release must use individually reviewed,
    // pre-marked placements; word count must never create ad units dynamically.
  }

  // Support-toast + support-link copy in the page's own language.
  // Page language (html lang) decides; English is the fallback. Short
  // reusable CTA strings only — never lesson content.
  function pageLang() {
    try {
      var l = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
      return l.split(/[-_]/)[0];
    } catch (e) { return "en"; }
  }

  var TOAST_COPY = {
    en: { title: "Support EkGuru", body: "Help keep free learning running.", cta: "Support EkGuru", close: "Dismiss", linksLabel: "Support free lessons:", coffee: "Buy us a coffee", tutor: "Book a tutor" },
    hi: { title: "EkGuru का समर्थन करें", body: "मुफ़्त पढ़ाई जारी रखने में मदद करें।", cta: "समर्थन करें", close: "बंद करें", linksLabel: "मुफ़्त पाठों का समर्थन करें:", coffee: "हमें एक कॉफ़ी पिलाएँ", tutor: "ट्यूटर बुक करें" },
    es: { title: "Apoya a EkGuru", body: "Ayuda a mantener gratis el aprendizaje.", cta: "Apoyar a EkGuru", close: "Descartar", linksLabel: "Apoya las lecciones gratis:", coffee: "Invítanos a un café", tutor: "Reserva un tutor" },
    fr: { title: "Soutenez EkGuru", body: "Aidez à garder l'apprentissage gratuit.", cta: "Soutenir EkGuru", close: "Fermer", linksLabel: "Soutenez les leçons gratuites :", coffee: "Offrez-nous un café", tutor: "Réserver un tuteur" },
    de: { title: "EkGuru unterstützen", body: "Hilf, das Lernen kostenlos zu halten.", cta: "EkGuru unterstützen", close: "Schließen", linksLabel: "Unterstütze kostenlose Lektionen:", coffee: "Gib uns einen Kaffee aus", tutor: "Tutor buchen" },
    pt: { title: "Apoie a EkGuru", body: "Ajude a manter o aprendizado grátis.", cta: "Apoiar a EkGuru", close: "Dispensar", linksLabel: "Apoie as lições grátis:", coffee: "Pague um café para nós", tutor: "Reservar um tutor" },
    ja: { title: "EkGuruを応援する", body: "無料学習の継続にご協力ください。", cta: "応援する", close: "閉じる", linksLabel: "無料レッスンを応援:", coffee: "コーヒーをおごる", tutor: "講師を予約する" },
    ar: { title: "ادعم EkGuru", body: "ساعد في إبقاء التعلّم مجانيًا.", cta: "ادعم EkGuru", close: "إغلاق", linksLabel: "ادعم الدروس المجانية:", coffee: "اشترِ لنا قهوة", tutor: "احجز معلّمًا" },
    bn: { title: "EkGuru-কে সমর্থন করুন", body: "বিনামূল্যে শেখা চালিয়ে যেতে সাহায্য করুন।", cta: "সমর্থন করুন", close: "বন্ধ করুন", linksLabel: "বিনামূল্যের পাঠ সমর্থন করুন:", coffee: "আমাদের একটি কফি খাওয়ান", tutor: "টিউটর বুক করুন" },
    ur: { title: "EkGuru کی حمایت کریں", body: "مفت سیکھنے کو جاری رکھنے میں مدد کریں۔", cta: "حمایت کریں", close: "بند کریں", linksLabel: "مفت اسباق کی حمایت کریں:", coffee: "ہمیں ایک کافی پلائیں", tutor: "ٹیوٹر بک کریں" },
    ta: { title: "EkGuru-வை ஆதரியுங்கள்", body: "இலவச கற்றல் தொடர உதவுங்கள்.", cta: "ஆதரியுங்கள்", close: "மூடுக", linksLabel: "இலவச பாடங்களை ஆதரியுங்கள்:", coffee: "எங்களுக்கு ஒரு காபி வாங்கித் தாருங்கள்", tutor: "ஆசிரியரை முன்பதிவு செய்க" },
    te: { title: "EkGuru‌కు మద్దతు ఇవ్వండి", body: "ఉచిత అభ్యాసం కొనసాగడానికి సహాయపడండి.", cta: "మద్దతు ఇవ్వండి", close: "మూసివేయి", linksLabel: "ఉచిత పాఠాలకు మద్దతు ఇవ్వండి:", coffee: "మాకు ఒక కాఫీ ఇవ్వండి", tutor: "ట్యూటర్‌ను బుక్ చేయండి" },
    mr: { title: "EkGuru ला पाठिंबा द्या", body: "मोफत शिक्षण सुरू ठेवण्यास मदत करा.", cta: "पाठिंबा द्या", close: "बंद करा", linksLabel: "मोफत धड्यांना पाठिंबा द्या:", coffee: "आम्हाला एक कॉफी द्या", tutor: "शिक्षक बुक करा" },
    gu: { title: "EkGuru ને ટેકો આપો", body: "મફત શિક્ષણ ચાલુ રાખવામાં મદદ કરો.", cta: "ટેકો આપો", close: "બંધ કરો", linksLabel: "મફત પાઠોને ટેકો આપો:", coffee: "અમને એક કોફી પીવડાવો", tutor: "ટ્યૂટર બુક કરો" },
    kn: { title: "EkGuru ಗೆ ಬೆಂಬಲ ನೀಡಿ", body: "ಉಚಿತ ಕಲಿಕೆ ಮುಂದುವರಿಯಲು ಸಹಾಯ ಮಾಡಿ.", cta: "ಬೆಂಬಲ ನೀಡಿ", close: "ಮುಚ್ಚಿ", linksLabel: "ಉಚಿತ ಪಾಠಗಳಿಗೆ ಬೆಂಬಲ ನೀಡಿ:", coffee: "ನಮಗೆ ಒಂದು ಕಾಫಿ ಕೊಡಿ", tutor: "ಶಿಕ್ಷಕರನ್ನು ಬುಕ್ ಮಾಡಿ" },
    ml: { title: "EkGuru-വിനെ പിന്തുണയ്ക്കൂ", body: "സൗജന്യ പഠനം തുടരാൻ സഹായിക്കൂ.", cta: "പിന്തുണയ്ക്കൂ", close: "അടയ്ക്കൂ", linksLabel: "സൗജന്യ പാഠങ്ങളെ പിന്തുണയ്ക്കൂ:", coffee: "ഞങ്ങൾക്ക് ഒരു കാപ്പി വാങ്ങി തരൂ", tutor: "ട്യൂട്ടറെ ബുക്ക് ചെയ്യൂ" },
    pa: { title: "EkGuru ਦਾ ਸਮਰਥਨ ਕਰੋ", body: "ਮੁਫ਼ਤ ਸਿੱਖਿਆ ਜਾਰੀ ਰੱਖਣ ਵਿੱਚ ਮਦਦ ਕਰੋ।", cta: "ਸਮਰਥਨ ਕਰੋ", close: "ਬੰਦ ਕਰੋ", linksLabel: "ਮੁਫ਼ਤ ਪਾਠਾਂ ਦਾ ਸਮਰਥਨ ਕਰੋ:", coffee: "ਸਾਨੂੰ ਇੱਕ ਕਾਫ਼ੀ ਪਿਆਓ", tutor: "ਟਿਊਟਰ ਬੁੱਕ ਕਰੋ" },
    it: { title: "Sostieni EkGuru", body: "Aiutaci a mantenere gratuito l'apprendimento.", cta: "Sostieni EkGuru", close: "Chiudi", linksLabel: "Sostieni le lezioni gratuite:", coffee: "Offrici un caffè", tutor: "Prenota un tutor" },
    ru: { title: "Поддержите EkGuru", body: "Помогите сохранить обучение бесплатным.", cta: "Поддержать EkGuru", close: "Закрыть", linksLabel: "Поддержите бесплатные уроки:", coffee: "Угостите нас кофе", tutor: "Записаться к репетитору" },
    ko: { title: "EkGuru 후원하기", body: "무료 학습이 계속되도록 도와주세요.", cta: "후원하기", close: "닫기", linksLabel: "무료 수업을 후원하세요:", coffee: "커피 한 잔 사주기", tutor: "튜터 예약하기" },
    zh: { title: "支持 EkGuru", body: "帮助我们保持免费学习。", cta: "支持 EkGuru", close: "关闭", linksLabel: "支持免费课程：", coffee: "请我们喝杯咖啡", tutor: "预约导师" },
    vi: { title: "Ủng hộ EkGuru", body: "Giúp duy trì việc học miễn phí.", cta: "Ủng hộ EkGuru", close: "Đóng", linksLabel: "Ủng hộ các bài học miễn phí:", coffee: "Mời chúng tôi một ly cà phê", tutor: "Đặt gia sư" },
    tr: { title: "EkGuru'yu destekle", body: "Ücretsiz öğrenmenin sürmesine yardım et.", cta: "EkGuru'yu destekle", close: "Kapat", linksLabel: "Ücretsiz dersleri destekle:", coffee: "Bize bir kahve ısmarla", tutor: "Öğretmen ayırt" },
    id: { title: "Dukung EkGuru", body: "Bantu agar pembelajaran gratis terus berjalan.", cta: "Dukung EkGuru", close: "Tutup", linksLabel: "Dukung pelajaran gratis:", coffee: "Traktir kami kopi", tutor: "Pesan tutor" },
    pl: { title: "Wesprzyj EkGuru", body: "Pomóż utrzymać darmową naukę.", cta: "Wesprzyj EkGuru", close: "Zamknij", linksLabel: "Wesprzyj darmowe lekcje:", coffee: "Postaw nam kawę", tutor: "Zarezerwuj korepetytora" },
    nl: { title: "Steun EkGuru", body: "Help gratis leren in stand te houden.", cta: "Steun EkGuru", close: "Sluiten", linksLabel: "Steun gratis lessen:", coffee: "Trakteer ons op koffie", tutor: "Boek een tutor" }
  };

  function toastCopy() {
    return TOAST_COPY[pageLang()] || TOAST_COPY.en;
  }

  // 2. Affiliate & Support Links
  function addSupportLinks() {
    var copy = toastCopy();
    var supportSelectors = document.querySelectorAll('.pw-support, .support-band');
    supportSelectors.forEach(function(el) {
      if (el.querySelector('.support-extra')) return;

      var extra = document.createElement('div');
      extra.className = 'support-extra';
      extra.style.cssText = 'margin-top:16px;padding-top:16px;border-top:1px solid #e4e4ef;display:flex;flex-wrap:wrap;gap:10px;align-items:center';
      extra.innerHTML =
        '<span style="font-size:.85rem;color:#5f6577"></span>' +
        '<a href="/support/" class="btn btn-ghost btn-sm" style="text-decoration:none"></a>' +
        '<a href="/find-tutors.html" class="btn btn-ghost btn-sm" style="text-decoration:none"></a>';
      var parts = extra.querySelectorAll('span, a');
      parts[0].textContent = copy.linksLabel;
      parts[1].textContent = copy.cta;
      parts[2].textContent = '👨‍🏫 ' + copy.tutor;

      el.appendChild(extra);
    });
  }

  // 4. Support EkGuru toast (v3 hardening, Gate 18) — ONE shared toast.
  // Bottom-left. First show ~60s after load, visible ~7s, repeats ~60s
  // later. Single chained setTimeout: no polling, no 1s timers, no
  // duplicate DOM, no duplicate timers. Never on /support/. Hidden while
  // search, the mobile nav, consent or a payment modal is on screen.
  // No aria-live: it must not announce itself every minute (Gate 26).
  var TOAST_FIRST_MS = 60000;
  var TOAST_VISIBLE_MS = 7000;
  var TOAST_REPEAT_MS = 60000;

  function toastSuppressed() {
    if (document.hidden) return true;
    if (document.body.classList.contains("nav-open")) return true;
    if (document.querySelector(".hdr .nav.open")) return true;
    /* search dropdown open (home hero) or search input focused */
    if (document.querySelector(".xp-searchbox.is-open")) return true;
    var sugg = document.getElementById("home-sugg");
    if (sugg && !sugg.hidden) return true;
    var ae = document.activeElement;
    if (ae && (ae.id === "home-q" || ae.id === "q")) return true;
    /* consent banner or a payment/modal dialog visible */
    var consent = document.getElementById("ekguru-consent");
    if (consent && consent.offsetParent !== null) return true;
    if (document.querySelector(".ekg-checkout-modal-overlay, #ekguru-mock-checkout-modal")) return true;
    var dlg = document.querySelector('[role="dialog"]');
    if (dlg && dlg.offsetParent !== null && dlg.id !== "ekguru-support-toast") return true;
    return false;
  }

  function startSupportToast() {
    /* Exclusions: the support page itself, admin, and utility/legal flows. */
    if (path.indexOf("/support") === 0) return;
    if (path.indexOf("/admin") === 0) return;
    if (pageClass === "UTILITY") return;
    /* Duplicate-load guard: the file must never schedule twice. */
    if (window.__EKGURU_SUPPORT_TOAST__) return;
    window.__EKGURU_SUPPORT_TOAST__ = true;
    /* QA hook only: window.__EKGURU_TOAST_TIMING__ = {first, visible, repeat} */
    try {
      var ov = window.__EKGURU_TOAST_TIMING__;
      if (ov && typeof ov === "object") {
        if (+ov.first > 0) TOAST_FIRST_MS = +ov.first;
        if (+ov.visible > 0) TOAST_VISIBLE_MS = +ov.visible;
        if (+ov.repeat > 0) TOAST_REPEAT_MS = +ov.repeat;
      }
    } catch (e) {}

    var copy = toastCopy();
    var lang = pageLang();
    var reduced = false;
    try {
      reduced = !!(window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    } catch (e2) {}

    var wrap = document.createElement("div");
    wrap.id = "ekguru-support-toast-wrap";
    wrap.className = "google-anno-skip";
    wrap.setAttribute("aria-hidden", "false");
    wrap.style.cssText = "position:fixed;left:0;right:0;bottom:0;z-index:90;" +
      "pointer-events:none;padding:0 16px calc(16px + env(safe-area-inset-bottom, 0px));" +
      "padding-left:calc(16px + env(safe-area-inset-left, 0px));";

    var toast = document.createElement("div");
    toast.id = "ekguru-support-toast";
    toast.className = "google-anno-skip";
    toast.style.cssText = "pointer-events:auto;display:flex;align-items:center;gap:12px;" +
      "max-width:min(360px,calc(100vw - 32px));background:#fff;color:#10131f;" +
      "border:1px solid #e4e4ef;border-radius:16px;box-shadow:0 8px 32px rgba(15,18,34,.14);" +
      "padding:12px 12px 12px 16px;font-size:.88rem;line-height:1.45;" +
      "opacity:0;transform:translateY(12px);" +
      (reduced ? "" : "transition:opacity .35s cubic-bezier(.22,1,.36,1),transform .35s cubic-bezier(.22,1,.36,1);") +
      "visibility:hidden;";
    if (document.documentElement.getAttribute("dir") === "rtl" || lang === "ar" || lang === "ur") {
      toast.setAttribute("dir", "rtl");
    }

    var icon = document.createElement("span");
    icon.setAttribute("aria-hidden", "true");
    icon.style.cssText = "flex:none;font-size:1.3rem;";
    icon.textContent = "☕";

    var text = document.createElement("div");
    text.style.cssText = "flex:1 1 auto;min-width:0;";
    var title = document.createElement("div");
    title.style.cssText = "font-weight:800;";
    title.textContent = copy.title;
    var body = document.createElement("div");
    body.style.cssText = "color:#5f6577;font-size:.82rem;";
    body.textContent = copy.body;
    text.appendChild(title);
    text.appendChild(body);

    var cta = document.createElement("a");
    cta.href = "/support/";
    cta.style.cssText = "flex:none;display:inline-flex;align-items:center;min-height:44px;" +
      "padding:8px 14px;border-radius:999px;background:linear-gradient(135deg,#4f32d9,#8b5cf6);" +
      "color:#fff;font-weight:700;font-size:.84rem;text-decoration:none;white-space:nowrap;";
    cta.textContent = copy.cta + " →";

    var close = document.createElement("button");
    close.type = "button";
    close.setAttribute("aria-label", copy.close);
    close.style.cssText = "flex:none;display:grid;place-items:center;width:44px;height:44px;" +
      "margin:-8px -8px -8px 0;background:none;border:0;cursor:pointer;" +
      "font-size:1.25rem;color:#5f6577;border-radius:12px;";
    close.textContent = "×";

    toast.appendChild(icon);
    toast.appendChild(text);
    toast.appendChild(cta);
    toast.appendChild(close);
    wrap.appendChild(toast);
    document.body.appendChild(wrap);

    var hideTimer = null;
    var showTimer = null;

    function show() {
      if (toastSuppressed()) { schedule(TOAST_REPEAT_MS); return; }
      toast.style.visibility = "visible";
      toast.style.opacity = "1";
      toast.style.transform = "translateY(0)";
      hideTimer = setTimeout(hide, TOAST_VISIBLE_MS);
    }

    function hide() {
      if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
      toast.style.opacity = "0";
      toast.style.transform = "translateY(12px)";
      setTimeout(function () { toast.style.visibility = "hidden"; }, reduced ? 0 : 380);
      schedule(TOAST_REPEAT_MS);
    }

    /* Single-chain scheduling: hide() can fire twice for one showing (close
       click + Escape, close + search-open), and each schedule() used to add
       another pending show — orphaning hide timers and doubling the chain
       forever. Clearing the pending show first keeps exactly one chain. */
    function schedule(ms) {
      if (showTimer) { clearTimeout(showTimer); showTimer = null; }
      showTimer = setTimeout(function () { showTimer = null; show(); }, ms);
    }

    /* Manual close hides this showing; the quiet hourly rhythm continues. */
    close.addEventListener("click", function () { hide(); });
    toast.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { hide(); try { close.blur(); } catch (e2) {} }
    });
    /* Search opened while visible: get out of the way at once. */
    document.addEventListener("ekguru:search-open", function () {
      if (toast.style.visibility === "visible") {
        if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
        toast.style.opacity = "0";
        toast.style.transform = "translateY(12px)";
        toast.style.visibility = "hidden";
        schedule(TOAST_REPEAT_MS);
      }
    });
    /* bfcache: never leave a half-visible toast with dead timers. */
    window.addEventListener("pageshow", function () {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(12px)";
      toast.style.visibility = "hidden";
    });

    schedule(TOAST_FIRST_MS);
  }

  // Initialize
  function init() {
    initAdSense();
    // Support toast: quiet 60s rhythm, owned entirely by startSupportToast.
    // The pre-v3 24h-dismiss key is retired; remove it once.
    try { localStorage.removeItem('ekguru_donate_dismissed'); } catch (e) {}
    startSupportToast();

    // Expose monetization info
    window.EKGURU_MONETIZATION = {
      pageClass: pageClass,
      channels: {
        adsense: { status: 'disabled_not_ready_do_not_apply', loaderEnabled: false },
        affiliate: { status: 'disabled_no_approved_identifiers' },
        support: { status: 'active_optional_external_payment_page', url: '/support/' },
        tutoring: { status: 'profile_introductions_only_no_site_payment_or_commission_claim' }
      },
      currentFunding: [
        "Optional one-time support through Razorpay's hosted payment page",
        "No AdSense loader or ad units in this release",
        "No affiliate tracking identifiers in this release",
        "EkGuru does not collect tutor-lesson payments in this release"
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
