/* =========================================================
   EkGuru — Advanced SEO engine
   ---------------------------------------------------------
   Runs before main.js. Injects per-page metadata, canonical/hreflang,
   social cards and JSON-LD. Homepage copy comes from js/i18n.js; tutor
   profiles use the public tutor data. FAQ/HowTo markup is emitted only
   when it matches visible course content. No tutor Offer/Service/Rating
   claims are generated here.
   ========================================================= */
(function () {
  "use strict";

  var S = window.EKGURU_SITE || {};
  var M = window.EKGURU_MARKETS || [];
  var T = window.EKGURU_TUTORS || [];
  var I18N = window.EKGURU_I18N || {};
  var BASE = (S.baseUrl || "").replace(/\/?$/, "/");

  /* ---------- helpers ---------- */
  function page() {
    var p = location.pathname.split("/").pop();
    return (!p || p === "") ? "index.html" : p;
  }
  function lang() {
    try {
      var q = new URLSearchParams(location.search).get("lang");
      if (q && M.some(function (m) { return m.code === q; })) return q;
    } catch (e) {}

    /* The translated directory is authoritative. A saved preference must
       not make /es/ return English metadata while the page itself is Spanish. */
    var parts = location.pathname.split("/").filter(Boolean);
    for (var i = 0; i < M.length; i++) {
      if (parts[0] === M[i].code) return M[i].code;
    }

    try {
      var s = localStorage.getItem("ekguru_lang");
      if (s && M.some(function (m) { return m.code === s; })) return s;
    } catch (e) {}
    var nav = (navigator.language || "en").slice(0, 2);
    for (var j = 0; j < M.length; j++) if (M[j].code === nav) return nav;
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

  function directoryCopy(locale) {
    var live = window.EKGURU_TUTORS;
    var hasPublicTutors = Array.isArray(live) && live.length > 0;
    var prefix = hasPublicTutors ? "seo.findActive" : "seo.findEmpty";
    var pack = I18N[locale] || I18N.en || {};
    var fallback = I18N.en || {};
    return {
      t: pack[prefix + "Title"] || fallback[prefix + "Title"] || "Hindi tutor directory | EkGuru",
      d: pack[prefix + "Description"] || fallback[prefix + "Description"] || "Tutor profiles are listed here when public. Free Hindi lessons and self-study tools are available.",
      k: "Hindi tutor directory, Hindi course, Hindi learning"
    };
  }

  function homeCopy(locale) {
    var pack = I18N[locale] || I18N.en || {};
    var fallback = I18N.en || {};
    return {
      t: pack["seo.homeTitle"] || fallback["seo.homeTitle"] || "Learn Hindi Online — Free Course | EkGuru",
      d: pack["seo.homeDescription"] || fallback["seo.homeDescription"] || "Start a free, self-paced Hindi course with lessons, practice and learning tools. No subscription or account required.",
      k: "learn Hindi online, free Hindi course, Devanagari, Hindi practice"
    };
  }

  function copyFor() {
    if (pg === "index.html") return homeCopy(L);
    if (pg === "find-tutors.html") return directoryCopy(L);
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
    var block = COPY[pg];
    return block ? (block[L] || block.en) : homeCopy("en");
  }

  /* which pages have a real translated file on disk */
  function hasLangFileEarly(page) {
    return ["index.html", "find-tutors.html", "join.html"].indexOf(page) > -1;
  }

  var c = copyFor();

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
    description: "EkGuru publishes free Hindi lessons, self-paced courses, practice and learning tools.",
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
     inventory, so do not emit Offer, Service, AggregateRating or Review data.
     27 Sep 2026 master audit — no "profile excerpt" meta-label in the
     description and no sameAs to an external marketplace profile (the
     sheet gate in js/sheet.js refuses preplyUrl anyway). --- */
  if (tutor) {
    graph.push({
      "@type": "Person",
      "@id": canonical + "#person",
      name: tutor.name,
      alternateName: tutor.nickname || undefined,
      jobTitle: "Hindi Tutor",
      description: (tutor.about && tutor.about[0]) || "",
      image: absUrl(tutor.photo),
      url: canonical,
      knowsLanguage: (tutor.speaks || []).map(function (s) { return s.lang; }),
      knowsAbout: tutor.teaches || []
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

  /* FAQ copy comes from the same localized strings used by the visible home
     page. The availability answer follows the PUBLIC roster and is refreshed
     when the sheet changes. Schema is emitted only where the FAQ is visible. */
  function translated(key) {
    var pack = I18N[L] || {};
    if (pack[key] != null) return pack[key];
    return (I18N.en && I18N.en[key]) || key;
  }
  function homeFaq() {
    var live = window.EKGURU_TUTORS;
    var hasPublicTutors = Array.isArray(live) && live.length > 0;
    var list = [];
    for (var i = 1; i <= 6; i++) {
      var suffix = i === 5 ? (hasPublicTutors ? "available" : "empty") : "a";
      list.push([translated("home.faq." + i + ".q"), translated("home.faq." + i + "." + suffix)]);
    }
    return list;
  }
  var faqList = homeFaq();
  if (pg === "index.html" && document.getElementById("faq-list")) {
    graph.push({
      "@type": "FAQPage",
      "@id": canonical + "#faq",
      mainEntity: faqList.map(function (q) {
        return { "@type": "Question", name: q[0], acceptedAnswer: { "@type": "Answer", text: q[1] } };
      })
    });
  }
  window.EKGURU_FAQ = faqList;

  /* --- HowTo mirrors the three visible self-study steps below. --- */
  if (pg === "index.html" && document.getElementById("how")) {
    var howPack = I18N[L] || I18N.en || {};
    function howText(key) { return howPack[key] || (I18N.en && I18N.en[key]) || ""; }
    var howSteps = [1, 2, 3].map(function (position) {
      return {
        "@type": "HowToStep",
        position: position,
        name: howText("how.s" + position + "t"),
        text: howText("how.s" + position + "d")
      };
    });
    if (howSteps.every(function (step) { return step.name && step.text; })) {
      graph.push({
        "@type": "HowTo",
        "@id": canonical + "#howto",
        name: howText("how.title"),
        description: howText("how.sub"),
        step: howSteps
      });
    }
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

  /* The sheet can change which tutor profiles are public after the first
     paint. Refresh roster-aware metadata and the homepage availability FAQ
     together. Home copy stays course-first; directory copy follows the public
     roster without inventing price, rating, or current availability claims. */
  function refreshLocalizedCopy() {
    try {
      var raw = copyFor();
      var title = raw.t, description = raw.d;
      if (document.title !== title) document.title = title;
      meta("name", "description", description);
      meta("name", "DC.description", description);
      meta("property", "og:title", title);
      meta("property", "og:description", description);
      meta("name", "twitter:title", title);
      meta("name", "twitter:description", description);

      faqList = homeFaq();
      window.EKGURU_FAQ = faqList;
      var node = document.getElementById("ekguru-jsonld");
      if (!node) return;
      var data = JSON.parse(node.textContent);
      var faq = (data["@graph"] || []).filter(function (x) {
        return x["@type"] === "FAQPage";
      })[0];
      if (faq) {
        faq.mainEntity = faqList.map(function (qa) {
          return {
            "@type": "Question",
            name: qa[0],
            acceptedAnswer: { "@type": "Answer", text: qa[1] }
          };
        });
        node.textContent = JSON.stringify(data);
      }
    } catch (e) {
      /* Search metadata must never interrupt page rendering. */
      if (window.console && console.warn) console.warn("[EkGuru seo] copy refresh", e);
    }
  }

  window.addEventListener("ekguru:sheet", refreshLocalizedCopy);
})();
