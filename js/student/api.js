// Only the seven operations in the reviewed Student OpenAPI 1.0.0 are allowed.
// The intended origin does not establish that the Worker is deployed.
import { studentConfig } from './config.js';
const ORIGIN='https://api.ekguru.shop';
const ID=/^[a-z0-9-]+$/;
const operations=Object.freeze({
  session:{method:'GET',path:'/v1/auth/session',shape:'session'},
  logout:{method:'POST',path:'/v1/auth/logout',shape:'logout'},
  profile:{method:'GET',path:'/v1/profile',shape:'profile'},
  updateProfile:{method:'PATCH',path:'/v1/profile',shape:'profile'},
  dashboard:{method:'GET',path:'/v1/dashboard',shape:'dashboard'},
  progress:{method:'PUT',path:'/v1/progress',shape:'progress'},
  lesson:{method:'GET',shape:'lesson',anonymous:true}
});
export class ApiUnavailable extends Error { constructor(message='The learning service is temporarily unavailable.') { super(message); this.name='ApiUnavailable'; } }
export class ApiUnauthorized extends Error { constructor() { super('Your session could not be verified. Please sign in again.'); this.name='ApiUnauthorized'; } }
export class ApiForbidden extends Error { constructor(code='access_denied') { super('This request is not permitted.'); this.name='ApiForbidden'; this.code=code; } }
const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
const str=x=>typeof x==='string';
const nullableString=x=>x===null||str(x);
function validProfile(p,photo=true){return object(p)&&str(p.id)&&nullableString(p.email)&&typeof p.emailVerified==='boolean'&&nullableString(p.displayName)&&(!photo||nullableString(p.photoUrl))&&['student','admin'].includes(p.role);}
function validCourse(c){return object(c)&&str(c.id)&&str(c.title_hi)&&str(c.title_en)&&['free','preview','premium'].includes(c.access_level)&&(typeof c.enrolled==='boolean'||Number.isInteger(c.enrolled))&&Number.isInteger(c.startedLessons)&&(c.completedSegments===null||Number.isInteger(c.completedSegments));}
function validSegment(s){return object(s)&&['segment_id','course_id','phase_id','chapter_id','lesson_id','kind','text_hi','text_en'].every(k=>str(s[k]))&&['free','preview','premium'].includes(s.access_level)&&['reviewed','pending'].includes(s.translation_status)&&nullableString(s.public_route);}
function validResponse(shape,v,params){
  if(!object(v))return false;
  if(shape==='session')return validProfile(v.user);
  if(shape==='profile')return validProfile(v.profile);
  if(shape==='logout')return v.loggedOut===true;
  if(shape==='dashboard')return validProfile(v.profile,false)&&Array.isArray(v.courses)&&v.courses.every(validCourse);
  if(shape==='progress')return Number.isInteger(v.accepted)&&v.accepted>=1&&v.accepted<=50;
  if(shape==='lesson')return v.courseId===params.courseId&&v.lessonId===params.lessonId&&Array.isArray(v.segments)&&v.segments.length<=100&&v.segments.every(validSegment)&&(v.body===null||object(v.body))&&nullableString(v.contentVersion);
  return false;
}
function progressItem(x){return object(x)&&Object.keys(x).every(k=>['courseId','lessonId','segmentId','completed'].includes(k))&&str(x.courseId)&&ID.test(x.courseId)&&str(x.lessonId)&&ID.test(x.lessonId)&&typeof x.completed==='boolean'&&(!Object.hasOwn(x,'segmentId')||str(x.segmentId));}
function validateBody(key,body){
  if(key==='updateProfile')return object(body)&&Object.keys(body).length===1&&str(body.displayName)&&body.displayName.length<=80;
  if(key==='progress')return progressItem(body)||(object(body)&&Object.keys(body).length===1&&Array.isArray(body.items)&&body.items.length>=1&&body.items.length<=50&&body.items.every(progressItem));
  return body===undefined;
}
export function apiReady(key) { return studentConfig.workerOrigin===ORIGIN&&Object.hasOwn(operations,key); }
export async function request(key,user,options={}) {
  const op=Object.hasOwn(operations,key)?operations[key]:null;
  if(!op||!apiReady(key))throw new ApiUnavailable('The learning service is not connected.');
  if(!user&&!op.anonymous)throw new ApiUnauthorized();
  if(!validateBody(key,options.body))throw new ApiUnavailable('The request is invalid.');
  let path=op.path,params=options.params||{};
  if(key==='lesson'){
    if(!str(params.courseId)||!ID.test(params.courseId)||!str(params.lessonId)||!ID.test(params.lessonId))throw new ApiUnavailable('The lesson identifier is invalid.');
    path='/v1/courses/'+encodeURIComponent(params.courseId)+'/lessons/'+encodeURIComponent(params.lessonId);
    if(params.preview===true)path+='?preview=1';else if(params.preview!==undefined&&params.preview!==false)throw new ApiUnavailable('The lesson request is invalid.');
  }
  const url=new URL(path,ORIGIN);if(url.origin!==ORIGIN)throw new ApiUnavailable('Invalid service configuration.');
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
    if(options.body!==undefined){headers['Content-Type']='application/json';init.body=JSON.stringify(options.body);}
    return fetch(url.href,init);
  }
  try{
    let res=await send(false);
    if(res.status===401&&op.method==='GET'&&user)res=await send(true);
    if(res.status===401)throw new ApiUnauthorized();
    if(res.status===403){let error={};try{error=await res.json();}catch(_){} const allowed=['recent_authentication_required','email_verification_required','course_access_denied'];throw new ApiForbidden(allowed.includes(error.error)?error.error:'access_denied');}
    if(!res.ok)throw new ApiUnavailable('The learning service could not complete this request.');
    if(!/^application\/json(?:\s*;|$)/i.test(res.headers.get('content-type')||''))throw new ApiUnavailable('The learning service returned an unexpected response.');
    let value;try{value=await res.json();}catch(_){throw new ApiUnavailable('The learning service returned an unexpected response.');}
    if(!validResponse(op.shape,value,params))throw new ApiUnavailable('The learning service returned an unexpected response.');
    return value;
  }catch(e){
    if(e instanceof ApiUnauthorized||e instanceof ApiUnavailable||e instanceof ApiForbidden)throw e;
    if(['auth/user-token-expired','auth/user-disabled','auth/invalid-user-token'].includes(e?.code))throw new ApiUnauthorized();
    throw new ApiUnavailable();
  }finally{clearTimeout(timer);options.signal?.removeEventListener('abort',cancel);}
}
