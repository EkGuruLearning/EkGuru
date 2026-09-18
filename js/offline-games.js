/* EkGuru — Offline Games for Children v300
   Purpose: Engaging games when offline, so children don't lose interest
   Games: Memory match, word scramble, dotted tracing, alphabet puzzle
   Works: Fully offline, no network needed, cached by service worker
*/
(function () {
  "use strict";

  var GAMES = [
    {
      id: 'memory',
      name: 'Memory Match',
      emoji: '🧠',
      desc: 'Match Hindi letters and words',
      age: 'A1-A2',
      color: '#fef3c7'
    },
    {
      id: 'scramble',
      name: 'Word Scramble',
      emoji: '🔤',
      desc: 'Unscramble Hindi words',
      age: 'A1-B1',
      color: '#d1fae5'
    },
    {
      id: 'trace',
      name: 'Trace & Draw',
      emoji: '✏️',
      desc: 'Trace dotted letters',
      age: 'A1-A2',
      color: '#dbeafe'
    },
    {
      id: 'puzzle',
      name: 'Alphabet Puzzle',
      emoji: '🧩',
      desc: 'Put letters in order',
      age: 'A1',
      color: '#fce7f3'
    },
    {
      id: 'quiz',
      name: 'Quick Quiz',
      emoji: '🎯',
      desc: 'Fast vocabulary quiz',
      age: 'A2-B2',
      color: '#e0e7ff'
    }
  ];

  var HINDI_LETTERS = "अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह".split("");
  var HINDI_WORDS = [
    { hi: "नमस्ते", en: "Hello", roman: "namaste" },
    { hi: "धन्यवाद", en: "Thank you", roman: "dhanyavaad" },
    { hi: "पानी", en: "Water", roman: "paani" },
    { hi: "घर", en: "House", roman: "ghar" },
    { hi: "दोस्त", en: "Friend", roman: "dost" },
    { hi: "प्यार", en: "Love", roman: "pyaar" },
    { hi: "खुशी", en: "Happiness", roman: "khushi" },
    { hi: "सूरज", en: "Sun", roman: "sooraj" }
  ];

  function createGameContainer() {
    if (document.getElementById('ekguru-offline-game')) return document.getElementById('ekguru-offline-game');
    
    var container = document.createElement('div');
    container.id = 'ekguru-offline-game';
    container.className = 'google-anno-skip';
    container.setAttribute('role', 'dialog');
    container.setAttribute('aria-label', 'Offline games');
    container.innerHTML = 
      '<div class="offline-game-header"><b>🎮 Offline Fun Zone</b><button type="button" class="offline-game-close" aria-label="Close">×</button></div>' +
      '<p style="font-size:.85rem;color:#5f6577;margin:0 0 12px">You\'re offline! Play and keep learning ❤️</p>' +
      '<div id="offline-game-list" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px"></div>' +
      '<div id="offline-game-play" style="display:none"></div>' +
      '<div class="offline-game-score"><span id="offline-score">Score: 0</span><span id="offline-level">A1 • Child</span></div>' +
      '<div class="offline-game-actions"><button type="button" class="btn btn-ghost btn-sm" id="offline-back" style="display:none">← Back</button><button type="button" class="btn btn-primary btn-sm" id="offline-new">New Game</button></div>';
    
    document.body.appendChild(container);
    
    container.querySelector('.offline-game-close').addEventListener('click', function() {
      container.classList.remove('show');
    });
    
    container.querySelector('#offline-back').addEventListener('click', function() {
      showGameList();
    });
    
    container.querySelector('#offline-new').addEventListener('click', function() {
      var current = container.getAttribute('data-current');
      if (current) startGame(current);
      else showGameList();
    });
    
    return container;
  }

  function showGameList() {
    var container = createGameContainer();
    var list = container.querySelector('#offline-game-list');
    var play = container.querySelector('#offline-game-play');
    var back = container.querySelector('#offline-back');
    
    list.style.display = 'grid';
    play.style.display = 'none';
    back.style.display = 'none';
    container.removeAttribute('data-current');
    
    list.innerHTML = GAMES.map(function(game) {
      return '<button type="button" class="offline-game-card" data-game="' + game.id + '" style="border:1px solid #e4e4ef;border-radius:14px;padding:12px;background:' + game.color + ';text-align:center;cursor:pointer;transition:.2s;min-height:80px">' +
        '<div style="font-size:1.8rem">' + game.emoji + '</div>' +
        '<b style="display:block;font-size:.9rem;margin:4px 0">' + game.name + '</b>' +
        '<small style="font-size:.7rem;color:#5f6577">' + game.desc + '<br>' + game.age + '</small>' +
      '</button>';
    }).join('');
    
    list.querySelectorAll('.offline-game-card').forEach(function(btn) {
      btn.addEventListener('click', function() {
        startGame(btn.getAttribute('data-game'));
      });
    });
  }

  function startGame(gameId) {
    var container = createGameContainer();
    var list = container.querySelector('#offline-game-list');
    var play = container.querySelector('#offline-game-play');
    var back = container.querySelector('#offline-back');
    
    list.style.display = 'none';
    play.style.display = 'block';
    back.style.display = 'inline-flex';
    container.setAttribute('data-current', gameId);
    
    var game = GAMES.find(function(g) { return g.id === gameId; });
    if (!game) return;
    
    container.querySelector('#offline-level').textContent = game.age + ' • ' + game.name;
    
    switch (gameId) {
      case 'memory': renderMemoryGame(play); break;
      case 'scramble': renderScrambleGame(play); break;
      case 'trace': renderTraceGame(play); break;
      case 'puzzle': renderPuzzleGame(play); break;
      case 'quiz': renderQuizGame(play); break;
      default: showGameList();
    }
  }

  function renderMemoryGame(container) {
    var letters = HINDI_LETTERS.slice(0, 8);
    var cards = [];
    letters.forEach(function(letter) {
      cards.push({ id: letter + '_1', text: letter, matched: false });
      cards.push({ id: letter + '_2', text: letter, matched: false });
    });
    // Shuffle
    for (var i = cards.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = cards[i]; cards[i] = cards[j]; cards[j] = temp;
    }
    
    var flipped = [];
    var matched = 0;
    var score = 0;
    
    function render() {
      container.innerHTML = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">' +
        cards.map(function(card, idx) {
          var isFlipped = flipped.indexOf(idx) >= 0 || card.matched;
          return '<button type="button" class="offline-game-cell ' + (isFlipped ? 'flipped' : '') + ' ' + (card.matched ? 'matched' : '') + '" data-idx="' + idx + '" style="font-size:1.4rem">' + (isFlipped ? card.text : '?') + '</button>';
        }).join('') +
      '</div><p style="text-align:center;margin:12px 0 0;font-size:.85rem">Matched: ' + matched + '/' + letters.length + '</p>';
      
      container.querySelectorAll('.offline-game-cell:not(.matched)').forEach(function(btn) {
        btn.addEventListener('click', function() {
          var idx = parseInt(btn.getAttribute('data-idx'), 10);
          if (flipped.indexOf(idx) >= 0 || flipped.length >= 2) return;
          
          flipped.push(idx);
          render();
          
          if (flipped.length === 2) {
            var first = cards[flipped[0]];
            var second = cards[flipped[1]];
            
            if (first.text === second.text) {
              first.matched = true;
              second.matched = true;
              matched++;
              score += 10;
              document.getElementById('offline-score').textContent = 'Score: ' + score;
              flipped = [];
              
              if (matched === letters.length) {
                setTimeout(function() {
                  container.innerHTML += '<div style="text-align:center;padding:16px;background:#d1fae5;border-radius:12px;margin-top:12px"><b>🎉 Amazing! You matched all letters!</b><br><small>You know ' + letters.length + ' Hindi letters now!</small></div>';
                }, 300);
              } else {
                setTimeout(render, 600);
              }
            } else {
              setTimeout(function() {
                flipped = [];
                render();
              }, 1000);
            }
          }
        });
      });
    }
    
    render();
  }

  function renderScrambleGame(container) {
    var words = HINDI_WORDS.slice(0, 5);
    var current = 0;
    var score = 0;
    
    function renderWord() {
      if (current >= words.length) {
        container.innerHTML = '<div style="text-align:center;padding:20px;background:#d1fae5;border-radius:12px"><b>🎉 You unscrambled ' + words.length + ' words!</b><br><small>Great job learning Hindi vocabulary!</small></div>';
        return;
      }
      
      var word = words[current];
      var letters = word.hi.split('');
      var scrambled = letters.slice();
      for (var i = scrambled.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = scrambled[i]; scrambled[i] = scrambled[j]; scrambled[j] = temp;
      }
      
      container.innerHTML = 
        '<div style="text-align:center">' +
          '<p style="font-size:.9rem;color:#5f6577">Unscramble this Hindi word:</p>' +
          '<div style="font-size:1.6rem;font-weight:800;letter-spacing:.1em;margin:12px 0;padding:12px;background:#f5f2ff;border-radius:12px;border:2px dashed #d9d6e8">' + scrambled.join(' ') + '</div>' +
          '<p style="font-size:.85rem;color:#5f6577">Hint: ' + word.en + ' (' + word.roman + ')</p>' +
          '<div id="scramble-built" style="min-height:48px;border:2px dashed #9fb4d0;border-radius:12px;padding:10px;margin:12px 0;background:#fbfdff">Tap letters to build</div>' +
          '<div id="scramble-pool" style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:12px 0"></div>' +
          '<div style="display:flex;gap:8px;justify-content:center"><button type="button" class="btn btn-ghost btn-sm" id="scramble-clear">Clear</button><button type="button" class="btn btn-primary btn-sm" id="scramble-check">Check ✓</button></div>' +
          '<p style="font-size:.8rem;margin-top:12px">' + (current + 1) + ' of ' + words.length + ' words</p>' +
        '</div>';
      
      var built = [];
      var builtEl = container.querySelector('#scramble-built');
      var poolEl = container.querySelector('#scramble-pool');
      
      scrambled.forEach(function(letter, idx) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'offline-game-cell';
        btn.style.cssText = 'width:44px;height:44px;font-size:1.2rem';
        btn.textContent = letter;
        btn.addEventListener('click', function() {
          if (btn.style.display === 'none') return;
          built.push(letter);
          builtEl.textContent = built.join('');
          btn.style.display = 'none';
        });
        poolEl.appendChild(btn);
      });
      
      container.querySelector('#scramble-clear').addEventListener('click', function() {
        built = [];
        builtEl.textContent = 'Tap letters to build';
        poolEl.querySelectorAll('.offline-game-cell').forEach(function(b) { b.style.display = 'grid'; });
      });
      
      container.querySelector('#scramble-check').addEventListener('click', function() {
        if (built.join('') === word.hi) {
          score += 10;
          document.getElementById('offline-score').textContent = 'Score: ' + score;
          builtEl.innerHTML = '<span style="color:#10b981;font-weight:800">✓ Correct! ' + word.hi + ' = ' + word.en + '</span>';
          setTimeout(function() { current++; renderWord(); }, 1500);
        } else {
          builtEl.innerHTML = '<span style="color:#ef4444">✗ Try again! Hint: ' + word.hi + '</span>';
        }
      });
    }
    
    renderWord();
  }

  function renderTraceGame(container) {
    var letters = HINDI_LETTERS.slice(0, 6);
    var current = 0;
    
    function renderLetter() {
      if (current >= letters.length) {
        container.innerHTML = '<div style="text-align:center;padding:20px;background:#dbeafe;border-radius:12px"><b>🎨 You traced ' + letters.length + ' letters!</b><br><small>Your handwriting is getting better!</small></div>';
        return;
      }
      
      var letter = letters[current];
      container.innerHTML = 
        '<div style="text-align:center">' +
          '<p style="font-size:.9rem;color:#5f6577">Trace this letter with your finger:</p>' +
          '<div style="width:200px;height:200px;margin:16px auto;border:2px dashed #d9d6e8;border-radius:16px;display:grid;place-items:center;background:repeating-linear-gradient(45deg,#f6f4ff,#f6f4ff 10px,#fff 10px,#fff 20px);position:relative;overflow:hidden">' +
            '<span style="font-size:6rem;font-weight:900;color:transparent;-webkit-text-stroke:3px #4f32d9;user-select:none">' + letter + '</span>' +
            '<canvas id="trace-canvas" width="200" height="200" style="position:absolute;inset:0;touch-action:none;cursor:crosshair"></canvas>' +
          '</div>' +
          '<p style="font-size:1.2rem;font-weight:700">' + letter + ' <small style="font-weight:400;color:#5f6577">— practice writing</small></p>' +
          '<div style="display:flex;gap:8px;justify-content:center;margin-top:12px"><button type="button" class="btn btn-ghost btn-sm" id="trace-clear">Clear</button><button type="button" class="btn btn-primary btn-sm" id="trace-next">Next →</button></div>' +
          '<p style="font-size:.8rem;margin-top:12px">' + (current + 1) + ' of ' + letters.length + ' letters</p>' +
        '</div>';
      
      var canvas = container.querySelector('#trace-canvas');
      var ctx = canvas.getContext('2d');
      var drawing = false;
      
      ctx.strokeStyle = '#4f32d9';
      ctx.lineWidth = 4;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      function getPos(e) {
        var rect = canvas.getBoundingClientRect();
        var clientX = e.touches ? e.touches[0].clientX : e.clientX;
        var clientY = e.touches ? e.touches[0].clientY : e.clientY;
        return { x: clientX - rect.left, y: clientY - rect.top };
      }
      
      canvas.addEventListener('mousedown', function(e) { drawing = true; var pos = getPos(e); ctx.beginPath(); ctx.moveTo(pos.x, pos.y); });
      canvas.addEventListener('mousemove', function(e) { if (!drawing) return; var pos = getPos(e); ctx.lineTo(pos.x, pos.y); ctx.stroke(); });
      canvas.addEventListener('mouseup', function() { drawing = false; });
      canvas.addEventListener('touchstart', function(e) { e.preventDefault(); drawing = true; var pos = getPos(e); ctx.beginPath(); ctx.moveTo(pos.x, pos.y); });
      canvas.addEventListener('touchmove', function(e) { e.preventDefault(); if (!drawing) return; var pos = getPos(e); ctx.lineTo(pos.x, pos.y); ctx.stroke(); });
      canvas.addEventListener('touchend', function() { drawing = false; });
      
      container.querySelector('#trace-clear').addEventListener('click', function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      });
      
      container.querySelector('#trace-next').addEventListener('click', function() {
        current++;
        var score = parseInt((document.getElementById('offline-score').textContent.match(/\d+/) || [0])[0], 10) + 5;
        document.getElementById('offline-score').textContent = 'Score: ' + score;
        renderLetter();
      });
    }
    
    renderLetter();
  }

  function renderPuzzleGame(container) {
    var letters = HINDI_LETTERS.slice(0, 5);
    var shuffled = letters.slice();
    for (var i = shuffled.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = shuffled[i]; shuffled[i] = shuffled[j]; shuffled[j] = temp;
    }
    
    var score = 0;
    
    function render() {
      var isCorrect = shuffled.join('') === letters.join('');
      
      container.innerHTML = 
        '<div style="text-align:center">' +
          '<p style="font-size:.9rem;color:#5f6577">Put Hindi letters in correct order:</p>' +
          '<p style="font-size:.8rem;color:#5f6577">Correct: ' + letters.join(' ') + '</p>' +
          '<div id="puzzle-area" style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:16px 0;min-height:60px;padding:12px;background:#f8f7fd;border-radius:12px;border:1px dashed #d9d6e8">' +
            shuffled.map(function(letter, idx) {
              return '<button type="button" class="offline-game-cell" data-idx="' + idx + '" draggable="true" style="width:48px;height:48px">' + letter + '</button>';
            }).join('') +
          '</div>' +
          (isCorrect ? '<div style="padding:12px;background:#d1fae5;border-radius:12px;color:#065f46;font-weight:700">✓ Perfect order! You know Hindi alphabet!</div>' : '<p style="font-size:.85rem;color:#5f6577">Drag or tap to reorder • Tap two letters to swap</p>') +
          '<div style="display:flex;gap:8px;justify-content:center;margin-top:12px"><button type="button" class="btn btn-ghost btn-sm" id="puzzle-shuffle">Shuffle</button><button type="button" class="btn btn-primary btn-sm" id="puzzle-check">Check</button></div>' +
        '</div>';
      
      var selected = null;
      
      container.querySelectorAll('.offline-game-cell').forEach(function(btn) {
        btn.addEventListener('click', function() {
          var idx = parseInt(btn.getAttribute('data-idx'), 10);
          if (selected === null) {
            selected = idx;
            btn.style.borderColor = '#4f32d9';
            btn.style.background = '#ede8ff';
          } else {
            if (selected !== idx) {
              var temp = shuffled[selected];
              shuffled[selected] = shuffled[idx];
              shuffled[idx] = temp;
              score += 1;
              document.getElementById('offline-score').textContent = 'Score: ' + score;
            }
            selected = null;
            render();
          }
        });
      });
      
      container.querySelector('#puzzle-shuffle').addEventListener('click', function() {
        for (var i = shuffled.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          var temp = shuffled[i]; shuffled[i] = shuffled[j]; shuffled[j] = temp;
        }
        render();
      });
      
      container.querySelector('#puzzle-check').addEventListener('click', function() {
        if (shuffled.join('') === letters.join('')) {
          document.getElementById('offline-score').textContent = 'Score: ' + (score + 10);
          container.innerHTML += '<div style="text-align:center;padding:12px;background:#d1fae5;border-radius:12px;margin-top:12px;font-weight:700">🎉 Correct order! Well done!</div>';
        } else {
          container.innerHTML += '<div style="text-align:center;padding:12px;background:#fef1f1;border-radius:12px;margin-top:12px">Not yet, keep trying!<br><small>Correct: ' + letters.join(' ') + '</small></div>';
          setTimeout(render, 2000);
        }
      });
    }
    
    render();
  }

  function renderQuizGame(container) {
    var questions = HINDI_WORDS.slice(0, 5).map(function(word) {
      var options = HINDI_WORDS.filter(function(w) { return w.hi !== word.hi; }).slice(0, 3).map(function(w) { return w.en; });
      options.push(word.en);
      for (var i = options.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = options[i]; options[i] = options[j]; options[j] = temp;
      }
      return { q: word.hi, answer: word.en, options: options, roman: word.roman };
    });
    
    var current = 0;
    var score = 0;
    
    function renderQ() {
      if (current >= questions.length) {
        container.innerHTML = '<div style="text-align:center;padding:20px;background:#e0e7ff;border-radius:12px"><b>🎯 Quiz finished!</b><br>Score: ' + score + '/' + questions.length + '<br><small>' + (score === questions.length ? 'Perfect! You\'re a Hindi star!' : score >= 3 ? 'Good job! Keep practicing!' : 'Keep learning, you\'ll get there!') + '</small></div>';
        document.getElementById('offline-score').textContent = 'Score: ' + score;
        return;
      }
      
      var q = questions[current];
      container.innerHTML = 
        '<div>' +
          '<p style="font-size:.85rem;color:#5f6577">Question ' + (current + 1) + ' of ' + questions.length + '</p>' +
          '<div style="text-align:center;padding:16px;background:#f5f2ff;border-radius:12px;margin:12px 0"><b style="font-size:1.6rem">' + q.q + '</b><br><small style="color:#5f6577">' + q.roman + '</small><br><small>What does this mean?</small></div>' +
          '<div style="display:grid;gap:8px">' +
            q.options.map(function(opt) {
              return '<button type="button" class="offline-game-cell" data-opt="' + opt + '" style="height:auto;min-height:44px;padding:10px;text-align:left;justify-content:start;font-size:.95rem">' + opt + '</button>';
            }).join('') +
          '</div>' +
          '<div id="quiz-fb" style="margin-top:12px;min-height:20px"></div>' +
        '</div>';
      
      container.querySelectorAll('[data-opt]').forEach(function(btn) {
        btn.addEventListener('click', function() {
          var chosen = btn.getAttribute('data-opt');
          var fb = container.querySelector('#quiz-fb');
          
          container.querySelectorAll('[data-opt]').forEach(function(b) {
            b.disabled = true;
            if (b.getAttribute('data-opt') === q.answer) {
              b.style.background = '#d1fae5';
              b.style.borderColor = '#10b981';
            }
          });
          
          if (chosen === q.answer) {
            score++;
            fb.innerHTML = '<span style="color:#10b981;font-weight:700">✓ Correct! ' + q.q + ' means ' + q.answer + '</span>';
          } else {
            btn.style.background = '#fef1f1';
            btn.style.borderColor = '#ef4444';
            fb.innerHTML = '<span style="color:#ef4444">✗ Correct answer: ' + q.answer + '</span>';
          }
          
          document.getElementById('offline-score').textContent = 'Score: ' + score;
          
          setTimeout(function() { current++; renderQ(); }, 1500);
        });
      });
    }
    
    renderQ();
  }

  function checkOffline() {
    return typeof navigator !== 'undefined' && navigator.onLine === false;
  }

  function init() {
    // Create container
    createGameContainer();
    
    // Show if offline
    if (checkOffline()) {
      setTimeout(function() {
        var container = document.getElementById('ekguru-offline-game');
        if (container) {
          container.classList.add('show');
          showGameList();
        }
      }, 2000);
    }
    
    // Listen for offline/online
    window.addEventListener('offline', function() {
      setTimeout(function() {
        var container = document.getElementById('ekguru-offline-game');
        if (container) {
          container.classList.add('show');
          showGameList();
        }
      }, 500);
    });
    
    window.addEventListener('online', function() {
      var container = document.getElementById('ekguru-offline-game');
      if (container) {
        container.innerHTML = '<div style="text-align:center;padding:20px"><b>🌐 Back online!</b><br><small>Your games saved, continue learning!</small><br><button type="button" class="btn btn-primary btn-sm" style="margin-top:12px" onclick="this.closest(\'#ekguru-offline-game\').classList.remove(\'show\')">Continue →</button></div>';
        setTimeout(function() {
          if (container) container.classList.remove('show');
        }, 3000);
      }
    });

    // Add offline game button to page if needed
    var offlineBtn = document.getElementById('offline-games-btn');
    if (!offlineBtn) {
      var host = document.querySelector('.pw-legacy, .art, .egc, main');
      if (host) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.id = 'offline-games-btn';
        btn.className = 'btn btn-ghost btn-sm google-anno-skip';
        btn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:999;background:#fff;border:1px solid #e4e4ef;border-radius:999px;box-shadow:0 4px 20px rgba(0,0,0,.1);display:none';
        btn.innerHTML = '🎮 Offline Games';
        btn.addEventListener('click', function() {
          var container = document.getElementById('ekguru-offline-game');
          if (container) {
            container.classList.add('show');
            showGameList();
          }
        });
        document.body.appendChild(btn);
        
        // Show button when offline or as fun extra
        if (checkOffline()) btn.style.display = 'inline-flex';
        else {
          // Show after 30s as engagement
          setTimeout(function() { btn.style.display = 'inline-flex'; }, 30000);
        }
        
        window.addEventListener('offline', function() { btn.style.display = 'inline-flex'; });
      }
    }

    window.EKGURU_OFFLINE_GAMES = {
      show: function() {
        var c = document.getElementById('ekguru-offline-game');
        if (c) { c.classList.add('show'); showGameList(); }
      },
      hide: function() {
        var c = document.getElementById('ekguru-offline-game');
        if (c) c.classList.remove('show');
      },
      isOffline: checkOffline,
      games: GAMES
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
