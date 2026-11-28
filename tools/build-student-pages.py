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
'account/':('My learning','dashboard','<section class="sa-narrow"><p class="sa-eyebrow">YOUR ACCOUNT</p><h1 data-welcome>My learning</h1>'+NOTICE+'<div data-protected hidden><section class="sa-card"><p>Email: <span data-profile-email>—</span></p><p>Verification: <span data-profile-verified>—</span></p><p><a href="/account/verify-email/">Email verification</a></p></section></div><button class="sa-secondary" type="button" data-logout disabled>Log out</button><p><a href="/learn/hindi/">Explore free Hindi lessons</a></p></section>')}
PAGES['account/dashboard/']=('My learning','dashboard',PAGES['account/'][2])
PAGES['account/reset-password/']=('Reset password','action',PAGES['account/action/'][2])
language_selector='<div class="sa-language"><label>Interface language <select data-student-language><option value="en">English</option><option value="hi" lang="hi">हिंदी</option></select></label></div>'
for url,(title,kind,body) in list(PAGES.items()):
    PAGES[url]=(title,kind,language_selector+body)

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
