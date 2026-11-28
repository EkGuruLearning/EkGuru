from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    raw=(root/'preview.html').read_text();page.set_content(raw);page.wait_for_timeout(800)
    page.screenshot(path=str(root/'desktop.png'),full_page=True,animations='disabled')
    page.screenshot(path=str(root/'hero.png'),animations='disabled')
    assert page.locator('.lang').count()==18
    assert page.locator('.lang:visible').count()==16
    page.locator('[data-language-group=World] .show-more').click();assert page.locator('.lang:visible').count()==18
    page.locator('#language-search').fill('日本語');assert page.locator('.lang:visible').count()==1
    page.locator('#language-search').fill('');page.locator('[data-filter=Indian]').click();assert page.locator('.lang:visible').count()==8
    page.locator('[data-filter=All]').click();page.locator('#theme').click();assert page.locator('html').get_attribute('data-theme')=='dark';page.screenshot(path=str(root/'dark.png'),full_page=True,animations='disabled');page.locator('#theme').click()
    for width in [320,375,390,430,768,1024,1280,1440,1920]:
        page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),width
    page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(root/'mobile.png'),full_page=True,animations='disabled')
    assert not errors,errors
    nojs=browser.new_page(java_script_enabled=False);nojs.set_content(raw);assert nojs.locator('.lang:visible').count()==18
    browser.close()
print('PASS: 18 language links, progressive expansion, native-script search, category filter, dark mode, 9 responsive widths, no-JS fallback, no page errors')
