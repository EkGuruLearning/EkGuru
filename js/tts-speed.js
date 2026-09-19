/* =========================================================
   EkGuru — VOICE SPEED  (js/tts-speed.js)

   One global speech-speed control for every voice surface on
   the site, the way the P0 command specifies it:

     · range 0.1× to 1.0×, in 0.1 steps
     · default 0.8×
     · persisted in localStorage (key ekguru_tts_rate — the
       key the speed pill has always written)
     · no autoplay anywhere: this module only supplies a rate,
       speech still starts from an explicit user tap
     · honest labeling: the voice is the browser's own
       speech-synthesis voice, not a recorded speaker — the
       pill says so, instead of implying a human recording

   Every speaking script asks this module for the current rate
   at speak time:

       var r = window.EKGURU_TTS ? window.EKGURU_TTS.getRate() : 0.8;

   so a change in the pill applies to the next utterance on
   any surface — storybook, course player, practice engine,
   the Hindi audio tools — with nothing to reload.

   The pill shows only on pages that actually speak: this
   script is injected site-wide, but it mounts the control
   only when the page loads one of the voice scripts.
   ========================================================= */
(function () {
  "use strict";
  if (typeof window === "undefined" || !window.document) return;

  var KEY = "ekguru_tts_rate";
  var MIN = 0.1, MAX = 1.0, STEP = 0.1, DEF = 0.8;

  /* 0.85 -> 0.9, 1.5 -> 1.0, 0.05 -> 0.1. One decimal is all
     the pill can honestly offer. */
  function snap(v) {
    v = parseFloat(v);
    if (isNaN(v)) return DEF;
    if (v < MIN) v = MIN;
    if (v > MAX) v = MAX;
    /* integer tenths, then divide: 3/10 is the exact 0.3 double,
       3*0.1 is not. */
    return Math.round(v * 10) / 10;
  }

  function getRate() {
    try {
      var v = parseFloat(window.localStorage && localStorage.getItem(KEY));
      if (!isNaN(v)) return snap(v);
    } catch (e) {}
    return DEF;
  }

  function setRate(r) {
    r = snap(r);
    try { if (window.localStorage) localStorage.setItem(KEY, String(r)); } catch (e) {}
    return r;
  }

  var pill = null, ri = 0;
  /* integer tenths -> exact doubles: 0.1, 0.2, ... 1.0 */
  var RATES = [];
  (function () { for (var i = 1; i <= 10; i++) RATES.push(i / 10); })();

  function paint() {
    var rate = RATES[ri];
    pill.innerHTML = "<b>" + rate + "×</b> <span>speed</span>";
    pill.setAttribute("aria-label",
      "Speech speed " + rate + " times — your browser's own voice, not a recorded speaker");
  }

  function mountPill() {
    if (pill || !("speechSynthesis" in window)) return;
    pill = document.createElement("button");
    pill.type = "button";
    pill.className = "sb-speed";
    pill.title = "Speech speed · your browser's own voice, not a recorded speaker — tap to change";
    for (var q = 0; q < RATES.length; q++) {
      if (Math.abs(RATES[q] - getRate()) < 0.01) { ri = q; break; }
    }
    paint();
    pill.addEventListener("click", function (ev) {
      ev.stopPropagation();
      ri = (ri + 1) % RATES.length;
      setRate(RATES[ri]);
      paint();
    });
    document.body.appendChild(pill);
  }

  window.EKGURU_TTS = {
    getRate: getRate,
    setRate: setRate,
    min: MIN, max: MAX, step: STEP, def: DEF,
    key: KEY,
    mountPill: mountPill
  };

  /* The pill belongs on pages that speak. Every page loads this
     module; the voice pages load one of the four voice scripts,
     so the presence of its tag is the honest test. */
  function pageSpeaks() {
    return !!document.querySelector(
      'script[src*="js/storybook.js"],script[src*="js/hindi-audio.js"],' +
      'script[src*="js/course-player.js"],script[src*="js/practice-engine.js"]');
  }

  function init() {
    if (pageSpeaks()) mountPill();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
