/* Hindi collection UI. Existing content, shared voice/SRS; no new storage or network. */
(function () {
  'use strict';
  function boot() {
    var root = document.querySelector('#hindi-learning-library');
    if (!root || root.dataset.ready) return;
    var data = window.EKGURU_HINDI_LIBRARY;
    if (!data || !Array.isArray(data.items) || !data.items.length) {
      var loading = root && root.querySelector('#hll-loading');
      if (loading) loading.textContent = 'The interactive collection could not load. Use the source lessons above.';
      return;
    }
    root.dataset.ready = 'true';
    var level = root.querySelector('#hll-level'), kind = root.querySelector('#hll-kind');
    var search = root.querySelector('#hll-search'), card = root.querySelector('#hll-card');
    var previous = root.querySelector('#hll-previous'), next = root.querySelector('#hll-next');
    var position = root.querySelector('#hll-position'), empty = root.querySelector('#hll-empty');
    var jump = root.querySelector('#hll-jump'), number = root.querySelector('#hll-number');
    var jumpNote = root.querySelector('#hll-jump-note');
    var items = [], index = 0;
    function element(tag, text, cls) {
      var el = document.createElement(tag);
      if (text !== undefined) el.textContent = text;
      if (cls) el.className = cls;
      return el;
    }
    function button(text, handler) {
      var el = element('button', text); el.type = 'button';
      if (handler) el.addEventListener('click', handler);
      return el;
    }
    function details(label, text, lang) {
      var el = element('details'), summary = element('summary', label), content = element('p', text);
      if (lang) content.lang = lang;
      el.append(summary, content); return el;
    }
    function listen(label, text) {
      var el = button(label);
      el.dataset.voiceText = text; el.dataset.voiceLang = 'hi';
      el.setAttribute('aria-label', label + ': ' + text);
      return el;
    }
    function stop() { if (window.EkGuruVoice) window.EkGuruVoice.stop(); }
    function sentenceBuilder(item) {
      var words = item.hi.split(/\s+/);
      if (words.length < 2 || words.length > 24) return;
      var box = element('section', undefined, 'hll-build'), heading = element('h4', 'Build the source model');
      box.append(heading, element('p', 'Choose the word buttons in order. This checks the printed model, not every valid Hindi word order. Select a chosen word again to remove it.'));
      var pool = element('div', undefined, 'hll-tiles'), preview = element('p', 'Your sentence appears here.', 'hll-preview');
      preview.lang = 'hi'; preview.setAttribute('aria-label', 'Your assembled sentence');
      pool.setAttribute('role', 'group'); pool.setAttribute('aria-label', 'Choose words in sentence order');
      var feedback = element('p', 'Choose all the words before checking.'); feedback.setAttribute('role', 'status');
      var selected = [], order = words.map(function (_, i) { return i; }); order.push(order.shift());
      function paint() {
        preview.textContent = selected.length ? selected.map(function (i) { return words[i]; }).join(' ') : 'Your sentence appears here.';
        pool.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(selected.indexOf(Number(b.dataset.word)) !== -1)); });
      }
      order.forEach(function (i) {
        var word = button(words[i], function () {
          var at = selected.indexOf(i); if (at < 0) selected.push(i); else selected.splice(at, 1);
          paint(); feedback.textContent = selected.length + ' of ' + words.length + ' words selected.';
        });
        word.lang = 'hi'; word.dataset.word = String(i); word.setAttribute('aria-pressed', 'false'); pool.append(word);
      });
      var check = button('Check model', function () {
        if (selected.length !== words.length) { feedback.textContent = 'Not checked: choose all the words first. Nothing has been scored.'; return; }
        var built = selected.map(function (i) { return words[i]; }).join(' ');
        feedback.textContent = built === item.hi ? 'You built the source model. Explain its meaning, then try reading it aloud.' : 'This differs from the source model. Compare with the printed Hindi above, then try again. Other word orders may be valid in context.';
      });
      var clear = button('Clear words', function () { selected = []; paint(); feedback.textContent = 'Words cleared. Try again at your own pace.'; pool.querySelector('button').focus(); });
      box.append(pool, preview, check, clear, feedback); card.append(box);
    }
    function meaningPractice(item) {
      // Ask about the printed source gloss, not every possible meaning of a word.
      var key = function (text) { return text.normalize('NFC').trim().toLowerCase(); };
      var candidates = data.items.filter(function (x) { return x.kind === 'word' && x.level === item.level && key(x.en) !== key(item.en); });
      var choices = [item], glosses = [key(item.en)];
      // Stable, distributed distractors make repeat attempts reproducible without a new store.
      var seed = parseInt(item.id.slice(-6), 16);
      for (var i = 0; i < candidates.length && choices.length < 4; i++) {
        var candidate = candidates[(seed + i) % candidates.length];
        var candidateKey = key(candidate.en);
        if (!glosses.some(function (gloss) { return gloss.indexOf(candidateKey) !== -1 || candidateKey.indexOf(gloss) !== -1; })) {
          choices.push(candidate); glosses.push(candidateKey);
        }
      }
      if (choices.length < 2) return;
      var offset = seed % choices.length;
      choices = choices.slice(offset).concat(choices.slice(0, offset));
      var box = element('section', undefined, 'hll-meaning');
      box.append(element('h4', 'Read and match'), element('p', 'Which English gloss does the source lesson use for this Hindi item? Try before opening the meaning. A word may have other meanings in other contexts.'));
      var group = element('fieldset'), legend = element('legend', 'Choose the source meaning');
      group.append(legend);
      choices.forEach(function (choice, i) {
        var label = element('label'), radio = element('input');
        radio.type = 'radio'; radio.name = 'hll-meaning-choice'; radio.value = String(i);
        label.append(radio, element('span', choice.en)); group.append(label);
      });
      var feedback = element('p', 'Choose an answer, then check. This practice does not save a score.');
      feedback.setAttribute('role', 'status');
      var check = button('Check meaning', function () {
        var selected = group.querySelector('input:checked');
        if (!selected) { feedback.textContent = 'Not checked: choose a meaning first.'; return; }
        feedback.textContent = choices[Number(selected.value)].id === item.id ? 'Matched the source meaning: ' + item.en + '. Try saying the Hindi, then use it in context.' : 'That is not the gloss used for this item in the source lesson. Try another choice, or open Show English meaning above.';
      });
      var clear = button('Clear meaning choice', function () {
        group.querySelectorAll('input').forEach(function (input) { input.checked = false; });
        feedback.textContent = 'Choice cleared. Try reading the Hindi again.'; group.querySelector('input').focus();
      });
      box.append(group, check, clear, feedback); card.append(box);
    }
    function render(focus) {
      stop(); card.replaceChildren();
      var item = items[index];
      empty.hidden = !!item; card.hidden = !item;
      previous.disabled = !item || index === 0; next.disabled = !item || index >= items.length - 1;
      number.disabled = !item; jump.querySelector('button').disabled = !item;
      number.max = String(items.length); number.value = item ? String(index + 1) : '';
      number.removeAttribute('aria-invalid');
      jumpNote.textContent = item ? 'Enter a whole number from 1 to ' + items.length + ' in this selection. No completion is recorded.' : 'Choose another filter or clear the search to navigate.';
      position.textContent = item ? item.level + ' · ' + item.kind + ' · Item ' + (index + 1) + ' of ' + items.length + ' in this selection. Opening is not completion.' : '0 matching items.';
      if (!item) return;
      card.dataset.itemId = item.id; card.dataset.kind = item.kind;
      card.append(element('h3', item.title));
      var hindi = element('p', item.hi, 'hll-hindi'); hindi.lang = 'hi'; hindi.dir = 'ltr'; card.append(hindi);
      card.append(listen(item.kind === 'paragraph' ? 'Listen to the whole paragraph' : 'Listen in Hindi', item.hi));
      if (item.kind === 'paragraph') {
        var lines = element('div', undefined, 'hll-sentence-audio');
        lines.append(element('p', 'Listen again, one sentence at a time:'));
        (item.hi.match(/[^।!?]+[।!?]*/g) || [item.hi]).forEach(function (text, i) { lines.append(listen('Listen to sentence ' + (i + 1), text.trim())); });
        card.append(lines);
      }
      card.append(details('Show romanisation', item.roman, 'hi-Latn'));
      card.append(details(item.kind === 'letter' ? 'Show the sound hint' : 'Show English meaning', item.en, 'en'));
      if (item.focus) card.append(element('p', 'Notice: ' + item.focus, 'hll-focus'));
      if (item.question) {
        var label = element('label', item.question), answer = element('textarea');
        answer.id = 'hll-response'; answer.rows = 3; answer.maxLength = 2000;
        label.htmlFor = answer.id; card.append(label, answer);
        card.append(element('p', 'Write or say your answer, then compare. This is a self-check, not automatic marking. Typed notes are not saved; moving to another item or changing a filter clears them.'));
        card.append(details('Compare with a model answer', item.answer));
      }
      if (item.kind === 'sentence') sentenceBuilder(item);
      if (item.kind === 'word') meaningPractice(item);
      var source = element('a', 'Open the full source lesson'); source.href = item.source;
      if (item.kind !== 'paragraph') card.append(source);
      var review = button('Add this item to my Hindi review', function () {
        var api = window.EkGuruGlobalSRS;
        if (!api) { reviewNote.textContent = 'Review is unavailable here. Your existing deck has not changed.'; return; }
        var result = api.add({ language: 'hi', prompt: item.hi, answer: item.en, target: item.hi,
          source: item.source, content_id: item.id, level: item.level, category: 'learning-library', skill: 'reading', srs_eligible: true });
        reviewNote.textContent = result.added ? 'Added to your existing Hindi review deck on this device.' : result.card && !result.reason ? 'This item is already in your Hindi review deck.' : 'Not added: ' + (result.reason || 'the deck could not be updated') + '. Existing data were preserved.';
      });
      var reviewNote = element('p'); reviewNote.setAttribute('role', 'status');
      card.append(review, reviewNote);
      if (window.EkGuruVoice) window.EkGuruVoice.mount(card);
      if (focus) card.focus();
    }
    function filter() {
      var q = search.value.trim().normalize('NFC').toLocaleLowerCase('en');
      items = data.items.filter(function (item) {
        return (level.value === 'all' || item.level === level.value) && (kind.value === 'all' || item.kind === kind.value) &&
          (!q || (item.hi + ' ' + item.en + ' ' + item.roman + ' ' + item.title).normalize('NFC').toLocaleLowerCase('en').indexOf(q) !== -1);
      });
      index = 0; render(false);
    }
    level.addEventListener('change', filter); kind.addEventListener('change', filter); search.addEventListener('input', filter);
    previous.addEventListener('click', function () { if (index > 0) { index--; render(true); } });
    next.addEventListener('click', function () { if (index < items.length - 1) { index++; render(true); } });
    root.querySelector('#hll-start').addEventListener('click', function () { level.value = 'all'; kind.value = 'all'; search.value = ''; filter(); card.focus(); });
    root.querySelector('#hll-readings').addEventListener('click', function () { level.value = 'all'; kind.value = 'paragraph'; search.value = ''; filter(); card.focus(); });
    jump.addEventListener('submit', function (event) {
      event.preventDefault();
      var value = number.value.trim(), target = Number(value);
      if (!value || !Number.isInteger(target) || target < 1 || target > items.length) {
        number.setAttribute('aria-invalid', 'true');
        jumpNote.textContent = 'Not moved: enter a whole number from 1 to ' + items.length + '.';
        number.focus(); return;
      }
      index = target - 1; render(true);
    });
    window.addEventListener('pagehide', stop);
    filter(); root.querySelector('#hll-loading').hidden = true; root.querySelector('#hll-app').hidden = false;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
