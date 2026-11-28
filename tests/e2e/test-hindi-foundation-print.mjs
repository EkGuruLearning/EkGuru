/* Optional browser gate: provide playwright-core, CHROMIUM_PATH and EKGURU_BASE.
   Produces reviewable PDFs in .artifacts; no PDF or external font is published. */
import assert from 'node:assert/strict';
import {mkdirSync, readFileSync} from 'node:fs';
import {chromium} from 'playwright-core';
const base=process.env.EKGURU_BASE||'http://127.0.0.1:8015';
const output=process.env.PRINT_TEST_OUTPUT||'.artifacts/hindi-print'; mkdirSync(output,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/tmp/chromium',args:['--no-sandbox','--no-zygote','--disable-dev-shm-usage']});
try {
  for(const [format,js] of [['A4',true],['Letter',true],['A4',false]]) {
    const context=await browser.newContext({javaScriptEnabled:js,viewport:{width:1200,height:900},reducedMotion:'reduce'});
    const page=await context.newPage();
    await page.route('**/*',route=>route.request().url().startsWith(base)?route.continue():route.abort());
    const errors=[];page.on('pageerror',error=>errors.push(error.message));
    await page.goto(base+'/learn/hindi/foundation/swar/',{waitUntil:'networkidle'});
    await page.emulateMedia({media:'print'});
    await page.evaluate(()=>document.fonts.ready);
    assert.match(await page.locator('.fd-letter .lt').first().evaluate(e=>getComputedStyle(e).fontFamily),/TextbookDevanagari/);
    assert.equal(await page.locator('.fd-letter').first().evaluate(e=>getComputedStyle(e).breakInside),'avoid');
    if(js){
      assert.match(await page.locator('.trace-cell text').first().evaluate(e=>getComputedStyle(e).fontFamily),/TextbookDevanagari/);
      assert.equal(await page.locator('.trace-cell').last().evaluate(e=>getComputedStyle(e).opacity),'1');
      assert.ok(await page.locator('.bk-ex').count());
      assert.equal(await page.locator('.bk-ex').first().evaluate(e=>getComputedStyle(e).display),'none');
    }
    const file=`${output}/vowels-${format}-${js?'js':'no-js'}.pdf`;
    await page.pdf({path:file,format,printBackground:true,margin:{top:'12mm',bottom:'12mm',left:'12mm',right:'12mm'}});
    const pdf=readFileSync(file);assert.ok(pdf.length>10000);assert.ok(pdf.includes(Buffer.from('NotoSansDevanagari')),'Hindi font embedded');
    assert.deepEqual(errors,[]); console.log(`PASS ${format} ${js?'JS':'no JS'}: local Hindi font, intact cards and printable lesson`);
    await context.close();
  }
} finally {await browser.close();}
