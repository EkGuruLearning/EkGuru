/* Small display preference; local journal and theme remain owned by EkGuru. */
(function(){'use strict';var button=document.querySelector('[data-ac-size]');if(!button)return;
  function update(on){document.documentElement.classList.toggle('ac-large',on);button.setAttribute('aria-pressed',String(on));button.textContent=on?'Standard text':'Larger text';}
  try{update(localStorage.getItem('ekguru:academy:text:v1')==='large');}catch(e){update(false);}
  button.addEventListener('click',function(){var on=!document.documentElement.classList.contains('ac-large');update(on);try{localStorage.setItem('ekguru:academy:text:v1',on?'large':'standard');}catch(e){}});
})();
