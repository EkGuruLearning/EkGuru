/* =========================================================
   EkGuru — COPYWATCH  (js/copywatch.js)
   ---------------------------------------------------------
   Prakash:

     "copyright only ekguru ke pass hi ye pata hona chahiye
      ki jo text apna hai vo apna hi ho ... admin mai agar
      koi sheet copy kar de to pata chal jaye ... watermark
      hona chahiye jab bhi koi print ya download kare."

   The watermark and the print rules are the stylesheet's
   job (css/experience.css §21/§22) — they work with no
   JavaScript at all, which is the point: a no-JS visitor
   still gets a watermarked print.

   This file is the part that needs a browser:

     1. COPY — when text is copied off the page, the source
        line travels with it:

            …the copied text…

            — EkGuru · ekguru.shop/answers/hindi-numbers-1-to-100/
            © EkGuru. Not free to republish.

        Only when the selection is worth attributing (80+
        characters). Copying "₹8" to check a price should not
        paste a paragraph of legal text into a chat.

     2. PRINT — before printing, stamp the source URL and the
        date onto the page as a real element, so the printed
        sheet says where it came from even if the visitor's
        browser ignores the stylesheet's fixed watermark.

     3. DOWNLOAD — the worksheets are printed to PDF from the
        page. Anything that leaves through a click gets the
        watermark attribute if it does not have one, and the
        filename suggestion carries the site name.

     4. The provenance record — every page gets a
        <meta name="ekguru-owner"> fingerprint. tools/
        build-copy-index.js writes the same fingerprint into
        data/copy-index.json, so the admin dashboard can
        answer "is this our text?" for any passage, months
        later, without the page.

   Nothing here blocks or annoys a reader: no right-click
   disabling (it does not stop a determined copier and it
   breaks the browser for everyone else), no selection
   blocking, no fake numbers.
   ========================================================= */

(function () {
  "use strict";

  var doc = document;
  var SITE = (window.EKGURU_SITE || {});
  var BRAND = SITE.brand || "EkGuru";
  var YEAR = new Date().getFullYear();

  function path() {
    var p = location.pathname.replace(/index\.html$/, "");
    return location.origin.replace(/^https?:\/\//, "") + p;
  }

  function sourceLine() {
    return "\n\n— " + BRAND + " · " + path() + "\n© " + YEAR + " " + BRAND +
      ". This text is EkGuru's own; please link to it instead of republishing it.";
  }

  /* ---------------------------------------------------------
     1. copy
     --------------------------------------------------------- */
  var MIN = 80;   /* characters worth attributing */

  function onCopy(e) {
    var sel = window.getSelection && window.getSelection();
    if (!sel || sel.isCollapsed) return;
    var text = String(sel);
    if (text.length < MIN) return;
    /* already attributed (a double-copy, or a second handler) */
    if (text.indexOf(BRAND + " · " + path()) > -1) return;
    if (!e.clipboardData) return;                  /* old browser: leave it */
    e.preventDefault();
    e.clipboardData.setData("text/plain", text.replace(/\s+$/, "") + sourceLine());
    /* The HTML flavour keeps links working when pasted into a document.
       A bare text-only copy loses the URL, which is the whole point. */
    try {
      var html = sel.getRangeAt(0).cloneContents();
      var wrap = doc.createElement("div");
      wrap.appendChild(html);
      e.clipboardData.setData("text/html",
        "<div>" + wrap.innerHTML + "</div>" +
        "<p style=\"font-size:12px;color:#666\">— <a href=\"" + location.href + "\">" +
        BRAND + " · " + path() + "</a> · © " + YEAR + " " + BRAND + "</p>");
    } catch (err) { /* text flavour is enough */ }
  }

  /* ---------------------------------------------------------
     2. print
     --------------------------------------------------------- */
  function beforePrint() {
    if (doc.getElementById("ekguru-print-src")) return;
    var note = doc.createElement("p");
    note.id = "ekguru-print-src";
    note.setAttribute("data-ekguru-print", "1");
    note.style.cssText =
      "border-top:1px solid #999;margin:18px 0 0;padding-top:8px;" +
      "font:400 11px/1.5 system-ui,sans-serif;color:#333";
    note.textContent = path() + "  ·  © " + YEAR + " " + BRAND +
      "  ·  printed " + new Date().toISOString().slice(0, 10) +
      "  ·  ekguru.shop";
    (doc.querySelector("main") || doc.body).appendChild(note);
  }

  /* ---------------------------------------------------------
     3. download
     ---------------------------------------------------------
     A worksheet is an HTML page printed to PDF, or saved with
     Ctrl+S / "Save page as". Both go through the same two
     paths, so both are covered: the print stamp above, and the
     attribute below for anything that renders a sheet on screen.
     --------------------------------------------------------- */
  function stampSheets() {
    var sel = "[data-watermark], .worksheet, .sheet, .print-area, .ws, .flashcards, .quiz-sheet";
    var nodes = doc.querySelectorAll(sel);
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (!el.getAttribute("data-watermark")) el.setAttribute("data-watermark", BRAND);
    }
  }

  /* ---------------------------------------------------------
     4. boot
     --------------------------------------------------------- */
  function boot() {
    try { stampSheets(); } catch (e) {}
    doc.addEventListener("copy", onCopy, true);
    window.addEventListener("beforeprint", beforePrint);
    /* Safari fires onafterprint only; Chrome and Firefox both */
    if (window.matchMedia) {
      var mq = window.matchMedia("print");
      var handler = function (m) { if (m.matches) beforePrint(); };
      if (mq.addEventListener) mq.addEventListener("change", handler);
      else if (mq.addListener) mq.addListener(handler);
    }
    /* Ctrl+S / "Save page as" and the browser's own print shortcut */
    try {
      doc.addEventListener("keydown", function (e) {
        if ((e.ctrlKey || e.metaKey) && String(e.key).toLowerCase() === "s") beforePrint();
      }, true);
    } catch (e2) {}
  }

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
