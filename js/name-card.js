/* Hindi name cards: local canvas only, no upload, tracker or payment. */
(function () {
  "use strict";
  var fontPromise;
  function loadCardFont() {
    if (!fontPromise) {
      fontPromise = (async function () {
        if (typeof FontFace !== "function" || !document.fonts) throw new Error("font API unavailable");
        var face = new FontFace("EkGuruCardDevanagari", "url(/images/fonts/noto-sans-devanagari-700.woff2)", { weight: "700" });
        var timer;
        try {
          await Promise.race([face.load(), new Promise(function (_, reject) {
            timer = setTimeout(function () { reject(new Error("font timeout")); }, 10000);
          })]);
          document.fonts.add(face);
        } finally { clearTimeout(timer); }
      })().catch(function (e) { fontPromise = null; throw e; });
    }
    return fontPromise;
  }
  function boot() {
    var button = document.getElementById("downloadNameCard");
    var status = document.getElementById("name-card-status");
    var input = document.getElementById("nameIn");
    if (!button || !status || !input || button.dataset.cardReady) return;
    button.dataset.cardReady = "1";
    button.addEventListener("click", async function () {
      var name = String(input.value || "").trim();
      var result = document.querySelector("#out .big");
      var hindi = result ? result.textContent.trim() : "";
      if (!name || !hindi) {
        status.textContent = "Type a name and wait for its spelling before downloading.";
        return;
      }
      if (Array.from(name).length > 80 || Array.from(hindi).length > 160) {
        status.textContent = "This card fits shorter names. Please use up to 80 characters; your result has not been truncated.";
        return;
      }
      button.disabled = true;
      status.textContent = "Preparing your card on this device…";
      var objectUrl;
      try {
        // Load one licensed, same-origin font only when a card is requested.
        // No typed name is included in this request. Fail visibly, not as tofu.
        await loadCardFont();
        var canvas = document.createElement("canvas");
        canvas.width = 1200; canvas.height = 630;
        var ctx = canvas.getContext("2d");
        if (!ctx) throw new Error("canvas unavailable");
        var bg = ctx.createLinearGradient(0, 0, 1200, 630);
        bg.addColorStop(0, "#24134a"); bg.addColorStop(1, "#49317d");
        ctx.fillStyle = bg; ctx.fillRect(0, 0, 1200, 630);
        ctx.fillStyle = "#f6cf80";
        ctx.fillRect(64, 64, 64, 6);
        ctx.font = '700 30px system-ui, sans-serif';
        ctx.textAlign = "left";
        ctx.fillText("EkGuru", 64, 118);
        ctx.fillStyle = "#e5d9ff";
        ctx.font = '24px system-ui, sans-serif';
        ctx.fillText("YOUR NAME IN HINDI", 64, 170);
        ctx.textAlign = "center";
        function fit(text, max, min, y, family) {
          var size = max;
          for (; size >= min; size -= 2) {
            ctx.font = '700 ' + size + 'px ' + family;
            if (ctx.measureText(text).width <= 1040) break;
          }
          if (size < min) throw new Error("name too wide");
          ctx.fillText(text, 600, y);
        }
        ctx.fillStyle = "#ffffff";
        fit(hindi, 112, 30, 330, '"EkGuruCardDevanagari", sans-serif');
        ctx.fillStyle = "#f6cf80";
        fit(name, 48, 20, 420, 'system-ui, sans-serif');
        ctx.fillStyle = "#e5d9ff";
        ctx.font = '22px system-ui, sans-serif';
        ctx.fillText("Transliteration · spelling may vary", 600, 505);
        ctx.fillStyle = "#ffffff";
        ctx.font = '600 25px system-ui, sans-serif';
        ctx.fillText("Try your name: ekguru.shop/name-in-hindi/", 600, 563);
        var blob = await new Promise(function (resolve) { canvas.toBlob(resolve, "image/png"); });
        if (!blob) throw new Error("PNG unavailable");
        objectUrl = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = objectUrl;
        a.download = "ekguru-name-card.png";
        document.body.appendChild(a); a.click(); a.remove();
        status.textContent = "PNG download started. The name is part of the image; share it only if you want to.";
        // Give the browser time to consume the download before releasing it.
        var release = objectUrl;
        setTimeout(function () { URL.revokeObjectURL(release); }, 30000);
        objectUrl = null;
      } catch (e) {
        status.textContent = "Could not create a PNG here. Try a shorter name or use Share link instead.";
      } finally {
        if (objectUrl) URL.revokeObjectURL(objectUrl);
        button.disabled = false;
      }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
