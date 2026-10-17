# AdSense review: repository status and owner checklist

Updated 17 October 2026. This is a repository-side readiness packet, not a claim
about Google's decision. Google alone determines eligibility and approval. The
counts below are automated triage evidence; they do not establish approval,
originality, native-speaker quality, or live production behavior.

Publisher ID: `pub-8175326569491671` · ads.txt seller: the same, `DIRECT`,
certification authority `f08c47fec0942fa0`.

## Account notice: verify before quoting

An earlier project note describes an AdSense notice mentioning insufficient
content and low content quality. The exact account message, site status, and
date have not been independently verified in this repository work. Check the
owner's AdSense account and the original email before quoting that wording or
using it as the confirmed reason for a decision.

## Current repository evidence

The reports were rebuilt on 17 October 2026 after aligning the readiness audit,
full-page inventory, and Phase 2 inventory on the same visible-body extractor.
Shared navigation, header/footer text, review notices, and `<head>` metadata are
not counted as page body content. These current `data/quality/` reports supersede
the dated snapshots under `reports/`; in particular, an older zero-thin-page
count is not supported by the corrected body-text audit.

| Check | Current result | What it means / does not mean |
|---|---:|---|
| Public HTML inventory | 2,721 pages: 1,006 indexable, 1,715 `noindex` | Static repository inventory; not a live crawl. No robots or canonical changes were made by these audits. |
| Body-depth triage | 76 indexable pages below 250 counted words; 1,089 pages total below the heuristic, of which 1,013 are `noindex` | All 76 indexable pages are under `/learn/` and classified as learning content. The 250-word cutoff is a review heuristic, not a Google minimum or automatic quality verdict. Review substance and task fit; do not add filler to reach a number. |
| Readiness page queue | 130 indexable pages: 76 body-depth reviews and 54 scalable-localization editorial reviews | The queue identifies work for a person; it is not a set of policy violations. |
| Phase 3 review priorities | P1: 76 · P2: 739 · P3: 191 | These priorities cover all 1,006 indexable pages. Recorded human editorial, native-language, source-fact, and external-similarity reviews completed: **0**. |
| Course inventory | 1,069 course files: 196 pass and 873 require review in the readiness audit | A machine pass is not independent linguistic or pedagogical verification. |
| Language/course release gate | `BLOCKED`: 690 baseline-indexable language-related URLs map to failing language profiles; course health separately lists 90 reviewer gaps and 124 unverified source references across 40 languages | Repository release gates, not Google's findings. These counts overlap other queues and do not authorize indexation changes. |
| Static technical inventory | 0 broken links; 0 indexable/sitemap mismatches; 0 `noindex` pages in the sitemap; 0 canonical mismatches | These are repository checks only. Phase 2 has live HTTP status pending for all 2,721 pages. |
| Ad policy | 504 pages are marked/eligible to load the AdSense loader under the repository policy | The loader gate is code-checked; placement, consent, rendered mobile behavior, and account configuration still need review. Ad serving remains disabled in `js/monetization.js`. |
| Publisher configuration | `ads.txt`, publisher-ID consistency, duplicate-loader, and page-class checks pass locally | This does not verify the live domain, AdSense account, a certified CMP, Auto ads settings, or approval. Consent and account-format status remain `REVIEW_REQUIRED`; approval is `NOT_ASSESSED`. |

Current machine-readable evidence:

- `data/quality/adsense-readiness.json`
- `data/quality/full-page-inventory.json`
- `data/quality/phase2-content-inventory.json`
- `data/quality/phase3-originality-audit.json`
- `data/quality/language-gate.json`
- `data/quality/course-health.json`
- `data/monetization/google-monetization.json`

### How to interpret the page reviews

The 76 under-threshold pages are review candidates, not automatically bad
pages. Check each page against its actual learning task: whether it provides
useful original instruction, examples, practice, answers or guidance, and
whether language claims and facts are sound. Improve a page only where a
specific learner need is unmet; do not pad text to satisfy an automated count.

The remaining 54 indexable page reviews concern scalable country/language
localization and need editorial confirmation that the localized details are
accurate and useful. Phase 3 flags all 1,006 indexable pages for some level of
priority review; its automated similarity signals are not proof of copying or
originality. Human review is still unrecorded.

**Do not change `noindex`, canonical, or domain status based on these counts.**
Those changes require the site owner's permission and a separate page-level
indexation decision. Keep Googlebot and human-visible content aligned.

## Remaining work before a resubmission decision

1. **Review the 76 P1 learning pages.** Record the named reviewer, date, page,
   language, evidence/source checks, and outcome. Make content changes only
   when they add genuine learner value. If a page should not be indexed, raise
   that as an owner decision; do not change its robots or canonical here.
2. **Continue the broader editorial queue.** Review the 739 P2 and 191 P3 pages
   for originality, accuracy, localization, and fit to user intent. The audit
   currently records no completed human, native-language, source-fact, or
   external-similarity checks.
3. **Clear the language/course release-gate findings.** `data/quality/language-gate.json`
   reports `BLOCKED`, with 690 baseline-indexable language-related URLs tied to
   failing profiles. `data/quality/course-health.json` separately records 90
   reviewer gaps and 124 unverified source references across 40 languages; the
   counts overlap other queues. Obtain named, digest-bound native/editorial
   review and verify sources. These are not instructions to remove or
   deindex existing pages.
4. **Complete course review.** Triage the 873 course files still marked for
   review. Resolve known Telugu C1/C2 practice-coverage gaps (12/28 and 12/32
   practice types respectively) through subject-matter review, not automatic
   expansion.
5. **Review language and profile warnings.** Malayalam romanization/script
   presentation needs human review. Three tutor drafts—Hemlata, Sarshtee
   Baliyan, and Tara—remain outside the tutor registry; do not present them as
   verified profiles.
6. **Run a production crawl and visual review.** Check HTTP status, redirects,
   canonical and robots behavior, rendered page content, ad placement, consent,
   mobile layouts, keyboard/accessibility behavior, and page performance on the
   live domain. The repository inventory currently has 2,721 HTTP checks
   pending.
7. **Verify account-side settings.** Confirm the actual site status and notice
   in AdSense; verify domain ownership and live `ads.txt`; configure and test a
   Google-certified CMP/IAB TCF and regional privacy messages where applicable;
   verify Auto ads formats, exclusions, and ad load; and confirm any payment or
   tax requirements in the account. These cannot be established from source
   code.
8. **Make the resubmission decision only after review.** Recheck the production
   site and the owner-controlled account configuration. No automated audit in
   this repository can predict Google's outcome.

## Optional short note for the review request

Fill the brackets only with changes verified on the live site and settings
confirmed in the owner's AdSense account; do not send the placeholders:

> EkGuru is a free Hindi-learning site. Since the previous review, we have
> [briefly list site-side changes verified in production]. Our consent/privacy
> and ad-format settings are [state only what was confirmed in the account].
> Please review the current site.

A concise request does not substitute for improving the site or completing
account-side setup. Remove any statement that cannot be independently confirmed.

## Repository checks

```bash
python3 tools/audit-adsense-readiness.py --selftest
python3 tools/audit-adsense-readiness.py
python3 tools/build-full-page-inventory.py --check
python3 tools/build-phase2-content-inventory.py --check
python3 tools/test-phase2-content-inventory.py
python3 tools/build-phase3-originality-audit.py --check
python3 tools/build-all.py check
```

`tools/adsready.js --local` checks repository-side publisher configuration;
without `--local`, it attempts live checks and requires network access. Neither
mode predicts AdSense approval.
