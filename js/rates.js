/* =========================================================
   EkGuru — LIVE EXCHANGE RATES
   ---------------------------------------------------------
   WHAT THIS FIXES

   js/site-config.js carries a table of hand-typed rates. They
   were correct when they were typed and then quietly rotted.
   Checked on 08/09/2026 against the real market:

       ARS   config 950      real 1511     59% wrong
       TRY   config 32       real 48.5     51% wrong
       GHS   config 15       real 11.4     24% wrong
       INR   config 83       real 94.5     14% wrong

   Average error across all 50 currencies: 9%. An Argentinian
   student was being quoted roughly a third of the real price.

   This file fetches today's real rates instead, once per day,
   and hands them to js/pricing.js before it converts anything.

   ---------------------------------------------------------
   THE SOURCE

   open.er-api.com — the free, open tier of exchangerate-api.com.
   No API key, no sign-up, no rate limit worth worrying about,
   CORS enabled so a static page can call it directly. It
   refreshes once every 24 hours and covers 166 currencies,
   against the 50 typed into site-config.

   A second source is tried if the first is unreachable:
   the Currency API mirrored on jsDelivr's CDN.

   ---------------------------------------------------------
   IT CAN NEVER BREAK THE SITE

   · The hand-typed rates in site-config.js stay exactly where
     they are and remain the fallback. If the network is down,
     the API is down, or the visitor is offline, prices still
     show — just with the older numbers.
   · Rates are cached in the browser for 24 hours, so this
     costs one small request per visitor per day at most.
   · A response that looks wrong (missing USD, absurd values)
     is rejected rather than trusted.
   · Nothing about the visitor is sent. It is a plain GET for
     a public list of numbers.

   ---------------------------------------------------------
   TO SWITCH IT OFF
   js/site-config.js  →  pricing: { liveRates: false }
   The site instantly goes back to the typed table.
   ========================================================= */

(function () {
  "use strict";

  var S = window.EKGURU_SITE || {};
  var CFG = S.pricing || {};

  var CACHE_KEY = "ekguru_rates_v1";
  /* =========================================================
     WHEN TO REFRESH  (rewritten v55)
     ---------------------------------------------------------
     Prakash asked for "every 8 hours, or whenever the API itself
     updates". Those turn out to be the same request answered two
     ways, and the feed already tells us the answer.

     open.er-api.com returns, in every response:

         time_next_update_unix: 1788913661

     — the exact moment its own numbers change next. Caching until
     that timestamp is strictly better than any interval we could
     guess: no stale prices after an update, and no pointless
     requests before one.

     MAX_AGE is now only the FALLBACK, used when a response has no
     next-update field. Eight hours, as asked: three checks a day,
     which catches the daily update within hours without hammering
     a free endpoint.

     A hard ceiling of 48 hours applies on top, so a malformed or
     far-future timestamp can never freeze prices indefinitely. */
  var MAX_AGE = 8 * 60 * 60 * 1000;         // fallback: 8 hours
  var HARD_MAX = 48 * 60 * 60 * 1000;       // never trust a cache longer

  /* Tried in order. The first one that answers sensibly wins. */
  var SOURCES = [
    {
      name: "open.er-api.com",
      url: "https://open.er-api.com/v6/latest/USD",
      parse: function (j) {
        if (!j || j.result !== "success" || !j.rates) return null;
        /* v55: carry the feed's own next-update time through, so the
           cache can expire exactly when the numbers change rather
           than on a guessed interval. */
        return { rates: j.rates, date: j.time_last_update_utc || "",
                 nextUpdate: j.time_next_update_unix || null };
      }
    },
    {
      name: "currency-api (jsDelivr)",
      url: "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json",
      parse: function (j) {
        if (!j || !j.usd) return null;
        /* that feed uses lowercase keys and includes crypto — keep
           only three-letter fiat codes, uppercased */
        var out = {};
        Object.keys(j.usd).forEach(function (k) {
          if (/^[a-z]{3}$/.test(k)) out[k.toUpperCase()] = j.usd[k];
        });
        return { rates: out, date: j.date || "" };
      }
    }
  ];

  /* A feed is only believed if it looks like real money data. */
  function sane(rates) {
    if (!rates || typeof rates !== "object") return false;
    if (!rates.EUR || !rates.INR || !rates.GBP) return false;
    /* USD against itself must be 1 if it is quoted at all */
    if (rates.USD && Math.abs(rates.USD - 1) > 0.01) return false;
    /* these three have never been anywhere near these bounds */
    if (rates.EUR < 0.3 || rates.EUR > 3) return false;
    if (rates.GBP < 0.3 || rates.GBP > 3) return false;
    if (rates.INR < 20 || rates.INR > 500) return false;
    return Object.keys(rates).length >= 30;
  }

  function readCache() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var c = JSON.parse(raw);
      if (!c || !c.t || !sane(c.rates)) return null;

      var age = Date.now() - c.t;
      /* Absolute ceiling first. A corrupt or far-future nextUpdate
         must never be able to freeze prices for weeks. */
      if (age > HARD_MAX) return { stale: true, data: c };

      /* The feed told us when it changes next. Prefer that. */
      if (c.nextUpdate && typeof c.nextUpdate === "number") {
        return { stale: Date.now() >= c.nextUpdate, data: c };
      }
      /* No next-update field — fall back to the interval. */
      return { stale: age > MAX_AGE, data: c };
    } catch (e) { return null; }
  }

  function writeCache(rates, source, date, nextUpdate) {
    try {
      /* nextUpdate is stored in milliseconds. Ignore anything in the
         past or absurdly far ahead — a bad value here is the one
         thing that could silently stop refreshes altogether. */
      var nu = null;
      if (nextUpdate) {
        var ms = nextUpdate * 1000;
        if (ms > Date.now() && ms < Date.now() + HARD_MAX) nu = ms;
      }
      localStorage.setItem(CACHE_KEY, JSON.stringify({
        t: Date.now(), rates: rates, source: source, date: date, nextUpdate: nu
      }));
    } catch (e) {}
  }

  /* Merge live numbers over the typed ones. Anything the feed
     does not carry keeps its typed value, so no currency ever
     disappears from the switcher. */
  function apply(rates, meta) {
    var target = CFG.rates || (CFG.rates = {});
    var changed = 0;
    Object.keys(rates).forEach(function (c) {
      var v = rates[c];
      if (typeof v !== "number" || !isFinite(v) || v <= 0) return;
      if (target[c] !== v) changed++;
      target[c] = v;
    });
    window.EKGURU_RATE_INFO = {
      live: true,
      source: meta.source,
      date: meta.date,
      fetchedAt: meta.t,
      count: Object.keys(rates).length,
      updated: changed
    };
    return changed;
  }

  function markOffline(why) {
    window.EKGURU_RATE_INFO = {
      live: false,
      source: "js/site-config.js (typed table)",
      reason: why,
      count: Object.keys(CFG.rates || {}).length
    };
  }

  /* Tell the rest of the page that prices moved, so anything
     already on screen can redraw itself. */
  function announce() {
    try {
      window.dispatchEvent(new CustomEvent("ekguru:rates", {
        detail: window.EKGURU_RATE_INFO
      }));
    } catch (e) {
      /* very old browsers */
      try {
        var ev = document.createEvent("Event");
        ev.initEvent("ekguru:rates", true, true);
        window.dispatchEvent(ev);
      } catch (e2) {}
    }
  }

  function fetchFrom(i) {
    if (i >= SOURCES.length) {
      markOffline("no source answered");
      announce();
      return;
    }
    var src = SOURCES[i];
    var ctrl = null, timer = null;
    try { ctrl = new AbortController(); } catch (e) {}
    if (ctrl) timer = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, 6000);

    fetch(src.url, { signal: ctrl ? ctrl.signal : undefined, cache: "default" })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("HTTP " + r.status)); })
      .then(function (j) {
        if (timer) clearTimeout(timer);
        var got = src.parse(j);
        if (!got || !sane(got.rates)) throw new Error("response failed the sanity check");
        writeCache(got.rates, src.name, got.date, got.nextUpdate);
        apply(got.rates, { source: src.name, date: got.date, t: Date.now() });
        announce();
      })
      .catch(function () {
        if (timer) clearTimeout(timer);
        fetchFrom(i + 1);
      });
  }

  /* ---------------------------------------------------------
     Go
     --------------------------------------------------------- */
  if (CFG.liveRates === false) { markOffline("switched off in site-config.js"); return; }
  if (typeof window.fetch !== "function") { markOffline("browser has no fetch"); return; }

  var cached = readCache();

  /* A fresh cache is used immediately and synchronously, which
     matters: pricing.js reads CFG.rates the moment it loads, so
     the very first paint already carries today's real numbers. */
  if (cached && !cached.stale) {
    apply(cached.data.rates, {
      source: cached.data.source + " (cached)",
      date: cached.data.date,
      t: cached.data.t
    });
  } else if (cached && cached.stale) {
    /* Yesterday's numbers beat last year's typed ones while the
       new set is on its way. */
    apply(cached.data.rates, {
      source: cached.data.source + " (stale, refreshing)",
      date: cached.data.date,
      t: cached.data.t
    });
    fetchFrom(0);
  } else {
    markOffline("first visit, fetching");
    fetchFrom(0);
  }

  /* Expose a manual refresh for the admin page and for testing. */
  window.EkGuruRates = {
    info: function () { return window.EKGURU_RATE_INFO; },
    refresh: function () {
      try { localStorage.removeItem(CACHE_KEY); } catch (e) {}
      fetchFrom(0);
    }
  };
})();
