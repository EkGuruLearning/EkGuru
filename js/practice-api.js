/* =========================================================
   EkGuru — PRACTICE SHARED API (v300)
   ---------------------------------------------------------
   Fixes: "practice questions use API so one user's flagged/
   liked questions visible to another" — previously only
   localStorage, so flags/likes were per-browser.

   New: shared flags/likes via API with fallback to localStorage
   + BroadcastChannel for multi-tab sync + server sync.

   Endpoints (mock-friendly):
     GET  /data/practice-flags.json   — shared flags/likes aggregate
     POST /api/practice/flag          — flag a question (if backend)
     POST /api/practice/like          — like a question
   Falls back to localStorage + BroadcastChannel if offline.

   Storage keys:
     ekguru_practice_flags_v2   — local flags
     ekguru_practice_likes_v2   — local likes
     ekguru_practice_shared_v2  — cached shared aggregate

   Security: no PII, only question hash + counts.
   ========================================================= */
(function(){
  "use strict";
  if (typeof window === "undefined") return;

  var FLAGS_KEY = "ekguru_practice_flags_v2";
  var LIKES_KEY = "ekguru_practice_likes_v2";
  var SHARED_KEY = "ekguru_practice_shared_v2";
  var API_BASE = "/api/practice";

  function read(key){
    try { return JSON.parse(localStorage.getItem(key) || "{}") || {}; } catch(e){ return {}; }
  }
  function write(key, data){
    try { localStorage.setItem(key, JSON.stringify(data)); } catch(e){}
  }

  // BroadcastChannel for multi-tab sync
  var bc = null;
  try {
    if ("BroadcastChannel" in window) {
      bc = new BroadcastChannel("ekguru_practice_sync");
      bc.onmessage = function(ev){
        if (!ev || !ev.data) return;
        if (ev.data.type === "flag" || ev.data.type === "like") {
          // merge into shared cache
          var shared = read(SHARED_KEY);
          var qh = ev.data.qhash;
          if (!shared[qh]) shared[qh] = { flags:0, likes:0, reports:[] };
          if (ev.data.type === "flag") shared[qh].flags = (shared[qh].flags||0)+1;
          if (ev.data.type === "like") shared[qh].likes = (shared[qh].likes||0)+1;
          write(SHARED_KEY, shared);
          // dispatch event for UI
          try { window.dispatchEvent(new CustomEvent("ekguru:practice-shared-update", { detail:{ qhash: qh, data: shared[qh] }})); } catch(e){}
        }
      };
    }
  } catch(e){}

  function qHash(questionText){
    var s = String(questionText||"").slice(0,120);
    var h=0;
    for (var i=0;i<s.length;i++) h = (h*31 + s.charCodeAt(i))|0;
    return "q_"+Math.abs(h).toString(36);
  }

  async function fetchShared(){
    if (typeof navigator !== "undefined" && navigator.onLine === false) return read(SHARED_KEY);
    try {
      var res = await fetch("/data/practice-flags.json", { cache:"no-store" });
      if (res.ok){
        var data = await res.json();
        write(SHARED_KEY, data);
        return data;
      }
    } catch(e){}
    return read(SHARED_KEY);
  }

  async function postAction(action, qhash, meta){
    var payload = { qhash: qhash, action: action, meta: meta||{}, at: Date.now(), anon: true };
    // Offline is local-first: never attempt a request the browser already knows cannot work.
    if (!(typeof navigator !== "undefined" && navigator.onLine === false)) try {
      var res = await fetch(API_BASE+"/"+action, {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        var updated = await res.json().catch(function(){ return null; });
        if (updated && updated.shared) {
          write(SHARED_KEY, updated.shared);
          return updated.shared;
        }
        // refetch
        return await fetchShared();
      }
    } catch(e){}
    // Fallback: local increment + broadcast
    var shared = read(SHARED_KEY);
    if (!shared[qhash]) shared[qhash] = { flags:0, likes:0, reports:[] };
    if (action === "flag") shared[qhash].flags = (shared[qhash].flags||0)+1;
    if (action === "like") shared[qhash].likes = (shared[qhash].likes||0)+1;
    if (meta && meta.reason) {
      shared[qhash].reports = shared[qhash].reports || [];
      shared[qhash].reports.push({ reason: meta.reason, at: Date.now() });
      // keep last 20
      if (shared[qhash].reports.length>20) shared[qhash].reports = shared[qhash].reports.slice(-20);
    }
    write(SHARED_KEY, shared);
    // broadcast
    try { if (bc) bc.postMessage({ type: action, qhash: qhash, meta: meta }); } catch(e){}
    try { window.dispatchEvent(new CustomEvent("ekguru:practice-shared-update", { detail:{ qhash: qhash, data: shared[qhash] }})); } catch(e){}
    return shared;
  }

  function flagQuestion(questionText, reason){
    var qh = qHash(questionText);
    var localFlags = read(FLAGS_KEY);
    if (localFlags[qh]) {
      // already flagged locally, still allow but don't double-count locally
      return postAction("flag", qh, { reason: reason||"flagged" });
    }
    localFlags[qh] = { at: Date.now(), reason: reason||"flagged" };
    write(FLAGS_KEY, localFlags);
    return postAction("flag", qh, { reason: reason||"flagged" });
  }

  function likeQuestion(questionText){
    var qh = qHash(questionText);
    var localLikes = read(LIKES_KEY);
    var isLiked = !!localLikes[qh];
    if (isLiked) {
      delete localLikes[qh];
      write(LIKES_KEY, localLikes);
      // unlike locally, but keep shared count (don't decrement global, only local toggle)
      var shared = read(SHARED_KEY);
      return Promise.resolve(shared);
    } else {
      localLikes[qh] = { at: Date.now() };
      write(LIKES_KEY, localLikes);
      return postAction("like", qh, {});
    }
  }

  function isFlagged(questionText){
    return !!read(FLAGS_KEY)[qHash(questionText)];
  }
  function isLiked(questionText){
    return !!read(LIKES_KEY)[qHash(questionText)];
  }
  function getSharedStats(questionText){
    var qh = qHash(questionText);
    var shared = read(SHARED_KEY);
    return shared[qh] || { flags:0, likes:0, reports:[] };
  }

  function enhancePracticeUI(){
    // Add flag/like buttons to practice engine UI
    document.addEventListener("click", function(e){
      var flagBtn = e.target.closest && e.target.closest("[data-practice-flag]");
      if (flagBtn) {
        var qText = flagBtn.getAttribute("data-practice-flag") || flagBtn.closest(".px-q")?.textContent || "";
        var reason = prompt("Why flag this question? (wrong answer, unclear, offensive, etc.)") || "flagged";
        flagQuestion(qText, reason).then(function(){
          flagBtn.textContent = "🚩 Flagged ("+getSharedStats(qText).flags+")";
          flagBtn.disabled = true;
        });
      }
      var likeBtn = e.target.closest && e.target.closest("[data-practice-like]");
      if (likeBtn) {
        var qText2 = likeBtn.getAttribute("data-practice-like") || likeBtn.closest(".px-q")?.textContent || "";
        likeQuestion(qText2).then(function(){
          var stats = getSharedStats(qText2);
          likeBtn.textContent = (isLiked(qText2) ? "❤️ Liked" : "🤍 Like") + " ("+stats.likes+")";
        });
      }
    });

    // Inject buttons after each question render via MutationObserver
    var observer = new MutationObserver(function(mutations){
      mutations.forEach(function(m){
        m.addedNodes.forEach(function(node){
          if (!(node instanceof Element)) return;
          var qEl = node.querySelector && (node.querySelector(".px-q") || (node.classList && node.classList.contains("px-q") ? node : null));
          if (!qEl) {
            // check if node itself is practice container
            if (node.querySelector) {
              var containers = node.querySelectorAll ? node.querySelectorAll(".px-q") : [];
              containers.forEach(injectButtons);
            }
            return;
          }
          injectButtons(qEl);
        });
      });
    });

    function injectButtons(qEl){
      if (!qEl || qEl.getAttribute("data-flag-injected")) return;
      qEl.setAttribute("data-flag-injected","1");
      var qText = qEl.textContent || "";
      var stats = getSharedStats(qText);
      var wrapper = document.createElement("div");
      wrapper.className = "px-shared-actions";
      wrapper.style.cssText = "display:flex;gap:8px;margin:8px 0 12px;flex-wrap:wrap;";
      wrapper.innerHTML =
        '<button type="button" class="btn btn-ghost" data-practice-like="'+escapeAttr(qText).slice(0,200)+'" style="font-size:12px;padding:4px 10px;border-radius:20px;border:1px solid #e5e7eb;">'+
          (isLiked(qText) ? '❤️ Liked' : '🤍 Like')+' ('+stats.likes+')</button>'+
        '<button type="button" class="btn btn-ghost" data-practice-flag="'+escapeAttr(qText).slice(0,200)+'" style="font-size:12px;padding:4px 10px;border-radius:20px;border:1px solid #e5e7eb;" '+(isFlagged(qText)?'disabled':'')+'>'+
          (isFlagged(qText) ? '🚩 Flagged ('+stats.flags+')' : '🚩 Flag ('+stats.flags+')')+'</button>'+
        '<span style="font-size:11px;color:#94a3b8;align-self:center;">Shared across all learners (API)</span>';
      qEl.parentNode.insertBefore(wrapper, qEl.nextSibling);
    }

    function escapeAttr(s){
      return String(s||"").replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    }

    // Initial scan
    document.querySelectorAll(".px-q").forEach(injectButtons);
    observer.observe(document.body, { childList:true, subtree:true });

    // Update on shared change
    window.addEventListener("ekguru:practice-shared-update", function(ev){
      if (!ev.detail) return;
      // re-render counts
      document.querySelectorAll("[data-practice-like],[data-practice-flag]").forEach(function(btn){
        var qText = btn.getAttribute("data-practice-like") || btn.getAttribute("data-practice-flag") || "";
        if (!qText) return;
        var stats = getSharedStats(qText);
        if (btn.hasAttribute("data-practice-like")) {
          btn.textContent = (isLiked(qText) ? "❤️ Liked" : "🤍 Like") + " ("+stats.likes+")";
        } else {
          if (!isFlagged(qText)) btn.textContent = "🚩 Flag ("+stats.flags+")";
        }
      });
    });

    // Initial fetch
    fetchShared();
  }

  function init(){
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", enhancePracticeUI);
    } else {
      enhancePracticeUI();
    }
  }
  init();

  window.EKGURU_PRACTICE_API = {
    flagQuestion: flagQuestion,
    likeQuestion: likeQuestion,
    isFlagged: isFlagged,
    isLiked: isLiked,
    getSharedStats: getSharedStats,
    qHash: qHash,
    fetchShared: fetchShared,
    postAction: postAction
  };
})();
