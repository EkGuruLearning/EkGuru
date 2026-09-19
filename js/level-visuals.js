/* EkGuru — Level Visuals with Age Progression v300
   A1 children's visuals -> C5 old man/woman visuals
   Country theme visuals, language-specific imagery
   Dotted tracing visuals for learning
*/
(function () {
  "use strict";

  var LEVEL_AGES = {
    A1: { age: 'child', emoji: '👶', label: 'Children (5-10)', desc: 'Playful, colorful, simple', colors: ['#fef3c7', '#fde68a'] },
    A2: { age: 'teen', emoji: '🧒', label: 'Kids (10-14)', desc: 'Fun, energetic, curious', colors: ['#d1fae5', '#a7f3d0'] },
    A3: { age: 'young', emoji: '👦', label: 'Young Teens (14-18)', desc: 'Learning, exploring', colors: ['#dbeafe', '#bfdbfe'] },
    B1: { age: 'adult-young', emoji: '🧑', label: 'Young Adults (18-30)', desc: 'Confident, social', colors: ['#e0e7ff', '#c7d2fe'] },
    B2: { age: 'adult', emoji: '👨', label: 'Adults (30-50)', desc: 'Professional, experienced', colors: ['#ede9fe', '#ddd6fe'] },
    B3: { age: 'adult-mature', emoji: '👨‍💼', label: 'Mature Adults (50-65)', desc: 'Wise, accomplished', colors: ['#fce7f3', '#fbcfe8'] },
    C1: { age: 'senior-young', emoji: '👴', label: 'Seniors (65-75)', desc: 'Knowledgeable, storytelling', colors: ['#f3f4f6', '#e5e7eb'] },
    C2: { age: 'senior', emoji: '👵', label: 'Elders (75+)', desc: 'Mastery, wisdom, heritage', colors: ['#fefce8', '#fef9c6'] },
    C3: { age: 'master', emoji: '🧙', label: 'Masters', desc: 'Deep cultural knowledge', colors: ['#ecfdf5', '#d1fae5'] },
    C4: { age: 'scholar', emoji: '👨‍🏫', label: 'Scholars', desc: 'Academic, research', colors: ['#eff6ff', '#dbeafe'] },
    C5: { age: 'guru', emoji: '🙏', label: 'Gurus', desc: 'Teaching, spiritual, complete mastery', colors: ['#fdf4ff', '#fae8ff'] }
  };

  var COUNTRY_THEMES = {
    'IN': { name: 'India', colors: ['#ff9933', '#ffffff', '#138808'], motif: '🕉️', pattern: 'paisley' },
    'JP': { name: 'Japan', colors: ['#bc002d', '#ffffff'], motif: '🌸', pattern: 'wave' },
    'DE': { name: 'Germany', colors: ['#000000', '#dd0000', '#ffce00'], motif: '🏰', pattern: 'geometric' },
    'FR': { name: 'France', colors: ['#0055a4', '#ffffff', '#ef4135'], motif: '🗼', pattern: 'fleur' },
    'ES': { name: 'Spain', colors: ['#aa151b', '#f1bf00'], motif: '💃', pattern: 'flamenco' },
    'BR': { name: 'Brazil', colors: ['#009b3a', '#fedf00', '#002776'], motif: '⚽', pattern: 'tropical' },
    'AE': { name: 'UAE', colors: ['#00732f', '#ffffff', '#000000', '#ff0000'], motif: '🕌', pattern: 'arabesque' },
    'US': { name: 'USA', colors: ['#b22234', '#ffffff', '#3c3b6e'], motif: '🗽', pattern: 'stars' }
  };

  function getLevelFromPath() {
    var path = location.pathname.toLowerCase();
    var match = path.match(/\/(a1|a2|a3|b1|b2|b3|c1|c2|c3|c4|c5)\//);
    if (match) return match[1].toUpperCase();
    
    var hash = location.hash.toLowerCase();
    match = hash.match(/(a1|a2|a3|b1|b2|b3|c1|c2|c3|c4|c5)/);
    if (match) return match[1].toUpperCase();
    
    // Check data attribute
    var el = document.querySelector('[data-level]');
    if (el) return el.getAttribute('data-level').toUpperCase();
    
    return null;
  }

  function getCountryFromPath() {
    var html = document.documentElement;
    var country = html.getAttribute('data-country');
    if (country) return country;
    
    var path = location.pathname.toLowerCase();
    var aliases = {
      india: "IN", japan: "JP", germany: "DE", france: "FR", spain: "ES",
      brazil: "BR", uae: "AE", usa: "US", uk: "GB", australia: "AU"
    };
    for (var slug in aliases) {
      if (path.indexOf(slug) >= 0) return aliases[slug];
    }
    return null;
  }

  function createAgeVisual(level) {
    var info = LEVEL_AGES[level] || LEVEL_AGES.A1;
    var container = document.createElement('div');
    container.className = 'age-visual age-visual-' + level.toLowerCase();
    container.setAttribute('data-level', level);
    container.setAttribute('data-age', info.age);
    container.style.cssText = 'display:flex;align-items:center;gap:16px;padding:16px;border-radius:16px;background:linear-gradient(135deg,' + info.colors[0] + ',' + info.colors[1] + ');border:1px solid rgba(0,0,0,.06);margin:16px 0';
    
    container.innerHTML = 
      '<div style="font-size:2.5rem;flex:none">' + info.emoji + '</div>' +
      '<div><b style="display:block;font-size:1rem">' + level + ' • ' + info.label + '</b>' +
      '<span style="font-size:.85rem;color:#4b5563">' + info.desc + '</span>' +
      '<div style="margin-top:6px;display:flex;gap:6px"><span style="font-size:.7rem;padding:3px 8px;border-radius:999px;background:rgba(255,255,255,.7);font-weight:700">' + info.age + '</span><span style="font-size:.7rem;padding:3px 8px;border-radius:999px;background:rgba(255,255,255,.7)">Visual learning</span></div></div>';
    
    return container;
  }

  function createCountryVisual(countryCode) {
    var theme = COUNTRY_THEMES[countryCode] || { name: countryCode, colors: ['#4f32d9', '#8b5cf6'], motif: '🌍', pattern: 'global' };
    var container = document.createElement('div');
    container.className = 'country-visual country-' + countryCode.toLowerCase();
    container.style.cssText = 'padding:20px;border-radius:16px;background:linear-gradient(135deg,' + theme.colors[0] + '15,' + (theme.colors[1] || '#fff') + ');border:1px solid ' + theme.colors[0] + '30;margin:16px 0;position:relative;overflow:hidden';
    
    container.innerHTML = 
      '<div style="position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,' + theme.colors.join(',') + ')"></div>' +
      '<div style="display:flex;align-items:center;gap:12px"><span style="font-size:2rem">' + theme.motif + '</span><div><b>' + theme.name + ' Theme</b><br><small style="color:#5f6577">' + theme.pattern + ' pattern • Cultural visuals</small></div></div>' +
      '<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">' + theme.colors.map(function(c) { return '<span style="width:24px;height:24px;border-radius:50%;background:' + c + ';border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.1);display:inline-block"></span>'; }).join('') + '</div>';
    
    return container;
  }

  function createDottedVisual(text, lang) {
    var container = document.createElement('div');
    container.className = 'dotted-visual';
    container.style.cssText = 'margin:20px 0;padding:20px;border:2px dashed #d9d6e8;border-radius:16px;background:repeating-linear-gradient(45deg,#f6f4ff,#f6f4ff 10px,#fff 10px,#fff 20px);text-align:center';
    
    var letters = text.split('');
    container.innerHTML = 
      '<p style="font-size:.85rem;color:#5f6577;margin:0 0 12px">✏️ Trace the dotted letters:</p>' +
      '<div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">' +
        letters.map(function(letter) {
          if (letter.trim() === '') return '<span style="width:20px"></span>';
          return '<span style="font-size:2.2rem;font-weight:900;color:transparent;-webkit-text-stroke:2px #4f32d9;padding:8px 12px;border-radius:12px;background:#fff;border:1px solid #e6e1fb;min-width:48px;text-align:center;display:inline-block">' + letter + '</span>';
        }).join('') +
      '</div>' +
      '<p style="font-size:.8rem;color:#8b7fb5;margin:12px 0 0">Practice writing • Visual learning • ' + (lang || 'Hindi') + '</p>';
    
    return container;
  }

  function enhanceLevelPages() {
    var level = getLevelFromPath();
    if (!level) return;
    
    var main = document.querySelector('.egc, .lv-main, .art, .pw-legacy');
    if (!main) return;
    
    // Don't add if already exists
    if (main.querySelector('.age-visual')) return;
    
    var ageVisual = createAgeVisual(level);
    var firstH1 = main.querySelector('h1');
    if (firstH1 && firstH1.parentNode) {
      firstH1.parentNode.insertBefore(ageVisual, firstH1.nextSibling);
    } else {
      main.insertBefore(ageVisual, main.firstChild);
    }
    
    // Add dotted visuals for A1-A2
    if (['A1', 'A2', 'A3'].indexOf(level) >= 0) {
      var vocab = main.querySelectorAll('.vocab, table');
      if (vocab.length > 0) {
        var firstWord = null;
        try {
          var rows = vocab[0].querySelectorAll('td');
          if (rows.length > 0) firstWord = rows[0].textContent.trim().slice(0, 10);
        } catch (e) {}
        
        if (firstWord) {
          var dotted = createDottedVisual(firstWord);
          var h2 = main.querySelector('h2');
          if (h2) h2.parentNode.insertBefore(dotted, h2.nextSibling);
        }
      }
    }
    
    // Add country theme if applicable
    var country = getCountryFromPath();
    if (country && COUNTRY_THEMES[country]) {
      var countryVisual = createCountryVisual(country);
      if (firstH1 && firstH1.parentNode) {
        firstH1.parentNode.insertBefore(countryVisual, ageVisual.nextSibling);
      }
    }
    
    // Set level class on container
    main.classList.add('level-' + level.toLowerCase());
    main.classList.add('age-' + (LEVEL_AGES[level] ? LEVEL_AGES[level].age : 'child'));
    document.documentElement.setAttribute('data-level', level);
    document.documentElement.setAttribute('data-age', LEVEL_AGES[level] ? LEVEL_AGES[level].age : 'child');
  }

  function enhanceCourseCards() {
    document.querySelectorAll('.course-card').forEach(function(card) {
      if (card.querySelector('.age-indicator')) return;
      
      var level = card.getAttribute('data-level') || 'A1';
      var info = LEVEL_AGES[level.toUpperCase()] || LEVEL_AGES.A1;
      
      var indicator = document.createElement('div');
      indicator.className = 'age-indicator';
      indicator.style.cssText = 'position:absolute;top:8px;right:8px;font-size:1.2rem;background:rgba(255,255,255,.9);width:32px;height:32px;border-radius:50%;display:grid;place-items:center;box-shadow:0 2px 8px rgba(0,0,0,.1);z-index:2';
      indicator.textContent = info.emoji;
      indicator.title = level + ' • ' + info.label;
      
      card.style.position = 'relative';
      card.appendChild(indicator);
    });
  }

  function init() {
    enhanceLevelPages();
    enhanceCourseCards();
    
    // Re-enhance on hash change (course player navigation)
    window.addEventListener('hashchange', function() {
      setTimeout(function() {
        enhanceLevelPages();
        enhanceCourseCards();
      }, 300);
    });
    
    // Watch for dynamically added content
    if (window.MutationObserver) {
      var observer = new MutationObserver(function(mutations) {
        var shouldEnhance = false;
        mutations.forEach(function(mutation) {
          if (mutation.addedNodes.length > 0) {
            for (var i = 0; i < mutation.addedNodes.length; i++) {
              var node = mutation.addedNodes[i];
              if (node.nodeType === 1 && (node.classList.contains('egc') || node.querySelector && node.querySelector('.egc'))) {
                shouldEnhance = true;
                break;
              }
            }
          }
        });
        if (shouldEnhance) {
          setTimeout(function() {
            enhanceLevelPages();
            enhanceCourseCards();
          }, 200);
        }
      });
      
      observer.observe(document.body, { childList: true, subtree: true });
    }

    window.EKGURU_LEVEL_VISUALS = {
      ages: LEVEL_AGES,
      countries: COUNTRY_THEMES,
      getLevel: getLevelFromPath,
      getCountry: getCountryFromPath,
      createAgeVisual: createAgeVisual,
      createCountryVisual: createCountryVisual,
      createDottedVisual: createDottedVisual
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
