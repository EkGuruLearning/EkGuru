/* =========================================================
   EkGuru — GOAL-BASED ONBOARDING  (Phase 7 §17, deterministic)
   ---------------------------------------------------------
   A rules-based recommender, NOT "AI personalization". It reads
   the language registry (js/languages.js) and the learning paths
   (js/learning-paths.js) and maps goal+level+time+script+context
   to a concrete recommendation. Honest: for a target language
   with no content it says so and points back to Hindi, which is
   the only PRODUCTION language today.

   Mounts on any element with id="onboarding-app".
   ========================================================= */
(function () {
  "use strict";

  var LANGS = window.EKGURU_LANGUAGES || [];
  var PATHS = window.EKGURU_PATHS || [];

  var GOALS = [
    ["everyday", "Everyday conversation", "Order food, talk to people, handle daily life."],
    ["travel", "Travel", "Survive a trip: airport, hotel, directions, food."],
    ["speaking", "Speaking", "Sound natural and be understood out loud."],
    ["reading", "Reading & writing", "Read the script and write it."],
    ["grammar", "Grammar", "Understand how the language actually works."],
    ["heritage", "Family & heritage", "Talk to family, grandparents, community."]
  ];
  var LEVELS = [["beginner", "Complete beginner"], ["elementary", "Some basics"], ["intermediate", "Conversational"]];
  var TIMES = [["5", "5–10 min a day"], ["15", "15 min a day"], ["30", "30+ min a day"]];
  var SCRIPT_GOALS = [["yes", "Yes — I want to read and write"], ["no", "No — speaking and listening only"]];

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function byId(id) { return document.getElementById(id); }

  var state = { source: "en", target: "hi", goal: "everyday", level: "beginner", time: "15", script: "yes", country: "" };

  function langOptions() {
    var prod = LANGS.filter(function (l) { return l.productionStatus === "PRODUCTION"; });
    var planned = LANGS.filter(function (l) { return l.productionStatus !== "PRODUCTION"; });
    return {
      prod: prod,
      planned: planned,
      opts: [].concat(prod, planned).map(function (l) {
        return '<option value="' + esc(l.id) + '">' + esc(l.name) + (l.productionStatus === "PRODUCTION" ? " — available" : " — coming") + "</option>";
      }).join("")
    };
  }

  function step1() {
    var lo = langOptions();
    var html =
      '<p class="lede">Three questions, no account, nothing saved. The result is a rule-based suggestion, not AI.</p>' +
      '<div class="ob-row"><label for="ob-target">What do you want to learn?</label>' +
      '<select id="ob-target">' + lo.opts + "</select></div>" +
      '<p class="muted" style="font-size:.8rem">Hindi is fully available. Other languages are listed honestly as "coming" until real content exists — no empty lessons.</p>';
    return html;
  }

  function step2() {
    return '<div class="ob-row"><label for="ob-goal">Your goal</label><select id="ob-goal">' +
      GOALS.map(function (g) { return '<option value="' + g[0] + '">' + esc(g[1]) + "</option>"; }).join("") +
      "</select></div>" +
      '<div class="ob-row"><label for="ob-level">Your level</label><select id="ob-level">' +
      LEVELS.map(function (l) { return '<option value="' + l[0] + '">' + esc(l[1]) + "</option>"; }).join("") +
      "</select></div>" +
      '<div class="ob-row"><label for="ob-time">Time you can give</label><select id="ob-time">' +
      TIMES.map(function (t) { return '<option value="' + t[0] + '">' + esc(t[1]) + "</option>"; }).join("") +
      "</select></div>" +
      '<div class="ob-row"><label for="ob-script">Reading &amp; writing?</label><select id="ob-script">' +
      SCRIPT_GOALS.map(function (s) { return '<option value="' + s[0] + '">' + esc(s[1]) + "</option>"; }).join("") +
      "</select></div>" +
      '<div class="ob-row"><label for="ob-country">Country / context (optional)</label>' +
      '<input id="ob-country" type="text" placeholder="e.g. India, USA, UK…" autocomplete="off"></div>';
  }

  /* rules (deterministic) — goal + level + script + context -> recommendation */
  function recommend() {
    var lang = null;
    LANGS.forEach(function (l) { if (l.id === state.target) lang = l; });
    if (!lang) return { unavailable: true };

    if (lang.productionStatus !== "PRODUCTION") {
      return {
        planned: true, lang: lang,
        msg: "honest: " + lang.name + " (" + lang.nativeName + ") has no lessons yet. Hindi is the only language with a full course today.",
      };
    }

    var goalSlug = { everyday: "everyday-hindi", travel: "travel-hindi", speaking: "speaking-starter",
                     reading: "reading-hindi", grammar: "grammar-foundations", heritage: "everyday-hindi" }[state.goal];
    if (state.level === "beginner") goalSlug = "hindi-from-zero";
    var path = null;
    PATHS.forEach(function (p) { if (p.slug === goalSlug) path = p; });
    var items = [];
    if (path) items.push({ title: path.title, note: path.tagline, href: "/learn/paths/" + path.slug + "/", cta: "Start this path" });
    if (state.script === "yes" && state.goal !== "reading") {
      items.push({ title: "The Hindi alphabet, explained", note: "Read Devanagari first — everything else gets easier.", href: "/learn/hindi-alphabet-for-beginners/", cta: "Learn the script" });
    }
    if (state.goal === "travel" || /india|visitor/i.test(state.country)) {
      items.push({ title: "Hindi phrases for travel", note: "Airport, hotel, food, directions, emergencies.", href: "/learn/hindi-phrases-for-travel/", cta: "Travel phrases" });
    }
    if (state.goal === "heritage" || /nri|diaspora|family|usa|uk|canada/i.test(state.country)) {
      items.push({ title: "Hindi family words", note: "Grandparents, relatives and home conversation.", href: "/learn/hindi-family-words/", cta: "Family words" });
    }
    items.push({ title: "Hindi Topic Quiz", note: "Check where you are with 5–15 questions and explanations.", href: "/learn/hindi/practice/quiz/", cta: "Take a quick quiz" });

    var timeNote = { "5": "Short sessions: use the 10-minute lessons and one practice tool a day.",
                     "15": "A lesson plus a practice session a day fits your time.",
                     "30": "Pair a lesson with review cards and a worksheet for deeper sessions." }[state.time];
    return { planned: false, lang: lang, items: items.slice(0, 4), timeNote: timeNote, path: path };
  }

  function renderResult() {
    var r = recommend();
    var html;
    if (r.unavailable) {
      html = '<div class="note">Please choose a language.</div>';
    } else if (r.planned) {
      html =
        '<div class="note"><b>' + esc(r.lang.name) + " (" + esc(r.lang.nativeName) + ") is planned.</b> " + esc(r.msg) +
        '</div><p><a class="btn" href="/learn/hindi/">Learn Hindi instead</a> <a class="btn ghost" href="/languages/">See all languages</a></p>' +
        '<p class="muted" style="font-size:.8rem">No empty lessons are created just to fill a language list. ' + esc(r.lang.name) +
        " becomes available when real, reviewed content exists.</p>";
    } else {
      var cards = r.items.map(function (it) {
        return '<div class="ob-card"><div><b>' + esc(it.title) + "</b><p class=\"muted\">" + esc(it.note) + "</p></div>" +
          '<a class="btn" href="' + esc(it.href) + '">' + esc(it.cta) + "</a></div>";
      }).join("");
      html =
        '<div class="note"><b>Your starting point for ' + esc(r.lang.name) + ".</b> " + esc(r.timeNote) + "</div>" +
        '<div class="ob-cards">' + cards + "</div>" +
        '<p class="muted" style="font-size:.8rem">Based on simple rules (goal, level, time, reading goal, context) — not AI. ' +
        "Everything is free; your choices are not saved.</p>";
    }
    byId("ob-result").innerHTML = html;
  }

  function mount(host) {
    host.innerHTML =
      '<div id="ob-step1"></div><div id="ob-step2" hidden></div>' +
      '<div class="ob-nav" style="margin:14px 0;display:flex;gap:10px;flex-wrap:wrap">' +
      '<button type="button" class="btn ghost" id="ob-back" hidden>Back</button>' +
      '<button type="button" class="btn" id="ob-next">Continue</button>' +
      "</div>" +
      '<div id="ob-result" style="margin-top:14px"></div>';

    byId("ob-step1").innerHTML = step1();
    byId("ob-step2").innerHTML = step2();

    function read() {
      state.target = byId("ob-target").value;
      state.goal = byId("ob-goal").value;
      state.level = byId("ob-level").value;
      state.time = byId("ob-time").value;
      state.script = byId("ob-script").value;
      state.country = byId("ob-country").value || "";
    }

    byId("ob-next").addEventListener("click", function () {
      if (byId("ob-step2").hidden) {
        byId("ob-step1").hidden = true;
        byId("ob-step2").hidden = false;
        byId("ob-back").hidden = false;
        byId("ob-next").textContent = "Show my starting point";
        return;
      }
      read();
      renderResult();
      byId("ob-result").scrollIntoView({ behavior: "smooth", block: "start" });
    });

    byId("ob-back").addEventListener("click", function () {
      byId("ob-step2").hidden = true;
      byId("ob-step1").hidden = false;
      byId("ob-back").hidden = true;
      byId("ob-next").textContent = "Continue";
    });
  }

  function boot() {
    var host = document.getElementById("onboarding-app");
    if (host) mount(host);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
