# 🔍 Search Console — Request Indexing

**How to tell Google your pages exist, instead of waiting weeks for it to notice.**

Total time: about 15 minutes. Do it once, today.

---

# PART 1 — VERIFY THE SITE (do this first)

You cannot request indexing until the property is verified. Both verification methods are
already live on your site, so this is quick.

### Step 1
Go to **https://search.google.com/search-console**
Sign in with **EkGuruLearning@gmail.com** — the same account you generated the code with.

### Step 2
If this is your first property you will see a "Welcome" screen.
Otherwise: click the **property dropdown** at the top left → **+ Add property**.

### Step 3
Two boxes appear. Choose the **right-hand one: URL prefix**.

> ⚠️ Do **not** choose "Domain" on the left. That one needs a DNS TXT record, and you do
> not control DNS for `github.io`. It will never verify. URL prefix is the correct choice.

Paste exactly this, with the trailing slash:

```
https://ekgurulearning.github.io/EkGuru/
```

Click **Continue**.

### Step 4
Google offers several verification methods. **"HTML file"** is usually shown first and it
will work immediately, because that file is already on your site — I verified it returns
a 200 response.

* Choose **HTML file** → click **Verify**

If for any reason it fails, expand **HTML tag** instead and click **Verify** there. That
tag is present on all 28 pages of your site.

You should see: **"Ownership verified"** ✅

---

# PART 2 — SUBMIT THE SITEMAP

The sitemap tells Google about all 25 of your pages in one go. Do this before requesting
individual pages.

1. In the left sidebar click **Sitemaps** (under *Indexing*)
2. In the "Add a new sitemap" box type just:
   ```
   sitemap.xml
   ```
   The domain prefix is already filled in for you.
3. Click **SUBMIT**

Status will show *"Couldn't fetch"* for a few minutes — that is normal, it means Google
has queued it. Refresh after an hour and it should say **Success**, with **25 discovered
pages**.

---

# PART 3 — REQUEST INDEXING (the part you asked about)

This pushes a single page to the front of Google's crawl queue. It typically saves
**two to four weeks** of waiting.

## The procedure, for one URL

### Step 1
At the very top of Search Console there is a long search box that says
**"Inspect any URL in https://ekgurulearning.github.io/EkGuru/"**.

Click into it.

### Step 2
Paste the **full URL**, including `https://`:

```
https://ekgurulearning.github.io/EkGuru/
```

Press **Enter**.

### Step 3
Google shows *"Retrieving data from index…"* for 10–30 seconds.

Then one of two things appears:

**"URL is not on Google"** — expected for a brand new site. This is fine.
**"URL is on Google"** — already indexed, even better.

### Step 4
Either way, click **REQUEST INDEXING**.

It is a small link on the right-hand side of the result panel.

### Step 5
A box appears: *"Testing if live URL can be indexed"* — this takes about a minute. Let it
finish.

Then: **"Indexing requested — URL added to a priority crawl queue."** ✅

Close the box. That URL is done.

---

## The 7 URLs to submit, in this order

Do the most important first, because Google limits you to roughly **10–12 requests per
day** per property.

Copy each one, paste, press Enter, click Request Indexing, wait for the tick, then move to
the next.

```
1.  https://ekgurulearning.github.io/EkGuru/

2.  https://ekgurulearning.github.io/EkGuru/tutor/sushila-g/

3.  https://ekgurulearning.github.io/EkGuru/tutor/hemlata/

4.  https://ekgurulearning.github.io/EkGuru/tutor/tara/

5.  https://ekgurulearning.github.io/EkGuru/find-tutors.html

6.  https://ekgurulearning.github.io/EkGuru/join.html

7.  https://ekgurulearning.github.io/EkGuru/tutor/
```

**Why the tutor pages come so early:** those are your pre-rendered pages with 485–813
words of real content, star ratings and video schema. They are the pages most likely to
actually rank, so they should be crawled first.

## Tomorrow — the language pages

Once the daily limit resets, submit these six:

```
https://ekgurulearning.github.io/EkGuru/es/
https://ekgurulearning.github.io/EkGuru/fr/
https://ekgurulearning.github.io/EkGuru/de/
https://ekgurulearning.github.io/EkGuru/pt/
https://ekgurulearning.github.io/EkGuru/ja/
https://ekgurulearning.github.io/EkGuru/ar/
```

These are real translated files, so each one can rank in its own market.

---

# ⚠️ COMMON PROBLEMS

### "Request indexing" is greyed out or missing
You have hit the daily quota. Wait 24 hours. The sitemap is still working in the
background regardless.

### "URL is not on Google" and you are worried
Completely normal for a new site. The whole point of clicking Request Indexing is to
change that.

### "Page cannot be indexed: Excluded by 'noindex' tag"
Only expected on `tutor.html` without an `?id=`, and on `404.html`. Both are deliberate —
those are shells, not real pages. If you see it on any other URL, tell me.

### "Discovered — currently not indexed"
Google knows about the page but has not crawled it yet. This is a waiting state, not an
error. Backlinks are what move a page out of it fastest — which brings us to the next
section.

### "Crawled — currently not indexed"
Google looked and decided not to index yet. Usually means the page needs more unique
content or more links pointing at it. Your tutor pages have real content, so this should
resolve on its own.

---

# ⏱️ WHAT HAPPENS NEXT

| Time | What to expect |
|---|---|
| Within hours | Google crawls the requested URLs |
| 1–3 days | Search `site:ekgurulearning.github.io/EkGuru` and see pages listed |
| Week 1–2 | Searching **ekguru** returns your site |
| Week 2–4 | **prakash mnit jaipur**, **hemlata hindi tutor** start appearing |
| Month 2 | Long-tail impressions appear in the Performance report |
| Month 3 | First students arriving from search |

## How to check progress yourself

Type this into Google:

```
site:ekgurulearning.github.io/EkGuru
```

It lists every page Google has indexed. Run it every few days — the number should climb
towards 25.

---

# 🥇 PART 4 — BING (2 minutes, genuinely worth it)

Bing powers DuckDuckGo, Yahoo and several AI assistants. It also **reads your keyword meta
tags in full**, which Google ignores — and your site publishes 1,622 keyword phrases per
page across 26 channels. Bing is where that work pays off.

1. Go to **https://www.bing.com/webmasters**
2. Sign in
3. Click **Import from Google Search Console**
4. Authorise, select your property, **Import**

Everything transfers automatically, including the sitemap. Bing usually indexes new sites
faster than Google.

---

# 🔴 PART 5 — THE ONE THING THAT MATTERS MOST

Everything above tells Google your site exists. **This tells Google your site matters.**

Open your **Preply tutor profile**, edit the description, and add a line:

> I also teach through EkGuru: https://ekgurulearning.github.io/EkGuru/

**Why this single action outweighs everything else on this page:** Preply is a
high-authority site about the exact same subject as yours. Google treats a link from a
site like that as a genuine recommendation. One such link will do more for your ranking
than every keyword, schema type and meta channel in this project combined.

Ask Sushila to add it to hers as well. Then add it to:

* YouTube channel → About → Links, and the first line of every video description
* LinkedIn → your profile (you already have `linkedin.com/in/itstheprakash`)
* Instagram bio, WhatsApp Business, your email signature

---

# ✅ TODAY'S CHECKLIST

- [ ] Search Console → Add property → **URL prefix** → verify
- [ ] Sitemaps → submit `sitemap.xml`
- [ ] Request indexing on the 7 URLs above
- [ ] Bing Webmaster → import from Google
- [ ] **Preply profile → add the site link**
- [ ] YouTube → channel About + video descriptions

Tomorrow: request indexing on the six language pages.

---

**Built by Prakash — MNIT Jaipur, CSE 2022–2026 batch pass out.**

© EkGuru — One Student. One Guru. One Goal.
