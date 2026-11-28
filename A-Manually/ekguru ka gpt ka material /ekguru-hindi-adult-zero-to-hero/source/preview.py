from pathlib import Path
import re,base64
R=Path(__file__).resolve().parents[1]; S=R/'site'; B=S/'learn/hindi/older-adults'
def embedded(path, disable_links=False):
 f=B/path/'index.html';h=f.read_text();h=re.sub(r'<link rel="stylesheet" href="[^"]+">','<style>'+ (S/'css/hindi-adult-reader.css').read_text()+'</style>',h);h=re.sub(r'<script src="[^"]+" defer></script>',lambda m:'<script>document.addEventListener("DOMContentLoaded",()=>{'+(S/'js/hindi-adult-reader.js').read_text()+'});</script>',h)
 def img(m):return 'src="data:image/svg+xml;base64,'+base64.b64encode((f.parent/m[1]).resolve().read_bytes()).decode()+'"'
 h=re.sub(r'src="([^"\s]+\.svg)"',img,h)
 if disable_links:
  h=re.sub(r'<a\b[^>]*href="(?!https://|#)[^"]+"[^>]*>(.*?)</a>',r'<span>\1</span>',h,flags=re.S);h=h.replace('<div class="reader-layout">','<p class="adult-note">Standalone lesson demo. Full navigation works when the ZIP is served from its site folder.</p><div class="reader-layout">',1)
 return h
if __name__=='__main__':(R/'preview-lesson.html').write_text(embedded('beginner/chapter-10/lesson-02',True))
