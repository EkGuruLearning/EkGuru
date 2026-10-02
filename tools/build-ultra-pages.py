#!/usr/bin/env python3
"""Honest trust/progress/design/review pages. All are noindex (owner rule: new pages stay noindex) and
claim nothing the evidence does not support. The shell, ad class and decorations are added by later build steps."""
import hashlib
import html
import sys
from lib.ultra_content import ROOT, load

POLICY = load('data/editorial/policy.json')
OWNER = POLICY['owner']
E = lambda x: html.escape(str(x), quote=True)


def page(title, description, route, body):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | EkGuru</title>
<meta name="description" content="{E(description)}">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://ekguru.shop{route}">
<link rel="icon" href="/images/logo.svg" type="image/svg+xml">
<meta property="og:title" content="{E(title)} | EkGuru">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="https://ekguru.shop{route}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://ekguru.shop/images/og-cover.jpg">
<link rel="stylesheet" href="/css/style.min.css">
</head>
<body>
<main id="main" class="eg-page"><p class="crumb"><a href="/">EkGuru</a> / {E(title)}</p>
<h1>{E(title)}</h1>
{body}
</main>
<script src="/js/cookie-consent.js" defer></script>
</body>
</html>
'''


def editorial():
    return f'''<p>This page says plainly how EkGuru lessons are prepared, what each trust line means, and what has <strong>not</strong> been verified. Where evidence is missing, we say “not recorded” instead of implying approval.</p>
<h2>Who runs EkGuru and who writes the pages</h2>
<p>EkGuru is run by <a href="/authors/prakash/">{E(OWNER['name'])}</a>, the founder and site maintainer in {E(OWNER['location'])}. There is no editorial team. {E(POLICY['unknown']['legacy_authorship'])} Maintaining the site does not make someone a native-speaker reviewer of every language it covers, and no teaching certificate or linguistics qualification is claimed for the maintainer.</p>
<h2>What the line under each heading means</h2>
<ul>
<li><strong>Written by</strong> names an author only when the author is actually recorded. Otherwise it says authorship is not independently recorded.</li>
<li><strong>Maintained by</strong> names who looks after the site.</li>
<li><strong>Reviewed by: not recorded</strong> means no named, verified reviewer exists for that page. It never means “probably fine”.</li>
<li><strong>Updated</strong> is shown only when the page's own text changed after the original record. It is not a rebuild timestamp; if the real date is unknown, we say so.</li>
</ul>
<h2>How a lesson becomes “reviewed”</h2>
<p>Draft → source and automatic checks → private review by a competent native speaker → the owner verifies the reviewer's competence and permission → strict release checks → an owner-authorised publication decision. A passing automatic check is never a review. <strong>No native-speaker review has been recorded for any language yet</strong>, so every language page carries a draft notice. A future review record binds a reviewer's opaque ID to the exact version of the lesson input; changing the input invalidates it. Reviewer names are public only with explicit consent.</p>
<h2>Sources and numbers</h2>
<p>A speaker count, an official-language statement or a country relationship appears only with a citable URL. A generic homepage is an imported reference, not proof that a figure was freshly verified. No source, no number.</p>
<h2>Audio and speech</h2>
<p>Browser speech is optional, starts only after a click, and is labelled <em>synthetic voice</em>. It speaks only with a voice installed for the same language; if there is none, playback is disabled and the page says so, with the romanisation still visible. A licensed human recording, if one is ever supplied, names its recorder and licence. A speech-to-text transcript is shown only when you press the microphone button and is never presented as a pronunciation score.</p>
<h2>AI assistance and originality</h2>
<p>{E(POLICY['ai_policy'])} We avoid copying textbook passages or other sites. A similarity check is a lead for an editor, not proof that a passage is original. If you believe something duplicates your work, tell us the URL and the original source.</p>
<h2>Corrections</h2>
<p>Use the <a href="/review/">corrections and review-offer form</a> or the <a href="/contact/">contact page</a> ({E(OWNER['contact'])}). A suggestion is queued for the maintainer; it is not an approval and no reply time is guaranteed. Verified corrections are made in the lesson source, not by editing a generated page by hand.</p>
<h2>Indexing and advertising</h2>
<p>{E(POLICY['owner_decisions']['indexing'])} {E(POLICY['owner_decisions']['ads'])}</p>
<h2>Your learning data</h2>
<p>Progress, review cards and streaks live in your own browser, not on an account. See <a href="/learn/progress/">your journal</a> and the <a href="/privacy/">privacy policy</a>.</p>'''


def founder():
    return f'''<p>{E(OWNER['name'])} is the founder and site maintainer of EkGuru. These facts are owner-provided and match the public About page; nothing else is claimed.</p>
<h2>Facts</h2>
<ul>
<li><strong>Role:</strong> founder and site maintainer.</li>
<li><strong>Based in:</strong> {E(OWNER['location'])}.</li>
<li><strong>Education:</strong> {E(OWNER['education'])}.</li>
<li><strong>Public profile:</strong> <a href="{E(OWNER['profile'])}" rel="noopener noreferrer">LinkedIn</a>.</li>
<li><strong>Contact:</strong> {E(OWNER['contact'])} or the <a href="/contact/">contact page</a>.</li>
</ul>
<h2>What this page does not claim</h2>
<p>{E(POLICY['unknown']['teaching_credentials'])} {E(POLICY['unknown']['native_review'])} Older lessons have no individual author log. The <a href="/editorial-policy/">editorial policy</a> explains how review status is recorded and corrected.</p>
<h2>Editorial responsibility</h2>
<p>The maintainer is responsible for how the site is built and for deciding what is published. Language accuracy depends on independent native-speaker review, which has not been recorded yet. Tutors listed on the site write their own profiles; at the moment no tutor is listed for booking, and the free lessons, practice and courses remain open.</p>'''


def progress():
    return '''<p>Your journal, review cards and streak are stored <strong>on this device only</strong>. There is no account, no tracking cookie and no paid reward. Completion is a self-report, XP and badges are activity records, and nothing here is a CEFR certificate or a pronunciation score.</p>
<div data-eg-progress><p>JavaScript is needed to show your journal. Without it, lessons, practice and every page of this site still work; only the device-only journal is unavailable.</p></div>
<h2>How your data is kept</h2>
<p>The journal lives under <code>ekguru:learning:v1</code> and each language has its own review deck. Export and import are validated JSON files of at most 2 MB, include only this journal and your review decks, and replace what is on the device after you confirm. Older path and lesson logs keep their original storage and are not erased or silently counted as new XP. A saved journal that cannot be read is preserved, not overwritten.</p>
<h2>Reminders and offline copies</h2>
<p>A study reminder is optional, asks for permission only when you press Enable, and works only while an EkGuru page is open; it is not background push. “Download this level for offline” saves a bounded list of public files; whether a voice works offline depends on your device.</p>
<p><a href="/start/">Find a starting point</a> · <a href="/learn/my-learning/">Open the existing learning tools</a> · <a href="/privacy/">Privacy details</a></p>'''


def review():
    return '''<p>Spotted a mistake, or able to review a language? Every message begins as <strong>pending</strong>. No native-speaker approval has been supplied yet. Read the <a href="/editorial-policy/">editorial policy</a> and the public <a href="https://github.com/EkGuruLearning/EkGuru/blob/main/docs/review-checklist.md" rel="noopener noreferrer">review checklist</a>. A correct-looking file, a language code or an offer to review is not approval evidence.</p>
<p>The owner verifies competence, identity, scope, sources and the exact lesson version privately. A public approved record uses an opaque reviewer ID, and a name appears only with your explicit consent. Do not include other people's private information, credentials or copyrighted textbook text.</p>
<form data-eg-review-form class="eg-journal" action="#" method="post">
<label>Type<select name="kind"><option value="correction">Content correction</option><option value="review_offer">Offer a native or editorial review</option></select></label>
<label>Language code<input name="language" required pattern="[a-z]{2,3}" maxlength="3" placeholder="hi" autocomplete="off"></label>
<label>Page URL (optional, EkGuru only)<input name="page_url" type="url" maxlength="500" placeholder="https://ekguru.shop/languages/hi/level/a1/"></label>
<label>Exact content digest (optional)<input name="content_digest" pattern="[a-f0-9]{64}" maxlength="64" autocomplete="off"></label>
<label>What should change, or what can you review?<textarea name="message" required minlength="10" maxlength="3000" rows="7"></textarea></label>
<label>Precise source URL (optional)<input name="source_url" type="url" maxlength="500"></label>
<label>Private contact email (optional; never an approval or a public record)<input name="contact_email" type="email" maxlength="254" autocomplete="email"></label>
<label><input type="checkbox" name="consent_to_publish"> I consent to a public attribution name only if a real review is later verified.</label>
<label>Public attribution name (needed only with consent)<input name="public_name" maxlength="100" disabled></label>
<label class="eg-honeypot" aria-hidden="true">Website (leave empty)<input name="website" tabindex="-1" autocomplete="off"></label>
<label><input name="agree" type="checkbox" required> This is a suggestion or review offer, not an approval, a publication permission or a guaranteed reply.</label>
<div class="eg-controls"><button type="submit">Send pending suggestion</button><button type="button" data-eg-review-export>Download suggestion JSON</button></div>
<p role="status">The private submission queue is not enabled or verified. You can download a JSON suggestion; nothing is sent or approved automatically.</p>
</form>
<noscript><p>The optional form needs JavaScript. Send a concise correction through the <a href="/contact/">contact page</a>, with the page URL and a source. Delivery must be confirmed separately and no approval is inferred.</p></noscript>
<p>If the owner enables the queue, suggestions go to a private owner-controlled spreadsheet; the public site never exposes the queue or a reviewer's identity. See the <a href="/privacy/">privacy details</a>.</p>
<script src="/js/review-form.js" defer></script>'''


def design():
    return '''<p>An internal preview of the v2 themes, learning components, script-aware type and accessible, reduced-motion-safe interactions. It is not indexed.</p>
<label>Appearance <select data-eg-theme><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option><option value="contrast">High contrast</option></select></label>
<h2>Lesson card and vocabulary row with audio</h2>
<div class="eg-demo-grid"><article class="eg-lesson-card" data-eg-reveal><span class="eg-badge">A1 · Lesson 1</span><h2>Greetings</h2><p>Say hello and introduce yourself.</p></article>
<article class="eg-lesson-card"><p lang="hi" dir="ltr">नमस्ते<button type="button" class="eg-voice" hidden data-voice-text="नमस्ते" data-voice-lang="hi" aria-label="Play नमस्ते in Hindi"></button></p><p>namaste — hello</p></article></div>
<div class="voice-settings"><p class="eg-voice-note" data-eg-voice-note="hi" lang="en"></p><div class="eg-controls"><label>Voice for Hindi<select data-eg-voice-picker="hi"></select></label><label>Speed<select data-eg-voice-rate><option value="0.6">0.6×</option><option value="0.8" selected>0.8×</option><option value="1">1×</option></select></label><button type="button" data-eg-voice-slow>Slow</button><button type="button" data-eg-voice-repeat>Repeat</button><button type="button" data-eg-voice-stop>Stop</button></div><p role="status" data-eg-voice-status></p></div>
<h2>Dialogue bubbles</h2>
<div class="eg-dialogue"><p><b>A:</b> <span lang="es">Hola, ¿cómo estás?</span></p><p><b>B:</b> <span lang="es">Muy bien, gracias.</span></p></div>
<h2>Flashcard flip</h2>
<button type="button" class="eg-flashcard" data-eg-flip aria-pressed="false"><span data-eg-front lang="hi">पानी</span><span data-eg-back hidden>water</span><small>Press to flip</small></button>
<h2>Answer states (icon + text, never colour alone)</h2>
<p class="eg-correct">✓ Correct — the answer is “water”.</p><p class="eg-wrong">✕ Not quite — try again.</p>
<h2>Level ladder and progress</h2>
<ol class="eg-ladder"><li>A1</li><li>A1+</li><li>A2</li><li>A2+</li><li>B1</li><li>B1+</li><li>B2</li><li>B2+</li><li>C1</li><li>C1+</li><li>C2</li></ol>
<div class="eg-progress-ring" role="img" aria-label="60 percent of this demonstration complete" style="--eg-progress:60"><span>60%</span></div>
<h2>Empty state, toast and celebration</h2>
<div class="eg-empty"><h3>No tutors available for booking</h3><p>Free lessons, practice and courses remain open.</p><a href="/learn/">Start learning</a></div>
<p><button type="button" data-eg-toast="Your choice was recorded on this device only.">Show a status message</button> <button type="button" data-eg-confetti>Celebrate a completed level</button></p>
<p>The celebration lasts at most 1.5 seconds, stops on click or Escape, and is disabled by reduced motion.</p>
<h2>Speaking transcript, not a score</h2>
<section data-eg-speaking data-eg-language="hi"><p>Recognition may use your browser provider's online service. Start only if you are comfortable sending microphone audio to that provider.</p><button type="button" data-eg-microphone>Start microphone</button> <button type="button" data-eg-microphone-stop disabled>Stop microphone</button><p role="status" data-eg-transcript>No microphone permission requested.</p></section>
<p><a href="/editorial-policy/">Editorial policy</a> · <a href="/learn/progress/">Learning journal</a></p>'''


PAGES = {
    'editorial-policy/index.html': ('Editorial policy', 'How EkGuru prepares, reviews and corrects lessons, labels AI-assisted drafts and synthetic speech, and records evidence. No native review is recorded yet.', editorial),
    'authors/prakash/index.html': ('Prakash — founder and maintainer', 'Owner-provided founder information and editorial responsibility. No undocumented teaching or native-review credential is claimed.', founder),
    'learn/progress/index.html': ('Your learning journal', 'Device-only learning progress, review decks, daily plan and validated JSON backup. No account and no advertising.', progress),
    'review/index.html': ('Corrections and native-review offers', 'A pending correction or review offer is not approval. Private owner verification, opaque reviewer IDs and explicit attribution consent.', review),
    'design/index.html': ('Design system v2', 'Internal preview of the v2 themes, learning components, script-aware typography and accessible reduced-motion interactions.', design),
}


def main():
    check = '--check' in sys.argv
    stale = []
    for rel, (title, desc, body) in PAGES.items():
        source = page(title, desc, '/' + rel[:-10], body())
        fp = '<!-- ekguru:ultra-page:fp:' + hashlib.sha256(source.encode()).hexdigest()[:20] + ' -->'
        path = ROOT / rel
        if check:
            if not path.exists() or fp not in path.read_text(encoding='utf-8'): stale.append(rel)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source.replace('</body>', fp + '\n</body>'), encoding='utf-8')
    print('ultra pages:', ('STALE ' + str(stale)) if stale else ('current' if check else f'{len(PAGES)} generated (noindex)'))
    return 1 if stale else 0


if __name__ == '__main__':
    raise SystemExit(main())
