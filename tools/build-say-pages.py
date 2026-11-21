#!/usr/bin/env python3
"""Generate 'how to say X in Hindi' Q&A pages for high-volume search queries.

WHY THIS EXISTS
---------------
The site already has ~15 'how to say X in Hindi' pages and they are among
the highest-CTR pages in the inventory: the query IS the page, the answer
sits in the first line, and Google's featured-snippet format matches the
structure exactly. But dozens of common phrase searches have no page —
so those queries get impressions from adjacent pages (the hub, or a
page about something else) and zero clicks.

This generator adds the missing high-volume phrases. Each page is
structurally identical to the existing ask/ pages: same shell, same
schema (QAPage + FAQPage + BreadcrumbList), same answer-first layout,
same cross-section links. The content is authored, not templated —
each phrase has its own genuine answer with the nuance a native speaker
would give.

  python3 tools/build-say-pages.py
  python3 tools/build-say-pages.py --check
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Each entry: (slug, question, answer_html, table_rows, extra_sections, faq_pairs)
# table_rows: list of (situation, say_html)
# extra_sections: list of (heading, body_html)
# faq_pairs: list of (question, answer_text)

PAGES = [
    {
        "slug": "how-to-say-good-night-in-hindi",
        "question": "How do you say good night in Hindi?",
        "answer": (
            "<strong>शुभ रात्रि</strong> <em>(shubh raatri)</em> is the "
            "direct translation and the one you will see in writing. In "
            "speech, <strong>नाيت्‌</strong> <em>(naite)</em> — borrowed "
            "from English — or simply saying it in English is far more "
            "common among younger speakers."
        ),
        "table": [
            ("Written, formal, a message", "शुभ रात्रि <em>shubh raatri</em>"),
            ("Among friends and family", '"good night" in English, or <em>naite</em>'),
            ("To someone you are close to", "रात värd <em>raat bhar</em> — sleep well all night"),
        ],
        "sections": [
            (
                "When people actually say it",
                "<p>In a WhatsApp message to a friend, <em>shubh raatri</em> is fine "
                "and warm. In person, especially between younger people, you will hear "
                "English far more often. Nobody will correct you for either — the "
                "language borrows freely and both are completely natural.</p>"
            ),
            (
                "The difference from good evening",
                "<p>Good evening is <strong>शुभ संध्या</strong> <em>(shubh sandhya)</em>, "
                "but like <em>suprabhaat</em> it is written far more than spoken. "
                "<strong>Namaste</strong> covers both evening and night greetings in "
                "conversation, which is the single most useful thing to know as a "
                "beginner.</p>"
            ),
        ],
        "faq": [
            ("Is shubh raatri the only way to say good night?",
             "No. Shubh raatri is the formal, written form. In speech, people say good night in English, or use naite, which is Hindi's phonetic spelling of the English word."),
            ("Can I use namaste at night?",
             "Yes. Namaste works at any time of day and is never wrong, including at night. It is the safest greeting for a beginner."),
            ("How do you say sleep well in Hindi?",
             "Khoon khaanchho (खोon khaao) in casual speech means sleep well, or khaancho achhaa (खानो | अच्छा) — but the most natural is simply a good night wish: शुभ रात्रि."),
            ("Is there a difference between good night and good night in Hindi?",
             "No — good night translates directly as shubh raatri. There is no separate cultural form that doesn't map onto the English phrase."),
        ],
    },
    {
        "slug": "how-to-say-excuse-me-in-hindi",
        "question": "How do you say excuse me in Hindi?",
        "answer": (
            "The word that covers almost every situation is "
            "<strong>क्षमा करें</strong> <em>(kshamaa karein)</em> — literally "
            "\"do forgive me.\" For getting someone's attention, "
            "<strong>क्यों</strong> <em>(kyoN)</em> — a short, rising "
            "\"why?\" used as a polite attention-getter — is what you will "
            "hear most."
        ),
        "table": [
            ("To get someone's attention (store, street)", "क्यों <em>kyoN</em>"),
            ("To apologise for bumping into someone", "क्षमा करें <em>kshamaa karein</em>"),
            ("To ask to pass by someone", "क्षमा करें, मैं өтना चाहता हूँ <em>kshamaa karein, main ootanaa chaahata hoon</em>"),
            ("To interrupt a conversation", "क्षमा करें <em>kshamaa karein</em>"),
        ],
        "sections": [
            (
                "KyoN — the everyday attention-getter",
                "<p><em>KyoN</em> literally means \"why,\" but when said with a rising "
                "tone and a polite expression it means \"excuse me\" in the sense of "
                "\"may I have your attention.\" You will hear it constantly in shops, "
                "on buses, and on the street. It is informal but never rude.</p>"
            ),
            (
                "Kshamaa karein — the formal apology",
                "<p><em>Kshamaa karein</em> is the polite, safe choice for any situation "
                "where you might be at fault — bumping into someone, interrupting, "
                "asking to correct a mistake. It is more formal than <em>maaf karo</em>, "
                "which is the casual version you hear between friends.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between kshamaa karein and maaf karo?",
             "Kshamaa karein is polite and formal — the safe choice with strangers, elders, or in any situation where you want to be respectful. Maaf karo is casual, used between friends and family."),
            ("Can I just say kyoN to a stranger?",
             "Yes. KyoN with a polite expression is the most common way to get a stranger's attention in India. It is informal but universally understood and never considered rude."),
            ("How do you say I am sorry in Hindi?",
             "The everyday phrase is माफ़ करें (maaf karein) for polite speech or माफ़ कर (maaf kar) between friends. See the how to say sorry in Hindi page for the full nuance."),
            ("How do you say pardon me in Hindi?",
             "You can use क्षमा करें (kshamaa karein) for a polite pardon, or simply say kyoN with a questioning tone. For not hearing someone, kshamaa karein is the safest choice."),
        ],
    },
    {
        "slug": "how-to-say-no-problem-in-hindi",
        "question": "How do you say no problem in Hindi?",
        "answer": (
            "<strong>कोई बात नहीं</strong> <em>(koi baat nahin)</em> is the "
            "direct, all-purpose translation — \"no matter, no issue.\" "
            "<strong> تەبرىك</strong> <em>(koi zaroorat nahin)</em> means "
            "\"no need\" and works when someone is thanking you or apologising."
        ),
        "table": [
            ("After someone thanks you", "कोई बात नहीं <em>koi baat nahin</em>"),
            ("After someone apologises", "कोई बात नहीं <em>koi baat nahin</em>, या कोई ज़रूरत नहीं <em>koi zaroorat nahin</em>"),
            ("To say it is not a problem at all", "कुछ भी नहीं <em>kuch bhi nahin</em>"),
            ("Very casual, between friends", "कोई बात नहीं, bhai <em>koi baat nahin</em>"),
        ],
        "sections": [
            (
                "Koi baat nahin — the default",
                "<p>This is the phrase you will hear in almost every situation where "
                "English says \"no problem.\" It literally means \"there is no talk, no "
                "matter\" and it is used after thanks, after apologies, and when "
                "agreeing to do something someone asks. It is neutral in register — "
                "fine with strangers and with friends.</p>"
            ),
            (
                "Kuch bhi nahin — a touch more emphasis",
                "<p><em>Kuch bhi nahin</em> means \"not anything\" and carries slightly "
                "more warmth or emphasis. It is a natural alternative when you want to "
                "say \"it's really no problem at all.\"</p>"
            ),
        ],
        "faq": [
            ("What is the difference between koi baat nahin and koi zaroorat nahin?",
             "Koi baat nahin means 'no matter, no issue' and is the general all-purpose phrase. Koi zaroorat nahin means 'no need' and is used specifically when someone is thanking you or apologising — it reassures them that their action was not a burden."),
            ("Can I say 'no problem' in English in India?",
             "Yes, absolutely. English is widely understood in urban India and 'no problem' is a completely natural response in many contexts, especially with younger speakers."),
            ("How do you say it's okay in Hindi?",
             "The common phrase is ठीक है (thiik hai), which means 'it is fine/OK.' It is a near-universal response to an apology, a request, or a thank you."),
            ("What is the Hindi for don't worry?",
             " चिंतन नहीं (chintaa nahin) means 'do not worry,' or you can say कोई बात नहीं (koi baat nahin) to reassure someone that something is not a problem."),
        ],
    },
    {
        "slug": "how-to-say-i-need-help-in-hindi",
        "question": "How do you say I need help in Hindi?",
        "answer": (
            "<strong>मुझे मदद चाहिए</strong> <em>(mujhe maadad chaahiye)</em> "
            "is the direct translation. For a more urgent or emergency situation, "
            "<strong>मदद कीजिए</strong> <em>(maadad kiijiye)</em> — "
            "\"please help\" — is more natural and gets attention faster."
        ),
        "table": [
            ("Asking calmly for assistance", "मुझे मदद चाहिए <em>mujhe maadad chaahiye</em>"),
            ("More urgent, asking for help right now", "मदद कीजिए <em>maadad kiijiye</em>"),
            ("To a stranger you are asking for directions", "कृपया मदद करे <em>krupayaa maadad kare</em>"),
            ("I can help you", "मैं मदद कर सकता हूँ <em>main maadad kar saktaa hoon</em>"),
        ],
        "sections": [
            (
                "Mujhe maadad chaahiye — the standard form",
                "<p>This is the most straightforward way to ask for help. "
                "<em>Mujhe</em> means \"to me,\" <em>maadad</em> is \"help,\" and "
                "<em>chaahiye</em> means \"is needed/wanted.\" Together: \"to me "
                "help is needed.\" It is polite, clear, and understood everywhere.</p>"
            ),
            (
                "Maadad kiijiye — when you need it now",
                "<p>When you are in a situation that needs immediate help — a "
                "crowded place, a confusing situation, someone who looks lost — "
                "<em>maadad kiijiye</em> is the form to use. The <em>-iye</em> ending "
                "is the polite imperative, so it means \"please help (you).\"</p>"
            ),
        ],
        "faq": [
            ("What is the difference between mujhe maadad chaahiye and maadad kiijiye?",
             "Mujhe maadad chaahiye means 'I need help' — a statement of need. Maadad kiijiye means 'please help' — a direct request, more urgent and more direct."),
            ("How do you say please help me in Hindi?",
             "The most natural urgent form is मदद कीजिए (maadad kiijiye). For extra politeness, add कृपया (krupayaa): कृपया मदद कीजिए."),
            ("How do you say can you help me in Hindi?",
             "क्या आप मेरी मदद कर सकते हैं (kyaa aap merii maadad kar sakte hain) is the direct 'can you help me.' In casual speech, the shorterԿարող (karo) form works among friends."),
            ("What is the Hindi for help me?",
             "The urgent form is मदद कीजिए (maadad kiijiye) — 'help, please.' For an emergency, shouting maadad! (help!) is what people will respond to."),
        ],
    },
    {
        "slug": "how-to-say-how-much-in-hindi",
        "question": "How do you say how much in Hindi?",
        "answer": (
            "<strong>कितने</strong> <em>(kitne)</em> for counting things and "
            "<strong>क्या</strong> <em>(kyaa)</em> for asking the price. For "
            "price specifically, <strong>कितना है</strong> <em>(kitanaa hai)</em> "
            "is the form you will hear in every market and shop."
        ),
        "table": [
            ("Asking the price of something", "यह कितना है? <em>yah kitanaa hai?</em>"),
            ("Asking how many (countable things)", "कितने? <em>kitne?</em>"),
            ("Asking how much (uncountable, e.g. milk)", "कितना? <em>kitnaa?</em>"),
            ("How much is it? (short, common)", " कितना? <em>kitnaa?</em>"),
        ],
        "sections": [
            (
                "Kitnaa hai — the price question",
                "<p>When you are buying something, <em>kitnaa hai</em> is the phrase "
                "you need. Literally \"how much is (it)?\" It works for anything — "
                "food, a taxi, a trinket. Point at the thing and say it; the response "
                "will be a number and you can negotiate from there.</p>"
            ),
            (
                "Kitne vs kitnaa — countable vs uncountable",
                "<p><em>Kitne</em> is used for things you can count (how many apples, "
                "how many people). <em>Kitnaa</em> is for things you measure (how "
                "much milk, how much money, how much time). In casual speech the "
                "distinction blurs, but getting it right marks you as someone who "
                "knows the language a little.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between kitne and kitnaa?",
             "Kitne is used for countable items (how many). Kitnaa is used for uncountable or measured things (how much). For price, always use kitnaa — यह कितना है? (yah kitanaa hai?)."),
            ("How do you say how much is this in Hindi?",
             "यह कितना है? (Yah kitanaa hai?) is the standard price question. You can point at the item and simply say कितना? (Kitnaa?) to keep it short."),
            ("How do you say how much does this cost in Hindi?",
             "The same phrase works: यह कितना है? (Yah kitanaa hai?) is understood as 'how much does this cost.' You can also say यह कितना kostet है — but the first is far more natural."),
            ("How do you ask for the price politely?",
             "To be more polite, add कृपया (krupayaa): कृपया यह कितना है? (Krupayaa, yah kitanaa hai?) — 'please, how much is this?' It is not necessary in markets, but it is appreciated."),
        ],
    },
    {
        "slug": "how-to-say-where-is-in-hindi",
        "question": "How do you say where is in Hindi?",
        "answer": (
            "<strong>कहाँ है</strong> <em>(kahaan hai)</em> is the direct "
            "translation — \"where is.\" Point at the thing you are asking "
            "about, or include its name, and this phrase works everywhere."
        ),
        "table": [
            ("Where is the bathroom?", "शौचालय कहाँ है? <em>shouchaalay kahaan hai?</em>"),
            ("Where is the station?", "स्टेशन कहाँ है? <em>sटे션 kahaan hai?</em>"),
            ("Where are you from?", "आप कहाँ से हैं? <em>aap kahaan se hain?</em>"),
            ("Where is this place?", "यह कहाँ है? <em>yah kahaan hai?</em>"),
        ],
        "sections": [
            (
                "Kahaan hai — the core phrase",
                "<p><em>Kahaan</em> means \"where\" and <em>hai</em> means \"is.\" "
                "Put them together and you have the universal question. In practice, "
                "you almost always add the thing you are asking about — point at a "
                "map, gesture toward a building, or name the place. The structure is: "
                "[thing] + kahaan hai?</p>"
            ),
            (
                "Kahaan se — \"from where\"",
                "<p>When you ask where someone is <em>from</em>, use <em>kahaan se</em>. "
                "<em>Se</em> means \"from,\" so <em>aap kahaan se hain?</em> is \"where "
                "are you from?\" This is a useful distinction — <em>kahaan hai</em> "
                "asks where something is located, <em>kahaan se</em> asks where "
                "something originates.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between kahaan hai and kahaan se?",
             "Kahaan hai means 'where is' (location). Kahaan se means 'from where' (origin). Use kahaan hai for places and kahaan se when asking where someone is from or where something comes from."),
            ("How do you say where is the bathroom in Hindi?",
             "शौचालय कहाँ है? (Shouchaalay kahaan hai?). In casual speech, many people say शौचालय (shouchaalay) or the shorter टपट (tapp) in some regions, but shouchalay is universally understood."),
            ("How do you say where are you in Hindi?",
             "आप कहाँ हैं? (Aap kahaan hain?) — using the plural/polite form of 'you' (aap) and the plural verb (hain). The informal version is तुम कहाँ हो? (tum kahaan ho?)."),
            ("How do you say which way is in Hindi?",
             "कौनसी दिशा (kaunsii dishaa) means 'which direction,' but in practice people say कौनса रास्ता (kaunsaa rastaa) — 'which way/road' — when asking for directions."),
        ],
    },
    {
        "slug": "how-to-say-what-time-is-it-in-hindi",
        "question": "How do you say what time is it in Hindi?",
        "answer": (
            "<strong>Giờ gì?</strong> <em>(kyaa samay hai)</em> is the formal "
            "way. In everyday speech, <strong>क्या समय है</strong> "
            "<em>(kyaa samay hai)</em> or simply <strong>समय क्या है</strong> "
            "<em>(samay kyaa hai)</em> are both natural — and in many "
            "contexts people just ask <strong>ағат</strong> <em>(kya baj raha "
            "hai?)</em>, meaning \"what is striking?\" i.e. what time is it."
        ),
        "table": [
            ("Formal, written", "क्या समय है? <em>kyaa samay hai?</em>"),
            ("Everyday speech", "समय क्या है? <em>samay kyaa hai?</em>"),
            ("Casual, common on the street", "क्या बज रहा है? <em>kyaa baj rahaa hai?</em>"),
            ("What time will it be?", "क्या समय होगा? <em>kyaa samay hoga?</em>"),
        ],
        "sections": [
            (
                "Samay kyaa hai — the everyday form",
                "<p><em>Samay</em> means \"time\" and <em>kyaa</em> means \"what.\" "
                "<em>Samay kyaa hai?</em> is the most common, natural way to ask "
                "the time in everyday speech. It is informal but perfectly polite "
                "and understood everywhere.</p>"
            ),
            (
                "Baj rahaa hai — what is striking",
                "<p><em>Baj rahaa hai</em> literally means \"is striking\" — referring "
                "to a clock or bell striking the hour. It is a very natural, casual "
                "way to ask, especially when you can hear a clock or when you are "
                "asking about a specific time. You will hear it often in everyday "
                "Indian Hindi.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between samay kyaa hai and kyaa samay hai?",
             "Both mean 'what time is it.' Samay kyaa hai (time what is) is slightly more common in everyday speech. Kyaa samay hai (what time is) is slightly more formal but both are completely natural."),
            ("How do you say what time in Hindi?",
             "क्या समय (kyaa samay) is 'what time.' You can use it to ask about a specific time: kya samay milega? (what time will it be / what time can we meet?)."),
            ("How do you say the time is in Hindi?",
             "समय है (samay hai) means 'the time is.' You would say samay das baje hai (the time is ten o'clock) or simply das baje hai (it is ten o'clock)."),
            ("How do you say o'clock in Hindi?",
             "The word baje (बाजे) is used after the number to mean 'o'clock': das baje (ten o'clock), paanch baje (five o'clock). It literally means 'at the striking of.'"),
        ],
    },
    {
        "slug": "how-to-say-see-you-later-in-hindi",
        "question": "How do you say see you later in Hindi?",
        "answer": (
            "<strong>बाद में मिलते हैं</strong> <em>(baad meN milte hain)</em> "
            "is the most natural and widely used — \"we meet later.\" "
            "<strong>तुमसे later</strong> <em>(tumse baad meN)</em> is a "
            "casual alternative, and <strong>फलाने</strong> is the "
            "colloquial way to fill in a specific time."
        ),
        "table": [
            ("Polite, all-purpose", "बाद में मिलते हैं <em>baad meN milte hain</em>"),
            ("Casual, between friends", "बाद में मिलता है <em>baad meN milta hai</em>"),
            ("With a specific time", " PM मिलते हैं <em>PM milte hain</em>"),
            ("A more final goodbye", "फिर मिलते हैं <em>phir milte hain</em> — we meet again"),
        ],
        "sections": [
            (
                "Baad meN milte hain — the standard farewell",
                "<p>This is the phrase you will hear most often when parting "
                "with someone you will see again. Literally \"later we meet,\" it "
                "is warm, natural, and works with friends, colleagues, and "
                "acquaintances. The plural <em>milte hain</em> is the polite "
                "form; with a close friend you might hear the singular "
                "<em>milta hai</em>.</p>"
            ),
            (
                "Phir milte hain — \"we meet again\"",
                "<p>When the goodbye carries a sense of finality but you still "
                "expect to see the person again, <em>phir milte hain</em> is the "
                "right choice. <em>Phir</em> means \"again,\" so it is slightly "
                "warmer than <em>baad meN milte hain</em> and implies a more "
                "meaningful parting.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between baad meN milte hain and phir milte hain?",
             "Baad meN milte hain means 'we meet later' — a standard, neutral farewell. Phir milte hain means 'we meet again' — slightly warmer, used when the parting feels more meaningful or when you are not sure when you will next see the person."),
            ("How do you say goodbye in Hindi?",
             "The most common spoken goodbye is अच्छா (acchā) or achha, which means 'okay/good.' Namaste also works as a formal goodbye. See the how to say goodbye in Hindi page for the full picture."),
            ("How do you say see you tomorrow in Hindi?",
             "कल मिलते हैं (kal milte hain) — 'we meet tomorrow.' Kal means tomorrow, and milte hain is 'we meet.' It is the most natural way to say see you tomorrow."),
            ("How do you say take care in Hindi?",
             "दिल से (dil se) is not the phrase. The common spoken form is anywhere from dhiyan rakhe (ध्यान रखें — 'keep attention/take care') to the simpler aap apna dhyan rakhein (आप अपना ध्यान रखें) — 'take care of yourself.'"),
        ],
    },
    {
        "slug": "how-to-say-how-old-are-you-in-hindi",
        "question": "How do you say how old are you in Hindi?",
        "answer": (
            "<strong>आपकी आयु क्या है</strong> <em>(aapkii aayu kyaa hai)</em> "
            "is the direct, polite form. In casual speech, <strong>आयु</strong> "
            "<em>(aayu)</em> is often replaced by the simpler "
            "<strong>उम्र</strong> <em>(umr)</em>, so you will hear "
            "<strong>आपकी उम्र क्या है</strong> <em>(aapki umr kyaa hai)</em> "
            "far more often in everyday conversation."
        ),
        "table": [
            ("Polite, formal", "आपकी आयु क्या है? <em>aapkii aayu kyaa hai?</em>"),
            ("Everyday, most common", "आपकी उम्र क्या है? <em>aapki umr kyaa hai?</em>"),
            ("Casual, informal", "तुमकी उम्र क्या है? <em>tumki umr kyaa hai?</em>"),
            ("My age is...", "मेरी उम्र है... <em>meri umr hai...</em>"),
        ],
        "sections": [
            (
                "Umr — the everyday word",
                "<p>While <em>aayu</em> is the formal word for \"age,\" <em>umr</em> is "
                "what you will hear in daily conversation. <em>Aapki umr kyaa hai?</em> "
                "is the standard way to ask someone their age politely. It works with "
                "strangers, colleagues, and acquaintances.</p>"
            ),
            (
                "Aap vs tum — the politeness level",
                "<p><em>Aap</em> is the polite, formal \"you\" and should be your "
                "default. <em>Tum</em> is the informal \"you\" used with close "
                "friends, children, or people younger than you. If you are unsure, "
                "use <em>aap</em> — it is never wrong, and using <em>tum</em> with "
                "the wrong person can sound rude.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between aayu and umr?",
             "Aayu (आयु) is the formal, written word for 'age.' Umr (उम्र) is the everyday, spoken word. In conversation, umr is far more common — you will rarely hear aayu outside of formal contexts."),
            ("How do you say my age is in Hindi?",
             "मेरी उम्र है (Meri umr hai) — 'my age is.' You would follow it with the number: मेरी उम्र २५ वर्ष है (Meri umr 25 varsh hai) — 'my age is 25 years.'"),
            ("How do you say how old is he in Hindi?",
             "ئۇنىڭ يېشى क्या है (Uski umr kyaa hai?) — 'his/her age is what?' The pronoun changed from aapki/tumki to uski (his/her), but umr kyaa hai stays the same."),
            ("Is it polite to ask someone's age in Hindi?",
             "It depends on the context and the person. Asking an older person's age can be considered rude in some contexts, but asking a peer or a shopkeeper their age in casual conversation is generally fine, especially if you are learning Hindi."),
        ],
    },
    {
        "slug": "how-to-say-i-dont-know-in-hindi",
        "question": "How do you say I don't know in Hindi?",
        "answer": (
            "<strong>मुझे नहीं पता</strong> <em>(mujhe nahin pataa)</em> is the "
            "most common and natural — \"to me not known.\" "
            "<strong>मुझे नहीं पता है</strong> <em>(mujhe nahin pataa hai)</em> "
            "adds the verb and is equally correct. For a firmer "
            "\"I really don't know,\" <strong>मुझे बिल्कुल नहीं पता</strong> "
            "<em>(mujhe bilkul nahin pataa)</em> adds emphasis."
        ),
        "table": [
            ("Everyday, all-purpose", "मुझे नहीं पता <em>mujhe nahin pataa</em>"),
            ("With the verb (equally correct)", "मुझे नहीं पता है <em>mujhe nahin pataa hai</em>"),
            ("Emphatic — I really don't know", "मुझे बिल्कुल नहीं पता <em>mujhe bilkul nahin pataa</em>"),
            ("I don't know that", "उस बात में मुझे नहीं पता <em>us baat meN mujhe nahin pataa</em>"),
        ],
        "sections": [
            (
                "Mujhe nahin pataa — the default",
                "<p>This is the phrase you will hear most often. <em>Mujhe</em> "
                "means \"to me,\" <em>nahin</em> means \"not,\" and <em>pataa</em> "
                "means \"known/known about.\" Together: \"to me not known.\" It is "
                "neutral in register — polite enough for strangers, natural "
                "enough for friends.</p>"
            ),
            (
                "Bilkul nahin pataa — stronger emphasis",
                "<p>When you want to be clear that you genuinely do not know, "
                "add <em>bilkul</em>, which means \"at all.\" <em>Mujhe bilkul "
                "nahin pataa</em> is a firm, unambiguous \"I have no idea at all.\" "
                "It can sound a little sharp if overused, so use it when you "
                "really need to emphasise the ignorance.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between mujhe nahin pataa and mujhe nahin pataa hai?",
             "Both mean 'I don't know.' Mujhe nahin pataa is the more common, slightly shorter spoken form. Mujhe nahin pataa hai adds the verb hai (is) and is equally correct, just slightly more complete."),
            ("How do you say I don't know in Hindi — the most common form?",
             "The most common is मुझे नहीं पता (mujhe nahin pataa). You will hear it constantly in everyday conversation."),
            ("How do you say I don't know anything in Hindi?",
             "मुझे कुछ भी नहीं पता (Mujhe kuch bhi nahin pataa) — 'I don't know anything.' Kuch bhi means 'anything,' so this is a stronger version of the basic phrase."),
            ("How do you say I don't know that in Hindi?",
             "It depends on context. The simplest is उस बारे में मुझे नहीं पता (us baare meN mujhe nahin pataa) — 'about that, I don't know.' Or you can just say नहीं (nahin) — 'no/don't' — as a short response."),
        ],
    },
    {
        "slug": "how-to-say-nice-to-meet-you-in-hindi",
        "question": "How do you say nice to meet you in Hindi?",
        "answer": (
            "<strong>आपसे मिलकर बहुत अच्छा लगा</strong> "
            "<em>(aapase mil kar bahut achhaa lagaa)</em> is the natural, "
            "warm translation — \"meeting you, it felt very good.\" "
            "<strong>आपसे मिलना अच्छा लगा</strong> "
            "<em>(aapase milnaa achhaa lagaa)</em> is a slightly more "
            "formal alternative."
        ),
        "table": [
            ("Warm, natural, most common", "आपसे मिलकर बहुत अच्छा लगा <em>aapase mil kar bahut achhaa lagaa</em>"),
            ("Slightly more formal", "आपसे मिलना अच्छा लगा <em>aapase milnaa achhaa lagaa</em>"),
            ("Short, casual", "मिलकर अच्छा लगा <em>mil kar achhaa lagaa</em>"),
            ("And you (in response)", "मुझे भी <em>mujhe bhi</em> — me too"),
        ],
        "sections": [
            (
                "Aapase mil kar bahut achhaa lagaa — the standard",
                "<p>This is the phrase you will hear most often when meeting someone "
                "for the first time in a polite context. <em>Aapase</em> means \"with "
                "you\" (polite), <em>mil kar</em> means \"having met,\" and "
                "<em>bahut achhaa lagaa</em> means \"it felt very good.\" The "
                "structure — \"having met you, it felt good\" — is the natural Hindi "
                "way to express \"nice to meet you.\"</p>"
            ),
            (
                "Mujhe bhi — the response",
                "<p>When someone says <em>aapase mil kar bahut achhaa lagaa</em> to "
                "you, the natural response is <em>mujhe bhi</em> — \"to me too,\" "
                "meaning \"nice to meet you too.\" It is short, warm, and the "
                "standard reply.</p>"
            ),
        ],
        "faq": [
            ("What is the most natural way to say nice to meet you in Hindi?",
             "आपसे मिलकर बहुत अच्छा लगा (Aapase mil kar bahut achhaa lagaa) is the most natural and commonly used. It literally means 'having met you, it felt very good.'"),
            ("How do you respond when someone says nice to meet you in Hindi?",
             "The standard response is मुझे भी (Mujhe bhi) — 'me too.' It is short, warm, and universally understood as 'nice to meet you too.'"),
            ("How do you say it's a pleasure to meet you in Hindi?",
             "आपसे मिलना एक आनंद की बात है (Aapase milnaa ek anand ki baat hai) is the more formal, literal version — 'meeting you is a matter of joy.' But the standard phrase above is far more common."),
            ("How do you say hello when meeting someone in Hindi?",
             "नमस्ते (Namaste) is the universal greeting for meeting someone. See the how to say hello in Hindi page for the full range of greetings and when to use each."),
        ],
    },
    {
        "slug": "how-to-say-happy-birthday-in-hindi",
        "question": "How do you say happy birthday in Hindi?",
        "answer": (
            "<strong>जन्मदिन मुबारक</strong> <em>(janmadin mubaanrak)</em> is "
            "the most common — it is borrowed from Urdu/Persian and used by "
            "Hindi and Urdu speakers alike. <strong> जन्मदिन की शुभकामनाएँ</strong> "
            "<em>(janmadin kii shubhkaamanaaen)</em> is the more purely Hindi "
            "alternative, meaning \"birthday's good wishes.\""
        ),
        "table": [
            ("Most common, all-purpose", "जन्मदिन मुबारक! <em>janmadin mubaanrak!</em>"),
            ("More purely Hindi", "जन्मदिन की शुभकामनाएँ! <em>janmadin kii shubhkaamanaaen!</em>"),
            ("Adding warmth", "बहुत-बहुत जन्मदिन मुबारक! <em>bahut-bahut janmadin mubaanrak!</em>"),
            ("Wishing someone a long life", "आपको लंबी उम्र मिले <em>aapko lambii umr mile</em>"),
        ],
        "sections": [
            (
                "Janmadin mubaanrak — the everyday form",
                "<p>This is the phrase you will hear and use in almost every "
                "context — at a party, in a message, on a card. <em>Janmadin</em> "
                "means \"birthday\" and <em>mubaanrak</em> means \"blessed/ "
                "auspicious.\" It is borrowed from Urdu but used universally by "
                "Hindi speakers and is completely standard.</p>"
            ),
            (
                "Bahut-bahut — adding emphasis",
                "<p>Repeating <em>bahut</em> — \"very, very\" — is a common way to "
                "add warmth: <em>bahut-bahut janmadin mubaanrak</em> means "
                "\"a very happy birthday.\" It is the natural way to express "
                "extra warmth, especially in a message or when speaking to "
                "someone you are fond of.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between janmadin mubaanrak and janmadin kii shubhkaamanaaen?",
             "Janmadin mubaanrak is the more common, everyday form — borrowed from Urdu and used by all Hindi speakers. Janmadin kii shubhkaamanaaen is the more purely Hindi form, meaning 'birthday's good wishes.' Both are correct and widely understood."),
            ("How do you say happy birthday in Hindi — the most common form?",
             "जन्मदिन मुबारक! (Janmadin mubaanrak!) is the most common. You will hear it at parties, see it on cards, and it is the standard spoken form."),
            ("How do you say many happy returns of the day in Hindi?",
             "There is no exact equivalent, but you can saybahagiaلىق से Many returns — the closest natural phrase is अनेक शुभकामनाएँ (anek shubhkaamanaaen) — 'many good wishes.' Or simply add bahut-bahut (very much) to the standard greeting."),
            ("How do you say happy birthday in Hindi for a friend?",
             "The same phrase works: जन्मदिन मुबारक! (Janmadin mubaanrak!) For a friend, you can add जीतुं (jitun) — 'long life' — or simply say bahut-bahut janmadin mubaanrak for extra warmth."),
        ],
    },
    {
        "slug": "how-to-say-good-luck-in-hindi",
        "question": "How do you say good luck in Hindi?",
        "answer": (
            "<strong>शुभकामनाएँ</strong> <em>(shubhkaamanaaen)</em> is the "
            "direct translation — \"good wishes.\" For exams, interviews, "
            "and big events, <strong>वहीं</strong> <em>(shubhkaamanaaen)</em> "
            "is what you will hear most. The colloquial "
            "<strong>लगभग</strong> form <strong>शुभकामनाएँ</strong> "
            "is universal."
        ),
        "table": [
            ("All-purpose, most common", "शुभकामनाएँ! <em>shubhkaamanaaen!</em>"),
            ("Before an exam or interview", "शुभकामनाएँ! <em>shubhkaamanaaen!</em>"),
            ("Adding warmth", "बहुत-बहुत शुभकामनाएँ! <em>bahut-bahut shubhkaamanaaen!</em>"),
            ("Wishing someone well on a journey", "यात्रा शुभ हो <em>yaatraa shubh ho</em> — may your journey be auspicious"),
        ],
        "sections": [
            (
                "Shubhkaamanaaen — the standard wish",
                "<p>This is the most common, all-purpose way to wish someone good "
                "luck. Literally \"good wishes,\" it is used before exams, interviews, "
                "journeys, new jobs, and any significant event. It is polite, warm, "
                "and understood everywhere. You will hear it constantly in Indian "
                "contexts.</p>"
            ),
            (
                "Yaatraa shubh ho — for a journey",
                "<p>When someone is travelling — going on a trip, moving to a new "
                "city — <em>yaatraa shubh ho</em> is the specific blessing: \"may "
                "your journey be auspicious.\" It is the traditional, warm way to "
                "wish someone well on a journey and is still used today.</p>"
            ),
        ],
        "faq": [
            ("What is the most common way to say good luck in Hindi?",
             "शुभकामनाएँ (Shubhkaamanaaen) is the most common and all-purpose — literally 'good wishes.' It is used before exams, interviews, journeys, and any significant event."),
            ("Is there a Hindi word that means exactly 'good luck'?",
             "There is no single word that translates 'good luck' exactly. Shubhkaamanaaen (good wishes) is the closest and most natural equivalent, and it is universally used in the contexts where English says 'good luck.'"),
            ("How do you say best of luck in Hindi?",
             "शुभकामनाएँ (Shubhkaamanaaen) covers it. For extra emphasis, you can say बहुत-बहुत शुभकामनाएँ (bahut-bahut shubhkaamanaaen) — 'very good wishes.'"),
            ("How do you say good luck with your exam in Hindi?",
             "आपकी परीक्षा के लिए शुभकामनाएँ (Aapkii parikhaa ke liye shubhkaamanaaen) — 'good wishes for your exam.' You can also simply say शुभकामनाएँ (shubhkaamanaaen) if the context is clear."),
        ],
    },
    {
        "slug": "how-to-say-take-care-in-hindi",
        "question": "How do you say take care in Hindi?",
        "answer": (
            "<strong>आप अपना ख्याल रखिए</strong> <em>(aap aapana khayaal "
            "rakhiye)</em> is the polite, standard form — \"you keep your "
            "care/attention.\" <strong>ख्याल रखना</strong> <em>(khayaal "
            "rakhnaa)</em> is the verb, and in casual speech "
            "<strong>धन्यवाद</strong> is sometimes added to close the "
            "conversation warmly."
        ),
        "table": [
            ("Polite, standard", "आप अपना ख्याल रखें <em>aap aapana khayaal rakhein</em>"),
            ("More formal", "आप अपना ख्याल रखिए <em>aap aapana khayaal rakhiye</em>"),
            ("Casual, between friends", "अपना ख्याल रख <em>apana khayaal rakh</em>"),
            ("Short, warm closing", "ख्याल रखें! <em>khayaal rakhein!</em>"),
        ],
        "sections": [
            (
                "Khayaal rakhnaa — the core verb",
                "<p><em>Khayaal</em> means \"care, attention, regard\" and "
                "<em>rakhnaa</em> means \"to keep.\" So <em>khayaal rakhnaa</em> "
                "is literally \"to keep care\" — \"to take care.\" It is the most "
                "common way to express this sentiment in Hindi and works in "
                "every context: a text message, a phone call, a face-to-face "
                "farewell.</p>"
            ),
            (
                "Aap aapana — the polite framing",
                "<p>The polite, complete form is <em>aap aapana khayaal rakhein</em> "
                "— \"you keep your care.\" <em>Aap</em> is the polite \"you\" and "
                "<em>apana</em> means \"your own.\" This is the form to use with "
                "strangers, colleagues, elders, or anyone you are not close to. "
                "The shorter <em>khayaal rakhein!</em> is fine when the context "
                "is already warm.</p>"
            ),
        ],
        "faq": [
            ("What is the most common way to say take care in Hindi?",
             "आप अपना ख्याल रखें (Aap aapana khayaal rakhein) is the standard, polite form. In casual conversation, people often shorten it to ख्याल रखें (Khayaal rakhein)."),
            ("What is the difference between rakhein and rakhiye?",
             "Both mean 'keep.' Rakhein is the polite/standard form. Rakhiye is slightly more formal and respectful. For everyday use, rakhein is more common. Rakhiye is used when you want to be extra polite, especially with elders."),
            ("How do you say take care in Hindi in a text message?",
             "ख्याल रखें (Khayaal rakhein) is the perfect, short form for a text. If you want to be warmer, say अपना ख्याल रखें (Apanaa khayaal rakhein) — 'keep your own care.'"),
            ("How do you say be safe in Hindi?",
             "सकुशल रहें (Sakshal rahen) means 'remain safe/well,' but the more common everyday phrase is ख्याल रखें (Khayaal rakhein) — which carries the sense of both 'take care' and 'be safe.'"),
        ],
    },
    {
        "slug": "how-to-say-where-are-you-from-in-hindi",
        "question": "How do you say where are you from in Hindi?",
        "answer": (
            "<strong>आप कहाँ से हैं?</strong> <em>(aap kahaan se hain?)</em> "
            "is the standard, polite form — \"you from where are?\" "
            "<strong>आप belong कहाँ से करते हैं?</strong> "
            "<em>(aap kahaan se belong karte hain?)</em> is a slightly more "
            "formal alternative, but <em>aap kahaan se hain?</em> is the "
            "one you will hear most."
        ),
        "table": [
            ("Polite, standard", "आप कहाँ से हैं? <em>aap kahaan se hain?</em>"),
            ("More formal", "आप कहाँ के रहते हैं? <em>aap kahaan ke rahte hain?</em>"),
            ("Casual, informal", "तुम कहाँ से हो? <em>tum kahaan se ho?</em>"),
            ("Where is your home? (warm)", "आपका घर कहाँ है? <em>aapkaa ghar kahaan hai?</em>"),
        ],
        "sections": [
            (
                "Kahaan se — the key phrase",
                "<p>The critical part here is <em>kahaan se</em> — \"from where.\" "
                "<em>Se</em> is the postposition meaning \"from,\" and it changes "
                "the meaning from \"where is\" (location) to \"where are you "
                "from\" (origin). <em>Aap kahaan se hain?</em> is the standard, "
                "polite form and the one you should use first.</p>"
            ),
            (
                "Aap vs tum — politeness",
                "<p><em>Aap</em> is the polite \"you\" and should be your default, "
                "especially with strangers or elders. <em>Tum</em> is informal, "
                "used with close friends or people younger than you. <em>Aap "
                "kahaan se hain?</em> is safe in every context.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between aap kahaan hain and aap kahaan se hain?",
             "Aap kahaan hain? means 'where are you?' (where are you located right now). Aap kahaan se hain? means 'where are you from?' (what is your origin). The word se ('from') is the key difference."),
            ("How do you say I am from in Hindi?",
             "मैं ... से हूँ (Main ... se hoon). For example: मैं अमेरिका से हूँ (Main Amerika se hoon) — 'I am from America.' See the how to introduce yourself in Hindi page for the full pattern."),
            ("How do you say where do you live in Hindi?",
             "आप कहाँ रहते हैं? (Aap kahaan rahte hain?) — 'where do you live?' This asks about current residence, while kahaan se hain asks about origin."),
            ("How do you say what country are you from in Hindi?",
             "आप किस देश से हैं? (Aap kis desh se hain?) — 'you from which country are?' Desh means country, and kis means 'which.' This is more specific than kahaan se hain."),
        ],
    },
    {
        "slug": "how-to-say-do-you-speak-english-in-hindi",
        "question": "How do you say do you speak English in Hindi?",
        "answer": (
            "<strong>क्या आप अंग्रेज़ी जानते हैं?</strong> "
            "<em>(kyaa aap angrezii jaante hain?)</em> is the direct, "
            "polite form — \"do you English know?\" In casual speech, "
            "<strong>अंग्रेज़ी आता है?</strong> <em>(angrezii aataa hai?)</em> "
            "is a very common shorter form, especially when the context "
            "makes clear you are asking about English."
        ),
        "table": [
            ("Polite, complete", "क्या आप अंग्रेज़ी जानते हैं? <em>kyaa aap angrezii jaante hain?</em>"),
            ("Casual, shorter", "अंग्रेज़ी आती है? <em>angrezii aatii hai?</em>"),
            ("Informal", "तुम अंग्रेज़ी जानते हो? <em>tum angrezii jaante ho?</em>"),
            ("Do you know English? (alternate)", "क्या आपको अंग्रेज़ी आना है? <em>kyaa aapko angrezii aanaa hai?</em>"),
        ],
        "sections": [
            (
                "Angrezii jaante hain — the standard form",
                "<p><em>Angrezii</em> means \"English\" and <em>jaante hain</em> "
                "means \"know.\" <em>Kyaa aap angrezii jaante hain?</em> is the "
                "polite, complete form and the one to use with strangers, "
                "elders, or in any formal context. It is clear, respectful, "
                "and universally understood.</p>"
            ),
            (
                "Angrezii aatii hai — the shorter form",
                "<p>In casual conversation, especially when the context is "
                "clear, you will hear <em>angrezii aatii hai?</em> — \"English "
                "comes?\" The verb <em>aanaa</em> (to come) is used colloquially "
                "to mean \"to know/come naturally,\" so <em>angrezii aatii hai</em> "
                "means \"do English come (to you)?\" It is informal but very "
                "natural and commonly used.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between angrezii jaante hain and angrezii aatii hai?",
             "Angrezii jaante hain ('do you know English?') is the more formal, complete form. Angrezii aatii hai ('do English come to you?') is the casual, shorter form — both mean 'do you speak English?' but the first is more polite and complete."),
            ("How do you say I speak English in Hindi?",
             "मैं अंग्रेज़ी बोलता हूँ (Main angrezii bolataa hoon) — 'I speak English.' For a female speaker, it would be बोलती हूँ (bolatii hoon). Or you can say मैं अंग्रेज़ी जानता हूँ (Main angrezii jaanta hoon) — 'I know English.'"),
            ("How do you say I don't speak English in Hindi?",
             "मैं अंग्रेज़ी नहीं बोलता (Main angrezii nahin bolataa) — 'I don't speak English.' For a female speaker: नहीं बोलती (nahin bolatii). Or use the shorter: अंग्रेज़ी नहीं आती (Angrezii nahin aatii) — 'English doesn't come to me.'"),
            ("How do you say can you speak English in Hindi?",
             "क्या आप अंग्रेज़ी बोल सकते हैं? (Kyaa aap angrezii bol sakte hain?) — 'can you speak English?' This uses the verb bolna (to speak) rather than jaana (to know), which is more specific to the act of speaking."),
        ],
    },
    {
        "slug": "how-to-say-i-am-lost-in-hindi",
        "question": "How do you say I am lost in Hindi?",
        "answer": (
            "<strong>मैं दबाव में हूँ</strong> — no, that is not right. "
            "<strong>मैं रास्ता खो चुका हूँ</strong> "
            "<em>(main rastaa kho chukaa hoon)</em> is the direct "
            "translation — \"I have lost the way.\" In everyday speech, "
            "<strong>मैं गुम हूँ</strong> <em>(main gum hoon)</em> is far "
            "more common — <em>gum</em> means \"lost\" in the sense of "
            "\"missing/disoriented.\""
        ),
        "table": [
            ("Most common, everyday", "मैं गुम हूँ <em>main gum hoon</em>"),
            ("I have lost the way (formal)", "मैं रास्ता खो चुका हूँ <em>main rastaa kho chukaa hoon</em>"),
            ("I can't find the way", "मुझे रास्ता नहीं मिल रहा <em>mujhe rastaa nahin mil rahaa</em>"),
            ("I am lost here (pointing)", "मैं यहाँ गुम हूँ <em>main yahaan gum hoon</em>"),
        ],
        "sections": [
            (
                "Gum hoon — the everyday form",
                "<p><em>Gum</em> (गुम) is the word you will hear most often. It "
                "comes from the Urdu/Persian <em>gum</em> meaning \"lost, "
                "missing,\" and it is the standard, natural way to say \"I am "
                "lost\" in everyday Hindi. <em>Main gum hoon</em> is simple, "
                "clear, and understood everywhere — on the street, in a shop, "
                "at a station.</p>"
            ),
            (
                "Rastaa kho chukaa hoon — the fuller form",
                "<p><em>Rastaa kho chukaa hoon</em> literally means \"I have lost "
                "the road/way.\" It is more complete and slightly more formal, "
                "and it is useful when you need to be very clear — for example, "
                "explaining your situation to a police officer or someone who "
                "may not know the casual <em>gum</em>. Both forms are correct; "
                "<em>gum hoon</em> is the everyday default.</p>"
            ),
        ],
        "faq": [
            ("What is the most common way to say I am lost in Hindi?",
             "मैं गुम हूँ (Main gum hoon) is the most common and natural. Gum means 'lost/disoriented' and is the everyday word used in conversation."),
            ("What is the difference between gum hoon and rastaa kho chukaa hoon?",
             "Gum hoon is the casual, everyday form — 'I am lost.' Rastaa kho chukaa hoon is more complete and formal — 'I have lost the way.' Both are correct; gum hoon is what you will hear most."),
            ("How do you say I can't find the way in Hindi?",
             "मुझे रास्ता नहीं मिल रहा (Mujhe rastaa nahin mil rahaa) — 'the way is not being found by me.' The verb mil rahaa (is being found) with the negative nahin conveys 'I can't find the way.'"),
            ("How do you say I need directions in Hindi?",
             "मुझे रसตา चाहिए (Mujhe rastaa chaahiye) or more naturally, directions: मुझे रास्ता बताइए (Mujhe rastaa bataaiye) — 'tell me the way.' See the how to ask for directions in Hindi page for more."),
        ],
    },
    {
        "slug": "how-to-say-i-am-tired-in-hindi",
        "question": "How do you say I am tired in Hindi?",
        "answer": (
            "<strong>मैं थरा गया हूँ</strong> <em>(main tharra gaa ya hoon)</em> "
            "or <strong>मैं थक गया हूँ</strong> "
            "<em>(main thaak gaa ya hoon)</em> are the two most common — "
            "\"I have become tired.\" <em>Thaak gaa ya hoon</em> is the "
            "more standard form; <em>tharra gaa ya hoon</em> carries a "
            "touch more weariness."
        ),
        "table": [
            ("Standard, all-purpose", "मैं थक गया हूँ <em>main thaak gayaa hoon</em>"),
            ("More weary, worn out", "मैं थरा गया हूँ <em>main tharra gaa ya hoon</em>"),
            ("Female speaker (standard)", "मैं थक गई हूँ <em>main thaak gaii hoon</em>"),
            ("I am very tired", "मैं बहुत थक गया हूँ <em>main bahut thaak gayaa hoon</em>"),
        ],
        "sections": [
            (
                "Thaak gayaa hoon — the standard form",
                "<p><em>Thaak</em> means \"tired\" and <em>gayaa</em> means "
                "\"became/gone.\" <em>Main thaak gayaa hoon</em> literally means "
                "\"I have become tired.\" It is the standard, all-purpose way to "
                "say you are tired and works in every context — after work, "
                "after a journey, after exercise. It is neutral in register and "
                "universally understood.</p>"
            ),
            (
                "Tharrnaa gaa ya hoon — more weary",
                "<p><em>Tharrnaa</em> is a slightly stronger, more colloquial "
                "verb than <em>thaaknaa</em>, carrying a sense of being worn "
                "out, exhausted, or drained. <em>Main tharra gaa ya hoon</em> "
                "means \"I am worn out,\" and it is the natural choice when you "
                "want to convey deeper fatigue — after a long day, a hard "
                "journey, or a stretch of being on your feet.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between thaak gayaa hoon and tharra gaa ya hoon?",
             "Thaak gayaa hoon is the standard, all-purpose 'I am tired.' Tharra gaa ya hoon is slightly stronger, meaning 'I am worn out/exhausted.' Both are correct; thaak gayaa hoon is the more common default."),
            ("How do you say I am tired in Hindi — for a female speaker?",
             "For a female speaker, the verb forms change: मैं थक गई हूँ (Main thaak gaii hoon) — 'I have become tired.' The past tense participle changes from gayaa (masc) to gaii (fem)."),
            ("How do you say I am very tired in Hindi?",
             "मैं बहुत थक गया हूँ (Main bahut thaak gayaa hoon) — 'I am very tired.' Bahut means 'very/much,' so adding it to the standard phrase gives you the emphasis."),
            ("How do you say I am exhausted in Hindi?",
             "मैं बहुत थरा गया हूँ (Main bahut tharra gaa ya hoon) or ฉัน exhaustion — the stronger tharra form with bahut (very) conveys 'I am exhausted.' You can also say मैं खटखटा गया हूँ for a very colloquial, worn-out feeling."),
        ],
    },
    {
        "slug": "how-to-say-what-is-this-in-hindi",
        "question": "How do you say what is this in Hindi?",
        "answer": (
            "<strong>यह क्या है?</strong> <em>(yah kyaa hai)</em> is the "
            "direct, universal translation. Point at the thing you are "
            "asking about and this phrase works everywhere. For something "
            "further away, use <strong>वह क्या है?</strong> "
            "<em>(voh kyaa hai)</em>."
        ),
        "table": [
            ("Pointing at something near", "यह क्या है? <em>yah kyaa hai?</em>"),
            ("Pointing at something far", "वह क्या है? <em>voh kyaa hai?</em>"),
            ("What is this called? (asking name)", "इसका नाम क्या है? <em>iskaa naam kyaa hai?</em>"),
            ("What is this thing? (emphatic)", "यह क्या चीज़ है? <em>yah kyaa cheez hai?</em>"),
        ],
        "sections": [
            (
                "Yah kyaa hai — the core phrase",
                "<p><em>Yah</em> means \"this\" (near you) and <em>kyaa</em> "
                "means \"what.\" <em>Yah kyaa hai?</em> is the most basic, "
                "universal question in Hindi — \"what is this?\" Point at the "
                "object and say it; the response will be the name or "
                "description. It is the first question structure every learner "
                "should master.</p>"
            ),
            (
                "Yah vs voh — near vs far",
                "<p><em>Yah</em> (this) is used for things close to you or "
                "close to the listener. <em>Voh</em> (that) is used for things "
                "further away. The distinction matters: if you point at "
                "something on the other side of the room, say <em>voh kyaa "
                "hai?</em>. If it is right in front of you or you are holding "
                "it, say <em>yah kyaa hai?</em>.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between yah kyaa hai and voh kyaa hai?",
             "Yah kyaa hai means 'what is this?' (referring to something near). Voh kyaa hai means 'what is that?' (referring to something far). Yah = this (near), voh = that (far)."),
            ("How do you say what is this called in Hindi?",
             "इसका नाम क्या है? (Iskaa naam kyaa hai?) — 'what is its name?' Iskaa means 'its,' naam means 'name,' and kyaa hai means 'what is.' This is the natural way to ask what something is called."),
            ("How do you say what are these in Hindi?",
             "ये क्या हैं? (Ye kyaa hain?) — the plural form. Ye (ये) is the plural of yah (this), and hain is the plural of hai. So ye kyaa hain? means 'what are these?'"),
            ("How do you say what is that in Hindi?",
             "वह क्या है? (Voh kyaa hai?) — 'what is that?' Use voh for something far from both you and the listener. If it is far from you but near the listener, you can use yah."),
        ],
    },
    {
        "slug": "how-to-say-i-like-it-in-hindi",
        "question": "How do you say I like it in Hindi?",
        "answer": (
            "<strong>मुझे यह पसंद है</strong> <em>(mujhe yah pasand "
            "hai)</em> is the direct, natural translation — \"to me this "
            "is liked.\" <strong>मैं इसे पसंद करता हूँ</strong> "
            "<em>(main ise pasand kartaa hoon)</em> is the alternative "
            "verb form — \"I it like.\" Both are correct and commonly used."
        ),
        "table": [
            ("Most common, natural", "मुझे यह पसंद है <em>mujhe yah pasand hai</em>"),
            ("Using the verb form", "मैं इसे पसंद करता हूँ <em>main ise pasand kartaa hoon</em>"),
            ("I like this a lot", "मुझे यह बहुत पसंद है <em>mujhe yah bahut pasand hai</em>"),
            ("Female speaker (verb form)", "मैं इसे पसंद करती हूँ <em>main ise pasand kartii hoon</em>"),
        ],
        "sections": [
            (
                "Mujhe yah pasand hai — the default",
                "<p>This is the most common, natural way to say \"I like it.\" "
                "<em>Mujhe</em> means \"to me,\" <em>yah</em> means \"this,\" "
                "and <em>pasand hai</em> means \"is liked.\" The structure — "
                "\"to me this is liked\" — is the standard Hindi way to express "
                "liking, and it is the phrase you will hear most often in "
                "everyday conversation.</p>"
            ),
            (
                "Pasand kartaa hoon — the verb form",
                "<p><em>Main ise pasand kartaa hoon</em> uses the verb "
                "<em>karnaa</em> (to do) — literally \"I do like it.\" It is "
                "equally correct but slightly more deliberate. The <em>mujhe "
                "pasand hai</em> form is more common and more natural in most "
                "contexts. Both are fine; the first is the default.</p>"
            ),
        ],
        "faq": [
            ("What is the most natural way to say I like it in Hindi?",
             "मुझे यह पसंद है (Mujhe yah pasand hai) is the most natural and common. It literally means 'to me this is liked' and is the standard way to express liking something."),
            ("What is the difference between mujhe yah pasand hai and main ise pasand kartaa hoon?",
             "Mujhe yah pasand hai is the more common, natural form — 'to me this is liked.' Main ise pasand kartaa hoon is the verb form — 'I like it.' Both are correct, but the first is the everyday default."),
            ("How do you say I like it very much in Hindi?",
             "मुझे यह बहुत पसंद है (Mujhe yah bahut pasand hai) — add bahut (very/much) to the standard phrase. For even more emphasis, आप much: मुझे यह बहुत-बहुत पसंद है."),
            ("How do you say I don't like it in Hindi?",
             "मुझे यह पसंद नहीं है (Mujhe yah pasand nahin hai) — add nahin (not) after pasand. The structure is identical, just with the negation inserted between pasand and hai."),
        ],
    },
    {
        "slug": "how-to-say-congratulations-in-hindi",
        "question": "How do you say congratulations in Hindi?",
        "answer": (
            "<strong>शुभकामनाएँ</strong> <em>(shubhkaamanaaen)</em> is the "
            "direct, all-purpose translation — \"good wishes.\" "
            "<strong> बधाई</strong> <em>(badhaii)</em> is the more "
            "celebratory, colloquial form used at weddings, for promotions, "
            "and at celebrations."
        ),
        "table": [
            ("All-purpose, formal", "शुभकामनाएँ! <em>shubhkaamanaaen!</em>"),
            ("Celebration, wedding, party", "बधाई! <em>badhaii!</em>"),
            ("Very warm, emphatic", "बहुत-बहुत बधाई! <em>bahut-bahut badhaii!</em>"),
            ("Congratulations on your success", "सफलता के लिए शुभकामनाएँ <em>safaltaa ke liye shubhkaamanaaen</em>"),
        ],
        "sections": [
            (
                "Shubhkaamanaaen — the formal wish",
                "<p>This is the safe, all-purpose word for \"congratulations.\" "
                "It means \"good wishes\" and works in any context — a promotion, "
                "an exam result, a new job, a graduation. It is polite, formal, "
                "and never wrong. If you are unsure which word to use, "
                "<em>shubhkaamanaaen</em> is the choice.</p>"
            ),
            (
                "Badhaii — the celebratory form",
                "<p><em>Badhaii</em> is the warmer, more colloquial form used at "
                "celebrations — weddings, parties, festivals. It carries more "
                "of the celebratory, joyful feel. If someone is celebrating "
                "something big — a wedding, a birth, a big win — <em>badhaii</em> "
                "is the more natural and enthusiastic choice. You will hear it "
                "constantly at Indian celebrations.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between shubhkaamanaaen and badhaii?",
             "Shubhkaamanaaen is the formal, all-purpose 'congratulations' — good wishes. Badhaii is the warmer, more celebratory form used at weddings, parties, and festivals. Shubhkaamanaaen is safe in any context; badhaii is more enthusiastic and celebration-specific."),
            ("What is the most common way to say congratulations in Hindi?",
             "Both are common. Shubhkaamanaaen is the formal all-purpose form. Badhaii is the celebratory form you will hear at weddings and parties. For a general congratulations, shubhkaamanaaen is the safest choice."),
            ("How do you say congratulations on your wedding in Hindi?",
             "शादी के लिए शुभकामनाएँ (Shaadii ke liye shubhkaamanaaen) — 'congratulations for the wedding.' At a wedding, people will also say badhaii! (celebration!) repeatedly."),
            ("How do you say congratulations on your success in Hindi?",
             "सफलता के लिए शुभकामनाएँ (Safaltaa ke liye shubhkaamanaaen) — 'congratulations for the success.' Safaltaa means success, ke liye means 'for,' and shubhkaamanaaen means 'good wishes/congratulations.'"),
        ],
    },
    {
        "slug": "how-to-say-where-is-the-bathroom-in-hindi",
        "question": "How do you say where is the bathroom in Hindi?",
        "answer": (
            "<strong>शौचालय कहाँ है?</strong> "
            "<em>(shouchaalay kahaan hai?)</em> is the direct, polite "
            "form. In casual speech, especially in a restaurant or shop, "
            "<strong>शौचालय</strong> <em>(shouchaalay)</em> is universally "
            "understood, and many people simply say <strong>टपट</strong> "
            "<em>(tapp)</em> or <strong>बathroom</strong> in informal "
            "contexts."
        ),
        "table": [
            ("Polite, formal", "शौचालय कहाँ है? <em>shouchaalay kahaan hai?</em>"),
            ("Pointing, short", "शौचालय? <em>shouchaalay?</em>"),
            ("Informal, common", "टपट कहाँ है? <em>tapp kahaan hai?</em>"),
            ("Can you tell me where the bathroom is?", "शौचालय का रस्ता बता सकते हैं? <em>shouchaalay ka rastaa bataa sakte hain?</em>"),
        ],
        "sections": [
            (
                "Shouchaalay — the universal word",
                "<p><em>Shouchaalay</em> (शौचालय) is the standard, polite word "
                "for \"bathroom/toilet\" and is understood everywhere in India. "
                "Combine it with <em>kahaan hai?</em> for \"where is the "
                "bathroom?\" It is the safe, correct choice in any context — "
                "a restaurant, a hotel, a public building. Nobody will "
                "misunderstand it.</p>"
            ),
            (
                "Tapp — the informal alternative",
                "<p>In informal settings, especially in some regions, you may "
                "hear <em>tapp</em> (टपट) or other colloquial words for "
                "bathroom. These are regional and informal — use <em>shouchaalay</em> "
                "with strangers or in any context where you want to be polite. "
                "The informal words are fine between friends or in casual "
                "settings but can be crude in formal contexts.</p>"
            ),
        ],
        "faq": [
            ("What is the most polite way to ask where the bathroom is in Hindi?",
             "शौचालय कहाँ है? (Shouchaalay kahaan hai?) is the most polite and universal. Shouchalay means 'bathroom/toilet' and kahaan hai means 'where is.'"),
            ("Is there a casual word for bathroom in Hindi?",
             "Yes. In some regions, people use टपट (tapp) or other informal words. However, shouchalay is universally understood and polite. Use shouchalay in any situation where you want to be respectful."),
            ("How do you say toilet in Hindi?",
             "शौचालय (Shouchaalay) is the polite, standard word. In formal written contexts, you may also see पचनाय (pachaanāy), but shouchalay is the everyday spoken form."),
            ("How do you say can I use the bathroom in Hindi?",
             "मैं शौचालय सकता हूँ? (Main shouchalay saktaa hoon?) is a direct way. More politely, you can say शौचालय इस्तेमाल कर सकता हूँ? (Shouchaalay istemaal kar saktaa hoon?) — 'can I use the bathroom?'"),
        ],
    },
    {
        "slug": "how-to-say-i-am-sorry-in-hindi",
        "question": "How do you say I am sorry in Hindi?",
        "answer": (
            "<strong>माफ़ करें</strong> <em>(maaf karein)</em> is the polite, "
            "standard form — \"forgive (me).\" <strong>माफ़ कर</strong> "
            "<em>(maaf kar)</em> is the casual version used between "
            "friends. For a more formal apology, "
            "<strong>क्षमा करें</strong> <em>(kshamaa karein)</em> is "
            "appropriate."
        ),
        "table": [
            ("Polite, all-purpose", "माफ़ करें <em>maaf karein</em>"),
            ("Casual, between friends", "माफ़ कर <em>maaf kar</em>"),
            ("More formal, serious apology", "क्षमा करें <em>kshamaa karein</em>"),
            ("I am sorry (statement)", "मैं माफ़ी चाहता हूँ <em>main maafii chaahata hoon</em>"),
        ],
        "sections": [
            (
                "Maaf karein — the everyday apology",
                "<p>This is the most common, all-purpose way to say \"sorry\" in "
                "Hindi. <em>Maaf</em> means \"forgive/pardon\" and <em>karein</em> "
                "is the polite imperative \"do.\" Together: \"please forgive.\" It "
                "is polite, natural, and works in almost every context — bumping "
                "into someone, being late, making a mistake. It is the safe "
                "default.</p>"
            ),
            (
                "Kshamaa karein — the formal apology",
                "<p><em>Kshamaa karein</em> is a more formal, weightier word "
                "for \"forgive.\" It is appropriate when the offence is more "
                "significant — a real mistake, a serious inconvenience. It "
                "carries more gravity than <em>maaf karein</em> and is the right "
                "choice when you want your apology to feel sincere and "
                "formal.</p>"
            ),
        ],
        "faq": [
            ("What is the difference between maaf karein and kshamaa karein?",
             "Maaf karein is the everyday, common 'sorry' — polite and all-purpose. Kshamaa karein is more formal and weightier, used for more serious apologies. For most everyday situations, maaf karein is the natural choice."),
            ("What is the most common way to say sorry in Hindi?",
             "माफ़ करें (Maaf karein) is the most common. You will hear it constantly in everyday situations — bumping into someone, making a mistake, being late. It is the standard, polite apology."),
            ("How do you say I am sorry in Hindi — the statement form?",
             "मैं माफ़ी चाहता हूँ (Main maafii chaahata hoon) — 'I want forgiveness/I apologise.' This is the full statement form, used when you want to express that you are apologising as a complete thought, rather than just saying 'forgive me.'"),
            ("How do you say sorry in Hindi between friends?",
             "माफ़ कर (Maaf kar) is the casual form used between friends, family, and people you are close to. The ending changes from the polite -ein to the casual -a, which signals informality."),
        ],
    },
]


def build_page(entry: dict, idx: int) -> str:
    """Render a single ask/ page, structurally identical to the existing ones."""
    slug = entry["slug"]
    q = entry["question"]
    desc = entry["answer"].replace("<strong>", "").replace("</strong>", "")
    desc = desc.replace("<em>", "").replace("</em>", "")
    desc = desc[:155] if len(desc) > 155 else desc

    # Breadcrumb + QAPage + FAQPage + BreadcrumbList schema
    schema_faq_pairs = "\n".join(
        f'            {{"@type":"Question","name":{json.dumps(fq[0])},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(fq[1])}}}}}'
        for fq in entry["faq"]
    )

    schema = (
        '<script type="application/ld+json">'
        + json.dumps({
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "QAPage",
                    "@id": f"https://ekguru.shop/ask/{slug}/#qa",
                    "mainEntity": {
                        "@type": "Question",
                        "name": q,
                        "text": q,
                        "answerCount": 1,
                        "dateCreated": "2026-11-21",
                        "author": {"@type": "Organization", "name": "EkGuru"},
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": entry["answer"].replace("<strong>", "").replace("</strong>", "")
                                .replace("<em>", "").replace("</em>", ""),
                            "dateCreated": "2026-11-21",
                            "url": f"https://ekguru.shop/ask/{slug}/",
                            "author": {"@type": "Organization", "name": "EkGuru", "url": "https://ekguru.shop/"},
                        },
                    },
                },
                {
                    "@type": "FAQPage",
                    "@id": f"https://ekguru.shop/ask/{slug}/#faq",
                    "mainEntity": [
                        {"@type": "Question", "name": fq[0],
                         "acceptedAnswer": {"@type": "Answer", "text": fq[1]}}
                        for fq in entry["faq"]
                    ],
                },
                {
                    "@type": "BreadcrumbList",
                    "@id": f"https://ekguru.shop/ask/{slug}/#breadcrumb",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "EkGuru", "item": "https://ekguru.shop/"},
                        {"@type": "ListItem", "position": 2, "name": "Hindi questions", "item": "https://ekguru.shop/ask/"},
                        {"@type": "ListItem", "position": 3, "name": q, "item": f"https://ekguru.shop/ask/{slug}/"},
                    ],
                },
            ],
        })
        + "</script>"
    )

    # Table rows
    table_rows = "\n".join(
        f'            <tr><td data-h="Situation">{r[0]}</td><td data-h="Say">{r[1]}</td></tr>'
        for r in entry["table"]
    )

    # Sections
    sections_html = "\n".join(
        f'    <h2>{h}</h2>\n    {b}' for h, b in entry["sections"]
    )

    # FAQ section
    faq_html = "\n".join(
        f'    <h3>{fq[0]}</h3>\n    <p>{fq[1]}</p>' for fq in entry["faq"]
    )

    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append("")
    parts.append('<html data-learning-language="hi" dir="ltr" lang="en" data-ad-class="HIGH_CONTENT">')
    parts.append('<head><!-- ekguru:ultra-head:start -->')
    parts.append("<script>(function(){var t;try{t=localStorage.getItem('ekguru:theme:v2')}catch(e){}if(['light','dark','contrast'].indexOf(t)<0)t=typeof matchMedia==='function'&&matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;document.documentElement.classList.add('eg-js')})()</script>")
    parts.append('<script src="/js/voice-languages.js" defer></script>')
    parts.append('<script src="/js/voice.js" defer></script>')
    parts.append('<script src="/js/ui-motion.js" defer></script>')
    parts.append('<!-- ekguru:ultra-head:end -->')
    parts.append("")
    parts.append('<meta charset="utf-8"/>')
    parts.append('<meta content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" name="google-site-verification"/>')
    parts.append('<meta content="width=device-width,initial-scale=1" name="viewport"/>')
    parts.append(f"<title>{q} | EkGuru</title>")
    parts.append(f'<meta content="{desc}" name="description"/>')
    parts.append('<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>')
    parts.append(f'<link href="https://ekguru.shop/ask/{slug}/" rel="canonical"/>')
    parts.append('<meta content="article" property="og:type"/>')
    parts.append(f'<meta content="{q} | EkGuru" property="og:title"/>')
    parts.append(f'<meta content="{desc}" property="og:description"/>')
    parts.append(f'<meta content="https://ekguru.shop/ask/{slug}/" property="og:url"/>')
    parts.append("")
    parts.append('           <meta content="https://ekguru.shop/images/og-cover.jpg" property="og:image"/>')
    parts.append('           <meta property="og:image:width" content="1200">')
    parts.append('           <meta property="og:image:height" content="630">')
    parts.append('           <meta property="og:image:alt" content="EkGuru — free, self-paced Hindi learning">')
    parts.append('<link href="../../images/favicon.ico" rel="icon" sizes="any"/>')
    parts.append('<link href="../../manifest.webmanifest" rel="manifest"/>')
    parts.append('<link href="../../images/apple-touch-icon.png" rel="apple-touch-icon"/>')
    parts.append('<meta content="#4f32d9" name="theme-color"/>')
    parts.append('<link href="../../css/style.min.css" rel="stylesheet"/>')
    parts.append('<!-- ekguru:storybook -->')
    parts.append('<link href="../../css/storybook.css" rel="stylesheet"/>')
    parts.append(schema)
    parts.append("")
    parts.append('<meta content="EkGuru" property="og:site_name"/><meta content="en_US" property="og:locale"/>')
    parts.append('<meta content="summary_large_image" name="twitter:card"/>')
    parts.append(f'<meta content="{q} | EkGuru" name="twitter:title"/>')
    parts.append(f'<meta content="{desc}" name="twitter:description"/>')
    parts.append('<meta content="https://ekguru.shop/images/og-cover.jpg" name="twitter:image"/>')
    parts.append('    <meta content="EkGuru — free, self-paced Hindi learning" name="twitter:image:alt"/><!-- ekguru:adsense:start -->')
    parts.append('<!-- Auto ads: one account loader, and Google places the units. Whether')
    parts.append("     this block is in the page at all is decided by the page's class")
    parts.append('     (html[data-ad-class]) and data/monetization/google-monetization.json')
    parts.append('     -> ad_policy. tools/inject-ads.py enforces it. -->')
    parts.append('<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>')
    parts.append('<link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>')
    parts.append('<meta name="google-adsense-account" content="ca-pub-8175326569491671">')
    parts.append('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8175326569491671" crossorigin="anonymous"></script>')
    parts.append('<!-- ekguru:adsense:end -->')
    parts.append('<!-- ekguru:ultra-assets:start -->')
    parts.append('<link rel="stylesheet" href="/css/tokens.css">')
    parts.append('<link rel="stylesheet" href="/css/ultra.css">')
    parts.append('<!-- ekguru:ultra-assets:end -->')
    parts.append('</head>')
    parts.append('<body data-topic="section-ask">')
    parts.append('<!-- ekguru:shell-header:start -->')
    parts.append('<header class="hdr">')
    parts.append('  <a class="skip" href="#main">Skip to content</a>')
    parts.append('  <div class="hdr-in">')
    parts.append('    <a class="logo" href="../../index.html">')
    parts.append('      <img class="logo-img" src="../../images/logo.svg" width="38" height="38" alt="EkGuru">')
    parts.append('      <span><span data-brand>EkGuru</span><small data-tagline>One Student. One Goal. One Guru.</small></span>')
    parts.append('    </a>')
    parts.append('    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><span></span></button>')
    parts.append('    <nav class="nav" aria-label="Main">')
    parts.append('      <a href="../../index.html">Home</a>')
    parts.append('      <a href="../../learn/">Learn</a>')
    parts.append('      <a href="../../find-tutors.html">Tutors</a>')
    parts.append('      <a href="../../about/">About</a>')
    parts.append('      <a href="../../contact/">Contact</a>')
    parts.append('      <a class="btn btn-primary btn-sm" href="../../find-tutors.html">Find tutors</a>')
    parts.append('    </nav>')
    parts.append('  </div>')
    parts.append('</header>')
    parts.append('<script src="../../js/site-shell.js" defer></script>')
    parts.append('<script src="../../js/copywatch.js" defer></script>')
    parts.append('<!-- ekguru:shell-header:end -->')
    parts.append('<main id="main">')
    parts.append('<div class="qw pw-legacy">')
    parts.append('<p class="crumb"><a href="../../">EkGuru</a> › <a href="../">Hindi questions</a></p>')
    parts.append('<!-- ekguru:chapter -->')
    parts.append('<div class="sb-chapter" style="--sb-accent:#b45309;--sb-tint:#fdf6ec"><span aria-hidden="true" class="sb-ch-mascot">❓</span><span class="sb-ch-name">Question <i>सवाल</i></span><span class="sb-ch-kind">Question</span><span aria-hidden="true" class="sb-ch-floats">क्यों</span></div>')
    parts.append(f'<h1>{q}</h1><!-- ekguru:ultra-byline:start -->')
    parts.append('<p class="eg-byline" lang="en" dir="ltr" data-eg-chrome="editorial">Author: not separately recorded. Maintained by <a href="/authors/prakash/" hreflang="en">Prakash</a>. Reviewed by: not recorded. Updated: last editorial date not recorded. <a href="/editorial-policy/" hreflang="en">Editorial policy and corrections</a>.</p>')
    parts.append('<!-- ekguru:ultra-byline:end -->')
    parts.append('<!-- ekguru:ultra-audio:start -->')
    parts.append('<p class="eg-voice-note" data-eg-voice-note="hi" lang="en" dir="ltr" data-eg-chrome="audio" aria-live="polite"></p>')
    parts.append('<!-- ekguru:ultra-audio:end -->')
    parts.append("")
    parts.append('<!-- ekguru:storybook -->')
    parts.append('<p class="sb-hint">🔊 <b>Tap any speaker button to hear Hindi spoken.</b> Too fast or slow? Use the <b>speed</b> button at the bottom-right of the page.</p>')
    parts.append(f'<div class="answer">{entry["answer"]}</div>')
    parts.append('<aside class="pg-note" role="note">')
    parts.append('<b>A note on the Hindi spellings</b>')
    parts.append('<p>Devanagari is easy to get slightly wrong when it is typed by hand — a')
    parts.append('    missing matra, the wrong nukta. If something here looks off to you, trust a')
    parts.append('    native speaker over this page and please')
    q_esc = q.replace('?', '%3F').replace('&', '%26')
    parts.append(f'    <a href="../../contact/?topic=Spelling&amp;subject=Hindi%20spelling%20on%3A%20{q_esc}&amp;about={q_esc}&amp;from=https%3A%2F%2Fekguru.shop%2Fask%2F{slug}%2F">tell us</a> so it gets fixed. Romanised')
    parts.append('    spellings are a guide to the sound, not a standard.</p>')
    parts.append('</aside>')
    parts.append('<h2>When to use it</h2>')
    parts.append('<table>')
    parts.append('<thead><tr><th>Situation</th><th>Say</th></tr></thead>')
    parts.append('<tbody>')
    parts.append(table_rows)
    parts.append('</tbody>')
    parts.append('</table>')
    parts.append(sections_html)
    parts.append('<h2>Frequently asked</h2>')
    parts.append(faq_html)
    parts.append('<aside class="pg-cta" aria-label="Next step">')
    parts.append('<h2>Practise this with a teacher</h2>')
    parts.append('<p>Reading an answer is one thing; being corrected while you say it is')
    parts.append('    another. EkGuru tutors teach one to one from')
    parts.append('    <strong data-usd="6" data-usd-mode="bare">$6</strong>')
    parts.append('    a lesson, and most offer a trial.</p>')
    parts.append('<p><a class="btn btn-primary" href="../../find-tutors.html">See the tutors</a>')
    parts.append('<a class="btn btn-ghost" href="../../learn/">Free guides</a></p>')
    parts.append('</aside>')
    parts.append('<div class="rel">')
    parts.append('<h2>Keep going</h2>')
    parts.append('<a href="../../learn/">Free Hindi guides — alphabet, numbers, verbs, phrases</a>')
    parts.append('<a href="../../answers/">Short answers to more Hindi questions</a>')
    parts.append('<a href="../../name-in-hindi/">Write your name in Hindi</a>')
    parts.append('<a href="../../find-tutors.html">Practise with a tutor</a>')
    parts.append('</div>')
    parts.append('<div class="rel">')
    parts.append('<h2>Other questions people ask</h2>')
    parts.append('<ul>')
    rel_links = [
        ("../how-to-say-hello-in-hindi-question/", "How do you say hello in Hindi?"),
        ("../how-to-say-thank-you-in-hindi/", "How do you say thank you in Hindi?"),
        ("../how-to-say-sorry-in-hindi/", "How do you say sorry in Hindi?"),
        ("../how-to-say-please-in-hindi/", "How do you say please in Hindi?"),
        ("../how-to-say-how-are-you-in-hindi/", "How do you say how are you in Hindi?"),
        ("../how-to-say-yes-and-no-in-hindi/", "How do you say yes and no in Hindi?"),
        ("../how-to-say-good-morning-in-hindi/", "How do you say good morning in Hindi?"),
        ("../what-does-namaste-really-mean/", "What does namaste actually mean?"),
        ("../what-does-acha-mean-in-hindi/", "What does acha mean in Hindi?"),
        ("../hindi-words-every-beginner-should-know/", "What are the most useful Hindi words for a beginner?"),
        ("../how-to-introduce-yourself-in-hindi/", "How do you introduce yourself in Hindi?"),
        ("../how-to-count-1-to-10-in-hindi/", "How do you count from 1 to 10 in Hindi?"),
        ("../how-to-practice-hindi-without-a-partner/", "How can I practise speaking Hindi if I have nobody to talk to?"),
        ("../what-does-yaar-mean-in-hindi/", "What does yaar mean in Hindi?"),
        ("../is-hindi-hard-to-learn/", "Is Hindi hard to learn for English speakers?"),
        ("../how-to-say-i-love-you-in-hindi/", "How do you say I love you in Hindi?"),
        ("../what-is-the-hardest-part-of-hindi/", "What is the hardest part of learning Hindi?"),
        ("../do-hindi-speakers-mind-mistakes/", "Will Hindi speakers mind if I make mistakes?"),
        ("../how-to-remember-hindi-genders/", "How do I remember whether a Hindi noun is masculine or feminine?"),
        ("../how-long-to-learn-hindi/", "How long does it take to learn Hindi?"),
    ]
    for href, text in rel_links:
        parts.append(f'<li><a href="{href}">{text}</a></li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('</div>')
    parts.append('<!-- ekguru:pw-bands:start -->')
    parts.append('<!-- ekguru:pw-bands:end -->')
    parts.append('</main>')
    parts.append('<script defer="" src="../../js/site-config.js"></script>')
    parts.append('<!-- ekguru:scroll-restore:start -->')
    parts.append('<script src="../../js/scroll-restore.js"></script>')
    parts.append('<!-- ekguru:scroll-restore:end -->')
    parts.append('<!-- ekguru:recovery:start -->')
    parts.append('<script defer="" src="../../js/recovery.js"></script>')
    parts.append('<!-- ekguru:recovery:end -->')
    parts.append('<script defer="" src="../../js/analytics.js"></script>')
    parts.append('</body>')
    parts.append('</html>')
    return "\n".join(parts)


def main():
    check = "--check" in sys.argv
    out_dir = ROOT / "ask"

    for i, entry in enumerate(PAGES):
        slug = entry["slug"]
        path = out_dir / slug / "index.html"
        content = build_page(entry, i)
        if check:
            if not path.exists():
                print(f"  ✗ {slug}/ — missing")
                sys.exit(1)
            if path.read_text() != content:
                print(f"  ✗ {slug}/ — out of date")
                sys.exit(1)
            print(f"  ✓ {slug}/")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            print(f"  ✓ wrote {slug}/")

    print(f"\n{len(PAGES)} pages {'checked' if check else 'generated'}.")


if __name__ == "__main__":
    main()
