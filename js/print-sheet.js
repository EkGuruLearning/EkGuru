/* EkGuru — Print ONLY the worksheet v300
   Fixes: "print worksheet pura page hi print karti hai, only worksheet print karna hai"
   Modern approach: clone only worksheet, hide everything else
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
    return el && el.textContent ? el.textContent.trim() : "One Student. One Goal. One Guru.";
  }

  function sheetElement() {
    // Priority 1: built worksheet
    var built = document.querySelector("#w-sheet .ws-page") ||
      document.querySelector(".ws-page");
    if (built && built.textContent.trim()) return built;

    // Priority 2: auto-build if button exists
    var make = document.getElementById("w-make");
    if (make) {
      try { make.click(); } catch (e) {}
      built = document.querySelector("#w-sheet .ws-page") ||
        document.querySelector(".ws-page");
      if (built && built.textContent.trim()) return built;
    }

    // Priority 3: marked print target
    var target = document.querySelector("[data-print-target]");
    if (target && target.textContent.trim()) return target;
    
    // Priority 4: any worksheet-like element
    var marked = document.querySelector(".worksheet, .print-area, .flashcards, .quiz-sheet, .lv-main, .art");
    if (marked && marked.textContent.trim()) {
      // For lesson pages, create a clean worksheet version
      if (marked.classList.contains('art') || marked.classList.contains('lv-main')) {
        return createWorksheetFromContent(marked);
      }
      return marked;
    }
    return null;
  }

  function createWorksheetFromContent(contentEl) {
    // For non-worksheet pages, create a printable version with only essential content
    var wrapper = document.createElement('div');
    wrapper.className = 'ws-page print-worksheet';
    
    var title = document.querySelector('h1');
    if (title) {
      var h = document.createElement('h1');
      h.textContent = title.textContent;
      h.style.cssText = 'font-size:1.8rem;margin:0 0 16px;color:#000';
      wrapper.appendChild(h);
    }
    
    // Clone only learning content, not navigation
    var clone = contentEl.cloneNode(true);
    // Remove controls
    var remove = clone.querySelectorAll('button, .no-print, .sb-hint, .hi-listen, .say, nav, .crumb, .pw-support, .pw-next, .prevnext, .chips, .facts');
    for (var i = 0; i < remove.length; i++) {
      if (remove[i].parentNode) remove[i].parentNode.removeChild(remove[i]);
    }
    
    wrapper.appendChild(clone);
    return wrapper;
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
    if (!el) {
      // If no worksheet found, print main content only (not whole page)
      var main = document.querySelector('main, .art, .pw-legacy, .egc, .pw');
      if (main) el = main;
      else return false;
    }

    var root = document.createElement("div");
    root.id = ROOT_ID;
    root.setAttribute("data-watermark", BRAND);
    root.style.cssText = 'display:none';

    var clone = el.cloneNode(true);
    clone.removeAttribute("data-print-target");
    clone.style.cssText = 'background:#fff;color:#000;padding:0;margin:0;max-width:none;box-shadow:none;border:none';
    
    // Remove non-worksheet elements from clone
    var kills = clone.querySelectorAll(".no-print, .sb-hint, .hi-listen, button, script, .hdr, .ftr, nav, .crumb, .pw-support, .pw-next, .prevnext, .course-tools, .course-hero, .xp-orb, .xp-progress, .adsbygoogle, #ekguru-consent");
    for (var i = 0; i < kills.length; i++) {
      if (kills[i].parentNode) kills[i].parentNode.removeChild(kills[i]);
    }
    
    // Clean up styles for print
    var all = clone.querySelectorAll('*');
    for (var j = 0; j < all.length; j++) {
      if (all[j].style) {
        all[j].style.boxShadow = 'none';
        all[j].style.background = all[j].style.background.includes('gradient') ? '#fff' : all[j].style.background;
      }
    }
    
    root.appendChild(clone);

    var line = document.createElement("p");
    line.className = "print-stamp";
    line.textContent = stampLine();
    line.style.cssText = 'margin-top:20px;padding-top:10px;border-top:1px solid #999;color:#666;font-size:9pt;text-align:center';
    root.appendChild(line);

    document.body.appendChild(root);
    document.documentElement.classList.add(CLASS);
    
    // Add print-only styles
    var style = document.createElement('style');
    style.id = 'ekguru-print-style';
    style.textContent = 
      '@media print {' +
        'html,body{background:#fff !important;margin:0 !important;padding:0 !important}' +
        'body > *:not(#' + ROOT_ID + '){display:none !important}' +
        '#' + ROOT_ID + '{display:block !important;position:static !important;width:100% !important;max-width:none !important}' +
        '#' + ROOT_ID + ' *{color:#000 !important;background:#fff !important;box-shadow:none !important}' +
        '#' + ROOT_ID + ' .ws-page{padding:0 !important;margin:0 !important;border:none !important}' +
      '}';
    document.head.appendChild(style);
    
    return true;
  }

  function clear() {
    var root = document.getElementById(ROOT_ID);
    if (root && root.parentNode) root.parentNode.removeChild(root);
    document.documentElement.classList.remove(CLASS);
    var style = document.getElementById('ekguru-print-style');
    if (style && style.parentNode) style.parentNode.removeChild(style);
  }

  // Hook into print events
  window.addEventListener("beforeprint", build);
  window.addEventListener("afterprint", clear);
  
  if (window.matchMedia) {
    var mq = window.matchMedia("print");
    var handler = function (m) { if (m.matches) build(); else clear(); };
    if (mq.addEventListener) mq.addEventListener("change", handler);
    else if (mq.addListener) mq.addListener(handler);
  }

  // Override all print buttons to use our method
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[onclick*="window.print"], .print-btn, #print-worksheet').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        window.EKGURU_PRINT_SHEET.now();
      });
    });
  });

  window.EKGURU_PRINT_SHEET = {
    build: build,
    clear: clear,
    now: function () {
      var had = build();
      // Small delay to ensure DOM is ready
      setTimeout(function() {
        window.print();
        if (had) setTimeout(clear, 500);
      }, 100);
    },
    // New: print only worksheet element
    printWorksheet: function(selector) {
      var el = document.querySelector(selector || '.ws-page, [data-print-target]');
      if (!el) return false;
      
      var root = document.createElement("div");
      root.id = ROOT_ID;
      root.setAttribute("data-watermark", BRAND);
      root.appendChild(el.cloneNode(true));
      
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
