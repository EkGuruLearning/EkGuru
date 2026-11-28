import { configured, watch } from './auth.js';
const group=document.querySelector('[data-student-nav]');
if (group && configured()) {
  watch(user => {
    group.querySelectorAll('[data-student-neutral]').forEach(e=>e.hidden=true);
    group.querySelectorAll('[data-guest]').forEach(e=>e.hidden=!!user);
    group.querySelectorAll('[data-signed-in]').forEach(e=>e.hidden=!user);
  }).catch(()=>{});
}
