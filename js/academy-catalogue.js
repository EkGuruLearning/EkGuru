/* Progressive enhancement: links remain server-rendered if fetching fails. */
(function () {
  'use strict';
  var host=document.getElementById('catalogue-filters'), list=document.getElementById('catalogue-list');
  if(!host || !list || !window.fetch) return;
  fetch('/data/hindi-academy/search-index.json').then(function(r){if(!r.ok) throw new Error('index unavailable');return r.json();}).then(function(data){
    if(data.version!==2 || !Array.isArray(data.lessons)) return;
    var records=new Map(data.lessons.map(function(x){return [x.id,x];}));
    var nodes=Array.from(list.querySelectorAll('[data-catalogue-id]'));
    if(nodes.some(function(n){return !records.has(n.dataset.catalogueId);})) return;
    var labels={course:'course_title',phase:'phase_title',chapter:'chapter_title'};
    host.querySelectorAll('select[data-filter]').forEach(function(select){
      var field=select.dataset.filter; if(field==='audio'||field==='worksheet') return;
      if(field==='ages'){[['4-6','Ages 4–6'],['7-9','Ages 7–9'],['10-12','Ages 10–12'],['adults','Adults'],['older-adults','Older adults']].forEach(function(p){var o=document.createElement('option');o.value=p[0];o.textContent=p[1];select.appendChild(o);});return;}
      var found=new Map(); data.lessons.forEach(function(x){var values=Array.isArray(x[field])?x[field]:[x[field]]; values.forEach(function(v){if(v) found.set(v,labels[field] ? x[labels[field]] : v);});});
      Array.from(found.entries()).sort(function(a,b){return a[1].localeCompare(b[1]);}).forEach(function(pair){var o=document.createElement('option');o.value=pair[0];o.textContent=pair[1];select.appendChild(o);});
    });
    function update(){
      var q=document.getElementById('catalogue-query').value.trim().toLocaleLowerCase(); var visible=0;
      nodes.forEach(function(n){var x=records.get(n.dataset.catalogueId), text=[x.title,x.topic,x.course_title,x.phase_title,x.chapter_title,x.terms].join(' ').toLocaleLowerCase(); var ok=!q||text.indexOf(q)>=0;
        host.querySelectorAll('select[data-filter]').forEach(function(s){if(!s.value) return;var v=x[s.dataset.filter]; if(Array.isArray(v)){if(v.indexOf(s.value)<0 && !(s.dataset.filter==='ages' && v.indexOf('all')>=0)) ok=false;} else if(String(v == null ? '' : v)!==s.value) ok=false;});
        n.hidden=!ok;if(ok)visible++;
      });
      list.querySelectorAll('.ac-directory-group').forEach(function(group){group.hidden=!group.querySelector('[data-catalogue-id]:not([hidden])');});
      document.getElementById('catalogue-count').textContent=visible+' of '+nodes.length+' registered lessons shown.';
    }
    host.addEventListener('input',update);host.addEventListener('change',update);
    document.getElementById('catalogue-reset').addEventListener('click',function(){document.getElementById('catalogue-query').value='';host.querySelectorAll('select').forEach(function(s){s.value='';});update();});
    host.hidden=false;update();
  }).catch(function(){ /* static links remain available */ });
})();
