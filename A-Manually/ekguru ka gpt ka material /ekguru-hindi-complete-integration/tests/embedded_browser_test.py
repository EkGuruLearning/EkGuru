from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[1];O=R/'screenshots';O.mkdir(exist_ok=True);html=(R/'preview.html').read_text()
# Same-origin navigation is blocked in this environment; inject an explicit test storage shim.
shim='''<script>window.__testStore=window.__testStore||{};Object.defineProperty(window,'localStorage',{value:{getItem:k=>window.__testStore[k]??null,setItem:(k,v)=>window.__testStore[k]=v}})</script>'''
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce');errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.set_content(html.replace('<head>','<head>'+shim,1));assert p.locator('.result').count()==24
 p.screenshot(path=str(O/'desktop.png'),full_page=False);p.locator('#more').click();assert p.locator('.result').count()==48
 p.locator('#search').fill('संधि');assert p.locator('.result').count()>0;p.locator('#search-book').select_option('advanced');p.locator('#search-type').select_option('lesson');assert p.locator('.result').count()>0
 p.locator('.result button').first.click();p.locator('#search').fill('');p.locator('#search-book').select_option('all');p.locator('#search-type').select_option('saved');assert p.locator('.result').count()==1
 p.locator('#practice-book').select_option('kids');first=p.locator('#face').inner_text();p.locator('#reveal').click();assert p.locator('#meaning').is_visible();p.locator('[data-rate="1"]').click();assert p.locator('#face').inner_text()!=first
 p.locator('#dict-reveal').click();answer=p.locator('#dict-answer').inner_text().split(' — ')[0];p.locator('#dict-input').fill(answer);p.locator('#dict-check').click();assert 'Exact text match' in p.locator('#dict-status').inner_text()
 p.locator('#practice').scroll_into_view_if_needed();p.screenshot(path=str(O/'practice.png'),full_page=False);p.locator('#theme').click();assert p.locator('html').get_attribute('data-theme')=='dark';p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'dark.png'));p.locator('#theme').click();p.locator('#large').click();assert 'large' in p.locator('html').get_attribute('class');p.locator('#large').click()
 p.evaluate("localStorage.setItem('ekguru:kids:done:v1',JSON.stringify(['kids-01-01','kids-01-01','invalid']));localStorage.setItem('ekguru:kids:last:v1',JSON.stringify('kids-01-01'));window.dispatchEvent(new Event('storage'))");assert p.locator('#total-done').inner_text()=='1 / 480';assert p.locator('[data-book="kids"] [data-resume]').is_visible()
 p.locator('#import').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps({'saved':['javascript:alert(1)'],'reviews':{},'theme':'light','large':False}).encode()});p.wait_for_function("document.querySelector('#backup-status').textContent.includes('restored')");p.locator('#search-type').select_option('saved');assert p.locator('.result').count()==0
 p.locator('#search-type').select_option('all');assert p.evaluate("JSON.parse(localStorage.getItem('ekguru:kids:done:v1')).length") ==3
 for w in [320,375,390,430,768,1024,1280,1440,1920]:
  p.set_viewport_size({'width':w,'height':900});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),w
 p.set_viewport_size({'width':390,'height':844});p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'mobile.png'),full_page=False);assert not errors,errors
 c=b.new_context(java_script_enabled=False);n=c.new_page();n.set_content(html);assert n.locator('.directory a').count()==965;assert n.locator('.course a').count()>=6;c.close();b.close()
print('PASS: embedded Chromium search, filters, bookmarks, flashcard ratings, exact-text dictation, theme, text scaling, progress aggregation with storage shim, import validation, 9 widths, no-JS directory. Hosted navigation and real storage persistence NOT verified.')
