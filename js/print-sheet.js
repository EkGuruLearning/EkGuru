/* EkGuru — print the sheet, not the website.
 *
 * Prakash, twice: "print worksheet pura page hi print karti hai, par humein
 * sirf worksheet hi print karni hai."
 *
 * css/experience.css §27 already hides the chrome on paper, and a page marked
 * data-print="sheet" only prints its marked element. This script exists for
 * the two cases a stylesheet cannot cover by itself:
 *
 *   1. The element is generated in the browser (a worksheet is built from the
 *      quiz bank when a reader clicks "Make worksheet"), so there is no
 *      element in the file for the CSS to mark. On beforeprint this clones
 *      the finished sheet into #ekguru-print-root and prints that one element
 *      — the header, the intro, the controls, the notes and the footer are
 *      not in the copy that goes to the printer.
 *
 *   2. Paper is the one place the watermark and the tagline must never be
 *      missing, and a browser that fires no beforeprint (older Safari) would
 *      otherwise print the page as it looks. The worksheet's own Print button
 *      calls EKGURU_PRINT_SHEET.build() itself, so the button always prints
 *      the sheet.
 *
 * The clone carries data-watermark="EkGuru" — the diagonal mark the print
 * layer draws — and a printer's line under it with the page's own address,
 * the year, the LIVE settings-sheet tagline, the print date and ekguru.shop.
 */
(function () {
  "use strict";

  var ROOT_ID = "ekguru-print-root";
  var CLASS = "eg-printing";
  var BRAND = "EkGuru";
  var YEAR = String(new Date().getFullYear());

  function liveTagline() {
    var sheet = window.EKGURU_SHEET_SETTINGS || {};
    if (sheet.tagline) return sheet.tagline;
    var el = document.querySelector("[data-tagline]");
    return el && el.textContent ? el.textContent.trim() : "";
  }

  /* The sheet, in the order of what a reader would call the worksheet. A
     worksheet that has not been built yet is built first — that is exactly
     what the Print button does — and only then does the marked print target
     (a printable guide) become the paper. */
  function sheetElement() {
    var built = document.querySelector("#w-sheet .ws-page") ||
      document.querySelector(".ws-page");
    if (built && built.textContent.trim()) return built;

    var make = document.getElementById("w-make");
    if (make) {
      try { make.click(); } catch (e) { /* nothing to build */ }
      built = document.querySelector("#w-sheet .ws-page") ||
        document.querySelector(".ws-page");
      if (built && built.textContent.trim()) return built;
    }

    var target = document.querySelector("[data-print-target]");
    if (target && target.textContent.trim()) return target;
    var marked = document.querySelector(".worksheet, .print-area, .flashcards, .quiz-sheet");
    return marked && marked.textContent.trim() ? marked : null;
  }

  function stampLine() {
    var path = location.pathname.replace(/index\.html$/, "");
    var tagline = liveTagline();
    return path + "  ·  © " + YEAR + " " + BRAND + (tagline ? "  ·  " + tagline : "") +
      "  ·  printed " + new Date().toISOString().slice(0, 10) + "  ·  ekguru.shop";
  }

  function build() {
    if (document.getElementById(ROOT_ID)) return true;
    var el = sheetElement();
    if (!el) return false;

    var root = document.createElement("div");
    root.id = ROOT_ID;
    root.setAttribute("data-watermark", BRAND);

    var clone = el.cloneNode(true);
    clone.removeAttribute("data-print-target");
    /* Anything the sheet itself says is a control does not go on paper. */
    var kills = clone.querySelectorAll(".no-print, .sb-hint, .hi-listen, button, script");
    for (var i = 0; i < kills.length; i++) {
      if (kills[i].parentNode) kills[i].parentNode.removeChild(kills[i]);
    }
    root.appendChild(clone);

    var line = document.createElement("p");
    line.className = "print-stamp";
    line.textContent = stampLine();
    root.appendChild(line);

    document.body.appendChild(root);
    document.documentElement.classList.add(CLASS);
    return true;
  }

  function clear() {
    var root = document.getElementById(ROOT_ID);
    if (root && root.parentNode) root.parentNode.removeChild(root);
    document.documentElement.classList.remove(CLASS);
  }

  window.addEventListener("beforeprint", build);
  window.addEventListener("afterprint", clear);
  /* Safari fires onafterprint only; Chrome and Firefox both. */
  if (window.matchMedia) {
    var mq = window.matchMedia("print");
    var handler = function (m) { if (m.matches) build(); else clear(); };
    if (mq.addEventListener) mq.addEventListener("change", handler);
    else if (mq.addListener) mq.addListener(handler);
  }

  window.EKGURU_PRINT_SHEET = {
    build: build,
    clear: clear,
    /* Called by the worksheet's own Print button: build, print, then put the
       page back the way it was so the reader can keep using it. */
    now: function () {
      var had = build();
      window.print();
      if (had) window.setTimeout(clear, 0);
    }
  };
})();
