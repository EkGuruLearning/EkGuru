import {test,afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {request,apiReady} from '../js/student/api.js';
const original=globalThis.fetch;
afterEach(()=>{globalThis.fetch=original});
const profile={id:'synthetic-user',email:null,emailVerified:true,displayName:'Student',photoUrl:null,role:'student'};
const course={id:'free',title_hi:'हिंदी',title_en:'Hindi',access_level:'free',enrolled:true,startedLessons:0,completedSegments:null};
const segment={segment_id:'s',course_id:'free',phase_id:'p',chapter_id:'c',lesson_id:'one',kind:'text',access_level:'free',text_hi:'नमस्ते',text_en:'Hello',translation_status:'reviewed',public_route:null};
const fixtures={session:{user:profile},logout:{loggedOut:true},profile:{profile},updateProfile:{profile},dashboard:{profile,courses:[course]},progress:{accepted:1},lesson:{courseId:'free',lessonId:'one',segments:[segment],body:null,contentVersion:null}};
const user={getIdToken:async()=> 'offline-synthetic-token'};
function respond(value,status=200){return new Response(JSON.stringify(value),{status,headers:{'content-type':'application/json'}})}
test('all seven operations use only their documented paths and methods',async()=>{
 const observed=[];globalThis.fetch=async(url,init)=>{observed.push({url,init});const key=['session','logout','profile','updateProfile','dashboard','progress','lesson'][observed.length-1];return respond(fixtures[key])};
 const cases=[['session'],['logout'],['profile'],['updateProfile',{body:{displayName:'Student'}}],['dashboard'],['progress',{body:{courseId:'free',lessonId:'one',completed:true}}],['lesson',{params:{courseId:'free',lessonId:'one',preview:true}}]];
 for(const [key,options] of cases){assert.equal(apiReady(key),true);assert.deepEqual(await request(key,user,options),fixtures[key]);}
 assert.deepEqual(observed.map(x=>[x.init.method,new URL(x.url).pathname]),[['GET','/v1/auth/session'],['POST','/v1/auth/logout'],['GET','/v1/profile'],['PATCH','/v1/profile'],['GET','/v1/dashboard'],['PUT','/v1/progress'],['GET','/v1/courses/free/lessons/one']]);
 assert.equal(new URL(observed[6].url).search,'?preview=1');
 for(const {url,init} of observed){assert.equal(init.headers.Authorization,'Bearer offline-synthetic-token');assert.equal(init.cache,'no-store');assert.equal(init.redirect,'error');assert.equal(init.credentials,'omit');assert.ok(!url.includes('offline-synthetic-token'));}
});
test('anonymous lesson has no authorization header',async()=>{globalThis.fetch=async(url,init)=>{assert.equal(init.headers.Authorization,undefined);return respond(fixtures.lesson)};await request('lesson',null,{params:{courseId:'free',lessonId:'one'}})});
test('reads refresh once on 401; mutations never replay',async()=>{let calls=0,refresh=[];globalThis.fetch=async()=>respond(fixtures.dashboard,++calls===1?401:200);await request('dashboard',{getIdToken:async force=>{refresh.push(force);return 'token'}});assert.deepEqual(refresh,[false,true]);assert.equal(calls,2);calls=0;globalThis.fetch=async()=>{calls++;return respond({error:'unauthorized'},401)};await assert.rejects(request('progress',user,{body:{courseId:'free',lessonId:'one',completed:true}}),{name:'ApiUnauthorized'});assert.equal(calls,1)});
test('invalid request is rejected before fetch',async()=>{let count=0;globalThis.fetch=async()=>{count++;throw Error('unexpected')};for(const [key,options] of [['updateProfile',{body:{displayName:'x',role:'admin'}}],['progress',{body:{courseId:'free',lessonId:'one',completed:true,userId:'other'}}],['progress',{body:{items:[]}}],['lesson',{params:{courseId:'../x',lessonId:'one'}}],['lesson',{params:{courseId:123,lessonId:'one'}}],['catalogue',{}]])await assert.rejects(request(key,user,options));assert.equal(count,0)});
test('forbidden and malformed responses fail closed without exposing error content',async()=>{globalThis.fetch=async()=>respond({error:'recent_authentication_required'},403);await assert.rejects(request('profile',user),e=>e.name==='ApiForbidden'&&e.code==='recent_authentication_required');globalThis.fetch=async()=>respond({profile:{role:'admin'}});await assert.rejects(request('profile',user),{name:'ApiUnavailable'});globalThis.fetch=async()=>new Response('not json',{status:200,headers:{'content-type':'text/html'}});await assert.rejects(request('dashboard',user),{name:'ApiUnavailable'})});
test('an expired Firebase token is unauthorized and cancellation does not send',async()=>{let calls=0;globalThis.fetch=async()=>{calls++;return respond({})};await assert.rejects(request('session',{getIdToken:async()=>{throw {code:'auth/user-token-expired'}}}),{name:'ApiUnauthorized'});const abort=new AbortController();abort.abort();await assert.rejects(request('session',user,{signal:abort.signal}),{name:'ApiUnavailable'});assert.equal(calls,0)});
