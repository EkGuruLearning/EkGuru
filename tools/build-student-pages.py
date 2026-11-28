#!/usr/bin/env python3
"""Own static noindex student page content; preserve shared generated shell."""
from pathlib import Path
import html
import importlib.util
import sys

ROOT=Path(__file__).resolve().parents[1]
START='<!-- ekguru:student-page:start -->'
END='<!-- ekguru:student-page:end -->'
CHECK='--check' in sys.argv

EMAIL='<label>Email address<input name="email" type="email" autocomplete="email" required maxlength="254"></label>'
PASSWORD='<label>Password<span class="sa-password"><input name="password" type="password" autocomplete="current-password" required minlength="6"><button type="button" data-password-toggle aria-label="Show password">Show</button></span></label>'
NOTICE='<p class="sa-status" data-status role="status" aria-live="polite">Checking availability. Free lessons remain open without an account.</p>'
NAME='<label>Full name<input name="fullName" type="text" autocomplete="name" required maxlength="100"></label>'
TERMS='<label class="sa-check"><input name="terms" type="checkbox" required> <span>I agree to the <a href="/terms/">Terms</a> and <a href="/privacy/">Privacy Policy</a>.</span></label><p class="sa-small">Account deletion is not yet available in the interface; contact us for privacy requests.</p>'
REMEMBER='<label class="sa-check"><input name="remember" type="checkbox"> <span>Remember me on this device</span></label>'

def auth_page(title, lead, fields, action, footer, google=False):
    art='register-world' if title.startswith('Start') else ('password-security' if title.startswith('Forgot') else 'login-journey')
    return (f'<div class="sa-auth-layout"><section class="sa-auth-card"><p class="sa-eyebrow">EKGURU LEARNING</p><h1>{title}</h1><p class="sa-lead">{lead}</p>{NOTICE}'
      + (f'<button class="sa-secondary" type="button" data-google disabled>{"Sign up with Google" if title.startswith("Start") else "Continue with Google"}</button><div class="sa-divider">or continue with email</div>' if google else '')
      + f'<form data-auth-form method="post" action="#">{fields}<button class="sa-primary" type="submit" disabled>{action}</button></form>'
      + f'<p class="sa-auth-footer">{footer}</p><p class="sa-small">Accounts are optional. <a href="/learn/hindi/">Explore free Hindi lessons</a>.</p></section>'
      f'<aside class="sa-auth-art"><img src="/images/lms/{art}.svg" alt="" aria-hidden="true" width="640" height="480"><div><p class="sa-eyebrow">LEARN AT YOUR PACE</p><h2>Your language journey starts here.</h2><p>Learn at your own pace with interactive lessons, bilingual explanations and personalized progress when connected.</p></div></aside></div>')

register_pw=PASSWORD.replace('current-password','new-password')+'<label>Confirm password<input name="confirm" type="password" autocomplete="new-password" required minlength="6"></label>'
PAGES={
'account/login/':('Log in','login',auth_page('Welcome back','Continue your language learning journey.',EMAIL+PASSWORD+REMEMBER+'<a href="/account/forgot-password/">Forgot password?</a>','Log in','New to EkGuru? <a href="/account/register/">Create an account</a>.',True)),
'account/register/':('Create account','register',auth_page('Start your learning journey','Create an optional student account.',NAME+EMAIL+register_pw+'<p class="sa-small">Your password must meet the Firebase project policy.</p>'+TERMS,'Create free account','Already have an account? <a href="/account/login/">Log in</a>.',True)),
'account/forgot-password/':('Reset password','forgot',auth_page('Forgot your password?','We can send a password reset link to your email.',EMAIL,'Send reset link','<a href="/account/login/">Back to login</a>')),
'account/action/':('Email action','action','<section class="sa-narrow"><p class="sa-eyebrow">ACCOUNT SECURITY</p><h1>Email verification or password reset</h1>'+NOTICE+'<div data-action-content><p>Open the secure link from your email to continue.</p></div><p><a href="/account/login/">Back to login</a></p></section>'),
'account/verify-email/':('Verify email','verify','<section class="sa-narrow"><p class="sa-eyebrow">ACCOUNT SECURITY</p><h1>Verify your email</h1>'+NOTICE+'<p>Check your inbox for a verification link. If needed, request another link.</p><p>If you just registered, your sign-in account may exist even though student setup is not connected. Do not register again; sign in later to continue.</p><button class="sa-primary" type="button" data-send-verification disabled>Send verification email</button><p><a href="/account/login/">Back to login</a></p></section>'),
'account/':('My learning','dashboard','<div class="sa-dashboard"><aside class="sa-sidebar" aria-label="Student navigation"><a href="/account/" aria-current="page">My learning</a><a href="/courses/premium/">Explore courses</a><a href="/account/settings/">Account settings</a><a href="/learn/hindi/">Free Hindi lessons</a><button type="button" data-logout disabled>Log out</button></aside><div class="sa-dashboard-content"><section class="sa-hero"><div><p class="sa-eyebrow">YOUR LEARNING SPACE</p><h1 data-welcome>My learning</h1><p>Pick up where you left off and explore what is next.</p></div><img src="/images/student-learning-illustration.webp" alt="" width="1200" height="670"></section>'+NOTICE+'<div data-protected hidden><div class="sa-grid"><section class="sa-card"><h2>Continue learning</h2><p data-dashboard-continue>Learning activity is not connected yet.</p></section><section class="sa-card"><h2>My courses</h2><p data-dashboard-courses>Your course list will appear when the learning service is available.</p></section><section class="sa-card"><h2>Learning activity</h2><p>Streaks, completed lessons, bookmarks and quiz results will appear when the learning service is connected.</p></section><section class="sa-card"><h2>Purchase history</h2><p>Purchase history is not connected yet.</p></section></div></div><section class="sa-discover"><h2>Keep learning for free</h2><p>Existing lessons do not require a student account.</p><a class="sa-secondary sa-link" href="/learn/hindi/">Explore free Hindi</a> <a class="sa-link" href="/courses/premium/">Explore future courses →</a></section></div></div>'),
'account/settings/':('Account settings','settings','<div class="sa-narrow"><p class="sa-eyebrow">YOUR ACCOUNT</p><h1>Account settings</h1>'+NOTICE+'<div data-protected hidden><section class="sa-card"><h2>Profile</h2><p>Email: <span data-profile-email>—</span></p><p>Verification: <span data-profile-verified>—</span></p><form data-profile-form method="post" action="#"><label>Display name<input name="displayName" maxlength="100" autocomplete="name"></label><button class="sa-primary" type="submit" disabled>Save name</button></form></section><section class="sa-card"><h2>Security</h2><a href="/account/forgot-password/">Reset password</a><p><a href="/account/verify-email/">Email verification</a></p><button type="button" data-logout disabled>Log out</button></section><section class="sa-card"><h2>Delete account</h2><p>Deletion is unavailable until the secure data-deletion service is connected.</p><a href="/account/delete/">Learn about deletion</a></section></div><p><a href="/account/">← My learning</a></p></div>'),
'account/delete/':('Delete account','delete','<div class="sa-narrow"><p class="sa-eyebrow">PRIVACY</p><h1>Delete your account</h1>'+NOTICE+'<section class="sa-card"><h2>Deletion is not available yet</h2><p>The deletion workflow must remove student data from the secure backend before the sign-in account is deleted. It is disabled until that backend contract is verified.</p><button class="sa-secondary" type="button" disabled>Delete account unavailable</button></section><p><a href="/account/settings/">← Account settings</a></p></div>'),
'courses/premium/':('Explore courses','catalogue','<section class="sa-catalogue"><p class="sa-eyebrow">EXPLORE EKGURU</p><h1>Find your next learning path</h1><p class="sa-lead">Free lessons are open to everyone. Premium courses, prices and access will appear only when the verified catalogue is connected.</p><div class="sa-grid"><article class="sa-card"><span class="sa-pill">FREE</span><h2>Learn Hindi</h2><p>Explore the existing Hindi lessons and practice tools without an account.</p><a class="sa-link" href="/learn/hindi/">Explore free Hindi →</a></article><article class="sa-card"><span class="sa-pill sa-pill-muted">COMING LATER</span><h2>Premium learning</h2><p>Course details, bundles, preview lessons, prices and enrolment status are not connected yet.</p><button class="sa-secondary" type="button" disabled>Checkout unavailable</button></article></div><p class="sa-small">No payment is processed here. Course access will be verified by the backend.</p></section>')}

# Keep the existing /account/ route while adding the requested dashboard URL.
old_sidebar='<aside class="sa-sidebar" aria-label="Student navigation"><a href="/account/" aria-current="page">My learning</a><a href="/courses/premium/">Explore courses</a><a href="/account/settings/">Account settings</a><a href="/learn/hindi/">Free Hindi lessons</a><button type="button" data-logout disabled>Log out</button></aside>'
new_sidebar='<aside class="sa-sidebar" aria-label="Student navigation"><a href="/account/dashboard/" aria-current="page">Overview</a><a href="/account/courses/">My Courses</a><a href="/account/progress/">Learning Progress</a><a href="/account/bookmarks/">Bookmarks</a><a href="/account/results/">Quiz Results</a><a href="/account/orders/">Orders</a><a href="/account/profile/">Profile</a><a href="/account/settings/">Settings</a><a href="/premium/courses/">Explore courses</a><button type="button" data-logout disabled>Log out</button></aside>'
t,k,b=PAGES['account/'];assert old_sidebar in b
PAGES['account/']=(t,k,b.replace(old_sidebar,new_sidebar).replace('/images/student-learning-illustration.webp','/images/lms/empty-progress.svg').replace('alt="" width="1200" height="670"','alt="" aria-hidden="true" width="640" height="480"'))
# Additional destinations remain unavailable until their reviewed API schemas exist.
PAGES['account/dashboard/']=('My learning','dashboard',PAGES['account/'][2])
PAGES['account/reset-password/']=('Reset password','action',PAGES['account/action/'][2])
PAGES['account/profile/']=('Profile','settings',PAGES['account/settings/'][2])
for slug,title,description in [
    ('courses','My courses','Your course enrolments are not connected yet.'),
    ('progress','Learning progress','Learning progress is not connected yet.'),
    ('bookmarks','Bookmarks','Bookmarks are not connected yet.'),
    ('results','Quiz results','Quiz results are not connected yet.'),
    ('orders','Orders','Order history is not connected yet.'),
    ('privacy','Account privacy','Account and data deletion requires a verified secure backend workflow.')]:
    PAGES['account/'+slug+'/']=(title,'account-section',f'<section class="sa-narrow"><p class="sa-eyebrow">YOUR LEARNING SPACE</p><h1>{title}</h1>'+NOTICE+f'<div data-protected hidden><section class="sa-card"><p>{description}</p><p><a href="/account/dashboard/">← Back to overview</a></p></section></div></section>')
course_names=[('Book 01','बाल हिंदी','Early Hindi'),('Book 02','प्रारंभिक हिंदी','Beginning Hindi'),('Book 03','मध्यम हिंदी','Intermediate Hindi'),('Book 04','उन्नत हिंदी','Advanced Hindi'),('Book 05','संपूर्ण हिंदी','Comprehensive Hindi'),('Independent pathway','Adult Hindi','Zero to Hero')]
planned=''.join(f'<article class="sa-card"><span class="sa-pill sa-pill-muted">PLANNING REFERENCE</span><h3>{number} — <span lang="hi">{hi}</span></h3><p>{en}</p><p>Availability, previews and pricing are not yet verified.</p></article>' for number,hi,en in course_names)
t,k,b=PAGES['courses/premium/'];b=b.replace('<p class="sa-small">No payment is processed here.', '<h2>Textbook pathways in development</h2><p>These titles describe curriculum planning, not courses available for purchase. The adult pathway is independent of the academic books.</p><div class="sa-grid">'+planned+'</div><p class="sa-small">No payment is processed here.')
PAGES['courses/premium/']=(t,k,b)
PAGES['premium/']=('Premium learning','catalogue',b)
PAGES['premium/courses/']=('Premium courses','catalogue',b)
PAGES['premium/reader/']=('Premium reader','reader','<section class="sa-narrow"><p class="sa-eyebrow">PREMIUM READER</p><h1>Lesson reader</h1><p class="sa-status" role="status">The secure lesson service is not connected. No restricted content is stored on this page.</p><p>Once available, lessons must be delivered by the backend after access is verified.</p><a href="/learn/hindi/">Explore free Hindi lessons</a></section>')
PAGES['premium/checkout/']=('Checkout','checkout','<section class="sa-narrow"><p class="sa-eyebrow">CHECKOUT</p><h1>Checkout unavailable</h1><p>Payments and course access are not connected. No payment can be started here.</p><button class="sa-secondary" type="button" disabled>Checkout unavailable</button><p><a href="/premium/courses/">Explore courses</a></p></section>')
mobile_nav='<nav class="sa-mobile-nav" aria-label="Student navigation"><a href="/account/dashboard/">Overview</a><a href="/account/courses/">Courses</a><a href="/account/progress/">Progress</a><a href="/account/profile/">Profile</a><details><summary>More</summary><div><a href="/account/bookmarks/">Bookmarks</a><a href="/account/results/">Quiz results</a><a href="/account/orders/">Orders</a><a href="/account/settings/">Settings and logout</a></div></details></nav>'
language_selector='<div class="sa-language"><label>Interface language <select data-student-language><option value="en">English</option><option value="hi" lang="hi">हिंदी</option></select></label></div>'
for url,(title,kind,body) in list(PAGES.items()):
    PAGES[url]=(title,kind,language_selector+body+(mobile_nav if kind in ('dashboard','account-section','settings') else ''))

def shell(url,title,kind,body):
    action=''
    if kind=='action':
        action="<script>(function(){var u=new URL(location.href),m=u.searchParams.get('mode'),c=u.searchParams.get('oobCode');if(m&&c&&c.length<2048)window.__egAction={mode:m,code:c};if(u.search||u.hash)history.replaceState(null,'',location.pathname)})();</script>"
    return f'''<!doctype html>
<html lang="en" data-ad-class="INTERACTIVE_LEARNING"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="no-referrer"><meta name="robots" content="noindex, follow"><title>{html.escape(title)} | EkGuru</title><meta name="description" content="Optional EkGuru student account and learning tools."><link rel="canonical" href="https://ekguru.shop/{url}">{action}<link rel="stylesheet" href="/css/style.min.css"><link rel="stylesheet" href="/css/tokens.css"><link rel="stylesheet" href="/css/student-account.css"><script type="module" src="/js/student/app.js"></script></head><body><header class="hdr"><a href="/">EkGuru</a><nav><a href="/learn/hindi/">Learn</a><a href="/find-tutors.html">Tutors</a></nav></header><main id="main" data-student-page="{kind}">
{START}
{body}
{END}
</main><footer class="ftr"><a href="/privacy/">Privacy</a> <a href="/contact/">Contact</a></footer></body></html>'''

def main():
    stale=[]
    sys.path.insert(0, str(ROOT/'tools'))
    spec=importlib.util.spec_from_file_location('student_ultra',ROOT/'tools/apply-ultra.py')
    ultra=importlib.util.module_from_spec(spec);spec.loader.exec_module(ultra)
    metadata=ultra.load('data/editorial/page-metadata.json',{'pages':{}})['pages']
    for url,(title,kind,body) in PAGES.items():
        path=ROOT/url/'index.html';old=path.read_text(encoding='utf8') if path.exists() else None
        if old is None:new=shell(url,title,kind,body)
        else:
            if old.count(START)!=1 or old.count(END)!=1:raise ValueError('student markers missing or duplicated: '+str(path))
            decorated='<!-- ekguru:ultra-head:start -->' in old
            base=ultra.strip(old) if decorated else old
            before,rest=base.split(START,1);_,after=rest.split(END,1);new=before+START+'\n'+body+'\n'+END+after
            if decorated:new=ultra.transform(new,path.relative_to(ROOT).as_posix(),metadata)
        if old!=new:
            stale.append(url)
            if not CHECK:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(new,encoding='utf8')
    print('Student pages:',len(PAGES),'routes;',len(stale),'stale' if CHECK else 'updated')
    return int(CHECK and bool(stale))
if __name__=='__main__':sys.exit(main())
