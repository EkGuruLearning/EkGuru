/* EkGuru — Level Visuals v301 (neutral ladder)
   A level describes what a learner can do — not what age they are.
   v300 keyed the visuals to age (A1 "Children (5-10)" -> C5 "Elders (75+)");
   that treated age as level eligibility and is gone. The banner now shows
   the level, its place on the eleven-level ladder (official CEFR vs EkGuru
   Extended Mastery) and what the level is for. No emojis, no age bands.
*/
(function () {
  "use strict";

  /* The eleven levels in the exact site order. cefr:false marks the EkGuru
     Extended Mastery levels — EkGuru's own extension, never official CEFR. */
  var LEVEL_META = {
    A1: { label: 'A1 · Beginner', band: 'start', cefr: true,  can: 'greet, count, read a shop sign' },
    A2: { label: 'A2 · Elementary', band: 'start', cefr: true,  can: 'talk about your day, shop, order food' },
    A3: { label: 'A3 · Independent everyday use', band: 'grow', cefr: false, can: 'hold everyday conversation without preparation' },
    B1: { label: 'B1 · Intermediate', band: 'grow', cefr: true,  can: 'explain a problem, write a message, follow a podcast' },
    B2: { label: 'B2 · Upper intermediate', band: 'mature', cefr: true,  can: 'read a newspaper, write a real letter, argue a point' },
    B3: { label: 'B3 · Mature fluency', band: 'mature', cefr: false, can: 'speak and write at length with precision' },
    C1: { label: 'C1 · Advanced', band: 'deep', cefr: true,  can: 'idiom, register, tone — and hear when it is wrong' },
    C2: { label: 'C2 · Mastery', band: 'deep', cefr: true,  can: 'poetry, law, humour, and the mistake that sounds foreign' },
    C3: { label: 'C3 · Specialization', band: 'expert', cefr: false, can: 'legal, medical, technical or literary language at depth' },
    C4: { label: 'C4 · Expert depth', band: 'expert', cefr: false, can: 'academic and professional writing, precise argument' },
    C5: { label: 'C5 · Teaching and mediation', band: 'expert', cefr: false, can: 'teach, translate and explain the language itself' }
  };

  var BAND_TINTS = {
    start:  ['#eef2ff', '#e0e7ff'],
    grow:   ['#ecfdf5', '#d1fae5'],
    mature: ['#fdf4ff', '#fae8ff'],
    deep:   ['#fffbeb', '#fef3c7'],
    expert: ['#f0f9ff', '#e0f2fe']
  };

  function getLevelFromPath() {
    var path = location.pathname.toLowerCase();
    var match = path.match(/\/(a1|a2|a3|b1|b2|b3|c1|c2|c3|c4|c5)\//);
    if (match) return match[1].toUpperCase();

    var hash = location.hash.toLowerCase();
    match = hash.match(/(a1|a2|a3|b1|b2|b3|c1|c2|c3|c4|c5)/);
    if (match) return match[1].toUpperCase();

    var el = document.querySelector('[data-level]');
    if (el) return el.getAttribute('data-level').toUpperCase();

    return null;
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* A neutral banner: the level, its rung on the ladder, and what it is for.
     No age, no emoji. Extended levels say so explicitly. */
  function createLevelVisual(level) {
    var info = LEVEL_META[level] || null;
    if (!info) return null;
    var tints = BAND_TINTS[info.band] || BAND_TINTS.start;
    var badge = info.cefr
      ? '<span style="font-size:.7rem;padding:3px 8px;border-radius:999px;background:rgba(255,255,255,.85);font-weight:700">Official CEFR level</span>'
      : '<span style="font-size:.7rem;padding:3px 8px;border-radius:999px;background:rgba(255,255,255,.85);font-weight:700">EkGuru Extended Mastery \u00b7 not CEFR</span>';

    var container = document.createElement('div');
    container.className = 'level-visual level-visual-' + level.toLowerCase();
    container.setAttribute('data-level', level);
    container.style.cssText = 'display:flex;align-items:center;gap:16px;padding:16px;border-radius:16px;background:linear-gradient(135deg,' + tints[0] + ',' + tints[1] + ');border:1px solid rgba(0,0,0,.06);margin:16px 0';

    container.innerHTML =
      '<div style="flex:none;font-size:1.6rem;font-weight:800;letter-spacing:.02em">' + level + '</div>' +
      '<div><b style="display:block;font-size:1rem">' + escapeHtml(info.label) + '</b>' +
      '<span style="font-size:.85rem;color:#4b5563">By the end of this level: ' + escapeHtml(info.can) + '. A learner of any age can study it.</span>' +
      '<div style="margin-top:6px;display:flex;gap:6px;flex-wrap:wrap">' + badge + '</div></div>';

    return container;
  }

  /* Kept from v300: a dotted tracing box for the first words of a lesson.
     It is a genuine writing practice for early levels; the emoji is gone. */
  function createDottedVisual(text, lang) {
    var container = document.createElement('div');
    container.className = 'dotted-visual';
    container.style.cssText = 'margin:20px 0;padding:20px;border:2px dashed #d9d6e8;border-radius:16px;background:repeating-linear-gradient(45deg,#f6f4ff,#f6f4ff 10px,#fff 10px,#fff 20px);text-align:center';

    var letters = String(text).split('');
    container.innerHTML =
      '<p style="font-size:.85rem;color:#5f6577;margin:0 0 12px">Trace the dotted letters:</p>' +
      '<div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">' +
        letters.map(function (letter) {
          if (letter.trim() === '') return '<span style="width:20px"></span>';
          return '<span style="font-size:2.2rem;font-weight:900;color:transparent;-webkit-text-stroke:2px #4f32d9;padding:8px 12px;border-radius:12px;background:#fff;border:1px solid #e6e1fb;min-width:48px;text-align:center;display:inline-block">' + escapeHtml(letter) + '</span>';
        }).join('') +
      '</div>' +
      '<p style="font-size:.8rem;color:#8b7fb5;margin:12px 0 0">Practice writing \u00b7 ' + escapeHtml(lang || 'this language') + '</p>';

    return container;
  }

  function enhanceLevelPages() {
    var level = getLevelFromPath();
    if (!level) return;

    var main = document.querySelector('.egc, .lv-main, .art, .pw-legacy');
    if (!main) return;

    // The built page already carries the level figure and copy; only add the
    // banner where the page does not have one yet.
    if (main.querySelector('.level-visual, .lv-fig')) return;

    var visual = createLevelVisual(level);
    if (!visual) return;
    var firstH1 = main.querySelector('h1');
    if (firstH1 && firstH1.parentNode) {
      firstH1.parentNode.insertBefore(visual, firstH1.nextSibling);
    } else {
      main.insertBefore(visual, main.firstChild);
    }

    // Tracing practice on the earliest authored levels only.
    if (['A1', 'A2'].indexOf(level) >= 0) {
      var vocab = main.querySelectorAll('.vocab, table');
      if (vocab.length > 0) {
        var firstWord = null;
        try {
          var rows = vocab[0].querySelectorAll('td');
          if (rows.length > 0) firstWord = rows[0].textContent.trim().slice(0, 10);
        } catch (e) {}

        if (firstWord && firstWord.length <= 10 && !main.querySelector('.dotted-visual')) {
          var h2 = main.querySelector('h2');
          var dotted = createDottedVisual(firstWord);
          if (h2) h2.parentNode.insertBefore(dotted, h2.nextSibling);
        }
      }
    }

    // Level identity on the container; no age attribute (v300 set data-age).
    main.classList.add('level-' + level.toLowerCase());
    document.documentElement.setAttribute('data-level', level);
  }

  function enhanceCourseCards() {
    document.querySelectorAll('.course-card[data-level]').forEach(function (card) {
      if (card.querySelector('.level-badge')) return;
      var level = card.getAttribute('data-level').toUpperCase();
      if (!LEVEL_META[level]) return;

      var badge = document.createElement('div');
      badge.className = 'level-badge';
      badge.style.cssText = 'position:absolute;top:8px;right:8px;font-size:.75rem;font-weight:800;background:rgba(255,255,255,.95);color:#1f2937;padding:4px 9px;border-radius:999px;box-shadow:0 2px 8px rgba(0,0,0,.12);z-index:2';
      badge.textContent = level;
      badge.title = LEVEL_META[level].label;

      card.style.position = 'relative';
      card.appendChild(badge);
    });
  }

  function init() {
    enhanceLevelPages();
    enhanceCourseCards();

    // Re-enhance on hash change (course player navigation)
    window.addEventListener('hashchange', function () {
      setTimeout(function () {
        enhanceLevelPages();
        enhanceCourseCards();
      }, 300);
    });

    // Watch for dynamically added content
    if (window.MutationObserver) {
      var observer = new MutationObserver(function (mutations) {
        var shouldEnhance = false;
        mutations.forEach(function (mutation) {
          if (mutation.addedNodes.length > 0) {
            for (var i = 0; i < mutation.addedNodes.length; i++) {
              var node = mutation.addedNodes[i];
              if (node.nodeType === 1 && (node.classList && node.classList.contains('egc') || (node.querySelector && node.querySelector('.egc')))) {
                shouldEnhance = true;
                break;
              }
            }
          }
        });
        if (shouldEnhance) {
          setTimeout(function () {
            enhanceLevelPages();
            enhanceCourseCards();
          }, 200);
        }
      });

      observer.observe(document.body, { childList: true, subtree: true });
    }

    window.EKGURU_LEVEL_VISUALS = {
      levels: LEVEL_META,
      getLevel: getLevelFromPath,
      createLevelVisual: createLevelVisual,
      createDottedVisual: createDottedVisual
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
