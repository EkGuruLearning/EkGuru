/* Run against a local static server with playwright-core and CHROMIUM_PATH. */
import assert from 'node:assert/strict';
import {chromium} from 'playwright-core';
import {mkdirSync} from 'node:fs';
const base=process.env.EKGURU_BASE||'http://127.0.0.1:8014';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/tmp/chromium',args:['--no-sandbox','--no-zygote','--disable-dev-shm-usage']});
const screenshots=process.env.VISUAL_SCREENSHOTS;if(screenshots)mkdirSync(screenshots,{recursive:true});
try{
 for(const [slug,count] of [['swar',13],['vyanjan-1',10],['vyanjan-2',10],['vyanjan-3',16]]){
  const ctx=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});const p=await ctx.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto(base+`/learn/hindi/foundation/${slug}/`,{waitUntil:'networkidle'});
  // A first-time visitor must be able to dismiss the real privacy notice before
  // reaching lesson controls on a small viewport; do not bypass it by force.
  await p.locator('#consent-reject').click();
  await p.getByRole('button',{name:'Whole lesson'}).click();
  const imgs=p.locator('img.fd-picture');assert.equal(await imgs.count(),count);
  for(let i=0;i<count;i++){
   const img=imgs.nth(i);await img.scrollIntoViewIfNeeded();await img.evaluate(el=>el.decode());
   assert(await img.evaluate(el=>el.complete&&el.naturalWidth>0));assert.match(await img.getAttribute('alt'),/^चित्र: .+/);
  }
  if(slug==='vyanjan-1'){
   await p.locator('.fd-air-demo summary').click();assert.equal(await p.locator('.fd-air-demo').getAttribute('open'),'');
   assert.equal(await p.locator('.fd-air-demo .air').first().evaluate(el=>getComputedStyle(el).animationName),'none');
   assert.match(await p.locator('.fd-air-demo').innerText(),/not an anatomical or measured diagram/);
  }
  assert.deepEqual(errors,[]);await ctx.close();
 }
 for(const width of [320,375,390,430,768,1024,1280,1440,1920]){
  const p=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});await p.goto(base+'/learn/hindi/foundation/swar/',{waitUntil:'networkidle'});
  await p.locator('#consent-reject').click();
  await p.getByRole('button',{name:'Whole lesson'}).click();await p.locator('img.fd-picture').first().scrollIntoViewIfNeeded();
  assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'horizontal overflow '+width);
  await p.locator('img.fd-picture').first().evaluate(el=>el.decode());assert(await p.locator('img.fd-picture').first().evaluate(el=>el.naturalWidth>0));
  if(screenshots&&[390,1440].includes(width))await p.screenshot({path:`${screenshots}/lesson-${width}.png`});await p.close();
 }
 const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const p=await ctx.newPage();
 await p.goto(base+'/learn/hindi/foundation/swar/');const first=p.locator('img.fd-picture').first();await first.scrollIntoViewIfNeeded();await first.evaluate(el=>el.decode());assert(await first.isVisible());assert.equal(await first.getAttribute('alt'),'चित्र: अनार');await ctx.close();
 console.log('PASS real Chromium: 49 illustration decodes across four chapters; reduced-motion airflow, nine widths and no-JS picture reading');
}finally{await browser.close()}
