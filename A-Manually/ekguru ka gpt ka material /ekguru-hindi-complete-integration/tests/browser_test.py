from pathlib import Path
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright
import mimetypes,json
R=Path(__file__).resolve().parents[1];S=R/'site';O=R/'screenshots';O.mkdir(exist_ok=True);U='https://ekguru-preview.invalid/learn/hindi/studio/'
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);ctx=b.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce');p=ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 def local(r):
  u=urlsplit(r.request.url); f=(S/unquote(u.path.lstrip('/'))).resolve(); f=f/'index.html' if f.is_dir() else f
  if u.hostname!='ekguru-preview.invalid' or not f.is_relative_to(S) or not f.is_file():r.fulfill(status=404,body='Not in local package');return
  r.fulfill(status=200,body=f.read_bytes(),content_type=mimetypes.guess_type(f.name)[0] or 'application/octet-stream')
 ctx.route('**/*',local);p.goto(U);p.wait_for_selector('.result');assert p.locator('.result').count()==24
 p.locator('#more').click();assert p.locator('.result').count()==48
 p.locator('#search').fill('संधि');assert p.locator('.result').count()>0;assert '0 results' not in p.locator('#result-count').inner_text().split(' · ')[0]
 p.locator('#search-book').select_option('advanced');p.locator('#search-type').select_option('lesson');assert p.locator('.result').count()>0
 p.locator('.result button').first.click();p.locator('#search').fill('');p.locator('#search-book').select_option('all');p.locator('#search-type').select_option('saved');assert p.locator('.result').count()==1
 p.reload();p.locator('#search-type').select_option('saved');assert p.locator('.result').count()==1
 p.locator('#practice-book').select_option('kids');first=p.locator('#face').inner_text();p.locator('#reveal').click();assert p.locator('#meaning').is_visible();p.locator('[data-rate="1"]').click();assert p.locator('#face').inner_text()!=first
 p.reload();p.locator('#practice-book').select_option('kids');assert p.locator('#face').inner_text()!=first
 p.locator('#dict-reveal').click();answer=p.locator('#dict-answer').inner_text().split(' — ')[0];p.locator('#dict-input').fill(answer);p.locator('#dict-check').click();assert 'Exact text match' in p.locator('#dict-status').inner_text()
 p.locator('#theme').click();assert p.locator('html').get_attribute('data-theme')=='dark';p.screenshot(path=str(O/'dark.png'),full_page=False);p.locator('#theme').click();p.locator('#large').click();assert 'large' in p.locator('html').get_attribute('class');p.locator('#large').click()
 # Navigate real pages at intercepted origin; reader storage is unchanged.
 p.goto('https://ekguru-preview.invalid/learn/hindi/kids/phase-01/chapter-01/lesson-01/');p.locator('[data-complete]').click();p.reload();assert p.locator('[data-complete]').get_attribute('aria-pressed')=='true';p.locator('.eg-studio-nav a').first.click();assert p.locator('#total-done').inner_text()=='1 / 480';assert p.locator('[data-book="kids"] [data-resume]').is_visible()
 p.goto('https://ekguru-preview.invalid/learn/hindi/kids/phase-04/chapter-40/lesson-02/');p.locator('.eg-next-book a').click();assert p.url.endswith('/beginner/');p.locator('.eg-studio-nav a').first.click();assert p.url.endswith('/studio/')
 # Export/import only Studio state; malicious URLs rejected.
 p.locator('#import').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps({'saved':['javascript:alert(1)'],'reviews':{},'theme':'light','large':False}).encode()});p.wait_for_function("document.querySelector('#backup-status').textContent.includes('restored')");p.locator('#search-type').select_option('saved');assert p.locator('.result').count()==0
 p.locator('#search-type').select_option('all');p.screenshot(path=str(O/'desktop.png'),full_page=False);p.locator('#practice').scroll_into_view_if_needed();p.screenshot(path=str(O/'practice.png'),full_page=False)
 for w in [320,375,390,430,768,1024,1280,1440,1920]:
  p.set_viewport_size({'width':w,'height':900});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),w
 p.set_viewport_size({'width':390,'height':844});p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'mobile.png'),full_page=True);assert not errors,errors
 c=b.new_context(java_script_enabled=False);c.route('**/*',local);n=c.new_page();n.goto(U);assert n.locator('.directory a').count()==965;assert n.locator('.course a').count()>=6;c.close();b.close()
print('PASS: intercepted-origin actual page navigation, completion/flashcard/bookmark reload persistence, search, filters, dictation, theme, text scaling, import validation, 9 widths, no-JS links. Not live network or production testing.')
