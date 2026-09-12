#!/usr/bin/env python3
"""Generate copyright/index.html from the terms/ shell (identical head,
footer, analytics) with copyright-specific content. One shell, one place.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
terms = (ROOT / "terms" / "index.html").read_text(encoding="utf-8")

# --- head replacements ---
head = (terms
    .replace("Terms of Use — EkGuru Hindi Lessons | EkGuru",
             "Copyright & Content Use — EkGuru | EkGuru")
    .replace("The terms for using EkGuru: what a booking request is, what the free guides are, prices and currency, and the limits of what this site promises.",
             "How EkGuru's original content may be used, quoted and linked, and how to report unauthorised copying.")
    .replace("https://ekguru.shop/terms/", "https://ekguru.shop/copyright/")
    .replace('"name":"Terms of Use"', '"name":"Copyright & Content Use"')
    .replace('"description":"The terms for using EkGuru: what a booking request is, what the free guides are, prices and currency, and the limits of what this site promises."',
             '"description":"How EkGuru\'s original content may be used, quoted and linked, and how to report unauthorised copying."')
    .replace('"name":"Terms","item":"https://ekguru.shop/terms/"',
             '"name":"Copyright","item":"https://ekguru.shop/copyright/"'))

# --- body content replacement ---
body = '''<p class="crumb"><a href="../">EkGuru</a> › Copyright</p>
<div class="legal">
<h1>Copyright &amp; Content Use</h1>
<p class="upd">Last updated 11 September 2026 · Applies to original material on
<a href="https://ekguru.shop/">https://ekguru.shop/</a>.</p>

<p class="lede">Short version: the lessons, tools, guides and explanations on this
site are original and written by hand. You are welcome to link to them and to
quote a reasonable extract with attribution. You may not republish them wholesale.</p>

<h2>What is original here</h2>
<p>Unless a page says otherwise, the following are original EkGuru content:</p>
<ul>
  <li>the Hindi lessons, guides and explanations</li>
  <li>the daily-practice series and question-and-answer pages</li>
  <li>the interactive tools and their example sentences</li>
  <li>the practice and quiz banks</li>
  <li>the tutor-marketplace editorial copy and page structure</li>
</ul>

<h2>What we do <b>not</b> claim</h2>
<ul>
  <li>public-domain facts about the Hindi language (a grammar rule is not owned by anyone)</li>
  <li>common, everyday words and phrases in Hindi or English</li>
  <li>third-party content, including tutor photographs and the tutors' own
  introductions, which belong to the tutors</li>
  <li>content published by users through the contact or booking forms</li>
</ul>

<h2>How you may use the material</h2>
<ul>
  <li><b>Link freely.</b> You do not need permission to link to any page.</li>
  <li><b>Quote briefly</b> with attribution to EkGuru and a link back.</li>
  <li><b>Personal study use</b> — print or save a copy for yourself.</li>
</ul>
<p>You may <b>not</b> republish pages or large extracts, scrape the site to
rebuild it elsewhere, sell the material, or present it as your own.</p>

<h2>Reporting copied content</h2>
<p>If you believe a page on this site reproduces your work without
permission, tell us the original URL and the EkGuru page, and it will be
reviewed promptly. The same goes the other way: if you find EkGuru content
reproduced elsewhere without attribution, we would like to hear about it.</p>
<p>Write to us at
<a data-s="email" href="mailto:EkGuruLearning@gmail.com">EkGuruLearning@gmail.com</a>
or use the <a href="../contact/?topic=Copyright">contact form</a>.</p>

<h2>How we protect original work</h2>
<p>We keep a fingerprint and version record of our original pages, monitor for
substantial copying, and keep evidence for genuine infringement cases. We do not
block copying, right-click or text selection — those harm real users and stop
nobody. Attribution and evidence are more useful than barriers.</p>

<div class="note">
  <b>Not sure if a use is allowed?</b>
  <p>Ask us — a quick email is cheaper than a dispute.
  <a href="../contact/?topic=Copyright">Contact us</a>.</p>
</div>
</div>
</div>
'''

# replace from '<p class="crumb">' to the first '</div>\n</div>' before the footer comment
start = head.index('<p class="crumb">')
end = head.index('</div>\n</div>\n<!-- =========================================================')
out = head[:start] + body + head[end + len('</div>\n</div>\n'):]

(ROOT / "copyright").mkdir(exist_ok=True)
(ROOT / "copyright" / "index.html").write_text(out, encoding="utf-8")
print("wrote copyright/index.html", len(out), "bytes")
