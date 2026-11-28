#!/usr/bin/env python3
"""Build the independent Prarambhik Hindi textbook. All page content is static and noindex until owner approval."""
from pathlib import Path
import json,re,html,posixpath,unicodedata,sys
R=Path(__file__).resolve().parents[1]; S=R/'site'; BASE='learn/hindi/beginner'; A='images/hindi-kids'; ART={w:A+'/'+v for w,v in json.loads((R/'source/art.json').read_text()).items()}; ART.update(json.loads((R/'source/new-art.json').read_text())); E=lambda s:html.escape(str(s),quote=True)
for alias,source in {'विद्यालय':'स्कूल','पुस्तक':'किताब','क़लम':'कलम','दरवाज़ा':'दरवाजा','सूर्य':'सूरज','वृक्ष':'पेड़','बगीचे':'बगीचा','मेज़':'मेज','समय':'घड़ी','जल':'पानी','वन':'वन','कक्ष':'कमरा','पौधे':'पौधा'}.items():
 if source in ART: ART[alias]=ART[source]
PHASES=[('लिपि और पठन','Script & reading','स्वर, मात्राएँ, वर्तनी और शब्दों से स्वतंत्र पठन।','किताब'),('व्याकरण की नींव','Grammar foundations','संज्ञा, सर्वनाम, लिंग, वचन, काल और वाक्य संबंध।','पुस्तकालय'),('जीवन की हिंदी','Everyday Hindi','परिचय, विद्यालय, बाज़ार, यात्रा और बातचीत।','रेल'),('पठन और अभिव्यक्ति','Reading & expression','कहानी, कविता, अनुच्छेद, पत्र और अंतिम अभ्यास।','पत्र')]
C=[]
for line in (R/'source/curriculum.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 p=line.split('|')
 if len(p)==4 and p[0].isdigit():
  n=int(p[0]); C.append(dict(n=n,hi=p[1],en=p[2],art=p[3],phase=(n-1)//10+1,lessons=[]))
 else:
  assert len(p)==9,(line,len(p)); hi,en,vocab,reading,activity,q,a,writing,rule=p
  vs=[v.split('~',1) for v in vocab.split(';')];assert all(len(v)==2 for v in vs)
  C[-1]['lessons'].append(dict(hi=hi,en=en,words=vs,reading=reading.split(';'),activity=activity,q=q,a=a,writing=writing,rule=rule))
assert [c['n'] for c in C]==list(range(1,41)) and all(len(c['lessons'])==2 for c in C)
for c in C:
 c['path']=f'{BASE}/phase-{c["phase"]:02}/chapter-{c["n"]:02}/'
 for i,l in enumerate(c['lessons'],1):l['path']=c['path']+f'lesson-{i:02}/';l['id']=f'beginner-{c["n"]:02}-{i:02}'
L=[l for c in C for l in c['lessons']]
def rel(cur,target):
 if target.startswith('https://'):return target
 trailing=target.endswith('/');x=posixpath.relpath(target.rstrip('/'),cur.rstrip('/'));return x+('/' if trailing else '')
def link(cur,target,label,cls=''):
 return f'<a class="{cls}" href="{E(rel(cur,target))}">{E(label)}</a>'
def pic(cur,w,cls=''):
 if w not in ART:return ''
 return f'<img class="{cls}" src="{E(rel(cur,ART[w]))}" alt="{E(w)}" width="200" height="200" loading="lazy" decoding="async">'
def audio(t):return f'<button class="audio" type="button" data-say="{E(t)}" aria-label="Listen: {E(t)}"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 9h4l5-4v14l-5-4H3zM15 8q5 4 0 8m3-11q8 7 0 14"/></svg></button>'
def heading(hi,en):return f'<div class="section-title"><h2 lang="hi">{E(hi)}</h2><span class="en" lang="en">{E(en)}</span></div>'
def nav(cur,prev,nxt,back):
 return f'<nav class="lesson-nav" aria-label="Lesson navigation">{link(cur,prev,"← पिछला · Back","btn outline") if prev else "<span></span>"}{link(cur,back,"विषय-सूची · Contents","btn outline")}{link(cur,nxt,"आगे · Next →","btn primary") if nxt else link(cur,BASE+"/#final","पुनरावृत्ति · Review","btn primary")}</nav>'
LABS=json.loads((R/'source/labs.json').read_text())
VISUALS=json.loads((R/'source/visual-models.json').read_text())
def visual_model(n,j):
 data=VISUALS.get(f'{n}-{j}')
 if not data:return ''
 choices=data['choices']; first=choices[0]
 buttons=''.join(f'<button type="button" data-model-choice="{i}" aria-pressed="{str(i==0).lower()}">{E(x["label"])}</button>' for i,x in enumerate(choices))
 states=''.join(f'<li>{E(x["label"])}: {E(" ".join(x["parts"]))} — {E(x["note"])}</li>' for x in choices)
 return heading(data['title'],'Visual grammar')+f'<section class="visual-model" data-visual-model data-model="{E(json.dumps(choices,ensure_ascii=False))}"><div class="model-choices">{buttons}</div><div class="model-parts" data-model-parts aria-live="polite">'+''.join(f'<span>{E(x)}</span>' for x in first['parts'])+f'</div><p data-model-note>{E(first["note"])}</p><details><summary>सभी रूप देखें</summary><ul>{states}</ul></details></section>'
def grammar_lab(n,j):
 data=LABS.get(f'{n}-{j}')
 if not data:return ''
 out=[heading('वाक्य प्रयोगशाला','Sentence lab'),'<div class="syntax-lab"><p>'+E(data['prompt'])+'</p>']
 for item in data['items']:
  out.append('<div class="syntax-row" data-quiz><strong>'+E(item['stem'])+'</strong><div class="choices">'+''.join(f'<button type="button" data-correct="{str(x==item["answer"]).lower()}">{E(x)}</button>' for x in item['options'])+'</div><p data-feedback aria-live="polite"></p><details><summary>उत्तर और कारण</summary><p>'+E(item['answer']+' — '+item['why'])+'</p></details></div>')
 return ''.join(out)+'</div>'
def page(cur,hi,en,body,crumb='',desc=None):
 dest=S/cur/'index.html';dest.parent.mkdir(parents=True,exist_ok=True)
 title=f'{hi} — {en} | EkGuru'; css=rel(cur,'css/hindi-beginner-reader.css');js=rel(cur,'js/hindi-beginner-reader.js')
 breadcrumb=f'<nav class="crumb" aria-label="Breadcrumb"><a href="https://ekguru.shop/">EkGuru</a><span>›</span><a href="https://ekguru.shop/learn/">Learn</a><span>›</span><a href="https://ekguru.shop/learn/hindi/">Hindi</a><span>›</span>{link(cur,BASE+"/","प्रारंभिक हिंदी")}{crumb}</nav>'
 desc=desc or f'{en}: प्रारंभिक हिंदी में पढ़ें, सुनें, व्याकरण समझें और लिखें। Free illustrated Hindi textbook lessons and activities.'
 h=f'''<!doctype html><html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, follow"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="https://ekguru.shop/{cur}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="https://ekguru.shop/{cur}"><link rel="stylesheet" href="{css}"><script src="{js}" defer></script></head><body><a class="skip" href="#main">मुख्य पाठ · Skip to lesson</a><header class="top"><div class="top-inner"><a class="brand" href="https://ekguru.shop/"><span class="logo">ए</span> EkGuru</a><div class="top-actions">{link(cur,BASE+"/","पुस्तक 02","book-link")}<button type="button" data-english aria-pressed="true" title="Toggle English assistance">EN</button><button type="button" data-theme aria-label="Toggle dark mode">◐</button></div></div></header><main id="main" class="wrap">{breadcrumb}{body}</main><footer><span>EkGuru · प्रारंभिक हिंदी</span><span lang="en">Free learning · <a href="https://ekguru.shop/editorial-policy/">Editorial policy</a> · <a href="https://ekguru.shop/review/">Suggest a correction</a></span></footer><div class="toast" data-toast role="status" aria-live="polite"></div></body></html>'''
 dest.write_text(h)
def crumbs(c,lesson=False):
 cur=c['path']; return f'<span>›</span>{link(cur,BASE+f"/phase-{c["phase"]:02}/","भाग "+str(c["phase"]))}'
def bookcard(cur,c):
 return f'<a class="chapter-card" href="{rel(cur,c["path"])}"><div class="chapter-thumb">{pic(cur,c["art"])}<span class="chapter-num">{c["n"]:02}</span></div><div><h3>{E(c["hi"])}</h3><span class="en">{E(c["en"])}</span><div class="tiny">2 पाठ · 1 कार्यपत्रक</div><span class="chapter-go">पढ़ें →</span></div></a>'
def stage(cur,i,mini=False):
 hi,en,desc,art=PHASES[i-1]; ch=[c for c in C if c['phase']==i]; t=BASE+f'/phase-{i:02}/'
 return f'<section class="phase"><div class="phase-head"><div><span class="kicker">भाग {i:02} · PHASE {i}</span><h2>{hi}</h2><p>{desc}</p><span class="en">{en}</span></div>{pic(cur,art,"phase-art")}</div><div class="phase-meta"><span>अध्याय {ch[0]["n"]:02}–{ch[-1]["n"]:02}</span>{link(cur,t,"विषय-सूची →","btn outline") if mini else ""}</div><div class="chapter-grid">'+''.join(bookcard(cur,c) for c in ch)+'</div></section>'
cur=BASE+'/'
body=f'''<section class="hero"><div><span class="kicker">पुस्तक 02 · प्रारंभिक हिंदी</span><h1>शब्द से<br><em>अपनी बात तक।</em></h1><p>व्याकरण समझें। कहानी पढ़ें। बातचीत करें और स्वतंत्र रूप से लिखें।</p><span class="en hero-en">Book 02 · Class 1–3 inspired · Independent beginner reader</span><div class="hero-buttons">{link(cur,L[0]['path'],'पहला पाठ पढ़ें →','btn gold')}<a class="btn glass" href="#contents">विषय-सूची</a><a class="btn glass resume" data-resume hidden href="{rel(cur,L[0]['path'])}">जहाँ छोड़ा था →</a></div></div><div class="hero-art"><span class="float a">अ</span><span class="float b">क</span><span class="float c">आ</span><div class="orbit"></div>{pic(cur,'किताब','hero-book')}<div class="hero-icons">{pic(cur,'आम')}{pic(cur,'चिड़िया')}{pic(cur,'पतंग')}</div></div></section><div class="stats"><div><b>4</b><span>भाग</span></div><div><b>40</b><span>अध्याय</span></div><div><b>80</b><span>पाठ</span></div><div><b>40</b><span>कार्यपत्रक</span></div></div><section class="progress" data-book-progress><div><b>मेरी प्रगति</b><p class="en">Saved on this device. No account needed.</p></div><progress max="80" value="0" data-progress></progress><span data-progress-count>0 / 80</span></section><div class="note">प्रवेश: बाल हिंदी या समान वर्णमाला ज्ञान। पहले दो भागों में लिपि और सरल व्याकरण मजबूत करें; फिर बातचीत, पठन और लेखन का स्वतंत्र अभ्यास करें। <span class="en">Draft curriculum; adult guidance and Hindi educator review recommended.</span></div><div class="section-title" id="contents"><h2>विषय-सूची</h2><span class="en">Table of contents</span></div><nav class="phase-jump">'''+''.join(link(cur,BASE+f'/phase-{i:02}/',f'भाग {i} · {PHASES[i-1][0]}','btn outline') for i in range(1,5))+'</nav>'+''.join(stage(cur,i,True) for i in range(1,5))+f'<section class="finish" id="final"><h2>अब आगे क्या?</h2><p>अंतिम अध्याय में अपने पढ़ने, लिखने, बोलने और सुनने का अभ्यास जाँचें।</p>{link(cur,C[-1]["path"],"अंतिम अभ्यास →","btn primary")} {link(cur,"https://ekguru.shop/learn/hindi/intermediate/","अगली किताब · मौजूदा मध्यम पाठ","btn outline")}</section>'
page(cur,'प्रारंभिक हिंदी','Book 2: Beginner Hindi',body)
for i in range(1,5):
 cur=BASE+f'/phase-{i:02}/';hi,en,_,_=PHASES[i-1];body=f'<div class="reader-head"><span class="kicker">पुस्तक 02 / भाग {i:02}</span><h1>{hi}</h1><p class="en">{en}</p></div>'+stage(cur,i)+nav(cur,BASE+f'/phase-{i-1:02}/' if i>1 else None,BASE+f'/phase-{i+1:02}/' if i<4 else C[-1]['path'],BASE+'/');page(cur,hi,en,body)
for c in C:
 cur=c['path']; n=c['n'];ph=BASE+f'/phase-{c["phase"]:02}/';previous=C[n-2]['path'] if n>1 else None;nextc=C[n]['path'] if n<40 else None
 crumb=f'<span>›</span>{link(cur,ph,"भाग "+str(c["phase"]))}<span>›</span> अध्याय {n:02}'
 body=f'<section class="chapter-hero"><div><span class="kicker">भाग {c["phase"]:02} · अध्याय {n:02}</span><h1>{E(c["hi"])}</h1><p class="en">{E(c["en"])}</p><p>दो पाठों में नियम, उदाहरण और स्वतंत्र अभ्यास पूरा करें।</p>{link(cur,c["lessons"][0]["path"],"पाठ 1 शुरू करें →","btn primary")}</div>{pic(cur,c["art"],"chapter-art")}</section>'+heading('इस अध्याय के पाठ','Lessons')+'<div class="lesson-grid">'
 for j,l in enumerate(c['lessons'],1):
  body+=f'<a class="lesson-card" href="{rel(cur,l["path"])}"><span class="round-number">0{j}</span><div><h3>{E(l["hi"])}</h3><span class="en">{E(l["en"])}</span><p>{E(" · ".join(w[0] for w in l["words"][:4]))}</p></div><span>→</span></a>'
 body+='</div>'+heading('अभ्यास और लेखन','Practice')+f'<div class="sheet-callout"><div><h3>कॉपी में लिखें और कार्यपत्रक पूरा करें</h3><span class="en">Guided copying · Questions · Answer key</span></div>{link(cur,cur+"worksheet/","कार्यपत्रक →","btn outline")}</div>'+nav(cur,previous,nextc,ph)
 page(cur,c['hi'],c['en'],body,crumb)
 for j,l in enumerate(c['lessons'],1):
  cur=l['path']; idx=(n-1)*2+j-1; crumb=f'<span>›</span>{link(cur,ph,"भाग "+str(c["phase"]))}<span>›</span>{link(cur,c["path"],"अध्याय "+str(n))}<span>›</span>पाठ {j}'
  body=f'<div class="reader-layout"><aside class="reader-side"><span class="kicker">पुस्तक 02</span><b>भाग {c["phase"]}: {PHASES[c["phase"]-1][0]}</b><div class="toc">'+''.join(link(cur,x['path'],f'{x["n"]:02} · {x["hi"]}', 'current' if x==c else '') for x in C if x['phase']==c['phase'])+f'</div>{link(cur,c["path"],"अध्याय की विषय-सूची →")}</aside><article class="reader"><header class="reader-head"><span class="kicker">अध्याय {n:02} / पाठ {j:02}</span><h1>{E(l["hi"])}</h1><p class="en">{E(l["en"])}</p><div class="reader-tools"><button type="button" data-say="{E(" ".join(w[0] for w in l["words"]))}" class="btn primary">▶ शब्द सुनें</button><button type="button" data-slow class="btn outline" aria-pressed="false">धीमे सुनें</button><button type="button" data-stop class="btn outline">रोकें</button></div><small class="en">Audio uses your device’s Hindi voice; availability varies. No native recordings included.</small></header>'
  body+=heading('आज का नियम','Understand the concept')+f'<div class="concept-box"><p>{E(l["rule"])}</p></div>'+heading('शब्द और अर्थ','Vocabulary')+'<div class="word-grid">'
  for w,m in l['words']:
   visual=pic(cur,w,'word-img') or f'<div class="word-glyph" aria-hidden="true">{E(w)}</div>'
   body+=f'<div class="word-card">{visual}<div class="word-label"><b>{E(w)}</b>{audio(w)}</div><span class="en" lang="en">{E(m)}</span></div>'
  body+='</div>'
  if n in [2,3,4,5,6]:
   signs=['','ा','ि','ी','ु','ू','ृ','े','ै','ो','ौ','ं','ः']; consonants=list('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह')
   body+=heading('मात्रा जोड़ो','Build a syllable')+'<div class="matra-lab"><div class="matra-display" data-matra-display>क</div><label>व्यंजन <select data-base>'+''.join(f'<option>{k}</option>' for k in consonants)+'</select></label><div class="matra-buttons">'+''.join(f'<button type="button" data-matra="{s}">{s or "अ"}</button>' for s in signs)+'</div><button type="button" class="btn outline" data-matra-audio>▶ सुनें</button><p>पहले व्यंजन चुनो, फिर मात्रा। आकृति बदलते हुए देखो।</p></div>'
   if n==6:
    body+='<details class="chart"><summary>सभी 33 व्यंजनों की बारहखड़ी · 13 रूप</summary><div class="table-scroll"><table><thead><tr>'+''.join(f'<th>{s or "अ"}</th>' for s in signs)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{k+s}</td>' for s in signs)+'</tr>' for k in consonants)+'</tbody></table></div><p>ये अभ्यास के लिए रूप हैं; सभी रूप सामान्य शब्द नहीं हैं।</p></details>'
  if n in [2,3,4,5,8,10,21,22,23,25,26,27,28,29,35,36,39]:
   candidates=[w for w,m in l['words'] if w in ART]
   if len(candidates)>=2:
    body+=heading('चित्र देखकर बोलो','Picture talk')+'<div class="picture-strip">'+''.join(f'<figure>{pic(cur,w)}<figcaption>{E(w)} {audio(w)}</figcaption></figure>' for w in candidates[:6])+'</div>'
  if n==15:
   body+='<div class="colour-strip" aria-label="Colour examples">'+''.join(f'<div><span style="background:{color}"></span><b>{name}</b></div>' for name,color in [('लाल','#c94343'),('पीला','#f4c744'),('हरा','#429364'),('नीला','#397bb9'),('सफेद','#fff'),('काला','#232323'),('गुलाबी','#e18da9'),('नारंगी','#ec893f'),('बैंगनी','#9061a9'),('भूरा','#946448')])+'</div>'
  if n==24:
   body+='<div class="number-lab"><label>गिनती चुनें <input type="range" min="1" max="20" value="5" data-count></label><output data-count-out>5 · ५</output><div class="count-dots" data-dots>'+ '<i></i>'*5 +'</div></div>'
  body+=visual_model(n,j)+grammar_lab(n,j)
  body+=heading('उदाहरण और पठन','Examples & reading')+'<div class="reading">'+''.join(f'<p><span>{E(line)}</span>{audio(line)}</p>' for line in l['reading'])+'</div>'
  body+=heading('बोलें और सोचें','Apply it')+f'<div class="activity"><span class="activity-icon">✦</span><p>{E(l["activity"])}</p></div>'
  body+=heading('लेखन अभ्यास','Writing practice')+f'<div class="copy-board"><div class="copy-model">{E(l["writing"])}</div><div class="copy-model ghost">{E(l["writing"])}</div><div class="copy-line"></div><div class="copy-line"></div></div><p class="hint">उदाहरण ध्यान से पढ़ें। फिर कॉपी में लिखें और अपने दो नए वाक्य बनाएँ।</p><div class="draw-pad"><canvas data-draw width="720" height="230" aria-label="Freehand writing practice"></canvas><div><button type="button" class="btn outline" data-undo>↶ वापस</button> <button type="button" class="btn outline" data-clear>साफ करें</button></div><small class="en">Freehand practice, not automatic handwriting scoring or verified stroke order.</small></div>'
  # two different recognition questions: authored comprehension plus vocabulary meaning check
  body+=heading('अपना ज्ञान जाँचें','Check your learning')+f'<div class="check"><h3>{E(l["q"])}</h3><details><summary>उत्तर देखें</summary><p>{E(l["a"])}</p></details></div>'
  w,m=l['words'][0]; options=[x for x in l['words'][1:] if x[1]!=m and x[0]!=w][:3]+[l['words'][0]]
  body+=f'<div class="check" data-quiz><h3>इस पाठ में दिए गए अर्थ से शब्द मिलाएँ: <span lang="en">{E(m)}</span></h3><div class="choices">'+''.join(f'<button type="button" data-correct="{str(x[0]==w).lower()}">{E(x[0])}</button>' for x in options)+'</div><p data-feedback aria-live="polite"></p><details><summary>उत्तर</summary><p>'+E(w)+'</p></details></div>'
  body+=f'<div class="finish"><button class="btn primary" type="button" data-complete="{l["id"]}">✓ पाठ पूरा किया</button>{link(cur,c["path"]+"worksheet/","कार्यपत्रक · Worksheet","btn outline")}<p class="en">Completion is self-marked and saved locally.</p></div>'+nav(cur,L[idx-1]['path'] if idx else None,L[idx+1]['path'] if idx+1<len(L) else None,c['path'])+'</article></div>'
  page(cur,l['hi'],l['en'],body,crumb)
 # One actual printable chapter worksheet, with separate answer disclosure.
 cur=c['path']+'worksheet/';body=f'<section class="worksheet"><div class="reader-head"><span class="kicker">अध्याय {n:02} / कार्यपत्रक</span><h1>{E(c["hi"])}</h1><p class="en">Printable practice sheet</p><div class="print-tools"><button class="btn primary" data-print type="button">Print / Save PDF</button><button class="btn outline" data-ink type="button" aria-pressed="false">Ink-saving</button></div></div><p>नाम: ____________________ &nbsp; दिनांक: ______________</p>'
 for j,l in enumerate(c['lessons'],1):
  body+=f'<section class="worksheet-part"><h2>{j}. {E(l["hi"])}</h2><p>क. उदाहरण लिखिए, फिर अपना एक उदाहरण बनाइए।</p><div class="copy-board"><div class="copy-model ghost">{E(l["writing"])}</div><div class="copy-line"></div><div class="copy-line"></div><div class="copy-line"></div></div><p>ख. {E(l["q"])}</p><div class="blank"></div><p>ग. सही अर्थ / शब्द जोड़ो।</p><div class="worksheet-match"><ol>'+''.join(f'<li>{E(w)} __________</li>' for w,m in l['words'][:3])+'</ol><ol type="A">'+''.join(f'<li>{E(m)}</li>' for w,m in reversed(l['words'][:3]))+'</ol></div><p>घ. '+E(l['activity'])+'</p><div class="blank"></div></section>'
 body+='<details class="answer-key"><summary>उत्तर कुंजी · Answer key</summary>'+''.join(f'<h3>{j}. {E(l["hi"])}</h3><p>{E(l["a"])}</p><p>'+E(' · '.join(f'{w} — {m}' for w,m in l['words'][:3]))+'</p>' for j,l in enumerate(c['lessons'],1))+'</details></section>'+nav(cur,None,c['lessons'][1]['path'],c['path'])
 page(cur,c['hi']+' — कार्यपत्रक',c['en']+' worksheet',body)
manifest={'version':1,'id':'beginner','status':'draft-review-required','root':BASE,'phases':[{'id':i,'hi':p[0],'en':p[1],'chapters':[c for c in C if c['phase']==i]} for i,p in enumerate(PHASES,1)]}
(S/'data/learning').mkdir(parents=True,exist_ok=True);(S/'data/learning/hindi-beginner-book.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(f'Generated {len(list((S/BASE).rglob("index.html")))} pages, {len(C)} chapters, {len(L)} lessons, {sum(len(l["words"]) for l in L)} word entries, {sum(len(l["reading"]) for l in L)} reading examples.')
