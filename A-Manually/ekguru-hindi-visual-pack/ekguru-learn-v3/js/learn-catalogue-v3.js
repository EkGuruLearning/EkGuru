/* Static links first; progressive search, filtering and bounded catalogue expansion. */
(() => {
  'use strict';
  const root=document.querySelector('.eg-learn-catalogue'); if(!root)return;
  const $=s=>root.querySelector(s), all=s=>[...root.querySelectorAll(s)];
  const input=$('#lc-search'), cards=all('[data-lc-card]'), sections=all('[data-lc-section]'), filters=all('[data-lc-filter]');
  const status=$('.lc-status'), empty=$('.lc-empty'), clear=$('.lc-clear');
  const chunk=12, limits=new Map(sections.map(s=>[s,chunk]));
  let category='all';
  const norm=s=>s.normalize('NFC').toLocaleLowerCase().trim().replace(/\s+/g,' ');
  const fold=s=>norm(s).normalize('NFD').replace(/\p{Script=Latin}\p{M}*/gu,v=>v.replace(/\p{M}/gu,'')).normalize('NFC');
  const index=new Map(cards.map(c=>[c,[norm(c.dataset.lcSearch),fold(c.dataset.lcSearch)]]));
  const reduced=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function update(animate=false){
    const q=norm(input.value),fq=fold(input.value);let total=0, shown=0;
    for(const s of sections){let n=0, visible=0;const button=s.querySelector('.lc-more-languages');
      for(const c of s.querySelectorAll('[data-lc-card]')){
        const [text,folded]=index.get(c);const match=(category==='all'||c.dataset.lcGroup===category)&&(!q||text.includes(q)||folded.includes(fq));
        if(match)n++;const show=match&&(!!q||n<=limits.get(s));const was=c.hidden;c.hidden=!show;
        if(show){visible++;if(animate&&was&&!reduced()){c.style.setProperty('--lc-order',Math.min(visible-1,7));c.classList.add('lc-arrive');}}
      }
      total+=n;shown+=visible;s.hidden=n===0;button.hidden=n<=visible;button.textContent=`Show ${Math.min(chunk,n-visible)} more · ${n-visible} remaining`;
    }
    for(const b of filters)b.setAttribute('aria-pressed',String(b.dataset.lcFilter===category));
    status.textContent=`${shown} of ${total} ${total===1?'language':'languages'} shown`;status.hidden=!q&&category==='all'&&shown===total;
    empty.hidden=total!==0;clear.hidden=!input.value;
  }
  for(const b of all('[data-lc-total]'))b.textContent=cards.filter(c=>b.dataset.lcTotal==='all'||c.dataset.lcGroup===b.dataset.lcTotal).length;
  cards.forEach(c=>c.addEventListener('animationend',()=>c.classList.remove('lc-arrive')));
  input.addEventListener('input',()=>update(true));clear.addEventListener('click',()=>{input.value='';update(true);input.focus();});
  for(const b of filters)b.addEventListener('click',()=>{category=b.dataset.lcFilter;update(true);});
  for(const s of sections)s.querySelector('.lc-more-languages').addEventListener('click',()=>{const first=s.querySelector('[data-lc-card][hidden]');limits.set(s,limits.get(s)+chunk);update(true);if(first&&!first.hidden)first.focus({preventScroll:true});});
  window.addEventListener('hashchange',()=>{if(['#li-hindi','#li-indian','#li-world'].includes(location.hash)){category='all';input.value='';update();document.getElementById(location.hash.slice(1))?.scrollIntoView();}});
  $('.lc-toolbar').hidden=false;update();
})();
