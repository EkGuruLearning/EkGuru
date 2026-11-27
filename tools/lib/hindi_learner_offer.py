"""Shared, non-promissory free-learning / independent-Hindi-tutoring next step."""
from html import escape


def hindi_learner_offer(heading_id, tutor_href, free_href):
    return f'''<section data-eg-hindi-help aria-labelledby="{escape(heading_id, quote=True)}">
<h2 id="{escape(heading_id, quote=True)}">Want help speaking Hindi?</h2>
<p>The self-paced materials are free. Independent Hindi tutoring is optional and separate from the free courses; tutor lessons are not included.</p>
<p>A tutor can help you practise a conversation, ask questions about pronunciation, or work on a specific goal. EkGuru's tutor directory is for Hindi, not a promise of teachers for every language in the library.</p>
<ol>
<li><strong>Choose a goal:</strong> first conversations, travel Hindi, reading, or speaking practice.</li>
<li><strong>Compare profiles:</strong> check the tutor's teaching approach, displayed lesson price and current availability. Profile details are tutor-provided, not a guarantee of qualifications or results.</li>
<li><strong>Ask before paying:</strong> share your level, goal, timezone and two suitable times. Confirm the lesson price and time directly with the tutor; a request is not a confirmed booking. EkGuru does not collect tutor-lesson payments in this release.</li>
</ol>
<p><a class="btn btn-primary" href="{escape(tutor_href, quote=True)}" data-goatcounter-click="hindi_help_tutor_directory">Compare Hindi tutor profiles</a></p>
<p>If no suitable tutor is listed, you can <a href="{escape(free_href, quote=True)}">continue learning Hindi for free</a>. No booking or account is needed to use the self-paced materials.</p>
</section>'''
