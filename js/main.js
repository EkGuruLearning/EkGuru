/* =========================================================
   EkGuru — main.js
   Rendering · i18n · filters · profile · video · animations
   Every render is wrapped in try/catch: a failure shows a
   visible message instead of a white page.
   ========================================================= */
(function () {
  "use strict";

  /* ---------- 0. Safety net ---------- */
  function showError(where, err) {
    try {
      console.error("[EkGuru]", where, err);
      var host = document.getElementById("app-error") || document.body;
      if (host.querySelector(".errbox")) return;
      var box = document.createElement("div");
      box.className = "errbox";
      box.innerHTML =
        "<b>Something went wrong while loading this section</b>" +
        "<p>Section: <code>" + where + "</code></p>" +
        "<p>" + String(err && err.message ? err.message : err) + "</p>" +
        "<p>Check that <code>js/tutors-data.js</code> loaded correctly and contains no syntax errors.</p>";
      host.appendChild(box);
    } catch (e) {}
  }
  window.addEventListener("error", function (e) {
    if (!document.querySelector(".errbox")) showError("runtime", e.error || e.message);
  });

  /* ---------- 1. State ---------- */
  var TUTORS = Array.isArray(window.EKGURU_TUTORS) ? window.EKGURU_TUTORS : [];
  var SITE = window.EKGURU_SITE || {};
  var MARKETS = window.EKGURU_MARKETS || [];
  var I18N = window.EKGURU_I18N || {};
  var LANG = window.EKGURU_LANG || "en";
  var CUR = SITE.currency || "$";

  /* Price display. Uses the country-aware layer when it is loaded,
     otherwise falls back to plain USD so nothing can ever break. */
  function px(usd) {
    if (usd == null) return "—";
    if (window.EkGuruPrice) return window.EkGuruPrice.price(usd);
    return CUR + usd;
  }
  function pxFull(usd) {
    if (usd == null) return "—";
    if (window.EkGuruPrice) return window.EkGuruPrice.priceWithUsd(usd);
    return CUR + usd;
  }

  function t(key) {
    var pack = I18N[LANG] || {};
    if (pack[key] != null) return pack[key];
    var en = I18N.en || {};
    return en[key] != null ? en[key] : key;
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function $(s, r) { return (r || document).querySelector(s); }
  function $all(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function stars(n) {
    var f = Math.round(Number(n) || 0), s = "";
    for (var i = 0; i < 5; i++) s += i < f ? "★" : "☆";
    return s;
  }
  function hasWa(v) { return !!v && !/[xX]/.test(v) && v.replace(/\D/g, "").length >= 10; }
  function waHref(num, who) {
    return "https://wa.me/" + String(num).replace(/\D/g, "") + "?text=" +
      encodeURIComponent("Hello " + (who || "") + "! I found your profile on EkGuru and I would like to learn Hindi. Could you tell me about a trial lesson?");
  }
  function mailHref(to, subject, body) {
    return "mailto:" + (to || SITE.email) +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
  }
  function safeImg(el) {
    el.onerror = function () {
      if (el.dataset.fbk === "1") {
        el.onerror = null;
        el.src = "data:image/svg+xml;utf8," + encodeURIComponent(
          '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect width="200" height="200" fill="#5b3df5"/><circle cx="100" cy="78" r="34" fill="#fff"/><path d="M32 200a68 68 0 01136 0z" fill="#fff"/></svg>');
        return;
      }
      el.dataset.fbk = "1";
      el.src = "images/placeholder-tutor.jpg";
    };
  }
  /* banner fallback: missing banner simply hides itself, never breaks layout */
  function safeBanner(el) {
    el.onerror = function () {
      if (el.dataset.fbk === "1") {
        el.onerror = null;
        var host = el.closest(".pf-banner");
        if (host) host.remove();
        var hero = document.querySelector(".pf-hero");
        if (hero) hero.classList.remove("has-banner");
        return;
      }
      el.dataset.fbk = "1";
      el.src = "images/placeholder-banner.jpg";
    };
  }

  function langHref(file, extra) {
    var q = [];
    if (extra) q.push(extra);
    if (LANG !== "en") q.push("lang=" + LANG);
    return file + (q.length ? "?" + q.join("&") : "");
  }

  /* ---------- 2. Language switcher ---------- */
  function setLang(code) {
    try { localStorage.setItem("ekguru_lang", code); } catch (e) {}
    var u = new URL(location.href);
    u.searchParams.set("lang", code);
    location.href = u.toString();
  }

  /* globe / language icon (inline SVG so it works with no network) */
  var GLOBE =
    '<svg class="globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>' +
    '<path d="M12 3a15 15 0 010 18a15 15 0 010-18z"/></svg>';

  function buildLangSwitcher() {
    var host = $("#lang-switch");
    if (!host || !MARKETS.length) return;
    var cur = MARKETS.filter(function (m) { return m.code === LANG; })[0] || MARKETS[0];
    host.innerHTML =
      '<button class="lang-btn" type="button" aria-haspopup="listbox" aria-expanded="false" ' +
        'aria-label="' + esc(t("ftr.langs")) + ': ' + esc(cur.label) + '">' +
        GLOBE +
        '<span class="flag">' + cur.flag + "</span>" +
        '<span class="lbl">' + esc(cur.label) + "</span>" +
        '<span class="car" aria-hidden="true">▾</span>' +
      "</button>" +
      '<div class="lang-menu" role="listbox" aria-label="' + esc(t("ftr.langs")) + '">' +
        '<div class="lang-menu-head">' + GLOBE + "<span>" + esc(t("ftr.langs")) + "</span></div>" +
        MARKETS.map(function (m) {
          return '<button type="button" role="option" data-code="' + m.code + '"' +
            (m.code === LANG ? ' aria-selected="true" class="on"' : ' aria-selected="false"') + ">" +
            '<span class="flag">' + m.flag + "</span><span>" + esc(m.label) + "</span>" +
            "<small>" + esc(m.country) + '</small><span class="tick">✓</span></button>';
        }).join("") +
      "</div>";

    var btn = $(".lang-btn", host), menu = $(".lang-menu", host);
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = host.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $all("button[data-code]", menu).forEach(function (b) {
      b.addEventListener("click", function () { setLang(b.dataset.code); });
    });
    document.addEventListener("click", function () {
      host.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    });
  }

  /* ---------- 3. Static text via data-i18n ---------- */
  function applyI18n() {
    $all("[data-i18n]").forEach(function (el) { el.textContent = t(el.getAttribute("data-i18n")); });
    $all("[data-i18n-ph]").forEach(function (el) { el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph"))); });
    $all("[data-i18n-aria]").forEach(function (el) { el.setAttribute("aria-label", t(el.getAttribute("data-i18n-aria"))); });
    $all("[data-brand]").forEach(function (el) { el.textContent = SITE.brand; });
    $all("[data-tagline]").forEach(function (el) { el.textContent = SITE.tagline; });
    $all("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
    $all("[data-email]").forEach(function (el) {
      el.textContent = SITE.email;
      if (el.tagName === "A") el.href = "mailto:" + SITE.email;
    });
    /* keep nav links on the current language */
    $all("a[data-navlink]").forEach(function (a) {
      var f = a.getAttribute("data-navlink"), hash = a.getAttribute("data-hash") || "";
      a.href = langHref(f) + hash;
    });
  }

  /* ---------- 3b. Status badge + founder credit ---------- */
  function initBadges() {
    /* small launch pill next to the logo */
    var st = (SITE.status || "live").toLowerCase();
    if (st !== "live") {
      var logo = $(".hdr .logo");
      if (logo && !$(".status-pill", logo.parentNode)) {
        var pill = document.createElement("span");
        pill.className = "status-pill " + (st === "beta" ? "is-beta" : "is-soon");
        pill.textContent = st === "beta" ? t("status.beta") : t("status.soon");
        pill.title = t("status.tip");
        logo.parentNode.insertBefore(pill, logo.nextSibling);
      }
    }

    /* founder line in the footer */
    var F = SITE.founder;
    if (!F || !F.name) return;
    $all("[data-founder]").forEach(function (el) {
      /* the founder's name links to their LinkedIn when one is set — this
         is a real, verifiable identity signal for Google's knowledge graph */
      var nameHtml = F.linkedin
        ? '<a class="fdr-name" href="' + esc(F.linkedin) + '" target="_blank" rel="me noopener">' + esc(F.name) + "</a>"
        : '<strong class="fdr-name">' + esc(F.name) + "</strong>";
      el.innerHTML =
        '<span class="fdr-lbl">' + esc(t("founder.by")) + "</span> " +
        nameHtml +
        '<span class="fdr-sep">·</span>' +
        '<a class="fdr-col" href="' + esc(F.collegeUrl || "#") + '" target="_blank" rel="noopener">' +
          esc(F.collegeShort) + "</a>" +
        '<span class="fdr-sep">·</span>' +
        '<span class="fdr-deg">' + esc(t("founder.cse")) + " " + esc(F.batch) + "</span>";
    });
  }

  /* ---------- 4. Header ---------- */
  function initHeader() {
    var b = $(".burger"), nav = $(".nav");
    if (b && nav) {
      b.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        b.setAttribute("aria-expanded", open ? "true" : "false");
        document.body.classList.toggle("nav-open", open);
      });
      function closeNav() {
        nav.classList.remove("open");
        b.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-open");
      }
      $all("a", nav).forEach(function (a) { a.addEventListener("click", closeNav); });
      /* close on Escape, and when tapping outside the drawer */
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && nav.classList.contains("open")) closeNav();
      });
      document.addEventListener("click", function (e) {
        if (!nav.classList.contains("open")) return;
        if (nav.contains(e.target) || b.contains(e.target)) return;
        closeNav();
      });
      /* if the window grows past the drawer breakpoint, reset cleanly */
      window.addEventListener("resize", function () {
        if (window.innerWidth > 1080 && nav.classList.contains("open")) closeNav();
      });
    }
    var pg = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    $all(".nav a[data-navlink]").forEach(function (a) {
      if (a.getAttribute("data-navlink").toLowerCase() === pg && !a.getAttribute("data-hash")) a.classList.add("active");
    });
  }

  /* ---------- 5. Scroll reveal ---------- */
  function initReveal(root) {
    var els = $all(".reveal, .stagger", root || document).filter(function (e) { return !e.classList.contains("in"); });
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("in"); }); return; }
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } });
    }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ---------- 6. Counter animation ---------- */
  /* Counts up to a figure. It starts from whatever the element already
     shows rather than from zero, because the static HTML holds the true
     number — animating down to 0 first would flash a wrong value at the
     visitor and at any crawler that runs JavaScript. */
  function countUp(el, to, suffix) {
    var current = parseInt(String(el.textContent).replace(/\D/g, ""), 10);
    if (isNaN(current) || current === to) {
      el.textContent = to + (suffix || "");
      return;
    }
    var start = null, dur = 1100, from = current < to ? 0 : current;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (to - from) * eased) + (suffix || "");
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------- 7. YouTube facade (fast, real, click-to-play) ---------- */
  function videoBlock(id, title) {
    if (!id) {
      return '<div class="video-box"><div class="video-ph"><div>' +
        '<div class="play">▶</div><b>' + esc(t("pf.videoSoon")) + "</b></div></div></div>";
    }
    return '<div class="video-box js-yt" data-yt="' + esc(id) + '" role="button" tabindex="0" aria-label="' + esc(t("pf.playVideo")) + '">' +
      '<img class="yt-thumb" src="https://i.ytimg.com/vi/' + esc(id) + '/maxresdefault.jpg" ' +
        'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/' + esc(id) + '/hqdefault.jpg\'" ' +
        'alt="' + esc(title || "Intro video") + '" loading="lazy" width="1280" height="720">' +
      '<span class="yt-play" aria-hidden="true"><svg viewBox="0 0 68 48" width="68" height="48">' +
        '<path d="M66.5 7.7a8.6 8.6 0 00-6-6C55.2 0 34 0 34 0S12.8 0 7.5 1.7a8.6 8.6 0 00-6 6A89.9 89.9 0 000 24a89.9 89.9 0 001.5 16.3 8.6 8.6 0 006 6C12.8 48 34 48 34 48s21.2 0 26.5-1.7a8.6 8.6 0 006-6A89.9 89.9 0 0068 24a89.9 89.9 0 00-1.5-16.3z" fill="#f00"/>' +
        '<path d="M27 34l18-10-18-10z" fill="#fff"/></svg></span>' +
      '<span class="yt-cap">' + esc(title || "Intro video") + "</span></div>";
  }

  function wireVideos(root) {
    $all(".js-yt", root || document).forEach(function (box) {
      function play() {
        var id = box.dataset.yt;
        box.classList.add("playing");
        box.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + esc(id) +
          '?autoplay=1&rel=0&modestbranding=1&playsinline=1" title="' + esc(t("pf.video")) +
          '" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>';
      }
      box.addEventListener("click", play);
      box.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); play(); }
      });
    });
  }

  /* ---------- 8. Tutor card ----------
     The whole card is clickable via a real stretched <a> link, so it also
     supports Ctrl/Cmd-click, middle-click, "open in new tab" and crawling. */
  /* strips the extension so the responsive variants can be addressed */
  function srcBase(x) {
    return esc(String(x.thumb || x.photo).replace(/\.(jpe?g|png|webp)$/i, ""));
  }

  function tutorCard(x) {
    var intro = (x.about && x.about[0]) || "";
    /* The card links to the pre-rendered page. It is the canonical version,
       it reads fully without JavaScript, and it immediately offers the
       interactive profile at the top — so a visitor loses nothing while a
       crawler gains the full text. */
    var href = "tutor/" + encodeURIComponent(x.id) + "/" + (LANG !== "en" ? "?lang=" + LANG : "");
    return '' +
      '<article class="tcard" data-id="' + esc(x.id) + '">' +
        '<a class="tcard-link" href="' + href + '" aria-label="' + esc(x.name) + ' — ' + esc(t("card.view")) + '"></a>' +
        '<div class="tcard-top">' +
          '<div class="tcard-photo">' +
            /* Cards display at 88px. Serving the full 800px original wasted
               about 125 KB per card, so responsive variants are used and the
               browser picks the right one. The original stays as the fallback
               for anything that cannot read WebP or srcset. */
            '<picture>' +
              '<source type="image/webp" srcset="' + srcBase(x) + '-176.webp 176w, ' + srcBase(x) + '-264.webp 264w" sizes="88px">' +
              '<source type="image/jpeg" srcset="' + srcBase(x) + '-176.jpg 176w, ' + srcBase(x) + '-264.jpg 264w" sizes="88px">' +
              '<img data-safe src="' + esc(x.thumb || x.photo) + '" alt="' + esc(x.name) + ', ' + esc(t("card.tutor")) + '" loading="lazy" decoding="async" width="88" height="88">' +
            '</picture>' +
            (x.verified ? '<span class="badge-verified" title="' + esc(t("pf.verified")) + '">✓</span>' : "") +
          "</div><div>" +
            "<h3>" + esc(x.name) + " <span>" + esc(x.countryFlag || "") + "</span></h3>" +
            '<p class="role">' + esc(t("card.tutor")) + (x.superTutor ? " · ⭐ " + esc(t("card.super")) : "") + "</p>" +
            '<div class="meta">' +
              '<span class="stars">' + stars(x.rating) + " <b>" + (x.rating || 0).toFixed(1) + "</b></span>" +
              "<span>" + (x.reviewsCount || 0) + " " + esc(t("card.reviews")) + "</span>" +
              "<span>" + (x.lessonsCount || 0) + " " + esc(t("card.lessons")) + "</span>" +
            "</div></div></div>" +
        '<div class="tcard-body"><p>' + esc(intro) + "</p>" +
          '<div class="tags">' +
            (x.teaches || []).slice(0, 2).map(function (v) { return '<span class="tag hi">' + esc(v) + "</span>"; }).join("") +
            (x.tags || []).slice(0, 3).map(function (v) { return '<span class="tag">' + esc(v) + "</span>"; }).join("") +
          "</div></div>" +
        '<div class="tcard-foot">' +
          '<div class="price"><b>' + px(x.priceUSD) + "</b><span>" + esc(x.lessonLength || "50 min") + " " + esc(t("card.lesson")) + "</span></div>" +
          '<span class="btn btn-primary btn-sm tcard-cta">' + esc(t("card.view")) + " →</span>" +
        "</div></article>";
  }

  /* Whole-card click. The stretched <a> already covers the card, so this
     only handles the rare case of a click landing on a nested element that
     sits above the link (images, badges) — it keeps every pixel clickable. */
  function wireCards(root) {
    $all("[data-safe]", root).forEach(safeImg);
    $all(".tcard", root).forEach(function (c) {
      c.addEventListener("click", function (e) {
        var a = e.target.closest("a");
        if (a) return;                       // a real link was clicked: let it work
        if (e.defaultPrevented) return;
        if (window.getSelection && String(window.getSelection()) !== "") return; // user was selecting text
        var link = c.querySelector(".tcard-link");
        if (!link) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) {
          window.open(link.href, "_blank", "noopener");
        } else {
          location.href = link.href;
        }
      });
    });
  }

  /* ---------- 8b. Text-version links ----------
     The pre-rendered pages under /tutor/ hold the full profile as plain
     HTML. Without a link from a real page they were reachable only via
     the sitemap, which crawlers treat as a much weaker signal. This
     strip gives them a genuine internal link from the home and search
     pages, and helps anyone browsing without JavaScript. */
  function renderTextVersions() {
    var host = $("#text-versions");
    if (!host || !TUTORS.length) return;
    host.innerHTML = esc(t("pf.textVersions")) + " " +
      TUTORS.map(function (x) {
        return '<a href="tutor/' + esc(x.id) + '/">' + esc(x.name) + "</a>";
      }).join(" · ") +
      ' · <a href="tutor/">' + esc(t("pf.allText")) + "</a>";
  }

  /* ---------- 9. Markets strip ---------- */
  function renderMarkets() {
    var host = $("#markets");
    if (!host) return;
    host.innerHTML = MARKETS.map(function (m) {
      return '<div class="mkt"><span class="mkt-flag">' + m.flag + "</span><b>" + esc(m.country) + "</b><span>" + esc(m.label) + "</span></div>";
    }).join("");
  }

  /* ---------- 10. FAQ (home) ---------- */
  function renderFaq() {
    var host = $("#faq-list");
    if (!host) return;
    var list = window.EKGURU_FAQ || [];
    host.innerHTML = list.map(function (q, i) {
      return '<details class="faq"' + (i === 0 ? " open" : "") + "><summary>" + esc(q[0]) + "</summary><p>" + esc(q[1]) + "</p></details>";
    }).join("");
  }

  /* ---------- 11. Home ---------- */
  function renderHome() {
    var host = $("#tutor-list");
    if (!host) return;

    if (!TUTORS.length) {
      host.innerHTML = '<div class="empty"><div>📚</div><p>No tutors have been added yet. Add one in <code>js/tutors-data.js</code>.</p></div>';
    } else {
      host.innerHTML = TUTORS.map(tutorCard).join("");
      wireCards(host);
    }

    var hc = $("#hero-tutor");
    if (hc && TUTORS.length) {
      var x = TUTORS[0];
      hc.innerHTML =
        '<img data-safe src="' + esc(x.photo) + '" alt="' + esc(x.name) + '" width="96" height="96">' +
        '<p class="hc-name">' + esc(x.name) + "</p>" +
        '<p class="sm">' + esc(t("card.tutor")) + " · " + esc(x.country) + "</p>" +
        '<p class="stars" style="margin:6px 0 10px">' + stars(x.rating) + " " + (x.rating || 0).toFixed(1) + "</p>" +
        '<a class="btn btn-primary btn-sm btn-block" href="' + langHref("tutor.html", "id=" + encodeURIComponent(x.id)) + '">' + esc(t("hero.viewProfile")) + "</a>";
      $all("[data-safe]", hc).forEach(safeImg);
    }

    var totalLessons = TUTORS.reduce(function (a, x) { return a + (x.lessonsCount || 0); }, 0);
    var avg = TUTORS.length ? (TUTORS.reduce(function (a, x) { return a + (x.rating || 0); }, 0) / TUTORS.length) : 0;
    var minP = TUTORS.length ? Math.min.apply(null, TUTORS.map(function (x) { return x.priceUSD || 0; })) : 0;

    var s1 = $("#stat-tutors"), s2 = $("#stat-lessons"), s3 = $("#stat-rating"), s4 = $("#stat-price");
    if (s3) s3.textContent = avg.toFixed(1) + "★";
    if (s4) s4.textContent = px(minP);
    if (s1 || s2) {
      var fired = false;
      function fire() {
        if (fired) return; fired = true;
        if (s1) countUp(s1, TUTORS.length, "");
        if (s2) countUp(s2, totalLessons, "+");
      }
      if ("IntersectionObserver" in window && s1) {
        var io = new IntersectionObserver(function (en) {
          en.forEach(function (x) { if (x.isIntersecting) { fire(); io.disconnect(); } });
        }, { threshold: 0.3 });
        io.observe(s1);
      } else fire();
    }
  }

  /* ---------- 12. Find tutors ---------- */
  function renderFind() {
    var host = $("#find-list");
    if (!host) return;
    var q = $("#f-q"), lvl = $("#f-level"), pr = $("#f-price"), so = $("#f-sort"), ct = $("#f-count");

    function apply() {
      var qs = ((q && q.value) || "").trim().toLowerCase();
      var lv = (lvl && lvl.value) || "";
      var mx = pr && pr.value ? Number(pr.value) : Infinity;
      var sort = (so && so.value) || "rating";

      var out = TUTORS.filter(function (x) {
        var hay = [x.name, x.headline, x.city, (x.teaches || []).join(" "), (x.tags || []).join(" ")].join(" ").toLowerCase();
        if (qs && hay.indexOf(qs) === -1) return false;
        if (lv && (x.levels || []).indexOf(lv) === -1) return false;
        if ((x.priceUSD || 0) > mx) return false;
        return true;
      }).sort(function (a, b) {
        if (sort === "price-low") return (a.priceUSD || 0) - (b.priceUSD || 0);
        if (sort === "price-high") return (b.priceUSD || 0) - (a.priceUSD || 0);
        if (sort === "lessons") return (b.lessonsCount || 0) - (a.lessonsCount || 0);
        return (b.rating || 0) - (a.rating || 0);
      });

      if (ct) ct.innerHTML = "<b>" + out.length + "</b> " + esc(out.length === 1 ? t("find.found1") : t("find.found"));
      host.innerHTML = out.length
        ? out.map(tutorCard).join("")
        : '<div class="empty"><div>🔍</div><p>' + esc(t("find.none")) + "</p></div>";
      wireCards(host);
    }

    [q, lvl, pr, so].forEach(function (el) {
      if (!el) return;
      el.addEventListener("input", apply);
      el.addEventListener("change", apply);
    });
    var rs = $("#f-reset");
    if (rs) rs.addEventListener("click", function () {
      if (q) q.value = ""; if (lvl) lvl.value = ""; if (pr) pr.value = ""; if (so) so.value = "rating";
      apply();
    });

    /* localise the price dropdown */
    if (pr) $all("option[data-amt]", pr).forEach(function (o) {
      o.textContent = t("find.upTo") + " " + px(Number(o.dataset.amt));
    });

    var pre = new URLSearchParams(location.search).get("q");
    if (pre && q) q.value = pre;
    apply();
  }

  /* ---------- 13. Profile ---------- */
  function renderProfile() {
    var host = $("#profile");
    if (!host) return;

    var id = new URLSearchParams(location.search).get("id");
    var x = TUTORS.filter(function (v) { return v.id === id; })[0] || TUTORS[0];

    if (!x) {
      host.innerHTML = '<div class="wrap"><div class="empty"><div>🙁</div><h2>' + esc(t("pf.notFound")) +
        "</h2><p>" + esc(t("pf.notFoundSub")) + '</p><a class="btn btn-primary" href="' + langHref("find-tutors.html") + '">' +
        esc(t("pf.seeAll")) + "</a></div></div>";
      return;
    }

    var subj = "Hindi lesson enquiry — " + x.name + " (EkGuru)";
    var body = "Hello " + x.name + ",\n\nI found your profile on EkGuru and I would like to learn Hindi.\n\nMy current level: \nMy goal: \nPreferred days and times (with my timezone): \n\nCould you tell me about a trial lesson?\n\nThank you!";
    var mail = mailHref(x.email || SITE.email, subj, body);

    var waTutor = hasWa(x.whatsapp) ? x.whatsapp : (hasWa(SITE.whatsapp) ? SITE.whatsapp : "");
    var waBig = waTutor
      ? '<a class="btn btn-wa btn-lg" href="' + waHref(waTutor, x.name) + '" target="_blank" rel="noopener">' + esc(t("pf.whatsapp")) + "</a>" : "";
    var waSmall = waTutor
      ? '<a class="btn btn-wa btn-block" href="' + waHref(waTutor, x.name) + '" target="_blank" rel="noopener">' + esc(t("pf.whatsapp")) + "</a>" : "";

    var preplyBig = x.preplyUrl
      ? '<a class="btn btn-ghost btn-lg" href="' + esc(x.preplyUrl) + '" target="_blank" rel="noopener nofollow">' + esc(t("pf.preplyProfile")) + " ↗</a>" : "";
    var preplySmall = x.preplyUrl
      ? '<a class="btn btn-primary btn-block" href="' + esc(x.preplyUrl) + '" target="_blank" rel="noopener nofollow">' + esc(t("pf.preply")) + " ↗</a>" : "";

    var days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    var av = x.availability || {};
    var sched = days.map(function (d) {
      var sl = av[d] || [];
      return '<div><div class="d">' + esc(t("days." + d)) + "</div>" +
        (sl.length ? sl.map(function (s) { return '<div class="slot">' + esc(s) + "</div>"; }).join("")
                   : '<div class="slot off">—</div>') + "</div>";
    }).join("");

    /* Reviews. On a phone these become a swipeable carousel (see
       features.js); on a desktop they stay as a normal stack. The
       markup is identical either way — only CSS and a small enhancer
       change the behaviour, so nothing breaks if JS is unavailable. */
    var revs = (x.reviews && x.reviews.length)
      ? '<div class="rev-wrap" data-rev-slider>' + x.reviews.map(function (r) {
          return '<article class="rev"><div class="rev-h"><div class="rev-av">' + esc(String(r.name || "?").charAt(0)) +
            "</div><div><b>" + esc(r.name) + '</b><span class="stars">' + stars(r.stars) +
            "</span> <span>· " + esc(r.date) + '</span></div></div><p class="rev-text">' + esc(r.text) + "</p></article>";
        }).join("") + "</div>"
      : '<p class="muted">' + esc(t("pf.noReviews")) + "</p>";

    host.innerHTML = '' +
      '<section class="pf-hero' + (x.banner ? " has-banner" : "") + '">' +
        (x.banner
          ? '<div class="pf-banner">' +
              '<img class="pf-banner-bg" src="' + esc(x.banner) + '" alt="" aria-hidden="true" role="presentation">' +
              '<img class="pf-banner-img" data-safe-banner src="' + esc(x.banner) + '" alt="' + esc(x.name) + ' — ' + esc(x.headline) + '" width="1280" height="720" fetchpriority="high">' +
            "</div>"
          : "") +
        '<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">' +
        '<a href="' + langHref("index.html") + '">' + esc(t("nav.home")) + "</a> › " +
        '<a href="' + langHref("find-tutors.html") + '">' + esc(t("nav.tutors")) + "</a> › <span>" + esc(x.name) + "</span></nav>" +
        '<div class="pf-top reveal"><div class="pf-photo">' +
          '<img data-safe src="' + esc(x.photo) + '" alt="' + esc(x.name) + ', ' + esc(t("card.tutor")) + '" width="200" height="200">' +
          (x.verified ? '<span class="badge-verified" title="' + esc(t("pf.verified")) + '">✓</span>' : "") +
        "</div><div>" +
          '<div class="pf-name"><h1>' + esc(x.name) + "</h1>" +
            (x.superTutor ? '<span class="chip brand">⭐ ' + esc(t("card.super")) + "</span>" : "") +
            '<span class="chip">' + esc(x.countryFlag || "") + " " + esc(x.country || "") + "</span></div>" +
          '<p class="pf-headline">' + esc(x.headline) + "</p>" +
          '<div class="tags">' + (x.tags || []).map(function (v) { return '<span class="tag hi">' + esc(v) + "</span>"; }).join("") + "</div>" +
          '<div class="pf-stats">' +
            '<div><b class="stars">' + stars(x.rating) + "</b><span>" + (x.rating || 0).toFixed(1) + " · " + (x.reviewsCount || 0) + " " + esc(t("card.reviews")) + "</span></div>" +
            "<div><b>" + (x.lessonsCount || 0) + "</b><span>" + esc(t("pf.lessonsTaught")) + "</span></div>" +
            "<div><b>" + (x.experienceYears || 0) + "+ " + esc(t("pf.yrs")) + "</b><span>" + esc(t("pf.exp")) + "</span></div>" +
            "<div><b>" + px(x.priceUSD) + "</b><span>" + esc(t("pf.per")) + " " + esc(x.lessonLength || "50 min") + "</span></div>" +
          "</div>" +
          '<div class="pf-actions">' +
            '<button class="btn btn-primary btn-lg" type="button" data-book="' + esc(x.id) + '">📅 ' + esc(t("book.cta")) + "</button>" +
            '<a class="btn btn-ghost btn-lg" href="' + mail + '">' + esc(t("pf.email")) + "</a>" +
            waBig + preplyBig +
          "</div>" +
          '<div class="share-box" id="share-box"></div>' +
          '<p class="pr-link"><a href="tutor/' + esc(x.id) + '/" rel="alternate">' +
            esc(t("pf.textVersion")) + "</a></p>" +
          "</div></div></div></section>" +

      '<div class="wrap"><div class="pf-layout"><main>' +
        '<section class="panel reveal"><h2><span class="ico">👋</span>' + esc(t("pf.about")) + "</h2>" +
          (x.about || []).map(function (p) { return "<p>" + esc(p) + "</p>"; }).join("") + "</section>" +

        '<section class="panel reveal"><h2><span class="ico">🎬</span>' + esc(t("pf.video")) + "</h2>" +
          videoBlock(x.youtubeId, x.videoTitle) +
          (x.youtubeId ? '<p class="vid-link"><a href="https://www.youtube.com/watch?v=' + esc(x.youtubeId) +
            '" target="_blank" rel="noopener">' + esc(t("pf.watchOn")) + " ↗</a></p>" : "") +
        "</section>" +

        '<section class="panel reveal"><h2><span class="ico">🎓</span>' + esc(t("pf.experience")) + '</h2><ul class="list">' +
          (x.experience || []).map(function (v) { return "<li>" + esc(v) + "</li>"; }).join("") + "</ul></section>" +

        '<section class="panel reveal"><h2><span class="ico">🧭</span>' + esc(t("pf.method")) + '</h2><div class="method">' +
          (x.methodology || []).map(function (m) {
            return '<div class="m"><b>' + esc(m.title) + "</b><span>" + esc(m.desc) + "</span></div>";
          }).join("") + "</div></section>" +

        '<section class="panel reveal"><h2><span class="ico">📚</span>' + esc(t("pf.teaches")) + "</h2>" +
          '<div class="tags">' + (x.teaches || []).map(function (v) { return '<span class="tag hi">' + esc(v) + "</span>"; }).join("") + "</div>" +
          '<dl class="kv" style="margin-top:18px">' +
            "<dt>" + esc(t("pf.levels")) + "</dt><dd>" + esc((x.levels || []).join(", ")) + "</dd>" +
            "<dt>" + esc(t("pf.speaks")) + "</dt><dd>" + (x.speaks || []).map(function (s) { return esc(s.lang) + " (" + esc(s.level) + ")"; }).join(", ") + "</dd>" +
            "<dt>" + esc(t("pf.location")) + "</dt><dd>" + esc(x.city || x.country) + "</dd>" +
            "<dt>" + esc(t("pf.timezone")) + "</dt><dd>" + esc(x.timezone || "IST") + "</dd>" +
          "</dl></section>" +

        '<section class="panel reveal"><h2><span class="ico">🗓️</span>' + esc(t("pf.schedule")) + "</h2>" +
          '<div class="sched">' + sched + "</div>" +
          '<p class="sched-note">' + esc(t("pf.schedNote")) + " " + esc(x.timezone || "IST") + ". " + esc(t("pf.schedNote2")) + "</p></section>" +

        '<section class="panel reveal"><h2><span class="ico">💬</span>' + esc(t("pf.reviews")) + "</h2>" + revs + "</section>" +
      "</main><aside><div class=\"side\"><div class=\"side-card reveal\">" +
        '<div class="side-price"><b>' + pxFull(x.priceUSD) + "</b><span>" + esc(x.lessonLength || "50 min") + " " + esc(t("card.lesson")) + "</span></div>" +
        '<button class="btn btn-primary btn-block" type="button" data-book="' + esc(x.id) + '">📅 ' + esc(t("book.cta")) + "</button>" +
        preplySmall +
        '<a class="btn btn-ghost btn-block" href="' + mail + '">' + esc(t("pf.email")) + "</a>" +
        waSmall +
        '<div class="trust">' +
          (x.trialAvailable ? "<div><span>✅</span>" + esc(t("pf.trial")) + "</div>" : "") +
          "<div><span>🕒</span>" + esc(x.timezone || "IST") + "</div>" +
          "<div><span>🗣️</span>" + esc((x.speaks || []).map(function (s) { return s.lang; }).join(" · ")) + "</div>" +
          "<div><span>🔒</span>" + esc(t("pf.oneOnOne")) + "</div>" +
        "</div></div></div></aside></div></div>";

    $all("[data-safe]", host).forEach(safeImg);
    $all("[data-safe-banner]", host).forEach(safeBanner);
    wireVideos(host);
    initReveal(host);
  }

  /* ---------- 14. Join page ----------
     If SITE.applyFormUrl is set, every apply button opens the Google Form
     and an "or email us instead" fallback link appears underneath.
     If it is empty, the buttons open a pre-filled email exactly as before. */
  function renderJoin() {
    var host = $("#join-mail");
    if (!host) return;
    var body =
      "Hello EkGuru team,\n\nI would like to join as a Hindi tutor. Here are my details:\n\n" +
      "1. Full name and city: \n" +
      "2. Short bio (150-250 words): \n" +
      "3. Profile photo: (attached)\n" +
      "4. Intro video link (YouTube): \n" +
      "5. Price per 50-minute lesson (USD): \n" +
      "6. Weekly availability and timezone: \n" +
      "7. Contact email: \n" +
      "8. WhatsApp number (optional): \n" +
      "9. Preply profile link (optional): \n" +
      "10. Years of teaching experience: \n\n" +
      "Thank you!";

    var mailUrl = mailHref(SITE.email, "Tutor application — EkGuru", body);
    var form = (SITE.applyFormUrl || "").trim();
    var buttons = [host].concat($all("#join-mail-2"));

    buttons.forEach(function (b) {
      if (!b) return;
      if (form) {
        b.href = form;
        b.target = "_blank";
        b.rel = "noopener";
        b.textContent = t("join.formBtn");
      } else {
        b.href = mailUrl;
        b.removeAttribute("target");
        b.textContent = t("join.emailBtn");
      }
    });

    /* fallback line under the main button */
    var alt = $("#join-alt");
    if (alt) {
      alt.innerHTML = form
        ? esc(t("join.orEmail")) + ' <a href="' + mailUrl + '">' + esc(SITE.email) + "</a>"
        : '<a href="' + mailUrl + '">' + esc(SITE.email) + "</a>";
    }

    var faq = $("#join-faq");
    if (faq) {
      var qa = [["join.q1", "join.a1f"], ["join.q2", "join.a2f"], ["join.q3", "join.a3f"], ["join.q4", "join.a4f"]];
      faq.innerHTML = qa.map(function (p, i) {
        return '<details class="faq"' + (i === 0 ? " open" : "") + "><summary>" + esc(t(p[0])) + "</summary><p>" + esc(t(p[1])) + "</p></details>";
      }).join("");
    }
  }

  /* ---------- 15. Home search ---------- */
  function initSearch() {
    var f = $("#home-search");
    if (!f) return;
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = (($("#home-q") && $("#home-q").value) || "").trim();
      location.href = langHref("find-tutors.html", v ? "q=" + encodeURIComponent(v) : "");
    });
  }

  /* ---------- 16. Contact links + floating button ---------- */
  function initContact() {
    var subj = "Enquiry — EkGuru";
    var body = "Hello EkGuru team,\n\nI would like to know more about your Hindi lessons.\n\nMy level: \nMy goal: \nMy timezone: \n\nThank you!";
    $all("[data-mail-main]").forEach(function (a) { a.href = mailHref(SITE.email, subj, body); });

    var fab = $("#contact-fab");
    if (!fab) return;
    if (hasWa(SITE.whatsapp)) {
      fab.href = waHref(SITE.whatsapp, "");
      fab.classList.add("fab-wa");
      fab.innerHTML = "💬";
      fab.setAttribute("aria-label", "WhatsApp");
    } else {
      fab.href = mailHref(SITE.email, subj, body);
      fab.classList.add("fab-mail");
      fab.innerHTML = "✉️";
      fab.setAttribute("aria-label", "Email " + SITE.email);
    }
  }

  /* ---------- 17. Boot ---------- */
  function boot() {
    try { applyI18n(); } catch (e) { showError("translations", e); }
    try { buildLangSwitcher(); } catch (e) { showError("language switcher", e); }
    try { initHeader(); } catch (e) { showError("header", e); }
    try { initBadges(); } catch (e) { showError("badges", e); }
    try { initContact(); } catch (e) { showError("contact", e); }
    try { renderMarkets(); } catch (e) { showError("markets", e); }
    try { renderTextVersions(); } catch (e) { showError("text versions", e); }
    try { renderHome(); } catch (e) { showError("home", e); }
    try { renderFaq(); } catch (e) { showError("faq", e); }
    try { renderFind(); } catch (e) { showError("find-tutors", e); }
    try { renderProfile(); } catch (e) { showError("profile", e); }
    try { renderJoin(); } catch (e) { showError("join", e); }
    try { initSearch(); } catch (e) { showError("search", e); }
    try { wireVideos(document); } catch (e) { showError("video", e); }
    try { initReveal(); } catch (e) { showError("animations", e); }

    if (!TUTORS.length) showError("tutors-data.js", new Error("EKGURU_TUTORS is empty or the file failed to load."));
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
