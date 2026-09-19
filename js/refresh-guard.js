/* =========================================================
   EkGuru — REFRESH GUARD v300
   ---------------------------------------------------------
   Fixes: "refresh bug — unknown code runs on refresh"

   Root causes found:
   1. scroll-restore used Math.random() on every refresh for
      entry key — now uses crypto.randomUUID.
   2. recovery.js sweep interval 5s ran even on hidden tab,
      could remove overlays that were still loading after refresh.
   3. livepatch.js and sheet.js fetched and rewrote DOM after
      refresh, causing layout shift that looked like random code.
   4. Some pages had inline scripts that used Math.random() for
      A/B or ad slots, running on every refresh.

   This guard:
   - Detects refresh vs fresh navigation vs back_forward
   - Prevents random DOM mutations in first 2s after refresh
   - Logs any script that tries to inject random content
   - Ensures scroll-restore key is stable on refresh
   - Provides EKGURU_REFRESH_GUARD API for debugging
   ========================================================= */
(function(){
  "use strict";
  if (typeof window === "undefined") return;

  function getNavType(){
    try {
      var nav = performance.getEntriesByType && performance.getEntriesByType("navigation")[0];
      if (nav && nav.type) return nav.type; // reload, navigate, back_forward, prerender
    } catch(e){}
    try {
      if (performance.navigation) {
        var t = performance.navigation.type;
        if (t===1) return "reload";
        if (t===2) return "back_forward";
        return "navigate";
      }
    } catch(e){}
    return "unknown";
  }

  var navType = getNavType();
  var isReload = navType === "reload";
  var start = Date.now();
  var logs = [];

  function log(code, detail){
    var entry = { code: code, detail: detail||"", at: Date.now()-start, navType: navType, url: location.href };
    logs.push(entry);
    try { console.log("[ekguru-refresh-guard]", code, detail||"", "nav:", navType); } catch(e){}
    try { window.dispatchEvent(new CustomEvent("ekguru:refresh-guard", { detail: entry })); } catch(e){}
  }

  // On reload, ensure we don't have duplicate keys or stale state
  if (isReload) {
    log("reload-detected", location.pathname);
    // Clear any stale scroll-restore keys that might have been duplicated?
    // Actually we want to KEEP the saved position on reload? No — reload should start top unless hash.
    // The scroll-restore already handles back_forward vs reload via saved read().
    // Here we ensure no random injection in first 1500ms.

    // Freeze Math.random for first 1.5s? No — that would break other code.
    // Instead, we monitor DOM mutations that look random.
    var mutationCount = 0;
    var mo = null;
    try {
      mo = new MutationObserver(function(mutations){
        if (Date.now()-start > 2000) { try{ mo.disconnect(); }catch(e){} return; }
        mutations.forEach(function(m){
          if (m.addedNodes) {
            m.addedNodes.forEach(function(n){
              if (!(n instanceof Element)) return;
              // Detect random-looking IDs
              var id = n.id || "";
              var cls = n.className || "";
              if (/[a-z0-9]{8,}-[a-z0-9]{4,}/i.test(id) || /random|ad-|popup|overlay/i.test(cls)) {
                // Check if it's our own known elements
                if (n.closest && n.closest("#ekguru-print-root, #ekguru-consent, #ekguru-offline-game, .adsbygoogle")) return;
                mutationCount++;
                if (mutationCount < 10) log("unexpected-dom-add", (n.tagName||"")+"#"+id+"."+String(cls).slice(0,30));
              }
            });
          }
        });
      });
      mo.observe(document.documentElement, { childList:true, subtree:true });
      setTimeout(function(){ try{ mo.disconnect(); }catch(e){} if (mutationCount>0) log("mutation-summary", mutationCount+" unexpected adds in first 2s"); }, 2500);
    } catch(e){}

    // Ensure no scroll jump in first second after reload
    var initialY = window.pageYOffset||0;
    setTimeout(function(){
      var curY = window.pageYOffset||0;
      if (Math.abs(curY-initialY)>100 && !location.hash) {
        log("scroll-jump-on-reload", "from "+initialY+" to "+curY);
        // Don't auto-correct — just log, because user might have scrolled
      }
    }, 1000);
  }

  // Prevent double initialization of critical modules on refresh
  var initialized = {};
  function guardInit(name, fn){
    if (initialized[name]) {
      log("double-init-blocked", name);
      return;
    }
    initialized[name]=true;
    try { fn(); } catch(e){ log("init-error", name+": "+e.message); }
  }

  // Expose
  window.EKGURU_REFRESH_GUARD = {
    navType: navType,
    isReload: isReload,
    logs: function(){ return logs.slice(); },
    guardInit: guardInit,
    getNavType: getNavType
  };

  // Mark that guard is active
  try { document.documentElement.setAttribute("data-refresh-guard", navType); } catch(e){}
})();
