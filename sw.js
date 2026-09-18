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

/* v41 — two things a learner can use with no network at all:
     · js/question-api.js, so a flag or a like thrown offline is queued and
       still shows its badge (the API syncs when the network comes back)
     · js/print-sheet.js, the printed-sheet clone
   Bump CACHE so a returning visitor actually gets them. */
/* v40 — a worksheet printed offline prints the sheet: js/print-sheet.js
   (loaded by tools/build-print-sheets.py) clones the finished worksheet into
   #ekguru-print-root. Cached, so the one place a learner prints has the same
   rule as the online one.

   v200.2 — ONE header and ONE footer on all 1,563 pages (tools/build-shell.js),
   translated on the six market pages, with one owner of the drawer: the cache
   generation moves so a returning visitor cannot keep the old chrome, the old
   tagline or the second click handler on the menu button. */
/* BUILD: 2026-09-18T17:16:22Z dc5dde0 v43 - unique build identifier per P0-B */
const BUILD_ID = "2026-09-18T17:16:22Z-dc5dde0-v43";
const CACHE = "ekguru-" + BUILD_ID;

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
  "./courses/",
  "./js/course-player.js",
  "./data/courses/index.json",
  "./data/global/language-country-relations.json",
  "./js/site-config.js",
  "./js/i18n.js",
  "./js/tutors/_registry.js",
  "./js/tutors-data.js",
  "./js/pricing.js",
  "./js/main.js",
  /* v200 — the language-aware experience layer. js/experience.js drives the
     redesigned home/support/courses/search pages (reveal animation, hero
     script letters, language rail, search suggestions); js/site-search.js is
     the /search/ engine. Both are useless without the bundled stylesheet
     above, so they belong in the same cache generation. */
  "./js/experience.js",
  "./js/site-search.js",
  /* v200.2 — the shell. Every content page now carries the site header and
     footer (tools/build-shell.js) and these two give it behaviour: the
     drawer, the sheet-owned tagline, the copy source line and the print
     watermark. A cached page without them is the half-open drawer. */
  "./js/site-shell.js",
  "./js/copywatch.js",
  /* v40 — what actually reaches the printer. js/print-sheet.js clones the
     finished worksheet into #ekguru-print-root on Ctrl+P, so a worksheet
     printed offline prints the sheet and not the page around it. It belongs
     in the same cache generation as the copy source line it complements. */
  "./js/print-sheet.js",
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
  /* v41 — flags and likes, offline-first (tools/apps-script-questions.gs is
     the server half; with no endpoint the votes stay on the device). */
  "./js/question-api.js",
  /* Phase 7 — global language registry + goal-based onboarding */
  "./js/languages.js",
  "./js/onboarding.js",
  /* v300 — modern learning enhancements, offline games, visuals, adaptive */
  "./js/offline-games.js",
  "./js/level-visuals.js",
  "./js/visual-learning.js",
  "./js/practice-api.js",
  "./js/refresh-guard.js",
  "./js/cookie-consent.js",
  "./js/monetization.js",
  "./js/adaptive-practice.js",
  "./js/offline-game.js",
  "./js/scroll-restore.js",
  "./js/seo.js",
  "./js/seo-engine.js",
  /* v200 — the world emblems. Three small SVGs (5-6 KB each) rather than the
     whole set: these are the ones the home page, support/ and the courses hub
     show, so they are worth having before the first paint. The other markets'
     files are cached on demand by the runtime handler like any other image. */
  "./images/xp/world-en.svg",
  "./images/xp/world-hi.svg",
  "./images/xp/world-multi.svg",
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
  /* v42 — CSS BELONGS IN THIS LIST, and its absence was the bug Prakash kept
     hitting. style.min.css is NOT fingerprinted: the name never changes and
     the contents change on every build. It was falling through to the
     stale-while-revalidate branch at the bottom, which paints the OLD
     stylesheet and only stores the new one for "next time". So the first
     refresh after a deploy showed the old rules — a fresh print fix, a fresh
     palette, a fresh layout — and the *next* refresh suddenly showed
     something different. "Refresh karne pe kuch aur hi chalta hai."

     Everything that is code or styling is network-first now: one request,
     and what you see after a refresh is what is deployed. Offline, the
     cached copy is used, which is what the cache is for. */
  const isCode = /\.(html?|js|json|webmanifest|css)$/i.test(url.pathname) ||
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
