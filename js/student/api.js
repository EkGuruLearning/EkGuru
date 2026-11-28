// Only the authentication session and logout operations are included.
// The intended origin does not establish that the Worker is deployed.
import { studentConfig } from './config.js';
const ORIGIN='https://api.ekguru.shop';
const operations=Object.freeze({
  session:{method:'GET',path:'/v1/auth/session',shape:'session'},
  logout:{method:'POST',path:'/v1/auth/logout',shape:'logout'}
});
export class ApiUnavailable extends Error { constructor(message='The learning service is temporarily unavailable.') { super(message); this.name='ApiUnavailable'; } }
export class ApiUnauthorized extends Error { constructor() { super('Your session could not be verified. Please sign in again.'); this.name='ApiUnauthorized'; } }
export class ApiForbidden extends Error { constructor(code='access_denied') { super('This request is not permitted.'); this.name='ApiForbidden'; this.code=code; } }
const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
const str=x=>typeof x==='string';
const nullableString=x=>x===null||str(x);
function validProfile(p,photo=true){return object(p)&&str(p.id)&&nullableString(p.email)&&typeof p.emailVerified==='boolean'&&nullableString(p.displayName)&&(!photo||nullableString(p.photoUrl))&&['student','admin'].includes(p.role);}
function validResponse(shape,v){
  if(!object(v))return false;
  if(shape==='session')return validProfile(v.user);
  if(shape==='logout')return v.loggedOut===true;
  return false;
}
export function apiReady(key) { return studentConfig.workerOrigin===ORIGIN&&Object.hasOwn(operations,key); }
export async function request(key,user,options={}) {
  const op=Object.hasOwn(operations,key)?operations[key]:null;
  if(!op||!apiReady(key))throw new ApiUnavailable('The learning service is not connected.');
  if(!user)throw new ApiUnauthorized();
  if(options.body!==undefined||options.params!==undefined)throw new ApiUnavailable('The request is invalid.');
  const url=new URL(op.path,ORIGIN);if(url.origin!==ORIGIN)throw new ApiUnavailable('Invalid service configuration.');
  const controller=new AbortController(),cancel=()=>controller.abort();
  if(options.signal?.aborted)cancel();else options.signal?.addEventListener('abort',cancel,{once:true});
  const timer=setTimeout(cancel,12000);
  async function send(refresh){
    if(controller.signal.aborted)throw new DOMException('Request cancelled','AbortError');
    const headers={'Accept':'application/json'};
    if(user){
      let onAbort;const interrupted=new Promise((_,reject)=>{onAbort=()=>reject(new DOMException('Request cancelled','AbortError'));controller.signal.addEventListener('abort',onAbort,{once:true});});
      let token;try{token=await Promise.race([user.getIdToken(refresh),interrupted]);}finally{controller.signal.removeEventListener('abort',onAbort);}
      if(!str(token)||!token||/[\r\n]/.test(token))throw new ApiUnauthorized();headers.Authorization='Bearer '+token;
    }
    const init={method:op.method,headers,cache:'no-store',credentials:'omit',redirect:'error',signal:controller.signal};
    return fetch(url.href,init);
  }
  try{
    let res=await send(false);
    if(res.status===401&&op.method==='GET'&&user)res=await send(true);
    if(res.status===401)throw new ApiUnauthorized();
    if(res.status===403){let error={};try{error=await res.json();}catch(_){} const allowed=['recent_authentication_required','email_verification_required'];throw new ApiForbidden(allowed.includes(error.error)?error.error:'access_denied');}
    if(!res.ok)throw new ApiUnavailable('The learning service could not complete this request.');
    if(!/^application\/json(?:\s*;|$)/i.test(res.headers.get('content-type')||''))throw new ApiUnavailable('The learning service returned an unexpected response.');
    let value;try{value=await res.json();}catch(_){throw new ApiUnavailable('The learning service returned an unexpected response.');}
    if(!validResponse(op.shape,value))throw new ApiUnavailable('The learning service returned an unexpected response.');
    return value;
  }catch(e){
    if(e instanceof ApiUnauthorized||e instanceof ApiUnavailable||e instanceof ApiForbidden)throw e;
    if(['auth/user-token-expired','auth/user-disabled','auth/invalid-user-token'].includes(e?.code))throw new ApiUnauthorized();
    throw new ApiUnavailable();
  }finally{clearTimeout(timer);options.signal?.removeEventListener('abort',cancel);}
}
