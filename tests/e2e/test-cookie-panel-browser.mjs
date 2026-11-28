#!/usr/bin/env node
// Run against a local server: COOKIE_TEST_BASE=http://127.0.0.1:8015 node tests/e2e/test-cookie-panel-browser.mjs
import assert from 'node:assert/strict';
import { chromium } from 'playwright-core';
const base = process.env.COOKIE_TEST_BASE || 'http://127.0.0.1:8015';
const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/tmp/chromium', args:['--no-sandbox']});
try {
  for (const [width,height] of [[320,568],[375,667],[390,844],[768,1024],[1440,900]]) {
    const context = await browser.newContext({viewport:{width,height},reducedMotion:'reduce'});
    const page = await context.newPage();
    await page.route('**/*', route => route.request().url().startsWith(base) ? route.continue() : route.abort());
    const errors=[]; page.on('pageerror', e=>errors.push(e.message));
    await page.goto(base + '/learn/hindi/',{waitUntil:'domcontentloaded'});
    const panel=page.locator('#ekguru-consent'); await panel.waitFor({state:'visible'});
    await page.waitForFunction(() => document.querySelector('#ekguru-consent').classList.contains('show'));
    const bounds=await panel.boundingBox();
    assert.ok(bounds.x>=0 && bounds.y>=0 && bounds.x+bounds.width<=width+1 && bounds.y+bounds.height<=height+1,`panel bounds at ${width}: ${JSON.stringify(bounds)}`);
    assert.equal(await page.locator('#ekguru-cookie-settings').isVisible(),false);
    assert.equal(await page.locator('#cc-analytics').isChecked(),true);
    assert.equal(await page.locator('#cc-advertising').isDisabled(),true);
    assert.equal(await page.locator('#consent-customize').getAttribute('aria-expanded'),'false');
    await page.locator('#consent-customize').focus(); await page.keyboard.press('Enter');
    assert.equal(await page.locator('#consent-customize').getAttribute('aria-expanded'),'true');
    assert.equal(await page.evaluate(()=>document.activeElement.id),'consent-custom-title');
    await page.locator('#consent-cancel-custom').click();
    assert.equal(await page.locator('#consent-customize').getAttribute('aria-expanded'),'false');
    assert.equal(await page.evaluate(()=>document.activeElement.id),'consent-customize');
    if(width===390 || width===1440) await page.screenshot({path:`.artifacts/cookie-panel-${width}.png`});
    await page.locator('#consent-reject').click();
    assert.equal(await page.locator('#ekguru-cookie-settings').isVisible(),true);
    assert.equal(await page.evaluate(()=>document.activeElement.id),'ekguru-cookie-settings');
    assert.deepEqual(await page.evaluate(()=>{let c=JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3'));return [c.functional,c.analytics,c.advertising]}),[true,false,false]);
    await page.reload({waitUntil:'domcontentloaded'}); await page.waitForTimeout(1400);
    assert.equal(await panel.count(),0);
    await page.locator('#ekguru-cookie-settings').click();
    assert.equal(await page.locator('#cc-analytics').isChecked(),false);
    assert.equal(await page.locator('#consent-customize').getAttribute('aria-expanded'),'true');
    await page.locator('#cc-functional').uncheck(); await page.locator('#consent-save-custom').click();
    assert.deepEqual(await page.evaluate(()=>{let c=JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3'));return [c.functional,c.analytics,c.advertising]}),[false,false,false]);
    assert.deepEqual(errors,[]); await context.close(); console.log(`PASS ${width}×${height}: responsive panel, keyboard, persistence and preferences`);
  }
  const context=await browser.newContext({viewport:{width:390,height:844}}), page=await context.newPage();
  await page.route('**/*', route => route.request().url().startsWith(base) ? route.continue() : route.abort());
  await page.goto(base + '/', {waitUntil:'domcontentloaded'}); await page.locator('#consent-close').click();
  assert.equal(await page.evaluate(()=>localStorage.getItem('ekguru_cookie_consent_v3')),null);
  await page.locator('#ekguru-cookie-settings').click(); await page.locator('#consent-accept-all').click();
  assert.deepEqual(await page.evaluate(()=>{let c=JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3'));return [c.functional,c.analytics,c.advertising]}),[true,true,false]);
  await page.evaluate(()=>window.EKGURU_COOKIES.withdrawOptional());
  assert.deepEqual(await page.evaluate(()=>{let c=JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3'));return [c.functional,c.analytics,c.advertising]}),[false,false,false]);
  console.log('PASS dismiss without choice, accept and withdrawal'); await context.close();
} finally { await browser.close(); }
