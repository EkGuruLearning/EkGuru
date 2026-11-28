from pathlib import Path
import json,html,re
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
BASE='https://ekguru.shop'

def records():
    rows=json.loads((ROOT/'source/languages.json').read_text())
    ids=set();paths=set()
    for r in rows:
        assert len(r)==7 and r[0] not in ids and r[4] not in paths and r[3] in ('Indian','World')
        assert re.fullmatch(r'/[a-z0-9/-]+/',r[4]) and all(re.fullmatch(r'#[A-Fa-f0-9]{6}',v) for v in r[5:])
        ids.add(r[0]);paths.add(r[4])
    return rows

def link(path,preview=False):return E(BASE+path if preview and path.startswith('/') else path)
def main_region(rows,preview=False):
    L=lambda p:link(p,preview)
    groups=[]
    for kind,title in [('Indian','Languages of India'),('World','Around the world')]:
        cards=[]
        symbols={'hi':'अ','bn':'অ','mr':'म','ta':'அ','te':'అ','gu':'અ','pa':'ੳ','ur':'ا','es':'Ñ','fr':'É','de':'Ä','ar':'ع','ja':'あ','ko':'한','zh':'中','pt':'Ã','it':'It','ru':'Я'}
        for code,name,native,group,path,tone,text in rows:
            if group!=kind:continue
            cards.append(f'<a class="lang" data-group="{group}" data-search="{E(name+" "+native+" "+code)}" href="{L(path)}"><span class="glyph" lang="{E(code)}" dir="auto" style="--tone:{tone};--text:{text}">{E(symbols.get(code,code.upper()[:3]))}</span><span><strong>{E(name)}</strong><small lang="{E(code)}" dir="auto">{E(native)}</small></span><span aria-hidden="true" class="arrow">↗</span></a>')
        groups.append(f'<section data-language-group="{kind}"><h3 class="group-title">{title}<span class="group-count">{len(cards)} languages</span></h3><div class="lang-grid">{"".join(cards)}</div><button type="button" class="btn show-more js-only" hidden>Show more {kind.lower()} languages ↓</button></section>')
    books=''.join(f'<div class="book" style="--tone:{t};--text:{f}"><span>BOOK 0{i+1}</span><b lang="hi">{g}</b><span lang="hi">{n}</span></div>' for i,(g,n,t,f) in enumerate([('अ','बाल हिंदी','#F8D98E','#604116'),('क','प्रारंभिक','#D9E9D5','#315C41'),('श','मध्यम','#D9E9FA','#2D537E'),('ज्ञ','उन्नत','#E6DDFB','#514183'),('हिं','संपूर्ण','#FAD8C9','#783D2F')]))
    tools=''.join(f'<a class="tool" href="{L(p)}"><span class="tool-icon" style="--tone:{t};--text:{f}">{ic}</span><strong>{name}</strong><small>{desc}</small></a>' for ic,name,desc,p,t,f in [('अ','Alphabet & writing','Read and practise Devanagari','/toolbox/hindi-alphabet/','#F8D98E','#604116'),('♫','Listening & speaking','Build your confidence aloud','/learn/practice/listening/','#E6DDFB','#514183'),('▤','Printable worksheets','Learn away from the screen','/materials/','#FAD8C9','#783D2F'),('↗','My learning','Review your local progress','/learn/progress/','#D9E9D5','#315C41')])
    return f'''<div class="wrap eg-global-home"><section class="hero"><div><div class="eyebrow">Languages bring us closer</div><h1>Learn a language.<br> <em>Open your world.</em></h1><p>Discover India’s languages and the world beyond. Study free lessons at your own pace, or find an independent Hindi tutor for personal guidance.</p><div class="actions"><a class="btn primary" href="#discover">Explore languages <span aria-hidden="true">↗</span></a><a class="btn" href="{L('/find-tutors.html')}">Find a Hindi tutor</a></div><div class="hero-bottom"><span>✓ Free self-paced materials</span><span>✓ No account required to study</span></div></div><div class="hero-art"><img src="/images/home-global/conversation.svg" width="630" height="490" alt="Illustration of two learners conversing over an open book" fetchpriority="high"><div class="float"><span lang="hi">नमस्ते</span> · Hello <small>Start with a word. Go further.</small></div></div></section>
<section class="section" id="discover"><div class="section-head"><div><h2>What would you like to learn?</h2><p class="sub">Start close to home, or explore a new culture.</p></div><a class="text-link" href="{L('/learn/')}">Browse all courses ↗</a></div><div class="discovery js-only"><label class="search"><span aria-hidden="true">⌕</span><input id="language-search" type="search" placeholder="Search Hindi, Español, 日本語..." aria-label="Search languages"></label><div class="filters" role="group" aria-label="Filter languages"><button class="filter" data-filter="All" aria-pressed="true">All languages</button><button class="filter" data-filter="Indian" aria-pressed="false">Indian</button><button class="filter" data-filter="World" aria-pressed="false">World</button></div></div><div id="search-status" class="status js-only" aria-live="polite"></div>{''.join(groups)}<p id="empty" hidden>No matching language. Try a different name or script.</p><p class="sub" style="margin-top:16px">Course depth varies by language. <a class="text-link" href="{L('/learn/')}">See available lessons.</a></p></section>
<section class="section"><div class="section-head"><div><h2>Two ways to make progress.</h2><p class="sub">A learning path for your goals, not a one-size-fits-all programme.</p></div></div><div class="feature-grid"><article class="panel hindi"><div class="eyebrow">Learn independently</div><h3>Hindi, from the first letter<br>to confident expression.</h3><p>Read, listen, write and practise. Explore Hindi lessons, grammar, stories and worksheets.</p><div class="books" aria-label="Illustrated five-book curriculum design concept">{books}</div><p class="sub">Five-book curriculum design preview — integration pending.</p><a class="btn gold" href="{L('/learn/hindi/')}">Explore Hindi ↗</a></article><article class="panel tutor"><div class="eyebrow">Learn with a person</div><h3>Real conversations.<br>Personal guidance.</h3><p>Browse independent Hindi tutor profiles, choose someone who fits your goals, and send a booking request.</p><div class="tutor-art" aria-hidden="true"><span class="talk">Hi!</span><span class="talk">न</span><span class="talk">?</span></div><a class="btn" href="{L('/find-tutors.html')}">Browse Hindi tutors ↗</a></article></div></section>
<section class="section"><div class="section-head"><div><h2>Make learning a habit.</h2><p class="sub">Free tools to practise between lessons.</p></div><a class="text-link" href="{L('/toolbox/')}">All tools ↗</a></div><div class="tools">{tools}</div></section>
<section class="final"><div><h2>Your next word starts here.</h2><p>Choose a language and start learning at your own pace.</p></div><a class="btn primary" href="#discover">Choose a language ↗</a></section></div>'''

def render(preview=True):
    rows=records();L=lambda p:link(p,preview)
    css=(ROOT/'css/home-global.css').read_text();js=(ROOT/'js/home-global.js').read_text();art=(ROOT/'images/conversation.svg').read_bytes()
    import base64
    region=main_region(rows,preview)
    if preview:region=region.replace('/images/home-global/conversation.svg','data:image/svg+xml;base64,'+base64.b64encode(art).decode())
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Learn languages at your own pace | EkGuru</title><meta name="description" content="Explore free Hindi, Indian and world language learning materials. Discover independent Hindi tutors, lessons and practice tools."><meta name="robots" content="noindex,follow"><style>{css}</style></head><body><a class="skip" href="#main">Skip to content</a><header class="site-head"><div class="wrap nav"><a href="{L('/')}" class="brand"><span class="logo" lang="hi">ए</span>EkGuru</a><nav class="nav-links" aria-label="Main navigation"><a href="{L('/learn/')}">Learn</a><a href="{L('/find-tutors.html')}">Find tutors</a><a href="{L('/toolbox/')}">Practice</a><a href="{L('/about/')}">About</a></nav><div class="right"><button id="theme" type="button" class="theme js-only" aria-label="Switch to dark mode">☾</button><a class="btn primary" href="{L('/learn/')}">Start learning</a></div></div></header><main id="main">{region}</main><footer class="foot"><div class="wrap"><div class="foot-row"><span>EkGuru · One student. One goal. One guru.</span><nav aria-label="Footer"><a href="{L('/about/')}">About</a><a href="{L('/contact/')}">Contact</a><a href="{L('/editorial-policy/')}">Editorial policy</a><a href="{L('/privacy/')}">Privacy</a><a href="{L('/terms/')}">Terms</a></nav></div><p class="preview-note">Design preview only. Course links open existing EkGuru pages; independent tutor arrangements remain separate.</p></div></footer><script>{js}</script></body></html>'''
if __name__=='__main__':
    (ROOT/'preview.html').write_text(render(),encoding='utf8')
    (ROOT/'source/home-region.html').write_text(main_region(records()),encoding='utf8')
