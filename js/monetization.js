/* EkGuru monetization safety layer.
 * Account-side AdSense settings still control whether formats run. This file
 * classifies pages and protects learning/UI text from Ad intents; it never
 * claims approval or enables an account product. */
(function () {
  "use strict";
  var path = location.pathname.replace(/^\/+/, "/");
  var excluded = [
    "/admin", "/privacy/", "/terms/", "/disclaimer/", "/contact/",
    "/search/", "/404", "/tutor.html", "/join", "/booking/",
    "/checkout/", "/payment/", "/courses/"
  ];
  var pageClass = "MEDIUM_CONTENT";
  if (excluded.some(function (prefix) { return path.indexOf(prefix) === 0; })) {
    pageClass = path.indexOf("/courses/") === 0 ? "INTERACTIVE_LEARNING" : "UTILITY";
  } else if (document.querySelector("article, main article, [itemtype*='Article']")) {
    pageClass = "HIGH_CONTENT";
  }
  document.documentElement.dataset.monetizationClass = pageClass;

  // Google documents google-anno-skip as the opt-out for all Ad-intent
  // treatment. Keep it on UI containers even on otherwise eligible pages.
  var selectors = [
    "header", "nav", "footer", "form", "button", "audio", "video",
    "[role='navigation']", "[role='dialog']", "[role='button']",
    "[aria-live]", ".course-player", ".egc", ".quiz", ".assessment",
    ".answer", ".accessibility-controls", ".audio-controls"
  ];
  document.querySelectorAll(selectors.join(",")).forEach(function (node) {
    node.classList.add("google-anno-skip");
  });
  if (pageClass !== "HIGH_CONTENT" && pageClass !== "MEDIUM_CONTENT") {
    document.body.classList.add("google-anno-skip");
  }
})();
