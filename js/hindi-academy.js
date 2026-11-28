(function () {
  'use strict';
  var size = document.querySelector('[data-size]');
  if (size) {
    try { if (localStorage.getItem('ekguru-academy-large') === '1') document.body.classList.add('large'); } catch (_) {}
    function sizeLabel() { size.textContent = document.body.classList.contains('large') ? 'Use standard text' : 'Use larger text'; }
    sizeLabel();
    size.addEventListener('click', function () { document.body.classList.toggle('large'); try { localStorage.setItem('ekguru-academy-large', document.body.classList.contains('large') ? '1' : '0'); } catch (_) {} sizeLabel(); });
  }
  var print = document.querySelector('[data-print]'); if (print) print.addEventListener('click', function () { window.print(); });
  var status = document.getElementById('audio-status');
  document.querySelectorAll('[data-speak]').forEach(function (btn) { btn.addEventListener('click', function () {
    var voice = window.EkGuruVoice;
    if (!voice || !voice.available('hi-IN', btn.dataset.speak)) { status.textContent = 'No Hindi voice is available on this device. Add a Hindi system voice or use the written examples.'; return; }
    var started = voice.speak(btn.dataset.speak, 'hi-IN', Number(document.getElementById('speed').value), function (ok) {
      if (ok === false) status.textContent = 'Hindi audio could not play on this device.';
    }, btn);
    status.textContent = started ? 'Playing Hindi audio. Device speech is synthesized and pronunciation may vary.' : 'Hindi audio could not play on this device.';
  }); });
  var stop = document.getElementById('stop-audio'); if (stop) stop.addEventListener('click', function () { if (window.EkGuruVoice) window.EkGuruVoice.stop(); status.textContent = 'Audio stopped.'; });
  var canvas = document.getElementById('trace');
  if (canvas) {
    var ctx = canvas.getContext('2d'), strokes = [], active = null, guide = document.getElementById('trace-model');
    function redraw() { ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.lineWidth = 8; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = '#5033c4'; strokes.forEach(function (stroke) { ctx.beginPath(); stroke.forEach(function (p, i) { if (!i) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y); }); if (stroke.length === 1) ctx.lineTo(stroke[0].x + 0.01, stroke[0].y); ctx.stroke(); }); }
    function point(e) { var r = canvas.getBoundingClientRect(); return { x: (e.clientX - r.left) * canvas.width / r.width, y: (e.clientY - r.top) * canvas.height / r.height }; }
    canvas.addEventListener('pointerdown', function (e) { if (active !== null) return; active = e.pointerId; canvas.setPointerCapture(e.pointerId); strokes.push([point(e)]); redraw(); });
    canvas.addEventListener('pointermove', function (e) { if (active !== e.pointerId) return; strokes[strokes.length - 1].push(point(e)); redraw(); });
    function end(e) { if (active === e.pointerId) active = null; }
    canvas.addEventListener('pointerup', end); canvas.addEventListener('pointercancel', end); canvas.addEventListener('lostpointercapture', end);
    document.getElementById('undo').addEventListener('click', function () { strokes.pop(); redraw(); });
    document.getElementById('clear').addEventListener('click', function () { strokes = []; redraw(); });
    document.getElementById('letter').addEventListener('change', function (e) { guide.textContent = e.target.value; strokes = []; redraw(); });
    document.getElementById('toggle-model').addEventListener('click', function () { var show = guide.hidden; guide.hidden = !show; this.setAttribute('aria-pressed', String(show)); this.textContent = show ? 'Hide guide' : 'Show guide'; });
  }
  var quiz = document.getElementById('quiz');
  if (quiz) {
    quiz.addEventListener('submit', function (e) { e.preventDefault(); var total = 0, answered = 0; quiz.querySelectorAll('fieldset').forEach(function (f) { var checked = f.querySelector('input:checked'), fb = f.querySelector('.feedback'); if (!checked) { fb.textContent = 'Choose an answer first.'; return; } answered++; var correct = checked.value === f.dataset.answer; if (correct) total++; fb.textContent = correct ? 'Correct.' : 'Not quite. Review the answer key and try again.'; }); document.getElementById('quiz-result').textContent = answered === 3 ? total + ' of 3 correct. Review the explanations below.' : 'Answer all three questions to see your score.'; if (answered === 3 && window.EkGuruProgress) window.EkGuruProgress.recordQuiz('academy-vowels', total, 3); });
    quiz.addEventListener('reset', function () { quiz.querySelectorAll('.feedback').forEach(function (f) { f.textContent = ''; }); document.getElementById('quiz-result').textContent = ''; });
  }
})();
