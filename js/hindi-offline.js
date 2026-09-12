/* =========================================================
   EkGuru — SAVE FOR OFFLINE  (v1)
   ---------------------------------------------------------
   Lets a learner pin a substantive lesson for offline reading.
   Honest limits:

     · Only same-origin pages are saved (the service worker
       refuses anything else).
     · The saved copy is a snapshot — it may be older than the
       live page. The UI says so.
     · Nothing private is cached: admin pages, booking data and
       utility states are never saved.
     · Full "offline mode" is only claimed for saved lessons
       (title + content + examples render); anything that needs
       the network (sheets, booking) is absent while offline.

   Works with sw.js's message channel (save-offline /
   remove-offline / list-offline) and tracks the saved set in
   localStorage under ekguru:hindi:v1:offline.
   ========================================================= */
(function () {
  "use strict";

  var KEY = "ekguru:hindi:v1:offline";

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; }
  }
  function write(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} }

  function path() { return (location.pathname || "/").replace(/\/EkGuru\//, "/"); }

  function swReady() {
    return navigator.serviceWorker && navigator.serviceWorker.ready;
  }

  function post(msg) {
    if (!swReady()) return Promise.reject(new Error("no service worker"));
    return navigator.serviceWorker.ready.then(function (reg) {
      return new Promise(function (resolve, reject) {
        var channel = new MessageChannel();
        channel.port1.onmessage = function (e) { resolve(e.data || {}); };
        reg.active.postMessage(msg, [channel.port2]);
        setTimeout(function () { reject(new Error("timeout")); }, 4000);
      });
    });
  }

  function isSaved() { return read().indexOf(path()) > -1; }

  var OFF = {
    isSaved: isSaved,

    save: function () {
      var p = path();
      return post({ type: "save-offline", url: p }).then(function (res) {
        if (!res.ok) throw new Error("save failed");
        var list = read();
        if (list.indexOf(p) < 0) { list.push(p); write(list); }
        return true;
      });
    },

    remove: function () {
      var p = path();
      return post({ type: "remove-offline", url: p }).then(function () {
        var list = read().filter(function (x) { return x !== p; });
        write(list);
        return true;
      });
    },

    savedList: function () { return read(); },

    mount: function () {
      var host = document.getElementById("offline-ctl");
      if (!host) return;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn ghost";
      function paint() {
        btn.textContent = isSaved() ? "✓ Saved for offline — remove" : "Save for offline";
        btn.setAttribute("aria-pressed", isSaved() ? "true" : "false");
      }
      paint();
      btn.addEventListener("click", function () {
        if (isSaved()) {
          OFF.remove().then(paint).catch(function () { paint(); });
        } else {
          OFF.save().then(paint).catch(function () {
            btn.textContent = "Could not save offline";
            setTimeout(paint, 2500);
          });
        }
      });
      var note = document.createElement("p");
      note.className = "muted";
      note.style.cssText = "font-size:.78rem;margin:6px 0 0";
      note.textContent = "Saves a snapshot of this page on this device. The offline copy may be older than the live page.";
      host.appendChild(btn);
      host.appendChild(note);

      // offline state notice
      if (typeof navigator !== "undefined" && navigator.onLine === false && isSaved()) {
        var off = document.createElement("p");
        off.setAttribute("role", "status");
        off.textContent = "You are offline — showing your saved copy.";
        host.appendChild(off);
      }
    }
  };

  window.EkGuruOffline = OFF;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { OFF.mount(); });
  } else {
    OFF.mount();
  }
})();
