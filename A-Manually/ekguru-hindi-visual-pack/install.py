#!/usr/bin/env python3
"""Apply the original EkGuru foundation picture pack to a compatible checkout.
Dry-run by default. Does not run git, deploy, install dependencies or edit unrelated paths.
"""
import argparse, html, json, re, shutil, sys
from pathlib import Path
import xml.etree.ElementTree as ET
PACK = Path(__file__).resolve().parent
RECORDS = json.loads((PACK/'illustrations.json').read_text(encoding='utf-8'))
GROUPS = ('swar', 'vyanjan-1', 'vyanjan-2', 'vyanjan-3')
MANIFEST = 'data/learning/hindi-textbook-illustrations.json'
GEN = 'tools/build-hindi-foundation.py'
CSS = 'css/foundation.css'
OLD_RULE = '.fd-letter .kw i{font-style:normal;font-size:1.5rem;display:block}'
NEW_RULE = OLD_RULE + '\n.fd-letter .fd-picture{display:block;width:min(100%,180px);height:auto;aspect-ratio:4/3;object-fit:contain;margin:4px auto 9px;border-radius:10px}'
ANIM_RULE = '''
.fd-air-demo{margin:18px 0;padding:14px;border:1px solid var(--line);border-radius:12px;background:var(--bg,#fff)}
.fd-air-demo summary{cursor:pointer;font-weight:600}
.fd-air-demo svg{display:block;width:min(100%,480px);height:auto;margin:10px auto}
.fd-air-demo .air{transform-box:fill-box;transform-origin:center;opacity:.75}
.fd-air-demo[open] .air{animation:fd-air-puff 1.5s ease-out 2}
.fd-air-demo[open] .air.strong{animation-delay:.2s}
@keyframes fd-air-puff{0%{transform:translateX(-12px) scale(.6);opacity:.2}60%{opacity:1}100%{transform:translateX(18px) scale(1.08);opacity:.75}}
@media(prefers-reduced-motion:reduce){.fd-air-demo[open] .air{animation:none}}
@media print{.fd-letter .fd-picture{width:95px}.fd-air-demo .air{animation:none!important}}
'''.strip()
DEMO = '''<details class="fd-air-demo"><summary lang="hi">क और ख — हवा का अंतर (Airflow)</summary><p lang="hi">हथेली मुँह के सामने रखिए। क बोलिए, फिर ख। ख में हवा का झोंका अधिक महसूस होता है।</p><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 124" role="img" aria-label="Schematic: a smaller air puff for ka, a stronger puff for kha"><rect x="1" y="1" width="318" height="122" rx="12" fill="#fff9ed" stroke="#d5cbb7"/><g stroke="#294d43" stroke-width="3" stroke-linecap="round" fill="none"><path d="M30 12Q65 11 65 27L76 31 66 37Q65 46 45 47M30 74Q65 73 65 89L76 93 66 99Q65 108 45 109"/><path d="M190 12V48M190 74V110" stroke="#8d7456" stroke-width="8"/></g><g fill="#357f93"><g class="air"><circle cx="104" cy="32" r="4"/><circle cx="124" cy="32" r="3"/></g><g class="air strong"><circle cx="103" cy="93" r="7"/><circle cx="125" cy="82" r="5"/><circle cx="126" cy="103" r="5"/><circle cx="148" cy="93" r="6"/><circle cx="168" cy="93" r="3"/></g></g><g fill="#23463d" font-family="sans-serif" font-size="13"><text x="208" y="35">ka</text><text x="208" y="97">kha</text></g></svg><p><small>Illustrative airflow, not an anatomical or measured diagram. Close and reopen to replay. Reduced-motion settings keep it still.</small></p></details>'''
HELPER = '''# Original picture-word illustrations; match both character and keyword.
# Future changed or unmapped keywords retain the existing fallback until illustrated.
_PICTURE_FILE = os.path.join(ROOT, "data", "learning", "hindi-textbook-illustrations.json")
with open(_PICTURE_FILE, encoding="utf-8") as _picture_file:
    _PICTURES = {(r["character"], r["word"]): r["path"] for r in json.load(_picture_file)}

def letter_illustration(lt, kw, emo):
    asset = _PICTURES.get((lt, kw))
    if not asset:
        return '<i aria-hidden="true">%s</i>' % e(emo)
    return '<img class="fd-picture" src="/%s" width="240" height="180" alt="" loading="lazy" decoding="async">' % e(asset)

'''
CARD = re.compile(r'(<span class="lt" lang="hi">([^<]+)</span><span class="rm">[^<]*</span><span class="kw" lang="hi">)(?:<i aria-hidden="true">[^<]*</i>|<img class="fd-picture"[^>]*>)([^<]+)(</span>)')
ANCHOR = '<h2>What to notice</h2><ul>'
def read(p): return p.read_text(encoding='utf-8')
def once(s,a,b,where):
    if s.count(a)!=1: raise ValueError(f'{where}: expected one exact anchor; found {s.count(a)}')
    return s.replace(a,b,1)
def img(r):return '<img class="fd-picture" src="/%s" width="240" height="180" alt="" loading="lazy" decoding="async">'%html.escape(r['path'],quote=True)
def build_changes(repo):
    records={(r['character'],r['word']):r for r in RECORDS}
    if len(records)!=49:raise ValueError('Expected exactly 49 distinct illustrations')
    changes={}
    for r in RECORDS:
        asset=PACK/r['path']; tree=ET.parse(asset).getroot()
        if tree.tag!='{http://www.w3.org/2000/svg}svg':raise ValueError(asset)
        changes[r['path']]=read(asset)
    changes[MANIFEST]=json.dumps(RECORDS,ensure_ascii=False,indent=2)+'\n'
    gen=read(repo/GEN); css=read(repo/CSS)
    if 'def letter_illustration(' not in gen:
        gen=once(gen,'def vcard(dev, rom, en, mt=""):',HELPER+'\ndef vcard(dev, rom, en, mt=""):',GEN)
        gen=once(gen,'<span class="kw" lang="hi"><i aria-hidden="true">%s</i>%s</span>','<span class="kw" lang="hi">%s%s</span>',GEN)
        gen=once(gen,'e(lt), e(rm), emo, e(kw),','e(lt), e(rm), letter_illustration(lt, kw, emo), e(kw),',GEN)
        gen=once(gen,'        b.append("<h2>What to notice</h2><ul>")','        if L["slug"] == "vyanjan-1":\n            b.append('+repr(DEMO)+')\n        b.append("<h2>What to notice</h2><ul>")',GEN)
        gen=once(gen,OLD_RULE,(NEW_RULE+'\n'+ANIM_RULE).replace('%','%%'),GEN)
    elif 'fd-air-demo' not in gen or 'fd-picture' not in gen:
        raise ValueError('Partial generator install; inspect manually')
    compile(gen,GEN,'exec')
    if '.fd-letter .fd-picture{' not in css:css=once(css,OLD_RULE,NEW_RULE+'\n'+ANIM_RULE,CSS)
    elif '.fd-air-demo{' not in css:raise ValueError('Partial CSS install; inspect manually')
    changes[GEN]=gen;changes[CSS]=css
    seen=set()
    for chapter in GROUPS:
        p=f'learn/hindi/foundation/{chapter}/index.html'; s=read(repo/p)
        expected={(r['character'],r['word']) for r in RECORDS if r['chapter']==chapter}; found=set()
        def replace(m):
            key=(html.unescape(m[2]),html.unescape(m[3]))
            if key not in expected or key in found:raise ValueError(f'{p}: unexpected or repeated card {key}')
            found.add(key);return m[1]+img(records[key])+m[3]+m[4]
        s=CARD.sub(replace,s)
        if found!=expected:raise ValueError(f'{p}: missing cards {expected-found}. Current Arena layout may differ; integrate by manifest instead.')
        if chapter=='vyanjan-1' and 'class="fd-air-demo"' not in s:
            s=once(s,ANCHOR,DEMO+'\n'+ANCHOR,p)
        changes[p]=s;seen.update(found)
    if seen!=set(records):raise ValueError('Incomplete coverage')
    return changes

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('repo',type=Path);ap.add_argument('--apply',action='store_true');a=ap.parse_args(); repo=a.repo.resolve()
    try:
        changes=build_changes(repo)
        pending={p:s for p,s in changes.items() if not (repo/p).is_file() or read(repo/p)!=s}
        print(f'Preflight PASS: 49 matched cards, 49 SVGs, four chapter pages, generator compiles; {len(pending)} pending files')
        if a.apply:
            for p,s in pending.items():
                target=repo/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(s,encoding='utf-8')
            print('Applied; run the actual repository build, browser and regression checks before committing.')
        else: print('Dry-run only; no checkout files changed. Add --apply to write.')
    except (OSError,ValueError,SyntaxError,ET.ParseError) as ex:print(f'STOP: {ex}',file=sys.stderr);return 1
    return 0
if __name__=='__main__':sys.exit(main())
