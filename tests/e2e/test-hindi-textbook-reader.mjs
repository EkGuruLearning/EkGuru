/* Provide playwright-core, CHROMIUM_PATH and EKGURU_BASE. */
import assert from 'node:assert/strict';
import {chromium} from 'playwright-core';
import {mkdirSync} from 'node:fs';
const base=process.env.EKGURU_BASE || 'http://127.0.0.1:8013';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/tmp/chromium',headless:true,args:['--no-sandbox','--no-zygote','--disable-dev-shm-usage']});
const dir=process.env.TEXTBOOK_SCREENSHOTS;if(dir)mkdirSync(dir,{recursive:true});
try {
  for(const width of [320,375,390,430,768,1024,1280,1440,1920]) {
    const ctx=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});const p=await ctx.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
    await p.goto(base+'/learn/hindi/foundation/swar/',{waitUntil:'networkidle'});
    assert.equal(await p.locator('.htr-nav details').count(),1);assert.equal(await p.locator('.htr-nav [aria-current=page]').count(),1);
    await p.locator('.htr-nav summary').click();assert.equal(await p.locator('.htr-nav ol a').count(),18);
    assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'horizontal overflow at '+width);
    assert.deepEqual(errors,[],'runtime errors at '+width);
    if(dir && [390,1440].includes(width))await p.screenshot({path:`${dir}/reader-${width}.png`});
    await p.locator('.htr-nav a[href="/learn/hindi/foundation/vyanjan-1/"]').click();
    assert.equal(new URL(p.url()).pathname,'/learn/hindi/foundation/vyanjan-1/');
    assert.equal(await p.locator('.htr-nav [aria-current=page]').getAttribute('href'),'/learn/hindi/foundation/vyanjan-1/');
    await ctx.close();
  }
  const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const p=await ctx.newPage();
  await p.goto(base+'/learn/hindi/foundation/swar/');await p.locator('.htr-nav summary').click();
  assert.equal(await p.locator('.htr-nav ol a').count(),18);assert.equal(await p.locator('h1').isVisible(),true);
  assert.equal(await p.getByText('Each letter with its word').isVisible(),true);
  await ctx.close();console.log('PASS textbook chapter navigation: 9 widths, real navigation and no-JS reading');
} finally {await browser.close();}
