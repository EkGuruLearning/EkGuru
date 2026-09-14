/* EkGuru cookie notice (v159): tiny, honest, dependency-free.
   Shows once per browser; dismissal persists. Links Privacy for details
   and opt-outs. Never blocks content; never claims to block cookies. */
(function () {
  try {
    if (window.localStorage.getItem("ekguru_consent") === "1") return;
    var css = ".ekg-consent{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));" +
      "z-index:400;max-width:560px;margin:0 auto;display:flex;gap:12px;align-items:center;" +
      "background:rgba(28,20,60,.96);color:#fff;border-radius:16px;padding:14px 16px;" +
      "box-shadow:0 12px 32px rgba(0,0,0,.3);font-size:.86rem;line-height:1.55;" +
      "transform:translateY(20px);opacity:0;transition:opacity .3s ease,transform .3s ease}" +
      ".ekg-consent.in{transform:none;opacity:1}" +
      ".ekg-consent a{color:#c4b5fd;font-weight:700}" +
      ".ekg-consent button{flex:none;border:none;border-radius:999px;padding:10px 20px;min-height:44px;" +
      "background:#fff;color:#4f32d9;font-weight:800;font-size:.86rem;cursor:pointer}" +
      "@media(prefers-reduced-motion:reduce){.ekg-consent{transition:none}}" +
      "@media print{.ekg-consent{display:none}}";
    var st = document.createElement("style");
    st.textContent = css;
    document.head.appendChild(st);
    var bar = document.createElement("div");
    bar.className = "ekg-consent";
    bar.setAttribute("role", "note");
    bar.setAttribute("aria-label", "Cookie notice");
    var tx = document.createElement("span");
    tx.textContent = "We use cookies for ads and analytics, as described in our ";
    var a = document.createElement("a");
    /* Privacy URL from our own script path: root-proof on any deploy. */
    var pre = "./";
    try {
      var src = document.currentScript && document.currentScript.src;
      if (src && src.indexOf("/js/cookie-consent.js") > -1) {
        pre = src.split("/js/cookie-consent.js")[0] + "/";
      }
    } catch (e0) {}
    a.href = pre + "privacy/";
    a.textContent = "Privacy Policy";
    tx.appendChild(a);
    tx.appendChild(document.createTextNode("."));
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = "Got it";
    b.addEventListener("click", function () {
      try { window.localStorage.setItem("ekguru_consent", "1"); } catch (e1) {}
      if (bar.parentNode) bar.parentNode.removeChild(bar);
    });
    bar.appendChild(tx);
    bar.appendChild(b);
    document.body.appendChild(bar);
    setTimeout(function () { try { bar.classList.add("in"); } catch (e2) {} }, 60);
  } catch (e) { /* consent never breaks the page */ }
})();
