/* =========================================================
   EkGuru — PATH PROGRESS TRACKER  (v100)
   ---------------------------------------------------------
   Renders a learning path's module/lesson list from
   js/learning-paths.js into #path-modules and tracks lesson
   completion in this browser only (localStorage). No account,
   no upload.

   The lesson list itself is DATA (single source of truth):
   a path page never lists its own lessons by hand, so the page
   and the admin gap engine can never drift apart.
   ========================================================= */
(function () {
  "use strict";
  var KEY = "ekguru_path_progress_v1";

  function slug() {
    var el = document.querySelector("[data-path]");
    return el ? el.getAttribute("data-path") : null;
  }
  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; }
  }
  function done() {
    var s = slug(), m = read();
    return m[s] || {};
  }
  function mark(url, on) {
    var s = slug(), m = read();
    var set = m[s] || {};
    if (on) set[url] = 1; else delete set[url];
    m[s] = set;
    try { localStorage.setItem(KEY, JSON.stringify(m)); } catch (e) {}
    paint();
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  var KIND_LABEL = { guide: "Read", tool: "Tool", practice: "Practise", daily: "Daily", quiz: "Quiz" };

  function paint() {
    var host = document.getElementById("path-modules");
    var paths = window.EKGURU_PATHS || [];
    var path = null;
    paths.forEach(function (p) { if (p.slug === slug()) path = p; });
    if (!host || !path) return;

    // Hide the static, no-JS outline now that the interactive tracker
    // is about to render — so JS users never see the lesson list twice.
    var outline = document.getElementById("path-outline");
    if (outline) outline.hidden = true;

    var set = done();
    var lessons = [];
    path.modules.forEach(function (m) {
      m.lessons.forEach(function (l) { lessons.push(l); });
    });
    var doneN = lessons.filter(function (l) { return set[l.url]; }).length;
    var pct = lessons.length ? Math.round(doneN / lessons.length * 100) : 0;

    var html =
      '<div class="pp-bar" role="progressbar" aria-valuenow="' + pct + '" aria-valuemin="0" aria-valuemax="100">' +
        '<span style="width:' + pct + '%"></span>' +
      "</div>" +
      '<p class="pp-count">' + doneN + " of " + lessons.length + " lessons done · " + pct + "%</p>";

    path.modules.forEach(function (m) {
      html += '<section class="pp-mod">' +
        "<h2>" + esc(m.title) + "</h2><ul class=\"pp-list\">" +
        m.lessons.map(function (l) {
          var isDone = !!set[l.url];
          return '<li class="' + (isDone ? "is-done" : "") + '">' +
            '<label class="pp-row">' +
              '<input type="checkbox" ' + (isDone ? "checked" : "") +
                ' data-url="' + esc(l.url) + '" aria-label="Mark done: ' + esc(l.title) + '">' +
              '<span class="pp-kind">' + (KIND_LABEL[l.kind] || l.kind) + "</span>" +
              '<span class="pp-txt"><a href="' + esc(l.url) + '">' + esc(l.title) + "</a>" +
                (l.minutes ? '<small>' + l.minutes + " min</small>" : "") + "</span>" +
            "</label></li>";
        }).join("") +
        "</ul></section>";
    });

    html += '<section class="pp-extra">' +
      "<h2>Practice and check</h2>" +
      '<ul class="pp-list">' +
        path.practice.map(function (p) {
          return '<li><a class="pp-row pp-link" href="' + esc(p.url) + '">' +
            '<span class="pp-kind">' + (KIND_LABEL[p.kind] || "Do") + "</span>" +
            "<span class=\"pp-txt\">" + esc(p.title) + "</span></a></li>";
        }).join("") +
        '<li><a class="pp-row pp-link" href="' + esc(path.quiz.url) + '">' +
          '<span class="pp-kind">Quiz</span><span class="pp-txt">' + esc(path.quiz.title) +
          '<small>' + esc(path.quiz.note) + "</small></span></a></li>" +
        '<li><a class="pp-row pp-link" href="' + esc(path.review.url) + '">' +
          '<span class="pp-kind">Review</span><span class="pp-txt">' + esc(path.review.title) +
          "<small>Goes over what is getting wobbly</small></span></a></li>" +
      "</ul>" +
      '<div class="pp-actions">' +
        '<button type="button" class="btn btn-ghost pp-reset">Reset progress</button>' +
      "</div></section>";

    if (pct === 100) {
      var next = paths.filter(function (p) { return p.slug === path.next; })[0];
      html += '<div class="pp-done" role="status">' +
        '<div class="pp-done-ic">✓</div><h2>Path complete</h2>' +
        "<p>" + esc(path.completion) + "</p>" +
        (next
          ? '<a class="btn btn-primary" href="../' + esc(next.slug) + '/">Next: ' + esc(next.title) + " →</a>"
          : "") +
      "</div>";
    }

    host.innerHTML = html;

    host.querySelectorAll("input[type=checkbox]").forEach(function (cb) {
      cb.addEventListener("change", function () {
        mark(cb.getAttribute("data-url"), cb.checked);
      });
    });
    var reset = host.querySelector(".pp-reset");
    if (reset) reset.addEventListener("click", function () {
      var s = slug(), m = read();
      delete m[s];
      try { localStorage.setItem(KEY, JSON.stringify(m)); } catch (e) {}
      paint();
    });
  }

  function boot() {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", paint);
    } else paint();
  }
  boot();
})();
