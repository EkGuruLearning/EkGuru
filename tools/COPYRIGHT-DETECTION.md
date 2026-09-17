# EkGuru — Copy Detection & Originality Evidence (owner guide)

Two questions get answered here:

1. **"Kaise pata karein ki hamara content kisne copy kiya?"**
2. **"Agar koi dispute ho, to kaise prove karein ki content hamara hai?"**

## 1. What we already keep (automatic, no effort)

`tools/contentguard.js` builds an originality inventory of the whole site and
writes it to `reports/fingerprints.json`:

| Fingerprint | What it proves |
|---|---|
| `content_hash` (per page) | The exact text of each page at a point in time — tamper-evident. If someone copies a page and later claims it was theirs, the hash + the git commit date is evidence of *our* earlier publication. |
| `simhash` (per page) | Near-duplicate detection — catches "thoda badla hua" copies, not just byte-identical ones. |
| `sha256` + `dhash` (per image) | Image originality, including resized/recompressed copies. |
| `word_count`, `asset_id` | Inventory proof (what existed, when). |

Regenerate any time after content changes:

```
node tools/contentguard.js
```

Git history is the second layer: every publish is a commit with a timestamp,
which is dated, third-party-hosted evidence of first publication.

## 2. How to detect someone copying us (external check)

Work down this list when you suspect a copy:

1. **Google exact-phrase search** — take one distinctive sentence from a page
   (a specific example sentence from a lesson or a unique turn of phrase),
   put it in quotes, search. Any site showing the same sentence verbatim is a
   copy candidate.
2. **Siteliner** (`siteliner.com`) — free, shows who duplicates *our* content.
3. **Copyscape** (`copyscape.com`) — premium but the standard tool; paste a URL
   and it finds copies across the web.
4. **Google Search Console → Performance** — if a page's clicks drop while the
   same topic climbs elsewhere, search the exact phrase (step 1) on the new
   ranking site.

### Distinctive phrases (built in)

Each lesson/answer page already contains original example sentences. For the
highest-value pages, keep a note of 2–3 natural, distinctive phrases (they are
in the content already — no need to add anything artificial). Those are your
search probes.

## 3. If we find a copy — evidence + takedown

1. Save the copy: URL, screenshot, and the date you found it.
2. Record **our** evidence: `reports/fingerprints.json` entry for that page +
   the git commit hash/date of its publication.
3. Send a polite takedown: "This material is original EkGuru content first
   published at <url> on <date> (fingerprint <hash>). Please remove it or add
   attribution."
4. Escalate via the host (DMCA), or Google's copyright removal tool if it is
   outranking us.

## 4. What we deliberately do NOT do

- No right-click blocking, no text-selection blocking, no hidden text. Those
  hurt real users and stop nobody.
- No watermarking every page with hidden markers.

Evidence and a dated fingerprint store are more useful than barriers.
