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
/* v49 — support page payment reset: the user-facing payment is now the
   OFFICIAL Razorpay Payment Page embed + direct payment-link fallback
   (support/index.html). The old hero, promo cards and the
   choose-a-method grid are gone; the custom API checkout stays disabled
   (PAYMENT_MODE = "COMING_SOON"). Cache generation moves so returning
   visitors cannot keep the old payment surface or the removed hero art. */
/* v50 — exec-v3 hardening pass: shared 8-language greeting (js/greeting.js)
   joins the shell so the cached home page greets offline too; the support
   surface lost its stale second Payment Page id and its stub section; the
   non-English support bands are localized. Cache generation moves so no
   returning visitor keeps the old greeting-less shell or the old bands. */
/* v51 — PR #8 final hardening: single-owner drawer (js/experience.js stands
   down protocol-side) with swipe-to-close restored in js/site-shell.js;
   single-chain support toast; double-evaluation guards on the payment,
   mailer, settings, lazy-loader and site-config chains; per-word greeting
   lang tags; duplicate script tags removed (/contact/, admin). Cache
   generation moves so no returning visitor keeps the double drawer, the
   pre-guard payment file or the old toast chain. */
/* BUILD: 2026-09-19T18:10:00Z v51 - pr8 final hardening: drawer-swipe-guards-toast */
/* v52 — ULTRA v3 device-only learning: bounded offline level snapshots, private/payment/contact routes
   never cached, runtime cache capped at 160 entries, voice/journal/theme scripts in the shell. The
   join and support pages are no longer pre-cached (forms and payment surfaces are never saved). */
/* v53 — the course-player's sentence reorder interaction now uses native,
   keyboard-operable word buttons and a live sentence preview. Rotate the
   shell cache so offline course learners receive the updated player too. */
/* v54 — course reorder motion is suppressed for reduced-motion users, and
   language pages now consume their generated abstract pattern tokens. Rotate
   the shell cache for updated shared assets. */
const BUILD_ID = "2026-10-06T00:00:00Z-v54-phase10-themes-motion";
const CACHE = "ekguru-" + BUILD_ID;

/* Phase 6 §14 — "Save for offline" pins learner-chosen pages in a dedicated
   cache that survives the main cache rotation. Only same-origin, non-private
   pages are ever saved (the message handler refuses everything else). */
const OFFLINE = "ekguru-offline-v1";
const MAX_RUNTIME = 160, MAX_PINNED = 200, MAX_PINNED_BYTES = 25 * 1024 * 1024, MAX_FILE_BYTES = 3 * 1024 * 1024;

const SHELL = [
  "./",
  "./index.html",
  "./find-tutors.html",
  "./css/style.min.css",
  "./css/support-razorpay.css",
  "./js/support-razorpay.js",
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
  /* v50 — the shared greeting. The cached home page mounts it in the hero;
     without this entry an offline revisit greets with an empty line. */
  "./js/greeting.js",
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
  /* v300 — modern learning enhancements, visuals, adaptive
     (offline games removed outright; see cleanupRemovedGame) */
  "./js/level-visuals.js",
  "./js/visual-learning.js",
  "./js/practice-api.js",
  "./js/refresh-guard.js",
  "./js/cookie-consent.js",
  "./js/monetization.js",
  "./js/adaptive-practice.js",
  "./js/scroll-restore.js",
  "./js/seo.js",
  "./js/seo-engine.js",
  /* v200 — the world emblems. Three small SVGs (5-6 KB each) rather than the
     whole set: these are the ones the home page, support/ and the courses hub
     show, so they are worth having before the first paint. The other markets'
     files are cached on demand by the runtime handler like any other image. */
  "./images/xp/world-en.svg",
  "./images/xp/world-multi.svg",
  "./images/logo.svg",
  /* v52 — design tokens, voice, device journal and the progress page */
  "./css/tokens.css",
  "./css/ultra.css",
  "./js/voice-languages.js",
  "./js/voice.js",
  "./js/speech-ui.js",
  "./js/ui-motion.js",
  "./js/global-srs.js",
  "./js/retention.js",
  "./data/learning/index.json",
  "./data/learning/offline-levels.json",
  "./learn/progress/"
];

/* Only explicit public learning inputs may be cached. Private/API/payment/contact/join/support routes,
   credentials, query strings and unknown data files are refused — in both caches, and in every fetch. */
function allowed(value) {
  try {
    if (typeof value !== "string" || !value || /%2f|%5c|\\|[<>\x00-\x1f]/i.test(value)) return false;
    const u = new URL(value, self.location.origin), path = decodeURIComponent(u.pathname);
    if (!["http:", "https:"].includes(u.protocol) || u.origin !== self.location.origin || u.search || u.username || u.password ||
        !path.startsWith("/") || path.split("/").some(x => x.startsWith("."))) return false;
    if (/^\/(?:api|admin|account|login|messages|notifications|checkout|payment|support|contact|join|booking|tutor)(?:[/.]|$)/i.test(path) ||
        /deploy-secrets|credentials|\.local\.|\.env(?:$|[/.])/i.test(path)) return false;
    if (path.startsWith("/data/") && !/^\/data\/(?:courses(?:\.json|\/(?:index\.json|phase-\d+\/[a-z]{2,3}_(?:A1|A2|B1|B2|C1|C2)[-_a-z0-9]*\.json))|global\/language-country-relations\.json|learning\/(?:index|offline-levels|placement\/[a-z]{2,3})\.json|audio-manifest\/[a-z]{2,3}\.json|practice(?:-flags)?\.json|practice\/index\.json)$/i.test(path)) return false;
    return true;
  } catch (_) { return false; }
}

let pinQueue = Promise.resolve();
function serialPin(task) { const next = pinQueue.then(task); pinQueue = next.catch(() => {}); return next; }

/* Runtime cache: never private/no-store, never over 3 MB, never more than MAX_RUNTIME entries. */
async function boundedPut(name, request, response) {
  if (/private|no-store/i.test(response.headers.get("cache-control") || "")) return;
  if (Number(response.headers.get("content-length")) > MAX_FILE_BYTES) return;
  const bytes = await response.arrayBuffer();
  if (bytes.byteLength > MAX_FILE_BYTES) return;
  const headers = new Headers(response.headers);
  headers.delete("content-length"); headers.delete("content-encoding");
  const cache = await caches.open(name);
  await cache.put(request, new Response(bytes, { status: response.status, headers }));
  const keys = await cache.keys();
  if (name === CACHE) for (const key of keys.slice(0, Math.max(0, keys.length - MAX_RUNTIME))) await cache.delete(key);
}

/* Pinned (saved-for-offline) files: 200 entries / 25 MiB in total, all-or-nothing with a rollback attempt. */
async function savePins(snapshots) {
  const cache = await caches.open(OFFLINE), existing = await cache.keys();
  const replacing = new Set(snapshots.map(([p]) => new URL(p, self.location.origin).href));
  let stored = 0, total = 0;
  for (const key of existing) if (!replacing.has(key.url)) { const r = await cache.match(key); stored += (await r.arrayBuffer()).byteLength; }
  for (const [, r] of snapshots) total += (await r.clone().arrayBuffer()).byteLength;
  if (stored + total > MAX_PINNED_BYTES || existing.filter(k => !replacing.has(k.url)).length + snapshots.length > MAX_PINNED) {
    throw new Error("Offline capacity reached. Clear saved learning snapshots in your journal first.");
  }
  const before = new Map(), changed = [];
  for (const [p] of snapshots) before.set(p, await cache.match(p));
  try { for (const [p, r] of snapshots) { changed.push(p); await cache.put(p, r); } }
  catch (error) {
    for (const p of changed.reverse()) try { before.get(p) ? await cache.put(p, before.get(p)) : await cache.delete(p); } catch (_) {}
    throw new Error("Offline storage is unavailable or full. Download did not complete.");
  }
  return { ok: true, files: snapshots.length, bytes: total };
}
async function snapshotOf(path) {
  const response = await fetch(path, { credentials: "omit", redirect: "error" });
  if (!response.ok || response.type === "opaque" || /private|no-store/i.test(response.headers.get("cache-control") || "")) throw new Error("File failed: " + path);
  const bytes = await response.arrayBuffer();
  if (bytes.byteLength > MAX_FILE_BYTES) throw new Error("File exceeds 3 MB.");
  const headers = new Headers(response.headers);
  headers.delete("content-encoding"); headers.delete("content-length"); headers.set("x-ekguru-snapshot-bytes", String(bytes.byteLength));
  return new Response(bytes, { status: 200, headers });
}
async function levelManifest() {
  const url = "/data/learning/offline-levels.json";
  let r;
  try { r = await fetch(url, { credentials: "omit" }); if (!r.ok) throw new Error("manifest"); } catch (_) { r = await caches.match(url); }
  if (!r) throw new Error("Offline download manifest unavailable. Open this level online first.");
  const data = await r.json();
  if (data.version !== 1 || !data.levels) throw new Error("Invalid download manifest.");
  return data;
}
async function downloadLevel(value) {
  const url = new URL(value, self.location.origin);
  if (!allowed(url.href) || url.hash || !/^\/languages\/[a-z]{2,3}\/level\/(?:a1|a2|b1|b2|c1|c2)\/$/.test(url.pathname)) throw new Error("refused");
  const spec = (await levelManifest()).levels[url.pathname];
  if (!spec || !Array.isArray(spec.urls) || spec.urls.length < 1 || spec.urls.length > 40 || !spec.urls.includes(url.pathname) ||
      spec.urls.some(u => !allowed(u) || new URL(u, self.location.origin).hash)) throw new Error("Invalid or excessive level download.");
  const snapshots = []; let total = 0;
  for (const path of spec.urls) {
    const r = await snapshotOf(path);
    total += Number(r.headers.get("x-ekguru-snapshot-bytes"));
    if (total > MAX_FILE_BYTES) throw new Error("Level download exceeded 3 MB.");
    snapshots.push([path, r]);
  }
  // Everything is fetched and checked BEFORE anything is written; a failed download never claims success.
  const result = await savePins(snapshots);
  return { ...result, url: url.pathname };
}

self.addEventListener("install", event => {
  /* Activate the new worker straight away instead of waiting for
     every tab to close. Without this, a fix can sit unused for
     days on a machine that never fully quits the browser. */
  self.skipWaiting();
  /* a missing file must not abort the whole install */
  event.waitUntil(
    caches.open(CACHE)
      .then(() => Promise.allSettled(SHELL.filter(allowed).map(async u => {
        const r = await fetch(u, { credentials: "omit", redirect: "error" });
        if (r.ok && r.type !== "opaque") await boundedPut(CACHE, u, r);
      })))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith("ekguru-") && k !== CACHE && k !== OFFLINE).map(k => caches.delete(k))))
      .then(() => caches.open(OFFLINE))
      .then(async pins => { for (const key of await pins.keys()) if (!allowed(key.url)) await pins.delete(key); })
      .then(() => self.clients.claim())
  );
});

/* Phase 6 §14 + v52 — message channel for Save-for-offline.
   save-offline {url} · remove-offline {url} · list-offline {} · download-level {url} · clear-offline {} */
self.addEventListener("message", event => {
  if (!event.ports || !event.ports[0]) return;
  const port = event.ports[0], d = event.data || {};
  event.waitUntil(serialPin(async () => {
    try {
      if (d.type === "download-level") { port.postMessage(await downloadLevel(d.url)); return; }
      if (d.type === "clear-offline") { await caches.delete(OFFLINE); await caches.delete(CACHE); port.postMessage({ ok: true }); return; }
      const cache = await caches.open(OFFLINE);
      if (d.type === "list-offline") { port.postMessage({ ok: true, urls: (await cache.keys()).filter(k => allowed(k.url)).map(k => new URL(k.url).pathname) }); return; }
      if (!allowed(d.url) || !["save-offline", "remove-offline"].includes(d.type)) throw new Error("refused");
      const url = new URL(d.url, self.location.origin);
      if (url.hash) throw new Error("refused");
      if (d.type === "remove-offline") await cache.delete(url.pathname);
      else await savePins([[url.pathname, await snapshotOf(url.pathname)]]);
      port.postMessage({ ok: true });
    } catch (error) { port.postMessage({ ok: false, reason: error.message || "cache-error" }); }
  }));
});

self.addEventListener("fetch", event => {
  const req = event.request;

  /* only handle our own GET requests; never touch YouTube, fonts or analytics */
  if (req.method !== "GET" || req.headers.has("authorization") || !allowed(req.url)) return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isImage = /\.(png|jpe?g|webp|svg|ico|gif|avif)$/i.test(url.pathname);

  if (isImage) {
    /* cache first: filenames are stable, so a hit is always correct */
    event.respondWith(
      caches.match(req).then(hit => hit || fetch(req).then(res => {
        if (res.ok) {
          const copy = res.clone();
          event.waitUntil(boundedPut(CACHE, req, copy).catch(() => {}));
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
          event.waitUntil(boundedPut(CACHE, req, copy).catch(() => {}));
        }
        return res;
      }).catch(() =>
        /* offline: prefer an explicitly saved copy, then any cached copy */
        caches.open(OFFLINE).then(c => c.match(req)).then(hit =>
          hit || caches.match(req)).then(hit => hit || new Response("This file has not been saved for offline use.", { status: 503, headers: { "Content-Type": "text/plain; charset=utf-8" } }))
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
          event.waitUntil(boundedPut(CACHE, req, copy).catch(() => {}));
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
