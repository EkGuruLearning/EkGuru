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
  if (error instanceof ApiForbidden && error.code==='email_verification_required') return 'Please verify your email before using connected learning services.';
  return 'The learning service is temporarily unavailable.';
}
async function initialiseProtected() {
  if (!configured()) { say('Student sign-in is not configured. Free lessons remain available.'); return; }
  let sdk,auth; try { ({sdk,auth}=await connect()); } catch (_) { say('Student sign-in is temporarily unavailable.',true); return; }
  let current=null,generation=0,controller=null,loggingOut=false;
  function clearProtected(){
    main.querySelectorAll('[data-protected]').forEach(x=>x.hidden=true);
    main.querySelectorAll('[data-profile-email],[data-profile-verified]').forEach(x=>x.textContent='—');
    setWelcome('');
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
  window.addEventListener('pagehide',()=>{generation++;controller?.abort();current=null;clearProtected();});
  window.addEventListener('pageshow',event=>{if(event.persisted)location.reload();});
  try { await watch(async user=>{
    if(loggingOut){clearProtected();return;}
    generation++;const version=generation;controller?.abort();controller=new AbortController();current=user;
    clearProtected();
    if (!user) { if(loggingOut)return;if (page==='dashboard') location.replace('/account/login/'); else say('Log in to send a verification email.'); return; }
    main.querySelectorAll('[data-logout]').forEach(b=>b.disabled=false);
    if (page==='verify') {
      const b=main.querySelector('[data-send-verification]');b.disabled=!!user.emailVerified;
      let notice='';try{notice=sessionStorage.getItem('eg-registration-notice')||'';sessionStorage.removeItem('eg-registration-notice');}catch(_){}
      const messages={'verification-failed':'Your account was created, but the verification email could not be sent. Open the verification page to retry.','name-failed':'Your account was created, but your name could not be saved.','both-failed':'Your account was created, but your name could not be saved and the verification email was not sent. Retry verification here.','verification-sent':'Verification email sent.'};
      say(user.emailVerified?'Your email is verified.':Object.hasOwn(messages,notice)?messages[notice]:'Your email is not verified yet.',notice==='verification-failed'||notice==='name-failed'||notice==='both-failed');
      b.onclick=async()=>{b.disabled=true;try{await sdk.sendEmailVerification(user,actionSettings());if(version===generation)say('Verification email sent.');}catch(error){if(version===generation){say(errorMessage(error),true);b.disabled=false;}}};return;
    }
    say('Please wait…');
    try {
      const session=await request('session',user,{signal:controller.signal});if(version!==generation)return;
      const info=session.user;
      main.querySelectorAll('[data-protected]').forEach(x=>x.hidden=false);setWelcome(info.displayName);
      const email=main.querySelector('[data-profile-email]');if(email)email.textContent=info.email||'Not available';
      const emailVerified=info.emailVerified===true&&user.emailVerified===true;
      const verified=main.querySelector('[data-profile-verified]');if(verified)verified.textContent=emailVerified?'Verified':'Not verified';
      say(emailVerified?'Signed in.':'Your email is not verified yet.');
    } catch(error) { if(version!==generation)return;main.querySelectorAll('[data-protected]').forEach(x=>x.hidden=true);say(readableError(error),true); }
  }); } catch (_) { say('Your session could not be restored. Please sign in again.',true); }
}
if (main) {
  window.addEventListener('pagehide',()=>{main.querySelectorAll('input[autocomplete="current-password"],input[autocomplete="new-password"]').forEach(input=>{input.value='';});});
  initialiseLanguage();initPasswordToggle();
  if (['login','register','forgot'].includes(page)) initialiseAuthForm();
  else if (page==='action') initialiseAction();
  else if (['dashboard','verify'].includes(page)) initialiseProtected();
}
