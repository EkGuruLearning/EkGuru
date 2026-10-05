# Phase 2 — Complete Content Inventory

**Status: started.** The repository-only content inventory is ready for review;
production HTTP status and live rendered behavior remain pending. This phase
follows **PHASE 2 — COMPLETE CONTENT INVENTORY** in
`docs/commands/EkGuru_AdSense_Original_Content_Recovery_Master_Command.md`.

## Where the Phase 2 work is stored

- **Main per-page inventory:** `data/quality/phase2-content-inventory.json`
- **Existing full-page technical inventory:** `data/quality/full-page-inventory.json`
- **Generator:** `tools/build-phase2-content-inventory.py`
- **Integrity test:** `tools/test-phase2-content-inventory.py`

Regenerate with `python3 tools/build-phase2-content-inventory.py`; verify
freshness with `python3 tools/build-phase2-content-inventory.py --check`. The
Phase 2 checks are also part of `python3 tools/build-all.py check`.

## Repository snapshot

The current inventory covers **2,720 repository-backed public HTML pages**:

- 1,006 are indexable in the current source tree; 1,714 are already `noindex`.
- 0 indexable pages are orphaned in the static internal-link graph. The 894
  total orphan rows are noindex pages; they are not counted as indexable orphans.
- 0 broken local links are reported by the refreshed technical inventory.
- Automated risk triage: 88 `HIGH`, 728 `MEDIUM`, 190 `LOW`, and 1,714
  `NOT_INDEXABLE` (the existing noindex state).
- Suggested actions: 816 `IMPROVE`, 190 `KEEP`, and 1,714 `NOINDEX`. No page is
  recommended for removal; no merge, removal, or indexation change was applied.
- 168 indexable pages have no explicit author attribution in page metadata;
  485 indexable pages have no known own-content update date. Unknown values
  remain unknown.
- The median mechanical triage score is 83/100. It is **not** a linguistic,
  editorial, originality, source-support, AdSense, or approval score.

The refreshed `data/quality/full-page-inventory.json` scans public pages only;
it does not count internal HTML source drafts under `tools/` or the Google
verification file as public pages. Its canonical parser reads the canonical
link's `href`, not a `content` attribute.

## What the metrics mean

- `word_count` and `visible_text_length` count visible body text after known
  shared chrome is removed. CJK and Thai use the repository's script-aware word
  counter.
- `unique_text_ratio` is the share of a page's distinct seven-token shingles
  that occur on only that page in this repository snapshot.
- `template_text_ratio` is the share of those shingles appearing on at least
  three pages. These are exact-shingle signals, not semantic originality or
  plagiarism detection.
- `internal_inlinks` and `internal_outlinks` count static repository HTML links;
  runtime-generated links and links from outside this repository are not known.
- `author` and `last_updated` are populated only from explicit page or editorial
  metadata. File modification times are deliberately not used.
- `http_status` is `null` on every row because this is a repository-only scan;
  the report does **not** claim a live crawl or production response status.
- `content_quality_score` is mechanical triage, not an editorial rating.
  `adsense_risk` and `action` are conservative recommendations only. Existing
  `noindex` pages remain noindex; no page was changed or removed.

## Scoped repeated-paragraph sample: course pages

The sample below was taken from actual visible paragraph text in the repository
HTML; it is not a native-language or independent editorial review. For this
scope, “course pages” means the inventory types `language_level`,
`language_lesson`, `language_course`, `language_practice`, and
`learning_content` (including `/learn/<language>/...` course guides).

The AdSense readiness report currently has **338 normalized repeated-paragraph
signature groups**. **246** intersect this course-page scope; after de-duplicating
path references, **244** span at least two distinct course-page URLs and 2 are
same-page signature collisions. Of the 246 intersecting groups, 217 touch at
least one indexable course page; 29 touch only noindex course pages. The
signature intentionally removes numerals, so one signature can contain
paragraphs with different counts. These are review signals, not proof of
copied pages or defects.

| Sample | Actual repository text | Scope and reading |
| --- | --- | --- |
| Unpublished level placeholders | “This address is kept so an old link does not look like a real lesson. There is no vocabulary, no dialogue and no test here.” | Shared on 887 level URLs; all 887 are noindex. This is a visible placeholder boundary, not lesson content. |
| Level-page tool note | “Optional JavaScript tools. Completion is a self-report, not a proficiency certificate. Only a bounded same-origin file list is downloaded; audio may need an installed voice.” | Shared on 92 indexable level pages. It describes the same offline/tool behavior; the paragraph alone does not make the lessons duplicates. |
| Flashcard fallback | “The interactive flashcards need JavaScript. The vocabulary above is the same deck.” | Shared on 19 course/practice pages (18 indexable). This is a short runtime instruction. |
| Flashcard lab description | “This language’s deck carries 300 of the 667 words the course authors, and the lab practises that deck. The lab shows one card at a time, flips on Enter or Space, moves with the arrow keys, and can save a card to your review queue.” | The signature spans 18 indexable practice pages and has 9 actual text variants; the course word totals differ by language. This is shared feature copy with language-specific figures, not evidence that whole pages match. |
| Grammar-guide paragraph | “Do not learn grammar as a list of rules. Learn it as a ladder with seven rungs, where every rung is something you can say out loud today.” | Exact paragraph on 9 `/learn/<language>/grammar/` guides; 7 are indexable. The sampled Bengali and Malayalam pages also contain different language-specific grammar examples, tables and explanations. The shared paragraph still merits contextual editorial review, but is not by itself a duplicate-page finding. |
| Numbers-guide exercise | “A practical exercise: for one week, say the time out loud every time you check your phone. It takes two seconds and it makes the words automatic within days — far faster than revisiting the table.” | Exact paragraph on 9 language-specific numbers guides; 7 are indexable. It is generic advice repeated across otherwise language-specific pages; no action was inferred from the paragraph alone. |
| Numeral-normalized reading-guide sample | “Then the 36 consonants. This is the part people find intimidating, and it is mostly an illusion created by an unfamiliar script: the table below gives you the sound of every letter, in words you already know.” | The signature spans 9 noindex reading guides, but the actual count varies (including 35, 36, 39 and 41 consonants). This is a concrete example of why signature matches need text inspection. |

This bounded sample found both intentional shared feature/placeholder copy and
verbatim generic prose across language-specific guides. The pages sampled also
contain language-specific examples and tables, so a shared paragraph alone does
not establish duplicated page intent. **No content was edited, merged, removed,
or reindexed as a result of this sample.** Native-speaker review, source checks,
and a wider contextual editorial decision remain open; no approval or source
verification is implied.

## Review still needed

This is the Phase 2 inventory baseline, not a final human content-quality audit.
The report cannot establish live HTTP status/redirects, linguistic correctness,
factual support, native-speaker approval, actual rendered/mobile behavior, or
Google AdSense policy compliance. Review the per-page `risk_flags`,
`similarity_group`, `author`, `last_updated`, and `http_status` fields in the
main JSON before deciding whether to keep, improve, merge, noindex, or remove
anything. No destructive action is automated.
