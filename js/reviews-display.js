/* =========================================================
   EkGuru — REVIEW DISPLAY FOR STATIC TUTOR PROFILE PAGES
   ---------------------------------------------------------
   Renders approved reviews (status=live from the sheet) on
   static tutor profile pages. Reviews are loaded by
   js/reviews.js which applies them to the tutor data and
   dispatches "ekguru:reviews" event.

   Only reviews with status=live from the sheet are shown.
   Pending reviews (reviews_pending tab) are NEVER displayed
   — they must be approved by the owner first.
   ========================================================= */
(function (root) {
  "use strict";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function stars(n) {
    var s = "";
    for (var i = 0; i < 5; i++) {
      s += i < n ? "★" : "☆";
    }
    return s;
  }

  function renderReviews(tutorId) {
    var host = root.document.querySelector('[data-eg-reviews][data-tutor="' + tutorId + '"]');
    if (!host) return;

    var tutor = (root.EKGURU_TUTOR_FILES || {})[tutorId];
    if (!tutor || !tutor.reviews || !tutor.reviews.length) {
      host.innerHTML = '<p class="muted">No reviews yet — be the first to share your experience after a lesson.</p>';
      return;
    }

    host.innerHTML = tutor.reviews.map(function (r) {
      return '<article class="rev">' +
        '<div class="rev-h"><div class="rev-av">' + esc(String(r.name || "?").charAt(0)) + "</div>" +
        "<div><b>" + esc(r.name) + '</b><span class="stars">' + stars(r.stars) +
        "</span> <span>· " + esc(r.date) + "</span></div></div>" +
        '<p class="rev-text">' + esc(r.text) + "</p></article>";
    }).join("");
  }

  function init() {
    /* Render after reviews.js has applied data */
    root.addEventListener("ekguru:reviews", function () {
      var hosts = root.document.querySelectorAll("[data-eg-reviews]");
      Array.prototype.forEach.call(hosts, function (h) {
        renderReviews(h.getAttribute("data-tutor"));
      });
    });

    /* Also render immediately if reviews.js already loaded */
    var hosts = root.document.querySelectorAll("[data-eg-reviews]");
    Array.prototype.forEach.call(hosts, function (h) {
      renderReviews(h.getAttribute("data-tutor"));
    });
  }

  if (root.document.readyState === "loading") {
    root.document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(typeof window !== "undefined" ? window : globalThis);
