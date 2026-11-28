from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from preview import embedded
O=R/'screenshots';O.mkdir(exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce');errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 def load(path=''):p.set_content(embedded(path));p.evaluate('scrollTo(0,0)')
 load();assert p.locator('.chapter-card').count()==40;p.screenshot(path=str(O/'book.png'),animations='disabled')
 lesson='phase-02/chapter-14/lesson-02';load(lesson);assert p.locator('.concept-box').count()==1;assert p.locator('.syntax-row').count()==2;p.screenshot(path=str(O/'lesson.png'),animations='disabled');p.locator('.visual-model').screenshot(path=str(O/'grammar.png'),animations='disabled');p.locator('.syntax-row [data-correct=false]').first.click();assert 'फिर' in p.locator('.syntax-row [data-feedback]').first.inner_text();p.locator('.syntax-row [data-correct=true]').first.click();assert 'सही' in p.locator('.syntax-row [data-feedback]').first.inner_text();p.locator('.syntax-row summary').first.click();assert 'में के पहले' in p.locator('.syntax-row details p').first.inner_text();p.locator('[data-model-choice=\"1\"]').click();assert 'दो किताबों' in p.locator('[data-model-parts]').inner_text();assert 'तिर्यक' in p.locator('[data-model-note]').inner_text()
 p.locator('[data-english]').click();assert p.locator('.word-card .en:visible').count()==0;p.locator('[data-english]').click();p.locator('button[data-theme]').click();p.screenshot(path=str(O/'dark.png'),animations='disabled');p.locator('button[data-theme]').click()
 c=p.locator('canvas');c.scroll_into_view_if_needed();box=c.bounding_box();p.mouse.move(box['x']+30,box['y']+30);p.mouse.down();p.mouse.move(box['x']+100,box['y']+80,steps=8);p.mouse.up();assert c.evaluate('c=>c.getContext("2d").getImageData(0,0,c.width,c.height).data.some(x=>x!==0)');p.locator('[data-undo]').click();assert not c.evaluate('c=>c.getContext("2d").getImageData(0,0,c.width,c.height).data.some(x=>x!==0)')
 p.locator('[data-complete]').click();assert p.locator('[data-complete]').get_attribute('aria-pressed')=='true';assert 'chapter-15' in p.locator('.lesson-nav .primary').get_attribute('href')
 load('phase-01/chapter-06/lesson-01');p.locator('[data-base]').select_option('म');p.locator('[data-matra="ि"]').click();assert p.locator('[data-matra-display]').inner_text()=='मि';p.locator('.chart summary').click();assert p.locator('.chart tbody td').count()==429;p.screenshot(path=str(O/'matra.png'),animations='disabled')
 load('phase-02/chapter-14/worksheet');p.locator('[data-ink]').click();assert 'ink' in p.locator('html').get_attribute('class');p.emulate_media(media='print');assert p.locator('.print-tools').is_hidden() and p.locator('.answer-key').is_hidden();p.emulate_media(media='screen');p.locator('.answer-key summary').click();p.emulate_media(media='print');assert p.locator('.answer-key').is_visible();p.emulate_media(media='screen');p.screenshot(path=str(O/'worksheet.png'),animations='disabled')
 for path in ['',lesson,'phase-01/chapter-06/lesson-01']:
  load(path)
  for w in [320,375,390,430,768,1024,1280,1440,1920]:
   p.set_viewport_size({'width':w,'height':950});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(path,w)
 p.set_viewport_size({'width':390,'height':844});load(lesson);p.screenshot(path=str(O/'mobile.png'),animations='disabled');assert not errors,errors
 p.set_viewport_size({'width':1440,'height':1000});load('phase-03/chapter-27/lesson-02');assert p.locator('.word-img').count()>=2;p.screenshot(path=str(O/'travel.png'),animations='disabled')
 a=b.new_page();a.set_content(embedded(lesson));a.evaluate("Object.defineProperty(window,'speechSynthesis',{value:{getVoices:()=>[{lang:'en-US'}],cancel(){},speak(){throw Error('wrong voice')}}})");a.locator('[data-say]').first.click();assert 'उपलब्ध नहीं' in a.locator('[data-toast]').inner_text()
 ctx=b.new_context(java_script_enabled=False);n=ctx.new_page();n.set_content(embedded(lesson));assert n.locator('.reading p').count()>=3;n.locator('.syntax-row details summary').first.click();assert n.locator('.syntax-row details p').first.is_visible();ctx.close();b.close()
print('PASS: 27 viewport/page checks; grammar lab, answer explanations, theme, English toggle, drawing and undo, completion, chart, print CSS, missing Hindi voice fallback, no-JS reading. Embedded DOM only; hosted navigation and persistent storage not tested.')
