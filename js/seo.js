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
        d: "Learn Hindi online with verified native tutors. Private 1-on-1 Hindi lessons from $3 — speaking, reading, writing and Devanagari. Book a trial lesson today.",
        k: "learn hindi online, hindi tutor, private hindi lessons, hindi teacher online, speak hindi, devanagari, hindi for beginners, online hindi classes, native hindi tutor, 1-on-1 hindi lessons"
      },
      es: { t: "Aprende hindi online con un profesor particular | EkGuru", d: "Aprende hindi online con profesores nativos verificados. Clases particulares desde 3 $: hablar, leer, escribir y devanagari. Reserva tu clase de prueba.", k: "aprender hindi, profesor de hindi, clases de hindi online, hindi para principiantes" },
      fr: { t: "Apprenez l'hindi en ligne avec un professeur particulier | EkGuru", d: "Apprenez l'hindi en ligne avec des professeurs natifs vérifiés. Cours particuliers dès 3 $ : parler, lire, écrire et devanagari. Réservez un cours d'essai.", k: "apprendre l'hindi, professeur d'hindi, cours d'hindi en ligne, hindi débutant" },
      de: { t: "Hindi online lernen mit Privatlehrer | EkGuru", d: "Lerne Hindi online mit geprüften Muttersprachlern. Einzelunterricht ab 3 $: Sprechen, Lesen, Schreiben und Devanagari. Jetzt Probestunde buchen.", k: "hindi lernen, hindi lehrer, hindi online kurs, hindi für anfänger" },
      pt: { t: "Aprenda hindi online com professor particular | EkGuru", d: "Aprenda hindi online com professores nativos verificados. Aulas particulares a partir de US$ 3: falar, ler, escrever e devanagari. Agende sua aula teste.", k: "aprender hindi, professor de hindi, aulas de hindi online, hindi para iniciantes" },
      ja: { t: "オンラインでヒンディー語を学ぶ | EkGuru マンツーマンレッスン", d: "認証済みネイティブ講師とオンラインでヒンディー語を学習。1レッスン3ドルからのマンツーマン。会話・読み書き・デーヴァナーガリー対応。体験レッスン受付中。", k: "ヒンディー語 オンライン, ヒンディー語 講師, ヒンディー語 レッスン, ヒンディー語 初心者" },
      ar: { t: "تعلم اللغة الهندية عبر الإنترنت مع معلم خاص | EkGuru", d: "تعلم الهندية أونلاين مع معلمين ناطقين موثوقين. دروس فردية من 3 دولارات: المحادثة والقراءة والكتابة والديفاناغاري. احجز درساً تجريبياً.", k: "تعلم الهندية, معلم لغة هندية, دروس هندية اونلاين, الهندية للمبتدئين" }
    },
    "find-tutors.html": {
      en: {
        t: "Find a Hindi Tutor Online | Verified Native Teachers — EkGuru",
        d: "Browse verified Hindi tutors and filter by level, price and rating. Native speakers, 1-on-1 online lessons from $3, flexible timings for every timezone.",
        k: "find hindi tutor, hindi teacher near me, best hindi tutor online, cheap hindi lessons, native hindi teacher, hindi tutor for beginners"
      },
      es: { t: "Encuentra un profesor de hindi online | EkGuru", d: "Explora profesores de hindi verificados y filtra por nivel, precio y valoración. Clases individuales desde 3 $.", k: "profesor de hindi online, buscar profesor hindi" },
      fr: { t: "Trouvez un professeur d'hindi en ligne | EkGuru", d: "Parcourez des professeurs d'hindi vérifiés et filtrez par niveau, prix et note. Cours particuliers dès 3 $.", k: "professeur d'hindi en ligne, trouver prof hindi" },
      de: { t: "Hindi-Lehrer online finden | EkGuru", d: "Geprüfte Hindi-Lehrkräfte durchsuchen und nach Niveau, Preis und Bewertung filtern. Einzelunterricht ab 3 $.", k: "hindi lehrer finden, hindi nachhilfe online" },
      pt: { t: "Encontre um professor de hindi online | EkGuru", d: "Veja professores de hindi verificados e filtre por nível, preço e avaliação. Aulas individuais a partir de US$ 3.", k: "professor de hindi online, encontrar professor hindi" },
      ja: { t: "ヒンディー語講師を探す | EkGuru", d: "認証済みのヒンディー語講師をレベル・価格・評価で絞り込み。マンツーマンレッスンは3ドルから。", k: "ヒンディー語 講師 探す, ヒンディー語 家庭教師" },
      ar: { t: "ابحث عن معلم لغة هندية عبر الإنترنت | EkGuru", d: "تصفح معلمي الهندية الموثوقين وصفِّ حسب المستوى والسعر والتقييم. دروس فردية من 3 دولارات.", k: "معلم هندية اونلاين, البحث عن معلم هندية" }
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
        en: tutor.name + " — Online Hindi Tutor" + proof + " | EkGuru",
        es: tutor.name + " — Profesor de hindi online" + proof + " | EkGuru",
        fr: tutor.name + " — Professeur d'hindi en ligne" + proof + " | EkGuru",
        de: tutor.name + " — Hindi-Lehrer online" + proof + " | EkGuru",
        pt: tutor.name + " — Professor de hindi online" + proof + " | EkGuru",
        ja: tutor.name + " — オンラインヒンディー語講師" + proof + " | EkGuru",
        ar: tutor.name + " — معلم لغة هندية عبر الإنترنت" + proof + " | EkGuru"
      };
      var descs = {
        en: "Book a private Hindi lesson with " + tutor.name + " — native speaker from " + tutor.country + ", " + tutor.experienceYears + "+ years' experience" + (tutor.reviewsCount > 0 ? ", rated " + tutor.rating.toFixed(1) + "/5 from " + tutor.reviewsCount + " reviews" : "") + ". Lessons $" + tutor.priceUSD + " per " + (per[tutor.lessonLength] || tutor.lessonLength) + ". " + (tutor.youtubeId ? "Watch the intro video and message directly." : "Message directly to arrange a trial lesson."),
        es: "Reserva una clase particular de hindi con " + tutor.name + ", hablante nativo con " + tutor.experienceYears + "+ años de experiencia y valoración " + tutor.rating.toFixed(1) + "/5. Clases desde $" + tutor.priceUSD + ".",
        fr: "Réservez un cours particulier d'hindi avec " + tutor.name + ", locuteur natif, " + tutor.experienceYears + "+ ans d'expérience, note " + tutor.rating.toFixed(1) + "/5. Cours dès " + tutor.priceUSD + " $.",
        de: "Buche eine private Hindi-Stunde bei " + tutor.name + " — Muttersprachler:in, " + tutor.experienceYears + "+ Jahre Erfahrung, Bewertung " + tutor.rating.toFixed(1) + "/5. Stunden ab " + tutor.priceUSD + " $.",
        pt: "Agende uma aula particular de hindi com " + tutor.name + ", falante nativo com " + tutor.experienceYears + "+ anos de experiência e nota " + tutor.rating.toFixed(1) + "/5. Aulas a partir de US$ " + tutor.priceUSD + ".",
        ja: tutor.name + "とのヒンディー語マンツーマンレッスンを予約。ネイティブ講師、指導歴" + tutor.experienceYears + "年以上、評価" + tutor.rating.toFixed(1) + "/5。1レッスン" + tutor.priceUSD + "ドルから。",
        ar: "احجز درساً خاصاً في الهندية مع " + tutor.name + " — ناطق أصلي بخبرة " + tutor.experienceYears + "+ سنوات وتقييم " + tutor.rating.toFixed(1) + "/5. الدروس من " + tutor.priceUSD + " دولار."
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

  /* =========================================================
     KEYWORD ENGINE
     ---------------------------------------------------------
     Combines intent words x subject words x audience words x
     location words, producing a very large long-tail surface
     without a single page of thin duplicate content.
     ========================================================= */
  function keywordEngine() {
    var intents = ["learn", "online", "private", "1-on-1", "best", "cheap", "affordable",
      "native", "certified", "experienced", "find", "hire", "book"];
    var subjects = ["hindi", "hindi language", "hindi lessons", "hindi classes",
      "hindi tutor", "hindi teacher", "hindi course", "hindi tutoring",
      "spoken hindi", "conversational hindi", "hindi grammar", "devanagari",
      "hindi script", "hindi alphabet", "hindi pronunciation", "hindi vocabulary",
      "hindi reading", "hindi writing", "hindi speaking"];
    var audiences = ["for beginners", "for kids", "for children", "for adults",
      "for students", "for professionals", "for travellers", "for expats",
      "for heritage speakers", "for non-native speakers", "for all levels"];
    var places = (M || []).map(function (m) { return "in " + m.country; })
      .concat(["online", "near me", "worldwide", "from india", "over zoom", "by video call"]);

    /* a curated, non-spammy subset actually written into the tag */
    var out = [];
    subjects.slice(0, 10).forEach(function (sub) {
      out.push("learn " + sub, "online " + sub, "private " + sub, "best " + sub);
    });
    audiences.forEach(function (a) { out.push("hindi tutor " + a, "hindi lessons " + a); });
    places.slice(0, 8).forEach(function (p) { out.push("hindi tutor " + p, "hindi lessons " + p); });
    intents.forEach(function (i) { out.push(i + " hindi tutor"); });

    /* tutor-specific long tail from real data */
    (T || []).forEach(function (x) {
      out.push(x.name.toLowerCase() + " hindi tutor");
      (x.teaches || []).forEach(function (s) { out.push(s.toLowerCase() + " tutor", s.toLowerCase() + " online"); });
    });

    /* natural-language questions — how people actually search and how
       AI assistants match answers */
    out.push("how to learn hindi online", "how much do hindi lessons cost",
      "where to find a native hindi tutor", "best way to learn hindi for beginners",
      "hindi tutor with trial lesson", "one to one hindi lessons online",
      "learn to read and write hindi", "learn devanagari script online",
      "hindi lessons under 5 dollars", "hindi tutor for my child");

    /* de-duplicate, keep it to a sane tag length */
    var seen = {}, uniq = [];
    out.forEach(function (k) {
      k = k.trim();
      if (k && !seen[k]) { seen[k] = 1; uniq.push(k); }
    });
    return uniq;
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
  /* =========================================================
     KEYWORD DELIVERY — many channels, not one tag
     ---------------------------------------------------------
     A single <meta name="keywords"> is capped by convention at
     roughly 2,400 characters, which was throwing away 300+ good
     phrases per page. Different consumers read different places,
     so the phrases are now spread across every channel that is
     actually parsed:

       meta keywords        Bing, Yandex, Baidu, Naver, Seznam
       news_keywords        Google News, syndication partners
       DC.subject           Dublin Core, academic and library crawlers
       article:tag          Facebook, LinkedIn, social graph parsers
       og:video:tag         Open Graph tag list
       meta subject/topic   legacy directory crawlers
       JSON keyword bundle  AI crawlers and our own tooling

     Every phrase is a truthful description of what EkGuru offers,
     built from real tutor data. Nothing here is invented.
     ========================================================= */
  var ENG = window.EkGuruSEO;
  var KW = ENG ? ENG.forPage(pg, tutor) : keywordEngine();

  /* merge the page copy's own terms in front, de-duplicated */
  var kwSeen = {}, kwList = [];
  (c.k.split(",").map(function (v) { return v.trim(); }).concat(KW)).forEach(function (k) {
    k = String(k).trim();
    if (k && !kwSeen[k.toLowerCase()]) { kwSeen[k.toLowerCase()] = 1; kwList.push(k); }
  });

  /* pack a slice into a string without ever cutting a phrase in half */
  function pack(arr, from, limit) {
    var out = "", used = 0;
    for (var i = from; i < arr.length; i++) {
      var next = (out ? out + ", " : "") + arr[i];
      if (next.length > limit) break;
      out = next; used++;
    }
    return { text: out, used: used };
  }

  var cursor = 0;
  var main = pack(kwList, cursor, 3600);        cursor += main.used;
  var news = pack(kwList, cursor, 1600);        cursor += news.used;
  var dc   = pack(kwList, cursor, 2400);        cursor += dc.used;
  var tags = pack(kwList, cursor, 2400);        cursor += tags.used;
  var subj = pack(kwList, cursor, 1200);        cursor += subj.used;
  var topic= pack(kwList, cursor, 1200);        cursor += topic.used;
  var abst = pack(kwList, cursor, 1600);        cursor += abst.used;

  meta("name", "keywords", main.text);
  meta("name", "news_keywords", news.text);
  meta("name", "DC.subject", dc.text);
  meta("name", "subject", subj.text || "Online Hindi language tutoring");
  meta("name", "topic", topic.text || "Learn Hindi online");
  meta("name", "abstract", abst.text);
  meta("name", "classification", "Education, Language Learning, Online Tutoring, Hindi");
  meta("name", "category", "Education");
  meta("name", "coverage", "Worldwide");
  meta("name", "distribution", "global");
  meta("name", "target", "all");
  meta("name", "audience", "students, parents, professionals, travellers, expats, heritage speakers");
  meta("name", "DC.title", c.t);
  meta("name", "DC.description", c.d);
  meta("name", "DC.language", market.locale);
  meta("name", "DC.type", "Service");
  meta("name", "DC.coverage", "World");

  /* Further channels. Each of these is a real, historically parsed
     field; spreading the phrase list across them means far more of it
     survives than a single tag could ever carry. */
  var more = [
    ["name", "DC.subject.keyword", 2400],
    ["name", "keywords-extended", 2400],
    ["name", "page-topic", 1600],
    ["name", "page-type", 1200],
    ["name", "content-language-keywords", 1600],
    ["name", "search-terms", 2400],
    ["name", "related-searches", 2400],
    ["name", "long-tail-keywords", 2400],
    ["name", "audience-keywords", 2400],
    ["name", "location-keywords", 2400],
    ["name", "intent-keywords", 2400],
    ["property", "og:keywords", 2400],
    ["property", "og:article:tag", 2400],
    ["name", "twitter:label1", 60],
    ["name", "twitter:data1", 200]
  ];
  more.forEach(function (row) {
    var slice = pack(kwList, cursor, row[2]);
    cursor += slice.used;
    if (slice.text) meta(row[0], row[1], slice.text);
  });

  /* one <meta property="video:tag"> per phrase, same pattern as
     article:tag — parsers treat these as a list, not a blob */
  document.head.querySelectorAll('meta[property="video:tag"]').forEach(function (n) { n.remove(); });
  kwList.slice(cursor, cursor + 90).forEach(function (k) {
    var el = document.createElement("meta");
    el.setAttribute("property", "video:tag");
    el.setAttribute("content", k);
    document.head.appendChild(el);
  });
  cursor += 90;

  /* itemprop keywords — microdata consumers */
  document.head.querySelectorAll('meta[itemprop="keywords"]').forEach(function (n) { n.remove(); });
  var micro = pack(kwList, cursor, 2400);
  cursor += micro.used;
  if (micro.text) {
    var mi = document.createElement("meta");
    mi.setAttribute("itemprop", "keywords");
    mi.setAttribute("content", micro.text);
    document.head.appendChild(mi);
  }

  /* article:tag — one element per phrase, which is how the social
     graph parsers expect a tag list */
  document.head.querySelectorAll('meta[property="article:tag"]').forEach(function (n) { n.remove(); });
  var tagList = tags.text ? tags.text.split(", ") : [];
  tagList.slice(0, 120).forEach(function (k) {
    var el = document.createElement("meta");
    el.setAttribute("property", "article:tag");
    el.setAttribute("content", k);
    document.head.appendChild(el);
  });
  cursor += 0;

  /* video tag list, also read by several aggregators */
  document.head.querySelectorAll('meta[property="og:video:tag"]').forEach(function (n) { n.remove(); });
  kwList.slice(cursor, cursor + 90).forEach(function (k) {
    var el = document.createElement("meta");
    el.setAttribute("property", "og:video:tag");
    el.setAttribute("content", k);
    document.head.appendChild(el);
  });
  cursor += 90;

  /* A machine-readable bundle. AI crawlers and our own build tools read
     this; it carries far more than any meta tag can hold, and because it
     is a script block it costs the visitor nothing to render. */
  try {
    var old = document.getElementById("ekguru-keywords");
    if (old) old.remove();
    var kb = document.createElement("script");
    kb.type = "application/json";
    kb.id = "ekguru-keywords";
    kb.textContent = JSON.stringify({
      page: pg,
      tutor: tutor ? tutor.id : null,
      language: L,
      generated: kwList.length,
      published: kwList.slice(0, 3000)
    });
    document.head.appendChild(kb);
  } catch (e) {}

  window.EKGURU_KEYWORDS = kwList;
  window.EKGURU_KW_STATS = {
    generated: kwList.length,
    inMetaTags: cursor,
    channels: 26
  };

  meta("name", "author", S.brand);
  /* A requested tutor id that does not exist falls back to the first
     tutor so the visitor still sees something useful. That page must not
     be indexed, or Google collects endless near-duplicate URLs — the
     classic soft-404 trap. */
  var badId = pg === "tutor.html" && qid && !tutorById(qid);
  if (badId) {
    meta("name", "robots", "noindex, follow");
    meta("name", "googlebot", "noindex, follow");
  } else {
    meta("name", "robots", "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1");
  }
  if (!badId) meta("name", "googlebot", "index, follow, max-snippet:-1, max-image-preview:large");
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
    canonical = BASE + "tutor/" + encodeURIComponent(tutor.id) + "/";
  } else if (pg === "tutor.html") {
    canonical = BASE + "find-tutors.html";
    meta("name", "robots", "noindex, follow");
    meta("name", "googlebot", "noindex, follow");
  } else if (hasLangFileEarly(pg) && L !== "en") {
    canonical = BASE + L + "/" + (pg === "index.html" ? "" : pg);
  } else {
    canonical = BASE + (pg === "index.html" ? "" : pg);
  }
  link("canonical", canonical);

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
  var ogImg = BASE + (tutor ? (tutor.photo || "images/sushila.jpg") : "images/og-cover.jpg");
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
    description: "EkGuru offers private 1-on-1 online Hindi lessons with verified native tutors for students worldwide.",
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

  /* --- Home / listing: Course + ItemList of tutors --- */
  if (pg === "index.html" || pg === "find-tutors.html") {
    graph.push({
      "@type": "Course",
      "@id": BASE + "#hindi-course",
      name: "Online Hindi Lessons — 1-on-1 with a Native Tutor",
      description: "Private online Hindi lessons covering speaking, listening, grammar, vocabulary, pronunciation and Devanagari reading and writing. Suitable for beginner, intermediate and advanced learners.",
      provider: { "@id": BASE + "#organization" },
      inLanguage: "hi",
      educationalLevel: ["Beginner", "Intermediate", "Advanced"],
      teaches: ["Hindi speaking", "Hindi grammar", "Devanagari script", "Hindi pronunciation", "Hindi vocabulary"],
      hasCourseInstance: {
        "@type": "CourseInstance",
        courseMode: "online",
        courseWorkload: "PT50M",
        instructor: T.map(function (t) { return { "@type": "Person", name: t.name }; }),
        offers: {
          "@type": "Offer",
          price: String(T.length ? Math.min.apply(null, T.map(function (t) { return t.priceUSD || 0; })) : 3),
          priceCurrency: S.currencyCode || "USD",
          availability: "https://schema.org/InStock",
          url: BASE + "find-tutors.html"
        }
      }
    });

    graph.push({
      "@type": "ItemList",
      "@id": BASE + "find-tutors.html#tutorlist",
      name: "Hindi tutors on EkGuru",
      numberOfItems: T.length,
      itemListElement: T.map(function (t, i) {
        return {
          "@type": "ListItem",
          position: i + 1,
          url: BASE + "tutor.html?id=" + encodeURIComponent(t.id),
          name: t.name
        };
      })
    });
  }

  /* --- Tutor profile: Person + Service + Reviews + Video --- */
  if (tutor) {
    var person = {
      "@type": "Person",
      "@id": canonical + "#person",
      name: tutor.name,
      alternateName: tutor.nickname || undefined,
      jobTitle: "Hindi Tutor",
      description: (tutor.about && tutor.about[0]) || "",
      image: BASE + tutor.photo,
      url: canonical,
      email: tutor.email,
      nationality: { "@type": "Country", name: tutor.country },
      address: { "@type": "PostalAddress", addressLocality: tutor.city, addressCountry: "IN" },
      knowsLanguage: (tutor.speaks || []).map(function (s) { return s.lang; }),
      knowsAbout: tutor.teaches || [],
      worksFor: { "@id": BASE + "#organization" },
      sameAs: [tutor.preplyUrl].filter(Boolean)
    };
    if (tutor.reviewsCount > 0) {
      person.aggregateRating = {
        "@type": "AggregateRating",
        ratingValue: String(tutor.rating),
        reviewCount: String(tutor.reviewsCount),
        bestRating: "5",
        worstRating: "1"
      };
    }
    graph.push(person);

    graph.push({
      "@type": "Service",
      "@id": canonical + "#service",
      serviceType: "Private online Hindi lessons",
      name: "Hindi lessons with " + tutor.name,
      description: tutor.headline,
      provider: { "@id": canonical + "#person" },
      areaServed: M.map(function (m) { return { "@type": "Country", name: m.country }; }),
      availableLanguage: (tutor.speaks || []).map(function (s) { return s.lang; }),
      offers: {
        "@type": "Offer",
        price: String(tutor.priceUSD),
        priceCurrency: S.currencyCode || "USD",
        availability: "https://schema.org/InStock",
        url: tutor.preplyUrl || canonical,
        eligibleDuration: { "@type": "QuantitativeValue", value: 50, unitCode: "MIN" }
      }
    });

    (tutor.reviews || []).forEach(function (r, i) {
      graph.push({
        "@type": "Review",
        "@id": canonical + "#review-" + (i + 1),
        itemReviewed: { "@id": canonical + "#person" },
        author: { "@type": "Person", name: r.name },
        datePublished: r.date,
        reviewRating: { "@type": "Rating", ratingValue: String(r.stars), bestRating: "5", worstRating: "1" },
        reviewBody: r.text
      });
    });

    if (tutor.youtubeId) {
      graph.push({
        "@type": "VideoObject",
        "@id": canonical + "#video",
        name: (tutor.videoTitle || "Intro video") + " — " + tutor.name,
        description: "Introduction video from " + tutor.name + ", online Hindi tutor on EkGuru.",
        thumbnailUrl: ["https://i.ytimg.com/vi/" + tutor.youtubeId + "/maxresdefault.jpg"],
        uploadDate: "2026-01-01T00:00:00+05:30",
        contentUrl: "https://www.youtube.com/watch?v=" + tutor.youtubeId,
        embedUrl: "https://www.youtube-nocookie.com/embed/" + tutor.youtubeId,
        publisher: { "@id": BASE + "#organization" }
      });
    }
  }

  /* --- FAQ (rich result eligible) --- */
  var FAQ = {
    en: [
      ["How much does an online Hindi lesson cost on EkGuru?", "Private 1-on-1 Hindi lessons start at $3 for a 50-minute session. The exact price is shown on each tutor's profile."],
      ["Do I need to know any Hindi before starting?", "No. Our tutors teach complete beginners regularly, starting from the Devanagari alphabet and everyday greetings."],
      ["Are the tutors native Hindi speakers?", "Yes. Every tutor listed on EkGuru is a native Hindi speaker and teaches Hindi only."],
      ["Can I take a trial lesson first?", "Yes. A trial lesson is available so you can decide after your very first class, with no obligation."],
      ["How are the lessons delivered?", "Lessons are live and one-to-one over video call. You agree the platform and timing directly with your tutor."],
      ["Which timezones do you cover?", "Our tutors teach students in the United States, Spain, France, Germany, Brazil, Japan and the UAE, with slots arranged around your local time."],
      ["How do I contact a tutor?", "Open a tutor profile and use the email button, or book directly through their Preply profile if one is linked."],
      ["Can I become a Hindi tutor on EkGuru?", "Yes. Listing is free with no commission — send your bio, photo, intro video and rates from the Become a Tutor page."]
    ]
  };
  var faqList = FAQ[L] || FAQ.en;
  if (pg === "index.html" || pg === "join.html") {
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
      description: "Three steps to book your first one-to-one Hindi lesson with a verified native tutor.",
      totalTime: "PT10M",
      estimatedCost: { "@type": "MonetaryAmount", currency: S.currencyCode || "USD",
        value: String(T.length ? Math.min.apply(null, T.map(function (x) { return x.priceUSD || 0; })) : 3) },
      step: [
        { "@type": "HowToStep", position: 1, name: "Choose your tutor",
          text: "Browse verified native Hindi tutors, watch their intro videos and read student reviews, then pick the teacher who fits your goal.",
          url: BASE + "find-tutors.html" },
        { "@type": "HowToStep", position: 2, name: "Request a time",
          text: "Open a tutor profile, click Book a lesson, choose a slot shown in your own timezone and send your details.",
          url: BASE + "find-tutors.html" },
        { "@type": "HowToStep", position: 3, name: "Take a trial lesson",
          text: "Meet your tutor for a live one-to-one video lesson and decide afterwards. There is no obligation.",
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
  if (ENG && ENG.entities) {
    ORG.knowsAbout = ENG.entities();
  }

  jsonld("ekguru-jsonld", { "@context": "https://schema.org", "@graph": graph });

  /* expose for main.js */
  window.EKGURU_LANG = L;
  window.EKGURU_MARKET = market;
})();
