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

const CACHE = "ekguru-v31-1dbed90";

/* Phase 6 §14 — "Save for offline" pins learner-chosen pages in a dedicated
   cache that survives the main cache rotation. Only same-origin, non-private
   pages are ever saved (the message handler refuses everything else). */
const OFFLINE = "ekguru-offline-v1";

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
  "./js/rates.js",
  "./js/store.js",
  "./js/analytics.js",
  "./js/sheet.js",
  /* v66 — these two were missing, and their absence was invisible.

     js/livepatch.js is what writes the sheet's values into the
     pre-rendered pages, and js/tutors/_overrides.js is the sheet
     baked in at build time. A returning visitor got the cached
     shell without either, so on their second visit the profile
     pages silently stopped following the spreadsheet — the exact
     bug v65 existed to fix, reintroduced by the cache.

     _overrides.js is regenerated on EVERY build, so it must also be
     network-first. It is .js, so the isCode branch below already
     handles that. */
  "./js/livepatch.js",
  "./js/tutors/_overrides.js",
  "./js/reviews.js",
  "./js/calendar.js",
  "./js/mailer.js",
  /* v78 — the contact form's behaviour. Precached with mailer.js
     because the two are useless apart: mailer.js without
     contact.js means the form falls back to a mailto:, and
     contact.js without mailer.js means submit does nothing at
     all. Caching one and not the other is a half-working form. */
  "./js/contact.js",
  /* v80 — the idle-interaction self-healing watchdog. Kept in the
     shell so a returning visitor offline still gets the recovery
     layer, not just the cached page. */
  "./js/recovery.js",
  /* Phase 6 — Hindi learning product scripts, precached so a saved-for-
     offline lesson keeps working with no network. All are small, native
     helpers (no framework). */
  "./js/hindi-quiz-bank.js",
  "./js/hindi-fuzzy.js",
  "./js/hindi-srs.js",
  "./js/hindi-progress.js",
  "./js/hindi-audio.js",
  "./js/hindi-offline.js",
  "./js/hindi-tools.js",
  /* Phase 7 — global language registry + goal-based onboarding */
  "./js/languages.js",
  "./js/onboarding.js",
  "./images/logo.svg"
];

self.addEventListener("install", event => {
  /* Activate the new worker straight away instead of waiting for
     every tab to close. Without this, a fix can sit unused for
     days on a machine that never fully quits the browser. */
  self.skipWaiting();
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
      .then(keys => Promise.all(keys.filter(k => k !== CACHE && k !== OFFLINE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* Phase 6 §14 — message channel for Save-for-offline.
   save-offline  {url}          → pin a same-origin page
   remove-offline {url}         → unpin
   list-offline  {}             → saved list */
self.addEventListener("message", event => {
  const d = event.data || {};
  const reply = port => {
    try {
      if (d.type === "save-offline") {
        const url = new URL(d.url, self.location.origin);
        /* refuse anything outside our origin, and never cache admin/private state */
        if (url.origin !== self.location.origin ||
            /\/admin(\.html)?($|\/)/.test(url.pathname) ||
            /booking|join|contact/.test(url.pathname)) {
          port.postMessage({ ok: false, reason: "refused" });
          return;
        }
        caches.open(OFFLINE)
          .then(c => c.add(url.pathname + url.search))
          .then(() => port.postMessage({ ok: true }))
          .catch(() => port.postMessage({ ok: false, reason: "cache-error" }));
      } else if (d.type === "remove-offline") {
        const url = new URL(d.url, self.location.origin);
        caches.open(OFFLINE)
          .then(c => c.delete(url.pathname + url.search))
          .then(() => port.postMessage({ ok: true }));
      } else if (d.type === "list-offline") {
        caches.open(OFFLINE).then(c => c.keys()).then(keys => {
          port.postMessage({ ok: true, urls: keys.map(k => new URL(k.url).pathname) });
        });
      } else {
        port.postMessage({ ok: false, reason: "unknown-type" });
      }
    } catch (e) {
      port.postMessage({ ok: false, reason: "error" });
    }
  };
  if (event.ports && event.ports[0]) reply(event.ports[0]);
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

  /* =========================================================
     CODE AND PAGES: NETWORK FIRST
     ---------------------------------------------------------
     This used to be "serve the cached copy at once, refresh
     behind it" — `return hit || network`. That is fast, and it
     caused a real problem: a tutor's WhatsApp number was removed
     from the code, the fix was deployed, and browsers kept
     showing the old file from cache. The number stayed visible
     on screen for days after it had been deleted.

     For a privacy fix, "eventually correct" is not good enough.
     So HTML and JavaScript now go to the network first and fall
     back to the cache only when offline. Images stay cache-first
     above, because a filename never changes meaning.

     The cost is a few milliseconds. The benefit is that when
     something is removed, it is actually gone.
     ========================================================= */
  const isCode = /\.(html?|js|json|webmanifest)$/i.test(url.pathname) ||
                 url.pathname.endsWith("/");

  if (isCode) {
    event.respondWith(
      fetch(req).then(res => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
        }
        return res;
      }).catch(() =>
        /* offline: prefer an explicitly saved copy, then any cached copy */
        caches.open(OFFLINE).then(c => c.match(req)).then(hit =>
          hit || caches.match(req))
      )
    );
    return;
  }

  /* =========================================================
     BUG FOUND v66 — A THEME CHANGE NEVER REACHED ANYONE.

     css was cache-first: serve the stored copy, refresh behind.
     That is correct for a fingerprinted file whose name changes
     with its contents. style.min.css is NOT fingerprinted — the
     name is fixed and the contents change on every build.

     So a returning visitor kept the old stylesheet indefinitely.
     The whole v65 palette, the responsive fixes and the dark mode
     would have shipped to new visitors only, and Prakash would have
     seen none of it on the machine he tests from.

     Stale-while-revalidate instead: paint from the cache so there
     is no flash of unstyled text, and ALWAYS fetch behind it, so
     the next load has the new file. One request, and the fix
     actually arrives.
     ========================================================= */
  event.respondWith(
    caches.match(req).then(hit => {
      const network = fetch(req).then(res => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
        }
        return res;
      }).catch(() => hit);

      /* Revalidate even on a hit — the returned promise is the
         cached copy, but the fetch is already in flight and its
         result is written to the cache for next time. */
      if (hit) { network.catch(() => {}); return hit; }
      return network;
    })
  );
});
