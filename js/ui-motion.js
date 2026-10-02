/* EkGuru v2: small optional motion and appearance, with keyboard/reduced-motion fallbacks. */
(function () {
  'use strict';
  if (window.EkGuruUI) return;
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var dark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var confetti = null, timer = null, frame = null;
  function theme(value) {
    if (['system', 'light', 'dark', 'contrast'].indexOf(value) < 0) value = 'system';
    document.documentElement.setAttribute('data-theme', value === 'system' ? (dark && dark.matches ? 'dark' : 'light') : value);
    document.querySelectorAll('[data-eg-theme]').forEach(function (s) { s.value = value; });
    try { localStorage.setItem('ekguru:theme:v2', value); } catch (_) {}
  }
  function readTheme() { try { return localStorage.getItem('ekguru:theme:v2') || 'system'; } catch (_) { return 'system'; } }
  function stop() {
    if (timer) clearTimeout(timer); if (frame) cancelAnimationFrame(frame);
    if (confetti) confetti.remove(); confetti = null; timer = null; frame = null;
  }
  function celebrate() {
    if (mq && mq.matches) { toast('Level complete. Celebration animation is disabled by reduced motion.'); return; }
    stop();
    var c = document.createElement('canvas'); c.className = 'eg-confetti'; c.setAttribute('aria-hidden', 'true');
    c.width = window.innerWidth; c.height = window.innerHeight;
    document.body.appendChild(c); confetti = c;
    c.addEventListener('click', stop);
    var ctx = c.getContext('2d'); if (!ctx) { stop(); return; }
    var colors = ['#5130aa', '#075985', '#0f6b48', '#9d174d', '#92400e'];
    var dots = Array.from({ length: 48 }, function (_, i) { return { x: c.width * Math.random(), y: -Math.random() * 150, v: 2 + Math.random() * 4, color: colors[i % colors.length] }; });
    function draw() {
      if (confetti !== c) return;
      ctx.clearRect(0, 0, c.width, c.height);
      dots.forEach(function (d) { d.y += d.v; ctx.fillStyle = d.color; ctx.fillRect(d.x, d.y, 5, 8); });
      frame = requestAnimationFrame(draw);
    }
    draw(); timer = setTimeout(stop, 1500);
  }
  function toast(message) {
    var old = document.querySelector('.eg-toast'); if (old) old.remove();
    var el = document.createElement('div'); el.className = 'eg-toast'; el.setAttribute('role', 'status');
    el.textContent = String(message).slice(0, 300); document.body.appendChild(el);
    setTimeout(function () { el.remove(); }, 5000);
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') stop(); });
  function boot() {
    theme(readTheme());
    document.querySelectorAll('[data-eg-theme]').forEach(function (s) { s.addEventListener('change', function () { theme(s.value); }); });
    document.querySelectorAll('[data-eg-flip]').forEach(function (b) {
      b.addEventListener('click', function () {
        var back = b.querySelector('[data-eg-back]'), front = b.querySelector('[data-eg-front]'), show = b.getAttribute('aria-pressed') !== 'true';
        b.setAttribute('aria-pressed', String(show)); if (back) back.hidden = !show; if (front) front.hidden = show;
      });
    });
    document.querySelectorAll('[data-eg-confetti]').forEach(function (b) { b.addEventListener('click', celebrate); });
    document.querySelectorAll('[data-eg-toast]').forEach(function (b) { b.addEventListener('click', function () { toast(b.getAttribute('data-eg-toast')); }); });
    document.querySelectorAll('[data-eg-stroke-play]').forEach(function (b) {
      b.addEventListener('click', function () {
        var svg = document.getElementById(b.getAttribute('data-eg-stroke-play')); if (!svg) return;
        svg.removeAttribute('data-animating');
        if (!(mq && mq.matches)) { void svg.getBoundingClientRect(); svg.setAttribute('data-animating', '1'); }
      });
    });
    if ('IntersectionObserver' in window && !(mq && mq.matches)) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('eg-enter'); observer.unobserve(x.target); } });
      }, { threshold: .05 });
      document.querySelectorAll('[data-eg-reveal]').forEach(function (el) { observer.observe(el); });
    }
  }
  if (dark && dark.addEventListener) dark.addEventListener('change', function () { if (readTheme() === 'system') theme('system'); });
  if (mq && mq.addEventListener) mq.addEventListener('change', function () { if (mq.matches) stop(); });
  window.addEventListener('pagehide', stop);
  window.EkGuruUI = { theme: theme, toast: toast, celebrate: celebrate, stop: stop };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
