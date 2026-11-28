from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from preview import embedded
OUT=R/'screenshots';OUT.mkdir(exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce');errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 def load(path=''):p.set_content(embedded(path));p.evaluate('scrollTo(0,0)')
 load();assert p.locator('.chapter-card').count()==40;p.screenshot(path=str(OUT/'book.png'),animations='disabled');assert p.locator('.hero .gold').get_attribute('href')=='phase-01/chapter-01/lesson-01/'
 load('phase-01/chapter-02/lesson-01');assert p.locator('.word-card').count()==6;assert p.locator('.word-img').count()>=2;p.screenshot(path=str(OUT/'lesson.png'),animations='disabled');p.locator('[data-english]').click();assert p.locator('.word-card .en:visible').count()==0;p.locator('[data-english]').click();p.locator('button[data-theme]').click();p.screenshot(path=str(OUT/'dark.png'),animations='disabled');p.locator('button[data-theme]').click()
 p.locator('[data-correct=false]').first.click();assert 'फिर' in p.locator('[data-feedback]').inner_text();p.locator('[data-correct=true]').click();assert 'सही' in p.locator('[data-feedback]').inner_text()
 c=p.locator('canvas');c.scroll_into_view_if_needed();box=c.bounding_box();p.mouse.move(box['x']+30,box['y']+30);p.mouse.down();p.mouse.move(box['x']+100,box['y']+80,steps=8);p.mouse.up();assert c.evaluate('c=>c.getContext("2d").getImageData(0,0,c.width,c.height).data.some(x=>x!==0)');p.locator('[data-undo]').click();assert not c.evaluate('c=>c.getContext("2d").getImageData(0,0,c.width,c.height).data.some(x=>x!==0)')
 p.locator('[data-complete]').click();assert p.locator('[data-complete]').get_attribute('aria-pressed')=='true';assert p.locator('.lesson-nav .primary').get_attribute('href')=='../lesson-02/'
 load('phase-02/chapter-19/lesson-01');p.locator('[data-base]').select_option('म');p.locator('[data-matra="ि"]').click();assert p.locator('[data-matra-display]').inner_text()=='मि';p.locator('.chart summary').click();assert p.locator('.chart tbody tr').count()==33;assert p.locator('.chart tbody td').count()==429;p.screenshot(path=str(OUT/'matra.png'),animations='disabled')
 load('phase-03/chapter-29/lesson-01');p.locator('[data-count]').fill('12');assert p.locator('[data-dots] i').count()==12
 load('phase-01/chapter-02/worksheet');p.locator('[data-ink]').click();assert 'ink' in p.locator('html').get_attribute('class');p.emulate_media(media='print');assert p.locator('.print-tools').is_hidden() and p.locator('.answer-key').is_hidden();p.emulate_media(media='screen');p.locator('.answer-key summary').click();p.emulate_media(media='print');assert p.locator('.answer-key').is_visible();p.emulate_media(media='screen');p.screenshot(path=str(OUT/'worksheet.png'),animations='disabled')
 for path in ['', 'phase-01/chapter-02/lesson-01','phase-02/chapter-19/lesson-01']:
  load(path)
  for w in [320,375,390,430,768,1024,1280,1440,1920]:
   p.set_viewport_size({'width':w,'height':950});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(path,w)
 p.set_viewport_size({'width':390,'height':844});load('phase-01/chapter-02/lesson-01');p.screenshot(path=str(OUT/'mobile.png'),animations='disabled');assert not errors,errors
 a=b.new_page();a.set_content(embedded('phase-01/chapter-02/lesson-01'));a.evaluate("Object.defineProperty(window,'speechSynthesis',{value:{getVoices:()=>[{lang:'en-US'}],cancel(){},speak(){throw Error('wrong voice')}}})");a.locator('[data-say]').first.click();assert 'उपलब्ध नहीं' in a.locator('[data-toast]').inner_text()
 ctx=b.new_context(java_script_enabled=False);n=ctx.new_page();n.set_content(embedded('phase-01/chapter-02/lesson-01'));assert n.locator('.reading p').count()>=2;n.locator('.check details summary').first.click();assert n.locator('.check details p').first.is_visible();ctx.close();b.close()
print('PASS: embedded Chromium rendering, 27 viewport/page checks, quiz, drawing/undo, self-mark, matra, 429-form chart, counting, theme, English toggle, print CSS, no-Hindi-voice fallback, JS-free reading. HTTP navigation and persistent storage require an integrated origin test.')
