/* ==========================================================================
   EkGuru — EXPERIENCE RUNTIME  (v200)
   --------------------------------------------------------------------------
   The behaviour half of css/experience.css. Loaded with `defer` on the
   redesigned pages (home, support, courses, search); every other page in the
   site gets the visual half through the bundled stylesheet and needs nothing
   from this file.

   EVERY FEATURE HERE IS AN ENHANCEMENT
   ------------------------------------
   The page must be complete and readable before this file runs, and must stay
   complete after it fails. That is not a slogan — it is enforced:

     · Nothing is hidden until html.xp-anim exists, and that class is only
       added when JS is running, IntersectionObserver exists and the visitor
       has not asked for reduced motion (css/experience.css §5).
     · A watchdog reveals every hidden block 4s after load even if the observer
       never fired, so a broken browser shows content rather than blank space.
     · Suggestions, hero letters and the language rail all render into
       containers that already hold real content in the HTML. If this file
       never loads, those containers are still correct.

   LANGUAGE AWARENESS
   ------------------
   The palette and motif come from css/experience.css keyed on html[lang]. This
   file adds the parts CSS cannot know: which script to show in the hero, what
   to say in the visitor's own language, and which way the arrow points.
     · the interface language  = html[lang]  (es, fr, de, pt, ja, ar, hi…)
     · the learning language   = html[data-target-lang] or "hi"  (EkGuru
       teaches Hindi, so a French visitor still meets Devanagari letters)

   No network request, no cookie, no storage of anything typed.
   ========================================================================== */
(function (root, doc) {
  "use strict";

  /* Double-load guard: a second copy must not re-run the inits (duplicate
     #home-sugg IDs, double listeners). Same pattern as greeting.js and the
     support toast. EkGuruXP is set synchronously at the end of the first
     evaluation, so a second <script> tag always sees it. */
  if (root.EkGuruXP) return;

  var html = doc.documentElement;

  /* The <script> tag itself, captured while it executes. document.currentScript
     is null by the time a deferred callback runs, and every path built below
     (search suggestions, prefetch) needs the site prefix this file was loaded
     from — the site is served from a sub-path on GitHub Pages, so a hardcoded
     "/" would 404. */
  var SELF = doc.currentScript || null;

  /* ---------- language packs ------------------------------------------- */

  /* Interface language → the short human touches that make a page feel
     written for the reader. Text that exists in js/i18n.js is NOT repeated
     here; this is only the ornament layer. */
  var LANG_COPY = {
    en: { hello: "Namaste", cta: "Start speaking today", hint: "Try “beginner”, “kids” or “conversation”" },
    hi: { hello: "नमस्ते", cta: "आज ही बोलना शुरू करें", hint: "“शुरुआती”, “बच्चे” या “बातचीत” आज़माएँ" },
    es: { hello: "¡Hola!", cta: "Empieza a hablar hoy", hint: "Prueba «principiante», «niños» o «conversación»" },
    fr: { hello: "Bonjour", cta: "Parlez dès aujourd’hui", hint: "Essayez « débutant », « enfants » ou « conversation »" },
    de: { hello: "Hallo", cta: "Sprich noch heute", hint: "Probier „Anfänger“, „Kinder“ oder „Konversation“" },
    pt: { hello: "Olá", cta: "Comece a falar hoje", hint: "Tente “iniciante”, “crianças” ou “conversa”" },
    ja: { hello: "こんにちは", cta: "今日から話しましょう", hint: "「初心者」「子ども」「会話」で試す" },
    ar: { hello: "مرحبا", cta: "ابدأ التحدث اليوم", hint: "جرّب «مبتدئ» أو «أطفال» أو «محادثة»" },
    it: { hello: "Ciao", cta: "Inizia a parlare oggi", hint: "Prova «principiante», «bambini» o «conversazione»" },
    ru: { hello: "Привет", cta: "Начните говорить сегодня", hint: "Попробуйте «новичок», «дети» или «разговор»" },
    nl: { hello: "Hallo", cta: "Begin vandaag met spreken", hint: "Probeer ‘beginner’, ‘kinderen’ of ‘conversatie’" },
    tr: { hello: "Merhaba", cta: "Bugün konuşmaya başla", hint: "“yeni başlayan”, “çocuklar” veya “konuşma” deneyin" },
    id: { hello: "Halo", cta: "Mulai berbicara hari ini", hint: "Coba “pemula”, “anak” atau “percakapan”" },
    bn: { hello: "নমস্কার", cta: "আজই কথা বলা শুরু করুন", hint: "“শিক্ষানবিশ”, “শিশু” বা “আলাপ” চেষ্টা করুন" },
    ta: { hello: "வணக்கம்", cta: "இன்றே பேசத் தொடங்குங்கள்", hint: "“தொடக்கம்”, “குழந்தைகள்” அல்லது “உரையாடல்”" },
    te: { hello: "నమస్కారం", cta: "ఈ రోజే మాట్లాడటం ప్రారంభించండి", hint: "“ప్రారంభ”, “పిల్లలు” లేదా “సంభాషణ” ప్రయత్నించండి" },
    ur: { hello: "السلام علیکم", cta: "آج ہی بولنا شروع کریں", hint: "«ابتدائی»، «بچے» یا «گفتگو» آزمائیں" },
    gu: { hello: "નમસ્તે", cta: "આજે જ બોલવાનું શરૂ કરો", hint: "“શરૂઆત”, “બાળકો” કે “વાતચીત” અજમાવો" },
    kn: { hello: "ನಮಸ್ತೆ", cta: "ಇಂದೇ ಮಾತನಾಡಲು ಪ್ರಾರಂಭಿಸಿ", hint: "“ಆರಂಭಿಕ”, “ಮಕ್ಕಳು” ಅಥವಾ “ಸಂಭಾಷಣೆ” ಪ್ರಯತ್ನಿಸಿ" },
    ml: { hello: "നമസ്തേ", cta: "ഇന്നുതന്നെ സംസാരിക്കാൻ തുടങ്ങൂ", hint: "“തുടക്കക്കാരൻ”, “കുട്ടികൾ” അല്ലെങ്കിൽ “സംഭാഷണം” പരീക്ഷിക്കൂ" },
    mr: { hello: "नमस्ते", cta: "आजच बोलायला सुरुवात करा", hint: "“सुरुवात”, “मुले” किंवा “संभाषण” करून पाहा" },
    pa: { hello: "ਨਮਸਤੇ", cta: "ਅੱਜ ਹੀ ਬੋਲਣਾ ਸ਼ੁਰੂ ਕਰੋ", hint: "“ਸ਼ੁਰੂਆਤੀ”, “ਬੱਚੇ” ਜਾਂ “ਗੱਲਬਾਤ” ਅਜ਼ਮਾਓ" },
    ko: { hello: "나마스테", cta: "오늘부터 말하기 시작하세요", hint: "“초보자”, “어린이”, “회화”를 입력해 보세요" },
    zh: { hello: "你好", cta: "今天就开始说", hint: "试试“初学者”、“儿童”或“会话”" },
    vi: { hello: "Namaste", cta: "Bắt đầu nói ngay hôm nay", hint: "Thử “người mới”, “trẻ em” hoặc “hội thoại”" },
    pl: { hello: "Namaste", cta: "Zacznij mówić już dziś", hint: "Wypróbuj „początkujący”, „dzieci” lub „konwersacja”" }
  };

  /* Learning language → the letters shown in the hero. EkGuru's main course is
     Hindi, so Devanagari is the default; a course page can override it by
     setting <html data-target-lang="ja"> etc. */
  var SCRIPT_LETTERS = {
    hi: ["अ", "आ", "क", "म"],
    mr: ["अ", "आ", "क", "म"],
    bn: ["অ", "আ", "ক", "ম"],
    ta: ["அ", "ஆ", "க", "ம"],
    te: ["అ", "ఆ", "క", "మ"],
    kn: ["ಅ", "ಆ", "ಕ", "ಮ"],
    ml: ["അ", "ആ", "ക", "മ"],
    gu: ["અ", "આ", "ક", "મ"],
    pa: ["ਅ", "ਆ", "ਕ", "ਮ"],
    ur: ["ا", "ب", "ج", "م"],
    ar: ["ا", "ب", "ج", "م"],
    fa: ["ا", "ب", "ج", "م"],
    he: ["א", "ב", "ג", "ם"],
    ru: ["А", "Б", "В", "Г"],
    uk: ["А", "Б", "В", "Г"],
    el: ["Α", "Β", "Γ", "Δ"],
    ja: ["あ", "い", "う", "え"],
    ko: ["가", "나", "다", "라"],
    zh: ["一", "人", "山", "水"],
    th: ["ก", "ข", "ค", "ง"],
    vi: ["A", "Ă", "Â", "B"],
    tr: ["A", "B", "C", "Ç"],
    es: ["A", "B", "C", "Ñ"],
    fr: ["A", "B", "C", "É"],
    de: ["A", "B", "C", "Ö"],
    pt: ["A", "B", "C", "Ã"],
    it: ["A", "B", "C", "È"],
    nl: ["A", "B", "C", "IJ"],
    pl: ["A", "B", "C", "Ł"],
    id: ["A", "B", "C", "D"],
    sw: ["A", "B", "C", "D"]
  };

  var RTL = { ar: 1, he: 1, fa: 1, ur: 1, ps: 1, sd: 1, yi: 1 };

  /* Interface language → the writing system the page moves in. Drives
     html[data-xp-script], which css/experience.css §22 uses to give each
     market its own entrance accent: a Devanagari page settles down from its
     headstroke, an RTL page enters from the right, a CJK page sets on a grid,
     everything else rises. Latin is the stylesheet default, so it is listed
     only for completeness — a missing entry can never leave a block hidden,
     it just gets the default motion. */
  var SCRIPT_FAMILY = {
    hi: "devanagari", mr: "devanagari", ne: "devanagari", sa: "devanagari", pa: "devanagari",
    bn: "devanagari", gu: "devanagari", as: "devanagari", or: "devanagari",
    ar: "rtl", ur: "rtl", fa: "rtl", he: "rtl", ps: "rtl", sd: "rtl", yi: "rtl",
    ja: "cjk", ko: "cjk", zh: "cjk",
    ru: "cyrillic", uk: "cyrillic", bg: "cyrillic", sr: "cyrillic", mk: "cyrillic", be: "cyrillic",
    el: "latin", th: "latin", vi: "latin", tr: "latin", id: "latin", sw: "latin", nl: "latin"
  };

  /* The markets that have a drawn emblem in images/xp/. The list is a whitelist
     on purpose: swapping the src to a file that does not exist would show a
     broken image on a page that was previously fine. */
  var WORLD_ART = { en: 1, hi: 1, es: 1, fr: 1, de: 1, pt: 1, ja: 1, ar: 1, multi: 1 };

  /* Two ways a page can use the artwork:
       data-xp-world="auto"   follow the interface language (the home pages —
                              a visitor who switches to Spanish gets the
                              Spanish emblem, so the drawing never contradicts
                              the text next to it)
       data-xp-world="ja"     this page belongs to one world and keeps it
                              (support/ is about Hindi lessons whoever reads
                              it; courses/ and search/ span every language)
     Neither can lose the emblem: an unknown value is left alone. */

  var lang = String(
    root.EKGURU_LANG || html.getAttribute("lang") || "en"
  ).toLowerCase().split(/[-_]/)[0];

  var target = String(
    html.getAttribute("data-target-lang") || "hi"
  ).toLowerCase().split(/[-_]/)[0];

  var copy = LANG_COPY[lang] || LANG_COPY.en;
  var letters = SCRIPT_LETTERS[target] || SCRIPT_LETTERS.hi;

  html.setAttribute("data-xp-lang", lang);
  html.setAttribute("data-xp-target", target);
  html.setAttribute("data-xp-dir", RTL[lang] ? "rtl" : "ltr");
  html.setAttribute("data-xp-script", SCRIPT_FAMILY[lang] || "latin");

  function reduced() {
    try {
      return root.matchMedia("(prefers-reduced-motion: reduce)").matches;
    } catch (e) {
      return false;
    }
  }

  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) {
    return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel));
  }
  function on(el, ev, fn, opts) {
    if (el && el.addEventListener) el.addEventListener(ev, fn, opts);
  }

  var API = {
    lang: lang,
    targetLanguage: target,
    dir: RTL[lang] ? "rtl" : "ltr",
    copy: copy,
    letters: letters,
    reducedMotion: reduced()
  };

  /* ======================================================================
     1. ENTRANCE MOTION
     ====================================================================== */

  var WATCHDOG = null;

  function revealAll() {
    $$(".reveal, .stagger, .xp-rise, .xp-stagger").forEach(function (el) {
      el.classList.add("in");
      el.classList.add("xp-in");
    });
  }

  function initMotion() {
    if (reduced() || !("IntersectionObserver" in root)) return;

    html.classList.add("xp-anim");

    var targets = $$(".reveal, .stagger, .xp-rise, .xp-stagger");
    if (!targets.length) return;

    if (!("IntersectionObserver" in root)) { revealAll(); return; }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        en.target.classList.add("xp-in");
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

    targets.forEach(function (el) { io.observe(el); });

    /* Anything already on screen at load is revealed immediately — waiting for
       a scroll event on a short page would leave the hero invisible. */
    var above = targets.filter(function (el) {
      var r = el.getBoundingClientRect();
      return r.top < (root.innerHeight || 800) * 0.92;
    });
    above.forEach(function (el) { el.classList.add("in"); el.classList.add("xp-in"); });

    /* The watchdog. If the observer is throttled, blocked, or the tab is
       backgrounded during load, nothing may stay hidden: after 4 seconds
       every block is shown, animation or not. */
    WATCHDOG = root.setTimeout(revealAll, 4000);
    on(root, "pagehide", function () {
      if (WATCHDOG) root.clearTimeout(WATCHDOG);
    });
  }

  /* ======================================================================
     2. SCROLL PROGRESS
     ====================================================================== */

  function initProgress() {
    var bar = doc.createElement("div");
    bar.className = "xp-progress";
    bar.setAttribute("aria-hidden", "true");
    doc.body.appendChild(bar);

    var ticking = false;

    function paint() {
      ticking = false;
      var h = doc.documentElement.scrollHeight - root.innerHeight;
      var pct = h > 0 ? (root.pageYOffset || doc.documentElement.scrollTop) / h : 0;
      bar.style.width = Math.max(0, Math.min(100, pct * 100)) + "%";
    }

    function ask() {
      if (ticking) return;
      ticking = true;
      if (root.requestAnimationFrame) root.requestAnimationFrame(paint);
      else paint();
    }

    on(root, "scroll", ask, { passive: true });
    on(root, "resize", ask);
    paint();
  }

  /* ======================================================================
     3. HERO SCRIPT LETTERS
     ----------------------------------------------------------------------
     The HTML ships the first four letters of the target script. This rotates
     the last tile through the rest of the alphabet every few seconds, so the
     hero slowly teaches the visitor what the writing looks like — the single
     clearest signal that this is a language site and not a template.
     ====================================================================== */

  var ALPHABET = {
    hi: "अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह".split(""),
    bn: "অআইঈউঊএঐওঔকখগঘচছজঝটঠডঢণতথদধনপফবভমযরলশষসহ".split(""),
    ta: "அஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநபமயரலவழளறன".split(""),
    te: "అఆఇఈఉఊఎఏఐఒఓఔకఖగఘచఛజఝటఠడఢణతథదధనపఫబభమయరలవశషసహ".split(""),
    kn: "ಅಆಇಈಉಊಎಏಐಒಓಔಕಖಗಘಚಛಜಝಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಲವಶಷಸಹ".split(""),
    ml: "അആഇഈഉഊഎഏഐഒഓഔകഖഗഘചഛജഝടഠഡഢണതഥദധനപഫബഭമയരലവശഷസഹ".split(""),
    gu: "અઆઇઈઉઊએઐઓઔકખગઘચછજઝટઠડઢણતથદધનપફબભમયરલવશષસહ".split(""),
    pa: "ਅਆਇਈਉਊਏਐਓਔਕਖਗਘਚਛਜਝਟਠਡਢਣਤਥਦਧਨਪਫਬਭਮਯਰਲਵਸਹ".split(""),
    ur: "اببپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنوہیے".split(""),
    ar: "اببپتثجحخدذرزسشصضطظعغفقكلمنهوي".split(""),
    ja: "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん".split(""),
    ko: "가나다라마바사아자차카타파하".split(""),
    zh: "一二三四五六七八九十人山水日月火木金土口目耳手".split(""),
    ru: "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ".split(""),
    el: "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ".split(""),
    th: "กขคงจฉชซญฎฏฐณดตถทธนบปผฝพฟภมยรลวศษสห".split("")
  };

  function initLetters() {
    var host = $("[data-xp-letters]");
    if (!host) return;

    var tiles = $$(".xp-letter", host);
    if (!tiles.length) return;

    var pool = ALPHABET[target];
    if (!pool || pool.length < 6) return;

    var i = 0;
    function step() {
      var tile = tiles[i % tiles.length];
      var ch = pool[(i * 7 + 3) % pool.length];
      if (tile && ch && tile.textContent !== ch) {
        tile.textContent = ch;
        if (!reduced() && tile.animate) {
          try {
            tile.animate(
              [{ transform: "translateY(0)", opacity: 1 },
               { transform: "translateY(-8px)", opacity: .35 },
               { transform: "translateY(0)", opacity: 1 }],
              { duration: 700, easing: "cubic-bezier(.22,1,.36,1)" }
            );
          } catch (e) { /* animation is optional */ }
        }
      }
      i++;
    }

    if (!reduced()) root.setInterval(step, 2600);
  }

  /* ======================================================================
     4. LANGUAGE RAIL — seamless marquee
     ----------------------------------------------------------------------
     The rail is a real list of links in the HTML. For a smooth loop the track
     needs to be at least twice the viewport width, so the list is cloned
     (aria-hidden, tabindex -1) until it is. Clones are decoration only.
     ====================================================================== */

  function initRail() {
    var rails = $$("[data-xp-rail]");
    if (!rails.length) return;

    rails.forEach(function (rail) {
      var track = $(".xp-rail-track", rail);
      if (!track) return;

      var originals = $$(".xp-rail-item", track);
      if (!originals.length) return;

      var need = Math.max(2, Math.ceil((rail.offsetWidth * 2) / Math.max(track.scrollWidth, 1)) + 1);

      for (var c = 1; c < need; c++) {
        originals.forEach(function (item) {
          var clone = item.cloneNode(true);
          clone.setAttribute("aria-hidden", "true");
          clone.setAttribute("tabindex", "-1");
          $$("a", clone).forEach(function (a) { a.setAttribute("tabindex", "-1"); });
          track.appendChild(clone);
        });
      }

      if (reduced()) track.style.animation = "none";
    });
  }

  /* ======================================================================
     5. KEYBOARD: "/" focuses search, Esc leaves it
     ====================================================================== */

  function initKeys() {
    on(doc, "keydown", function (e) {
      var box = $("#home-q") || $("#q");
      if (!box) return;

      var tag = (e.target && e.target.tagName || "").toLowerCase();
      var typing = tag === "input" || tag === "textarea" || tag === "select" ||
                   (e.target && e.target.isContentEditable);

      if (e.key === "/" && !typing && !e.metaKey && !e.ctrlKey && !e.altKey) {
        e.preventDefault();
        box.focus();
        if (box.select) box.select();
      } else if (e.key === "Escape" && (e.target === box)) {
        box.blur();
      }
    });
  }

  /* ======================================================================
     6. HOME SEARCH SUGGESTIONS
     ----------------------------------------------------------------------
     The home form already navigates to find-tutors.html?q=… (js/main.js
     §15). This adds a live dropdown from the same search-index.json the
     /search/ page uses. The index is fetched on the FIRST keystroke, not on
     load, so a visitor who never types pays nothing.
     ====================================================================== */

  function initHomeSuggest() {
    var form = $("#home-search");
    var input = $("#home-q");
    if (!form || !input) return;

    var box = doc.createElement("div");
    box.className = "xp-sugg";
    box.id = "home-sugg";
    box.setAttribute("role", "listbox");
    box.setAttribute("aria-label", copy.hint);
    box.hidden = true;
    var holder = form.parentNode;
    if (holder) holder.appendChild(box);

    var IDX = null, items = [], active = -1, loading = false;

    var esc = function (s) {
      return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    };

    var BASE = (function () {
      var src = SELF && SELF.src ? SELF.src : "";
      var m = src.match(/^(.*?)\/js\/experience\.js/);
      return m ? m[1] + "/" : "/";
    })();

    function load() {
      if (IDX || loading) return;
      loading = true;
      fetch(BASE + "search-index.json", { cache: "force-cache" })
        .then(function (r) { return r.json(); })
        .then(function (json) {
          IDX = json || [];
          /* The placeholder shown while the index downloaded is replaced by
             real matches the moment it arrives — otherwise the visitor keeps
             reading a generic "search every page" row they did not ask for. */
          if (input.value.trim().length > 1) run();
        })
        .catch(function () { IDX = []; });
    }

    function score(row, terms) {
      var t = String(row.t || "").toLowerCase();
      var d = String(row.d || "").toLowerCase();
      var k = String(row.k || "").toLowerCase();
      var s = 0;
      for (var i = 0; i < terms.length; i++) {
        var w = terms[i], best = 0;
        if (t.indexOf(w) > -1) best = 10;
        else if (d.indexOf(w) > -1) best = 4;
        else if (k.indexOf(w) > -1) best = 1;
        if (!best) return 0;
        s += best;
      }
      if (t.indexOf(terms.join(" ")) > -1) s += 8;
      return s;
    }

    function announce(open) {
      /* The support toast (js/monetization.js) hides while search is open so
         the two surfaces can never overlap. A plain DOM event keeps the two
         features decoupled: either file can load without the other. */
      try {
        var holder = form.parentNode;
        if (holder && holder.classList) {
          if (open) holder.classList.add("is-open");
          else holder.classList.remove("is-open");
        }
        var ev;
        if (typeof root.CustomEvent === "function") {
          ev = new root.CustomEvent(open ? "ekguru:search-open" : "ekguru:search-close");
        } else if (doc.createEvent) {
          ev = doc.createEvent("Event");
          ev.initEvent(open ? "ekguru:search-open" : "ekguru:search-close", false, false);
        }
        if (ev) doc.dispatchEvent(ev);
      } catch (e) { /* coordination is optional */ }
    }

    function close() {
      var wasOpen = !box.hidden;
      box.hidden = true;
      active = -1;
      input.setAttribute("aria-expanded", "false");
      if (wasOpen) announce(false);
    }

    function paint(list) {
      items = list;
      /* Empty results must not leave the pre-index placeholder rows in the
         box: hidden or not, a zero-result panel should hold zero rows. */
      if (!list.length) { box.innerHTML = ""; close(); return; }
      announce(true);
      box.innerHTML =
        '<div class="xp-sugg-head"><span>' + esc(copy.hint) + "</span>" +
        '<span class="xp-kbd">Enter</span></div>' +
        list.map(function (r, i) {
          return '<a role="option" href="' + esc(BASE + r.u) + '"' +
            (i === 0 ? ' aria-selected="true"' : "") + '>' + esc(r.t) +
            " <small style=\"opacity:.7\">· " + esc(r.s) + "</small></a>";
        }).join("") +
        '<a href="' + esc(base2("search/")) + '"><b>View all results →</b></a>';
      box.hidden = false;
      input.setAttribute("aria-expanded", "true");
    }

    function base2(path) {
      /* The home page lives at the site root; keep the existing convention
         used by the header links (search/index.html). */
      return BASE + path;
    }

    function run() {
      var q = String(input.value || "").trim().toLowerCase();
      if (q.length < 2) { close(); return; }
      if (!IDX) {
        load();
        /* First keystroke: show something useful immediately rather than an
           empty dropdown while the index downloads. */
        paint([
          { u: "find-tutors.html?q=" + encodeURIComponent(q), t: 'Search tutors for “' + q + '”', s: "Tutors" },
          { u: "search/index.html?q=" + encodeURIComponent(q), t: "Search every page for “" + q + "”", s: "Site" }
        ]);
        return;
      }
      var terms = q.split(/\s+/).filter(Boolean);
      var hits = [];
      for (var i = 0; i < IDX.length && hits.length < 24; i++) {
        var sc = score(IDX[i], terms);
        if (sc > 0) hits.push({ r: IDX[i], sc: sc });
      }
      hits.sort(function (a, b) { return b.sc - a.sc; });
      paint(hits.slice(0, 6).map(function (h) { return h.r; }));
    }

    function move(dir) {
      var links = $$("a[role=option]", box);
      if (!links.length) return;
      active = (active + dir + links.length) % links.length;
      links.forEach(function (a, i) {
        a.setAttribute("aria-selected", i === active ? "true" : "false");
      });
      links[active].scrollIntoView({ block: "nearest" });
    }

    var t = null;
    on(input, "input", function () {
      clearTimeout(t);
      t = setTimeout(run, 120);
    });
    on(input, "focus", function () { if (input.value.trim().length > 1) run(); });

    on(input, "keydown", function (e) {
      if (box.hidden) return;
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Escape") { close(); }
      else if (e.key === "Enter" && active > -1) {
        var link = $$("a[role=option]", box)[active];
        if (link) { e.preventDefault(); link.click(); }
      }
    });

    on(doc, "click", function (e) {
      if (!box.hidden && !form.parentNode.contains(e.target)) close();
    });
  }

  /* ======================================================================
     7. WORLD ARTWORK — the emblem follows the interface language
     ----------------------------------------------------------------------
     Each page ships the emblem for the market it was written for
     (index.html → world-en.svg, /ja/ → world-ja.svg), so a crawler and a
     no-JS visitor get the right picture. js/settings.js lets a visitor change
     the interface language of the root pages, and when they do the drawing has
     to follow — a Spanish page showing a violet English emblem is exactly the
     problem this layer exists to remove.

     The <script> tag's own src gives us the site prefix, so this works from
     /, /es/ and any nested page without a hardcoded root.
     ====================================================================== */

  function sitePrefix() {
    var src = SELF && SELF.getAttribute ? SELF.getAttribute("src") || "" : "";
    var m = src.match(/^(.*?)js\/experience\.js/);
    return m ? m[1] : "";
  }

  function initWorld() {
    var arts = $$("[data-xp-world]");
    if (!arts.length) return;

    var want = WORLD_ART[lang] ? lang : "en";
    var prefix = sitePrefix();

    arts.forEach(function (img) {
      if (img.getAttribute("data-xp-world") !== "auto") return;   /* fixed world */
      img.setAttribute("data-xp-world", want);
      img.setAttribute("src", prefix + "images/xp/world-" + want + ".svg");
    });
  }

  /* ======================================================================
     8. TRANSLATED LANDING PAGES  (es/ fr/ de/ pt/ ja/ ar/)
     ----------------------------------------------------------------------
     The twenty-four translated pages (index, find-tutors, join in six
     languages) are separate small documents with their own `.lp-*` markup.
     They were written before this layer existed, so they carry no animation
     hooks at all. Rather than editing twenty-four files — where the next
     regeneration would drop the edits anyway — the hooks are attached here
     from the markup that is already there.

     This is an enhancement by construction: the classes added below
     (xp-rise / xp-stagger) only hide anything once html.xp-anim exists, and
     that class is added by JS only. A visitor without JavaScript, or with a
     failed script, sees the page exactly as it was.
     ====================================================================== */

  function initLanding() {
    var wrap = $(".lp-wrap");
    if (!wrap) return;

    html.classList.add("xp-landing");

    /* Entrance order: the note, the headline and the lead-in first, then the
       tutor cards and the long tail of the page in staggered groups. */
    $$(".lp-wrap > .lp-note, .lp-wrap > h1, .lp-wrap > .lp-lead, .lp-wrap > p:not(.lp-lead):not(.lp-note)")
      .forEach(function (el) { el.classList.add("xp-rise"); });

    $$(".lp-cards, .lp-more-links, .lp-wrap > ol, .lp-wrap > ul, .lp-wrap > .lp-cards + *")
      .forEach(function (el) { el.classList.add("xp-stagger"); });

    /* Decoration: the letters of the language these pages teach, in the
       visitor's own palette. aria-hidden because it is ornament — the real
       heading above it already says what the page is about. */
    var h1 = $(".lp-wrap > h1");
    if (h1 && !$(".xp-lp-band", wrap)) {
      var band = doc.createElement("div");
      band.className = "xp-lp-band";
      band.setAttribute("data-xp-letters", "");
      band.setAttribute("aria-hidden", "true");
      band.innerHTML = letters.map(function (ch) {
        return '<span class="xp-letter">' + ch + "</span>";
      }).join("");
      h1.parentNode.insertBefore(band, h1.nextSibling);
    }
  }

  /* ======================================================================
     9. INTENT PREFETCH
     ----------------------------------------------------------------------
     Hovering (or focus) a tutor or course link for a moment fetches the page
     it points at, so the click feels instant. Four per page, same-origin only,
     skipped on a metered/slow connection and when the browser is offline.
     ====================================================================== */

  function initPrefetch() {
    try {
      var c = navigator.connection;
      if (c && (c.saveData || /2g|slow-2g|3g/.test(c.effectiveType || ""))) return;
    } catch (e) { /* no Network Information API — fine */ }

    var used = 0, seen = {};

    function maybe(e) {
      if (used >= 4) return;
      var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (!href || href.charAt(0) === "#" || /^(mailto:|tel:|https?:)/i.test(href)) return;
      if (!/tutor|courses|learn|materials/.test(href)) return;
      if (seen[href]) return;
      seen[href] = 1;
      used++;
      var link = doc.createElement("link");
      link.rel = "prefetch";
      link.href = href;
      link.as = "document";
      doc.head.appendChild(link);
    }

    on(doc, "pointerover", maybe, { passive: true });
    on(doc, "focusin", maybe);
  }

  /* ======================================================================
     10. SMALL TEXT UPGRADES
     ----------------------------------------------------------------------
     Copy that only makes sense once JS is running: placeholders that match the
     interface language, and the hero greeting. Both are additive — the
     English/dev text stays in the HTML for crawlers and no-JS readers, and is
     only replaced when a translation for the current language exists.
     ====================================================================== */

  function initCopy() {
    if (lang === "en") return;

    $$("[data-xp-ph]").forEach(function (el) {
      var key = el.getAttribute("data-xp-ph");
      if (key === "hint") el.setAttribute("placeholder", copy.hint);
    });

    $$("[data-xp-hello]").forEach(function (el) {
      el.textContent = copy.hello;
    });

    $$("[data-xp-cta]").forEach(function (el) {
      el.textContent = copy.cta;
    });
  }

  /* ======================================================================
     BOOT
     ====================================================================== */

  API.revealAll = revealAll;

  /* ======================================================================
     11. THE HEADER DRAWER ON THE TRANSLATED PAGES  (es fr de pt ja ar)
     ----------------------------------------------------------------------
     js/main.js wires the burger on the English pages, but the translated
     pages deliberately do not load it: it expects to run from the site root.
     Their header then had no burger at all, so on a phone four items and a
     pill-button wrapped into two ragged rows and the button was clipped off
     the right edge.

     The drawer CSS already ships in the shell stylesheet. All that was
     missing was something to open it. If js/main.js did bind the header it
     has already given the nav an id — then we leave it alone, so the two can
     never fight over aria-expanded.
     ====================================================================== */

  function initNav() {
    var nav = $(".hdr .nav"), burger = $(".hdr .burger");
    if (!nav || !burger) return;

    var MENU = { es: "Menú", fr: "Menu", de: "Menü", pt: "Menu",
                 ja: "メニュー", ar: "القائمة", hi: "मेनू" };
    /* The label is owner-independent and idempotent: whoever binds the
       drawer, the burger is named in the page language. (Previously this
       sat behind the early return, so on shell-owned pages it never ran.) */
    if (burger.getAttribute("aria-label") === "Menu") {
      burger.setAttribute("aria-label", MENU[lang] || "Menu");
    }

    /* Binding is another matter. js/main.js and js/site-shell.js own richer
       drawers (focus trap, focus return); this one exists only for pages
       that load neither. Presence — not execution order — decides, so tag
       order can never reintroduce the double-drawer (index.html bound both
       this and main.js: same classes, two state machines, kept working only
       by mirrored toggling). Comments mentioning main.js do not match:
       querySelector sees elements, not comments. */
    if (nav.id || root.EKGURU_DRAWER) return;
    if (doc.querySelector('script[src*="main.js"], script[src*="site-shell.js"]')) return;
    root.EKGURU_DRAWER = "experience";

    nav.id = "primary-nav";
    burger.setAttribute("aria-controls", nav.id);

    var backdrop = $(".nav-backdrop");
    if (!backdrop) {
      backdrop = doc.createElement("div");
      backdrop.className = "nav-backdrop";
      backdrop.setAttribute("aria-hidden", "true");
      doc.body.appendChild(backdrop);
    }

    var open = false;
    var savedY = 0;

    /* ==================================================================
       THE LOCK — same shape as js/main.js v74, for the same reason.

       Prakash, twice: "header mai 3 lines open kerne pr kai bug hai
       background running nahi hota." — open the drawer on a phone
       part-way down a long page and the page behind either keeps
       scrolling under the finger or snaps to the top, and once it has
       snapped the drawer's own links no longer point where the visitor
       was reading.

       The class alone is not a lock. body.nav-open is position:fixed
       (that is what stops the scroll), and a fixed body with no offset
       is a body at the top of the document. So the offset is recorded
       before the class goes on, written into `top`, and restored on
       close with behavior:"auto" — with smooth scrolling on <html>,
       the restore animates and reads as the very jump this prevents.
       ================================================================== */

    function set(next) {
      if (next === open) return;
      open = next;
      if (open) {
        savedY = window.scrollY || window.pageYOffset || 0;
        nav.classList.add("open");
        doc.body.classList.add("nav-open");
        doc.body.style.top = "-" + savedY + "px";
        burger.setAttribute("aria-expanded", "true");
        backdrop.setAttribute("aria-hidden", "false");
        nav.removeAttribute("aria-hidden");
        var first = nav.querySelector("a[href], button:not([disabled])");
        if (first) { try { first.focus(); } catch (e) {} }
      } else {
        nav.classList.remove("open");
        doc.body.classList.remove("nav-open");
        backdrop.setAttribute("aria-hidden", "true");
        burger.setAttribute("aria-expanded", "false");
        doc.body.style.top = "";
        try { window.scrollTo({ top: savedY, behavior: "auto" }); }
        catch (e2) { window.scrollTo(0, savedY); }
      }
    }

    on(burger, "click", function (e) { e.stopPropagation(); set(!open); });
    on(nav, "click", function (e) {
      var a = e.target && e.target.closest ? e.target.closest("a") : null;
      if (a && open) set(false);
    });
    on(doc, "click", function (e) {
      if (open && !nav.contains(e.target) && !burger.contains(e.target)) set(false);
    });
    on(doc, "keydown", function (e) {
      if (e.key === "Escape" && open) { set(false); burger.focus(); }
    });
    /* Growing past the drawer breakpoint (1200px, the same one main.js uses)
       must unlock the page, or a visitor who resized cannot scroll. */
    on(root, "resize", function () { if (open && root.innerWidth > 1200) set(false); });
    /* Back from the bfcache with body.nav-open still set is a page that
       cannot scroll with no visible reason. Reset it. */
    on(root, "pageshow", function () { if (open) set(false); });
  }

  function boot() {
    /* initLanding first: it attaches the xp-rise / xp-stagger hooks that
       initMotion then observes, and adds the letter band initLetters fills. */
    var jobs = [initNav, initLanding, initWorld, initMotion, initProgress, initLetters,
                initRail, initKeys, initHomeSuggest, initPrefetch, initCopy];
    jobs.forEach(function (job) {
      try { job(); } catch (e) {
        /* One failed enhancement must never stop the others, and must never
           leave content hidden: force everything visible and carry on. */
        try { revealAll(); } catch (e2) {}
      }
    });
  }

  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  root.EkGuruXP = API;
})(window, document);
