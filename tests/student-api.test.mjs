import {test,afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {request,apiReady} from '../js/student/api.js';
const original=globalThis.fetch;
afterEach(()=>{globalThis.fetch=original});
const profile={id:'synthetic-user',email:null,emailVerified:true,displayName:'Student',photoUrl:null,role:'student'};
const user={getIdToken:async()=> 'offline-synthetic-token'};
function respond(value,status=200){return new Response(JSON.stringify(value),{status,headers:{'content-type':'application/json'}})}
test('only session and logout use their documented paths and methods',async()=>{
 const observed=[];globalThis.fetch=async(url,init)=>{observed.push({url,init});return respond(observed.length===1?{user:profile}:{loggedOut:true})};
 assert.deepEqual(await request('session',user),{user:profile});assert.deepEqual(await request('logout',user),{loggedOut:true});
 assert.deepEqual(observed.map(x=>[x.init.method,new URL(x.url).pathname]),[['GET','/v1/auth/session'],['POST','/v1/auth/logout']]);
 for(const {url,init} of observed){assert.equal(init.headers.Authorization,'Bearer offline-synthetic-token');assert.equal(init.cache,'no-store');assert.equal(init.redirect,'error');assert.equal(init.credentials,'omit');assert.ok(!url.includes('offline-synthetic-token'));assert.equal(init.body,undefined);}
 for(const key of ['profile','updateProfile','dashboard','progress','lesson','catalogue'])assert.equal(apiReady(key),false);
});
test('authentication is required before either request is sent',async()=>{let calls=0;globalThis.fetch=async()=>{calls++;throw Error('unexpected')};for(const key of ['session','logout'])await assert.rejects(request(key,null),{name:'ApiUnauthorized'});assert.equal(calls,0)});
test('session retries once on 401; logout never replays',async()=>{let calls=0,refresh=[];globalThis.fetch=async()=>respond({user:profile},++calls===1?401:200);await request('session',{getIdToken:async force=>{refresh.push(force);return 'token'}});assert.deepEqual(refresh,[false,true]);assert.equal(calls,2);calls=0;globalThis.fetch=async()=>{calls++;return respond({error:'unauthorized'},401)};await assert.rejects(request('logout',user),{name:'ApiUnauthorized'});assert.equal(calls,1)});
test('unknown operations and extra parameters are rejected before fetch',async()=>{let count=0;globalThis.fetch=async()=>{count++;throw Error('unexpected')};for(const [key,options] of [['profile',{}],['dashboard',{}],['progress',{}],['lesson',{}],['session',{body:{role:'admin'}}],['logout',{params:{extra:'x'}}]])await assert.rejects(request(key,user,options));assert.equal(count,0)});
test('forbidden and malformed responses fail closed',async()=>{globalThis.fetch=async()=>respond({error:'email_verification_required'},403);await assert.rejects(request('session',user),e=>e.name==='ApiForbidden'&&e.code==='email_verification_required');globalThis.fetch=async()=>respond({user:{role:'admin'}});await assert.rejects(request('session',user),{name:'ApiUnavailable'});globalThis.fetch=async()=>new Response('not json',{status:200,headers:{'content-type':'text/html'}});await assert.rejects(request('session',user),{name:'ApiUnavailable'});globalThis.fetch=async()=>respond({loggedOut:false});await assert.rejects(request('logout',user),{name:'ApiUnavailable'})});
test('expired Firebase token and cancellation do not send',async()=>{let calls=0;globalThis.fetch=async()=>{calls++;return respond({})};await assert.rejects(request('session',{getIdToken:async()=>{throw {code:'auth/user-token-expired'}}}),{name:'ApiUnauthorized'});const abort=new AbortController();abort.abort();await assert.rejects(request('session',user,{signal:abort.signal}),{name:'ApiUnavailable'});assert.equal(calls,0)});
