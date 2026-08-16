/* =========================================================
   EkGuru — service worker
   ---------------------------------------------------------
   GitHub Pages sends a 10-minute cache lifetime on everything and
   there is no way to change that header. On a repeat visit the
   browser therefore re-downloads the stylesheet, the scripts and
   the photos even though none of them have changed.

   This worker keeps a local copy instead:

     · the shell (HTML, CSS, JS) is served from cache immediately,
       then refreshed in the background, so a repeat visit paints
       almost instantly and still picks up new work
     · images are served from cache first and kept, since they are
       versioned by filename and never change in place

   Bump CACHE when you deploy and the old one is cleared out.
   ========================================================= */

const CACHE = "ekguru-v21";

const SHELL = [
  "./",
  "./index.html",
  "./find-tutors.html",
  "./join.html",
  "./css/style.min.css",
  "./js/site-config.js",
  "./js/i18n.js",
  "./js/tutors/_registry.js",
  "./js/tutors-data.js",
  "./js/pricing.js",
  "./js/main.js",
  "./images/logo.svg"
];

self.addEventListener("install", event => {
  /* a missing file must not abort the whole install */
  event.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.allSettled(SHELL.map(u => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;

  /* only handle our own GET requests; never touch YouTube, fonts or analytics */
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isImage = /\.(png|jpe?g|webp|svg|ico|gif|avif)$/i.test(url.pathname);

  if (isImage) {
    /* cache first: filenames are stable, so a hit is always correct */
    event.respondWith(
      caches.match(req).then(hit => hit || fetch(req).then(res => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
        }
        return res;
      }).catch(() => hit))
    );
    return;
  }

  /* everything else: serve the cached copy at once, refresh behind it */
  event.respondWith(
    caches.match(req).then(hit => {
      const network = fetch(req).then(res => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
        }
        return res;
      }).catch(() => hit);
      return hit || network;
    })
  );
});
