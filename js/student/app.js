import { configured, connect, actionSettings, watch } from './auth.js';
import { request, ApiUnauthorized, ApiForbidden } from './api.js';
import { initialiseLanguage, applyLanguage, setWelcome, translate } from './i18n.js';

const main = document.querySelector('[data-student-page]');
const page = main?.dataset.studentPage;
let status = main?.querySelector('[data-status]');
function say(text, error=false) { if (status) { status.textContent=text; status.dataset.error=String(error); applyLanguage(); } }
function errorMessage(error) {
  const code=error?.code || '';
  if (code==='auth/invalid-email') return 'Please enter a valid email address.';
  if (code==='auth/weak-password') return 'Please choose a stronger password.';
  if (code==='auth/email-already-in-use') return 'We could not complete that request. Please try again later.';
  if (code==='auth/invalid-credential' || code==='auth/wrong-password' || code==='auth/user-not-found') return 'Email or password was not accepted.';
  if (code==='auth/popup-closed-by-user') return 'Google sign-in was closed before it finished.';
  if (code==='auth/popup-blocked') return 'Your browser blocked the sign-in window. Allow popups and try again.';
  if (code==='auth/unauthorized-domain') return 'This domain is not authorised for sign-in yet.';
  if (code==='auth/too-many-requests') return 'Too many attempts. Please try again later.';
  if (code==='auth/expired-action-code' || code==='auth/invalid-action-code') return 'This link is invalid or has expired. Request a new one.';
  if (code==='auth/network-request-failed') return 'Network unavailable. Check your connection and try again.';
  return 'We could not complete that request. Please try again later.';
}
function buttons(enabled) {
  main.querySelectorAll('[data-auth-form] button[type=submit], [data-google]').forEach(b => { b.disabled=!enabled; });
}
function initPasswordToggle() {
  main.querySelectorAll('[data-password-toggle]').forEach(button => button.addEventListener('click', () => {
    const input=button.parentElement.querySelector('input');
    const show=input.type==='password'; input.type=show?'text':'password'; button.textContent=show?'Hide':'Show';
    button.setAttribute('aria-label',translate(show?'Hide password':'Show password')); applyLanguage();
  }));
}
async function initialiseAuthForm() {
  if (!configured()) { say('Student sign-in is not configured. Free lessons remain available.'); return; }
  let c; try { c=await connect(); } catch (_) { say('Student sign-in is temporarily unavailable.',true); return; }
  const {sdk,auth}=c; const form=main.querySelector('[data-auth-form]');let busy=false;
  function setAuthBusy(value){busy=value;buttons(!value);}
  buttons(true);
  let localLogoutWarning=false;
  if(page==='login')try{localLogoutWarning=sessionStorage.getItem('eg-local-signout-warning')==='1';sessionStorage.removeItem('eg-local-signout-warning');}catch(_){}
  say(localLogoutWarning?'Could not revoke the server session. You were signed out locally.':'Your account is optional; existing free lessons remain available.',localLogoutWarning);
  if (form) form.addEventListener('submit',async event => {
    event.preventDefault(); if (busy || !form.reportValidity()) return;
    const fields=new FormData(form), email=String(fields.get('email')||'').trim(), password=String(fields.get('password')||'');
    if (page==='register' && !String(fields.get('fullName')||'').trim()) { say('Please enter your full name.',true); form.elements.fullName.focus(); return; }
    if (page==='register' && password!==String(fields.get('confirm')||'')) { say('Passwords do not match.',true); return; }
    setAuthBusy(true); say('Please wait…');
    try {
      if (page==='login') {
        await sdk.setPersistence(auth, fields.has('remember') ? sdk.browserLocalPersistence : sdk.browserSessionPersistence);
        await sdk.signInWithEmailAndPassword(auth,email,password); location.assign('/account/dashboard/');
      }
      if (page==='register') {
        await sdk.setPersistence(auth,sdk.browserSessionPersistence);
        const result=await sdk.createUserWithEmailAndPassword(auth,email,password);
        let nameSaved=true,verificationSent=true;
        try { await sdk.updateProfile(result.user,{displayName:String(fields.get('fullName')||'').trim()}); }
        catch (_) { nameSaved=false; }
        try { await sdk.sendEmailVerification(result.user,actionSettings()); }
        catch (_) { verificationSent=false; }
        try { sessionStorage.setItem('eg-registration-notice',!verificationSent&&!nameSaved?'both-failed':!verificationSent?'verification-failed':!nameSaved?'name-failed':'verification-sent'); } catch (_) {}
        location.assign('/account/verify-email/');
      }
      if (page==='forgot') { await sdk.sendPasswordResetEmail(auth,email,actionSettings()); say('If the address can receive a reset email, check your inbox.'); form.reset(); }
    } catch (error) {
      if (page==='forgot' && error?.code==='auth/user-not-found') say('If the address can receive a reset email, check your inbox.');
      else say(errorMessage(error),true);
    } finally { setAuthBusy(false); }
  });
  const google=main.querySelector('[data-google]');
  if (google) google.addEventListener('click',async () => {
    if(busy)return;
    const terms=form?.elements.terms;
    if (page==='register' && (!terms || !terms.checked)) { say('Please accept the Terms and Privacy Policy before signing up.',true); terms?.focus(); return; }
    setAuthBusy(true); say('Opening Google sign-in…');
    try {
      await sdk.setPersistence(auth,form?.elements.remember?.checked ? sdk.browserLocalPersistence : sdk.browserSessionPersistence);
      await sdk.signInWithPopup(auth,new sdk.GoogleAuthProvider()); location.assign('/account/dashboard/');
    }
    catch (error) { say(errorMessage(error),true); }
    finally { setAuthBusy(false); }
  });
}
async function initialiseAction() {
  const action=window.__egAction; delete window.__egAction;
  if (!action) { say('Open a verification or reset link from your email.',true); return; }
  if (!configured()) { say('Student accounts are not connected yet. This link cannot be processed.',true); return; }
  try {
    const {sdk,auth}=await connect();
    if (action.mode==='verifyEmail' || action.mode==='recoverEmail') {
      const info=await sdk.checkActionCode(auth,action.code);
      const expected=action.mode==='verifyEmail'?'VERIFY_EMAIL':'RECOVER_EMAIL';
      if (info.operation!==expected) { say('This link does not match the requested email action.',true); return; }
      await sdk.applyActionCode(auth,action.code); say('Your email action is complete. You can log in.'); return;
    }
    if (action.mode!=='resetPassword') { say('This email action is not supported.',true); return; }
    await sdk.verifyPasswordResetCode(auth,action.code);
    const box=main.querySelector('[data-action-content]'); box.textContent='';
    const form=document.createElement('form'); form.method='post'; form.action='#';
    const label=document.createElement('label'); label.textContent='New password';
    const input=document.createElement('input'); input.name='password'; input.type='password'; input.required=true; input.minLength=6; input.autocomplete='new-password';
    const button=document.createElement('button'); button.className='sa-primary'; button.type='submit'; button.textContent='Set new password';
    label.append(input); form.append(label,button); box.append(form); say('Choose a new password.');
    form.addEventListener('submit',async e=>{e.preventDefault();if(!form.reportValidity())return;button.disabled=true;
      try { await sdk.confirmPasswordReset(auth,action.code,input.value); form.remove(); say('Password updated. You can log in now.'); }
      catch(error){say(errorMessage(error),true);button.disabled=false;}
    });
  } catch (error) { say(errorMessage(error),true); }
}
function readableError(error) {
  if (error instanceof ApiUnauthorized) return 'Your session could not be verified. Please sign in again.';
  if (error instanceof ApiForbidden) {
    if (error.code==='recent_authentication_required') return 'Please sign in again before updating your profile.';
    if (error.code==='email_verification_required') return 'Please verify your email before using connected learning services.';
    if (error.code==='course_access_denied') return 'This lesson is not available for your account.';
  }
  return 'The learning service is temporarily unavailable.';
}
function renderCourses(courses) {
  const target=main.querySelector('[data-dashboard-courses]');if(!target)return;
  target.replaceChildren();
  if(!courses.length){target.textContent='No published courses are available yet.';applyLanguage();return;}
  const list=document.createElement('ul');list.setAttribute('data-no-translate','');
  courses.forEach(course=>{const item=document.createElement('li');item.textContent=course.title_hi+' / '+course.title_en;list.append(item);});
  target.append(list);
}
function renderAccountCourses(courses,progress) {
  let target=main.querySelector('[data-account-courses]');
  if(!target){const placeholder=main.querySelector('[data-protected] .sa-card > p');if(!placeholder)return;target=document.createElement('div');target.setAttribute('data-account-courses','');placeholder.replaceWith(target);}
  const selected=progress?courses:courses.filter(course=>course.enrolled===true||course.enrolled===1);
  target.replaceChildren();
  if(!selected.length){target.textContent=progress?'No published courses are available yet.':'No enrolled courses are available yet.';applyLanguage();return;}
  const list=document.createElement('ul');
  selected.forEach(course=>{
    const item=document.createElement('li'),title=document.createElement('span');
    title.setAttribute('data-no-translate','');title.textContent=course.title_hi+' / '+course.title_en;item.append(title);
    if(progress){const details=document.createElement('span'),started=document.createElement('span'),completed=document.createElement('span');started.textContent='Started lessons';completed.textContent='Completed segments';details.append(' — ',started,': '+course.startedLessons+'; ',completed,': '+(course.completedSegments===null?'—':course.completedSegments));item.append(details);}
    list.append(item);
  });target.append(list);
}
async function initialiseProtected() {
  if (!configured()) { say('Student sign-in is not configured. Free lessons remain available.'); return; }
  let sdk,auth; try { ({sdk,auth}=await connect()); } catch (_) { say('Student sign-in is temporarily unavailable.',true); return; }
  let current=null,generation=0,controller=null,loggingOut=false;
  const profile=main.querySelector('[data-profile-form]');
  function clearProtected(){
    main.querySelectorAll('[data-protected]').forEach(x=>x.hidden=true);
    main.querySelectorAll('[data-profile-email],[data-profile-verified]').forEach(x=>x.textContent='—');
    if(profile){profile.elements.displayName.value='';profile.querySelector('button').disabled=true;}
    renderCourses([]);main.querySelector('[data-account-courses]')?.replaceChildren();setWelcome('');
  }
  main.querySelectorAll('[data-logout]').forEach(button=>button.addEventListener('click',async()=>{
    if(!current||loggingOut)return;const owner=current;loggingOut=true;button.disabled=true;
    generation++;controller?.abort();current=null;clearProtected();say('Signing out…');
    const remoteController=new AbortController();let timer;
    const remote=Promise.race([
      request('logout',owner,{signal:remoteController.signal}).then(()=>true,()=>false),
      new Promise(resolve=>{timer=setTimeout(()=>{remoteController.abort();resolve(false);},2000);})
    ]);
    try {
      await sdk.signOut(auth);const revoked=await remote;clearTimeout(timer);
      try{if(revoked)sessionStorage.removeItem('eg-local-signout-warning');else sessionStorage.setItem('eg-local-signout-warning','1');}catch(_){}
      location.replace('/account/login/');
    } catch(error) {
      remoteController.abort();clearTimeout(timer);loggingOut=false;current=owner;
      say('Could not sign out locally. Please try again.',true);button.disabled=false;
    }
  }));
  if(profile) {
    profile.elements.displayName.maxLength=80;
    profile.addEventListener('submit',async e=>{
      e.preventDefault();if(!current||!profile.reportValidity())return;
      const owner=current,version=generation,signal=controller.signal,button=profile.querySelector('button');button.disabled=true;
      try { const result=await request('updateProfile',owner,{body:{displayName:String(new FormData(profile).get('displayName')||'').trim()},signal});if(owner!==current||version!==generation)return;profile.elements.displayName.value=result.profile.displayName||'';setWelcome(result.profile.displayName);say('Display name saved.'); }
      catch(error){if(owner===current&&version===generation)say(readableError(error),true);} finally{if(owner===current&&version===generation)button.disabled=false;}
    });
  }
  window.addEventListener('pagehide',()=>{generation++;controller?.abort();current=null;clearProtected();});
  window.addEventListener('pageshow',event=>{if(event.persisted)location.reload();});
  try { await watch(async user=>{
    if(loggingOut){clearProtected();return;}
    generation++;const version=generation;controller?.abort();controller=new AbortController();current=user;
    clearProtected();
    if (!user) { if(loggingOut)return;if (['dashboard','settings','delete','account-section'].includes(page)) location.replace('/account/login/'); else say('Log in to send a verification email.'); return; }
    main.querySelectorAll('[data-logout]').forEach(b=>b.disabled=false);
    if (page==='verify') {
      const b=main.querySelector('[data-send-verification]');b.disabled=!!user.emailVerified;
      let notice='';try{notice=sessionStorage.getItem('eg-registration-notice')||'';sessionStorage.removeItem('eg-registration-notice');}catch(_){}
      const messages={'verification-failed':'Your account was created, but the verification email could not be sent. Open the verification page to retry.','name-failed':'Your account was created, but your name could not be saved. You can update it in settings.','both-failed':'Your account was created, but your name could not be saved and the verification email was not sent. Retry verification here and update your name in settings.','verification-sent':'Verification email sent.'};
      say(user.emailVerified?'Your email is verified.':Object.hasOwn(messages,notice)?messages[notice]:'Your email is not verified yet.',notice==='verification-failed'||notice==='name-failed'||notice==='both-failed');
      b.onclick=async()=>{b.disabled=true;try{await sdk.sendEmailVerification(user,actionSettings());if(version===generation)say('Verification email sent.');}catch(error){if(version===generation){say(errorMessage(error),true);b.disabled=false;}}};return;
    }
    if (page==='delete') { say('Secure account and data deletion is not connected yet.'); return; }
    say('Please wait…');
    try {
      const session=await request('session',user,{signal:controller.signal});if(version!==generation)return;
      let info=session.user;
      if(page==='settings'){const result=await request('profile',user,{signal:controller.signal});if(version!==generation)return;info=result.profile;}
      const coursePage=page==='account-section'&&['/account/courses/','/account/progress/'].includes(location.pathname);
      if(page==='dashboard'||coursePage){const data=await request('dashboard',user,{signal:controller.signal});if(version!==generation)return;if(coursePage)renderAccountCourses(data.courses,location.pathname==='/account/progress/');else{renderCourses(data.courses);const activity=main.querySelector('[data-dashboard-continue]');if(activity)activity.textContent='Select a published course to continue.';}}
      main.querySelectorAll('[data-protected]').forEach(x=>x.hidden=false);setWelcome(info.displayName);
      const email=main.querySelector('[data-profile-email]');if(email)email.textContent=info.email||'Not available';
      const emailVerified=info.emailVerified===true&&user.emailVerified===true;
      const verified=main.querySelector('[data-profile-verified]');if(verified)verified.textContent=emailVerified?'Verified':'Not verified';
      if(profile){profile.elements.displayName.value=info.displayName||'';profile.querySelector('button').disabled=false;}
      say(emailVerified?'Signed in.':'Your email is not verified yet.');
    } catch(error) { if(version!==generation)return;main.querySelectorAll('[data-protected]').forEach(x=>x.hidden=true);say(readableError(error),true); }
  }); } catch (_) { say('Your session could not be restored. Please sign in again.',true); }
}
async function initialiseReader() {
  const section=main.querySelector('section');if(!section)return;
  const old=section.querySelector('.sa-status');if(old){old.removeAttribute('data-status');old.textContent='Enter a course and lesson identifier to request an authorized lesson.';status=old;}
  const oldDescription=Array.from(section.querySelectorAll('p')).find(p=>p.textContent.startsWith('Once available,'));if(oldDescription)oldDescription.remove();
  const form=document.createElement('form');form.className='sa-card';
  for(const [name,label] of [['courseId','Course identifier'],['lessonId','Lesson identifier']]){const l=document.createElement('label');l.textContent=label;const input=document.createElement('input');input.name=name;input.required=true;input.pattern='[a-z0-9-]+';input.maxLength=120;l.append(input);form.append(l);}
  const load=document.createElement('button');load.type='submit';load.className='sa-primary';load.textContent='Open lesson';form.append(load);section.append(form);
  const content=document.createElement('div');content.setAttribute('data-no-translate','');section.append(content);
  let current=null,generation=0,controller=null;
  try{if(configured())await watch(user=>{current=user;generation++;controller?.abort();content.replaceChildren();load.disabled=false;});}catch(_){/* Anonymous free lessons can still be requested. */}
  window.addEventListener('pagehide',()=>{generation++;controller?.abort();current=null;content.replaceChildren();});
  window.addEventListener('pageshow',event=>{if(event.persisted)location.reload();});
  form.addEventListener('submit',async e=>{
    e.preventDefault();if(!form.reportValidity())return;generation++;const version=generation;controller?.abort();controller=new AbortController();content.replaceChildren();load.disabled=true;say('Please wait…');
    const fields=new FormData(form),params={courseId:String(fields.get('courseId')),lessonId:String(fields.get('lessonId'))},owner=current;
    try{
      const result=await request('lesson',owner,{params,signal:controller.signal});if(version!==generation)return;
      if(!result.segments.length){say('No published lesson segments are available yet.');return;}
      result.segments.forEach(segment=>{const article=document.createElement('article');article.className='sa-card';const hindi=document.createElement('p');hindi.lang='hi';hindi.textContent=segment.text_hi;article.append(hindi);if(segment.translation_status==='reviewed'){const english=document.createElement('p');english.lang='en';english.textContent=segment.text_en;article.append(english);}content.append(article);});
      if(owner&&owner.emailVerified){const done=document.createElement('button');done.type='button';done.textContent='Mark lesson complete';done.className='sa-secondary';done.addEventListener('click',async()=>{done.disabled=true;try{await request('progress',owner,{body:{courseId:params.courseId,lessonId:params.lessonId,completed:true},signal:controller.signal});if(version===generation)say('Learning progress saved.');}catch(error){if(version===generation){say(readableError(error),true);done.disabled=false;}}});content.append(done);}
      say('Lesson loaded.');
    }catch(error){if(version===generation)say(readableError(error),true);}finally{if(version===generation)load.disabled=false;}
  });
}
if (main) {
  window.addEventListener('pagehide',()=>{main.querySelectorAll('input[autocomplete="current-password"],input[autocomplete="new-password"]').forEach(input=>{input.value='';});});
  initialiseLanguage();initPasswordToggle();
  if (['login','register','forgot'].includes(page)) initialiseAuthForm();
  else if (page==='action') initialiseAction();
  else if (page==='reader') initialiseReader();
  else if (['dashboard','settings','verify','delete','account-section'].includes(page)) initialiseProtected();
}
