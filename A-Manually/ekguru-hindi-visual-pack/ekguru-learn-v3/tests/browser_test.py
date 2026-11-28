from playwright.sync_api import sync_playwright
from pathlib import Path
import os,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from lib.learn_catalogue_v3 import render_catalogue
p=ROOT/'preview-standalone.html'
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None),args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1050},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(p.read_text(),wait_until='load');print('cards',page.locator('[data-lc-card]:visible').count());assert page.locator('[data-lc-card]:visible').count()==18
 page.locator('#lc-search').fill('বাংলা');assert page.locator('[data-lc-card]:visible').count()==1
 page.locator('.lc-clear').click();page.locator('[data-lc-filter=world]').click();assert page.locator('[data-lc-card]:visible').count()==10
 page.locator('#lc-search').fill('francais');assert page.locator('[data-lc-card]:visible').count()==1
 page.locator('#lc-search').fill('zzzz');assert page.locator('.lc-empty').is_visible()
 page.locator('.lc-clear').click();page.locator('[data-lc-filter=all]').click();assert page.locator('[data-lc-card]:visible').count()==18
 for w in [320,375,390,430,768,1024,1280,1440,1920]:
  page.set_viewport_size({'width':w,'height':1000});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),w
 page.set_viewport_size({'width':1440,'height':1050});page.screenshot(path=str(ROOT/'preview/desktop.png'),animations='disabled');page.locator('#theme').click();assert page.locator('html').get_attribute('data-theme')=='dark';page.screenshot(path=str(ROOT/'preview/dark.png'),animations='disabled');page.set_viewport_size({'width':390,'height':844});page.locator('#theme').click();page.screenshot(path=str(ROOT/'preview/mobile.png'),animations='disabled',full_page=True)
 assert not errors,errors
 # Use real renderer with synthetic records; fixture does not enter production.
 rows=[(f'fixture-{i}',f'x-{i}',f'Fixture {i:02}',f'Script {i}',[],[],[],[]) for i in range(50)]
 fragment=render_catalogue(rows,[],{},'',lambda t:'/'+t+'/')
 import re
 fragment=re.sub(r'<link rel="stylesheet"[^>]*>','',fragment);fragment=re.sub(r'<script src="[^"]+" defer></script>','',fragment)
 html=p.read_text(); start=html.index('<!-- ekguru:learn-index:start -->');end=html.index('<!-- ekguru:learn-index:end -->')+len('<!-- ekguru:learn-index:end -->')
 page.set_content(html[:start]+fragment+html[end:]);assert page.locator('[data-lc-card]:visible').count()==12
 page.locator('#li-indian .lc-more-languages').click();assert page.locator('[data-lc-card]:visible').count()==24
 page.locator('#lc-search').fill('Fixture 49');assert page.locator('[data-lc-card]:visible').count()==1
 assert page.locator('[data-lc-card]:visible').get_attribute('href')=='/learn/fixture-49/'
 assert not errors,errors
 ctx=b.new_context(java_script_enabled=False);no=ctx.new_page();no.set_content(p.read_text());assert no.locator('[data-lc-card]:visible').count()==18;assert no.locator('.lc-toolbar').is_hidden();ctx.close();b.close()
print('PASS: standalone browser search, filter, dark theme, no JS, nine widths, 50-record expansion fixture')
