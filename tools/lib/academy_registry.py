"""Language-neutral, versioned Academy registry helpers (static build time only).

Entries point at real pages, never at planned placeholders. Existing pages remain
owned by their existing generators. Relationship validation is deliberately strict.
"""
import html
import json
import re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

KINDS = ('languages', 'courses', 'levels', 'phases', 'chapters', 'lessons', 'activities', 'resources', 'vocabulary')
ID = re.compile(r'^[a-z0-9][a-z0-9-]*$')

def esc(s):
    return html.escape(str(s), quote=True)

def target(root, url):
    u = urlsplit(url)
    if u.scheme or u.netloc or u.query or not u.path.startswith('/') or '..' in unquote(u.path).split('/') or '//' in u.path:
        raise ValueError('unsafe URL: ' + url)
    path = root / unquote(u.path).lstrip('/')
    if u.path.endswith('/'): path = path / 'index.html'
    if not path.is_file(): raise ValueError('missing URL: ' + url)
    if u.fragment:
        text = path.read_text(encoding='utf8')
        if not re.search(r'\bid=["\']' + re.escape(unquote(u.fragment)) + r'["\']', text):
            raise ValueError('missing fragment: ' + url)
    return path

def validate(data, root):
    if data.get('version') != 2: raise ValueError('unsupported registry version')
    all_ids = set()
    indexes = {}
    for kind in KINDS:
        records = data.get(kind)
        if not isinstance(records, list): raise ValueError('missing list: ' + kind)
        indexes[kind] = {}
        for x in records:
            ident = x.get('id', '')
            if not ID.fullmatch(ident) or ident in all_ids: raise ValueError('invalid or duplicate id: ' + ident)
            all_ids.add(ident); indexes[kind][ident] = x
            if 'url' in x: target(root, x['url'])
            if 'catalogue_url' in x: target(root, x['catalogue_url'])
    for track in data.get('tracks', []):
        for x in [track, *track.get('phases', [])]:
            ident = x.get('id', '')
            if not ID.fullmatch(ident) or ident in all_ids: raise ValueError('invalid or duplicate id: ' + ident)
            all_ids.add(ident)
            if 'url' in x: target(root, x['url'])
    for kind, field, parent in [('courses','language','languages'), ('levels','language','languages'), ('phases','course','courses'), ('phases','level','levels'), ('chapters','phase','phases'), ('lessons','phase','phases'), ('activities','lesson','lessons'), ('resources','lesson','lessons'), ('vocabulary','lesson','lessons')]:
        for x in data[kind]:
            if x.get(field) not in indexes[parent]: raise ValueError(f'{kind}: {x["id"]} has unknown {field}')
    for x in data['lessons']:
        if x.get('chapter') and x['chapter'] not in indexes['chapters']: raise ValueError('unknown chapter')
        if x.get('chapter') and indexes['chapters'][x['chapter']]['phase'] != x['phase']: raise ValueError('chapter and lesson phases disagree')
        if x.get('audio') not in ('none','device','recorded'): raise ValueError('invalid audio status')
        if not isinstance(x.get('worksheet'), bool): raise ValueError('invalid worksheet status')
        if x['worksheet'] and not any(r['lesson'] == x['id'] and r['kind'] == 'worksheet' for r in data['resources']): raise ValueError('worksheet claim has no resource')
    for resource in data['resources']:
        if resource.get('kind') == 'recorded-audio':
            if Path(urlsplit(resource['url']).path).suffix.lower() not in ('.mp3', '.ogg', '.opus', '.wav', '.m4a'):
                raise ValueError('recorded audio must point to an audio file')
            if resource.get('license') not in ('CC0-1.0', 'CC-BY-4.0', 'CC-BY-SA-4.0', 'owner-recorded'):
                raise ValueError('recorded audio requires an allowed license')
    for lesson in data['lessons']:
        if lesson['audio']=='recorded' and not any(r['lesson']==lesson['id'] and r.get('kind')=='recorded-audio' for r in data['resources']):
            raise ValueError('recording claim has no audio resource')
    for p in data['phases']:
        if indexes['courses'][p['course']]['language'] != indexes['levels'][p['level']]['language']: raise ValueError('phase language mismatch')
    if "textbook" in data or "character_coverage" in data:
        validate_textbook(data, indexes, root)
    return indexes

REQUIRED_CHARACTERS = {
    'independent-vowel': list('अआइईउऊऋएऐओऔ'),
    'traditional-chart-form': ['अं', 'अः', 'अँ'],
    'consonant': list('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह'),
    'additional-letter': ['ड़', 'ढ़', 'क़', 'ख़', 'ग़', 'ज़', 'फ़'],
    'conjunct': ['क्ष', 'त्र', 'ज्ञ', 'श्र'],
    'vowel-sign': ['ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ'],
    'mark': ['ं', 'ँ', 'ः', '्'],
}

def validate_textbook(data, indexes, root):
    """Validate planned relationships without publishing or inventing lessons.

    Existing lessons remain in the shared registry, so a chapter references the
    source rather than copying it. Planned URLs are never treated as live links.
    """
    model=data.get('textbook', {})
    coverage=data.get('character_coverage', {})
    if model.get('version') != 2 or coverage.get('version') != 1:
        raise ValueError('textbook and character coverage version required')
    pathways=model.get('pathways')
    if not isinstance(pathways,list) or [p.get('id') for p in pathways] != ['academic','adult']:
        raise ValueError('independent academic and adult pathways required')
    expected={'academic':['kids','beginner','intermediate','advanced','mastery'],
              'adult':['adult-foundation','adult-beginner','adult-intermediate','adult-advanced','adult-mastery']}
    seen=set(); seen_paths=set(); lesson_owner={}
    def identifier(value):
        if not isinstance(value,str) or not ID.fullmatch(value) or value in seen:
            raise ValueError('invalid or duplicate textbook id: '+str(value))
        seen.add(value)
    for pathway in pathways:
        identifier(pathway['id'])
        if pathway.get('planned_url') != ('/learn/hindi/' if pathway['id']=='academic' else '/learn/hindi/older-adults/'):
            raise ValueError('invalid pathway route')
        books=pathway.get('books')
        if not isinstance(books,list) or [b.get('id') for b in books] != expected[pathway['id']]:
            raise ValueError('five ordered books or adult stages required')
        previous=None
        for book in books:
            identifier(book.get('id'))
            fields=('title_hi','title_en','age_guidance','prerequisites','entry_competencies','exit_competencies',
                    'vocabulary_targets','grammar_coverage','reading_complexity','writing_complexity',
                    'speaking_ability','listening_comprehension','assessment_criteria')
            if not all(isinstance(book.get(k),str) and book[k].strip() for k in fields):
                raise ValueError('book requires competency planning fields')
            if book.get('prerequisite_book_ids') != ([previous] if previous else []):
                raise ValueError('prerequisite progression must stay within its own pathway')
            previous=book['id']
            slug=book['id'].removeprefix('adult-') if pathway['id']=='adult' else book['id']
            prefix=('/learn/hindi/older-adults/' if pathway['id']=='adult' else '/learn/hindi/')+slug+'/'
            if book.get('planned_url') != prefix or prefix in seen_paths: raise ValueError('invalid book route')
            seen_paths.add(prefix)
            phases=book.get('phases')
            if not isinstance(phases,list) or len(phases)!=4: raise ValueError('book requires four phases')
            for n,phase in enumerate(phases,1):
                identifier(phase.get('id'))
                suffix='phase-%02d' % n
                if phase['id'] != book['id']+'-'+suffix or phase.get('planned_url') != prefix+suffix+'/':
                    raise ValueError('invalid phase route')
                if phase['planned_url'] in seen_paths: raise ValueError('duplicate phase route')
                seen_paths.add(phase['planned_url'])
                if not phase.get('title') or not isinstance(phase.get('chapters'),list): raise ValueError('invalid phase')
                topics=phase.get('planned_topics')
                if not isinstance(topics,list) or any(not x.get('title_hi') or x.get('status')!='planned-not-a-lesson' for x in topics):
                    raise ValueError('unpublished topics must be clearly identified')
                for chapter in phase['chapters']:
                    identifier(chapter.get('id'))
                    ids=chapter.get('lesson_ids')
                    if not chapter.get('title') or not isinstance(ids,list) or not ids or len(set(ids))!=len(ids): raise ValueError('chapter requires real lessons')
                    if any(x not in indexes['lessons'] for x in ids): raise ValueError('unknown lesson reference')
                    if chapter.get('source_url') != indexes['lessons'][ids[0]]['url']: raise ValueError('chapter source mismatch')
                    if chapter.get('status') not in ('existing-draft','reviewed'): raise ValueError('chapter status required')
                    for id in ids:
                        if id in lesson_owner: raise ValueError('the same lesson cannot be counted as multiple textbook chapters')
                        lesson_owner[id]=book['id']
                if phase.get('status') != 'incomplete' or book.get('status') != 'incomplete':
                    raise ValueError('completion requires a future verified completeness gate')
    picture_file=root/'data/learning/hindi-textbook-illustrations.json'
    pictures=json.loads(picture_file.read_text(encoding='utf8')) if picture_file.is_file() else []
    picture_keys={(r['character'],r['word'],r['path'],r['review']) for r in pictures}
    chars=coverage.get('characters')
    if not isinstance(chars,list): raise ValueError('characters required')
    pairs=[]
    for item in chars:
        pair=(item.get('category'),item.get('character'))
        if pair in pairs: raise ValueError('duplicate character coverage')
        pairs.append(pair)
        refs=item.get('existing_group_lesson_ids')
        if not isinstance(refs,list) or any(x not in indexes['lessons'] for x in refs): raise ValueError('unknown character source')
        if item.get('complete') is not False: raise ValueError('character completion requires future verification gate')
        if item.get('illustration'):
            image=item['illustration']
            if (item['character'],image.get('word'),image.get('path'),image.get('review')) not in picture_keys: raise ValueError('illustration does not match visual manifest')
            target(root,'/'+image['path'])
        if any(not item.get(k) for k in ('individual_lesson','stroke_order','educational_illustrations','human_audio','worksheet','editorial_review')):
            raise ValueError('character coverage review fields required')
    required={(category,c) for category, values in REQUIRED_CHARACTERS.items() for c in values}
    if not required.issubset(set(pairs)): raise ValueError('required character coverage record missing')
    inherent=coverage.get('inherent_vowel',{})
    if inherent.get('complete') is not False or any(x not in indexes['lessons'] for x in inherent.get('existing_group_lesson_ids',[])):
        raise ValueError('invalid inherent vowel coverage')
    return True

def rows(data):
    ix = {kind:{x['id']:x for x in data[kind]} for kind in KINDS}
    result = []
    for lesson in data['lessons']:
        phase=ix['phases'][lesson['phase']]; course=ix['courses'][phase['course']]
        chapter=ix['chapters'].get(lesson.get('chapter'))
        related=[r for r in data['resources'] if r['lesson']==lesson['id']]
        words=[w for w in data['vocabulary'] if w['lesson']==lesson['id']]
        terms=' '.join([r['title'] for r in related] + [' '.join([w.get('hi',''), w.get('roman',''), w.get('meaning','')]) for w in words])
        audio='recorded' if any(r.get('kind')=='recorded-audio' for r in related) else ('device' if any(r.get('kind')=='device-audio' for r in related) else lesson['audio'])
        result.append({**lesson, 'audio':audio, 'worksheet':lesson['worksheet'] or any(r.get('kind')=='worksheet' for r in related), 'terms':terms, 'course':course['id'], 'course_title':course['title'], 'phase_title':phase['title'], 'chapter_title':chapter['title'] if chapter else '', 'level_title':ix['levels'][phase['level']]['title']})
    return result

def search_index(data):
    return {'version':2, 'lessons':rows(data)}

def counts(data):
    return {kind:len(data[kind]) for kind in KINDS}

def nav(data, lesson_id):
    items=rows(data); current=next(x for x in items if x['id']==lesson_id)
    ordered=[x for x in items if x['course']==current['course']]
    i=next(i for i,x in enumerate(ordered) if x['id']==lesson_id)
    return {'current':current, 'previous':ordered[i-1] if i else None, 'next':ordered[i+1] if i+1<len(ordered) else None}

def catalogue_html(data):
    items=rows(data)
    parts=[]
    for phase in data['phases']:
        related=[x for x in items if x['phase']==phase['id']]
        if not related: continue
        parts.append(f'<details open class="ac-directory-group" id="phase-{esc(phase["id"])}"><summary>{esc(phase["title"])} <span>({len(related)} lessons)</span></summary><ul>')
        for x in related:
            parts.append(f'<li data-catalogue-id="{esc(x["id"])}"><a href="{esc(x["url"])}">{esc(x["title"])}</a> <span>{esc(x["level_title"])} · {esc(x["topic"])}</span></li>')
        parts.append('</ul></details>')
    return '\n'.join(parts)

class HeadMetadata(HTMLParser):
    def __init__(self):
        super().__init__(); self.robots=''; self.canonical=''
    def handle_starttag(self, tag, attrs):
        attr=dict(attrs)
        if tag=='meta' and attr.get('name','').lower()=='robots': self.robots=attr.get('content','')
        if tag=='link' and 'canonical' in attr.get('rel','').lower().split(): self.canonical=attr.get('href','')

def publication(root, url):
    parser=HeadMetadata(); parser.feed(target(root, url).read_text(encoding='utf8').split('</head>',1)[0])
    expected='https://ekguru.shop'+urlsplit(url).path
    robots={part.strip() for part in parser.robots.lower().split(',')}
    return {'canonical':parser.canonical, 'indexable':'noindex' not in robots and parser.canonical == expected}

def index_json(data, root=None):
    result=search_index(data)
    if root is not None:
        for row in result['lessons']: row['publication']=publication(root,row['url'])
    return json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n'

def lesson_navigation(data, lesson_id):
    step = nav(data, lesson_id); current=step['current']
    course=next(x for x in data['courses'] if x['id']==current['course'])
    phase_url=course.get('catalogue_url', course['url'])+'#phase-'+current['phase'] if course.get('catalogue_url') else course['url']
    crumb=f'<nav aria-label="Course breadcrumb"><a href="{esc(course["url"])}">{esc(course["title"])}</a> / <a href="{esc(phase_url)}">{esc(current["phase_title"])}</a>'
    if current['chapter_title']: crumb+=' / '+esc(current['chapter_title'])
    crumb+='</nav>'
    links = []
    for key, label in [('previous', 'Previous lesson'), ('next', 'Next lesson')]:
        item = step[key]
        if item: links.append(f'<a href="{esc(item["url"])}">{label}: {esc(item["title"])}</a>')
    related=[x for x in data['resources'] if x['lesson']==lesson_id]
    resources=''.join(f'<li><a href="{esc(r["url"])}">{esc(r["title"])}</a></li>' for r in related)
    return crumb+'<nav aria-label="Course lesson sequence" class="chapter-nav">'+' '.join(links)+'</nav>'+('<p>Related resources</p><ul>'+resources+'</ul>' if related else '')


def home_html(data, day_count):
    """Bounded homepage: track cards, course summaries and links to studios."""
    c=counts(data)
    cards=[]
    icons=['✦','अ','◈','✺','☼']
    for i,t in enumerate(data['tracks']):
        cards.append(f'<a class="ac-track ac-track-{i%5}" href="/learn/hindi/academy/#{esc(t["id"])}"><span class="ac-track-icon" aria-hidden="true">{icons[i%5]}</span><span class="ac-track-kicker">LEARNING PATH {i+1:02}</span><strong>{esc(t["title"])}</strong><span>{esc(t["description"])}</span><b>Explore path <span aria-hidden="true">↗</span></b></a>')
    courses=[]
    for course in data['courses']:
        phases=[p for p in data['phases'] if p['course']==course['id']]
        lessons=[x for x in rows(data) if x['course']==course['id']]
        phase_links=''.join(f'<li><a href="{esc(course.get("catalogue_url", course["url"]))}#phase-{esc(p["id"])}">{esc(p["title"])}</a></li>' for p in phases)
        chapter_count=sum(1 for x in data['chapters'] if x['phase'] in {p['id'] for p in phases})
        courses.append(f'<details class="ac-explorer"><summary><span><strong>{esc(course["title"])}</strong><small>{len(phases)} phases · {chapter_count} registered chapters · {len(lessons)} registered lessons</small></span><span aria-hidden="true">＋</span></summary><p>{esc(course.get("description", ""))}</p><ol>{phase_links}</ol><a href="{esc(course["url"])}">Open course →</a></details>')
    studios=[('✎','Writing & Devanagari','Learn the script, matras and handwriting.','/learn/hindi/foundation/'),('◖','Listening & pronunciation','Hear, compare and practise Hindi sounds.','/learn/practice/pronunciation/'),('अ','Vocabulary & grammar','Build the words and patterns you need.','/learn/hindi/vocabulary/'),('▤','Reading & stories','Read from first letters to longer texts.','/learn/practice/reading/'),('◇','Games & practice labs','Put what you learn into practice.','/learn/hindi/practice/'),('▧','Printable worksheets','Take your Hindi practice to paper.','/learn/hindi/practice/worksheets/')]
    studio_cards=''.join(f'<a class="ac-studio-card" href="{esc(u)}"><span aria-hidden="true">{ico}</span><strong>{esc(title)}</strong><small>{esc(desc)}</small><b aria-hidden="true">↗</b></a>' for ico,title,desc,u in studios)
    return f'''<div class="ac-home" id="academy-home">
<section class="ac-hero" aria-labelledby="ac-hero-title"><div class="ac-hero-copy"><p class="ac-eyebrow">✦ &nbsp; THE FREE HINDI LEARNING ACADEMY</p><h2 id="ac-hero-title">A little Hindi,<br><em>a world of connection.</em></h2><p>From your very first letter to the conversations that matter. Find your path, practise at your pace, and make Hindi part of your everyday.</p><div class="ac-actions"><a class="ac-primary" href="/learn/hindi/academy/vowels/">Start learning <span aria-hidden="true">↗</span></a><a class="ac-outline" href="/learn/practice/placement/">Find my level →</a></div><p class="ac-trust">✦ Free to learn &nbsp; · &nbsp; No account needed &nbsp; · &nbsp; Your own pace</p></div><img src="/images/hindi-academy-hero.webp" width="1200" height="670" alt="" aria-hidden="true" fetchpriority="high"></section>
<div class="ac-welcome"><div><span class="ac-eyebrow">YOUR JOURNEY, YOUR WAY</span><h2>Namaste, learner. <span lang="hi">नमस्ते</span></h2><p>Whether you’re beginning or building on what you know, there’s a place for you here.</p></div><div class="ac-continue"><span class="ac-icon" aria-hidden="true">↗</span><div><strong>Pick up where you left off</strong><p data-eg-continue data-eg-language="hi"><a href="/learn/hindi/my-progress/">Open your learning journal →</a></p></div></div></div>
<section class="ac-stats" aria-label="Academy at a glance"><div><b>{len(data['tracks']):02}</b><span>learning paths<small>choose your own route</small></span></div><div><b>{c['lessons']:02}</b><span>registered lessons<small>in this first catalogue</small></span></div><div><b>{day_count}</b><span>days of Hindi<small>in the existing daily course</small></span></div><div><b>Free</b><span>self-paced learning<small>no account needed</small></span></div></section>
<section class="ac-section" id="ac-paths"><div class="ac-heading"><div><p class="ac-eyebrow">FIND YOUR WAY</p><h2>One language. <em>Your journey.</em></h2><p>Choose a suggested route based on your interests, not your age or a test score.</p></div><a href="/learn/hindi/academy/">View all paths ↗</a></div><div class="ac-track-grid">{''.join(cards)}</div><p class="ac-note">These paths curate existing resources; dedicated age-specific courses are still in development.</p></section>
<section class="ac-section ac-explore-section" id="ac-explorer"><div class="ac-heading"><div><p class="ac-eyebrow">EXPLORE AT YOUR PACE</p><h2>Your course, <em>your pace.</em></h2><p>Browse a registered course by phase, or explore proficiency separately.</p></div><a href="/learn/hindi/academy/catalogue/">Browse lesson catalogue ↗</a></div><div class="ac-explorer-grid"><div>{''.join(courses)}</div><div class="ac-levels"><span class="ac-track-kicker">PROFICIENCY EXPLORER</span><h3>Find your next step</h3><p>A1–C2 is a separate proficiency dimension. EkGuru’s additional levels are not official CEFR levels.</p><div>{''.join(f'<a href="/languages/hi/level/{level.lower()}/">{level}</a>' for level in ['A1','A2','B1','B2','C1','C2'])}</div><a href="/how-levels-work/">How levels work →</a></div></div><div class="ac-search-callout"><div><strong>Looking for something specific?</strong><p>Search registered lessons by topic, course, phase or skill.</p></div><a class="ac-primary" href="/learn/hindi/academy/catalogue/">Search lesson catalogue ↗</a></div></section>
<section class="ac-section" id="ac-studio"><div class="ac-heading"><div><p class="ac-eyebrow">THE LEARNING STUDIO</p><h2>Make Hindi <em>your own.</em></h2><p>Explore the skills, tools and resources that make practice feel natural.</p></div><a href="/learn/hindi/practice/">Explore all practice ↗</a></div><div class="ac-studio-grid">{studio_cards}</div></section>
<section class="ac-bottom-grid"><div class="ac-daily"><p class="ac-eyebrow">A LITTLE EVERY DAY</p><h2>Small steps.<br><em>Big progress.</em></h2><p>Build a habit with one idea and a little practice each day.</p><a href="/daily-hindi/">Explore Daily Hindi →</a></div><div class="ac-review"><p class="ac-eyebrow">YOUR LEARNING, SAVED LOCALLY</p><h2>Keep your momentum.</h2><p>Review what you have learned and see your self-reported progress on this device.</p><a href="/learn/hindi/my-progress/">Open your journal →</a> <a href="/learn/hindi/review/">Review words →</a></div></section>
<section class="ac-faq"><p class="ac-eyebrow">GOOD TO KNOW</p><h2>Questions, answered.</h2><details><summary>Is self-paced Hindi learning free?</summary><p>Yes. Lessons, practice and learning tools are free and do not require an account.</p></details><details><summary>Where should I begin?</summary><p>Try the <a href="/learn/hindi/academy/vowels/">vowels companion</a>, the <a href="/learn/hindi/foundation/">foundation course</a> or the <a href="/learn/practice/placement/">starting-point check</a>.</p></details><details><summary>Do I need a tutor?</summary><p>No. Independent tutor lessons are optional; you can study on your own.</p></details></section>
<div class="ac-final"><div><p class="ac-eyebrow">A LITTLE HELP, IF YOU WANT IT</p><h2>Learn on your own. <em>Or together.</em></h2><p>Self-paced learning is free. Explore independent tutors if you’d like personal guidance.</p></div><a class="ac-primary" href="/find-tutors.html">Meet independent tutors ↗</a></div><p class="ac-other"><a href="/learn/">Exploring another language? Discover all language courses →</a></p>
</div>'''
