"""Render the Hindi landing page from the legacy generator + explicit textbook registry."""
import json,re
from html import escape,unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
START='<!-- ekguru:hindi-hub:start -->'; END='<!-- ekguru:hindi-hub:end -->'
GROUPS={'hh-start':('शुरुआत','Getting started'),'hh-levels':('स्तर','Existing levels'),'hh-topics':('विषय','Topics'),'hh-guides':('पाठ','Detailed lessons'),'hh-daily':('दैनिक हिंदी','Daily Hindi'),'hh-practice':('अभ्यास','Practice & review'),'hh-tools':('लेखन और कार्यपत्रक','Tools & worksheets'),'hh-questions':('प्रश्न','Questions & guides'),'hh-tutors':('शिक्षक','Optional tutors'),'hh-other':('अन्य भाषाएँ','Other languages'),'ht-chapters':('अध्याय','Individual chapters')}
class Links(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True);self.items=[];self.current=None;self.bold=False
 def handle_starttag(self,tag,attrs):
  if tag=='a': self.current=[dict(attrs).get('href',''),[],[]]
  if tag=='b' and self.current: self.bold=True
 def handle_endtag(self,tag):
  if tag=='b': self.bold=False
  if tag=='a' and self.current:
   url,words,bold=self.current; self.current=None;self.bold=False
   label=' '.join(''.join(bold or words).split()) or url
   if url and not url.lower().startswith(('javascript:','data:')):self.items.append((url,label))
 def handle_data(self,data):
  if self.current:
   self.current[1].append(data)
   if self.bold:self.current[2].append(data)
def inventory(region):
 parts=re.split(r'<h2\b[^>]*\bid=["\']([^"\']+)["\'][^>]*>',region,flags=re.I)
 result={};p=Links();p.feed(parts[0]);result['hh-start']=p.items
 for i in range(1,len(parts),2):
  p=Links();p.feed(parts[i+1]);result.setdefault(parts[i],[]).extend(p.items)
 return {k:list(dict.fromkeys(v)) for k,v in result.items()}
def render_hindi_hub(legacy,href,root=Path('.')):
 root=Path(root); data=json.loads((root/'data/learning/hindi-textbook-catalogue.json').read_text()); groups=inventory(legacy)
 # Discover actual lesson pages, not guessed routes. The registry controls future books.
 for course in ['foundation']+[r['route'].removeprefix('learn/hindi/') for r in data['academic']+data['adult'] if r['status'] in ('existing','published')]:
  base=root/'learn/hindi'/course
  for path in sorted(base.rglob('index.html')):
   if path.parent==base:continue
   title=re.search(r'<title>(.*?)</title>',path.read_text(encoding='utf-8'),re.S)
   if title:
    name=unescape(title[1]).split(' | EkGuru')[0].strip()
    groups.setdefault('ht-chapters',[]).append((href(path.parent.relative_to(root).as_posix()),name))
 if 'ht-chapters' in groups:groups['ht-chapters']=list(dict.fromkeys(groups['ht-chapters']))
 e=lambda s:escape(str(s),quote=True)
 def exists(t):return (root/(t if t.endswith('.html') else t+'/index.html')).is_file()
 def link(t,label,cls=''):
  return f'<a class="{cls}" href="{e(href(t))}">{e(label)} <span aria-hidden="true">↗</span></a>' if exists(t) else ''
 def book(r,i,adult=False):
  status=r['status']; ready=status in ('existing','published') and exists(r['route']); state=('Available lessons' if status=='existing' else 'Open textbook') if ready else 'In development'
  tag='a' if ready else 'div'; dest=f' href="{e(href(r["route"]))}"' if ready else ''
  return f'<{tag} class="ht-book ht-tone-{i%5}"{dest}><div class="ht-cover"><span class="ht-volume">0{i+1}</span><span lang="hi" class="ht-glyph">{e(r.get("glyph",r["hi"][0]))}</span><span class="ht-spine"></span><span class="ht-cover-line"></span></div><div class="ht-book-text"><span class="ht-level">{e(r.get("level","Level "+str(i+1)))}</span><h3 lang="hi">{e(r["hi"])}</h3><b>{e(r["en"])}</b><p>{e(r.get("description",""))}</p><span class="ht-state">{state}{" ↗" if ready else ""}</span></div></{tag}>'
 out=[START,'<link rel="stylesheet" href="/css/hindi-textbook-hub.css">','<div class="ht" data-hindi-hub>']
 out+=['<section class="ht-hero" aria-label="Hindi learning"><div class="ht-hero-copy"><span class="ht-eyebrow"><span></span> HINDI · हिंदी</span><div class="ht-hero-title" lang="hi">अक्षर से<br><em>अभिव्यक्ति तक।</em></div><p>Read, write, listen and speak Hindi.</p><div class="ht-actions">',link('learn/hindi/foundation','Start from zero','ht-primary'),link('learn/practice/placement','Find my level','ht-secondary'),'</div></div><div class="ht-art" aria-hidden="true"><div class="ht-orbit"></div><div class="ht-orbit ht-orbit-two"></div><span class="ht-float ht-f1">अ</span><span class="ht-float ht-f2">क</span><span class="ht-float ht-f3">आ</span><span class="ht-spark">✧</span><svg viewBox="0 0 400 260" class="ht-openbook"><path d="M28 63Q112 25 200 82Q288 25 372 63L384 221Q284 193 200 244Q116 193 16 221Z" fill="#a46b36"/><path d="M35 49Q119 18 200 78V230Q115 186 24 208Z" fill="#ffefce"/><path d="M365 49Q281 18 200 78V230Q285 186 376 208Z" fill="#ebd8ae"/><path d="M200 79V230" stroke="#ad8652" stroke-width="3"/><g fill="none" stroke="#b39b6c" stroke-width="2"><path d="M52 116Q123 93 176 126M49 137Q122 114 177 147M47 158Q119 136 177 168M224 126Q278 93 348 116M223 147Q278 114 351 137M223 168Q281 136 353 158"/></g><g font-size="39" fill="#35574a" text-anchor="middle"><text x="113" y="92">अ आ</text><text x="288" y="92">क ख</text></g><path d="M339 49v57l10-8 10 8V46" fill="#ca754a"/></svg><span class="ht-art-caption" lang="hi">पढ़ें · लिखें · बोलें</span></div></section>']
 out+=['<nav class="ht-jump" aria-label="Hindi sections"><a href="#hh-levels">Textbooks</a><a href="#ht-adults">Adults</a><a href="#hh-practice">Practice</a><a href="#ht-library">All lessons</a>',link('learn/hindi/my-progress','My progress'),'</nav>']
 out+=['<section id="hh-levels" class="ht-section"><div class="ht-heading"><div><span class="ht-kicker">01 / TEXTBOOKS</span><h2 lang="hi">हिंदी की पाठ्यपुस्तकें</h2><p>Progressive Hindi · preschool to advanced study</p></div><span class="ht-count">'+str(len(data['academic']))+' stages</span></div><div class="ht-books">',*[book(r,i) for i,r in enumerate(data['academic'])],'</div><p class="ht-note">Class ranges describe the planned learning depth, not accredited qualifications. Available lessons are not a claim that an entire textbook is complete.</p><div class="ht-inline">'+link('learn/hindi/foundation','Devanagari foundation')+link('learn/hindi/elementary','Elementary lessons')+link('languages/hi/level','Existing A1–C2 levels')+'</div></section>']
 out+=['<section id="ht-adults" class="ht-section ht-adult"><div class="ht-heading"><div><span class="ht-kicker">02 / ADULT LEARNING</span><h2 lang="hi">वयस्कों के लिए हिंदी</h2><p>Independent, age-appropriate progression from zero to mastery.</p></div></div><div class="ht-adult-steps">']
 for i,r in enumerate(data['adult']):
  ready=r['status'] in ('existing','published') and exists(r['route']); tag='a' if ready else 'div'; dest=f' href="{e(href(r["route"]))}"' if ready else ''
  out.append(f'<{tag} class="ht-adult-step"{dest}><span>{i+1:02}</span><b lang="hi">{e(r["hi"])}</b><small>{e(r["en"])}</small><small>{"Available" if ready else "Planned"}</small></{tag}>')
 out+=['</div><p class="ht-note">Use the existing practical lessons while the dedicated adult textbooks are developed.</p><div class="ht-inline">'+link('learn/paths/hindi-from-zero','Hindi from zero')+link('learn/paths/everyday-hindi','Everyday Hindi')+link('learn/hindi-phrases-for-travel','Travel Hindi')+'</div></section>']
 out+=['<section class="ht-section"><div class="ht-heading"><div><span class="ht-kicker">03 / PRACTICE</span><h2 lang="hi">अभ्यास करें</h2><p>Choose a skill.</p></div></div><div class="ht-skills">']
 for glyph,hi,en,t in [('अ','लेखन','Writing','learn/practice/writing'),('◖','श्रवण','Listening','learn/practice/listening'),('क','उच्चारण','Pronunciation','learn/practice/pronunciation'),('श','शब्दावली','Vocabulary','learn/practice/vocabulary'),('व','व्याकरण','Grammar','learn/practice/grammar'),('▤','कार्यपत्रक','Worksheets','learn/hindi/practice/worksheets')]:
  if exists(t):out.append(f'<a href="{e(href(t))}" class="ht-skill"><span aria-hidden="true">{glyph}</span><b lang="hi">{hi}</b><small>{en}</small></a>')
 out+=['</div></section>','<section id="ht-library" class="ht-section"><div class="ht-heading"><div><span class="ht-kicker">04 / LIBRARY</span><h2 lang="hi">सभी पाठ और संसाधन</h2><p>Search the existing Hindi learning library.</p></div></div><div class="ht-search" hidden><label for="ht-query">Search lessons</label><input id="ht-query" type="search" placeholder="स्वर, vowels, grammar…" autocomplete="off"><button type="button" data-ht-clear>Clear</button><output aria-live="polite" data-ht-result></output></div><div class="ht-library">']
 for k,items in groups.items():
  if not re.fullmatch(r'[a-zA-Z0-9_-]+',k):continue
  hi,en=GROUPS.get(k,(k,k)); anchor='ht-existing-levels' if k=='hh-levels' else k
  # Preserve existing fragments; hh-levels already points to textbook section.
  rows=[(u,l) for u,l in items if not u.startswith('#')]
  out.append(f'<details id="{e(anchor)}" class="ht-group"><summary><span><b lang="hi">{e(hi)}</b><small>{e(en)}</small></span><span>{len(rows)} <i aria-hidden="true">+</i></span></summary><ul>')
  for u,l in rows:
   aliases=' '.join(v for k,v in [('swar','स्वर vowels'),('vowel','स्वर'),('vyanjan','व्यंजन consonants'),('consonant','व्यंजन'),('matra','मात्रा'),('barakhadi','बारहखड़ी'),('grammar','व्याकरण'),('writing','लेखन'),('number','गिनती'),('story','कहानी'),('kahani','कहानी')] if k in (u+' '+l).lower())
   out.append(f'<li data-ht-entry data-ht-alias="{e(aliases)}"><a href="{e(u)}">{e(l)}</a></li>')
  out.append('</ul></details>')
 out+=['</div><p class="ht-note">Free self-paced materials. Review status varies; see the editorial information on each lesson.</p></section></div><script src="/js/hindi-textbook-hub.js" defer></script>',END]
 return '\n'.join(out)
