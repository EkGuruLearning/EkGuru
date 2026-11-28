from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from preview import embedded
OUT=R/'screenshots';OUT.mkdir(exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);p=b.new_page(viewport={'width':1366,'height':900});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 def go(path):p.set_content(embedded(path),wait_until='load');p.evaluate('document.fonts.ready')
 go('');p.screenshot(path=str(OUT/'home.png'),animations='disabled');assert p.locator('[data-chapter-grid] a').count()==40;p.locator('[data-filter]').fill('यात्रा');assert 0<p.locator('[data-chapter-grid] a:visible').count()<40;p.locator('[data-filter]').fill('NOT-A-CHAPTER');assert p.locator('[data-chapter-grid] a:visible').count()==0
 go('foundation/chapter-01/lesson-01');p.locator('[data-large]').click();assert p.locator('html').evaluate('(x)=>x.classList.contains("large-text")');p.locator('[data-large]').click();p.locator('[data-english]').click();assert not p.locator('.adult-phrase .en').first.is_visible();p.locator('[data-english]').click();p.locator('button[data-theme]').click();assert p.locator('html').get_attribute('data-theme')=='dark';p.screenshot(path=str(OUT/'dark.png'),animations='disabled');p.locator('button[data-theme]').click();p.locator('[data-quiz] [data-correct=false]').first.click();assert p.locator('[data-feedback]').first.inner_text();p.locator('[data-quiz] [data-correct=true]').first.click();assert p.locator('[data-quiz] [data-correct=true]').first.get_attribute('data-state')=='correct'
 canvas=p.locator('[data-draw]');canvas.scroll_into_view_if_needed();r=canvas.bounding_box();p.mouse.move(r['x']+20,r['y']+20);p.mouse.down();p.mouse.move(r['x']+100,r['y']+80,steps=5);p.mouse.up();assert canvas.evaluate('(c)=>c.getContext("2d").getImageData(0,0,c.width,c.height).data.some(x=>x!==0)');p.locator('[data-undo]').click();assert not canvas.evaluate('(c)=>c.getContext("2d").getImageData(0,0,c.width,c.height).data.some(x=>x!==0)')
 go('foundation/chapter-04/lesson-01');p.locator('[data-base]').select_option('म');p.locator('[data-matra="ि"]').click();assert p.locator('[data-matra-display]').inner_text()=='मि'
 go('beginner/chapter-10/lesson-02');p.screenshot(path=str(OUT/'lesson.png'),animations='disabled');p.locator('.dialogue').screenshot(path=str(OUT/'dialogue.png'),animations='disabled');p.locator('[data-draft]').fill('मैं हिंदी सीख रहा हूँ।');assert p.locator('[data-word-count]').inner_text()=='5 शब्द';p.locator('[data-save-draft]').click();assert p.locator('[data-draft-status]').inner_text()
 go('beginner/chapter-10/worksheet');p.locator('[data-ink]').click();assert p.locator('html').evaluate('(x)=>x.classList.contains("ink")');p.emulate_media(media='print');assert not p.locator('.top').is_visible();p.emulate_media(media='screen');p.screenshot(path=str(OUT/'worksheet.png'),animations='disabled')
 n=0
 for w in [320,375,390,430,768,1024,1280,1440,1920]:
  p.set_viewport_size({'width':w,'height':850})
  for path in ['', 'beginner/chapter-10/lesson-02', 'mastery/assessment']:
   go(path);assert p.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(w,path);n+=1
   if w==390 and path=='beginner/chapter-10/lesson-02':p.screenshot(path=str(OUT/'mobile.png'),animations='disabled')
 assert not errors,errors
 p=b.new_page(java_script_enabled=False);p.set_content(embedded(''));assert p.locator('[data-chapter-grid] a:visible').count()==40;p.set_content(embedded('foundation/chapter-01/lesson-01'));assert p.locator('.adult-phrase').count()==4;assert p.locator('.lesson-nav .primary').is_visible();b.close();print(f'{n} responsive checks, embedded browser search, large text, theme, translation toggle, quizzes, canvas, matra, draft feedback, print CSS and no-JS reading PASS. Hosted navigation and persistence not tested.')
