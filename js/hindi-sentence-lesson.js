/* Approved single-lesson pilot. No storage, network, score, microphone or library. */
(function () {
  "use strict";
  function boot() {
    var root = document.querySelector('[data-hindi-pilot="sentence"] .hsl-lesson');
    if (!root || root.dataset.hslReady) return;
    root.dataset.hslReady = "1";
    // Storybook generates TOC IDs. Retain the pilot's stable anchors and labels
    // without changing that shared owner or leaving its TOC links broken.
    root.querySelectorAll('[data-hsl-heading]').forEach(function (heading) {
      var oldId = heading.id, stableId = heading.dataset.hslHeading;
      root.querySelectorAll('.sb-toc a').forEach(function (link) {
        if (link.getAttribute('href') === '#' + oldId) link.setAttribute('href', '#' + stableId);
      });
      heading.id = stableId;
    });
    var contents = root.querySelector('.sb-toc');
    if (contents) contents.open = false;
    var controls = root.querySelector('.hsl-demo-controls');
    var note = root.querySelector('#hsl-demo-note');
    if (controls && note) {
      controls.querySelectorAll('[data-highlight]').forEach(function (button) {
        button.addEventListener('click', function () {
          var part = button.dataset.highlight;
          controls.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === button)); });
          root.querySelectorAll('.hsl-piece').forEach(function (p) { p.classList.toggle('is-active', p.dataset.part === part); });
          note.textContent = button.dataset.explanation;
        });
      });
      controls.hidden = false;
    }
    // Keep the existing storybook owner of card flipping; only expose its state.
    root.querySelectorAll('.vcard[data-sb-flip]').forEach(function (card) {
      function sync() { card.setAttribute('aria-pressed', String(card.classList.contains('flip'))); }
      sync();
      card.addEventListener('click', sync);
      card.addEventListener('keydown', function (e) { if (e.target === card && (e.key === 'Enter' || e.key === ' ')) sync(); });
      // A key on the nested native Listen button must not also flip the parent.
      card.addEventListener('keydown', function (e) { if (e.target !== card) e.stopPropagation(); }, true);
    });
    document.documentElement.classList.add('hsl-ready');
    var host = root.querySelector('#hsl-exercise');
    if (!host) return;
    var models = Array.from(root.querySelectorAll('[data-hsl-model]'));
    if (!models.length) return;
    var bank = host.querySelector('#hsl-bank'), answer = host.querySelector('#hsl-answer');
    var prompt = host.querySelector('#hsl-prompt'), progress = host.querySelector('#hsl-progress');
    var feedback = host.querySelector('#hsl-feedback'), next = host.querySelector('#hsl-next');
    var index = 0, selected = [], built = new Set();
    function current() { return models[index]; }
    function words() { return current().dataset.bank.split('|'); }
    function message(text, state) { feedback.textContent = text; feedback.dataset.state = state || 'hint'; }
    function updateProgress() {
      progress.textContent = 'Practice ' + (index + 1) + ' of ' + models.length + ' · ' + built.size + ' model' + (built.size === 1 ? '' : 's') + ' built in this visit. Not a proficiency score.';
    }
    function paint() {
      var pool = words();
      bank.querySelectorAll('button').forEach(function (button, i) { button.setAttribute('aria-pressed', String(selected.indexOf(i) !== -1)); });
      answer.replaceChildren();
      if (!selected.length) {
        var empty = document.createElement('p'); empty.textContent = 'Your sentence will appear here.'; answer.appendChild(empty);
      }
      selected.forEach(function (wordIndex, pos) {
        var tile = document.createElement('button'); tile.type = 'button'; tile.className = 'hsl-tile'; tile.lang = 'hi';
        tile.textContent = pool[wordIndex]; tile.setAttribute('aria-label', 'Remove word ' + (pos + 1) + ': ' + pool[wordIndex]);
        tile.addEventListener('click', function () {
          selected.splice(pos, 1); paint();
          var replacements = answer.querySelectorAll('button');
          if (replacements.length) replacements[Math.min(pos, replacements.length - 1)].focus();
          else bank.querySelector('button').focus();
          message('Word removed. Choose a word to keep building.');
        });
        answer.appendChild(tile);
      });
    }
    function load() {
      selected = []; bank.replaceChildren(); prompt.textContent = current().dataset.prompt;
      words().forEach(function (word, i) {
        var button = document.createElement('button'); button.type = 'button'; button.className = 'hsl-tile'; button.lang = 'hi';
        button.textContent = word; button.setAttribute('aria-pressed', 'false');
        button.addEventListener('click', function () {
          var at = selected.indexOf(i);
          if (at === -1) selected.push(i); else selected.splice(at, 1);
          paint(); message('Selected ' + selected.length + ' of ' + words().length + ' words. Check when you are ready.');
        });
        bank.appendChild(button);
      });
      next.textContent = index === models.length - 1 ? 'Back to first practice' : 'Next practice';
      paint(); updateProgress(); message('Choose words in the neutral order taught above. You can remove a word or clear your attempt.');
    }
    host.querySelector('#hsl-check').addEventListener('click', function () {
      if (selected.length !== words().length) { message('Not checked yet: choose all ' + words().length + ' words first. Nothing has been scored.', 'retry'); return; }
      var typed = selected.map(function (i) { return words()[i]; }).join(' ');
      var model = current().querySelector('[lang="hi"]').textContent.trim().replace(/।$/, '');
      if (typed === model) {
        built.add(index); updateProgress();
        message('Model built: ' + model + '। ' + current().dataset.explanation, 'correct');
      } else {
        message('Try the neutral pattern for this exercise: ' + current().dataset.explanation + ' Other word orders can occur in Hindi; this task practises the model above.', 'retry');
      }
    });
    host.querySelector('#hsl-clear').addEventListener('click', function () { selected = []; paint(); message('Attempt cleared. Models already built in this visit are unchanged.'); bank.querySelector('button').focus(); });
    host.querySelector('#hsl-reveal').addEventListener('click', function () {
      message('Model answer: ' + current().querySelector('[lang="hi"]').textContent.trim() + ' ' + current().dataset.explanation + ' Revealing does not mark the model as built.');
    });
    next.addEventListener('click', function () { index = (index + 1) % models.length; load(); prompt.focus(); });
    load(); host.hidden = false;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
