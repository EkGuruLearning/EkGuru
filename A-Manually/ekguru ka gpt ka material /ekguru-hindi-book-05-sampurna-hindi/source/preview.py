from pathlib import Path
from html import escape
import re,base64
R=Path(__file__).resolve().parents[1];S=R/'site';B=S/'learn/hindi/mastery'
def embedded(path):
 f=B/path/'index.html';h=f.read_text()
 h=re.sub(r'<link rel="stylesheet" href="[^"]+">','<style>'+ (S/'css/hindi-mastery-reader.css').read_text()+'</style>',h)
 h=re.sub(r'<script src="[^"]+" defer></script>',lambda m:'<script defer>document.addEventListener("DOMContentLoaded",()=>{'+(S/'js/hindi-mastery-reader.js').read_text()+'});</script>',h)
 def img(m):
  file=(f.parent/m[1]).resolve();return 'src="data:image/svg+xml;base64,'+base64.b64encode(file.read_bytes()).decode()+'"'
 h=re.sub(r'src="([^"\s]+\.svg)"',img,h)
 return h
if __name__=='__main__':
 h=embedded('phase-03/chapter-23/lesson-02')
 # Standalone reader demo has no uninstalled route links. The full ZIP has all 165 navigable pages.
 h=re.sub(r'<a\b[^>]*href="(?!https://|#)[^"]+"[^>]*>(.*?)</a>',r'<span>\1</span>',h,flags=re.S)
 h=h.replace('<div class="reader-layout">','<p class="note" lang="en">Standalone sample: Chapter 23, Lesson 2. Full course navigation is in the ZIP (serve the site folder).</p><div class="reader-layout">',1)
 (R/'preview-lesson.html').write_text(h)
