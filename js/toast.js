/* EkGuru — toast + skeleton primitives (motion §23/§24).
   Dependency-free, no layout dependency, ES5-safe.

   Toasts: enter → remain → exit, short motion, click to dismiss,
   auto-dismiss after ~4.5s. The text is always in the DOM and the
   toast carries role="status" (role="alert" for errors), so success
   or failure is never communicated by animation alone — the message
   is announced to assistive tech even with motion turned off.

   Skeletons: used only where a real wait exists (admin live-health
   fetches). Under prefers-reduced-motion the shimmer is disabled and
   the block renders as a static neutral surface, so nothing flashes.
*/
(function () {
  "use strict";

  var prefersReduced = false;
  try {
    prefersReduced = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) { prefersReduced = false; }

  function stack() {
    var s = document.getElementById("ekg-toast-stack");
    if (s) return s;
    s = document.createElement("div");
    s.id = "ekg-toast-stack";
    s.className = "toast-stack";
    s.setAttribute("aria-live", "polite");
    document.body.appendChild(s);
    return s;
  }

  function show(message, kind) {
    if (message == null || message === "") return null;
    var t = document.createElement("div");
    t.className = "toast toast--" + (kind === "err" ? "err" : kind === "ok" ? "ok" : "info");
    t.setAttribute("role", kind === "err" ? "alert" : "status");
    t.textContent = String(message);
    stack().appendChild(t);

    /* enter (instant under reduced motion) */
    if (prefersReduced) {
      t.classList.add("is-in");
    } else {
      requestAnimationFrame(function () { t.classList.add("is-in"); });
    }

    function dismiss() {
      if (t._gone) return;
      t._gone = true;
      if (t._timer) clearTimeout(t._timer);
      if (prefersReduced) {
        if (t.parentNode) t.parentNode.removeChild(t);
      } else {
        t.classList.remove("is-in");
        t.classList.add("is-out");
        setTimeout(function () {
          if (t.parentNode) t.parentNode.removeChild(t);
        }, 260);
      }
    }
    t.addEventListener("click", dismiss);
    t._timer = setTimeout(dismiss, 4500);
    return t;
  }

  window.EkGuruToast = {
    show: show,
    info: function (m) { return show(m, "info"); },
    ok: function (m) { return show(m, "ok"); },
    err: function (m) { return show(m, "err"); }
  };
})();
