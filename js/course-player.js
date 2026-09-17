/* EkGuru — PHASE COURSE PLAYER (generic, data-driven).
   NEW file: renders data/courses/phase-1/<code>_<level>.json + data/courses/index.json.
   No dependencies. Progress in localStorage. TTS via speechSynthesis. */
(function () {
"use strict";

var TTS_LANG = { en: "en-GB", fil: "fil-PH", pl: "pl-PL", ro: "ro-RO", tr: "tr-TR", uk: "uk-UA", uzn: "uz-UZ", vi: "vi-VN", kk: "kk-KZ", npi: "ne-NP", zsm: "ms-MY", sw: "sw-KE", nl: "nl-NL", es: "es-ES", fr: "fr-FR", de: "de-DE", it: "it-IT", pt: "pt-BR", ru: "ru-RU", ar: "ar-SA", ja: "ja-JP", ko: "ko-KR", zh: "zh-CN", hi: "hi-IN", bn: "bn-IN", pa: "pa-IN", ur: "ur-PK", ta: "ta-IN", te: "te-IN", mr: "mr-IN", gu: "gu-IN", kn: "kn-IN", ml: "ml-IN" };
var LEVEL_NAMES = { A1: "Beginner", A2: "Elementary", B1: "Intermediate", B2: "Advanced", C1: "Proficient", C2: "Mastery" };
var LS_KEY = "eg-course-progress-v1";
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

var CSS = [
".egc{font-family:system-ui,-apple-system,'Segoe UI',Roboto,'Noto Sans',sans-serif;line-height:1.6;color:#1c2430;max-width:860px;margin:0 auto;padding:12px}",
".egc h1{font-size:1.6rem}.egc h2{font-size:1.25rem;margin-top:1.6em;border-bottom:2px solid #e5eaf1;padding-bottom:.3em}.egc h3{font-size:1.05rem;margin-top:1.2em}",
".egc .crumbs{font-size:.85rem;color:#5b6b7f;margin-bottom:.6em}.egc .crumbs a{color:#0b6bcb;text-decoration:none}",
".egc .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}",
".egc .card{border:1px solid #dbe3ee;border-radius:12px;padding:12px;background:#fff;box-shadow:0 1px 2px rgba(20,40,80,.06)}",
".egc .card a{color:inherit;text-decoration:none;display:block}.egc .card b{font-size:1.05rem}.egc .card .sub{font-size:.82rem;color:#5b6b7f}",
".egc .lvlrow{display:flex;gap:8px;margin:10px 0;flex-wrap:wrap}.egc .lvlab{border:1px solid #0b6bcb;color:#0b6bcb;border-radius:999px;padding:4px 12px;text-decoration:none;font-weight:600;font-size:.9rem}",
".egc .lvlab.done{background:#e7f6ec;border-color:#1d9e57;color:#14713d}",
".egc .pill{display:inline-block;background:#eef4fb;color:#0b4a8f;border-radius:999px;padding:2px 10px;font-size:.8rem;margin:2px 4px 2px 0}",
".egc table.vocab{border-collapse:collapse;width:100%;font-size:.95rem}.egc table.vocab th,.egc table.vocab td{border:1px solid #e1e7f0;padding:6px 8px;text-align:left}",
".egc table.vocab th{background:#f2f6fb}.egc .roman{color:#6a5aa8;font-style:italic}.egc .pos{font-size:.75rem;color:#7b8aa0}",
".egc .dlg{border-left:4px solid #0b6bcb;background:#f6f9fe;border-radius:0 10px 10px 0;padding:8px 12px;margin:8px 0}",
".egc .dlg .sp{font-weight:700;color:#0b4a8f}.egc .dlg .en{color:#4c5b70;font-size:.92rem}",
".egc button.sayn{margin-left:8px;font-size:.8rem;border:1px solid #c7d5ea;background:#fff;border-radius:999px;padding:2px 10px;cursor:pointer}",
".egc .ex{background:#fffbe8;border:1px solid #f0dfa0;border-radius:10px;padding:8px 12px;margin:8px 0}",
".egc .mist{background:#fef1f1;border:1px solid #f3c2c2;border-radius:10px;padding:8px 12px;margin:8px 0}",
".egc .q{border:1px solid #dbe3ee;border-radius:12px;padding:12px;margin:10px 0;background:#fff}",
".egc .q input[type=text]{width:100%;box-sizing:border-box;font-size:1rem;padding:8px;border:1px solid #c3cede;border-radius:8px;margin:6px 0}",
".egc .q .opts{display:flex;flex-direction:column;gap:6px;margin:6px 0}.egc .q .opt{border:1px solid #c3cede;border-radius:8px;padding:8px 10px;background:#fbfdff;cursor:pointer;text-align:left;font-size:.95rem}",
".egc .q .opt:hover{border-color:#0b6bcb}.egc .q .opt.right{border-color:#1d9e57;background:#e7f6ec}.egc .q .opt.wrong{border-color:#d64545;background:#fdeeee}",
".egc .btn{display:inline-block;border:0;border-radius:10px;background:#0b6bcb;color:#fff;font-weight:700;padding:10px 18px;font-size:.95rem;cursor:pointer;margin:6px 6px 6px 0}",
".egc .btn.ghost{background:#eef2f7;color:#1c2430}.egc .btn.green{background:#1d9e57}",
".egc .fb{font-weight:700;margin-top:6px}.egc .fb.ok{color:#14713d}.egc .fb.no{color:#b42323}.egc .why{font-size:.88rem;color:#4c5b70}",
".egc .ro-words{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.egc .ro-w{border:1px solid #0b6bcb;border-radius:8px;padding:6px 10px;cursor:pointer;background:#f4f8ff}",
".egc .ro-built{min-height:44px;border:1px dashed #9fb4d0;border-radius:8px;padding:6px;background:#fbfdff;margin:6px 0}",
".egc .fc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}",
".egc .fc{border:1px solid #dbe3ee;border-radius:12px;padding:14px;min-height:86px;cursor:pointer;background:linear-gradient(180deg,#fff,#f4f7fc);text-align:center}",
".egc .fc .front{font-weight:700;font-size:1.05rem}.egc .fc .back{display:none}.egc .fc.flip .front{display:none}.egc .fc.flip .back{display:block}",
".egc .score{font-size:1.2rem;font-weight:800;background:#eef4fb;border-radius:12px;padding:12px;text-align:center}",
".egc .navrow{display:flex;justify-content:space-between;margin:18px 0;gap:8px;flex-wrap:wrap}",
".egc .alpha{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px}.egc .alpha .card{text-align:center}",
".egc .count{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}.egc .rules{background:#f2f6fb;border-radius:10px;padding:10px 14px;margin-top:10px}",
"@media print{.egc .noprint{display:none!important}.egc{max-width:none}}"
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
  self.fetchJSON(self.base + "data/courses/index.json").then(function (idx) {
    self.index = idx;
    if (!r.lang) return self.renderHub();
    if (!r.level) return self.renderLang(r.lang);
    var key = r.lang + "_" + r.level;
    var entry = self.langMeta(r.lang);
    var phase = entry.phase || "phase-1";
    var file = key + ".json";
    (entry.files || []).forEach(function (f) { if (f.indexOf(key) === 0) file = f; });
    return self.fetchJSON(self.base + "data/courses/" + phase + "/" + file).then(function (d) {
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
  var courses = (this.index && this.index.courses) || [];
  var h = '<div class="egc google-anno-skip"><h1>EkGuru Phase Courses</h1>';
  h += '<p>Complete beginner-to-advanced courses: alphabet, counting, 24 deep lessons and level tests — all free, in your browser.</p>';
  var phases = {};
  courses.forEach(function (c) { var ph = c.phase || "phase-1"; (phases[ph] = phases[ph] || []).push(c); });
  Object.keys(phases).sort().forEach(function (ph) {
    h += "<h2>Phase " + esc(String(ph).replace("phase-", "")) + "</h2><div class='grid'>";
    phases[ph].forEach(function (c) {
      var lvs = Object.keys(c.levels || {});
      var tick = c.complete ? " ✓ complete" : "";
      h += '<div class="card"><a href="#/' + esc(c.code) + '"><b>' + esc(c.name) + tick + '</b><div class="sub">' + esc(lvs.join(" · ")) + "</div></a></div>";
    });
    h += "</div>";
  });
  if (!courses.length) h += "<p>No courses found in index.</p>";
  h += "</div>";
  this.mount.innerHTML = h;
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
    var wrap = el('<div class="q"><span class="pill">' + esc(practiceLabel(it.type)) + '</span><br><b>' + (idx + 1) + ".</b> " + esc(it.q || "") + '<div class="body"></div><div class="fb"></div></div>');
    var body = wrap.querySelector(".body"), fb = wrap.querySelector(".fb");
    function ok(msg) { fb.className = "fb ok"; fb.textContent = "✓ " + (msg || "Correct!"); }
    function no(msg) { fb.className = "fb no"; fb.textContent = "✗ " + (msg || ("Answer: " + it.answer)); }
    if (hasType(PRACTICE_AUDIO, it.type)) {
      var audioBtn = el('<button class="btn ghost">🔊 Play synthetic ' + esc(TTS_LANG[code] || "voice") + ' audio</button>');
      audioBtn.addEventListener("click", function () { if (!speak(it.audio_source || it.answer, code)) no("Synthetic audio is unavailable on this device."); });
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
      sb.addEventListener("click", function () { if (!speak(it.answer, code)) no("Audio not available — read aloud!"); });
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
