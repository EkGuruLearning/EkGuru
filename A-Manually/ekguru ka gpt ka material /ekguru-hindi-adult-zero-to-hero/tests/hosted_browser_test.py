"""Real Chromium navigation against intercepted local static files; no public network."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlsplit,unquote
import mimetypes
R=Path(__file__).resolve().parents[1];S=R/'site'; B='/learn/hindi/older-adults/'; OUT=R/'screenshots';OUT.mkdir(exist_ok=True);origin='https://ekguru-preview.test'
def route(r):
 u=urlsplit(r.request.url)
 if u.netloc!='ekguru-preview.test':return r.abort()
 f=(S/unquote(u.path).lstrip('/')).resolve()
 if f.is_dir():f/= 'index.html'
 if f.is_relative_to(S.resolve()) and f.is_file():return r.fulfill(status=200,body=f.read_bytes(),content_type=mimetypes.guess_type(f)[0] or 'application/octet-stream')
 return r.fulfill(status=404,body='Not found')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);ctx=browser.new_context(viewport={'width':1366,'height':900});ctx.route('**/*',route);p=ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 def go(path):
  resp=p.goto(origin+B+path);assert resp.status==200;p.wait_for_load_state('load')
 go('');p.screenshot(path=str(OUT/'home.png'),animations='disabled');assert p.locator('[data-chapter-grid] a').count()==40
 p.locator('[data-filter]').fill('यात्रा');assert p.locator('[data-chapter-grid] a:visible').count()>0 and p.locator('[data-chapter-grid] a:visible').count()<40
 p.locator('[data-filter]').fill('NOT-A-CHAPTER');assert p.locator('[data-chapter-grid] a:visible').count()==0
 p.locator('[data-filter]').fill('');assert p.locator('[data-chapter-grid] a:visible').count()==40
 p.locator('a.gold').click();assert '/foundation/chapter-01/lesson-01/' in p.url
 p.locator('[data-complete]').click();p.reload();assert p.locator('[data-complete]').get_attribute('aria-pressed')=='true'
 p.locator('[data-large]').click();assert p.locator('html').evaluate('(x)=>x.classList.contains("large-text")');p.reload();assert p.locator('[data-large]').get_attribute('aria-pressed')=='true';p.locator('[data-large]').click()
 p.locator('[data-english]').click();assert not p.locator('.adult-phrase .en').first.is_visible();p.locator('[data-english]').click()
 p.locator('button[data-theme]').click();assert p.locator('html').get_attribute('data-theme')=='dark';p.screenshot(path=str(OUT/'dark.png'),animations='disabled');p.locator('button[data-theme]').click()
 p.locator('[data-quiz] [data-correct=false]').first.click();assert p.locator('[data-feedback]').first.inner_text();p.locator('[data-quiz] [data-correct=true]').first.click();assert p.locator('[data-quiz] [data-correct=true]').first.get_attribute('data-state')=='correct'
 canvas=p.locator('[data-draw]');canvas.scroll_into_view_if_needed();b=canvas.bounding_box();p.mouse.move(b['x']+20,b['y']+20);p.mouse.down();p.mouse.move(b['x']+100,b['y']+80,steps=5);p.mouse.up();assert canvas.evaluate('(c)=>c.getContext("2d").getImageData(0,0,c.width,c.height).data.some(x=>x!==0)');p.locator('[data-undo]').click();assert not canvas.evaluate('(c)=>c.getContext("2d").getImageData(0,0,c.width,c.height).data.some(x=>x!==0)')
 p.locator('.lesson-nav .primary').click();assert '/lesson-02/' in p.url;p.locator('[data-draft]').fill('मैं हिंदी सीख रहा हूँ।');p.locator('[data-save-draft]').click();p.reload();assert p.locator('[data-draft]').input_value()=='मैं हिंदी सीख रहा हूँ।'
 go('');assert p.locator('[data-progress-count]').inner_text()=='1 / 80';p.locator('[data-resume]').click();assert '/foundation/chapter-01/lesson-02/' in p.url
 go('foundation/chapter-04/lesson-01/');p.locator('[data-base]').select_option('म');p.locator('[data-matra="ि"]').click();assert p.locator('[data-matra-display]').inner_text()=='मि'
 go('foundation/chapter-08/lesson-02/');p.locator('.lesson-nav .primary').click();assert p.url.endswith('/foundation/assessment/');p.locator('.lesson-nav .primary').click();assert p.url.endswith('/beginner/')
 go('beginner/chapter-10/lesson-02/');p.screenshot(path=str(OUT/'lesson.png'),animations='disabled');p.locator('.dialogue').screenshot(path=str(OUT/'dialogue.png'),animations='disabled')
 go('beginner/chapter-10/worksheet/');p.locator('[data-ink]').click();assert p.locator('html').evaluate('(x)=>x.classList.contains("ink")');p.emulate_media(media='print');assert not p.locator('.top').is_visible();p.pdf(path=str(OUT/'worksheet-test.pdf'),format='A4');p.emulate_media(media='screen');p.screenshot(path=str(OUT/'worksheet.png'),animations='disabled')
 n=0
 for w in [320,375,390,430,768,1024,1280,1440,1920]:
  p.set_viewport_size({'width':w,'height':850})
  for path in ['', 'beginner/chapter-10/lesson-02/', 'mastery/assessment/']:
   go(path);assert p.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(w,path);n+=1
   if w==390 and path=='beginner/chapter-10/lesson-02/':p.screenshot(path=str(OUT/'mobile.png'),animations='disabled')
 assert not errors,errors
 ctx.close();ctx=browser.new_context(java_script_enabled=False);ctx.route('**/*',route);p=ctx.new_page();go('');assert p.locator('[data-chapter-grid] a:visible').count()==40;p.locator('a.gold').click();assert p.locator('.adult-phrase').count()==4;assert p.locator('.lesson-nav .primary').is_visible();browser.close();print(f'{n} responsive checks + local route navigation, search, local persistence, larger text, dark mode, quizzes, canvas undo, matra, A4 PDF generation and no-JS reading passed.')
