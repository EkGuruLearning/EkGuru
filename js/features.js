/* =========================================================
   EkGuru — features.js
   Runs after main.js and adds:
     1. Live instant search (dropdown, keyboard, no page reload)
     2. Booking request modal (pick a slot → send by email/WhatsApp)
     3. Timezone converter for the weekly schedule
     4. Share buttons
     5. Back-to-top button
     6. Quick topic filter chips on the search page
   Everything degrades safely: if a piece fails, the page still works.
   ========================================================= */
(function () {
  "use strict";

  var T = Array.isArray(window.EKGURU_TUTORS) ? window.EKGURU_TUTORS : [];
  var SITE = window.EKGURU_SITE || {};
  var I18N = window.EKGURU_I18N || {};
  var LANG = window.EKGURU_LANG || "en";
  var CUR = SITE.currency || "$";
  function px(usd) {
    if (usd == null) return "—";
    if (window.EkGuruPrice) return window.EkGuruPrice.price(usd);
    return CUR + usd;
  }

  function t(k) {
    var p = I18N[LANG] || {}, e = I18N.en || {};
    return p[k] != null ? p[k] : (e[k] != null ? e[k] : k);
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function $(s, r) { return (r || document).querySelector(s); }
  function $all(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function warn(where, e) { console.warn("[EkGuru features]", where, e); }

  /* Environment shims. Every browser since 2015 has these, but a stray
     missing API must never take a feature down with it. */
  function mq(query) {
    try {
      if (typeof window.matchMedia === "function") return window.matchMedia(query).matches;
    } catch (e) {}
    /* fall back to a width comparison */
    var m = /max-width:\s*(\d+)/.exec(query);
    if (m) return (window.innerWidth || 1024) <= parseInt(m[1], 10);
    var n = /min-width:\s*(\d+)/.exec(query);
    if (n) return (window.innerWidth || 1024) >= parseInt(n[1], 10);
    return false;
  }
  function hasIO() { return typeof window.IntersectionObserver === "function"; }

  /* coin icon for the currency control — inline so it needs no network */
  var COIN =
    '<svg class="coin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<circle cx="12" cy="12" r="9"/><path d="M14.5 9a2.8 2.8 0 00-2.5-1.4c-1.5 0-2.6.9-2.6 2.1 0 2.7 5.2 1.6 5.2 4.3 0 1.2-1.1 2.1-2.6 2.1A2.8 2.8 0 019.5 15"/>' +
    '<path d="M12 6.2v11.6"/></svg>';
  function safeSession(k) {
    try { return sessionStorage.getItem(k); } catch (e) { return null; }
  }
  /* scrollIntoView is missing in some environments — never let it throw */
  function scrollTo(el, opts) {
    try { if (el && typeof el.scrollIntoView === "function") el.scrollIntoView(opts); } catch (e) {}
  }
  function hasWa(v) { return !!v && !/[xX]/.test(v) && String(v).replace(/\D/g, "").length >= 10; }
  function langHref(file, extra) {
    var q = [];
    if (extra) q.push(extra);
    if (LANG !== "en") q.push("lang=" + LANG);
    return file + (q.length ? "?" + q.join("&") : "");
  }
  function tutorById(id) {
    for (var i = 0; i < T.length; i++) if (T[i].id === id) return T[i];
    return null;
  }

  /* =========================================================
     1. LIVE INSTANT SEARCH  (works on EVERY page)
     ========================================================= */

  /* Synonyms so real-world wording still finds a tutor.
     "cheap" -> price words, "child" -> kids, "script" -> devanagari, etc. */
  var SYN = {
    kid: "kids children child young school", kids: "kids children child young school",
    child: "kids children child young", children: "kids children child young",
    baby: "kids children young", teen: "kids children teenager young",
    beginner: "beginner basics start starter new zero foundation",
    beginners: "beginner basics start starter new zero foundation",
    basic: "beginner basics start", start: "beginner basics start",
    newbie: "beginner basics start", zero: "beginner basics start",
    advanced: "advanced fluent fluency expert",
    fluent: "advanced fluent fluency conversation",
    intermediate: "intermediate improve",
    speak: "speaking conversation talk speak oral fluency",
    speaking: "speaking conversation talk speak oral",
    talk: "speaking conversation talk", talking: "speaking conversation talk",
    conversation: "conversation speaking talk oral",
    conversational: "conversation speaking talk oral",
    read: "reading read devanagari script alphabet",
    reading: "reading read devanagari script alphabet",
    write: "writing write devanagari script alphabet",
    writing: "writing write devanagari script alphabet",
    script: "devanagari script alphabet reading writing letters",
    alphabet: "devanagari script alphabet letters",
    devanagari: "devanagari script alphabet reading writing",
    letter: "devanagari script alphabet letters",
    grammar: "grammar rules structure tenses",
    vocab: "vocabulary words", vocabulary: "vocabulary words",
    pronounce: "pronunciation accent sound speaking",
    pronunciation: "pronunciation accent sound speaking",
    accent: "pronunciation accent sound",
    exam: "exam academic school study test cbse",
    school: "school academic exam kids study cbse",
    academic: "academic exam school study",
    business: "business professional work office corporate",
    work: "business professional work office",
    office: "business professional work office",
    travel: "travel tourist trip holiday india",
    tourist: "travel tourist trip",
    india: "india indian travel culture",
    culture: "culture cultural india literature",
    bollywood: "culture film movies bollywood conversation",
    movie: "culture film movies bollywood",
    music: "culture music songs",
    family: "family relatives conversation home heritage",
    heritage: "family heritage roots culture",
    cheap: "cheap budget affordable low price",
    budget: "cheap budget affordable low price",
    affordable: "cheap budget affordable low price",
    free: "trial free first lesson",
    trial: "trial free first lesson demo",
    demo: "trial free first lesson demo",
    online: "online remote video zoom class lesson",
    class: "class lesson course online",
    lesson: "class lesson course online",
    course: "class lesson course online",
    tutor: "tutor teacher guru instructor",
    teacher: "tutor teacher guru instructor",
    guru: "tutor teacher guru instructor",
    native: "native fluent mother tongue",
    hindi: "hindi hindustani indian devanagari",
    urdu: "hindi urdu hindustani",
    female: "female woman she her lady",
    woman: "female woman she her lady",
    male: "male man he him",
    patient: "patient calm gentle friendly",
    fun: "fun engaging enjoyable friendly",
    cheapest: "cheap budget affordable low price"
  };

  function expand(term) {
    var extra = SYN[term] || "";
    return (term + " " + extra).trim();
  }

  /* Forgiving match: exact, then one-character typo tolerance.
     Handles a missing letter ("grammer"), a doubled letter ("beginer"
     vs "beginner") and two swapped letters ("hindi" / "hindi"). */
  function fuzzyHit(hay, term) {
    if (term.length < 3) return hay.indexOf(term) > -1 ? 1 : 0;
    if (hay.indexOf(term) > -1) return 1;
    var i, v;
    /* 1. a character was typed that should not be there */
    for (i = 0; i < term.length; i++) {
      v = term.slice(0, i) + term.slice(i + 1);
      if (v.length >= 3 && hay.indexOf(v) > -1) return 0.6;
    }
    /* 2. a character is missing — try doubling each letter */
    for (i = 0; i < term.length; i++) {
      v = term.slice(0, i) + term[i] + term.slice(i);
      if (hay.indexOf(v) > -1) return 0.6;
    }
    /* 3. two neighbouring characters were swapped */
    for (i = 0; i < term.length - 1; i++) {
      v = term.slice(0, i) + term[i + 1] + term[i] + term.slice(i + 2);
      if (hay.indexOf(v) > -1) return 0.6;
    }
    /* 4. long words: match on a solid prefix */
    if (term.length >= 6 && hay.indexOf(term.slice(0, term.length - 2)) > -1) return 0.5;
    return 0;
  }

  function haystack(x) {
    if (x.__hay) return x.__hay;
    var parts = [
      x.name, x.nickname, x.headline, x.city, x.country, x.subject,
      (x.teaches || []).join(" "), (x.tags || []).join(" "),
      (x.levels || []).join(" "),
      (x.speaks || []).map(function (s) { return s.lang + " " + s.level; }).join(" "),
      (x.about || []).join(" "),
      (x.methodology || []).map(function (m) { return m.title + " " + m.desc; }).join(" "),
      (x.experience || []).join(" "),
      x.trialAvailable ? "trial free first lesson" : "",
      "hindi tutor teacher guru online lesson class native",
      "$" + x.priceUSD, x.priceUSD <= 5 ? "cheap budget affordable low price" : ""
    ];
    x.__hay = parts.join(" ").toLowerCase();
    return x.__hay;
  }

  function searchTutors(q) {
    q = String(q || "").trim().toLowerCase();
    if (!q) return [];
    var raw = q.split(/[\s,]+/).filter(Boolean);

    return T.map(function (x) {
      var hay = haystack(x);
      var nm = String(x.name).toLowerCase();
      var teach = (x.teaches || []).join(" ").toLowerCase();
      var tags = (x.tags || []).join(" ").toLowerCase();
      var score = 0, matchedAll = true;

      raw.forEach(function (term) {
        var best = 0;
        expand(term).split(" ").forEach(function (w) {
          if (!w) return;
          if (nm.indexOf(w) === 0) best = Math.max(best, 120);
          else if (nm.indexOf(w) > -1) best = Math.max(best, 70);
          if (fuzzyHit(teach, w)) best = Math.max(best, 40 * fuzzyHit(teach, w));
          if (fuzzyHit(tags, w)) best = Math.max(best, 22 * fuzzyHit(tags, w));
          if (fuzzyHit(hay, w)) best = Math.max(best, 10 * fuzzyHit(hay, w));
        });
        if (!best) matchedAll = false;
        score += best;
      });

      /* every word should match somewhere, but a single strong hit still counts */
      if (!matchedAll && raw.length > 1) score = score * 0.35;
      /* gentle nudge: better rated and cheaper tutors first on equal relevance */
      score += (x.rating || 0) * 0.4;
      return { t: x, score: score };
    }).filter(function (r) { return r.score > 3; })
      .sort(function (a, b) { return b.score - a.score; })
      .map(function (r) { return r.t; });
  }
  window.EkGuruSearch = searchTutors;

  function matchedTopic(x, q) {
    q = String(q).trim().toLowerCase();
    var words = expand(q.split(/\s+/)[0]).split(" ");
    var hit = (x.teaches || []).filter(function (s) {
      var l = s.toLowerCase();
      return words.some(function (w) { return w && l.indexOf(w) > -1; });
    })[0];
    return hit || (x.teaches || [])[0] || "";
  }

  /* Wire ANY input into a live dropdown. Used by the hero box and the
     header box, so search works from every page. */
  function attachSearch(input, opts) {
    if (!input || input.dataset.acReady) return;
    input.dataset.acReady = "1";
    opts = opts || {};

    var wrap = document.createElement("div");
    wrap.className = "ac-wrap" + (opts.compact ? " ac-compact" : "");
    input.parentNode.insertBefore(wrap, input);
    wrap.appendChild(input);

    var box = document.createElement("div");
    box.className = "ac-box";
    box.setAttribute("role", "listbox");
    box.hidden = true;
    wrap.appendChild(box);

    var active = -1;

    function render(q) {
      var results = searchTutors(q);
      if (!q.trim()) { box.hidden = true; return; }
      active = -1;

      if (!results.length) {
        box.innerHTML = '<div class="ac-empty"><b>' + esc(t("search.none")) + "</b><span>" +
          esc(t("search.noneSub")) + "</span>" +
          '<a class="ac-all" href="' + langHref("find-tutors.html") + '">' + esc(t("pf.seeAll")) + " →</a></div>";
        box.hidden = false;
        return;
      }

      box.innerHTML =
        '<div class="ac-head">' + esc(t("search.suggest")) + " · " + results.length + "</div>" +
        results.slice(0, 5).map(function (x, i) {
          return '<a class="ac-item" role="option" data-i="' + i + '" href="' +
            langHref("tutor.html", "id=" + encodeURIComponent(x.id)) + '">' +
            '<img src="' + esc(x.thumb || x.photo) + '" alt="" width="40" height="40" loading="lazy">' +
            '<span class="ac-txt"><b>' + esc(x.name) + "</b><small>" + esc(matchedTopic(x, q)) + "</small></span>" +
            '<span class="ac-price">' + px(x.priceUSD) + "</span></a>";
        }).join("") +
        '<a class="ac-all" href="' + langHref("find-tutors.html", "q=" + encodeURIComponent(q)) + '">' +
          esc(t("search.viewAll")) + " (" + results.length + ") →</a>";
      box.hidden = false;
    }

    function items() { return $all(".ac-item, .ac-all", box); }
    function setActive(n) {
      var list = items();
      if (!list.length) return;
      if (n < 0) n = list.length - 1;
      if (n >= list.length) n = 0;
      active = n;
      list.forEach(function (el, i) { el.classList.toggle("on", i === n); });
      scrollTo(list[n], { block: "nearest" });
    }

    var timer;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { render(input.value); }, 80);
    });
    input.addEventListener("focus", function () { if (input.value.trim()) render(input.value); });
    input.addEventListener("keydown", function (e) {
      if (box.hidden) return;
      if (e.key === "ArrowDown") { e.preventDefault(); setActive(active + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); setActive(active - 1); }
      else if (e.key === "Enter") {
        var list = items();
        if (active > -1 && list[active]) { e.preventDefault(); location.href = list[active].href; return; }
        var r = searchTutors(input.value);
        e.preventDefault();
        location.href = r.length === 1
          ? langHref("tutor.html", "id=" + encodeURIComponent(r[0].id))
          : langHref("find-tutors.html", "q=" + encodeURIComponent(input.value.trim()));
      } else if (e.key === "Escape") { box.hidden = true; input.blur(); }
    });
    document.addEventListener("click", function (e) { if (!wrap.contains(e.target)) box.hidden = true; });
  }

  function initLiveSearch() {
    /* hero box on the home page */
    var hero = $("#home-q");
    if (hero) {
      attachSearch(hero);
      var form = $("#home-search");
      if (form) form.addEventListener("submit", function (e) {
        e.preventDefault();
        var q = hero.value.trim();
        var r = searchTutors(q);
        location.href = (q && r.length === 1)
          ? langHref("tutor.html", "id=" + encodeURIComponent(r[0].id))
          : langHref("find-tutors.html", q ? "q=" + encodeURIComponent(q) : "");
      }, true);
    }

    /* header search — injected into EVERY page so search is always reachable */
    var nav = $(".nav");
    if (nav && !$("#hdr-search")) {
      var holder = document.createElement("div");
      holder.className = "hdr-search";
      holder.innerHTML = '<span class="hs-ico" aria-hidden="true">🔍</span>' +
        '<input id="hdr-search" type="search" autocomplete="off" placeholder="' +
        esc(t("search.headerPh")) + '" aria-label="' + esc(t("find.search")) + '">';
      nav.insertBefore(holder, nav.firstChild);
      attachSearch($("#hdr-search"), { compact: true });
    }

    /* the search page input also gets the dropdown */
    var fq = $("#f-q");
    if (fq) attachSearch(fq, { compact: true });
  }

  /* =========================================================
     2. QUICK TOPIC CHIPS (search page)
     ========================================================= */
  function initChips() {
    var host = $("#topic-chips");
    if (!host) return;
    var input = $("#f-q");
    if (!input) return;

    var counts = {};
    T.forEach(function (x) {
      (x.teaches || []).forEach(function (s) { counts[s] = (counts[s] || 0) + 1; });
    });
    var topics = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; }).slice(0, 7);

    host.innerHTML = '<span class="chips-label">' + esc(t("search.popular")) + "</span>" +
      topics.map(function (s) {
        return '<button type="button" class="chip-btn" data-q="' + esc(s) + '">' + esc(s) + "</button>";
      }).join("") +
      '<button type="button" class="chip-btn chip-clear" data-q="">' + esc(t("find.reset")) + "</button>";

    host.addEventListener("click", function (e) {
      var b = e.target.closest(".chip-btn");
      if (!b) return;
      input.value = b.dataset.q;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      $all(".chip-btn", host).forEach(function (x) { x.classList.toggle("on", x === b && !!b.dataset.q); });
      var list = $("#find-list");
      scrollTo(list, { behavior: "smooth", block: "start" });
    });
  }

  /* =========================================================
     3. TIMEZONE HELPERS
     ========================================================= */
  /* "IST (GMT+5:30)" -> 330 minutes */
  function tzOffsetMin(str) {
    var m = /GMT([+-])(\d{1,2})(?::(\d{2}))?/i.exec(String(str || ""));
    if (!m) return null;
    var sign = m[1] === "-" ? -1 : 1;
    return sign * (parseInt(m[2], 10) * 60 + (m[3] ? parseInt(m[3], 10) : 0));
  }
  function myOffsetMin() { return -new Date().getTimezoneOffset(); }
  function myTzLabel() {
    try {
      var z = Intl.DateTimeFormat().resolvedOptions().timeZone;
      var o = myOffsetMin(), s = o < 0 ? "-" : "+", a = Math.abs(o);
      var lbl = "GMT" + s + Math.floor(a / 60) + (a % 60 ? ":" + String(a % 60).padStart(2, "0") : "");
      return z ? z + " (" + lbl + ")" : lbl;
    } catch (e) { return "your local time"; }
  }
  var DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  /* convert a slot to the visitor's timezone, returning {day, time, shift} */
  function convertSlot(dayIdx, hhmm, fromMin, toMin) {
    var p = hhmm.split(":");
    var mins = parseInt(p[0], 10) * 60 + parseInt(p[1], 10);
    var delta = toMin - fromMin;
    var abs = dayIdx * 1440 + mins + delta;
    var week = 7 * 1440;
    while (abs < 0) abs += week;
    while (abs >= week) abs -= week;
    var nd = Math.floor(abs / 1440), nm = abs % 1440;
    return {
      day: nd,
      time: String(Math.floor(nm / 60)).padStart(2, "0") + ":" + String(nm % 60).padStart(2, "0"),
      shift: nd !== dayIdx
    };
  }

  function initTimezoneToggle() {
    var sched = $(".sched");
    if (!sched) return;
    var note = $(".sched-note");
    var id = new URLSearchParams(location.search).get("id");
    var x = tutorById(id) || T[0];
    if (!x) return;

    var from = tzOffsetMin(x.timezone);
    var to = myOffsetMin();
    if (from == null) return;

    var same = from === to;
    var bar = document.createElement("div");
    bar.className = "tz-bar";
    bar.innerHTML = same
      ? '<span class="tz-same">🕒 ' + esc(t("tz.same")) + "</span>"
      : '<button type="button" class="tz-toggle" aria-pressed="false">' +
          '<span class="tz-dot"></span><span class="tz-lbl">' + esc(t("tz.myTime")) + "</span></button>" +
        '<span class="tz-info">' + esc(myTzLabel()) + "</span>";
    sched.parentNode.insertBefore(bar, sched);
    if (same) return;

    /* remember the original markup so we can switch back */
    var original = sched.innerHTML;
    var av = x.availability || {};

    function renderConverted() {
      var grid = {};
      DAYS.forEach(function (d, i) { grid[i] = []; });
      DAYS.forEach(function (d, i) {
        (av[d] || []).forEach(function (s) {
          var c = convertSlot(i, s, from, to);
          grid[c.day].push({ time: c.time, shift: c.shift });
        });
      });
      sched.innerHTML = DAYS.map(function (d, i) {
        var list = grid[i].sort(function (a, b) { return a.time.localeCompare(b.time); });
        return '<div><div class="d">' + esc(t("days." + d)) + "</div>" +
          (list.length
            ? list.map(function (s) {
                return '<div class="slot' + (s.shift ? " shifted" : "") + '">' + esc(s.time) + "</div>";
              }).join("")
            : '<div class="slot off">—</div>') + "</div>";
      }).join("");
    }

    var btn = $(".tz-toggle", bar);
    var on = false;
    btn.addEventListener("click", function () {
      on = !on;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      bar.classList.toggle("on", on);
      $(".tz-lbl", btn).textContent = on ? t("tz.tutorTime") : t("tz.myTime");
      if (on) renderConverted(); else sched.innerHTML = original;
      if (note) {
        note.innerHTML = on
          ? "🕒 " + esc(t("tz.showingYours")) + " <b>" + esc(myTzLabel()) + "</b>. " + esc(t("pf.schedNote2"))
          : esc(t("pf.schedNote")) + " " + esc(x.timezone) + ". " + esc(t("pf.schedNote2"));
      }
    });
  }

  /* =========================================================
     4. BOOKING REQUEST MODAL
     ========================================================= */
  var modal = null, modalTutor = null, chosen = null, lastFocus = null;

  function buildModal() {
    if (modal) return modal;
    modal = document.createElement("div");
    modal.className = "bk-overlay";
    modal.hidden = true;
    modal.innerHTML =
      '<div class="bk-modal" role="dialog" aria-modal="true" aria-labelledby="bk-title">' +
        '<button class="bk-x" type="button" aria-label="' + esc(t("book.close")) + '">×</button>' +
        '<div class="bk-head"><img class="bk-av" alt="" width="52" height="52">' +
          '<div><h3 id="bk-title"></h3><p class="bk-sub"></p></div></div>' +
        '<div class="bk-body">' +
          '<div class="bk-step"><span class="bk-n">1</span><b>' + esc(t("book.step1")) + "</b></div>" +
          '<div class="bk-slots"></div>' +
          '<div class="bk-step"><span class="bk-n">2</span><b>' + esc(t("book.step2")) + "</b></div>" +
          '<div class="bk-grid">' +
            '<label class="bk-f"><span>' + esc(t("book.name")) + ' *</span><input type="text" id="bk-name" autocomplete="name"></label>' +
            '<label class="bk-f"><span>' + esc(t("book.email")) + ' *</span><input type="email" id="bk-email" autocomplete="email"></label>' +
            '<label class="bk-f"><span>' + esc(t("book.level")) + '</span><select id="bk-level">' +
              '<option value="Complete beginner">' + esc(t("book.lvl1")) + "</option>" +
              '<option value="Beginner">' + esc(t("book.lvl2")) + "</option>" +
              '<option value="Intermediate">' + esc(t("book.lvl3")) + "</option>" +
              '<option value="Advanced">' + esc(t("book.lvl4")) + "</option>" +
            "</select></label>" +
            '<label class="bk-f"><span>' + esc(t("book.tz")) + '</span><input type="text" id="bk-tz" readonly></label>' +
          "</div>" +
          '<label class="bk-f bk-full"><span>' + esc(t("book.goal")) + '</span><textarea id="bk-goal" rows="3" placeholder="' + esc(t("book.goalPh")) + '"></textarea></label>' +
          '<div class="bk-step"><span class="bk-n">3</span><b>' + esc(t("book.step3")) + "</b></div>" +
          '<div class="bk-preview"><div class="bk-prev-h">' + esc(t("book.summary")) + '</div><pre class="bk-prev-t"></pre></div>' +
          '<p class="bk-err" hidden></p>' +
          '<div class="bk-actions"></div>' +
          '<p class="bk-note">' + esc(t("book.note")) + "</p>" +
        "</div>" +
      "</div>";
    document.body.appendChild(modal);

    $(".bk-x", modal).addEventListener("click", closeBooking);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeBooking(); });
    document.addEventListener("keydown", function (e) {
      if (!modal.hidden && e.key === "Escape") closeBooking();
    });
    ["bk-name", "bk-email", "bk-goal", "bk-level"].forEach(function (id) {
      modal.addEventListener("input", function (e) { if (e.target.id === id) updatePreview(); });
      modal.addEventListener("change", function (e) { if (e.target.id === id) updatePreview(); });
    });
    return modal;
  }

  function slotLabel() {
    if (!chosen) return "";
    return t("days." + DAYS[chosen.day]) + " " + chosen.time +
      (chosen.mine ? " (" + t("tz.yourTime") + ")" : " (" + modalTutor.timezone + ")");
  }

  function buildMessage() {
    var name = ($("#bk-name") || {}).value || "";
    var email = ($("#bk-email") || {}).value || "";
    var level = ($("#bk-level") || {}).value || "";
    var goal = ($("#bk-goal") || {}).value || "";
    var tz = ($("#bk-tz") || {}).value || "";
    return "Hello " + modalTutor.name + ",\n\n" +
      "I would like to book a Hindi lesson with you through EkGuru.\n\n" +
      "Preferred time: " + (chosen ? slotLabel() : "(not selected)") + "\n" +
      "My name: " + (name || "-") + "\n" +
      "My email: " + (email || "-") + "\n" +
      "My level: " + level + "\n" +
      "My timezone: " + tz + "\n" +
      "My goal: " + (goal || "-") + "\n\n" +
      "Lesson: " + (modalTutor.lessonLength || "50 min") + " at $" + modalTutor.priceUSD +
        (window.EkGuruPrice && window.EkGuruPrice.isConverted() ? " (about " + px(modalTutor.priceUSD) + ")" : "") + "\n\n" +
      "Please confirm if this time works for you.\n\nThank you!";
  }

  function updatePreview() {
    var pre = $(".bk-prev-t", modal);
    if (pre) pre.textContent = buildMessage();
    buildActions();
  }

  function buildActions() {
    var host = $(".bk-actions", modal);
    if (!host) return;
    var to = modalTutor.email || SITE.email;
    var subj = "Lesson booking request — " + modalTutor.name + " (EkGuru)";
    var mail = "mailto:" + to + "?subject=" + encodeURIComponent(subj) + "&body=" + encodeURIComponent(buildMessage());
    var wa = hasWa(modalTutor.whatsapp) ? modalTutor.whatsapp : (hasWa(SITE.whatsapp) ? SITE.whatsapp : "");
    host.innerHTML =
      '<button class="btn btn-primary btn-lg bk-send" type="button" data-href="' + esc(mail) + '">✉️ ' + esc(t("book.sendEmail")) + "</button>" +
      (wa ? '<a class="btn btn-wa btn-lg" target="_blank" rel="noopener" href="https://wa.me/' + String(wa).replace(/\D/g, "") +
        "?text=" + encodeURIComponent(buildMessage()) + '">💬 ' + esc(t("book.sendWa")) + "</a>" : "") +
      '<button class="btn btn-ghost bk-copy" type="button">📋 ' + esc(t("book.copy")) + "</button>";

    $(".bk-send", host).addEventListener("click", function () {
      if (!validate()) return;
      location.href = this.dataset.href;
    });
    $(".bk-copy", host).addEventListener("click", function () {
      var btn = this, txt = buildMessage();
      function done() {
        btn.textContent = "✓ " + t("book.copied");
        setTimeout(function () { btn.textContent = "📋 " + t("book.copy"); }, 1800);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(txt).then(done, fallback);
      } else fallback();
      function fallback() {
        var ta = document.createElement("textarea");
        ta.value = txt; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  }

  function validate() {
    var err = $(".bk-err", modal);
    var name = ($("#bk-name") || {}).value.trim();
    var email = ($("#bk-email") || {}).value.trim();
    var msg = "";
    if (!chosen) msg = t("book.noSlot");
    else if (!name || !email) msg = t("book.required");
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) msg = t("book.badEmail");
    if (msg) {
      err.textContent = "⚠️ " + msg;
      err.hidden = false;
      scrollTo(err, { behavior: "smooth", block: "center" });
      return false;
    }
    err.hidden = true;
    return true;
  }

  function renderSlots() {
    var host = $(".bk-slots", modal);
    var av = modalTutor.availability || {};
    var from = tzOffsetMin(modalTutor.timezone);
    var to = myOffsetMin();
    var showMine = from != null && from !== to;

    var rows = DAYS.map(function (d, i) {
      var list = (av[d] || []).map(function (s) {
        var lbl = s, mine = false;
        if (showMine) { var c = convertSlot(i, s, from, to); lbl = c.time; mine = true; }
        return { raw: s, label: lbl, day: i, mine: mine };
      });
      if (!list.length) return "";
      return '<div class="bk-day"><span class="bk-dname">' + esc(t("days." + d)) + "</span>" +
        list.map(function (s) {
          return '<button type="button" class="bk-slot" data-day="' + s.day + '" data-time="' +
            esc(s.label) + '" data-mine="' + (s.mine ? 1 : 0) + '">' + esc(s.label) + "</button>";
        }).join("") + "</div>";
    }).filter(Boolean).join("");

    host.innerHTML = (rows || '<p class="muted">' + esc(t("book.noSlots")) + "</p>") +
      (showMine ? '<p class="bk-tznote">🕒 ' + esc(t("tz.showingYours")) + " <b>" + esc(myTzLabel()) + "</b></p>"
                : '<p class="bk-tznote">🕒 ' + esc(t("pf.schedNote")) + " " + esc(modalTutor.timezone) + "</p>");

    $all(".bk-slot", host).forEach(function (b) {
      b.addEventListener("click", function () {
        $all(".bk-slot", host).forEach(function (o) { o.classList.remove("on"); });
        b.classList.add("on");
        chosen = { day: +b.dataset.day, time: b.dataset.time, mine: b.dataset.mine === "1" };
        $(".bk-err", modal).hidden = true;
        updatePreview();
      });
    });
  }

  function openBooking(id) {
    modalTutor = tutorById(id) || T[0];
    if (!modalTutor) return;
    buildModal();
    chosen = null;
    lastFocus = document.activeElement;

    $(".bk-av", modal).src = modalTutor.thumb || modalTutor.photo;
    $(".bk-av", modal).alt = modalTutor.name;
    $("#bk-title", modal).textContent = t("book.title") + " " + modalTutor.name;
    $(".bk-sub", modal).textContent = (modalTutor.lessonLength || "50 min") + " · " + px(modalTutor.priceUSD) +
      (modalTutor.trialAvailable ? " · " + t("pf.trial") : "");
    $("#bk-tz", modal).value = myTzLabel();
    $("#bk-name", modal).value = "";
    $("#bk-email", modal).value = "";
    $("#bk-goal", modal).value = "";
    $(".bk-err", modal).hidden = true;

    renderSlots();
    updatePreview();

    modal.hidden = false;
    document.body.classList.add("no-scroll");
    requestAnimationFrame(function () {
      modal.classList.add("show");
      var f = $(".bk-slot", modal) || $("#bk-name", modal);
      if (f) f.focus();
    });
  }

  function closeBooking() {
    if (!modal) return;
    modal.classList.remove("show");
    document.body.classList.remove("no-scroll");
    setTimeout(function () { modal.hidden = true; }, 220);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function initBooking() {
    document.addEventListener("click", function (e) {
      var b = e.target.closest("[data-book]");
      if (!b) return;
      e.preventDefault();
      openBooking(b.getAttribute("data-book"));
    });
    window.EkGuruBook = openBooking;
  }

  /* =========================================================
     5. SHARE BUTTONS
     ========================================================= */
  function initShare() {
    var host = $("#share-box");
    if (!host) return;
    var id = new URLSearchParams(location.search).get("id");
    var x = tutorById(id) || T[0];
    var url = location.href;
    var title = x ? (x.name + " — Hindi tutor on EkGuru") : "EkGuru — learn Hindi online";

    host.innerHTML = '<span class="share-lbl">' + esc(t("share.title")) + "</span>" +
      '<a class="share-b wa" target="_blank" rel="noopener" title="WhatsApp" href="https://wa.me/?text=' +
        encodeURIComponent(title + " " + url) + '">💬</a>' +
      '<a class="share-b fb" target="_blank" rel="noopener" title="Facebook" href="https://www.facebook.com/sharer/sharer.php?u=' +
        encodeURIComponent(url) + '">f</a>' +
      '<a class="share-b tw" target="_blank" rel="noopener" title="X" href="https://twitter.com/intent/tweet?text=' +
        encodeURIComponent(title) + "&url=" + encodeURIComponent(url) + '">𝕏</a>' +
      '<a class="share-b em" title="Email" href="mailto:?subject=' + encodeURIComponent(title) +
        "&body=" + encodeURIComponent(url) + '">✉</a>' +
      '<button class="share-b cp" type="button" title="' + esc(t("share.copy")) + '">🔗</button>';

    $(".cp", host).addEventListener("click", function () {
      var btn = this;
      function done() {
        btn.classList.add("ok"); btn.textContent = "✓";
        setTimeout(function () { btn.classList.remove("ok"); btn.textContent = "🔗"; }, 1600);
      }
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () {});
      else done();
    });

    /* native share sheet on mobile */
    if (navigator.share) {
      var nb = document.createElement("button");
      nb.className = "share-b nt";
      nb.type = "button";
      nb.title = t("share.title");
      nb.textContent = "⤴";
      nb.addEventListener("click", function () {
        navigator.share({ title: title, url: url }).catch(function () {});
      });
      host.appendChild(nb);
    }
  }

  /* =========================================================
     6. BACK TO TOP
     ========================================================= */
  function initTop() {
    var b = document.createElement("button");
    b.className = "to-top";
    b.type = "button";
    b.setAttribute("aria-label", t("common.top"));
    b.innerHTML = "↑";
    document.body.appendChild(b);
    b.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        b.classList.toggle("show", window.scrollY > 700);
        ticking = false;
      });
    }, { passive: true });
  }


  /* =========================================================
     7. MOBILE REVIEW SLIDER
     ---------------------------------------------------------
     Below 768px the review list becomes a horizontal, snapping
     carousel. It is built on native CSS scroll-snap, so the
     scrolling itself is done by the browser — buttery smooth,
     no library, no touch-event maths.

     This layer only adds: dot indicators, a first-visit nudge
     so people realise it swipes, arrow-key support, and a
     "read more" fold for long reviews.
     ========================================================= */
  function initReviewSlider() {
    var wrap = $("[data-rev-slider]");
    if (!wrap) return;

    var cards = $all(".rev", wrap);
    if (cards.length < 2) return;               // one review needs no slider

    var MOBILE = function () { return mq("(max-width:767px)"); };

    /* ---- dots ---- */
    var dots = document.createElement("div");
    dots.className = "rev-dots";
    dots.setAttribute("role", "tablist");
    dots.setAttribute("aria-label", t("pf.reviews"));
    cards.forEach(function (c, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "rev-dot" + (i === 0 ? " on" : "");
      b.setAttribute("role", "tab");
      b.setAttribute("aria-label", (i + 1) + " / " + cards.length);
      b.addEventListener("click", function () {
        wrap.scrollTo({ left: c.offsetLeft - wrap.offsetLeft, behavior: "smooth" });
      });
      dots.appendChild(b);
    });
    wrap.parentNode.insertBefore(dots, wrap.nextSibling);

    /* ---- counter, e.g. "1 of 3" ---- */
    var count = document.createElement("p");
    count.className = "rev-count";
    count.textContent = "1 / " + cards.length;
    dots.appendChild(count);

    /* ---- keep dots in step with the scroll position ---- */
    var ticking = false;
    function sync() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var mid = wrap.scrollLeft + wrap.clientWidth / 2;
        var best = 0, bestD = Infinity;
        cards.forEach(function (c, i) {
          var cMid = c.offsetLeft - wrap.offsetLeft + c.offsetWidth / 2;
          var d = Math.abs(cMid - mid);
          if (d < bestD) { bestD = d; best = i; }
        });
        $all(".rev-dot", dots).forEach(function (d, i) {
          d.classList.toggle("on", i === best);
          d.setAttribute("aria-selected", i === best ? "true" : "false");
        });
        count.textContent = (best + 1) + " / " + cards.length;
        ticking = false;
      });
    }
    wrap.addEventListener("scroll", sync, { passive: true });

    /* ---- keyboard ---- */
    wrap.setAttribute("tabindex", "0");
    wrap.addEventListener("keydown", function (e) {
      if (!MOBILE()) return;
      var step = wrap.clientWidth * 0.9;
      if (e.key === "ArrowRight") { e.preventDefault(); wrap.scrollBy({ left: step, behavior: "smooth" }); }
      if (e.key === "ArrowLeft") { e.preventDefault(); wrap.scrollBy({ left: -step, behavior: "smooth" }); }
    });

    /* ---- first-visit nudge: a small shove so the swipe is discoverable ---- */
    if (MOBILE() && hasIO() && !safeSession("ekguru_rev_nudged")) {
      var io2 = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          io2.disconnect();
          try { sessionStorage.setItem("ekguru_rev_nudged", "1"); } catch (e) {}
          setTimeout(function () {
            wrap.scrollTo({ left: 46, behavior: "smooth" });
            setTimeout(function () { wrap.scrollTo({ left: 0, behavior: "smooth" }); }, 480);
          }, 420);
        });
      }, { threshold: 0.5 });
      io2.observe(wrap);
    }

    /* ---- fold long reviews behind a "read more" ---- */
    cards.forEach(function (c) {
      var txt = $(".rev-text", c);
      if (!txt) return;
      requestAnimationFrame(function () {
        if (txt.scrollHeight <= txt.clientHeight + 4) return;   // short enough
        c.classList.add("is-clamped");
        var more = document.createElement("button");
        more.type = "button";
        more.className = "rev-more";
        more.textContent = t("rev.more");
        more.addEventListener("click", function () {
          var open = c.classList.toggle("is-open");
          more.textContent = open ? t("rev.less") : t("rev.more");
        });
        c.appendChild(more);
      });
    });

    sync();
  }


  /* =========================================================
     8. STICKY MOBILE BOOKING BAR
     ---------------------------------------------------------
     Profile pages are long on a phone. By the time somebody has
     read the bio, the schedule and the reviews, the Book button
     is far off-screen. This pins a compact bar to the bottom
     once the user scrolls past the header, which is the single
     biggest mobile conversion win on a page like this.
     ========================================================= */
  function initStickyBook() {
    if (!$("#profile")) return;
    var id = new URLSearchParams(location.search).get("id");
    var x = tutorById(id) || T[0];
    if (!x) return;

    var bar = document.createElement("div");
    bar.className = "sticky-book";
    bar.setAttribute("aria-hidden", "true");
    bar.innerHTML =
      '<img class="sb-av" src="' + esc(x.thumb || x.photo) + '" alt="" width="38" height="38" loading="lazy">' +
      '<div class="sb-info"><b class="sb-name">' + esc(x.name) + "</b>" +
        '<span class="sb-price">' + px(x.priceUSD) + " · " + esc(x.lessonLength || "50 min") + "</span></div>" +
      '<button class="btn btn-primary sb-btn" type="button" data-book="' + esc(x.id) + '">' +
        esc(t("book.sticky")) + "</button>";
    document.body.appendChild(bar);

    var hero = $(".pf-hero");
    if (!hasIO() || !hero) return;
    var io3 = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var show = !en.isIntersecting;
        bar.classList.toggle("show", show);
        bar.setAttribute("aria-hidden", show ? "false" : "true");
        document.body.classList.toggle("has-sticky-book", show);
      });
    }, { rootMargin: "-120px 0px 0px 0px" });
    io3.observe(hero);
  }

  /* =========================================================
     9. COLLAPSIBLE PANELS ON MOBILE
     ---------------------------------------------------------
     Seven fully-open panels make the phone page enormous. The
     first two stay open (About, Intro video) and the rest fold
     into tappable headers, cutting the page length by roughly
     60% while keeping every word present for search engines —
     the content is only visually collapsed, never removed.
     ========================================================= */
  function initCollapsePanels() {
    if (!$("#profile")) return;
    if (!mq("(max-width:767px)")) return;

    var panels = $all("#profile .panel");
    panels.forEach(function (p, i) {
      var h = $("h2", p);
      if (!h) return;
      if (i < 2) { p.classList.add("is-open"); return; }   // About + Video stay open

      p.classList.add("is-collapsible");
      h.setAttribute("role", "button");
      h.setAttribute("tabindex", "0");
      h.setAttribute("aria-expanded", "false");

      var caret = document.createElement("span");
      caret.className = "panel-caret";
      caret.setAttribute("aria-hidden", "true");
      caret.textContent = "▾";
      h.appendChild(caret);

      function toggle() {
        var open = p.classList.toggle("is-open");
        h.setAttribute("aria-expanded", open ? "true" : "false");
      }
      h.addEventListener("click", toggle);
      h.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
      });
    });
  }


  /* =========================================================
     10. CURRENCY SWITCHER
     ---------------------------------------------------------
     The country guess is right most of the time, but a traveller
     or an expat may want a different currency. This adds a small
     selector to the footer, next to the founder credit.
     ========================================================= */
  function initCurrencySwitch() {
    var P = window.EkGuruPrice;
    if (!P || P.mode === "off") return;
    if (!(SITE.pricing && SITE.pricing.allowManualSwitch)) return;

    var list = P.list();
    if (list.length < 2) return;

    /* Currency names, so the menu reads "₹ INR — Indian Rupee" rather
       than a bare code most visitors will not recognise. */
    var NAMES = {
      USD: "US Dollar", INR: "Indian Rupee", EUR: "Euro", GBP: "British Pound",
      JPY: "Japanese Yen", AED: "UAE Dirham", BRL: "Brazilian Real",
      CAD: "Canadian Dollar", AUD: "Australian Dollar", NZD: "NZ Dollar",
      SGD: "Singapore Dollar", ZAR: "South African Rand", MXN: "Mexican Peso",
      PHP: "Philippine Peso", MYR: "Malaysian Ringgit", THB: "Thai Baht",
      IDR: "Indonesian Rupiah", VND: "Vietnamese Dong", KRW: "Korean Won",
      CNY: "Chinese Yuan", HKD: "Hong Kong Dollar", SAR: "Saudi Riyal",
      QAR: "Qatari Riyal", KWD: "Kuwaiti Dinar", TRY: "Turkish Lira",
      PLN: "Polish Zloty", SEK: "Swedish Krona", NOK: "Norwegian Krone",
      DKK: "Danish Krone", CHF: "Swiss Franc", ILS: "Israeli Shekel",
      PKR: "Pakistani Rupee", BDT: "Bangladeshi Taka", NPR: "Nepalese Rupee",
      LKR: "Sri Lankan Rupee", NGN: "Nigerian Naira", KES: "Kenyan Shilling",
      EGP: "Egyptian Pound", MAD: "Moroccan Dirham", RUB: "Russian Ruble",
      UAH: "Ukrainian Hryvnia", CZK: "Czech Koruna", HUF: "Hungarian Forint",
      RON: "Romanian Leu", ARS: "Argentine Peso", CLP: "Chilean Peso",
      COP: "Colombian Peso", PEN: "Peruvian Sol", MUR: "Mauritian Rupee",
      FJD: "Fijian Dollar", GHS: "Ghanaian Cedi"
    };
    var SYM = {
      USD: "$", INR: "₹", EUR: "€", GBP: "£", JPY: "¥", AUD: "A$", CAD: "C$",
      NZD: "NZ$", SGD: "S$", BRL: "R$", ZAR: "R", MXN: "$", PHP: "₱",
      KRW: "₩", CNY: "¥", HKD: "HK$", TRY: "₺", PLN: "zł", SEK: "kr",
      NOK: "kr", DKK: "kr", CHF: "Fr", ILS: "₪", PKR: "₨", NGN: "₦",
      RUB: "₽", UAH: "₴", THB: "฿", VND: "₫", IDR: "Rp", AED: "د.إ"
    };
    function label(c) { return (SYM[c] || "") + " " + c; }
    function full(c) { return label(c) + (NAMES[c] ? " — " + NAMES[c] : ""); }

    /* Sort: current first, then the seven market currencies, then the rest
       alphabetically. Most visitors find theirs in the first few rows. */
    var MARKET_CUR = ["USD", "EUR", "GBP", "INR", "JPY", "BRL", "AED"];
    var ordered = [P.currency()]
      .concat(MARKET_CUR.filter(function (c) { return c !== P.currency() && list.indexOf(c) > -1; }))
      .concat(list.filter(function (c) {
        return c !== P.currency() && MARKET_CUR.indexOf(c) === -1;
      }).sort());

    /* ---------- 1. HEADER: a dropdown beside the language globe ---------- */
    var nav = $(".nav");
    if (nav && !$("#cur-switch")) {
      var wrap = document.createElement("div");
      wrap.className = "cur-wrap";
      wrap.id = "cur-switch";
      wrap.innerHTML =
        '<button class="cur-btn" type="button" aria-haspopup="listbox" aria-expanded="false" ' +
          'aria-label="' + esc(t("cur.label")) + ': ' + esc(P.currency()) + '">' +
          COIN +
          '<span class="cur-lbl">' + esc(label(P.currency())) + "</span>" +
          '<span class="car" aria-hidden="true">▾</span>' +
        "</button>" +
        '<div class="cur-menu" role="listbox" aria-label="' + esc(t("cur.label")) + '">' +
          '<div class="cur-menu-head">' + COIN + "<span>" + esc(t("cur.label")) + "</span></div>" +
          '<div class="cur-menu-scroll">' +
          ordered.map(function (c) {
            return '<button type="button" role="option" data-cur="' + c + '"' +
              (c === P.currency() ? ' aria-selected="true" class="on"' : ' aria-selected="false"') + ">" +
              '<span class="cur-sym">' + esc(SYM[c] || c.charAt(0)) + "</span>" +
              "<span>" + esc(c) + "</span>" +
              "<small>" + esc(NAMES[c] || "") + '</small><span class="tick">✓</span></button>';
          }).join("") +
          "</div>" +
          (P.isConverted()
            ? '<p class="cur-menu-note">' + esc(t("cur.note")) + "</p>"
            : "") +
        "</div>";

      /* sit it directly after the language switcher when that exists */
      var langWrap = $("#lang-switch", nav);
      if (langWrap && langWrap.nextSibling) nav.insertBefore(wrap, langWrap.nextSibling);
      else if (langWrap) nav.appendChild(wrap);
      else nav.appendChild(wrap);

      var cbtn = $(".cur-btn", wrap), cmenu = $(".cur-menu", wrap);
      cbtn.addEventListener("click", function (e) {
        e.stopPropagation();
        var open = wrap.classList.toggle("open");
        cbtn.setAttribute("aria-expanded", open ? "true" : "false");
        if (open) {
          var sel = $(".cur-menu button.on", cmenu);
          if (sel) scrollTo(sel, { block: "center" });
        }
      });
      $all("button[data-cur]", cmenu).forEach(function (b) {
        b.addEventListener("click", function () { P.setCurrency(b.dataset.cur); });
      });
      document.addEventListener("click", function () {
        wrap.classList.remove("open");
        cbtn.setAttribute("aria-expanded", "false");
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") wrap.classList.remove("open");
      });
    }

    /* ---------- 2. FOOTER: a plain select, always reachable ---------- */
    var foot = $(".ftr-bot");
    if (foot && !$("#cur-sel")) {
      var box = document.createElement("p");
      box.className = "cur-switch";
      box.innerHTML = '<label for="cur-sel">' + esc(t("cur.label")) + "</label>" +
        '<select id="cur-sel" aria-label="' + esc(t("cur.label")) + '">' +
        ordered.map(function (c) {
          return '<option value="' + c + '"' + (c === P.currency() ? " selected" : "") + ">" +
            esc(full(c)) + "</option>";
        }).join("") + "</select>" +
        '<span class="cur-note">' + esc(t("cur.note")) + "</span>";
      foot.insertBefore(box, foot.firstChild);
      $("#cur-sel", box).addEventListener("change", function () { P.setCurrency(this.value); });
    }

    /* ---------- 3. tell the visitor we guessed, and let them undo it ---------- */
    if (P.isConverted() && !safeSession("ekguru_cur_seen")) {
      try { sessionStorage.setItem("ekguru_cur_seen", "1"); } catch (e) {}
      var tip = document.createElement("div");
      tip.className = "cur-tip";
      tip.setAttribute("role", "status");
      tip.innerHTML =
        "<span>" + esc(t("cur.detected").replace("{cur}", P.currency())) + "</span>" +
        '<button type="button" class="cur-tip-x" aria-label="' + esc(t("book.close")) + '">×</button>';
      document.body.appendChild(tip);
      setTimeout(function () { tip.classList.add("show"); }, 900);
      var hide = function () {
        tip.classList.remove("show");
        setTimeout(function () { if (tip.parentNode) tip.parentNode.removeChild(tip); }, 400);
      };
      $(".cur-tip-x", tip).addEventListener("click", hide);
      setTimeout(hide, 7000);
    }
  }

  /* =========================================================
     BOOT
     ========================================================= */
  function boot() {
    try { initLiveSearch(); } catch (e) { warn("live search", e); }
    try { initChips(); } catch (e) { warn("chips", e); }
    try { initBooking(); } catch (e) { warn("booking", e); }
    try { initTimezoneToggle(); } catch (e) { warn("timezone", e); }
    try { initShare(); } catch (e) { warn("share", e); }
    try { initTop(); } catch (e) { warn("back to top", e); }
    try { initReviewSlider(); } catch (e) { warn("review slider", e); }
    try { initStickyBook(); } catch (e) { warn("sticky book bar", e); }
    try { initCollapsePanels(); } catch (e) { warn("collapsible panels", e); }
    try { initCurrencySwitch(); } catch (e) { warn("currency switcher", e); }
  }

  /* main.js renders the profile synchronously on DOMContentLoaded,
     so running at the end of the same tick is enough. */
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
