/* EkGuru — PHASE COURSE PLAYER (generic, data-driven).
   NEW file: renders data/courses/phase-1/<code>_<level>.json + data/courses/index.json.
   No dependencies. Progress in localStorage. TTS via speechSynthesis. */
(function () {
"use strict";

var TTS_LANG = { en: "en-GB", fil: "fil-PH", pl: "pl-PL", ro: "ro-RO", tr: "tr-TR", uk: "uk-UA", uzn: "uz-UZ", vi: "vi-VN", kk: "kk-KZ", npi: "ne-NP", zsm: "ms-MY", sw: "sw-KE", nl: "nl-NL", fa: "fa-IR", so: "so-SO", ca: "ca-ES", id: "id-ID", el: "el-GR", af: "af-ZA", es: "es-ES", fr: "fr-FR", de: "de-DE", it: "it-IT", pt: "pt-BR", ru: "ru-RU", ar: "ar-SA", ja: "ja-JP", ko: "ko-KR", zh: "zh-CN", hi: "hi-IN", bn: "bn-IN", pa: "pa-IN", ur: "ur-PK", ta: "ta-IN", te: "te-IN", mr: "mr-IN", gu: "gu-IN", kn: "kn-IN", ml: "ml-IN" };
/* Phase directories the course files may be grouped into. A course's 6 level
   files normally share one phase, but split batches in history left a few
   courses (bn/mr/pa/te) with A1-B2 in one directory and C1-C2 in another.
   fetchLevel below probes these in order so a level always resolves. */
var ALL_PHASES = ["phase-1", "phase-2", "phase-3", "phase-4", "phase-5", "phase-6", "phase-7", "phase-8", "phase-9", "phase-10"];
var LEVEL_NAMES = { 
  A1: "Beginner - Child", 
  A2: "Elementary - Kids", 
  A3: "Pre-Intermediate - Teens", 
  B1: "Intermediate - Young Adults", 
  B2: "Upper Intermediate - Adults", 
  B3: "Advanced - Mature Adults", 
  C1: "Proficient - Seniors", 
  C2: "Mastery - Elders", 
  C3: "Expert - Masters", 
  C4: "Scholar - Academic", 
  C5: "Guru - Complete Mastery" 
};
var EXTENDED_LEVELS = ["A1","A2","A3","B1","B2","B3","C1","C2","C3","C4","C5"];
var LS_KEY = "eg-course-progress-v1";
var PRACTICE_KEY = "eg-course-practice-v1";
var PRACTICE_CHOICE = ["choose", "multiple_choice", "matching", "word_selection", "listen_and_choose"];
var PRACTICE_REORDER = ["reorder", "sentence_building", "listen_and_reorder", "discourse_ordering"];
var PRACTICE_AUDIO = ["listening_comprehension", "dictation", "listen_and_choose", "listen_and_reorder", "listen_and_fill", "repeat_after_audio", "pronunciation", "shadowing"];
var PRACTICE_SPEAK = ["speak", "repeat_after_audio", "pronunciation", "shadowing", "guided_speaking", "free_response", "roleplay"];
function hasType(list, type) { return list.indexOf(type) >= 0; }
function practiceLabel(type) { return String(type || "practice").replace(/_/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); }); }

function esc(s) {
  return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function norm(s) {
  return String(s == null ? "" : s).toLowerCase().trim().replace(/[\s.\u00a0!?¡¿,;:'"«»„“”‘’—–\-()\[\]]+/g, " ").replace(/\s+/g, " ").trim();
}
function el(html) {
  var d = document.createElement("div");
  d.innerHTML = html;
  return d.firstChild;
}
function speak(text, code) {
  try {
    if (!("speechSynthesis" in window)) return false;
    var u = new SpeechSynthesisUtterance(String(text));
    u.lang = TTS_LANG[code] || "en-US";
    u.rate = 0.92;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
    return true;
  } catch (e) { return false; }
}
function loadProgress() {
  try { return JSON.parse(localStorage.getItem(LS_KEY) || "{}"); } catch (e) { return {}; }
}
function saveProgress(p) {
  try { localStorage.setItem(LS_KEY, JSON.stringify(p)); } catch (e) {}
}
function markDone(key, lessonId) {
  var p = loadProgress();
  p[key] = p[key] || { done: [], test: 0 };
  if (p[key].done.indexOf(lessonId) < 0) p[key].done.push(lessonId);
  saveProgress(p);
}
function markTest(key, score) {
  var p = loadProgress();
  p[key] = p[key] || { done: [], test: 0 };
  p[key].test = Math.max(p[key].test || 0, score);
  saveProgress(p);
}
/* Free, quota-free course-data API: versioned JSON is fetched once and cached above.
   Attempt state stays on-device, so reloads never erase question history or mastery. */
function practiceId(code, item) {
  var raw = code + "|" + String(item.type || "") + "|" + String(item.q || "") + "|" + String(item.answer || "");
  var h = 2166136261;
  for (var i = 0; i < raw.length; i++) { h ^= raw.charCodeAt(i); h = Math.imul(h, 16777619); }
  return code + ":" + (h >>> 0).toString(36);
}
function practiceHistory() {
  try { return JSON.parse(localStorage.getItem(PRACTICE_KEY) || "{}") || {}; } catch (e) { return {}; }
}
function recordPractice(code, item, correct) {
  var all = practiceHistory(), id = practiceId(code, item), row = all[id] || { attempts: 0, correct: 0, last: 0 };
  row.attempts++; if (correct) row.correct++; row.last = Date.now(); all[id] = row;
  try { localStorage.setItem(PRACTICE_KEY, JSON.stringify(all)); } catch (e) {}
  return row;
}

var CSS = [
"/* Modern responsive course player v300 - fixes laptop visual bug */",
".egc{font-family:Inter,system-ui,-apple-system,'Segoe UI',Roboto,'Noto Sans',sans-serif;line-height:1.7;color:#10131f;max-width:1180px;margin:0 auto;padding:clamp(12px,2vw,24px);width:100%;box-sizing:border-box}",
".egc h1{font-size:clamp(1.5rem,4vw,2.2rem);line-height:1.2;letter-spacing:-.02em;margin:12px 0}.egc h2{font-size:clamp(1.2rem,3vw,1.5rem);margin-top:2em;border-bottom:2px solid #e5eaf1;padding-bottom:.4em}.egc h3{font-size:clamp(1rem,2.5vw,1.2rem);margin-top:1.4em}",
".egc .crumbs{font-size:.85rem;color:#5b6b7f;margin-bottom:1em;flex-wrap:wrap;display:flex;gap:6px;align-items:center}.egc .crumbs a{color:#4f32d9;text-decoration:none;font-weight:600}.egc .crumbs a:hover{text-decoration:underline}",
".egc .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,280px),1fr));gap:14px}",
".egc .card{border:1px solid #e6e1fb;border-radius:16px;padding:16px;background:#fff;box-shadow:0 2px 12px rgba(15,18,34,.06);transition:.25s cubic-bezier(.22,1,.36,1);overflow:hidden}",
".egc .card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(15,18,34,.12);border-color:#4f32d9}",
".egc .card a{color:inherit;text-decoration:none;display:block}.egc .card b{font-size:1.05rem;display:block;line-height:1.3}.egc .card .sub{font-size:.84rem;color:#5b6b7f;margin-top:4px}",
".egc .lvlrow{display:flex;gap:10px;margin:16px 0;flex-wrap:wrap}.egc .lvlab{border:1px solid #4f32d9;color:#4f32d9;border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:700;font-size:.9rem;transition:.2s;min-height:40px;display:inline-flex;align-items:center}",
".egc .lvlab:hover{background:#f5f2ff;transform:translateY(-1px)}.egc .lvlab.done{background:#e7f6ec;border-color:#1d9e57;color:#14713d}",
".egc .pill{display:inline-flex;align-items:center;gap:6px;background:#f5f2ff;color:#4f32d9;border:1px solid #e6e1fb;border-radius:999px;padding:6px 12px;font-size:.8rem;font-weight:700;margin:2px}",
".egc table.vocab{border-collapse:separate;border-spacing:0;width:100%;font-size:.95rem;border:1px solid #e6e1fb;border-radius:12px;overflow:hidden;background:#fff}.egc table.vocab th,.egc table.vocab td{border-bottom:1px solid #e6e1fb;padding:10px 12px;text-align:left}.egc table.vocab th{background:#f6f4ff;font-weight:700;color:#4f32d9}.egc .roman{color:#6a5aa8;font-style:italic}.egc .pos{font-size:.75rem;color:#7b8aa0;background:#f5f2ff;padding:2px 6px;border-radius:6px}",
".egc .dlg{border-left:4px solid #4f32d9;background:linear-gradient(135deg,#f6f4ff,#fff);border-radius:0 12px 12px 0;padding:12px 16px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,.04)}",
".egc .dlg .sp{font-weight:800;color:#4f32d9}.egc .dlg .en{color:#4c5b70;font-size:.92rem;margin-top:4px}",
".egc button.sayn{margin-left:8px;font-size:.8rem;border:1px solid #d9d6e8;background:#fff;border-radius:999px;padding:6px 12px;cursor:pointer;transition:.2s;min-height:32px}.egc button.sayn:hover{border-color:#4f32d9;color:#4f32d9;background:#f5f2ff}",
".egc .ex{background:#fffbe8;border:1px solid #f0dfa0;border-radius:12px;padding:12px 16px;margin:12px 0}.egc .mist{background:#fef1f1;border:1px solid #f3c2c2;border-radius:12px;padding:12px 16px;margin:12px 0}",
".egc .q{border:1px solid #e6e1fb;border-radius:16px;padding:16px;margin:14px 0;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.04);transition:.2s}.egc .q:hover{box-shadow:0 4px 16px rgba(0,0,0,.06)}",
".egc .q input[type=text]{width:100%;box-sizing:border-box;font-size:1rem;padding:12px 14px;border:1px solid #d9d6e8;border-radius:12px;margin:8px 0;transition:.2s}.egc .q input[type=text]:focus{outline:0;border-color:#4f32d9;box-shadow:0 0 0 3px rgba(79,50,217,.12)}",
".egc .q .opts{display:flex;flex-direction:column;gap:8px;margin:10px 0}.egc .q .opt{border:1px solid #d9d6e8;border-radius:12px;padding:12px 14px;background:#fbfdff;cursor:pointer;text-align:left;font-size:.95rem;transition:.2s;min-height:44px}",
".egc .q .opt:hover{border-color:#4f32d9;background:#f5f2ff;transform:translateY(-1px)}.egc .q .opt.right{border-color:#1d9e57;background:#e7f6ec;color:#14713d}.egc .q .opt.wrong{border-color:#d64545;background:#fdeeee;color:#b42318}",
".egc .btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:0;border-radius:999px;background:linear-gradient(135deg,#4f32d9,#8b5cf6);color:#fff;font-weight:700;padding:12px 20px;font-size:.95rem;cursor:pointer;margin:6px;min-height:44px;transition:.2s;box-shadow:0 4px 12px rgba(79,50,217,.2);text-decoration:none}",
".egc .btn:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(79,50,217,.3)}.egc .btn.ghost{background:#fff;color:#10131f;border:1px solid #e4e4ef;box-shadow:none}.egc .btn.ghost:hover{border-color:#4f32d9;color:#4f32d9}.egc .btn.green{background:linear-gradient(135deg,#1d9e57,#10b981)}",
".egc .fb{font-weight:700;margin-top:10px;padding:8px 12px;border-radius:8px}.egc .fb.ok{color:#14713d;background:#e7f6ec}.egc .fb.no{color:#b42323;background:#fef1f1}.egc .why{font-size:.88rem;color:#4c5b70;margin-top:8px;padding:8px 12px;background:#f8f7fd;border-radius:8px}",
".egc .ro-words{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.egc .ro-w{border:1px solid #4f32d9;border-radius:10px;padding:8px 12px;cursor:pointer;background:#f4f8ff;font-weight:600;transition:.2s;min-height:36px}.egc .ro-w:hover{background:#4f32d9;color:#fff;transform:translateY(-1px)}",
".egc .ro-built{min-height:52px;border:2px dashed #9fb4d0;border-radius:12px;padding:12px;background:#fbfdff;margin:10px 0;font-size:1.05rem}",
".egc .fc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,180px),1fr));gap:12px}",
".egc .fc{border:1px solid #e6e1fb;border-radius:16px;padding:16px;min-height:100px;cursor:pointer;background:linear-gradient(180deg,#fff,#f6f4ff);text-align:center;transition:.25s;box-shadow:0 2px 8px rgba(0,0,0,.04)}.egc .fc:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.08)}",
".egc .fc .front{font-weight:800;font-size:1.1rem;color:#4f32d9}.egc .fc .back{display:none}.egc .fc.flip .front{display:none}.egc .fc.flip .back{display:block}",
".egc .score{font-size:clamp(1.1rem,3vw,1.3rem);font-weight:800;background:linear-gradient(135deg,#f5f2ff,#ede8ff);border:1px solid #e6e1fb;border-radius:16px;padding:16px;text-align:center;color:#4f32d9}",
".egc .navrow{display:flex;justify-content:space-between;margin:24px 0;gap:12px;flex-wrap:wrap}",
".egc .alpha{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,130px),1fr));gap:10px}.egc .alpha .card{text-align:center;padding:20px}",
".egc .count{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,140px),1fr));gap:10px}.egc .rules{background:linear-gradient(135deg,#f6f4ff,#fff);border:1px solid #e6e1fb;border-radius:12px;padding:14px 16px;margin-top:14px}",
"@media(max-width:900px){.egc .grid{grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr))}}",
"@media(max-width:640px){.egc{padding:12px}.egc .grid{grid-template-columns:1fr}.egc .alpha{grid-template-columns:repeat(auto-fill,minmax(100px,1fr))}.egc .fc-grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr))}.egc .navrow{flex-direction:column}.egc .btn{width:100%}}",
"@media print{.egc .noprint{display:none!important}.egc{max-width:none!important;padding:0!important}.egc .card,.egc .q{box-shadow:none!important;border:1px solid #999!important;break-inside:avoid}}",
"/* Age-based visual theming */",
".egc.level-a1{background:linear-gradient(180deg,#fefce8 0,#fff 300px)}.egc.level-a2{background:linear-gradient(180deg,#f0fdf4 0,#fff 300px)}.egc.level-a3{background:linear-gradient(180deg,#ecfdf5 0,#fff 300px)}",
".egc.level-b1{background:linear-gradient(180deg,#eff6ff 0,#fff 300px)}.egc.level-b2{background:linear-gradient(180deg,#eef2ff 0,#fff 300px)}.egc.level-b3{background:linear-gradient(180deg,#f5f3ff 0,#fff 300px)}",
".egc.level-c1{background:linear-gradient(180deg,#fdf2f8 0,#fff 300px)}.egc.level-c2{background:linear-gradient(180deg,#faf5ff 0,#fff 300px)}.egc.level-c3,.egc.level-c4,.egc.level-c5{background:linear-gradient(180deg,#f8fafc 0,#fff 300px)}",
"/* Dotted tracing visuals */",
".egc .dotted{font-size:2rem;font-weight:900;color:transparent;-webkit-text-stroke:2px #4f32d9;letter-spacing:.1em;border:2px dashed #d9d6e8;border-radius:12px;padding:16px;text-align:center;margin:12px 0;background:repeating-linear-gradient(45deg,#f6f4ff,#f6f4ff 10px,#fff 10px,#fff 20px)}",
".egc .visual-hint{display:flex;align-items:center;gap:10px;padding:10px 14px;background:#fff8e6;border:1px solid #f0dfa0;border-radius:10px;margin:10px 0;font-size:.9rem}"
].join("\n");

function ensureCSS() {
  if (document.getElementById("egc-css")) return;
  var s = document.createElement("style");
  s.id = "egc-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}

function Player(mount, opts) {
  this.mount = mount;
  this.base = (opts && opts.base) || "./";
  if (this.base.slice(-1) !== "/") this.base += "/";
  this.index = null;
  this.cache = {};
  var self = this;
  window.addEventListener("hashchange", function () { self.route(); });
}
Player.prototype.fetchJSON = function (path) {
  var self = this;
  if (self.cache[path]) return Promise.resolve(self.cache[path]);
  return fetch(path).then(function (r) {
    if (!r.ok) throw new Error("HTTP " + r.status + " for " + path);
    return r.json();
  }).then(function (d) { self.cache[path] = d; return d; });
};
/* Load one level file, probing every phase directory the course data has ever
   used. Never throws on a phase mismatch: a missing variant is just skipped.
   Resolves the data or rejects with a single clear error. */
Player.prototype.fetchLevel = function (phase, level) {
  var self = this;
  var probes = [];
  if (phase) probes.push(phase);
  ALL_PHASES.forEach(function (p) { if (probes.indexOf(p) < 0) probes.push(p); });
  var tried = [];
  var next = function (i) {
    if (i >= probes.length) {
      var err = new Error("Level file not found for " + (level || "?"));
      err.tried = tried.slice();
      return Promise.reject(err);
    }
    var p = probes[i];
    var path = self.base + "data/courses/" + p + "/" + level + ".json";
    tried.push(path);
    return fetch(path).then(function (r) {
      if (r.ok) return r.json();
      throw new Error("HTTP " + r.status + " for " + path);
    }).then(function (d) { self.cache[path] = d; return d; })
      .catch(function () { return next(i + 1); });
  };
  return next(0);
};
Player.prototype.parseHash = function () {
  var h = (location.hash || "").replace(/^#\/?/, "");
  var parts = h.split("/").filter(Boolean);
  var q = {};
  try {
    location.search.slice(1).split("&").forEach(function (kv) {
      var p = kv.split("="); if (p[0]) q[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || "");
    });
  } catch (e) {}
  return {
    lang: parts[0] || q.lang || "",
    level: (parts[1] || q.level || "").toUpperCase(),
    lesson: parts[2] || q.lesson || "",
    test: parts[2] === "test" || q.view === "test"
  };
};
Player.prototype.route = function () {
  var self = this;
  var r = self.parseHash();
  self.mount.innerHTML = '<div class="egc google-anno-skip"><p>Loading…</p></div>';
  Promise.all([
    self.fetchJSON(self.base + "data/courses/index.json"),
    self.fetchJSON(self.base + "data/global/language-country-relations.json").catch(function () { return { relations: [] }; })
  ]).then(function (payload) {
    self.index = payload[0];
    self.relations = payload[1].relations || [];
    if (!r.lang) return self.renderHub();
    if (!r.level) return self.renderLang(r.lang);
    var key = r.lang + "_" + r.level;
    var entry = self.langMeta(r.lang);
    var phase = entry.phase || "phase-1";
    var file = key + ".json";
    (entry.files || []).forEach(function (f) { if (f.indexOf(key) === 0) file = f; });
    // The manifest's `files` list may not actually mirror where each level
    // physically lives (e.g. bn_A1 only exists under phase-2 while bn_C1 is
    // under phase-1). Prefer the concrete path when the manifest names it,
    // otherwise probe every phase directory so the level still loads.
    var fetcher;
    if (file !== key + ".json") {
      fetcher = self.fetchJSON(self.base + "data/courses/" + phase + "/" + file)
        .catch(function () { return self.fetchLevel(phase, key); });
    } else {
      fetcher = self.fetchLevel(phase, key);
    }
    return fetcher.then(function (d) {
      if (d && d.file_level !== r.level) {
        throw new Error("Found a mismatched level file for " + key);
      }
      if (r.test) return self.renderTest(d, key);
      if (r.lesson) return self.renderLesson(d, key, r.lesson);
      return self.renderLevel(d, key);
    });
  }).catch(function (e) {
    self.mount.innerHTML = '<div class="egc google-anno-skip"><h1>Course failed to load</h1><p>' + esc(e.message) + '</p><p><a href="#/">Back to all courses</a></p></div>';
  });
};
Player.prototype.crumbs = function (items) {
  return '<div class="crumbs">' + items.map(function (it, i) {
    var sep = i ? " › " : "";
    return sep + (it.href ? '<a href="' + it.href + '">' + esc(it.t) + "</a>" : esc(it.t));
  }).join("") + "</div>";
};
Player.prototype.renderHub = function () {
  var self = this, courses = (this.index && this.index.courses) || [], relations = this.relations || [];
  /* Country contexts per course code. Six languages have no ISO 639-1 row in
     the relations data (Standard Arabic is only "arb", Mandarin only "cmn"),
     so without the bridge their cards showed no countries at all while the
     static HTML — which uses the same bridge — showed thirty. */
  var ISO3_ALIAS = { arb: "ar", cmn: "zh", fil: "fil", npi: "npi", uzn: "uzn", zsm: "zsm" };
  var countriesByCode = {};
  relations.forEach(function (r) {
    var code = r.iso_639_1 || ISO3_ALIAS[r.iso_639_3] || r.iso_639_3;
    if (!code) return;
    (countriesByCode[code] = countriesByCode[code] || []).push(r.country_id);
  });
  Object.keys(countriesByCode).forEach(function (k) {
    countriesByCode[k] = Array.from(new Set(countriesByCode[k])).sort();
  });
  var relationsByCountry = {};
  relations.forEach(function (r) { (relationsByCountry[r.country_id] = relationsByCountry[r.country_id] || []).push(r); });
  var countries = Array.from(new Set([].concat.apply([], Object.keys(countriesByCode).map(function (k) { return countriesByCode[k]; })))).sort();

  /* Which countries actually have a course — computed BEFORE the hero, which
     counts them, and used again by the dropdown and the empty state. */
  var courseCountries = {}, countryCourseCount = {};
  courses.forEach(function (c) {
    (countriesByCode[c.code] || []).forEach(function (cc) {
      courseCountries[cc] = 1;
      countryCourseCount[cc] = (countryCourseCount[cc] || 0) + 1;
    });
  });
  var withCourses = countries.filter(function (c) { return courseCountries[c]; });
  var withoutCourses = countries.filter(function (c) { return !courseCountries[c]; });

  var displayNames;
  try { displayNames = new Intl.DisplayNames([document.documentElement.lang || "en"], { type: "region" }); } catch (e) {}
  function countryName(code) { try { return displayNames ? displayNames.of(code) : code; } catch (e) { return code; } }
  var h = '<div class="egc course-hub google-anno-skip"><section class="course-hero"><span class="pill">Worldwide · A1–C2 · free</span><h1>Choose your language journey</h1>';
  /* "course mai language ko country wise bi search kr ske": the dropdown and
     the search box below cover the question for anyone who types. The static
     page covers everyone else — 194 countries written out, linked and
     crawlable — so it is linked from here rather than hidden in a footer. */
  h += '<p>One complete learning space for courses, country contexts, lessons, deep practice, review history and level tests. Not sure which language? <a href="' + esc(self.base) + 'courses/by-country/"><b>Browse courses by country</b></a> — ' + withCourses.length + ' countries with a course today.</p><div class="course-orbit" aria-hidden="true"><i>अ</i><i>Α</i><i>ع</i><i>あ</i><i>മ</i></div></section>';
  /* Which countries actually have a course. The dropdown used to list every
     country in the inventory — all 200 — so picking most of them emptied the
     grid with a bare "0 courses", which reads as a broken search. Prakash:
     "course mai language ko country wise bi search kr ske jo abhi work nahi
     kar raha". The two groups tell the truth up front: countries you can
     learn a language for today, and countries the inventory documents but no
     course has been written for yet. */
  h += '<div class="course-tools"><label>Find a language or country<input id="course-search" type="search" placeholder="e.g. Italian, Japan, Arabic" autocomplete="off" aria-describedby="course-result-count"></label><label>Country context<select id="country-filter">';
  h += '<option value="">All countries</option>';
  h += '<optgroup label="Learn a language for (' + withCourses.length + ')">' + withCourses.map(function (c) { return '<option value="' + esc(c) + '">' + esc(countryName(c)) + ' · ' + countryCourseCount[c] + '</option>'; }).join("") + '</optgroup>';
  /* Today the inventory's 194 countries are all covered by at least one of the
     39 courses, so this group is usually empty — an empty <optgroup> renders
     as a stray heading, so it is only written when it has members. A country
     added to the inventory before its language is authored lands here. */
  if (withoutCourses.length) {
    h += '<optgroup label="Documented, no course yet (' + withoutCourses.length + ')">' + withoutCourses.map(function (c) { return '<option value="' + esc(c) + '">' + esc(countryName(c)) + '</option>'; }).join("") + '</optgroup>';
  }
  h += '</select></label><span id="course-result-count" role="status"></span></div>';
  h += '<section id="country-story" class="country-story" hidden aria-live="polite"></section>';
  h += '<div id="course-empty" class="course-empty" hidden></div>';
  var phases = {};
  courses.forEach(function (c) { var ph = c.phase || "phase-1"; (phases[ph] = phases[ph] || []).push(c); });
  Object.keys(phases).sort().forEach(function (ph) {
    h += '<section class="course-phase"><h2>Collection ' + esc(String(ph).replace("phase-", "")) + '</h2><div class="grid course-grid">';
    phases[ph].forEach(function (c, ci) {
      var lvs = Object.keys(c.levels || {}), cs = countriesByCode[c.code] || [], hue = Math.abs(c.code.split("").reduce(function (a, x) { return a * 31 + x.charCodeAt(0); }, 7)) % 360;
      var saved = loadProgress(), done = 0, total = 0;
      lvs.forEach(function (lv) { var row = saved[c.code + "_" + lv]; done += row && row.done ? row.done.length : 0; total += (c.levels[lv] && c.levels[lv].lessons) || 6; });
      var pct = total ? Math.min(100, Math.round(done / total * 100)) : 0;
      /* Native name lookup. The catalogue is keyed by ISO 639-1 and some
         row sets carry only ISO 639-3 (Arabic ships as "arb", Chinese as
         "cmn"), so those codes are bridged instead of falling back to the
         English name — which is how a card ended up reading "Arabic /
         Arabic". When the native name really is the English name the line is
         dropped rather than repeated. */
      var nativeName = c.native || ((relations.find(function (r) {
        return (r.iso_639_1 === c.code || ISO3_ALIAS[r.iso_639_3] === c.code || r.iso_639_3 === c.code) && r.native_name;
      }) || {}).native_name) || "";
      var nativeSpan = (nativeName && nativeName.toLowerCase() !== String(c.name).toLowerCase())
        ? '<span class="native-name" lang="' + esc(c.code) + '" dir="auto">' + esc(nativeName) + '</span>'
        : "";
      if (!nativeName) nativeName = c.name;
      /* The voice control is a button, so it must live OUTSIDE the <a> that
         opens the course (a <button> inside an <a> is invalid HTML and lets a
         tap trigger the link instead of the sound). The link is stretched to
         cover the card; the button sits above it with a higher z-index. */
      /* data-search is what the box matches against — the language, its own
         name, its code, and every country it is documented in. The first
         version matched the language name only, so typing "Japan" or "UAE"
         returned nothing and the country box was the only way through. */
      var searchBlob = [c.name, nativeName, c.code, c.phase || ""]
        .concat(cs, cs.map(countryName))
        .concat(cs.map(function (x) { return countryName(x); }).join(" "))
        .join(" ");
      h += '<article class="card course-card" data-name="' + esc(c.name.toLowerCase()) + '" data-search="' + esc(norm(searchBlob)) + '" data-countries="' + esc(cs.join(" ")) + '" style="--course-hue:' + hue + '"><a href="#/' + esc(c.code) + '" class="course-link" aria-label="Open ' + esc(c.name) + ' course"><span class="course-monogram" aria-hidden="true">' + esc(nativeName.slice(0, 2)) + '</span><span class="course-copy"><b>' + esc(c.name) + '</b>' + nativeSpan + '<span class="sub">' + esc(lvs.join(" · ")) + (c.complete ? " · complete" : "") + '</span><span class="country-chips">' + cs.slice(0, 5).map(function (x) { return '<em title="' + esc(countryName(x)) + '">' + esc(countryName(x)) + '</em>'; }).join("") + (cs.length > 5 ? '<em>+' + (cs.length - 5) + '</em>' : '') + '</span><span class="course-progress"><i style="width:' + pct + '%"></i></span><small class="progress-label">' + (done ? done + ' of ' + total + ' lessons complete' : 'Start at A1 or choose your level') + '</small></span><span class="course-arrow">→</span></a><button type="button" class="course-voice" data-voice-code="' + esc(c.code) + '" data-voice-text="' + esc(nativeName) + '" aria-label="Hear ' + esc(c.name) + '">🔊 Hear language</button></article>';
    });
    h += "</div></section>";
  });
  if (!courses.length) h += "<p>No courses found in index.</p>";
  h += "</div>";
  this.mount.innerHTML = h;
  this.mount.querySelectorAll(".course-voice").forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault(); event.stopPropagation();
      var text = button.getAttribute("data-voice-text"), code = button.getAttribute("data-voice-code");
      if (!speak(text, code)) button.textContent = "Voice unavailable";
    });
  });
  var search = this.mount.querySelector("#course-search"), filter = this.mount.querySelector("#country-filter"), count = this.mount.querySelector("#course-result-count"), story = this.mount.querySelector("#country-story");
  var empty = this.mount.querySelector("#course-empty");

  /* ---------------------------------------------------------------
     Country → language, the two directions of the same question.

     A reader arrives with one of these in their head:

        "I am in Japan — what can I learn?"     (the country box)
        "Japanese — is that here?"              (the search box)
        "What do you have for the Gulf?"        (a country, by name, typed)

     All three have to work, and they have to say something useful when the
     answer is "nothing yet" — an empty grid with no explanation is what made
     this look broken. So: every card is searchable by its countries, the
     country list is split into countries with a course and countries without,
     and an empty result offers the closest real options instead of a blank.
     --------------------------------------------------------------- */

  /* The first inventory row for a course's language — its family and script
     are what "closest course" is decided on. */
  var relByCode = {};
  relations.forEach(function (r) {
    var code = r.iso_639_1 || ISO3_ALIAS[r.iso_639_3] || r.iso_639_3;
    if (code && !relByCode[code]) relByCode[code] = r;
  });

  function documented(country) {
    var seen = {}, rows = [];
    (relationsByCountry[country] || []).forEach(function (r) {
      var k = r.language_id || r.language_name;
      if (!k || seen[k]) return;
      seen[k] = 1;
      rows.push(r);
    });
    return rows.sort(function (x, y) {
      return String(x.language_name).localeCompare(String(y.language_name));
    });
  }

  function hasCourse(row) {
    var code = row.iso_639_1 || ISO3_ALIAS[row.iso_639_3] || row.iso_639_3;
    return courses.some(function (c) { return c.code === code; });
  }

  /* "The closest thing we do have": the same language if we have it, else a
     language sharing the country's writing system, else the same family. */
  function suggestionsFor(country, limit) {
    var rows = documented(country), fams = {}, scripts = {}, langs = {};
    rows.forEach(function (r) {
      if (r.language_family) fams[r.language_family] = 1;
      if (r.script) scripts[r.script] = 1;
      langs[r.iso_639_1 || r.iso_639_3] = 1;
    });
    var out = [];
    courses.forEach(function (c) {
      var rel = relByCode[c.code] || {}, why = "";
      if (langs[c.code]) why = "the language itself";
      else if (rel.script && scripts[rel.script]) why = "same writing system (" + rel.script + ")";
      else if (rel.language_family && fams[rel.language_family]) why = "same language family (" + rel.language_family + ")";
      if (why) out.push({ c: c, why: why });
    });
    out.sort(function (x, y) {
      var xs = x.why === "the language itself" ? 0 : 1, ys = y.why === "the language itself" ? 0 : 1;
      return xs - ys || String(x.c.name).localeCompare(String(y.c.name));
    });
    return out.slice(0, limit || 3);
  }

  function courseLink(c, why) {
    return '<a class="course-suggest" href="#/' + esc(c.code) + '"><b>' + esc(c.name) + "</b>" +
      (why ? "<small>" + esc(why) + "</small>" : "") + "</a>";
  }

  function renderCountryStory(country) {
    if (!country) { story.hidden = true; story.innerHTML = ""; return; }
    var langs = documented(country), categories = {}, scripts = {}, bands = {};
    langs.forEach(function (r) {
      if (r.category) categories[r.category] = 1;
      if (r.script) scripts[r.script] = 1;
      if (r.estimated_speaker_band) bands[r.estimated_speaker_band] = 1;
    });
    var available = langs.filter(hasCourse);
    var hue = Math.abs(country.charCodeAt(0) * 31 + country.charCodeAt(1)) % 360;
    story.style.setProperty("--country-hue", hue);
    var chips = (available.length ? available : langs.slice(0, 12)).map(function (r) {
      var code = r.iso_639_1 || ISO3_ALIAS[r.iso_639_3] || r.iso_639_3;
      var course = courses.filter(function (c) { return c.code === code; })[0];
      /* The course's own name when there is one: the inventory calls the same
         language "Mandarin" where the course is "Chinese", and a link that
         opens the Chinese course should say "Chinese". */
      var label = course ? course.name : r.language_name;
      return course
        ? '<a href="#/' + esc(code) + '"><b>' + esc(label) + "</b><small>" + esc(r.native_name || "") + " · course ready</small></a>"
        : '<span class="country-lang-nocourse"><b>' + esc(label) + "</b><small>" + esc(r.native_name || "") + " · documented, no course yet</small></span>";
    }).join("");
    var more = !available.length && langs.length > 12
      ? '<p class="source-note">Showing the first 12 of ' + langs.length + " documented languages.</p>" : "";
    story.innerHTML = '<div class="country-emblem" aria-hidden="true"><span>' + esc(country) + '</span><i></i><i></i><i></i></div><div class="country-narrative"><span class="pill">Country learning guide</span><h2>' + esc(countryName(country)) + '</h2><p>Explore this country through its documented language landscape. EkGuru connects one canonical language course to every relevant country context instead of duplicating the same course by border.</p><div class="country-facts"><span><b>' + langs.length + '</b> documented language relationships</span><span><b>' + available.length + '</b> courses available now</span><span><b>' + Object.keys(scripts).length + '</b> writing systems represented</span></div><div class="country-languages">' + chips + '</div>' + more + '<details><summary>Language context and evidence</summary><p>Relationship categories: ' + esc(Object.keys(categories).sort().join(", ") || "documented") + '. Speaker bands represented: ' + esc(Object.keys(bands).sort().join(", ") || "not stated") + '. Scripts: ' + esc(Object.keys(scripts).sort().join(", ") || "not stated") + '.</p><p class="source-note">Source: EkGuru canonical global language-country inventory. These are language-learning contexts, not claims that every resident has the same identity or language.</p></details></div>';
    story.hidden = false;
  }

  /* The country a typed query names, if any — "Japan", "japan", "JP". */
  function countryFromQuery(q) {
    if (!q) return "";
    for (var i = 0; i < countries.length; i++) {
      var c = countries[i];
      if (c.toLowerCase() === q || norm(countryName(c)) === q) return c;
    }
    return "";
  }

  function renderEmpty(q, country, shown) {
    if (!empty) return;
    if (shown) { empty.hidden = true; empty.innerHTML = ""; return; }
    var h = "";
    var rowsInCountry = country ? courses.filter(function (c) {
      return (countriesByCode[c.code] || []).indexOf(country) >= 0;
    }) : [];
    if (country && !rowsInCountry.length) {
      /* No course for this country at all (the future case: a country in the
         inventory whose language has not been authored yet). */
      var documentedRows = documented(country), sug0 = suggestionsFor(country, 3);
      h += "<h3>No course for " + esc(countryName(country)) + " yet</h3>";
      h += "<p>The inventory documents <b>" + documentedRows.length + "</b> language" +
        (documentedRows.length === 1 ? "" : "s") + " in " + esc(countryName(country)) +
        ", and none of them has a finished EkGuru course. Courses are written one language " +
        "at a time, by hand — more are coming.</p>";
      if (sug0.length) {
        h += '<p class="course-empty-h">Closest courses we do have</p><div class="course-suggest-row">' +
          sug0.map(function (x) { return courseLink(x.c, x.why); }).join("") + "</div>";
      }
      h += '<p class="source-note">Want a language added? <a href="' + self.base + 'contact/?topic=Course%20request">Ask for it</a> — requests decide what is built next.</p>';
    } else if (country) {
      /* The reachable case: a country has courses, but the query excluded all
         of them. Say which filter did it and offer the way back — an empty
         grid that keeps the reader staring at it is the bug report. */
      h += "<h3>Nothing in " + esc(countryName(country)) + " matches “" + esc(q) + "”</h3>";
      h += "<p>" + esc(countryName(country)) + " has <b>" + rowsInCountry.length + "</b> course" +
        (rowsInCountry.length === 1 ? "" : "s") + " on EkGuru. Clear the search box to see " +
        (rowsInCountry.length === 1 ? "it" : "them all") + ", or start with one of these.</p>";
      h += '<div class="course-suggest-row">' + rowsInCountry.slice(0, 4).map(function (c) {
        return courseLink(c, "");
      }).join("") + "</div>";
      h += '<p class="source-note"><button type="button" class="btn btn-sm" id="course-empty-clear">Clear the search</button></p>';
    } else {
      var hitCountries = countries.filter(function (c) {
        return courseCountries[c] && (norm(countryName(c)).indexOf(q) === 0 || c.toLowerCase().indexOf(q) === 0);
      }).slice(0, 6);
      var names = courses.map(function (c) { return c.name; }).filter(function (n) { return norm(n).indexOf(q) === 0; }).slice(0, 6);
      h += "<h3>Nothing matches “" + esc(q) + "”</h3>";
      h += "<p>Every course name, native name, code and country is searchable — try a country (Japan), a language (Italian) or a code (it).</p>";
      if (hitCountries.length) {
        h += '<p class="course-empty-h">Countries with courses</p><div class="course-suggest-row">' +
          hitCountries.map(function (c) { return '<a class="course-suggest" href="?country=' + esc(c) + '"><b>' + esc(countryName(c)) + "</b><small>" + countryCourseCount[c] + " language" + (countryCourseCount[c] === 1 ? "" : "s") + "</small></a>"; }).join("") + "</div>";
      }
      if (names.length) {
        h += '<p class="course-empty-h">Languages</p><div class="course-suggest-row">' +
          names.map(function (n) { var c = courses.filter(function (x) { return x.name === n; })[0]; return courseLink(c, ""); }).join("") + "</div>";
      }
    }
    empty.innerHTML = h;
    empty.hidden = false;
    var clear = doc_clear();
    if (clear) clear.addEventListener("click", function () { search.value = ""; applyFilters(); search.focus(); });
  }

  function doc_clear() {
    return empty.querySelector("#course-empty-clear");
  }

  function applyFilters() {
    var q = norm(search.value), country = filter.value, shown = 0;
    if (country) {
      var countryHue = Math.abs(country.charCodeAt(0) * 31 + country.charCodeAt(1)) % 360;
      document.documentElement.setAttribute("data-country", country);
      document.documentElement.style.setProperty("--country-visual", "hsl(" + countryHue + " 62% 45%)");
    }
    renderCountryStory(country);
    self.mount.querySelectorAll(".course-card").forEach(function (card) {
      var blob = card.getAttribute("data-search") || card.getAttribute("data-name") || "";
      var visible = (!q || blob.indexOf(q) >= 0) && (!country || (" " + card.getAttribute("data-countries") + " ").indexOf(" " + country + " ") >= 0);
      card.hidden = !visible; if (visible) shown++;
    });
    self.mount.querySelectorAll(".course-phase").forEach(function (phase) { phase.hidden = !phase.querySelector(".course-card:not([hidden])"); });
    renderEmpty(q, country, shown);
    /* The status line names what is filtering the grid — a country the
       reader picked, and a country their query named. */
    var named = q ? countryFromQuery(q) : "";
    var where = country ? countryName(country) : (named ? countryName(named) : "");
    count.textContent = shown + (shown === 1 ? " course" : " courses") +
      (where ? " · " + where : "");
  }
  /* ?country=JP opens the hub already filtered — the country page links here,
     and so does anything the reader bookmarks. Anything unknown is ignored
     rather than silently emptying the grid. */
  try {
    var pre = new URLSearchParams(location.search);
    var preCountry = (pre.get("country") || "").toUpperCase();
    if (preCountry && filter.querySelector('option[value="' + preCountry.replace(/"/g, "") + '"]')) {
      filter.value = preCountry;
    }
    var preQ = pre.get("q");
    if (preQ) search.value = preQ;
  } catch (e) {}

  search.addEventListener("input", applyFilters); filter.addEventListener("change", applyFilters); applyFilters();

  /* The filter belongs in the URL too: a filtered hub is worth linking to,
     and it means the country page's chips and the back button both work. */
  filter.addEventListener("change", function () {
    try {
      var params = new URLSearchParams(location.search);
      if (filter.value) params.set("country", filter.value); else params.delete("country");
      var qs = params.toString();
      history.replaceState(null, "", qs ? "?" + qs : location.pathname);
    } catch (e) {}
    applyFilters();
  });
  window.scrollTo(0, 0);
};
Player.prototype.langMeta = function (code) {
  var courses = (this.index && this.index.courses) || [];
  for (var i = 0; i < courses.length; i++) {
    if (courses[i].code === code) return courses[i];
  }
  return { code: code, name: code, native: "", levels: { A1: 1, A2: 1, B1: 1, B2: 1, C1: 1, C2: 1 } };
};
Player.prototype.renderLang = function (code) {
  var meta = this.langMeta(code);
  var levels = Object.keys(meta.levels || { A1: 1, A2: 1, B1: 1, B2: 1, C1: 1, C2: 1 });
  var p = loadProgress();
  var h = '<div class="egc google-anno-skip">' + this.crumbs([{ t: "Courses", href: "#/" }, { t: meta.name }]);
  h += "<h1>" + esc(meta.name) + " (" + esc(meta.code) + ")</h1>";
  h += "<p>Pick a level. A1 starts with the alphabet and counting.</p><div class='lvlrow'>";
  levels.forEach(function (lv) {
    var key = code + "_" + lv;
    var done = p[key] && p[key].done ? p[key].done.length : 0;
    var cls = done >= 6 ? "lvlab done" : "lvlab";
    h += '<a class="' + cls + '" href="#/' + esc(code) + "/" + lv + '">' + lv + " · " + LEVEL_NAMES[lv] + (done ? " (" + done + "/6)" : "") + "</a>";
  });
  h += "</div></div>";
  this.mount.innerHTML = h;
  window.scrollTo(0, 0);
};
Player.prototype.renderLevel = function (d, key) {
  var code = d.code, lv = d.file_level;
  var L = d.level || {};
  var h = '<div class="egc google-anno-skip">' + this.crumbs([{ t: "Courses", href: "#/" }, { t: d.name, href: "#/" + code }, { t: lv }]);
  h += "<h1>" + esc(d.name) + " " + esc(lv) + "</h1>";
  h += "<p>" + esc(L.title || "") + "</p>";
  if (L.goals && L.goals.length) {
    h += "<h2>Goals</h2><ul>" + L.goals.map(function (g) { return "<li>" + esc(g) + "</li>"; }).join("") + "</ul>";
  }
  if (d.pronunciation && d.pronunciation.length) {
    h += "<h2>Pronunciation first</h2>" + d.pronunciation.map(function (x) {
      return '<div class="ex"><b>' + esc(x.t) + '</b><div class="roman">' + esc(x.r || "") + "</div><div>" + esc(x.tip || "") + "</div></div>";
    }).join("");
  }
  if (d.alphabet) {
    var A = d.alphabet;
    h += "<h2>" + esc(A.title || "Alphabet") + "</h2><p>" + esc(A.explain || "") + "</p>";
    h += '<div class="alpha">' + (A.letters || []).map(function (x) {
      return '<div class="card"><b>' + esc(x.t) + '</b><div class="roman">' + esc(x.r || "") + "</div></div>";
    }).join("") + "</div>";
  }
  if (d.counting) {
    var C = d.counting;
    h += "<h2>" + esc(C.title || "Counting") + "</h2><p>" + esc(C.explain || "") + "</p>";
    h += '<div class="count">' + (C.numbers || []).map(function (x) {
      return '<div class="card"><b>' + esc(x.t) + '</b><div class="roman">' + esc(x.r || "") + '</div><div class="sub">' + esc(x.en == null ? "" : x.en) + "</div></div>";
    }).join("") + "</div>";
    if (C.rules) h += '<div class="rules"><b>Rules</b><ul>' + C.rules.map(function (r) { return "<li>" + esc(r) + "</li>"; }).join("") + "</ul></div>";
  }
  var p = loadProgress()[key] || { done: [] };
  (L.units || []).forEach(function (u) {
    h += "<h2>" + esc(u.id) + " · " + esc(u.title) + "</h2>";
    (u.lessons || []).forEach(function (ls) {
      var tick = p.done.indexOf(ls.id) >= 0 ? " ✓" : "";
      h += '<div class="card" style="margin:8px 0"><a href="#/' + esc(code) + "/" + esc(lv) + "/" + esc(ls.id) + '"><b>' + esc(ls.id) + " · " + esc(ls.title) + tick + "</b></a></div>";
    });
  });
  h += '<div class="navrow"><a class="btn" href="#/' + esc(code) + "/" + esc(lv) + '/test">Take the ' + esc(lv) + ' final test</a></div>';
  h += "</div>";
  this.mount.innerHTML = h;
  window.scrollTo(0, 0);
};
Player.prototype.findLesson = function (d, lessonId) {
  var units = (d.level && d.level.units) || [];
  for (var i = 0; i < units.length; i++) {
    var ls = units[i].lessons || [];
    for (var j = 0; j < ls.length; j++) {
      if (ls[j].id === lessonId) {
        var prev = j > 0 ? ls[j - 1].id : (i > 0 ? units[i - 1].lessons[units[i - 1].lessons.length - 1].id : null);
        var next = j < ls.length - 1 ? ls[j + 1].id : (i < units.length - 1 ? units[i + 1].lessons[0].id : null);
        return { lesson: ls[j], unit: units[i], prev: prev, next: next };
      }
    }
  }
  return null;
};
Player.prototype.renderLesson = function (d, key, lessonId) {
  var self = this;
  var f = self.findLesson(d, lessonId);
  if (!f) { self.mount.innerHTML = '<div class="egc google-anno-skip"><p>Lesson not found.</p></div>'; return; }
  var code = d.code, lv = d.file_level, ls = f.lesson;
  var h = '<div class="egc google-anno-skip">' + self.crumbs([{ t: "Courses", href: "#/" }, { t: d.name, href: "#/" + code }, { t: lv, href: "#/" + code + "/" + lv }, { t: ls.id }]);
  h += "<h1>" + esc(ls.id) + " · " + esc(ls.title) + "</h1>";
  h += "<h2>Learn</h2><p>" + esc(ls.learn || "") + "</p>";
  if (ls.vocab && ls.vocab.length) {
    h += "<h2>Vocabulary</h2><table class='vocab'><tr><th>Word</th><th>Say it</th><th>Meaning</th></tr>";
    ls.vocab.forEach(function (v) {
      h += "<tr><td><b>" + esc(v.t) + "</b> <span class='pos'>" + esc(v.pos || "") + "</span></td><td class='roman'>" + esc(v.r || "") + "</td><td>" + esc(v.en || "") + "</td></tr>";
    });
    h += "</table>";
  }
  if (ls.grammar) {
    var g = ls.grammar;
    h += "<h2>Grammar: " + esc(g.title || "") + "</h2><p>" + esc(g.explain || "") + "</p>";
    if (g.pattern) h += "<p><span class='pill'>" + esc(g.pattern) + "</span></p>";
    (g.examples || []).forEach(function (x) {
      h += '<div class="ex"><b>' + esc(x.t) + '</b><button class="sayn" data-say="' + esc(x.t) + '">🔊</button><div class="roman">' + esc(x.r || "") + "</div><div>" + esc(x.en || "") + "</div></div>";
    });
    (g.mistakes || []).forEach(function (m) { h += '<div class="mist">⚠️ ' + esc(m) + "</div>"; });
  }
  if (ls.dialogue && ls.dialogue.length) {
    h += "<h2>Dialogue</h2>";
    ls.dialogue.forEach(function (x) {
      h += '<div class="dlg"><span class="sp">' + esc(x.sp) + ":</span> <b>" + esc(x.t) + '</b><button class="sayn" data-say="' + esc(x.t) + '">🔊</button><div class="roman">' + esc(x.r || "") + '</div><div class="en">' + esc(x.en || "") + "</div></div>";
    });
  }
  h += "<h2>Practice</h2><div id='egc-prac'></div>";
  h += "<h2>Quiz</h2><div id='egc-quiz'></div>";
  h += "<h2>Flashcards</h2><div class='fc-grid' id='egc-fc'></div>";
  if (ls.worksheet) {
    var w = ls.worksheet;
    h += "<h2>Worksheet: " + esc(w.title || "") + "</h2>";
    (w.tasks || []).forEach(function (t, ti) {
      h += "<p><b>Task " + (ti + 1) + ".</b> " + esc(t.instruction || "") + "</p><ol>";
      (t.items || []).forEach(function (it) { h += "<li>" + esc(it) + "</li>"; });
      h += "</ol>";
    });
    h += '<div class="noprint"><button class="btn ghost" onclick="window.print()">🖨️ Print worksheet</button></div>';
    h += "<details><summary>Answer key</summary><ol>";
    (w.tasks || []).forEach(function (t) { (t.key || []).forEach(function (k) { h += "<li>" + esc(k) + "</li>"; }); });
    h += "</ol></details>";
  }
  var prevH = f.prev ? '<a class="btn ghost" href="#/' + code + "/" + lv + "/" + f.prev + '">← Previous</a>' : "";
  var nextH = f.next ? '<a class="btn" href="#/' + code + "/" + lv + "/" + f.next + '">Next →</a>' : '<a class="btn green" href="#/' + code + "/" + lv + '/test">Take the test →</a>';
  h += '<div class="navrow">' + prevH + '<button class="btn green" id="egc-done">✓ Mark complete</button>' + nextH + "</div>";
  h += "</div>";
  self.mount.innerHTML = h;
  window.scrollTo(0, 0);
  self.mount.querySelectorAll("[data-say]").forEach(function (b) {
    b.addEventListener("click", function () { speak(b.getAttribute("data-say"), code); });
  });
  self.buildPractice(self.mount.querySelector("#egc-prac"), ls.practice || [], code);
  self.buildQuiz(self.mount.querySelector("#egc-quiz"), ls.quiz || [], code, null);
  var fc = self.mount.querySelector("#egc-fc");
  var srsTerms = ls.srs_candidates || [];
  var flashVocab = (ls.vocab || []).filter(function (v) { return !srsTerms.length || srsTerms.indexOf(v.t) >= 0; });
  flashVocab.forEach(function (v) {
    var c = el('<div class="fc"><div class="front">' + esc(v.t) + '</div><div class="back"><b>' + esc(v.en || "") + '</b><div class="roman">' + esc(v.r || "") + "</div></div></div>");
    c.addEventListener("click", function () { c.classList.toggle("flip"); });
    fc.appendChild(c);
  });
  self.mount.querySelector("#egc-done").addEventListener("click", function () {
    markDone(key, ls.id);
    this.textContent = "✓ Completed!";
    this.disabled = true;
  });
};
Player.prototype.checkText = function (input, answer) {
  return norm(input) === norm(answer);
};
Player.prototype.buildPractice = function (box, items, code) {
  var self = this;
  items.forEach(function (it, idx) {
    var prior = practiceHistory()[practiceId(code, it)];
    var historyNote = prior ? '<div class="why">Saved history: ' + prior.correct + '/' + prior.attempts + ' correct · attempts do not reset on reload</div>' : '';
    var wrap = el('<div class="q"><span class="pill">' + esc(practiceLabel(it.type)) + '</span><br><b>' + (idx + 1) + ".</b> " + esc(it.q || "") + historyNote + '<div class="body"></div><div class="fb"></div></div>');
    var body = wrap.querySelector(".body"), fb = wrap.querySelector(".fb"), recorded = false;
    function saveResult(good) { if (!recorded) { recordPractice(code, it, good); recorded = true; } }
    function ok(msg) { saveResult(true); fb.className = "fb ok"; fb.textContent = "✓ " + (msg || "Correct!"); }
    function no(msg) { saveResult(false); fb.className = "fb no"; fb.textContent = "✗ " + (msg || ("Answer: " + it.answer)); }
    if (hasType(PRACTICE_AUDIO, it.type)) {
      var audioBtn = el('<button class="btn ghost">🔊 Play synthetic ' + esc(TTS_LANG[code] || "voice") + ' audio</button>');
      audioBtn.addEventListener("click", function () { if (!speak(it.audio_source || it.answer, code)) { fb.className = "fb no"; fb.textContent = "Synthetic audio is unavailable on this device."; } });
      body.appendChild(audioBtn);
    }
    if (hasType(PRACTICE_CHOICE, it.type)) {
      var ol = el('<div class="opts"></div>');
      (it.options || []).forEach(function (o) {
        var b = el('<button class="opt">' + esc(o) + "</button>");
        b.addEventListener("click", function () {
          var good = norm(o) === norm(it.answer);
          ol.querySelectorAll(".opt").forEach(function (x) { x.disabled = true; if (norm(x.textContent) === norm(it.answer)) x.classList.add("right"); });
          if (good) { ok(); } else { b.classList.add("wrong"); no(); }
        });
        ol.appendChild(b);
      });
      body.appendChild(ol);
    } else if (hasType(PRACTICE_REORDER, it.type)) {
      var words = String(it.answer || "").split(/\s+/).filter(Boolean);
      var pool = words.slice();
      for (var i = pool.length - 1; i > 0; i--) { var k = Math.floor(Math.random() * (i + 1)); var t = pool[i]; pool[i] = pool[k]; pool[k] = t; }
      var built = [], builtBox = el('<div class="ro-built"></div>'), poolBox = el('<div class="ro-words"></div>');
      function draw() { builtBox.textContent = built.join(" ") || "— tap words —"; }
      draw();
      pool.forEach(function (w) {
        var c = el('<span class="ro-w">' + esc(w) + "</span>");
        c.addEventListener("click", function () { built.push(w); c.style.display = "none"; draw(); });
        poolBox.appendChild(c);
      });
      var chk = el('<button class="btn">Check</button>'), clr = el('<button class="btn ghost">Clear</button>');
      chk.addEventListener("click", function () {
        if (norm(built.join(" ")) === norm(it.answer)) ok(); else no();
      });
      clr.addEventListener("click", function () { built = []; poolBox.querySelectorAll(".ro-w").forEach(function (x) { x.style.display = ""; }); draw(); fb.textContent = ""; });
      body.appendChild(builtBox); body.appendChild(poolBox); body.appendChild(chk); body.appendChild(clr);
    } else if (hasType(PRACTICE_SPEAK, it.type)) {
      var sb = el('<button class="btn">🔊 Listen</button>'), mb = el('<button class="btn green">I said it ✓</button>');
      sb.addEventListener("click", function () { if (!speak(it.answer, code)) { fb.className = "fb no"; fb.textContent = "Audio not available — read aloud!"; } });
      mb.addEventListener("click", function () { ok("Self-check recorded. No microphone evaluation was performed."); });
      body.appendChild(sb); body.appendChild(mb);
    } else {
      var inp = document.createElement("input");
      inp.type = "text"; inp.placeholder = "Type your answer…"; inp.setAttribute("aria-label", it.q || "answer");
      var go = el('<button class="btn">Check</button>');
      go.addEventListener("click", function () {
        if (self.checkText(inp.value, it.answer)) ok(); else no();
      });
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") go.click(); });
      body.appendChild(inp); body.appendChild(go);
    }
    box.appendChild(wrap);
  });
};
Player.prototype.buildQuiz = function (box, items, code, onDone) {
  var self = this;
  var score = 0, answered = 0;
  var total = items.length;
  var scoreBox = el('<div class="score">Score: 0 / ' + total + "</div>");
  box.appendChild(scoreBox);
  items.forEach(function (it, idx) {
    var wrap = el('<div class="q"><b>Q' + (idx + 1) + ".</b> " + esc(it.q || "") + '<div class="opts"></div><div class="fb"></div><div class="why"></div></div>');
    var ol = wrap.querySelector(".opts");
    (it.options || []).forEach(function (o, oi) {
      var b = el('<button class="opt">' + esc(o) + "</button>");
      b.addEventListener("click", function () {
        if (b.disabled) return;
        ol.querySelectorAll(".opt").forEach(function (x, xi) {
          x.disabled = true;
          if (xi === it.answer) x.classList.add("right");
        });
        answered++;
        if (oi === it.answer) { score++; wrap.querySelector(".fb").className = "fb ok"; wrap.querySelector(".fb").textContent = "✓ Correct!"; }
        else { b.classList.add("wrong"); wrap.querySelector(".fb").className = "fb no"; wrap.querySelector(".fb").textContent = "✗ Correct: " + it.options[it.answer]; }
        wrap.querySelector(".why").textContent = it.why || "";
        scoreBox.textContent = "Score: " + score + " / " + total;
        if (onDone) onDone(score, answered, total);
      });
      ol.appendChild(b);
    });
    box.appendChild(wrap);
  });
};
Player.prototype.renderTest = function (d, key) {
  var self = this;
  var code = d.code, lv = d.file_level;
  var T = d.test || { items: [] };
  var items = T.items || [];
  var h = '<div class="egc google-anno-skip">' + self.crumbs([{ t: "Courses", href: "#/" }, { t: d.name, href: "#/" + code }, { t: lv, href: "#/" + code + "/" + lv }, { t: "Test" }]);
  h += "<h1>" + esc(T.title || (lv + " final test")) + "</h1><p>Answer all " + items.length + " questions. Pass mark: 7 / " + items.length + ".</p>";
  h += "<div id='egc-test'></div>";
  h += '<div class="navrow"><a class="btn ghost" href="#/' + code + "/" + lv + '">← Back to ' + esc(lv) + "</a></div></div>";
  self.mount.innerHTML = h;
  window.scrollTo(0, 0);
  var box = self.mount.querySelector("#egc-test");
  var score = 0, answered = 0;
  var scoreBox = el('<div class="score">Score: 0 / ' + items.length + "</div>");
  box.appendChild(scoreBox);
  items.forEach(function (it, idx) {
    var wrap = el('<div class="q"><b>Q' + (idx + 1) + ".</b> " + esc(it.q || "") + '<div class="body"></div><div class="fb"></div></div>');
    var body = wrap.querySelector(".body"), fb = wrap.querySelector(".fb");
    var graded = false;
    function grade(good) {
      if (graded) return; graded = true; answered++;
      if (good) { score++; fb.className = "fb ok"; fb.textContent = "✓ Correct!"; }
      else { fb.className = "fb no"; fb.textContent = "✗ Answer: " + it.answer; }
      scoreBox.textContent = "Score: " + score + " / " + items.length;
      if (answered >= items.length) {
        markTest(key, score);
        var pass = score >= 7;
        scoreBox.textContent = (pass ? "🎉 PASSED! " : "📚 Keep practising! ") + "Final score: " + score + " / " + items.length;
      }
    }
    if (it.type === "choose") {
      (it.options || []).forEach(function (o) {
        var b = el('<button class="opt">' + esc(o) + "</button>");
        b.addEventListener("click", function () {
          body.querySelectorAll(".opt").forEach(function (x) { x.disabled = true; if (norm(x.textContent) === norm(it.answer)) x.classList.add("right"); });
          var good = norm(o) === norm(it.answer);
          if (!good) b.classList.add("wrong");
          grade(good);
        });
        body.appendChild(b);
      });
    } else if (it.type === "reorder") {
      var words = String(it.answer || "").split(/\s+/).filter(Boolean);
      var pool = words.slice();
      for (var i = pool.length - 1; i > 0; i--) { var k = Math.floor(Math.random() * (i + 1)); var t = pool[i]; pool[i] = pool[k]; pool[k] = t; }
      var built = [], builtBox = el('<div class="ro-built"></div>'), poolBox = el('<div class="ro-words"></div>');
      builtBox.textContent = "— tap words —";
      pool.forEach(function (w) {
        var c = el('<span class="ro-w">' + esc(w) + "</span>");
        c.addEventListener("click", function () { if (!graded) { built.push(w); c.style.display = "none"; builtBox.textContent = built.join(" "); } });
        poolBox.appendChild(c);
      });
      var chk = el('<button class="btn">Check</button>');
      chk.addEventListener("click", function () { grade(norm(built.join(" ")) === norm(it.answer)); });
      body.appendChild(builtBox); body.appendChild(poolBox); body.appendChild(chk);
    } else if (it.type === "speak") {
      var sb = el('<button class="btn">🔊 Listen</button>'), mb = el('<button class="btn green">I said it ✓</button>');
      sb.addEventListener("click", function () { speak(it.answer, code); });
      mb.addEventListener("click", function () { grade(true); });
      body.appendChild(sb); body.appendChild(mb);
    } else {
      var inp = document.createElement("input");
      inp.type = "text"; inp.placeholder = "Type your answer…";
      var go = el('<button class="btn">Check</button>');
      go.addEventListener("click", function () { grade(self.checkText(inp.value, it.answer)); });
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") go.click(); });
      body.appendChild(inp); body.appendChild(go);
    }
    box.appendChild(wrap);
  });
};

function initFromDOM() {
  ensureCSS();
  document.querySelectorAll("[data-course-player]").forEach(function (m) {
    var p = new Player(m, { base: m.getAttribute("data-base") || "./" });
    p.route();
  });
}
window.EKGURU_COURSE_PLAYER = { Player: Player, init: initFromDOM };
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initFromDOM);
else initFromDOM();

})();
