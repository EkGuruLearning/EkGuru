# Approved two-script CSS build-system migration

## Scope and approval

This phase implements only the eight paths registered in
`build-system-path-map.json`, starting from current worktree commit
`3c671e9be32cde6833948bcec219a426dbfe6731` on
`arena/5aa71e50-ekguru`. No other generators, content modules, source banks,
integrations, runtime assets or publication directories move.

```text
tools/
  bundle-experience-css.py          # legacy CLI/Python API adapter
  build-dark-fix.py                 # legacy CLI/Python API adapter
  pipeline/assets/
    bundle-experience-css.py        # canonical processor
    build-dark-fix.py               # canonical processor
```

The other four approved paths are the additive unit test, this document, the
phase-specific registry, and one additive offline CI step. Existing commands,
including bundle-before-dark ordering in `tools/build-all.py`, remain unchanged.
The completed cleanup registry and all 22 existing test launchers stay intact.

## Implementation and API contract

The canonical implementations retain their original bytes except one ROOT
assignment apiece. Reversing that assignment must reproduce the registered
original SHA-256 exactly; no CSS algorithm, source list, threshold, marker,
whitespace formatting, diagnostic message or CLI argument behavior changes.

- The bundler derives ROOT with **four** `os.path.dirname()` operations around
  `os.path.abspath(__file__)`. ROOT remains a string, and import still performs
  `os.chdir(ROOT)`. From `tools/pipeline/assets/<file>`, the four dirname results
  are assets → pipeline → tools → repository.
- Dark-fix uses `Path(__file__).resolve().parents[3]`. ROOT remains Path-valued;
  importing it does not change the caller's current directory.
- Each adapter compiles canonical bytes with `dont_inherit=True` and executes
  them in its own module globals. A `try/finally` restores the caller's legacy
  `__file__`, including normal import, SystemExit, runtime/compile errors and
  failures reading canonical bytes. Temporary adapter names are removed.
- Exported functions retain that module's globals dictionary; monkeypatching
  ROOT, SRC, BUNDLE, SOURCES, markers or functions continues to affect execution.
  CLI, importlib file loads and runpy default/custom/main names are covered.
  Function code locations identify the new canonical implementation, as expected
  for moved code; legacy module `__file__`/name/spec are not replaced with a
  separately imported module. There is no subprocess-only/main-only shim and no
  second maintained copy of either implementation.

## Acceptance: preserve behavior, not a new algorithmic property

The original processors document **individual** idempotence. The new suite
checks each independently with controlled inputs and no intervening generator.
It executes the registered original processor as well as both migrated paths.

The untouched baseline can add a separator newline on the second combined
bundle → dark-fix pass. Individual idempotence does not establish composition
idempotence when another generator changes the shared input between calls.
The accepted migration contract is byte-for-byte equality **between baseline
and candidate at each corresponding checkpoint**, not equality between combined
pass one and pass two. No newline normalization or allowed-output-difference
list is used. The known separator behavior is preserved, not repaired here.

The earlier isolated prototype transcript remains **17 PASS / 1 FAIL**. Its
SHA-256 is
`1e48d34fa8af6259b65fe8257a02dca02a515aa4eb4a7fce94222b0e70bdbaf9`.
It is retained as external evidence, not relabelled as a passing run or added as
a ninth checkout file. The final suite has its own transcript and count.

## Offline compatibility test and CI

```sh
python3 -B tests/unit/test-build-system-compatibility.py
```

The additive CI step runs this command immediately before the existing master
check; no existing step, dependency, gate or assertion is changed. The suite
uses only the standard library, small repository-shaped temporary paths with
spaces, and copied scripts/controlled CSS and JS input fixtures. It does not
run a full build, access services, or write working-tree CSS. Negative controls
use an existing but incorrect directory to ensure ROOT tests check the exact
value and type rather than merely existence.

For baseline checks the test reconstructs the registered pre-move bytes by
reversing only the canonical ROOT assignment, verifies the original SHA-256,
and writes them to temporary legacy paths. There is no duplicate baseline
implementation checked into the repository. Both ordered passes compare full
output bytes, process exits and stdout/stderr at all four checkpoints.

## Publisher and public-file protection

`tools/build-public-dist.py`, `_site/`, `.github/workflows/pages.yml`, public
HTML/assets/URLs, robots, sitemaps, service worker, runtime/voice and integrations
are unchanged. Both canonical files are beneath the publisher's already
private `tools/` ancestor. No root `build/` tree or publisher-rule change is
introduced. The registry/document/test files remain in existing private trees.

Validation must use pristine baseline/candidate copies of the current worktree,
not only HEAD or a different branch. Execute the actual publisher commands in
those isolated copies, retain their artifacts and logs, compare every public
path/hash, and validate sitemap/precache/private references with the unchanged
publisher. Also execute the existing offline discovery-reference audit. Never
replace artifact generation with syntax checks or merely assume equal inputs
mean a successful publisher check.

## Inventory accounting

The earlier audit hashed **6,627** existing regular files from the unique union
of tracked and nonignored untracked paths (`git ls-files -co
--exclude-standard -z`). The pre-migration inventory is **6,628** because commit
`3c671e9be32cde6833948bcec219a426dbfe6731` added exactly
`docs/architecture/EkGuru-Build-System-Audit.zip`. The archive is private under
`docs/` and does not add a public page. No file was lost or counted twice.

The shared `js/tutors/_overrides.js` hash also differs from the earlier audit
because the upstream main Sheet refresh was retained during the preceding
merge; that is a content-hash difference, not a count difference. This phase
preserves its current pre-migration bytes. There remain **5,499 retained public
files**. The final migration introduces five private files in addition to the
three modified tracked files; inventory changes must match that exact allowlist.
Ignored dependencies/caches, isolated artifacts and Git internals are not part
of the regular-file inventory.

## Rollback

Restore each legacy processor from its captured pre-move bytes only after
checking for concurrent edits; its original SHA-256 is registered. Remove only
the corresponding new canonical file and this phase's approved additive test,
registry/document and CI step. Do not restore from a different commit, reset,
stash, clean, switch branches or overwrite earlier cleanup/SEO work. Public
outputs are not part of the patch and must not be copied back from generator
experiments. No Git publication/deployment is authorized by this document.

## Validation record

Results are recorded below only after execution. PASS means an actually run
applicable check, FAIL remains visible, and NOT RUN is not inferred from syntax
or process status. Full transcripts, complete patch and public hash inventories
are delivered as external evidence rather than added outside the eight paths.

### Executed local validation results

All execution below used isolated baseline/candidate copies, Python 3.11.2 and
Node 22.22.3. Existing node_modules were reused; no dependency was installed.
Outbound network operations were denied by the validation harness, with zero
network attempts recorded. No existing test assertion or lockfile changed.

| Check | Baseline | Migrated candidate |
|---|---|---|
| New compatibility suite | Not applicable | **20 tests PASS**, about 2 seconds |
| Existing repository-layout tests | **4 PASS** | **4 PASS** |
| Existing SEO diagnostic unit tests | **64 PASS** | **64 PASS** |
| Existing public ads.txt fixtures | **2 PASS** | **2 PASS** |
| Existing sitemap-freshness fixtures | **3 PASS** | **3 PASS** |
| Existing discovery-integrity fixtures | **10 PASS** | **10 PASS** |
| Existing owner indexing/canonical contract | **PASS** | **PASS** |
| Existing public-surface Node gate | **48 passed, 0 failed** | **48 passed, 0 failed** |
| Existing theme contrast/budget gate | **PASS: 4,320 semantic pairs** | **PASS: 4,320 semantic pairs** |
| Existing experience DOM and shell-drawer suites | **PASS** | **PASS** |
| Actual publisher --check --out _site | **PASS: 5,499 files / 1,576 sitemap URLs** | **PASS: same** |
| Actual normal publisher --out _site and subsequent artifact check | **PASS** | **PASS** |
| Public HTML references checked against actual artifact | **PASS: 3,016 HTML / 249,514 references / 0 errors** | **PASS: same** |
| Actual service-worker SHELL targets present | **67/67 PASS** | **67/67 PASS** |

The final-artifact checker executes the unchanged publisher's `check('_site')`
after the normal build, not just the combined --check build. The built artifacts
are identical by complete path inventory and SHA-256 and match all 5,499 retained
pre-migration public files, including style.min.css, sw.js, all sitemap XML,
robots, voice output, HTML, course data and images. No generated file is promoted
back into the checkout.

Additional equivalence probes compare the captured original modules against
both migrated entrypoints: all **four module API comparisons PASS**. Reversing
only the ROOT assignments reproduces both original source files exactly. Using
the actual production CSS/JS inputs in separate run trees, all four ordered
checkpoints match untouched baseline exits, stdout, stderr and CSS bytes for both
legacy and canonical paths. Controlled fixtures separately preserve the known
separator behavior; cross-pass combined equality is never asserted.

The initial independent SW-reference harness assumed a PRECACHE variable name;
source inspection showed the runtime uses SHELL. The external harness was
corrected to inspect the actual list, then verified all 67 targets. No service
worker, publisher, algorithm or application assertion changed.

**NOT RUN:** full build-all/npm aggregates that include unrelated/live behavior,
real-browser or live-service suites, Python 3.12, remote Actions, deployment.
These are not implied PASS by the local validation. The historical 17/1 failure
remains separately preserved with its original bytes/hash.
