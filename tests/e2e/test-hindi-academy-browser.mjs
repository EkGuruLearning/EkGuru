/* Optional: install playwright-core and provide CHROMIUM_PATH (no project dependency). */
import assert from 'node:assert/strict';
import { chromium } from 'playwright-core';
import { mkdirSync } from 'node:fs';
const base=process.env.EKGURU_BASE || 'http://127.0.0.1:8010';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/tmp/chromium',headless:true,args:['--no-sandbox','--no-zygote','--disable-dev-shm-usage']});
const screenshots=process.env.ACADEMY_SCREENSHOTS;
if(screenshots) mkdirSync(screenshots,{recursive:true});
try {
  for(const width of [320,375,390,430,768,1024,1280,1440,1920]){
    const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(base+'/learn/hindi/',{waitUntil:'networkidle'});
    for (const route of ['foundation/', 'beginner/', 'elementary/', 'intermediate/', 'advanced/']) assert((await page.locator(`.hh-card[href="${route}"]`).count()) >= 1,route);
    assert.equal(await page.locator('#academy-home, .hh-archive').count(),0,'no duplicate homepage');
    assert.equal(await page.locator('#hh-topics').count(),1,'legacy deep link preserved');
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth),true,`overflow ${width}`);
    assert.deepEqual(errors,[],`errors ${width}`);
    if(screenshots && [390,1440].includes(width)) await page.screenshot({path:`${screenshots}/hub-${width}.png`});
    await page.close();
  }
  const ctx=await browser.newContext({viewport:{width:390,height:844}});const page=await ctx.newPage();
  await page.goto(base+'/learn/hindi/');
  await page.goto(base+'/learn/hindi/academy/catalogue/',{waitUntil:'networkidle'});
  await page.waitForSelector('#catalogue-filters:not([hidden])');
  assert.match(await page.locator('#catalogue-count').innerText(),/19 of 19/);
  await page.locator('#catalogue-query').fill('mango');assert.match(await page.locator('#catalogue-count').innerText(),/1 of 19/);
  assert.equal(await page.locator('[data-catalogue-id="academy-vowels"]').isVisible(),true);
  await page.locator('#catalogue-reset').click();await page.locator('[data-filter="worksheet"]').selectOption('true');assert.match(await page.locator('#catalogue-count').innerText(),/1 of 19/);
  await page.locator('#catalogue-reset').click();await page.locator('[data-filter="worksheet"]').selectOption('false');assert.match(await page.locator('#catalogue-count').innerText(),/18 of 19/);
  await page.locator('#catalogue-reset').click();await page.locator('[data-filter="ages"]').selectOption('older-adults');assert.match(await page.locator('#catalogue-count').innerText(),/19 of 19/);
  await page.locator('#catalogue-reset').click();await page.locator('[data-filter="skills"]').selectOption('speaking');assert.match(await page.locator('#catalogue-count').innerText(),/1 of 19/);
  await page.locator('#catalogue-query').focus();await page.keyboard.type('missingxyz');assert.match(await page.locator('#catalogue-count').innerText(),/0 of 19/);
  if(screenshots) await page.screenshot({path:`${screenshots}/catalogue-390.png`});
  await page.goto(base+'/learn/hindi/academy/vowels/',{waitUntil:'networkidle'});
  await page.evaluate(()=>localStorage.setItem('ekguru:hindi:v1:progress',JSON.stringify({version:1,opened:[],completed:{old:{title:'Old',at:1}},quizzes:{}})));
  await page.reload();await page.locator('#lesson-complete button').click();await page.reload();
  assert(await page.evaluate(()=>{let x=JSON.parse(localStorage.getItem('ekguru:hindi:v1:progress'));return !!x.completed.old && !!x.completed['academy-vowels'];}));
  await page.locator('#trace').scrollIntoViewIfNeeded();let c=await page.locator('#trace').boundingBox();await page.mouse.move(c.x+30,c.y+30);await page.mouse.down();await page.mouse.move(c.x+120,c.y+130);await page.mouse.up();
  assert(await page.locator('#trace').evaluate(c=>Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data).some(v=>v!==0)));
  await page.locator('#undo').click();assert(!(await page.locator('#trace').evaluate(c=>Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data).some(v=>v!==0))));
  await page.goto(base+'/learn/hindi/',{waitUntil:'networkidle'});
  assert.equal(await page.locator('.hh-intro a[href="my-progress/"]').count(),1,'progress page remains available');
  await page.goto(base+'/learn/hindi/academy/worksheet/');await page.emulateMedia({media:'print'});
  assert.equal(await page.locator('.hdr').isVisible(),false);assert.equal(await page.locator('h1').isVisible(),true);assert.equal(await page.locator('[data-print]').isVisible(),false);
  if(screenshots) await page.screenshot({path:`${screenshots}/worksheet-print.png`});
  await ctx.close();
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:800}});const pg=await nojs.newPage();
  await pg.goto(base+'/learn/hindi/academy/catalogue/');assert.equal(await pg.locator('[data-catalogue-id]').count(),19);assert.equal(await pg.locator('[data-catalogue-id]').first().isVisible(),true);
  await pg.goto(base+'/learn/hindi/#hh-topics');assert.equal(await pg.locator('#hh-topics').isVisible(),true);assert.equal(await pg.locator('.hh-intro a[href="foundation/swar/"]').isVisible(),true);await nojs.close();
  console.log('PASS real Chromium: nine widths, reduced motion, filters, keyboard search, local progress, tracing, print CSS and no-JS links');
} finally {await browser.close();}
