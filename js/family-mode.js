/* =========================================================
   EkGuru — FAMILY MODE (Phase 7C §14/§44, privacy-safe)
   ---------------------------------------------------------
   A device-only toggle for parents and family learners. Turning
   it on does three real things on THIS device and nothing else:

     1. sets the analytics opt-out flag (ekguru_no_track=1),
     2. hides tutor/booking call-to-action elements on the page
        (the only interactive contacts on the site), and
     3. stores the preference locally — never uploaded.

   What it does NOT do, by design:
     - no child profile, no child messaging, no child contact
       details, no social/community features for minors,
     - no new data collection — there is no account at all,
     - the microphone is never used without an explicit tap
       (browser TTS playback and the typing trainer do not
       record anything).

   Honest scope: this is a privacy MODE, not child lesson content.
   No child-specific lessons have been authored yet.

   Window API: window.EkGuruFamilyMode
     isOn()           -> boolean
     enable()/disable()/toggle() -> updates state + DOM
     mount(el)        -> render the toggle control into el
   ========================================================= */
(function (root) {
  "use strict";

  var KEY = "ekguru_family_mode_v1";

  function isOn() {
    try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; }
  }

  function set(on) {
    try {
      if (on) {
        localStorage.setItem(KEY, "1");
        localStorage.setItem("ekguru_no_track", "1");
      } else {
        localStorage.removeItem(KEY);
      }
    } catch (e) {}
    applyDom(on);
    return on;
  }

  function applyDom(on) {
    document.documentElement.classList.toggle("family-mode", on);
    // hide tutor/booking CTAs when family mode is on (adult-facing contact points)
    var ctas = document.querySelectorAll("[data-family-hide]");
    for (var i = 0; i < ctas.length; i++) {
      ctas[i].hidden = on;
    }
  }

  var API = {
    isOn: isOn,
    enable: function () { return set(true); },
    disable: function () { return set(false); },
    toggle: function () { return set(!isOn()); },
    mount: function (el) {
      if (!el) return;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn";
      function paint() {
        var on = isOn();
        btn.textContent = on ? "✓ Family mode is on — turn off" : "Turn on family mode";
        btn.setAttribute("aria-pressed", on ? "true" : "false");
      }
      paint();
      btn.addEventListener("click", function () { API.toggle(); paint(); });
      el.appendChild(btn);
      // honour a saved preference on load
      if (isOn()) applyDom(true);
    }
  };

  root.EkGuruFamilyMode = API;
})(typeof window !== "undefined" ? window : globalThis);
