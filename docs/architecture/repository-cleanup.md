# Approved repository cleanup — implementation and verification

## Scope and execution boundary

Snapshot verified before changes: branch `arena/5aa71e50-ekguru`, HEAD
`d9aeb63316f780bcc686a65655f09be06c8ea5a3`, clean working tree.
This pass implements only documentation/archive organization, test organization,
and publishing-boundary safeguards. **No commit, push, PR, merge or deployment.**
No framework rewrite, dependency installation, lockfile change, content-source
migration or generator relocation. The working branch and HEAD remain unchanged.

The original read-only audit counted 6,599 tracked files. This migration preserves
all 197 relocated files: 152 tests, 14 root Markdown reports, 2 root patches,
2 text fragments, 24 research files and 3 historical Arena files. Renames are
filesystem changes left unstaged for review. Original SHA-256 values are recorded
in `cleanup-path-map.json`; original content remains available at the audit commit.
Only path/reference adaptations are made in the relocated historical evidence.

## Final folder tree (implemented portions)

```text
EkGuru/
├── .github/workflows/              # Same workflow names/deployment architecture
├── docs/
│   ├── ARCHITECTURE.md             # Authoritative path retained, current-scope note
│   ├── HANDOVER-FOR-AI.md          # Historical operational statements clearly labelled
│   ├── architecture/
│   │   ├── repository-cleanup.md
│   │   ├── cleanup-path-map.json
│   │   └── cleanup-reference-changes.json
│   ├── audits/legacy/
│   │   ├── [14 historical Markdown reports]
│   │   ├── patches/                # 2 historical root patches
│   │   └── patch-fragments/        # 2 _as2 fragments
│   ├── commands/legacy-arena/01a0e655-ekguru/
│   │   ├── session-note.txt
│   │   ├── after-fasst.md
│   │   └── read-firsst.md
│   ├── research/                   # 24 relocated research files
│   ├── decisions/                  # Existing decisions retained
│   └── marketing/                  # All assets/evidence retained
├── tests/
│   ├── README.md
│   ├── unit/                       # 4 original tests + 1 new layout guard
│   ├── integration/                # 27 original tests
│   ├── regression/                 # 116 original tests
│   ├── e2e/                        # 5 original browser suites
│   └── fixtures/                   # 4 original TSV files, unchanged
├── tools/                         # Generators/content stay; selected thin launchers
├── src/runtime/voice.js            # Unchanged
├── apps-script/                    # Sources/artifact unchanged; setup-doc refs updated
├── server/                        # Unchanged
├── data/                          # All existing bytes/paths preserved
├── js/ css/ images/                # All existing bytes/paths preserved
├── learn/ languages/ tutor/ ...    # All public route folders preserved
└── root public routes/discovery files unchanged
```

No empty placeholder `generators/`, `integrations/`, `config/`, `scripts/`,
`src/content/` or `src/styles/` directories were introduced. The redundant old
Arena-folder nesting was removed by relocating its three files, not dropping them.

## Publishing safeguards

`tools/build-public-dist.py` still builds `_site/`; `.github/workflows/pages.yml`
is unchanged. `PRIVATE_DIRS` now also excludes `generators`, `integrations`,
`config`, `scripts`, `_site` and `.artifacts`. The HTML private-reference check
also recognizes the new internal root names. The public-surface regression adds
these exclusions without dropping its original root-report exclusion assertion.

The new unit guard creates hostile sentinel files inside internal folders in a
temporary fixture and exercises the real copy function. No internal sentinel may
be published; root discovery files, public JS and a sample learning route must
remain present. It also checks all 197 destinations, 152 original test bodies,
compatibility entrypoints and package/CI/master-build test command targets.

## Public URL and generated output verification

The baseline publishing rules classify **5,501** source files as public. After
cleanup there are **5,499**, with exactly these approved archival removals:

- `join-form-full-width.patch`
- `join-responsive-width-fix.patch`

They were old developer patch downloads, not website routes/assets. No claim of
an entirely identical file set is made: these two deliberate removals are the only
exceptions. **All 5,499 retained public files are byte-identical; zero new public
files.** This includes every public HTML page, JS/CSS/image/data asset, all sitemap
files, robots, ads.txt, CNAME, .nojekyll, service worker, manifest and llms files.
The isolated copy also had zero changed retained public files after build/tests.

The full artifact check passed with all **1,576 sitemap URLs** resolving and no
private-path failures. No SEO indexing baseline, publication contract, consent,
AdSense implementation, payment backend, form/feed backend, booking, intake,
Sheets behavior, Telegram gateway or voice source/generated relationship changed.

## References and configuration

- `package.json`: canonical test commands now point to `tests/`; description updated.
  Dependency declarations are unchanged and `package-lock.json` is byte-identical.
- `tools/build-all.py`: test registrations use the new locations; the new layout
  guard is registered. Generation order is unchanged.
- `.github/workflows/ci.yml` and `sheet-sync.yml`: test command paths updated.
  Pages, live-guard, course-health and Playwright workflow architecture are unchanged.
- `playwright.config.mjs`: `testDir` is `tests/e2e`; `testMatch` still selects only
  `test-journeys.mjs`; base URL and web-server behavior are unchanged.
- Relocated tests: repository roots, `import.meta.url`, `import.meta.dirname`,
  `createRequire`, `__dirname`, Python `__file__`/`sys.path`, sibling module imports,
  schema imports, subprocess paths and fixture lookup paths adapted to the new depth.
- Email security scanner: the existing non-production `test-*` placeholder-token
  exemption follows the moved test directories as well as old tool launchers.
  Production-source token assertions and checks are retained.
- Browser fixture URLs in the drawer test remain unchanged; they are not filesystem
  import paths. The original public-surface root-report assertion is retained.
- `tools/build-inventory.py`: internal research report destination is now
  `docs/research`; existing public metadata/provenance bytes are not regenerated.
- Internal documentation, reports and command references are updated. The complete
  per-existing-file change inventory, including checksums, is in
  `cleanup-reference-changes.json`.

Protected public files and Apps Script sources cite some old test commands. Their
bytes are intentionally preserved. **22 thin compatibility entrypoints** at those
old tool paths forward to canonical test files; no assertions are duplicated in
the launchers. Public research metadata retains historical source-location strings;
`cleanup-path-map.json` provides the explicit old-to-new crosswalk. Those strings
are not asserted to be newly generated/current source paths.

## Checks actually executed

Write-capable checks ran in the isolated filesystem copy at
`.cache/restructure-qa/worktree/`; no generated outputs were copied back. Existing
installed Node dependencies were reused without installation. Baseline hashes,
logs and the isolated copy are excluded QA artifacts, not deployment assets.
The master build check passed twice; after final documentation sync the layout
guard, public-surface gate and artifact check were rerun successfully.

| Check | Result |
|---|---|
| Syntax: every one of the 152 relocated original test files | PASS |
| Assertion-count comparison across all 152 originals | No counted assertions removed |
| JS literal relative import/file-URL target scan | No missing target |
| `python3 tools/build-all.py check` | PASS in isolated copy |
| `npm test` | PASS in isolated copy |
| `npm run test:courses` | PASS |
| `npm run test:learners` | PASS |
| `npm run test:advertising` | PASS |
| `npm run test:contract` | PASS |
| `npm run test:analytics` | PASS |
| `npm run test:home` | PASS |
| `npm run test:monetization` | PASS |
| Original Apps Script health-classifier unit tests | 3 PASS |
| Original root ads.txt artifact fixture tests | 2 PASS |
| Original sitemap freshness unit tests | 3 PASS; intentional negative fixtures remain negative |
| New repository-layout/sentinel guard | 4 PASS |
| Offline data-source fixture mode | 21 checks, 0 failures; external health deliberately not exercised |
| Shared Sheet-fetch fixture tests | 35 checks, 0 failures |
| Extra 19 local integration/regression suites | PASS after path adaptations |
| Real-life booking/review integration | 38 PASS, included in extra suites |
| Real-life Sheet cycle integration | 167 PASS, included in extra suites |
| Googlebot/Chrome local response parity | 15 pages PASS, included in extra suites |
| Public-surface gate, final targeted rerun | 48 PASS |
| Root ads-policy compatibility launcher | 27 PASS |
| Public artifact check | 5,499 files; 1,576 sitemap URLs; PASS |
| Before/after public hashes and protected-code comparison | No retained public/protected code differences |
| `git diff --check` | PASS at final verification |
| Complete patch: `git apply --check --cached` against unchanged baseline index | PASS; read-only check, no staging |

Initial execution exposed relocated schema/root imports and a moved placeholder
fixture exemption; those were corrected without removing assertions. One real-life
Sheet-cycle attempt hit an 80-second harness limit; rerunning that suite alone
with sufficient time completed in about 84 seconds, 167 passed/0 failed. Initial
failed/timeout attempts are not counted as passes. They remain visible in the QA logs.

Successfully invoked **121 distinct original test files**, plus the new
layout guard. All 152 originals were syntax-checked; **not every original suite
was executed**. Browser and live-service claims are deliberately limited.

### Continuation validation — six additional local suites

Four additional original suites passed: Hindi audio, Hindi learning features,
Hindi quizzes and Phase 7 registries. The combined successful original-suite
count is now **121**. In total 123 original files were invoked; the two diagnostics
below are **not** counted as successful gates. 29 original suites remain unexecuted.

- `tests/regression/test-phase6-seo.py`: exit 0 but its JSON report has `pass:false`
  and 28 missing-description/canonical messages affecting 14 pages. Its regex
  requires a specific attribute order. Independent HTMLParser inspection confirms
  both fields exist on all 14 pages. This is a legacy test diagnostic failure,
  not a demonstrated metadata regression. Assertions and exit behavior were not
  changed in this cleanup.
- `tests/regression/test-phase7c-seo-scale.py`: exit 0, but no pass/fail contract.
  Its report records 3,002 pages, 0 broken links, one duplicate-title group,
  14 canonical differences and 1,066 orphans under its legacy traversal/model.
  These raw counts are not proof of new defects or successful SEO acceptance;
  aliases/noindex policy and current inventory require separate reconciliation.
- Each of the six original scripts from the unchanged audit commit was also run
  at its original tool location in the isolated copy. Report data matched the
  relocated version exactly after ignoring generation timestamps. No original
  source test or production file was overwritten in the working repository.
- The 5,499 retained public files were re-hashed and remain byte-identical.

Detailed excluded evidence: `.cache/restructure-qa/continuation-validation.json`,
`legacy-seo-parser-verification.json`, and `continue-*.log` / `baseline-*.log`.
This does not authorize legacy test hardening, content/generator migration,
commit, push or deployment.

### Unexecuted checks / remaining verification boundary

The five Playwright journeys were not run: `@playwright/test` is not installed in
this checkout. Its existing CI workflow installs it separately. No dependency was
installed for this cleanup, and an existing browser suite's skip is not claimed
as a browser pass. Python browser suites, real email sending, payment provider
calls, live Google endpoints and production deployment were not verified.

Original suites not invoked in this pass:

- `tests/e2e/test-hindi-learning-browser.py`
- `tests/e2e/test-join-buttons-browser.mjs`
- `tests/e2e/test-journeys.mjs`
- `tests/e2e/test-release-browser.py`
- `tests/e2e/test-tools-browser.py`
- `tests/integration/test-email-e2e.py`
- `tests/integration/test-email-live.js`
- `tests/integration/test-sheet-loader.js`
- `tests/regression/test-card-interactions.py`
- `tests/regression/test-header-geometry.py`
- `tests/regression/test-hindi-offline.py`
- `tests/regression/test-idle-parallel.py`
- `tests/regression/test-idle-regression.py`
- `tests/regression/test-idle-scenarios.py`
- `tests/regression/test-phase6-matrix.py`
- `tests/regression/test-phase7-browser.py`
- `tests/regression/test-phase7c-admin.py`
- `tests/regression/test-phase7c-context.py`
- `tests/regression/test-phase7c-conversation.py`
- `tests/regression/test-phase7c-engines.py`
- `tests/regression/test-phase7c-langpack.py`
- `tests/regression/test-phase7c-langs.py`
- `tests/regression/test-phase7c-stage6.py`
- `tests/regression/test-phase7c-stage7.py`
- `tests/regression/test-phase7c-starter.py`
- `tests/regression/test-phase7c-viewports.py`
- `tests/regression/test-phase7c.py`
- `tests/regression/test-recovery.py`
- `tests/regression/test-tools-functional.py`

## Files deliberately retained / next phases

All 133 content files in the eight audited `tools/` subtrees remain at their
original paths. All generators remain in `tools/`; only necessary reference/output
path adaptations were made. Runtime assets, duplicate-looking logos/icons, marketing
videos, large reports, fixtures, indexing contracts, native-review evidence and
separate Apps Script deployment sources/artifacts are retained. No files were
approved as unnecessary deletion candidates.

Future approval is required for source/template separation, generator/shared-library
migration, source/generated data separation, integration project retirement or any
hosting/output change. Do not run the old proposed bulk migration from the historic
architecture section automatically.

## Complete move mapping

The machine-readable authoritative list is `cleanup-path-map.json`. The original
checksum and compatibility flag accompany every entry there.

| Old path | New path |
|---|---|
| `A1-A2-REMEDIATION-REPORT.md` | `docs/audits/legacy/A1-A2-REMEDIATION-REPORT.md` |
| `Arena latest command  arena/01a0e655-ekguru` | `docs/commands/legacy-arena/01a0e655-ekguru/session-note.txt` |
| `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/after fasst.md` | `docs/commands/legacy-arena/01a0e655-ekguru/after-fasst.md` |
| `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/read firsst.md` | `docs/commands/legacy-arena/01a0e655-ekguru/read-firsst.md` |
| `BUTTONS-BUGFIX-REPORT.md` | `docs/audits/legacy/BUTTONS-BUGFIX-REPORT.md` |
| `CONSOLIDATION-INSPECTION-BLOCKED.md` | `docs/audits/legacy/CONSOLIDATION-INSPECTION-BLOCKED.md` |
| `CONSOLIDATION-REPORT.md` | `docs/audits/legacy/CONSOLIDATION-REPORT.md` |
| `DEFECT-FIXES-REPORT.md` | `docs/audits/legacy/DEFECT-FIXES-REPORT.md` |
| `FINAL-IMPLEMENTATION-REPORT.md` | `docs/audits/legacy/FINAL-IMPLEMENTATION-REPORT.md` |
| `FINAL-READONLY-QA-REPORT.md` | `docs/audits/legacy/FINAL-READONLY-QA-REPORT.md` |
| `FINAL-VERIFICATION-REPORT.md` | `docs/audits/legacy/FINAL-VERIFICATION-REPORT.md` |
| `FINAL_REPORT.md` | `docs/audits/legacy/FINAL_REPORT.md` |
| `PREFLIGHT-AUDIT.md` | `docs/audits/legacy/PREFLIGHT-AUDIT.md` |
| `REAL-LIFE-TEST-REPORT.md` | `docs/audits/legacy/REAL-LIFE-TEST-REPORT.md` |
| `RESPONSIVE-AUDIT-join.md` | `docs/audits/legacy/RESPONSIVE-AUDIT-join.md` |
| `U0-ACCEPTANCE-REPORT.md` | `docs/audits/legacy/U0-ACCEPTANCE-REPORT.md` |
| `VISUAL-QA-REPORT.md` | `docs/audits/legacy/VISUAL-QA-REPORT.md` |
| `join-form-full-width.patch` | `docs/audits/legacy/patches/join-form-full-width.patch` |
| `join-responsive-width-fix.patch` | `docs/audits/legacy/patches/join-responsive-width-fix.patch` |
| `research/china-language-inventory.md` | `docs/research/china-language-inventory.md` |
| `research/country-language-summary.md` | `docs/research/country-language-summary.md` |
| `research/ethiopia-language-inventory.md` | `docs/research/ethiopia-language-inventory.md` |
| `research/global-language-inventory.md` | `docs/research/global-language-inventory.md` |
| `research/hindi-a1-c2-cefr-blueprint.md` | `docs/research/hindi-a1-c2-cefr-blueprint.md` |
| `research/hindi-a1-c2-ekguru-product-spec.md` | `docs/research/hindi-a1-c2-ekguru-product-spec.md` |
| `research/hindi-a1-c2-platform-comparison.md` | `docs/research/hindi-a1-c2-platform-comparison.md` |
| `research/hindi-a1-c2-platform-study.md` | `docs/research/hindi-a1-c2-platform-study.md` |
| `research/hindi-practice-quiz-worksheet-blueprint.md` | `docs/research/hindi-practice-quiz-worksheet-blueprint.md` |
| `research/india-language-inventory.md` | `docs/research/india-language-inventory.md` |
| `research/indonesia-language-inventory.md` | `docs/research/indonesia-language-inventory.md` |
| `research/iran-language-inventory.md` | `docs/research/iran-language-inventory.md` |
| `research/language-data-sources.md` | `docs/research/language-data-sources.md` |
| `research/language-inventory-report.json` | `docs/research/language-inventory-report.json` |
| `research/language-research-limitations.md` | `docs/research/language-research-limitations.md` |
| `research/malaysia-language-inventory.md` | `docs/research/malaysia-language-inventory.md` |
| `research/nigeria-language-inventory.md` | `docs/research/nigeria-language-inventory.md` |
| `research/papua-new-guinea-language-inventory.md` | `docs/research/papua-new-guinea-language-inventory.md` |
| `research/philippines-language-inventory.md` | `docs/research/philippines-language-inventory.md` |
| `research/russia-language-inventory.md` | `docs/research/russia-language-inventory.md` |
| `research/south-africa-language-inventory.md` | `docs/research/south-africa-language-inventory.md` |
| `research/thailand-language-inventory.md` | `docs/research/thailand-language-inventory.md` |
| `research/turkey-language-inventory.md` | `docs/research/turkey-language-inventory.md` |
| `research/vietnam-language-inventory.md` | `docs/research/vietnam-language-inventory.md` |
| `tools/_as2_patch.txt` | `docs/audits/legacy/patch-fragments/_as2_patch.txt` |
| `tools/_as2_patch2.txt` | `docs/audits/legacy/patch-fragments/_as2_patch2.txt` |
| `tools/test-ad-policy.mjs` | `tests/regression/test-ad-policy.mjs` |
| `tools/test-adaptive-practice.js` | `tests/regression/test-adaptive-practice.js` |
| `tools/test-adsense-publisher-tags.py` | `tests/regression/test-adsense-publisher-tags.py` |
| `tools/test-adsready-diagnostics.mjs` | `tests/regression/test-adsready-diagnostics.mjs` |
| `tools/test-advertising-launch.mjs` | `tests/regression/test-advertising-launch.mjs` |
| `tools/test-affiliate-disclosure.mjs` | `tests/regression/test-affiliate-disclosure.mjs` |
| `tools/test-analytics-lifecycle.mjs` | `tests/regression/test-analytics-lifecycle.mjs` |
| `tools/test-answer-first-pages.py` | `tests/regression/test-answer-first-pages.py` |
| `tools/test-application-backend.mjs` | `tests/integration/test-application-backend.mjs` |
| `tools/test-application-pipeline.mjs` | `tests/integration/test-application-pipeline.mjs` |
| `tools/test-apps-script.mjs` | `tests/integration/test-apps-script.mjs` |
| `tools/test-appscript-health.py` | `tests/unit/test-appscript-health.py` |
| `tools/test-book-mode.mjs` | `tests/regression/test-book-mode.mjs` |
| `tools/test-browser-qa.mjs` | `tests/regression/test-browser-qa.mjs` |
| `tools/test-card-interactions.py` | `tests/regression/test-card-interactions.py` |
| `tools/test-combined-code.mjs` | `tests/integration/test-combined-code.mjs` |
| `tools/test-consent-persistence.mjs` | `tests/regression/test-consent-persistence.mjs` |
| `tools/test-consent-release.mjs` | `tests/regression/test-consent-release.mjs` |
| `tools/test-contextual-entry-links.py` | `tests/regression/test-contextual-entry-links.py` |
| `tools/test-copy-index.mjs` | `tests/regression/test-copy-index.mjs` |
| `tools/test-country-phrase-consolidation.py` | `tests/regression/test-country-phrase-consolidation.py` |
| `tools/test-country-visuals.mjs` | `tests/regression/test-country-visuals.mjs` |
| `tools/test-course-country.mjs` | `tests/regression/test-course-country.mjs` |
| `tools/test-course-levels.mjs` | `tests/regression/test-course-levels.mjs` |
| `tools/test-course-matching.mjs` | `tests/regression/test-course-matching.mjs` |
| `tools/test-course-placeholders.mjs` | `tests/regression/test-course-placeholders.mjs` |
| `tools/test-course-reorder.mjs` | `tests/regression/test-course-reorder.mjs` |
| `tools/test-course-voice-buttons.py` | `tests/regression/test-course-voice-buttons.py` |
| `tools/test-daily-hindi-future-content.py` | `tests/regression/test-daily-hindi-future-content.py` |
| `tools/test-data-sources.py` | `tests/integration/test-data-sources.py` |
| `tools/test-defect-regressions.mjs` | `tests/regression/test-defect-regressions.mjs` |
| `tools/test-discovery-integrity.py` | `tests/unit/test-discovery-integrity.py` |
| `tools/test-email-e2e.py` | `tests/integration/test-email-e2e.py` |
| `tools/test-email-live.js` | `tests/integration/test-email-live.js` |
| `tools/test-email-security.js` | `tests/integration/test-email-security.js` |
| `tools/test-email-system.js` | `tests/integration/test-email-system.js` |
| `tools/test-experience-dom.mjs` | `tests/regression/test-experience-dom.mjs` |
| `tools/test-flashcards.mjs` | `tests/regression/test-flashcards.mjs` |
| `tools/test-googlebot-parity.mjs` | `tests/regression/test-googlebot-parity.mjs` |
| `tools/test-header-geometry.py` | `tests/regression/test-header-geometry.py` |
| `tools/test-hindi-audio.py` | `tests/regression/test-hindi-audio.py` |
| `tools/test-hindi-foundation-depth.py` | `tests/regression/test-hindi-foundation-depth.py` |
| `tools/test-hindi-hunger-answer-content.py` | `tests/regression/test-hindi-hunger-answer-content.py` |
| `tools/test-hindi-learning-browser.py` | `tests/e2e/test-hindi-learning-browser.py` |
| `tools/test-hindi-learning-features.py` | `tests/regression/test-hindi-learning-features.py` |
| `tools/test-hindi-learning-library.mjs` | `tests/regression/test-hindi-learning-library.mjs` |
| `tools/test-hindi-offline.py` | `tests/regression/test-hindi-offline.py` |
| `tools/test-hindi-phrase-discovery.py` | `tests/regression/test-hindi-phrase-discovery.py` |
| `tools/test-hindi-quizzes.py` | `tests/regression/test-hindi-quizzes.py` |
| `tools/test-hindi-sentence-lesson.mjs` | `tests/regression/test-hindi-sentence-lesson.mjs` |
| `tools/test-hindi-text-counter.mjs` | `tests/regression/test-hindi-text-counter.mjs` |
| `tools/test-home-practice.mjs` | `tests/regression/test-home-practice.mjs` |
| `tools/test-home-tutor-reveal.mjs` | `tests/regression/test-home-tutor-reveal.mjs` |
| `tools/test-idle-parallel.py` | `tests/regression/test-idle-parallel.py` |
| `tools/test-idle-regression.py` | `tests/regression/test-idle-regression.py` |
| `tools/test-idle-scenarios.py` | `tests/regression/test-idle-scenarios.py` |
| `tools/test-intake-real-life.mjs` | `tests/integration/test-intake-real-life.mjs` |
| `tools/test-intake.js` | `tests/integration/test-intake.js` |
| `tools/test-join-buttons-browser.mjs` | `tests/e2e/test-join-buttons-browser.mjs` |
| `tools/test-join-css-visibility.mjs` | `tests/regression/test-join-css-visibility.mjs` |
| `tools/test-join-wizard-nav.mjs` | `tests/regression/test-join-wizard-nav.mjs` |
| `tools/test-join-wizard.mjs` | `tests/regression/test-join-wizard.mjs` |
| `tools/test-journeys.mjs` | `tests/e2e/test-journeys.mjs` |
| `tools/test-language-course-uniqueness.py` | `tests/regression/test-language-course-uniqueness.py` |
| `tools/test-language-course-voice-controls.py` | `tests/regression/test-language-course-voice-controls.py` |
| `tools/test-learner-trust.mjs` | `tests/regression/test-learner-trust.mjs` |
| `tools/test-learning-storage.mjs` | `tests/regression/test-learning-storage.mjs` |
| `tools/test-learning-worker.mjs` | `tests/regression/test-learning-worker.mjs` |
| `tools/test-level-visuals.mjs` | `tests/regression/test-level-visuals.mjs` |
| `tools/test-live-feed.js` | `tests/integration/test-live-feed.js` |
| `tools/test-live-payment-contract.mjs` | `tests/integration/test-live-payment-contract.mjs` |
| `tools/test-mail-flow.mjs` | `tests/integration/test-mail-flow.mjs` |
| `tools/test-menu-search.mjs` | `tests/regression/test-menu-search.mjs` |
| `tools/test-monetization-disclosures.mjs` | `tests/regression/test-monetization-disclosures.mjs` |
| `tools/test-name-card.mjs` | `tests/regression/test-name-card.mjs` |
| `tools/test-name-page.mjs` | `tests/regression/test-name-page.mjs` |
| `tools/test-name-share-privacy.mjs` | `tests/regression/test-name-share-privacy.mjs` |
| `tools/test-no-competitor-attribution.js` | `tests/regression/test-no-competitor-attribution.js` |
| `tools/test-numbers-page.mjs` | `tests/regression/test-numbers-page.mjs` |
| `tools/test-offline-playable.mjs` | `tests/regression/test-offline-playable.mjs` |
| `tools/test-orphan-tutor-quarantine.mjs` | `tests/regression/test-orphan-tutor-quarantine.mjs` |
| `tools/test-page-layer.mjs` | `tests/regression/test-page-layer.mjs` |
| `tools/test-page-skeleton.mjs` | `tests/regression/test-page-skeleton.mjs` |
| `tools/test-partial-course-publication.py` | `tests/regression/test-partial-course-publication.py` |
| `tools/test-payment-e2e.mjs` | `tests/integration/test-payment-e2e.mjs` |
| `tools/test-phase2-content-inventory.py` | `tests/regression/test-phase2-content-inventory.py` |
| `tools/test-phase3-content.py` | `tests/regression/test-phase3-content.py` |
| `tools/test-phase3-originality-audit.py` | `tests/regression/test-phase3-originality-audit.py` |
| `tools/test-phase5-ekguru-value.py` | `tests/regression/test-phase5-ekguru-value.py` |
| `tools/test-phase6-matrix.py` | `tests/regression/test-phase6-matrix.py` |
| `tools/test-phase6-seo.py` | `tests/regression/test-phase6-seo.py` |
| `tools/test-phase7-browser.py` | `tests/regression/test-phase7-browser.py` |
| `tools/test-phase7-registries.py` | `tests/regression/test-phase7-registries.py` |
| `tools/test-phase7c-admin.py` | `tests/regression/test-phase7c-admin.py` |
| `tools/test-phase7c-context.py` | `tests/regression/test-phase7c-context.py` |
| `tools/test-phase7c-conversation.py` | `tests/regression/test-phase7c-conversation.py` |
| `tools/test-phase7c-engines.py` | `tests/regression/test-phase7c-engines.py` |
| `tools/test-phase7c-langpack.py` | `tests/regression/test-phase7c-langpack.py` |
| `tools/test-phase7c-langs.py` | `tests/regression/test-phase7c-langs.py` |
| `tools/test-phase7c-seo-scale.py` | `tests/regression/test-phase7c-seo-scale.py` |
| `tools/test-phase7c-stage6.py` | `tests/regression/test-phase7c-stage6.py` |
| `tools/test-phase7c-stage7.py` | `tests/regression/test-phase7c-stage7.py` |
| `tools/test-phase7c-starter.py` | `tests/regression/test-phase7c-starter.py` |
| `tools/test-phase7c-viewports.py` | `tests/regression/test-phase7c-viewports.py` |
| `tools/test-phase7c.py` | `tests/regression/test-phase7c.py` |
| `tools/test-photo-fallback.mjs` | `tests/regression/test-photo-fallback.mjs` |
| `tools/test-print-sheet-dom.mjs` | `tests/regression/test-print-sheet-dom.mjs` |
| `tools/test-print-sheets.mjs` | `tests/regression/test-print-sheets.mjs` |
| `tools/test-print-visible.mjs` | `tests/regression/test-print-visible.mjs` |
| `tools/test-public-ads-txt.py` | `tests/unit/test-public-ads-txt.py` |
| `tools/test-public-surface.mjs` | `tests/regression/test-public-surface.mjs` |
| `tools/test-published-vocabulary.py` | `tests/regression/test-published-vocabulary.py` |
| `tools/test-question-api.mjs` | `tests/regression/test-question-api.mjs` |
| `tools/test-razorpay-api.mjs` | `tests/integration/test-razorpay-api.mjs` |
| `tools/test-reading-layer.mjs` | `tests/regression/test-reading-layer.mjs` |
| `tools/test-real-life-booking-review.mjs` | `tests/integration/test-real-life-booking-review.mjs` |
| `tools/test-real-life-sheet-cycle.mjs` | `tests/integration/test-real-life-sheet-cycle.mjs` |
| `tools/test-recovery.py` | `tests/regression/test-recovery.py` |
| `tools/test-refresh-quiet.mjs` | `tests/regression/test-refresh-quiet.mjs` |
| `tools/test-release-browser.py` | `tests/e2e/test-release-browser.py` |
| `tools/test-retention.mjs` | `tests/regression/test-retention.mjs` |
| `tools/test-reviews-fallback.js` | `tests/integration/test-reviews-fallback.js` |
| `tools/test-routing.js` | `tests/integration/test-routing.js` |
| `tools/test-runtime-qa.mjs` | `tests/regression/test-runtime-qa.mjs` |
| `tools/test-script-map.mjs` | `tests/regression/test-script-map.mjs` |
| `tools/test-search-facets.mjs` | `tests/regression/test-search-facets.mjs` |
| `tools/test-seo-runtime.mjs` | `tests/regression/test-seo-runtime.mjs` |
| `tools/test-sheet-apply.js` | `tests/integration/test-sheet-apply.js` |
| `tools/test-sheet-fetch.mjs` | `tests/integration/test-sheet-fetch.mjs` |
| `tools/test-sheet-loader.js` | `tests/integration/test-sheet-loader.js` |
| `tools/test-sheet-only-bake.mjs` | `tests/integration/test-sheet-only-bake.mjs` |
| `tools/test-sheetsync-policy.js` | `tests/integration/test-sheetsync-policy.js` |
| `tools/test-shell-drawer.mjs` | `tests/regression/test-shell-drawer.mjs` |
| `tools/test-sitemap-freshness.py` | `tests/unit/test-sitemap-freshness.py` |
| `tools/test-support-static.mjs` | `tests/regression/test-support-static.mjs` |
| `tools/test-theme-contrast.mjs` | `tests/regression/test-theme-contrast.mjs` |
| `tools/test-time-page.mjs` | `tests/regression/test-time-page.mjs` |
| `tools/test-toolbox-visuals.mjs` | `tests/regression/test-toolbox-visuals.mjs` |
| `tools/test-tools-browser.py` | `tests/e2e/test-tools-browser.py` |
| `tools/test-tools-functional.py` | `tests/regression/test-tools-functional.py` |
| `tools/test-tutor-activation.mjs` | `tests/integration/test-tutor-activation.mjs` |
| `tools/test-tutor-claims.js` | `tests/regression/test-tutor-claims.js` |
| `tools/test-tutor-fixes.mjs` | `tests/regression/test-tutor-fixes.mjs` |
| `tools/test-ultra-integration.py` | `tests/regression/test-ultra-integration.py` |
| `tools/test-usability-home.mjs` | `tests/regression/test-usability-home.mjs` |
| `tools/test-voice-mounted-controls.mjs` | `tests/regression/test-voice-mounted-controls.mjs` |
| `tools/test-voice-page-coverage.py` | `tests/regression/test-voice-page-coverage.py` |
| `tools/test-voice-ux.mjs` | `tests/regression/test-voice-ux.mjs` |
| `tools/test-voice.mjs` | `tests/regression/test-voice.mjs` |
| `tools/test-wizard-sheets-e2e.mjs` | `tests/integration/test-wizard-sheets-e2e.mjs` |
| `tools/test-world-course-numbers-content.py` | `tests/regression/test-world-course-numbers-content.py` |
| `tools/test-world-course-quiz-content.py` | `tests/regression/test-world-course-quiz-content.py` |

## Compatibility entrypoints retained

- `tools/test-ad-policy.mjs` → `tests/regression/test-ad-policy.mjs`
- `tools/test-adaptive-practice.js` → `tests/regression/test-adaptive-practice.js`
- `tools/test-affiliate-disclosure.mjs` → `tests/regression/test-affiliate-disclosure.mjs`
- `tools/test-application-backend.mjs` → `tests/integration/test-application-backend.mjs`
- `tools/test-copy-index.mjs` → `tests/regression/test-copy-index.mjs`
- `tools/test-course-levels.mjs` → `tests/regression/test-course-levels.mjs`
- `tools/test-email-security.js` → `tests/integration/test-email-security.js`
- `tools/test-email-system.js` → `tests/integration/test-email-system.js`
- `tools/test-join-css-visibility.mjs` → `tests/regression/test-join-css-visibility.mjs`
- `tools/test-join-wizard-nav.mjs` → `tests/regression/test-join-wizard-nav.mjs`
- `tools/test-join-wizard.mjs` → `tests/regression/test-join-wizard.mjs`
- `tools/test-live-feed.js` → `tests/integration/test-live-feed.js`
- `tools/test-question-api.mjs` → `tests/regression/test-question-api.mjs`
- `tools/test-reviews-fallback.js` → `tests/integration/test-reviews-fallback.js`
- `tools/test-routing.js` → `tests/integration/test-routing.js`
- `tools/test-sheet-fetch.mjs` → `tests/integration/test-sheet-fetch.mjs`
- `tools/test-sheet-only-bake.mjs` → `tests/integration/test-sheet-only-bake.mjs`
- `tools/test-support-static.mjs` → `tests/regression/test-support-static.mjs`
- `tools/test-theme-contrast.mjs` → `tests/regression/test-theme-contrast.mjs`
- `tools/test-tools-functional.py` → `tests/regression/test-tools-functional.py`
- `tools/test-tutor-activation.mjs` → `tests/integration/test-tutor-activation.mjs`
- `tools/test-usability-home.mjs` → `tests/regression/test-usability-home.mjs`

## Complete diff and change inventory

- All moves: `docs/architecture/cleanup-path-map.json`.
- Every modified existing file/reference: `docs/architecture/cleanup-reference-changes.json`.
- Full review patch, including untracked new files (not just `git diff`'s tracked-file
  subset): `.cache/restructure-qa/complete-cleanup.diff`.
- Focused original-to-relocated test edits: `.cache/restructure-qa/relocated-test-edits.diff`.
- Detailed logs and before/after public hashes: `.cache/restructure-qa/`.

The patch and isolated-copy artifacts are deliberately not added to the repository.
No staging/commit/push/merge/PR/deployment was performed.
