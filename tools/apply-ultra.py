#!/usr/bin/env python3
"""Additive, idempotent and strip-invertible site features. Everything it adds sits between
<!-- ekguru:ultra-NAME:start/end --> markers (plus one data-learning-language attribute on <html>), so
`--strip` restores the exact pre-decoration page. It never edits robots, canonicals, titles, existing text,
the ad loader or an existing generator's output. Modes: (default) apply · --strip · --check."""
import html
import json
import re
import sys
from lib.ultra_content import ROOT, load, pages, route

SLOTS = ['head', 'assets', 'byline', 'notice', 'audio', 'continue', 'today', 'placement', 'lesson', 'privacy', 'appearance']
SLUG_CODE = {'hindi': 'hi', 'bengali': 'bn', 'gujarati': 'gu', 'kannada': 'kn', 'malayalam': 'ml', 'marathi': 'mr', 'punjabi': 'pa', 'tamil': 'ta', 'telugu': 'te', 'urdu': 'ur'}
# Long-form world-course guides live under readable slugs rather than codes.
# Keep them out of SLUG_CODE so they are not mistaken for generated course hubs.
WORLD_GUIDE_CODES = {'arabic': 'ar', 'spanish': 'es', 'german': 'de'}
LOCALES = ['ar', 'de', 'es', 'fr', 'ja', 'pt']
REGISTRY = {r['code']: r for r in load('data/languages/registry.json', {'languages': []})['languages']}
AVAILABLE = {l['code'] for l in load('data/learning/index.json', {'languages': []})['languages']}
LEVEL_PAGES = set(load('data/learning/offline-levels.json', {'levels': {}})['levels'])
UTILITY = re.compile(r'^/(?:privacy|terms|disclaimer|copyright|cookie-policy|monetization-disclosure|contact|search|offline|tutor|join|support|booking|checkout|payment|admin|404|find-tutors|courses|start|editorial-policy|authors|review|design)(?:[/.]|$)')
NEW_PAGES = {'editorial-policy/index.html', 'authors/prakash/index.html', 'learn/progress/index.html', 'review/index.html', 'design/index.html'}
AI_DRAFT_PREFIXES = ('learn/arabic/', 'learn/spanish/', 'learn/german/')
UI = {  # appearance control + byline labels per UI locale (policy/review pages stay English and are linked with hreflang)
    'en': {'appearance': 'Settings', 'appearance': 'Appearance', 'opts': ['System', 'Light', 'Dark', 'High contrast'], 'policy': 'Editorial policy', 'journal': 'Learning journal', 'written': 'Written by: authorship not independently recorded', 'maintained': 'Maintained by', 'reviewed': 'Reviewed by: not recorded', 'updated': 'Updated: ', 'unknown': 'legacy editorial date unknown', 'corrections': 'Editorial policy and corrections'},
    'ar': {'appearance': 'الإعدادات', 'appearance': 'المظهر', 'opts': ['النظام', 'فاتح', 'داكن', 'تباين عالٍ'], 'policy': 'سياسة التحرير (بالإنجليزية)', 'journal': 'سجل التعلم (بالإنجليزية)', 'written': 'التأليف: لم يوثّق بشكل مستقل', 'maintained': 'صيانة الموقع:', 'reviewed': 'المراجعة: لا يوجد سجل', 'updated': 'التحديث: ', 'unknown': 'تاريخ التحرير القديم غير معروف', 'corrections': 'سياسة التحرير والتصحيحات (بالإنجليزية)'},
    'de': {'appearance': 'Einstellungen', 'appearance': 'Darstellung', 'opts': ['System', 'Hell', 'Dunkel', 'Hoher Kontrast'], 'policy': 'Redaktionsrichtlinie (Englisch)', 'journal': 'Lernjournal (Englisch)', 'written': 'Autorenschaft: nicht unabhängig dokumentiert', 'maintained': 'Website gepflegt von', 'reviewed': 'Prüfung: nicht dokumentiert', 'updated': 'Aktualisiert: ', 'unknown': 'früheres redaktionelles Datum unbekannt', 'corrections': 'Redaktionsrichtlinie und Korrekturen (Englisch)'},
    'es': {'appearance': 'Ajustes', 'appearance': 'Apariencia', 'opts': ['Sistema', 'Claro', 'Oscuro', 'Alto contraste'], 'policy': 'Política editorial (en inglés)', 'journal': 'Diario de aprendizaje (en inglés)', 'written': 'Autoría: no documentada de forma independiente', 'maintained': 'Sitio mantenido por', 'reviewed': 'Revisión: no registrada', 'updated': 'Actualizado: ', 'unknown': 'fecha editorial anterior desconocida', 'corrections': 'Política editorial y correcciones (en inglés)'},
    'fr': {'appearance': 'Paramètres', 'appearance': 'Apparence', 'opts': ['Système', 'Clair', 'Sombre', 'Contraste élevé'], 'policy': 'Politique éditoriale (en anglais)', 'journal': 'Journal d’apprentissage (en anglais)', 'written': 'Auteur : non documenté indépendamment', 'maintained': 'Site maintenu par', 'reviewed': 'Révision : non enregistrée', 'updated': 'Mise à jour : ', 'unknown': 'ancienne date éditoriale inconnue', 'corrections': 'Politique éditoriale et corrections (en anglais)'},
    'ja': {'appearance': '設定', 'appearance': '表示', 'opts': ['システム', 'ライト', 'ダーク', '高コントラスト'], 'policy': '編集方針（英語）', 'journal': '学習記録（英語）', 'written': '執筆者：独立した確認記録はありません', 'maintained': 'サイト管理：', 'reviewed': '校閲：記録なし', 'updated': '更新：', 'unknown': '以前の編集日は不明です', 'corrections': '編集方針と訂正（英語）'},
    'pt': {'appearance': 'Definições', 'appearance': 'Aparência', 'opts': ['Sistema', 'Claro', 'Escuro', 'Alto contraste'], 'policy': 'Política editorial (em inglês)', 'journal': 'Diário de aprendizagem (em inglês)', 'written': 'Autoria: não documentada de forma independente', 'maintained': 'Site mantido por', 'reviewed': 'Revisão: não registada', 'updated': 'Atualizado: ', 'unknown': 'data editorial anterior desconhecida', 'corrections': 'Política editorial e correções (em inglês)'},
}
INIT = "(function(){var t;try{t=localStorage.getItem('ekguru:theme:v2')}catch(e){}if(['light','dark','contrast'].indexOf(t)<0)t=typeof matchMedia==='function'&&matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;document.documentElement.classList.add('eg-js')})()"
PRIVACY = '''<section class="eg-learning-privacy" data-eg-chrome="privacy"><h2 id="device-learning-and-optional-services">Device learning, voice and optional services</h2>
<p>The learning journal and the per-language review decks use local storage on this device and origin, not a learning account. Older path and lesson logs keep their keys. JSON export and import is an explicit, validated, learning-only replacement bounded to 2 MB; it excludes booking, payment, contact and consent storage. An export file can still contain words you added yourself, so keep your files private.</p>
<p>Study activity, self-reported completion, review ratings and approximate active time are local records, not a fluency or pronunciation certificate. A saved journal or deck that cannot be read is preserved rather than overwritten. Browser storage and cache APIs are not transactional: failed saves and downloads never claim completion, and a rollback is attempted. Offline files can be evicted by the browser. Clearing the worker's snapshots does not erase local study records or the browser's own HTTP cache.</p>
<p>Device speech is optional and starts only after a click, and only with a voice installed for the same language. Browser or operating-system voices and microphone recognition may use the browser provider's online processing. The microphone is never started on page load; recognition shows a transcript, never a pronunciation score, and EkGuru does not post it anywhere. A licence and recorder are shown for any supplied human recording.</p>
<p>Local notifications need your explicit Enable action and device permission. The reminder works only while EkGuru is open; it is not background Web Push and creates no subscription. You can disable it in one action.</p>
<p>The correction and review-offer form is separate from learning backups. Its queue is disabled until the owner verifies one. If it is enabled and you press send, what you typed goes to a private owner-controlled spreadsheet; names are never public without attribution consent and a real review, and a suggestion is never an approval. A cross-origin request does not prove delivery.</p>
<p>Fonts are system fonts; no font CDN is used. Other third-party services described elsewhere in this policy are not made anonymous by the local journal. <a href="/editorial-policy/" hreflang="en">Editorial evidence policy</a> · <a href="/learn/progress/" hreflang="en">Learning tools and controls</a></p></section>'''
E = lambda x: html.escape(str(x), quote=True)


def block(name, body):
    return f'<!-- ekguru:ultra-{name}:start -->\n{body}\n<!-- ekguru:ultra-{name}:end -->\n'


STRIP = re.compile(r'<!-- ekguru:ultra-(?:' + '|'.join(SLOTS) + r'):start -->\n[\s\S]*?<!-- ekguru:ultra-(?:' + '|'.join(SLOTS) + r'):end -->\n')


def strip(raw):
    raw = STRIP.sub('', raw)
    return re.sub(r'(<html\b[^>]*?) data-learning-language="[^"]*"', r'\1', raw, count=1, flags=re.I)


def learning_code(rel):
    parts = rel.split('/')
    if parts[0] == 'languages' and len(parts) > 2 and parts[1] in REGISTRY: return parts[1]
    if parts[0] == 'learn' and len(parts) > 2 and parts[1] in SLUG_CODE: return SLUG_CODE[parts[1]]
    if parts[0] == 'learn' and len(parts) > 2 and parts[1] in WORLD_GUIDE_CODES: return WORLD_GUIDE_CODES[parts[1]]
    if parts[0] in SLUG_CODE and len(parts) > 1: return SLUG_CODE[parts[0]]
    return 'hi'


def is_course_page(rel):
    parts = rel.split('/')
    return (parts[0] == 'languages' and len(parts) > 2 and parts[1] in REGISTRY) or (parts[0] == 'learn' and len(parts) > 2 and parts[1] in SLUG_CODE)


def review_pending(code):
    return REGISTRY.get(code, {}).get('review', {}).get('status') != 'reviewed'


def head_block(raw, rel, code):
    voice = any(m in raw for m in ('storybook.js', 'hindi-audio.js', 'data-voice-text', 'data-sb-say', 'data-say=', 'course-player.js', 'practice-engine.js', 'data-eg-speaking'))
    learning = bool(re.match(r'^(?:index\.html|(?:learn|languages|courses|start|daily-hindi|toolbox|hindi)/)', rel)) or 'hindi-srs.js' in raw
    scripts = ['<script>' + INIT + '</script>']
    if learning and 'hindi-srs.js' in raw: scripts.append('<script src="/js/global-srs.js"></script>')  # the compat deck needs it before the page's own scripts
    for name, wanted in (('voice-languages.js', voice), ('voice.js', voice), ('speech-ui.js', 'data-eg-speaking' in raw), ('ui-motion.js', True),
                         ('global-srs.js', learning and 'hindi-srs.js' not in raw), ('retention.js', learning)):
        if wanted: scripts.append(f'<script src="/js/{name}" defer></script>')
    return block('head', '\n'.join(scripts))


def assets_block(rel, code, learning):
    links = ['<link rel="stylesheet" href="/css/tokens.css">', '<link rel="stylesheet" href="/css/ultra.css">']
    if learning and (ROOT / f'css/themes/{code}.css').exists(): links.append(f'<link rel="stylesheet" href="/css/themes/{code}.css">')
    return block('assets', '\n'.join(links))


def byline_block(rel, code, metadata, locale):
    u = UI[locale]
    meta = metadata.get(rel, {})
    date = f'<time datetime="{meta["updated"]}">{meta["updated"]}</time>' if meta.get('updated') else E(u['unknown'])
    is_ai_draft = rel in NEW_PAGES or rel.startswith(AI_DRAFT_PREFIXES)
    author = 'Written by: AI-assisted draft for owner review' if is_ai_draft else u['written']
    rtl = ' dir="rtl"' if locale == 'ar' else ' dir="ltr"'
    return block('byline', f'<p class="eg-byline" lang="{locale}"{rtl} data-eg-chrome="editorial">{E(author)}. {E(u["maintained"])} <a href="/authors/prakash/" hreflang="en">Prakash</a>. {E(u["reviewed"])}. {E(u["updated"])}{date}. <a href="/editorial-policy/" hreflang="en">{E(u["corrections"])}</a>.</p>')


def notice_block(code):
    return block('notice', '<p class="eg-review-notice" lang="en" dir="ltr" data-eg-chrome="review">Draft: not yet reviewed by a native speaker. Existing availability and indexing are preserved by owner instruction; that is not an editorial approval. <a href="/review/">Suggest a correction</a>.</p>')


def audio_block(code):
    return block('audio', f'<p class="eg-voice-note" data-eg-voice-note="{code}" lang="en" dir="ltr" data-eg-chrome="audio" aria-live="polite"></p>')


def appearance_block(locale):
    u = UI[locale]
    opts = ''.join(f'<option value="{v}">{E(t)}</option>' for v, t in zip(('system', 'light', 'dark', 'contrast'), u['opts']))
    rtl = 'rtl' if locale == 'ar' else 'ltr'
    return block('appearance', f'<section class="eg-appearance" lang="{locale}" dir="{rtl}" data-eg-chrome="appearance"><label>{E(u["appearance"])} <select data-eg-theme>{opts}</select></label> · <a href="/editorial-policy/" hreflang="en">{E(u["policy"])}</a> · <a href="/learn/progress/" hreflang="en">{E(u["journal"])}</a></section>')


def hub_blocks(code):
    # Usability 18 (3 Oct 2026): the journal strip was one bare link
    # ("Learning journal and continue links on this device") with no heading
    # and no explanation, so on a first visit it read as an orphan button in
    # the middle of the page. It is now a labelled panel: what it is, what is
    # stored where, and the one thing you can do. js/retention.js replaces
    # the body with "Continue where you left off" once this device has
    # progress — the fallback below is what everyone else reads.
    return (block('continue', f'<section class="eg-continue" data-eg-continue data-eg-language="{code}" data-eg-chrome="continue"><h2 class="eg-continue-h">Your learning journal</h2><p>Lessons you mark complete, cards you review and any streak are saved in this browser only — nothing is uploaded, and there is no account to create.</p><a class="eg-continue-go" href="/learn/progress/">Open the journal</a></section>') +
            block('today', f'<section class="eg-today" data-eg-today data-eg-language="{code}" data-eg-chrome="plan"><h2>Today: one small learning step</h2><p>Read one lesson, review up to ten due cards, and listen once if your device has a matching voice. <a href="/learn/progress/">Open your device-only journal</a>.</p></section>'))


def lesson_block(code, level, url):
    return block('lesson', f'<section class="eg-lesson-controls" data-eg-chrome="learning-controls" data-eg-lesson-page data-eg-language="{code}" data-eg-level="{level}"><h2>Your device-only learning tools</h2><button type="button" hidden data-eg-complete="{url}" data-eg-level="{level}">Mark this level reading complete</button> <button type="button" hidden data-eg-download-level="{url}">Download this level for offline</button><p role="status">Optional JavaScript tools. Completion is a self-report, not a proficiency certificate. Only a bounded same-origin file list is downloaded; audio may need an installed voice.</p><a href="/learn/progress/">Review and export your journal</a></section>')


def transform(raw, rel, metadata):
    if rel == 'admin.html': return raw
    raw = strip(raw)
    parts = rel.split('/')
    locale = parts[0] if parts[0] in LOCALES else 'en'
    code = learning_code(rel); url = route(rel)
    learning = bool(re.match(r'^(?:index\.html|(?:learn|languages|courses|start|daily-hindi|toolbox|hindi)/)', rel)) or 'hindi-srs.js' in raw
    raw = re.sub(r'<html\b', f'<html data-learning-language="{code}"', raw, count=1, flags=re.I)
    m = re.search(r'<head\b[^>]*>', raw, re.I)
    if m: raw = raw[:m.end()] + head_block(raw, rel, code) + raw[m.end():]
    if '</head>' in raw: raw = raw.replace('</head>', assets_block(rel, code, learning) + '</head>', 1)
    h1 = re.search(r'</h1>', raw)
    home = rel == 'index.html' or bool(re.match(r'^(?:ar|de|es|fr|ja|pt)/index\.html$', rel))  # hero pages keep the footer links only
    if h1 and not home and (rel in NEW_PAGES or not UTILITY.match(url)):
        text = byline_block(rel, code, metadata, locale)
        if is_course_page(rel) and review_pending(code) and locale == 'en': text += notice_block(code)
        if re.search(r'storybook\.js|data-voice-text|data-sb-say|data-say=|course-player\.js|hindi-audio\.js', raw) and locale == 'en': text += audio_block(code)
        raw = raw[:h1.end()] + text + raw[h1.end():]
    extra = ''
    hub = (rel == 'index.html' and True) or (parts[0] == 'languages' and len(parts) == 3 and parts[2] == 'index.html' and parts[1] in AVAILABLE) or (parts[0] == 'learn' and len(parts) == 3 and parts[2] == 'index.html' and SLUG_CODE.get(parts[1]) in AVAILABLE)
    if hub and locale == 'en': extra += hub_blocks(code)
    if url in LEVEL_PAGES: extra += lesson_block(code, parts[3].upper(), url)
    if rel == 'start/index.html': extra += block('placement', '<section class="eg-journal" data-eg-placement data-eg-chrome="placement"><h2>Optional adaptive starting-point check</h2><p>With JavaScript you can take 5–10 recognition questions in a language with available levels. It suggests a starting lesson, not a certified CEFR level. The manual learning paths remain available.</p></section>')
    if rel == 'privacy/index.html': extra += block('privacy', PRIVACY)
    if extra:
        anchor = raw.find('<!-- ekguru:pw-bands:start -->')
        end = raw.rfind('</main>')
        pos = anchor if anchor >= 0 and (end < 0 or anchor < end) else end
        if pos >= 0: raw = raw[:pos] + extra + raw[pos:]
    foot = raw.find('<!-- ekguru:shell-footer:start -->')
    pos = foot if foot >= 0 else raw.rfind('</body>')
    if pos >= 0: raw = raw[:pos] + appearance_block(locale) + raw[pos:]
    return raw


def main():
    mode = 'strip' if '--strip' in sys.argv else 'check' if '--check' in sys.argv else 'apply'
    metadata = load('data/editorial/page-metadata.json', {'pages': {}})['pages']
    changed = []
    for p in pages():
        rel = p.relative_to(ROOT).as_posix(); raw = p.read_text(encoding='utf-8')
        out = strip(raw) if mode == 'strip' and rel != 'admin.html' else transform(raw, rel, metadata)
        if out != raw:
            changed.append(rel)
            if mode != 'check': p.write_text(out, encoding='utf-8')
    verb = {'strip': 'stripped', 'apply': 'decorated', 'check': 'stale'}[mode]
    print(f'ultra integration: {len(changed)} pages {verb}' + (' (existing indexing/canonicals untouched)' if mode == 'apply' else ''))
    for rel in changed[:12] if mode == 'check' else []: print('STALE', rel)
    return 1 if mode == 'check' and changed else 0


if __name__ == '__main__':
    raise SystemExit(main())
