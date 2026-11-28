from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];h=(R/'preview-standalone.html').read_text()
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':1050},reduced_motion='reduce');errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.set_content(h)
 assert p.locator('.ht-book').count()==5;assert p.locator('a.ht-book').count()==3;assert p.locator('.ht-adult-step').count()==5
 p.locator('#ht-query').fill('स्वर');assert p.locator('[data-ht-entry]:visible').count()>0;assert p.locator('[data-ht-result]').inner_text().startswith('4 ') or 'matching' in p.locator('[data-ht-result]').inner_text()
 p.locator('#ht-query').fill('notfoundxyz');assert p.locator('[data-ht-entry]:visible').count()==0
 p.locator('[data-ht-clear]').click();assert p.locator('.ht-group:visible').count()>=10
 p.locator('#hh-topics summary').click();assert p.locator('#hh-topics').get_attribute('open') is not None;p.locator('#hh-topics summary').click()
 for w in [320,375,390,430,768,1024,1280,1440,1920]:
  p.set_viewport_size({'width':w,'height':1000});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),w
 p.set_viewport_size({'width':1440,'height':1050});p.evaluate('scrollTo(0,0)');p.screenshot(path=str(R/'preview/desktop.png'),full_page=True,animations='disabled');p.locator('#theme').click();p.screenshot(path=str(R/'preview/dark.png'),full_page=True,animations='disabled');p.set_viewport_size({'width':390,'height':844});p.locator('#theme').click();p.screenshot(path=str(R/'preview/mobile.png'),full_page=True,animations='disabled');assert not errors,errors
 ctx=b.new_context(java_script_enabled=False);n=ctx.new_page();n.set_content(h);assert n.locator('.ht-search').is_hidden();n.locator('#hh-topics summary').click();assert n.locator('#hh-topics a:visible').count()==34;ctx.close();b.close()
print('PASS: textbook states, Hindi search, empty result, details, dark mode, nine viewport widths, JS-free links')
