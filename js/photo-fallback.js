/* Static tutor-profile image recovery. The dynamic cards have an equivalent
   handler in main.js; this tiny listener is for pre-rendered profile pages. */
(function () {
  "use strict";
  document.addEventListener("error", function (event) {
    var img = event.target;
    if (!img || img.tagName !== "IMG" || !img.hasAttribute("data-eg-photo-fallback")) return;

    var src = String(img.currentSrc || img.src || "");
    var match = /lh\d?\.googleusercontent\.com\/d\/([A-Za-z0-9_-]{10,})/i.exec(src);
    if (!match && /^https:\/\/(?:drive\.google\.com|drive\.usercontent\.google\.com|docs\.google\.com)\//i.test(src)) {
      match = /\/(?:file\/d|d)\/([A-Za-z0-9_-]{10,})/i.exec(src) ||
        /[?&]id=([A-Za-z0-9_-]{10,})(?:[&#]|$)/i.exec(src);
    }
    var driveId = match && match[1];
    var attempt = Number(img.dataset.driveRetry || 0);
    var driveSources = driveId ? [
      "https://drive.google.com/thumbnail?id=" + driveId + "&sz=w800",
      "https://drive.google.com/uc?export=view&id=" + driveId,
      "https://drive.usercontent.google.com/download?id=" + driveId + "&export=view"
    ] : [];
    if (attempt < driveSources.length) {
      img.dataset.driveRetry = String(attempt + 1);
      img.src = driveSources[attempt];
      return;
    }
    if (img.dataset.localRetry !== "1") {
      img.dataset.localRetry = "1";
      img.removeAttribute("srcset");
      img.src = "/images/placeholder-tutor.jpg";
      return;
    }
    img.removeAttribute("srcset");
    img.onerror = null;
    img.src = "data:image/svg+xml;utf8," + encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#6741d9"/><stop offset="1" stop-color="#a855f7"/></linearGradient></defs><rect width="200" height="200" rx="30" fill="url(#g)"/><circle cx="100" cy="77" r="33" fill="#fff" fill-opacity=".94"/><path d="M30 200a70 70 0 01140 0z" fill="#fff" fill-opacity=".94"/></svg>'
    );
  }, true);
})();
