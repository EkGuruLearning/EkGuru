/* =========================================================
   EkGuru — Print ONLY the worksheet v301 (honest)
   ---------------------------------------------------------
   "print worksheet pura page hi print karti hai, par humein sirf
   worksheet hi print karni hai."

   What a "Print Worksheet" action prints — and nothing else:
     1. a worksheet already on the page (#w-sheet .ws-page)
     2. otherwise: click the builder's "Make worksheet" and use that
     3. otherwise: the page's explicit [data-print-target] (worksheet
        builders and the printable /materials/ guides, marked by
        tools/build-print-sheets.py)

   Honest abort: if none of those exists on the page, nothing is
   printed and the visitor is told so. This script never falls back
   to <main>, <article> or the page body — a button that says
   "Print Worksheet" must not print a lesson.

   The learner's sheet never carries the answer key: answer blocks
   are classed "no-print" at build time (the CSS print rules hide
   them without JavaScript) and are also stripped from the cloned
   copy made for the print dialog.

   Watermark: a subtle diagonal EKGURU mark on every printed
   worksheet is drawn by css/experience.css §27 as an ::after
   overlay on .ws-page (pseudo-elements are not touched by the
   *{background:#fff} print cleanup, so nothing can wipe it).

   Normal printing (Ctrl+P on a lesson, an article, a hub) is left
   to the stylesheet: the chrome is hidden and the content prints.
   This script does not clone anything on ordinary pages.

   API: window.EKGURU_PRINT_SHEET = { build, clear, now, hasSheet }
   ========================================================= */
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
    return el && el.textContent ? el.textContent.trim() : "One Student. One Goal. One Guru.";
  }

  function sheetElement() {
    // Priority 1: a worksheet already built on the page
    var built = document.querySelector("#w-sheet .ws-page") ||
      document.querySelector(".ws-page");
    if (built && built.textContent.trim()) return built;

    // Priority 2: the builder is here, so build it the same way the
    // "Make worksheet" button does, then use the result.
    var make = document.getElementById("w-make");
    if (make) {
      try { make.click(); } catch (e) {}
      built = document.querySelector("#w-sheet .ws-page") ||
        document.querySelector(".ws-page");
      if (built && built.textContent.trim()) return built;
    }

    // Priority 3: the page's explicit print target
    var target = document.querySelector("[data-print-target]");
    if (target && target.textContent.trim()) return target;

    // Nothing real: the caller must tell the visitor, not print a page.
    return null;
  }

  function hasSheet() {
    return !!sheetElement();
  }

  /* The answer key never goes on the learner's paper. Answer blocks are
     classed "no-print" by the builders (the stylesheet hides them without
     JavaScript); this also removes an "Answers" heading plus the answer
     lines that follow it, keeping the sheet's footer note. */
  function stripAnswerKey(scope) {
    var removed = 0;
    var hs = scope.querySelectorAll("h2, h3");
    for (var i = 0; i < hs.length; i++) {
      var h = hs[i];
      if (!/^\s*answers?\s*$/i.test(h.textContent || "")) continue;
      var node = h.nextSibling;
      h.parentNode.removeChild(h);
      while (node && node.nodeType === 1 &&
             node.tagName.toLowerCase() === "p" &&
             !/quiz bank|free to print/i.test(node.textContent || "")) {
        var nxt = node.nextSibling;
        node.parentNode.removeChild(node);
        removed++;
        node = nxt;
      }
    }
    /* "…then check the answer section" stops being true once the answers
       are gone from the paper. */
    var ps = scope.querySelectorAll("p");
    for (var k = 0; k < ps.length; k++) {
      if (/check the answer section/i.test(ps[k].textContent || "")) {
        ps[k].parentNode && ps[k].parentNode.removeChild(ps[k]);
        removed++;
      }
    }
    return removed;
  }

  function stampLine() {
    var path = location.pathname.replace(/index\.html$/, "");
    var tagline = liveTagline();
    return path + "  ·  © " + YEAR + " " + BRAND + "  ·  " + tagline +
      "  ·  printed " + new Date().toISOString().slice(0, 10) + "  ·  ekguru.shop";
  }

  function build() {
    if (document.getElementById(ROOT_ID)) return true;
    var el = sheetElement();
    if (!el) return false;   // honest abort — see the header comment

    var root = document.createElement("div");
    root.id = ROOT_ID;
    root.setAttribute("data-watermark", BRAND.toUpperCase());
    root.style.cssText = "display:none";

    var clone = el.cloneNode(true);
    clone.removeAttribute("data-print-target");
    clone.style.cssText = "background:#fff;color:#000;padding:0;margin:0;max-width:none;box-shadow:none;border:none";

    /* The sheet only: no controls, no ads, no chrome, no answers. */
    var kills = clone.querySelectorAll(
      ".no-print, .sb-hint, .hi-listen, button, script, .hdr, .ftr, nav, " +
      ".crumb, .pw-support, .pw-next, .prevnext, .course-tools, .course-hero, " +
      ".xp-orb, .xp-progress, .adsbygoogle, ins, #ekguru-consent, " +
      "#ekguru-offline-game, details, .ans, #w-make, #w-topic, #w-n, #w-ans, #w-print");
    for (var i = 0; i < kills.length; i++) {
      if (kills[i].parentNode) kills[i].parentNode.removeChild(kills[i]);
    }
    stripAnswerKey(clone);

    /* Flattened print styles */
    var all = clone.querySelectorAll("*");
    for (var j = 0; j < all.length; j++) {
      if (all[j].style) {
        all[j].style.boxShadow = "none";
        all[j].style.background =
          String(all[j].style.background).indexOf("gradient") >= 0 ? "#fff" : all[j].style.background;
      }
    }

    root.appendChild(clone);

    var line = document.createElement("p");
    line.className = "print-stamp";
    line.textContent = stampLine();
    line.style.cssText = "margin-top:20px;padding-top:10px;border-top:1px solid #999;color:#666;font-size:9pt;text-align:center";
    root.appendChild(line);

    document.body.appendChild(root);
    document.documentElement.classList.add(CLASS);

    /* Print-only styles. The watermark itself comes from the stylesheet
       (::after on .ws-page) so it survives this *{background:#fff} reset. */
    var style = document.createElement("style");
    style.id = "ekguru-print-style";
    style.textContent =
      "@media print {" +
      "html,body{background:#fff !important;margin:0 !important;padding:0 !important}" +
      "body > *:not(#" + ROOT_ID + "){display:none !important}" +
      "#" + ROOT_ID + "{display:block !important;position:static !important;width:100% !important;max-width:none !important}" +
      "#" + ROOT_ID + " *{color:#000 !important;background:#fff !important;box-shadow:none !important}" +
      "#" + ROOT_ID + " .ws-page{padding:0 !important;margin:0 !important;border:none !important;position:relative !important;overflow:visible !important}" +
      "}";
    document.head.appendChild(style);

    return true;
  }

  function clear() {
    var root = document.getElementById(ROOT_ID);
    if (root && root.parentNode) root.parentNode.removeChild(root);
    document.documentElement.classList.remove(CLASS);
    var style = document.getElementById("ekguru-print-style");
    if (style && style.parentNode) style.parentNode.removeChild(style);
  }

  /* Honest abort UI: a small visible notice, no silent print. */
  function tellNoSheet() {
    var n = document.createElement("div");
    n.id = "ekguru-print-notice";
    n.style.cssText =
      "position:fixed;bottom:16px;left:50%;transform:translateX(-50%);" +
      "max-width:min(92vw,520px);background:#fff;color:#111;z-index:9999;" +
      "border:1px solid #999;border-radius:10px;padding:12px 16px;" +
      "font:14px/1.5 system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.18)";
    n.textContent =
      "There is no worksheet on this page to print. Worksheets live under " +
      "Practice → Worksheets for each language. Nothing was printed.";
    document.body.appendChild(n);
    setTimeout(function () {
      if (n.parentNode) n.parentNode.removeChild(n);
    }, 9000);
  }

  /* Ctrl+P / browser print: build the sheet copy when this page has one;
     on ordinary pages the stylesheet handles the print (chrome off,
     content on). Never clone main/article into the print root. */
  function onBeforePrint() {
    if (document.getElementById(ROOT_ID)) return;
    if (!hasSheet()) return;
    build();
  }
  function onAfterPrint() {
    clear();
  }

  window.addEventListener("beforeprint", onBeforePrint);
  window.addEventListener("afterprint", onAfterPrint);
  if (window.matchMedia) {
    var mq = window.matchMedia("print");
    var handler = function (m) { if (m.matches) onBeforePrint(); else onAfterPrint(); };
    if (mq.addEventListener) mq.addEventListener("change", handler);
    else if (mq.addListener) mq.addListener(handler);
  }

  /* Every print button on the site runs the same honest path. */
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('[onclick*="window.print"], .print-btn, #print-worksheet, #w-print')
      .forEach(function (btn) {
        if (btn.__ekguruPrintWired) return;
        btn.__ekguruPrintWired = true;
        btn.addEventListener("click", function (e) {
          /* The worksheet builder wires #w-print itself (it knows whether a
             sheet was made); only take over buttons that print directly. */
          if (btn.id === "w-print") return;
          e.preventDefault();
          window.EKGURU_PRINT_SHEET.now();
        });
      });
  });

  window.EKGURU_PRINT_SHEET = {
    build: build,
    clear: clear,
    hasSheet: hasSheet,
    now: function () {
      var had = build();
      if (!had) {
        tellNoSheet();
        return false;
      }
      /* Small delay so the clone is laid out before the dialog opens. */
      setTimeout(function () {
        window.print();
        setTimeout(clear, 500);
      }, 100);
      return true;
    },
    printWorksheet: function (selector) {
      var el = selector ? document.querySelector(selector) : sheetElement();
      if (!el || !el.textContent.trim()) {
        tellNoSheet();
        return false;
      }
      /* Reuse the same honest pipeline with an explicit element. */
      if (document.getElementById(ROOT_ID)) clear();
      var root = document.createElement("div");
      root.id = ROOT_ID;
      root.setAttribute("data-watermark", BRAND.toUpperCase());
      root.style.cssText = "display:none";
      var clone = el.cloneNode(true);
      clone.removeAttribute("data-print-target");
      var kills = clone.querySelectorAll(
        ".no-print, .sb-hint, .hi-listen, button, script, .hdr, .ftr, nav, " +
        ".crumb, .pw-support, .adsbygoogle, ins, #ekguru-consent, details, .ans");
      for (var i = 0; i < kills.length; i++) {
        if (kills[i].parentNode) kills[i].parentNode.removeChild(kills[i]);
      }
      stripAnswerKey(clone);
      root.appendChild(clone);
      var line = document.createElement("p");
      line.className = "print-stamp";
      line.textContent = stampLine();
      root.appendChild(line);
      document.body.appendChild(root);
      document.documentElement.classList.add(CLASS);
      window.print();
      setTimeout(clear, 500);
      return true;
    }
  };
})();
