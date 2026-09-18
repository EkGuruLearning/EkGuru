/* ==========================================================================
   EkGuru — QUESTIONS API  (shared flags and likes, offline-first)
   --------------------------------------------------------------------------
   Prakash: "practice questions mai API use karo — jo ek user ne flag ya like
   kiya, wo doosre user ko bhi dikhna chahiye."

   The site is static, so "the API" is a small Google Apps Script Web App
   (tools/apps-script-questions.gs) that keeps one row per vote in a Sheet and
   answers two things: the counts for a bank, and the list of questions other
   learners flagged. Nothing here talks to a server until the endpoint is set
   in js/site-config.js — until then every vote lives on the device and the UI
   says so, honestly.

   THE CONTRACT  (Content-Type: text/plain, like js/mailer.js — an Apps Script
   Web App cannot answer a JSON preflight)

     GET  <endpoint>?bank=<slug>&action=top        → { ok, bank, counts }
     POST <endpoint>  { action, bank, id, reason, client }
          action: flag | unflag | like | unlike
          → { ok, bank, id, flags, likes }

   WHAT IS STORED, AND WHAT IS NOT
     · one row per vote: timestamp, bank, question id, action, reason, client
     · `client` is a random id made by the browser (ekguru_q_client_v1) and the
       server stores only a salted hash of it, so a flag can be counted once
       per device without keeping anything that identifies a person
     · no names, no emails, no IPs, no free text beyond the menu of reasons

   OFFLINE FIRST
     Votes are written to localStorage immediately, queued, and flushed when
     the tab comes online (or on the next load). Counts come from the last
     good answer plus this device's own votes, so a flagged question still
     shows its badge with no network at all.
   ========================================================================== */
(function () {
  "use strict";

  var QUEUE = "ekguru_q_queue_v1";
  var VOTES = "ekguru_q_votes_v1";
  var CACHE = "ekguru_q_cache_v1";
  var CLIENT = "ekguru_q_client_v1";
  var TTL = 6 * 60 * 60 * 1000;          /* counts are good for six hours */

  var REASONS = [
    "wrong answer",
    "typo or spelling",
    "confusing wording",
    "duplicate question",
    "not in the lesson"
  ];

  function config() {
    var site = window.EKGURU_SITE || {};
    var api = site.api || {};
    var url = api.questions || "";
    /* Only an Apps Script /exec URL is accepted — the same fail-soft rule the
       mailer uses, so a half-pasted value can never eat votes. */
    return /^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(url) ? url : "";
  }

  function read(key, fallback) {
    try {
      var raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) { return fallback; }
  }
  function write(key, value) {
    try { window.localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  }

  function clientId() {
    var id = read(CLIENT, null);
    if (!id) {
      id = "c" + Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);
      write(CLIENT, id);
    }
    return id;
  }

  function key(bank, id) { return bank + ":" + id; }

  function emit(bank) {
    try {
      window.dispatchEvent(new CustomEvent("ekguru:questions", { detail: { bank: bank } }));
    } catch (e) {}
  }

  /* ---- what this device has voted ------------------------------------- */
  function votes() { return read(VOTES, {}); }

  function myVote(bank, id) {
    var v = votes()[key(bank, id)];
    return v || null;                     /* "flag" | "like" | null */
  }

  /* ---- counts ----------------------------------------------------------- */
  function counts(bank) {
    var cache = read(CACHE, {});
    var entry = cache[bank] || {};
    var out = {};
    var k;
    for (k in (entry.counts || {})) out[k] = { flags: entry.counts[k].flags | 0, likes: entry.counts[k].likes | 0 };
    /* this device's votes, so a badge appears even before any sync */
    var mine = votes();
    for (k in mine) {
      if (k.indexOf(bank + ":") !== 0) continue;
      var id = k.slice(bank.length + 1);
      out[id] = out[id] || { flags: 0, likes: 0 };
      if (mine[k] === "flag") out[id].flags++;
      else out[id].likes++;
    }
    return out;
  }

  function topFlagged(bank, limit) {
    var c = counts(bank), rows = [];
    for (var id in c) if (c[id].flags > 0) rows.push({ id: id, flags: c[id].flags, likes: c[id].likes });
    rows.sort(function (a, b) { return b.flags - a.flags || (a.id < b.id ? -1 : 1); });
    return rows.slice(0, limit || 5);
  }

  /* ---- voting ----------------------------------------------------------- */
  /* The reason has to be part of the entry BEFORE the flush starts: adding it
     to the queue afterwards put it on a later parse of the array, while flush
     was already posting the earlier one — the server received a bare "flag"
     with no reason. (tools/test-question-api.mjs caught exactly that.) */
  function vote(bank, id, action, reason) {
    if (!bank || !id) return false;
    var mine = votes();
    var k = key(bank, id);
    var kind = action === "like" || action === "unlike" ? "like" : "flag";
    var want = action === "unlike" || action === "unflag" ? null : kind;
    mine[k] = want;
    if (want === null) delete mine[k];
    write(VOTES, mine);

    var entry = { action: action, bank: bank, id: id, client: clientId(), at: Date.now() };
    if (kind === "flag") {
      entry.reason = REASONS.indexOf(reason) >= 0 ? reason : "wrong answer";
    }
    var queue = read(QUEUE, []);
    queue.push(entry);
    write(QUEUE, queue);
    emit(bank);
    flush();
    return true;
  }

  function flag(bank, id, reason) { return vote(bank, id, "flag", reason); }

  function like(bank, id) { return vote(bank, id, myVote(bank, id) === "like" ? "unlike" : "like"); }
  function unflag(bank, id) { return vote(bank, id, "unflag"); }

  /* ---- the wire --------------------------------------------------------- */
  function post(entry) {
    var url = config();
    if (!url) return Promise.resolve(false);
    return fetch(url, {
      method: "POST",
      /* text/plain on purpose: a JSON content-type triggers a CORS preflight
         an Apps Script Web App cannot answer. */
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(entry)
    }).then(function (r) { return r.ok ? r.json() : false; })
      .then(function (j) { return !!(j && j.ok); })
      .catch(function () { return false; });
  }

  function same(a, b) {
    return a && b && a.at === b.at && a.bank === b.bank && a.id === b.id && a.action === b.action;
  }

  /* One flush at a time, and callers get the SAME promise. Two sources race
     for the queue — the vote itself, and the window coming back online — and
     without this the second caller was told "0 sent" while the first was
     still in the air, which is exactly what the test caught. */
  var inflight = null;

  function flush() {
    if (inflight) return inflight;
    var url = config();
    var queue = read(QUEUE, []);
    if (!url || !queue.length) return Promise.resolve(0);
    if (typeof navigator !== "undefined" && navigator.onLine === false) return Promise.resolve(0);

    var sent = 0;
    var chain = Promise.resolve();
    queue.forEach(function (entry) {
      chain = chain.then(function () {
        return post(entry).then(function (ok) {
          if (ok) {
            sent++;
            /* Match by the entry's own stamp, not by object identity: the
               queue on disk is a fresh parse, so the objects are never the
               same reference and indexOf() would silently remove nothing —
               the vote would be re-sent on every load. */
            var rest = read(QUEUE, []);
            for (var i = 0; i < rest.length; i++) {
              if (same(rest[i], entry)) { rest.splice(i, 1); break; }
            }
            write(QUEUE, rest);
          }
        });
      });
    });

    var lastBank = queue[queue.length - 1].bank;
    inflight = chain.then(function () {
      /* Refresh once the queue is empty, so the badges show the community's
         count and not only this device's. */
      return refresh(lastBank).then(function () { return sent; }, function () { return sent; });
    }).then(function (n) {
      inflight = null;
      return n;
    });
    return inflight;
  }

  function refresh(bank) {
    var url = config();
    if (!url || !bank) return Promise.resolve(false);
    return fetch(url + "?bank=" + encodeURIComponent(bank) + "&action=top", { method: "GET" })
      .then(function (r) { return r.ok ? r.json() : false; })
      .then(function (j) {
        if (!j || !j.ok || !j.counts) return false;
        var cache = read(CACHE, {});
        cache[bank] = { at: Date.now(), counts: j.counts };
        write(CACHE, cache);
        emit(bank);
        return true;
      })
      .catch(function () { return false; });
  }

  /* Counts cached for longer than the TTL are refreshed quietly on load. */
  function stale(bank) {
    var entry = (read(CACHE, {})[bank] || {});
    return !entry.at || (Date.now() - entry.at) > TTL;
  }

  function boot() {
    var queue = read(QUEUE, []);
    if (queue.length) flush();
    var cache = read(CACHE, {});
    Object.keys(cache).forEach(function (bank) { if (stale(bank)) refresh(bank); });
  }

  window.addEventListener("online", function () { flush(); });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();

  window.EKGURU_QUESTIONS = {
    reasons: REASONS,
    enabled: function () { return !!config(); },
    flag: flag,
    unflag: unflag,
    like: like,
    myVote: myVote,
    counts: counts,
    topFlagged: topFlagged,
    refresh: refresh,
    flush: flush,
    pending: function () { return read(QUEUE, []).length; }
  };
})();
