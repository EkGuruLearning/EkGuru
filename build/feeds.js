const {load,ROOT}=require('./load.js');
const fs=require('fs'),path=require('path');
const W=load(),S=W.EKGURU_SITE,T=W.EKGURU_TUTORS,F=S.founder||{};
const BASE=S.baseUrl.replace(/\/?$/,'/');
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const now=new Date().toUTCString();
const minP=Math.min(...T.map(t=>t.priceUSD)), maxP=Math.max(...T.map(t=>t.priceUSD));

const llms=`# EkGuru

> Online Hindi tutoring. Verified native Hindi tutors from India teach one-to-one
> live lessons to students worldwide, from ${S.currency}${minP} per lesson.
> Founded by ${F.name||'Prakash'} — MNIT Jaipur, CSE ${F.batch||'2022-2026'} batch pass out.

EkGuru is a Hindi-only tutoring platform. Every tutor listed teaches Hindi and nothing
else. Students contact tutors directly; EkGuru takes no commission. Lessons cover
speaking, listening, grammar, vocabulary, pronunciation and the Devanagari script,
for beginner through advanced learners.

## Tutors

${T.map(t=>`- [${t.name}](${BASE}tutor/${t.id}/): ${t.headline}. ${S.currency}${t.priceUSD} per ${t.lessonLength}. Teaches ${(t.teaches||[]).join(', ')}. Levels: ${(t.levels||[]).join(', ')}. Based in ${t.city}, timezone ${t.timezone}.${t.reviewsCount?` Rated ${t.rating}/5 from ${t.reviewsCount} reviews.`:''}${t.youtubeId?` Intro video: https://youtu.be/${t.youtubeId}`:''}`).join('\n')}

## Pages

- [Home](${BASE}): overview, how it works, frequently asked questions
- [Find Tutors](${BASE}find-tutors.html): search and filter by level, price and rating
- [Become a Tutor](${BASE}join.html): free listing for Hindi teachers, no commission
- [Tutor directory](${BASE}tutor/): plain text listing of every tutor

## Languages

The site is available in English, Spanish, French, German, Portuguese, Japanese and
Arabic. Translated pages: ${(W.EKGURU_MARKETS||[]).filter(m=>m.code!=='en').map(m=>`[${m.label}](${BASE}${m.code}/)`).join(', ')}

## Founder

${F.name||'Prakash'} — ${F.title||'Founder'}. ${F.bio||''}
${F.linkedin?`LinkedIn: ${F.linkedin}`:''}
Alma mater: ${F.college||'MNIT Jaipur'} (${F.collegeShort||'MNIT Jaipur'}), ${F.batch||'2022-2026'}.

## Facts

- Languages taught: Hindi only
- Lesson format: live one-to-one video call, ${T[0].lessonLength} typical
- Price range: ${S.currency}${minP} to ${S.currency}${maxP} per lesson
- Currency: shown automatically in the visitor's local currency, charged in USD
- Trial lessons: available with ${T.filter(t=>t.trialAvailable).length} of ${T.length} tutors
- Booking: by email or WhatsApp directly with the tutor, no account needed
- Contact: ${S.email}

## Optional

- [Sitemap](${BASE}sitemap.xml)
- [RSS feed](${BASE}feed.xml)
`;
fs.writeFileSync(path.join(ROOT,'llms.txt'),llms);

const items=T.map(t=>`  <item>
    <title>${esc(t.name)} — ${esc(t.headline)}</title>
    <link>${BASE}tutor/${t.id}/</link>
    <guid isPermaLink="true">${BASE}tutor/${t.id}/</guid>
    <description>${esc((t.about||[])[0]||'')} Lessons ${S.currency}${t.priceUSD} per ${esc(t.lessonLength)}. Teaches ${esc((t.teaches||[]).join(', '))}.</description>
    <category>Hindi tutoring</category>
    <pubDate>${now}</pubDate>
  </item>`).join('\n');

fs.writeFileSync(path.join(ROOT,'feed.xml'),`<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>EkGuru — Online Hindi Tutors</title>
  <link>${BASE}</link>
  <atom:link href="${BASE}feed.xml" rel="self" type="application/rss+xml"/>
  <description>Verified native Hindi tutors teaching one-to-one online lessons worldwide.</description>
  <language>en</language>
  <lastBuildDate>${now}</lastBuildDate>
  <generator>EkGuru static build</generator>
${items}
</channel>
</rss>`);
console.log('llms.txt + feed.xml ✓');
