/* EkGuru — Visual Learning System v300
   Purpose: Add visuals to every language, country theme, age-based
   Features: Dotted tracing, illustrations, cultural motifs, SEO images
*/
(function () {
  "use strict";

  var VISUALS = {
    // Language-specific visual motifs
    languages: {
      hi: { script: 'Devanagari', motif: '🕉️', colors: ['#ff9933', '#138808'], pattern: 'mandala', example: 'नमस्ते' },
      ar: { script: 'Arabic', motif: '🕌', colors: ['#0f766e', '#eab308'], pattern: 'arabesque', example: 'مرحبا' },
      ja: { script: 'Hiragana/Kanji', motif: '🌸', colors: ['#bc002d', '#ffffff'], pattern: 'wave', example: 'こんにちは' },
      es: { script: 'Latin', motif: '💃', colors: ['#aa151b', '#f1bf00'], pattern: 'flamenco', example: 'Hola' },
      fr: { script: 'Latin', motif: '🗼', colors: ['#0055a4', '#ef4135'], pattern: 'fleur', example: 'Bonjour' },
      de: { script: 'Latin', motif: '🏰', colors: ['#000000', '#dd0000', '#ffce00'], pattern: 'geometric', example: 'Hallo' },
      zh: { script: 'Hanzi', motif: '🐉', colors: ['#de2910', '#ffde00'], pattern: 'dragon', example: '你好' },
      ru: { script: 'Cyrillic', motif: '🏛️', colors: ['#ffffff', '#0039a6', '#d52b1e'], pattern: 'matryoshka', example: 'Привет' }
    },
    
    // Country-specific visuals
    countries: {
      IN: { landmarks: ['Taj Mahal', 'Red Fort'], festivals: ['Diwali', 'Holi'], food: ['Biryani', 'Dosa'] },
      JP: { landmarks: ['Mount Fuji', 'Tokyo Tower'], festivals: ['Cherry Blossom', 'Obon'], food: ['Sushi', 'Ramen'] },
      DE: { landmarks: ['Brandenburg Gate', 'Neuschwanstein'], festivals: ['Oktoberfest'], food: ['Bratwurst', 'Pretzel'] },
      FR: { landmarks: ['Eiffel Tower', 'Louvre'], festivals: ['Bastille Day'], food: ['Croissant', 'Baguette'] }
    }
  };

  function createVisualCard(type, data) {
    var card = document.createElement('div');
    card.className = 'visual-card';
    
    var bgColor = data.colors ? data.colors[0] + '15' : '#f6f4ff';
    card.style.background = bgColor;
    
    card.innerHTML = 
      '<div style="height:120px;background:linear-gradient(135deg,' + (data.colors ? data.colors.join(',') : '#4f32d9,#8b5cf6') + ');display:grid;place-items:center;font-size:3rem;color:#fff;position:relative;overflow:hidden">' +
        '<span style="position:relative;z-index:1">' + (data.motif || '🌍') + '</span>' +
        '<div style="position:absolute;inset:0;background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.2),transparent 50%)"></div>' +
        '<span style="position:absolute;bottom:8px;right:8px;font-size:.7rem;background:rgba(0,0,0,.3);padding:2px 6px;border-radius:4px">' + (data.script || type) + '</span>' +
      '</div>' +
      '<div class="visual-card-content">' +
        '<b>' + (data.name || type) + ' ' + (data.example ? '(' + data.example + ')' : '') + '</b>' +
        '<span>' + (data.desc || 'Visual learning helps remember better') + '</span>' +
        (data.pattern ? '<small style="display:block;margin-top:6px;color:#8b7fb5;font-size:.75rem">Pattern: ' + data.pattern + '</small>' : '') +
      '</div>';
    
    return card;
  }

  function createDottedAlphabet(langCode) {
    var lang = VISUALS.languages[langCode] || VISUALS.languages.hi;
    var container = document.createElement('div');
    container.className = 'dotted-alphabet';
    container.style.cssText = 'margin:24px 0;padding:20px;border:1px solid #e6e1fb;border-radius:16px;background:#fff';
    
    var letters = [];
    if (langCode === 'hi') letters = "अआइईउऊएऐओऔकखगघ".split("");
    else if (langCode === 'ar') letters = "ابتثجحخدذرز".split("");
    else if (langCode === 'ja') letters = "あいうえおかきくけこ".split("");
    else letters = "ABCDEabcde".split("");
    
    container.innerHTML = 
      '<h3 style="margin:0 0 12px;display:flex;align-items:center;gap:8px"><span style="font-size:1.5rem">' + lang.motif + '</span> Trace & Learn: ' + lang.script + '</h3>' +
      '<p style="font-size:.9rem;color:#5f6577;margin:0 0 16px">Tap letters to practice writing. Dotted visuals help muscle memory!</p>' +
      '<div class="dotted-grid">' +
        letters.map(function(letter) {
          return '<button type="button" class="dotted-cell" data-letter="' + letter + '" aria-label="Trace letter ' + letter + '">' + letter + '</button>';
        }).join('') +
      '</div>' +
      '<div id="dotted-canvas-area" style="display:none;margin-top:16px;padding:16px;background:#f8f7fd;border-radius:12px;text-align:center">' +
        '<p style="margin:0 0 12px;font-weight:700">Trace: <span id="dotted-current" style="font-size:1.5rem;color:#4f32d9"></span></p>' +
        '<canvas id="dotted-canvas" width="300" height="200" style="border:2px dashed #d9d6e8;border-radius:12px;background:#fff;touch-action:none;cursor:crosshair;display:block;margin:0 auto;max-width:100%"></canvas>' +
        '<div style="margin-top:12px;display:flex;gap:8px;justify-content:center"><button type="button" class="btn btn-ghost btn-sm" id="dotted-clear">Clear</button><button type="button" class="btn btn-primary btn-sm" id="dotted-done">Done ✓</button></div>' +
      '</div>';
    
    // Add interaction
    setTimeout(function() {
      var cells = container.querySelectorAll('.dotted-cell');
      var canvasArea = container.querySelector('#dotted-canvas-area');
      var currentSpan = container.querySelector('#dotted-current');
      var canvas = container.querySelector('#dotted-canvas');
      if (!canvas) return;
      
      var ctx = canvas.getContext('2d');
      var drawing = false;
      
      cells.forEach(function(cell) {
        cell.addEventListener('click', function() {
          var letter = cell.getAttribute('data-letter');
          currentSpan.textContent = letter;
          canvasArea.style.display = 'block';
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          canvasArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
      });
      
      ctx.strokeStyle = '#4f32d9';
      ctx.lineWidth = 4;
      ctx.lineCap = 'round';
      
      function getPos(e) {
        var rect = canvas.getBoundingClientRect();
        var x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
        var y = (e.touches ? e.touches[0].clientY : e.clientY) - rect.top;
        return { x: x * (canvas.width / rect.width), y: y * (canvas.height / rect.height) };
      }
      
      canvas.addEventListener('mousedown', function(e) { drawing = true; var p = getPos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); });
      canvas.addEventListener('mousemove', function(e) { if (!drawing) return; var p = getPos(e); ctx.lineTo(p.x, p.y); ctx.stroke(); });
      canvas.addEventListener('mouseup', function() { drawing = false; });
      canvas.addEventListener('touchstart', function(e) { e.preventDefault(); drawing = true; var p = getPos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); });
      canvas.addEventListener('touchmove', function(e) { e.preventDefault(); if (!drawing) return; var p = getPos(e); ctx.lineTo(p.x, p.y); ctx.stroke(); });
      canvas.addEventListener('touchend', function() { drawing = false; });
      
      container.querySelector('#dotted-clear').addEventListener('click', function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      });
      
      container.querySelector('#dotted-done').addEventListener('click', function() {
        canvasArea.style.display = 'none';
        // Celebration
        var celebration = document.createElement('div');
        celebration.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#fff;border:2px solid #10b981;border-radius:16px;padding:20px;box-shadow:0 12px 40px rgba(0,0,0,.15);z-index:10000;text-align:center';
        celebration.innerHTML = '<div style="font-size:2rem">🎉</div><b>Great tracing!</b><br><small>Keep practicing handwriting</small>';
        document.body.appendChild(celebration);
        setTimeout(function() { if (celebration.parentNode) celebration.parentNode.removeChild(celebration); }, 2000);
      });
    }, 100);
    
    return container;
  }

  function enhanceLanguagePages() {
    var path = location.pathname;
    var langMatch = path.match(/\/languages\/([a-z]{2,3})\//);
    var langCode = langMatch ? langMatch[1] : null;
    
    if (!langCode) {
      langCode = document.documentElement.lang || 'hi';
      langCode = langCode.split('-')[0];
    }
    
    var main = document.querySelector('.art, .pw-legacy, .egc, main');
    if (!main) return;
    
    // Add visual learning section for A1-A2
    var isBeginner = location.pathname.indexOf('/a1/') >= 0 || location.pathname.indexOf('/A1') >= 0 || location.hash.toLowerCase().indexOf('a1') >= 0;
    if (isBeginner && !main.querySelector('.dotted-alphabet')) {
      var dotted = createDottedAlphabet(langCode);
      var firstH2 = main.querySelector('h2');
      if (firstH2) firstH2.parentNode.insertBefore(dotted, firstH2);
      else main.appendChild(dotted);
    }
    
    // Add country visuals
    var country = document.documentElement.getAttribute('data-country');
    if (country && VISUALS.countries[country] && !main.querySelector('.country-visual')) {
      var countryData = VISUALS.countries[country];
      var countryEl = document.createElement('div');
      countryEl.className = 'country-visual';
      countryEl.style.cssText = 'margin:20px 0;padding:16px;border-radius:12px;background:linear-gradient(135deg,#f6f4ff,#fff);border:1px solid #e6e1fb';
      countryEl.innerHTML = 
        '<h3 style="margin:0 0 10px">🌍 ' + country + ' Cultural Context</h3>' +
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;font-size:.85rem">' +
          '<div><b>Landmarks:</b><br>' + countryData.landmarks.join(', ') + '</div>' +
          '<div><b>Festivals:</b><br>' + countryData.festivals.join(', ') + '</div>' +
          '<div><b>Food:</b><br>' + countryData.food.join(', ') + '</div>' +
        '</div>';
      
      var h1 = main.querySelector('h1');
      if (h1) h1.parentNode.insertBefore(countryEl, h1.nextSibling);
    }
    
    // Add visual learning grid
    if (!main.querySelector('.visual-learning-grid') && (main.innerText || main.textContent || '').length > 500) {
      var langInfo = VISUALS.languages[langCode];
      if (langInfo) {
        var grid = document.createElement('div');
        grid.className = 'visual-learning-grid';
        grid.innerHTML = '<h3 style="grid-column:1/-1;margin:0">🎨 Visual Learning Aids</h3>';
        
        // Create 2-3 visual cards
        var card1 = createVisualCard('script', {
          name: langInfo.script + ' Script',
          example: langInfo.example,
          motif: langInfo.motif,
          colors: langInfo.colors,
          pattern: langInfo.pattern,
          desc: 'Learn through visual memory'
        });
        
        grid.appendChild(card1);
        
        var h2 = main.querySelectorAll('h2');
        if (h2.length > 1) {
          h2[1].parentNode.insertBefore(grid, h2[1]);
        }
      }
    }
  }

  function init() {
    enhanceLanguagePages();
    
    // Re-enhance on navigation
    window.addEventListener('hashchange', function() {
      setTimeout(enhanceLanguagePages, 500);
    });
    
    // Observe for new content
    if (window.MutationObserver) {
      var observer = new MutationObserver(function(mutations) {
        var shouldEnhance = false;
        mutations.forEach(function(m) {
          if (m.addedNodes.length > 0) {
            for (var i = 0; i < m.addedNodes.length; i++) {
              var node = m.addedNodes[i];
              if (node.nodeType === 1 && node.querySelector && node.querySelector('h1')) {
                shouldEnhance = true;
                break;
              }
            }
          }
        });
        if (shouldEnhance) setTimeout(enhanceLanguagePages, 300);
      });
      observer.observe(document.body, { childList: true, subtree: true });
    }

    window.EKGURU_VISUALS = {
      data: VISUALS,
      createCard: createVisualCard,
      createDotted: createDottedAlphabet
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
