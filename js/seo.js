/* =========================================================
   EkGuru — Advanced SEO engine
   ---------------------------------------------------------
   Runs BEFORE main.js. Injects, per page and per language:
     · <title> + meta description + keywords
     · canonical + hreflang (7 markets + x-default)
     · Open Graph + Twitter Card
     · JSON-LD: Organization, WebSite+SearchAction, BreadcrumbList,
                Course, Person, Service, FAQPage, AggregateRating,
                Review, VideoObject
   All of it is data-driven from tutors-data.js + site-config.js,
   so it stays correct automatically when you edit your data.
   ========================================================= */
(function () {
  "use strict";

  var S = window.EKGURU_SITE || {};
  var M = window.EKGURU_MARKETS || [];
  var T = window.EKGURU_TUTORS || [];
  var BASE = (S.baseUrl || "").replace(/\/?$/, "/");

  /* =========================================================
     A PRICE IN PROSE IS A PRICE THAT GOES STALE  (v63)
     ---------------------------------------------------------
     THE BUG. Seven meta descriptions and one FAQ answer had "$3"
     typed into them, in seven languages:

       "Private 1-on-1 Hindi lessons from $3 …"
       "Clases particulares desde 3 $ …"
       "Private 1-on-1 Hindi lessons start at $3 for a 50-minute
        session."      ← this one is published as FAQPage schema

     $3 came from a tutor FILE. The Google Sheet later said $10 and
     the cheapest tutor on the site became $8. Those strings kept
     advertising $3 — in the search snippet, which is the first
     thing anyone sees, and in structured data, which is what
     Google quotes as an answer.

     A published price is a quote. Advertising one nobody can book
     is a misleading price indication, and the FAQ version is worse
     than the meta one because Google may show it as a direct
     answer without the visitor ever reaching the site.

     Fixed with a token filled from the live tutor list. Same idea
     and the same token names as js/main.js fillTokens() — the two
     are separate because this file runs standalone on pages that
     do not load main.js.

     ⚠️ These are META tags: they are read once, at page load, and
     the sheet may not have arrived yet. So this ALSO re-runs on
     ekguru:sheet — see the listener at the bottom of this file.
     Without that, the description would carry the file's price on
     a first visit, which is precisely the bug it is fixing.
     ========================================================= */
  function money(usd) {
    try {
      if (window.EkGuruPrice && window.EkGuruPrice.price) return window.EkGuruPrice.price(usd);
    } catch (e) {}
    return (S.currency || "$") + usd;
  }

  function fillTokens(str) {
    if (typeof str !== "string" || str.indexOf("{") === -1) return str;
    /* Read the global every time, not the T captured at load: the
       sheet mutates that array in place and may have hidden the
       tutor who used to be cheapest. */
    var live = window.EKGURU_TUTORS || [];
    var prices = live.map(function (x) { return Number(x.priceUSD) || 0; })
                     .filter(function (n) { return n > 0; });
    return str
      /* Empty rather than "$0" or "$Infinity" — Math.min of an empty
         array is Infinity and would have printed literally. */
      .replace(/\{minPrice\}/g, prices.length ? money(Math.min.apply(null, prices)) : "")
      .replace(/\{maxPrice\}/g, prices.length ? money(Math.max.apply(null, prices)) : "")
      .replace(/\{tutors\}/g, String(live.length));
  }

  /* ---------- helpers ---------- */
  function page() {
    var p = location.pathname.split("/").pop();
    return (!p || p === "") ? "index.html" : p;
  }
  function lang() {
    try {
      var q = new URLSearchParams(location.search).get("lang");
      if (q) return q;
      var s = localStorage.getItem("ekguru_lang");
      if (s) return s;
    } catch (e) {}
    var nav = (navigator.language || "en").slice(0, 2);
    for (var i = 0; i < M.length; i++) if (M[i].code === nav) return nav;
    return "en";
  }
  function meta(attr, key, content) {
    if (!content) return;
    var el = document.head.querySelector("meta[" + attr + '="' + key + '"]');
    if (!el) { el = document.createElement("meta"); el.setAttribute(attr, key); document.head.appendChild(el); }
    el.setAttribute("content", content);
  }
  function link(rel, href, extra) {
    var sel = 'link[rel="' + rel + '"]' + (extra && extra.hreflang ? '[hreflang="' + extra.hreflang + '"]' : "");
    var el = document.head.querySelector(sel);
    if (!el) { el = document.createElement("link"); el.setAttribute("rel", rel); document.head.appendChild(el); }
    el.setAttribute("href", href);
    if (extra) for (var k in extra) el.setAttribute(k, extra[k]);
  }
  function jsonld(id, obj) {
    try {
      var old = document.getElementById(id);
      if (old) old.remove();
      var s = document.createElement("script");
      s.type = "application/ld+json";
      s.id = id;
      s.textContent = JSON.stringify(obj);
      document.head.appendChild(s);
    } catch (e) { /* SEO must never break the page */ }
  }
  function tutorById(id) {
    for (var i = 0; i < T.length; i++) if (T[i].id === id) return T[i];
    return null;
  }

  var L = lang();
  var market = M.filter(function (m) { return m.code === L; })[0] || M[0] || { locale: "en-US", dir: "ltr" };
  var pg = page();
  var qid = new URLSearchParams(location.search).get("id");
  var tutor = pg === "tutor.html" ? (tutorById(qid) || T[0]) : null;

  /* =========================================================
     1. Per-page copy (title / description / keywords)
     ========================================================= */
  var COPY = {
    "index.html": {
      en: {
        t: "Learn Hindi Online with a Private Tutor | EkGuru — 1-on-1 Hindi Lessons",
        d: "Explore Hindi tutor profiles and request private 1-on-1 lessons. Check each profile for background, subjects, displayed price and current availability.",
        k: "learn hindi online, hindi tutor profiles, private hindi lessons, speak hindi, devanagari, hindi for beginners, online hindi classes, 1-on-1 hindi lessons"
      },
      es: { t: "Aprende hindi online con un profesor particular | EkGuru", d: "Explora perfiles de profesores de hindi. Comprueba la experiencia, las materias, el precio mostrado y la disponibilidad de cada perfil antes de solicitar una clase.", k: "aprender hindi, profesor de hindi, clases de hindi online, hindi para principiantes" },
      /* v50: was "Apprenez l'hindi en ligne avec un professeur particulier | EkGuru"
         — 65 characters, so Google cut the brand off. French is wordier than
         English and was the only pack over the ~60-character limit. */
      fr: { t: "Cours d'hindi en ligne — profils de professeurs | EkGuru", d: "Explorez les profils de professeurs d'hindi. Vérifiez le parcours, les matières, le prix affiché et les disponibilités avant une demande.", k: "apprendre l'hindi, professeur d'hindi, cours d'hindi en ligne, hindi débutant" },
      de: { t: "Hindi online lernen mit Privatlehrer | EkGuru", d: "Sieh dir Hindi-Lehrkraftprofile an. Prüfe den angegebenen Hintergrund, die Fächer, den angezeigten Preis und die Verfügbarkeit vor einer Anfrage.", k: "hindi lernen, hindi lehrer, hindi online kurs, hindi für anfänger" },
      pt: { t: "Aprenda hindi online com professor particular | EkGuru", d: "Explore perfis de professores de hindi. Confira a experiência, as matérias, o preço exibido e a disponibilidade antes de solicitar uma aula.", k: "aprender hindi, professor de hindi, aulas de hindi online, hindi para iniciantes" },
      ja: { t: "オンラインでヒンディー語を学ぶ | EkGuru マンツーマンレッスン", d: "ヒンディー語講師のプロフィールを確認し、申告された言語背景、科目、表示料金、空き状況を見てからレッスンをリクエストできます。", k: "ヒンディー語 オンライン, ヒンディー語 講師, ヒンディー語 レッスン, ヒンディー語 初心者" },
      ar: { t: "تعلم اللغة الهندية عبر الإنترنت مع معلم خاص | EkGuru", d: "استعرض ملفات معلمي الهندية وتحقق من الخلفية والمواد والسعر المعروض والتوفر قبل إرسال طلب درس.", k: "تعلم الهندية, معلم لغة هندية, دروس هندية اونلاين, الهندية للمبتدئين" }
    },
    "find-tutors.html": {
      en: {
        t: "Find a Hindi Tutor Online | Tutor Profiles — EkGuru",
        d: "Browse Hindi tutor profiles and filter by level, displayed price and rating. Check each profile’s stated language background and availability.",
        k: "find hindi tutor, hindi tutor profiles, online hindi lessons, hindi tutor for beginners"
      },
      es: { t: "Encuentra un profesor de hindi online | EkGuru", d: "Explora perfiles de profesores de hindi y filtra por nivel, precio mostrado y valoración. Comprueba los datos de cada perfil antes de solicitar una clase.", k: "profesor de hindi online, buscar profesor hindi" },
      fr: { t: "Trouvez un professeur d'hindi en ligne | EkGuru", d: "Parcourez les profils de professeurs d'hindi et filtrez par niveau, prix affiché et note. Vérifiez les détails avant une demande.", k: "professeur d'hindi en ligne, trouver prof hindi" },
      de: { t: "Hindi-Lehrer online finden | EkGuru", d: "Hindi-Lehrkraftprofile nach Niveau, angezeigtem Preis und Bewertung filtern. Angaben vor einer Anfrage prüfen.", k: "hindi lehrer finden, hindi nachhilfe online" },
      pt: { t: "Encontre um professor de hindi online | EkGuru", d: "Veja perfis de professores de hindi e filtre por nível, preço exibido e avaliação. Confira os detalhes antes de solicitar uma aula.", k: "professor de hindi online, encontrar professor hindi" },
      ja: { t: "ヒンディー語講師を探す | EkGuru", d: "ヒンディー語講師のプロフィールをレベル、表示料金、評価で絞り込み、申告内容を確認してからリクエストできます。", k: "ヒンディー語 講師 探す, ヒンディー語 家庭教師" },
      ar: { t: "ابحث عن معلم لغة هندية عبر الإنترنت | EkGuru", d: "تصفح ملفات معلمي الهندية وصفِّ حسب المستوى والسعر المعروض والتقييم، ثم تحقق من التفاصيل قبل الطلب.", k: "معلم هندية اونلاين, البحث عن معلم هندية" }
    },
    "join.html": {
      en: {
        t: "Become a Hindi Tutor — Teach on EkGuru | Free Tutor Listing",
        d: "Teach Hindi online with EkGuru. Free profile listing, no commission, students contact you directly. Send your bio, photo, intro video and rates to apply.",
        k: "become a hindi tutor, teach hindi online, hindi teaching jobs online, online tutor jobs, teach hindi from home"
      },
      es: { t: "Sé profesor de hindi — Enseña en EkGuru", d: "Enseña hindi online con EkGuru. Perfil gratuito, sin comisiones, los alumnos te contactan directamente.", k: "ser profesor de hindi, enseñar hindi online" },
      fr: { t: "Devenez professeur d'hindi — Enseignez sur EkGuru", d: "Enseignez l'hindi en ligne avec EkGuru. Profil gratuit, aucune commission, les élèves vous contactent directement.", k: "devenir professeur d'hindi, enseigner l'hindi en ligne" },
      de: { t: "Hindi-Lehrer werden — Unterrichte auf EkGuru", d: "Unterrichte Hindi online mit EkGuru. Kostenloses Profil, keine Provision, Schüler kontaktieren dich direkt.", k: "hindi lehrer werden, hindi online unterrichten" },
      pt: { t: "Seja professor de hindi — Ensine na EkGuru", d: "Ensine hindi online com a EkGuru. Perfil gratuito, sem comissão, os alunos falam direto com você.", k: "ser professor de hindi, ensinar hindi online" },
      ja: { t: "ヒンディー語講師になる — EkGuruで教える", d: "EkGuruでヒンディー語をオンライン指導。掲載無料、手数料なし、生徒から直接連絡が届きます。", k: "ヒンディー語 講師 募集, オンライン 講師 求人" },
      ar: { t: "كن معلم لغة هندية — درّس على EkGuru", d: "درّس الهندية عبر الإنترنت مع EkGuru. إدراج مجاني، بدون عمولة، والطلاب يتواصلون معك مباشرة.", k: "كن معلم هندية, تدريس الهندية اونلاين" }
    }
  };

  function copyFor() {
    if (tutor) {
      var per = { "50 min": "50-minute" };
      /* only advertise numbers we actually have: a brand-new tutor should not
         show "5.0★, 0 lessons" in Google — it reads worse than no badge at all */
      var proof = "";
      if (tutor.reviewsCount > 0 && tutor.lessonsCount > 0) {
        proof = " (" + tutor.rating.toFixed(1) + "★, " + tutor.lessonsCount + " lessons)";
      } else if (tutor.reviewsCount > 0) {
        proof = " (" + tutor.rating.toFixed(1) + "★)";
      } else if (tutor.lessonsCount > 0) {
        proof = " (" + tutor.lessonsCount + " lessons)";
      }

      var titles = {
        en: tutor.name + " — Online Hindi Tutor Profile | EkGuru",
        es: tutor.name + " — Perfil de profesor de hindi online | EkGuru",
        fr: tutor.name + " — Profil de professeur d'hindi en ligne | EkGuru",
        de: tutor.name + " — Profil einer Hindi-Lehrkraft online | EkGuru",
        pt: tutor.name + " — Perfil de professor de hindi online | EkGuru",
        ja: tutor.name + " — オンラインヒンディー語講師プロフィール | EkGuru",
        ar: tutor.name + " — ملف معلم لغة هندية عبر الإنترنت | EkGuru"
      };
      /* ---------------------------------------------------------
         Every fragment below is conditional. A tutor may have no
         country, no years of experience and no reviews yet — that
         is normal for someone just added. Before this guard those
         gaps printed as "native speaker from undefined" and
         "rated 0.0/5 from 0 reviews" straight into the meta
         description, in all seven languages.
         --------------------------------------------------------- */
      var from = tutor.country ? " — profile location: " + tutor.country : "";
      var yrs  = tutor.experienceYears > 0 ? tutor.experienceYears : 0;
      var rated = tutor.reviewsCount > 0 && tutor.rating > 0;
      var lesson = per[tutor.lessonLength] || tutor.lessonLength || "50 min";
      var price = tutor.priceUSD > 0 ? tutor.priceUSD : null;

      /* "$8 per 50 min" only when there is a real price */
      function cost(prefix, suffix) {
        return price == null ? "" : (prefix || "") + price + (suffix || "");
      }
      function yearsEn() { return yrs ? ", " + yrs + "+ years' experience" : ""; }
      function ratingEn() {
        return rated ? ", rated " + tutor.rating.toFixed(1) + "/5 from " +
          tutor.reviewsCount + " reviews" : "";
      }
      /* localised "N+ years' experience, rated X/5" tail */
      function tail(yearsWord, ratedWord) {
        var out = "";
        if (yrs) out += ", " + yrs + "+ " + yearsWord;
        if (rated) out += ", " + ratedWord + " " + tutor.rating.toFixed(1) + "/5";
        return out;
      }

      var descs = {
        en: "Tutor-provided profile for " + tutor.name +
            ": stated subjects, languages and lesson details. Confirm current pricing and availability before booking.",
        es: "Perfil aportado por " + tutor.name +
            ": materias, idiomas y datos de clases declarados. Confirma el precio y la disponibilidad antes de reservar.",
        fr: "Profil fourni par " + tutor.name +
            " : matières, langues et détails de cours déclarés. Confirmez le prix et les disponibilités avant de réserver.",
        de: "Von " + tutor.name +
            " bereitgestelltes Profil mit genannten Fächern, Sprachen und Unterrichtsdetails. Preis und Verfügbarkeit vor der Buchung bestätigen.",
        pt: "Perfil fornecido por " + tutor.name +
            ": matérias, idiomas e detalhes de aula declarados. Confirme o preço e a disponibilidade antes de reservar.",
        ja: tutor.name + "講師提供のプロフィールです。記載された科目、言語、レッスン情報を確認し、予約前に現在の料金と空き状況を確認してください。",
        ar: "ملف قدمه المعلم " + tutor.name +
            " ويعرض المواد واللغات وتفاصيل الدرس المذكورة. أكد السعر والتوافر الحالي قبل الحجز."
      };
      return {
        t: titles[L] || titles.en,
        d: descs[L] || descs.en,
        k: [tutor.name + " hindi tutor", "online hindi tutor", "private hindi lessons"].concat(tutor.teaches || []).join(", ").toLowerCase()
      };
    }
    var block = COPY[pg] || COPY["index.html"];
    return block[L] || block.en;
  }

  /* which pages have a real translated file on disk */
  function hasLangFileEarly(page) {
    return ["index.html", "find-tutors.html", "join.html"].indexOf(page) > -1;
  }

  /* v63: resolve {minPrice} ONCE, here, rather than at each of the
     nine places c.t and c.d are used. Missing one of those nine —
     og:description, say — would publish a raw "{minPrice}" to
     Facebook while the page itself looked fine. Doing it at the
     source makes that impossible. */
  var c = (function () {
    var raw = copyFor(), out = {};
    Object.keys(raw).forEach(function (k) { out[k] = fillTokens(raw[k]); });
    return out;
  })();

  /* =========================================================
     2. Head tags
     ========================================================= */
  document.documentElement.setAttribute("lang", L);
  document.documentElement.setAttribute("dir", market.dir || "ltr");
  document.title = c.t;

  meta("name", "description", c.d);
  meta("name", "author", S.brand);
  /* A requested tutor id that does not exist falls back to the first
     tutor so the visitor still sees something useful. That page must not
     be indexed, or Google collects endless near-duplicate URLs — the
     classic soft-404 trap. */
  var badId = pg === "tutor.html" && qid && !tutorById(qid);

  /* tutor.html is noindex in the raw HTML, on purpose: it is the
     interactive twin of the pre-rendered /tutor/<id>/ pages and must
     never compete with them. It used to be overwritten to "index"
     here, which was wrong twice over:
       · Googlebot reads the raw HTML long before it renders any
         JavaScript, so it saw noindex anyway — the two disagreed.
       · Google's own guidance is never to put noindex and
         rel=canonical on the same page; they contradict each other
         and the outcome is unpredictable.
     So this page keeps whatever the HTML already declared, and the
     canonical block below no longer re-states noindex either. */
  var isTutorShell = pg === "tutor.html";

  if (badId) {
    meta("name", "robots", "noindex, follow");
    meta("name", "googlebot", "noindex, follow");
  } else if (!isTutorShell) {
    meta("name", "robots", "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1");
    meta("name", "googlebot", "index, follow, max-snippet:-1, max-image-preview:large");
  }
  meta("name", "theme-color", "#5b3df5");
  meta("name", "format-detection", "telephone=no");
  meta("name", "rating", "general");
  meta("name", "distribution", "global");

  /* ---------- canonical ----------
     A tutor profile exists at two addresses: the interactive
     tutor.html?id=X and the pre-rendered tutor/X/. They show the same
     information, so one of them must be declared authoritative or
     Google splits the ranking signal between them and may index the
     thinner one.

     The static page wins: it carries the full text without JavaScript,
     which is what a crawler actually reads. So the interactive page
     points its canonical at the static twin.

     Bare tutor.html with no id is only a shell, so it is not indexed. */
  var canonical;
  if (tutor && qid) {
    /* No canonical here either — and this is not an oversight.
       tutor.html declares noindex in its raw HTML, which is what a
       crawler reads before it ever runs JavaScript, so a canonical
       injected afterwards is invisible to Google anyway. Shipping
       both would only be the noindex + rel=canonical contradiction
       Google warns against, with no upside.

       Nothing is lost: the authoritative page is /tutor/<id>/, it is
       the only one in sitemap.xml, and every internal link and card
       on the site points straight at it. This interactive shell is
       for people, not for the index. A plain <link rel="alternate">
       is added instead, which states the relationship without
       claiming anything about indexing. */
    canonical = "";
    link("alternate", BASE + "tutor/" + encodeURIComponent(tutor.id) + "/");
  } else if (pg === "tutor.html") {
    /* Bare tutor.html with no ?id= is only an empty shell. The HTML
       already declares noindex; adding a canonical on top of that
       would be the exact contradiction Google warns about, so this
       page simply gets none. */
    canonical = "";
  } else if (hasLangFileEarly(pg) && L !== "en") {
    canonical = BASE + L + "/" + (pg === "index.html" ? "" : pg);
  } else {
    canonical = BASE + (pg === "index.html" ? "" : pg);
  }
  /* An empty canonical means "deliberately none" — see above. Removing
     any stale tag matters because the shell and ?id= share this code. */
  if (canonical) link("canonical", canonical);
  else {
    var stale = document.head.querySelector('link[rel="canonical"]');
    if (stale) stale.parentNode.removeChild(stale);
  }

  /* ---------- hreflang ----------
     For the three main pages a real translated file now exists at
     /es/, /fr/, /de/ and so on, so hreflang points at those. Google
     can fetch each one and see genuinely different content.

     Tutor profiles have no per-language file, so they advertise the
     ?lang= form. That is honest: the same URL genuinely serves the
     other language once it loads. */
  document.head.querySelectorAll('link[rel="alternate"][hreflang]').forEach(function (n) { n.remove(); });
  var fileName = (pg === "index.html" ? "" : pg);
  var hasLangFile = !tutor && ["index.html", "find-tutors.html", "join.html"].indexOf(pg) > -1;

  M.forEach(function (m) {
    var el = document.createElement("link");
    el.rel = "alternate";
    el.hreflang = m.locale;
    if (hasLangFile) {
      el.href = m.code === "en" ? BASE + fileName : BASE + m.code + "/" + fileName;
    } else {
      el.href = BASE + fileName + "?" +
        (tutor ? "id=" + encodeURIComponent(tutor.id) + "&" : "") + "lang=" + m.code;
    }
    document.head.appendChild(el);
  });
  /* bare language codes as well, which Google accepts alongside locales */
  M.forEach(function (m) {
    if (m.locale.split("-")[0] === m.code) return;
    var el = document.createElement("link");
    el.rel = "alternate";
    el.hreflang = m.code;
    el.href = hasLangFile
      ? (m.code === "en" ? BASE + fileName : BASE + m.code + "/" + fileName)
      : BASE + fileName + "?" + (tutor ? "id=" + encodeURIComponent(tutor.id) + "&" : "") + "lang=" + m.code;
    document.head.appendChild(el);
  });
  var xd = document.createElement("link");
  xd.rel = "alternate"; xd.hreflang = "x-default"; xd.href = canonical;
  document.head.appendChild(xd);

  /* Open Graph */
  /* BUG FOUND v62 — see the same fix in tools/prerender.js.
     BASE + an already-absolute URL produces
     "https://ekguru.shop/https://lh3.google…",
     which every social card and Google's rich result would show as
     no image at all. A photo from Google Drive is absolute. */
  function absUrl(p) { return /^https?:\/\//i.test(String(p || "")) ? String(p) : BASE + String(p || ""); }
  var ogImg = tutor ? absUrl(tutor.photo || "images/sushila.jpg") : BASE + "images/og-cover.jpg";
  meta("property", "og:site_name", S.brand);
  meta("property", "og:type", tutor ? "profile" : "website");
  meta("property", "og:title", c.t);
  meta("property", "og:description", c.d);
  meta("property", "og:url", canonical);
  meta("property", "og:image", ogImg);
  meta("property", "og:image:alt", tutor ? tutor.name + " — Hindi tutor on EkGuru" : "EkGuru — learn Hindi online");
  meta("property", "og:locale", (market.locale || "en_US").replace("-", "_"));
  M.forEach(function (m) {
    if (m.code === L) return;
    var el = document.createElement("meta");
    el.setAttribute("property", "og:locale:alternate");
    el.setAttribute("content", m.locale.replace("-", "_"));
    document.head.appendChild(el);
  });

  /* Twitter */
  meta("name", "twitter:card", "summary_large_image");
  meta("name", "twitter:title", c.t);
  meta("name", "twitter:description", c.d);
  meta("name", "twitter:image", ogImg);

  /* Perf hints for the YouTube facade */
  [["preconnect", "https://www.youtube-nocookie.com"], ["preconnect", "https://i.ytimg.com"], ["dns-prefetch", "https://www.google.com"]]
    .forEach(function (p) {
      var el = document.createElement("link");
      el.rel = p[0]; el.href = p[1];
      document.head.appendChild(el);
    });

  /* =========================================================
     3. Structured data (JSON-LD)
     ========================================================= */
  var ORG = {
    "@type": "EducationalOrganization",
    "@id": BASE + "#organization",
    name: S.brand,
    alternateName: "EkGuru Learning",
    url: BASE,
    slogan: S.tagline,
    description: "EkGuru publishes Hindi learning resources and independent tutor profiles for one-to-one online lesson requests.",
    email: S.email,
    logo: { "@type": "ImageObject", url: BASE + "images/sushila.jpg" },
    foundingDate: String(S.foundingYear || 2024),
    areaServed: M.map(function (m) { return { "@type": "Country", name: m.country }; }),
    knowsLanguage: ["hi", "en"],
    sameAs: [S.youtubeChannel, S.facebook, S.instagram].filter(Boolean)
  };

  var WEBSITE = {
    "@type": "WebSite",
    "@id": BASE + "#website",
    url: BASE,
    name: S.brand,
    description: c.d,
    inLanguage: M.map(function (m) { return m.locale; }),
    publisher: { "@id": BASE + "#organization" },
    potentialAction: {
      "@type": "SearchAction",
      target: { "@type": "EntryPoint", urlTemplate: BASE + "find-tutors.html?q={search_term_string}" },
      "query-input": "required name=search_term_string"
    }
  };

  var graph = [ORG, WEBSITE];

  /* --- Breadcrumbs --- */
  var crumbs = [{ "@type": "ListItem", position: 1, name: "Home", item: BASE }];
  if (pg === "find-tutors.html") crumbs.push({ "@type": "ListItem", position: 2, name: "Find Hindi Tutors", item: BASE + "find-tutors.html" });
  if (pg === "join.html") crumbs.push({ "@type": "ListItem", position: 2, name: "Become a Tutor", item: BASE + "join.html" });
  if (tutor) {
    crumbs.push({ "@type": "ListItem", position: 2, name: "Hindi Tutors", item: BASE + "find-tutors.html" });
    crumbs.push({ "@type": "ListItem", position: 3, name: tutor.name, item: canonical });
  }
  graph.push({ "@type": "BreadcrumbList", "@id": canonical + "#breadcrumb", itemListElement: crumbs });

  /* --- Home / listing: the current public tutor profiles. These are profile
     links, not Course/Offer inventory; current terms require confirmation. --- */
  if (pg === "index.html" || pg === "find-tutors.html") {
    graph.push({
      "@type": "ItemList",
      "@id": BASE + "find-tutors.html#tutorlist",
      name: "Hindi tutors on EkGuru",
      numberOfItems: T.length,
      itemListElement: T.map(function (t, i) {
        return {
          "@type": "ListItem",
          position: i + 1,
          url: BASE + "tutor/" + encodeURIComponent(t.id) + "/",
          name: t.name
        };
      })
    });
  }

  /* --- Tutor profile: Person + Video. Imported profile fields are not live
     inventory, so do not emit Offer, Service, AggregateRating or Review data. --- */
  if (tutor) {
    graph.push({
      "@type": "Person",
      "@id": canonical + "#person",
      name: tutor.name,
      alternateName: tutor.nickname || undefined,
      jobTitle: "Hindi Tutor",
      description: "Tutor-provided profile excerpt: " + ((tutor.about && tutor.about[0]) || ""),
      image: absUrl(tutor.photo),
      url: canonical,
      knowsLanguage: (tutor.speaks || []).map(function (s) { return s.lang; }),
      knowsAbout: tutor.teaches || [],
      sameAs: [tutor.preplyUrl].filter(Boolean)
    });

    if (tutor.youtubeId) {
      graph.push({
        "@type": "VideoObject",
        "@id": canonical + "#video",
        name: (tutor.videoTitle || "Intro video") + " — " + tutor.name,
        description: "Introduction video from " + tutor.name + ", online Hindi tutor on EkGuru.",
        thumbnailUrl: ["https://i.ytimg.com/vi/" + tutor.youtubeId + "/maxresdefault.jpg"],
        contentUrl: "https://www.youtube.com/watch?v=" + tutor.youtubeId,
        embedUrl: "https://www.youtube-nocookie.com/embed/" + tutor.youtubeId,
        publisher: { "@id": BASE + "#organization" }
      });
    }
  }

  /* --- FAQ (rich result eligible) --- */
  var FAQ = {
    en: [
      ["How much does an online Hindi lesson cost on EkGuru?", "Profiles show imported USD prices and estimated local-currency displays. Confirm the current price, billing currency and external-platform terms before booking."],
      ["Do I need to know any Hindi before starting?", "EkGuru has free beginner materials. For paid lessons, check the levels stated on each profile and ask whether your starting point is suitable."],
      ["What language background do tutors have?", "Each profile states the tutor’s language background and subjects. Review those tutor-provided details before sending an enquiry."],
      ["Can I request a trial lesson?", "Trial terms are not universal or guaranteed. Ask about the current format, price and cancellation terms before booking."],
      ["How are the lessons delivered?", "Profiles describe online one-to-one lessons. Confirm the video platform, duration and timing in the enquiry response before booking."],
      ["Which timezones do you cover?", "No timezone coverage is guaranteed. Include your timezone and preferred times in the enquiry and wait for availability confirmation."],
      ["How do I contact a tutor?", "Send an enquiry from a profile; EkGuru may forward it using the contact information on file. You can also review a linked external profile directly."],
      ["Can I apply to become a Hindi tutor on EkGuru?", "You can submit the requested profile information from the Become a Tutor page. Publication and current terms are confirmed during review."]
    ]
  };
  var faqList = (FAQ[L] || FAQ.en).map(function (qa) {
    /* v63: the cost answer carries {minPrice} and this list is
       published as FAQPage schema, so the token MUST be resolved
       before it reaches Google. An unresolved "{minPrice}" in
       structured data is an invalid answer; a stale "$3" is a
       worse one, because it is wrong rather than obviously broken. */
    return [fillTokens(qa[0]), fillTokens(qa[1])];
  });
  if (pg === "index.html") {
    graph.push({
      "@type": "FAQPage",
      "@id": canonical + "#faq",
      mainEntity: faqList.map(function (q) {
        return { "@type": "Question", name: q[0], acceptedAnswer: { "@type": "Answer", text: q[1] } };
      })
    });
  }
  window.EKGURU_FAQ = faqList;

  /* --- Speakable (voice assistants) --- */
  graph.push({
    "@type": "WebPage",
    "@id": canonical + "#webpage",
    url: canonical,
    name: c.t,
    description: c.d,
    inLanguage: market.locale,
    isPartOf: { "@id": BASE + "#website" },
    about: { "@id": BASE + "#organization" },
    speakable: {
      "@type": "SpeakableSpecification",
      cssSelector: ["h1", ".pf-headline", ".lead", ".sec-head p"]
    },
    potentialAction: {
      "@type": "ReadAction",
      target: [canonical]
    }
  });

  /* --- HowTo: "how to start learning Hindi" — earns a rich result --- */
  if (pg === "index.html") {
    graph.push({
      "@type": "HowTo",
      "@id": BASE + "#howto",
      name: "How to start learning Hindi online with a private tutor",
      description: "Three steps to request a first one-to-one Hindi lesson from a tutor profile.",
      totalTime: "PT10M",
      step: [
        { "@type": "HowToStep", position: 1, name: "Choose your tutor",
          text: "Browse tutor profiles, check the stated background, terms and any reviews, then choose the teacher who fits your goal.",
          url: BASE + "find-tutors.html" },
        { "@type": "HowToStep", position: 2, name: "Send an enquiry",
          text: "Open a tutor profile, include your timezone and preferred times, and send a lesson enquiry.",
          url: BASE + "find-tutors.html" },
        { "@type": "HowToStep", position: 3, name: "Confirm current details",
          text: "Wait for confirmation of the current price, format and availability before booking.",
          url: BASE }
      ]
    });
  }

  /* --- Founder: Person entity, knowledge-graph eligible --- */
  var F = S.founder || {};
  if (F.name) {
    meta("name", "author", F.displayName || F.name);
    meta("name", "designer", F.name);
    meta("name", "owner", F.name);
    meta("property", "article:author", F.name);
    meta("property", "og:article:author", F.name);

    graph.push({
      "@type": "Person",
      "@id": BASE + "#founder",
      name: F.name,
      alternateName: [F.displayName, F.name + " MNIT Jaipur", F.name + " EkGuru"].filter(Boolean),
      jobTitle: F.title || "Founder",
      description: F.bio || "",
      email: F.email || S.email,
      worksFor: { "@id": BASE + "#organization" },
      founder: true,
      knowsAbout: ["Hindi language education", "EdTech", "Online tutoring platforms",
        "Computer Science and Engineering", "Software engineering", "Startups in India"],
      alumniOf: {
        "@type": "CollegeOrUniversity",
        name: F.college || "Malaviya National Institute of Technology Jaipur",
        alternateName: F.collegeShort || "MNIT Jaipur",
        url: F.collegeUrl || "https://www.mnit.ac.in/",
        address: { "@type": "PostalAddress", addressLocality: "Jaipur",
                   addressRegion: "Rajasthan", addressCountry: "IN" }
      },
      hasCredential: {
        "@type": "EducationalOccupationalCredential",
        credentialCategory: "degree",
        educationalLevel: "Bachelor of Technology",
        about: F.degree || "Computer Science & Engineering",
        recognizedBy: { "@type": "CollegeOrUniversity", name: F.collegeShort || "MNIT Jaipur" },
        dateCreated: String(F.batch || "2022-2026").split(/[-–]/).pop().trim()
      },
      address: { "@type": "PostalAddress", addressLocality: "Jaipur",
                 addressRegion: "Rajasthan", addressCountry: "IN" },
      birthPlace: (function () {
        var b = F.birthplace || {};
        if (!b.village) return undefined;
        return {
          "@type": "Place",
          name: [b.hamlet, b.village, b.district].filter(Boolean).join(", "),
          address: {
            "@type": "PostalAddress",
            streetAddress: b.hamlet || undefined,
            addressLocality: b.village,
            addressRegion: b.state || "Rajasthan",
            postalCode: b.pincode,
            addressCountry: "IN"
          },
          containedInPlace: {
            "@type": "AdministrativeArea",
            name: (b.district || "Dausa") + " district, " + (b.state || "Rajasthan") + ", India"
          }
        };
      })(),
      nationality: { "@type": "Country", name: "India" },
      sameAs: [F.linkedin, F.twitter, S.youtubeChannel].filter(Boolean)
    });
    ORG.founder = { "@id": BASE + "#founder" };
    ORG.employee = { "@id": BASE + "#founder" };
  }

  /* --- topical entities so Google understands the subject matter --- */
  var ENG = window.EkGuruSEO;
  if (ENG && ENG.entities) {
    ORG.knowsAbout = ENG.entities();
  }

  jsonld("ekguru-jsonld", { "@context": "https://schema.org", "@graph": graph });

  /* expose for main.js */
  window.EKGURU_LANG = L;
  window.EKGURU_MARKET = market;

  /* =========================================================
     RE-RESOLVE THE PRICE TOKENS WHEN THE SHEET LANDS  (v63)
     ---------------------------------------------------------
     THE HALF-FIX THAT WOULD HAVE SHIPPED WITHOUT THIS.

     Tokenising the strings was not enough. This file runs at page
     load; js/sheet.js answers a few hundred milliseconds later. So
     on a FIRST visit — every visitor from Google — the description
     and the FAQ schema were resolved against the tutor FILES, not
     the sheet.

     Caught by testing it properly: with the sheet saying the
     cheapest tutor was $22, the visible prose said $22 (main.js
     repaints) while the meta description and the FAQPage schema
     both still said $8. Half the page telling the truth is not a
     fix; it is a harder bug to find later.

     So the same three things are rewritten on ekguru:sheet. They
     are cheap string swaps on tags that are already in the head.

     Why the schema is rebuilt rather than patched: it is one JSON
     blob, and a regex over published structured data is how you
     end up with invalid JSON in front of Google. jsonld() replaces
     the whole node by id, which is atomic. */
  function refreshPriceClaims() {
    try {
      var raw = copyFor();
      var t = fillTokens(raw.t), d = fillTokens(raw.d);

      if (document.title !== t) document.title = t;
      meta("name", "description", d);
      meta("name", "DC.description", d);
      meta("property", "og:title", t);
      meta("property", "og:description", d);
      meta("name", "twitter:title", t);
      meta("name", "twitter:description", d);

      /* The FAQ cost answer carries {minPrice} and is published as
         FAQPage schema, so Google can quote it as a direct answer
         without the visitor ever loading the page. A stale figure
         here is the single most consequential place a wrong price
         can sit.

         The FAQ is one node inside the single #ekguru-jsonld @graph,
         not a script of its own — so find it by @type and rewrite
         the whole blob. Never patch published structured data with
         a regex; that is how you ship invalid JSON to Google. */
      var node = document.getElementById("ekguru-jsonld");
      if (node) {
        var data = JSON.parse(node.textContent);
        var faq = (data["@graph"] || []).filter(function (x) {
          return x["@type"] === "FAQPage";
        })[0];
        /* Rebuild from the SOURCE strings, not from what is in the
           document. The tokens there were already resolved on the
           first pass, so filling them again would find nothing and
           silently leave the old figure — a fix that quietly does
           nothing is worse than no fix, because the test passes. */
        var src = FAQ[L] || FAQ.en;
        if (faq && Array.isArray(faq.mainEntity) && faq.mainEntity.length === src.length) {
          faq.mainEntity = src.map(function (qa) {
            return {
              "@type": "Question",
              name: fillTokens(qa[0]),
              acceptedAnswer: { "@type": "Answer", text: fillTokens(qa[1]) }
            };
          });
          node.textContent = JSON.stringify(data);
        }
      }
    } catch (e) {
      /* A failure here must never take the page down — the tags
         already hold the previous, valid values. */
      if (window.console && console.warn) console.warn("[EkGuru seo] price refresh", e);
    }
  }

  window.addEventListener("ekguru:sheet", refreshPriceClaims);
})();
