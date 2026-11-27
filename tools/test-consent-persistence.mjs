#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { JSDOM } from 'jsdom';
const source = fs.readFileSync(new URL('../js/cookie-consent.js', import.meta.url), 'utf8');
const key='ekguru_cookie_consent_v3', date='ekguru_consent_date_v3';
async function boot(record, storedDate) {
  const dom=new JSDOM('<!doctype html><html><head></head><body><main>Lesson</main></body></html>',{url:'https://ekguru.shop/',runScripts:'outside-only',pretendToBeVisual:true});
  await new Promise(r=>dom.window.addEventListener('load',r,{once:true}));
  const w=dom.window;w.HTMLElement.prototype.scrollIntoView=()=>{};
  if(record!==undefined)w.localStorage.setItem(key,record);
  if(storedDate!==undefined)w.localStorage.setItem(date,storedDate);
  w.eval(source);return dom;
}
const choice={necessary:true,functional:false,analytics:false,advertising:false,timestamp:123456789};
let dom=await boot(JSON.stringify(choice),'original date');
let w=dom.window;
assert.equal(w.localStorage.getItem(key),JSON.stringify(choice));assert.equal(w.localStorage.getItem(date),'original date');
w.document.getElementById('ekguru-cookie-settings').click();
assert.equal(w.document.getElementById('cc-functional').checked,false);assert.equal(w.document.getElementById('cc-analytics').checked,false);
w.document.getElementById('cc-functional').checked=true;
w.document.getElementById('consent-save-custom').click();
const updated=w.localStorage.getItem(key), updatedDate=w.localStorage.getItem(date);
assert.equal(JSON.parse(updated).functional,true);assert.equal(JSON.parse(updated).analytics,false);
assert.equal(JSON.parse(updated).advertising,false);dom.window.close();
dom=await boot(updated,updatedDate);w=dom.window;
await new Promise(r=>setTimeout(r,1250));assert.equal(w.document.getElementById('ekguru-consent'),null);
assert.equal(w.localStorage.getItem(key),updated);assert.equal(w.localStorage.getItem(date),updatedDate);
w.document.getElementById('ekguru-cookie-settings').click();assert.equal(w.document.getElementById('cc-functional').checked,true);assert.equal(w.document.getElementById('cc-analytics').checked,false);
w.EKGURU_COOKIES.withdrawOptional();assert.equal(JSON.parse(w.localStorage.getItem(key)).functional,false);assert.equal(JSON.parse(w.localStorage.getItem(key)).analytics,false);dom.window.close();
console.log('PASS choices restore across visits without renewing consent date; settings and withdrawal remain accessible');
for(const invalid of ['{bad','[]','true','{"timestamp":1}','{"necessary":true,"functional":true,"analytics":"false","advertising":false,"timestamp":1}']){
 dom=await boot(invalid);w=dom.window;assert.equal(w.EKGURU_COOKIES.hasConsent(),false);assert.equal(w.localStorage.getItem(key),invalid);
 await new Promise(r=>setTimeout(r,1250));assert.ok(w.document.getElementById('ekguru-consent'));dom.window.close();
}
console.log('PASS invalid or incomplete records do not hide the choice banner or overwrite the old data');
dom=await boot(JSON.stringify(choice),'old date');w=dom.window;
const proto=w.Storage.prototype,set=proto.setItem;let failed=false;
proto.setItem=function(k,v){if(k===date&&!failed){failed=true;throw new Error('quota fixture');}return set.call(this,k,v);};
assert.equal(w.EKGURU_COOKIES.setConsent({functional:true,analytics:false,advertising:true}),false);
assert.equal(w.localStorage.getItem(key),JSON.stringify(choice));assert.equal(w.localStorage.getItem(date),'old date');
assert.match(w.document.getElementById('ekguru-consent-storage-status').textContent,/could not save/);
assert.equal(JSON.parse(w.document.documentElement.dataset.consent).advertising,false);
proto.setItem=set;assert.equal(w.EKGURU_COOKIES.setConsent({functional:false,analytics:false,advertising:false}),true);
assert.equal(w.document.getElementById('ekguru-consent-storage-status'),null);dom.window.close();
console.log('PASS partial storage failure rolls back persisted record/date and warns; retry can save; no forced advertising consent');
