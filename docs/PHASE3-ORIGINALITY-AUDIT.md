# Phase 3 — Originality Audit and Human Review Queue

**Status:** the repository-backed audit and per-page editorial queue are complete.
The master command calls for a **human-edited** originality audit; no named
human editor, native-language reviewer, or external fact-checker performed this
work. Those review statuses deliberately remain pending in every row. This is
not an AI-detector exercise, originality certification, or AdSense approval.

This is **Phase 3 in**
`docs/commands/EkGuru_AdSense_Original_Content_Recovery_Master_Command.md`.
It is separate from the repository's unrelated Phase 3 long-form Learn-content
build.

## Deliverables and regeneration

- **Per-page audit and review queue:** `data/quality/phase3-originality-audit.json`
- **Generator:** `tools/build-phase3-originality-audit.py`
- **Integrity/safety tests:** `tools/test-phase3-originality-audit.py`
- **Input inventory:** `data/quality/phase2-content-inventory.json`

Regenerate and verify with:

```bash
python3 tools/build-phase3-originality-audit.py
python3 tools/build-phase3-originality-audit.py --check
python3 tools/test-phase3-originality-audit.py
```

The generator reads repository HTML only. It does not crawl the live site,
compare against external sites, edit page copy, or change canonical, robots,
indexability, or publication state. The Phase 3 freshness and safety checks are
included in `python3 tools/build-all.py check`.

## Scope and current triage

Every one of the **2,720 public pages** in the Phase 2 inventory has a row and
all ten master-command questions. The currently indexable pages are prioritized
using Phase 2's mechanical risk categories; existing noindex content and
utility/placeholder pages remain explicitly held.

| Review queue | Pages | Meaning |
| --- | ---: | --- |
| `P1_REVIEW` | 88 | Indexable; Phase 2 `HIGH` mechanical triage. First editorial queue, not a finding of poor content. |
| `P2_REVIEW` | 728 | Indexable; Phase 2 `MEDIUM` triage. |
| `P3_CONFIRM` | 190 | Indexable; Phase 2 `LOW` triage. Confirm intent and value; this is not an approval. |
| `HELD_NOINDEX_CONTENT` | 187 | Noindex content-type pages with at least 100 repository words. Keep the existing noindex state pending separate review. |
| `NOINDEX_UTILITY_OR_PLACEHOLDER` | 1,527 | Existing noindex utilities, research pages, and short placeholders. No promotion is recommended by this audit. |

The queue records repository facts and excerpts—title, meta, H1, word count,
text ratios, headings, body samples, links, tables/lists, interactive controls,
script-specific characters, and repeated-paragraph signatures. Shared text is
an evidence pointer only: it **does not independently raise priority or imply a
defect**. The generator reports 326 normalized paragraph signatures appearing
on at least three distinct URLs, spanning 1,554 pages. It found no shared
opening-paragraph signature among currently indexable pages. The focused text
samples and interpretation are in `docs/PHASE2-CONTENT-INVENTORY.md`.

## Concrete repository findings sampled

These are samples from current repository HTML, not source, author, or
linguistic verification:

| Page(s) | Observed text/evidence | Triage |
| --- | --- | --- |
| `/languages/{ar,de,es,fr,it,ja,ko,pt,ru,zh}/quiz/` | The visible quiz introduction refers to an internal identifier such as `EKGURU_COURSE_AR` (“Every question is drawn from the EKGURU_COURSE_AR lesson bank…”). The identifier varies by language across all 10 pages. | High-confidence visible template-token candidate; leave for a deliberate copy/build fix in the content-rebuild phase. It is not hidden-script text. |
| `/answers/how-to-say-i-am-hungry-in-hindi/` | 234 words, four H2s; its excerpt gives a specific Hindi construction and contrasts feelings such as hunger, thirst, and cold. | `P1_REVIEW` because of the mechanical under-250-word signal. The answer may be useful despite its length; an editor should judge completeness and source needs. |
| `/daily-hindi/day-23/` | 249 words, seven H2s, a table and an interactive control; the excerpt includes a specific future-tense pattern and a timed learner task. | `P1_REVIEW` on the same mechanical threshold. A one-word margin is not an editorial verdict. |
| `/languages/es/lessons/numbers-1-to-20/` | 216 words, a table, and links to the Spanish course, practice and quiz; the sampled ending gives Spanish price questions and regional wording. | `P1_REVIEW`; the short count alone cannot establish thin intent or low usefulness. |
| `/languages/ar/quiz/` | 185 words and three interactive controls, alongside the visible internal course-code token above. | `P1_REVIEW`; review both the useful quiz task and the visible copy defect, rather than treating word count as the whole decision. |
| `/learn/bengali/advanced/` | 126 words, one list and no H2s; its short introduction is also the closing paragraph. | `P1_REVIEW`; assess whether the hub provides enough orientation and a useful next step. No automatic rewrite was made. |
| `/tutor/shikha-dutta/` | One phrase, “I have taught,” matched a first-person-experience review pattern. | Candidate for confirmation with the profile owner; the audit does not label the claim false or verified. |

The under-250-word signal covers varied page purposes, including answers,
short lessons, and interactive quizzes. It is a queueing signal—not proof of
thinness, duplication, or low value. Likewise, script-specific examples,
interactive controls, citations, and outgoing links are recorded as observable
signals, not proof of originality, accuracy, or source support.

## What remains unassessed

The report answers the ten questions only where repository evidence supports a
**candidate or structural signal**. It leaves the following explicitly
unverified for every page:

- whether the page answers the learner's real question completely;
- whether EkGuru adds value versus relevant alternatives;
- whether examples and exercises are original or pedagogically sound;
- whether wording is natural in the target language;
- whether statements, numbers, or citations are accurate and source-supported;
- whether any wording is copied from outside the repository;
- whether a first-person, tutor, author, or expertise claim is true;
- whether a language-specific human editor approves the page.

The report records **0 human editorial reviews, 0 native-language reviews, 0
source fact-checks, 0 external similarity checks, and 0 content/indexation
changes**. Those values are intentional—not missing evidence to infer. Phase 3's
repository audit is complete; completing the human-edited portion requires
actual editor review and must not be represented as done by this artifact.
