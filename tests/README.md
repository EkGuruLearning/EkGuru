# EkGuru tests

The 152 pre-cleanup test bodies are retained with their original filenames:

- `unit/`: 4 original fixture/helper contracts, plus the new repository-layout guard.
- `integration/`: 27 original application, payment, mail, intake and Sheet suites.
- `regression/`: 116 original DOM, learning, content, SEO and runtime regressions.
- `e2e/`: 5 original browser suites; the Playwright runner targets `test-journeys.mjs` only.
- `fixtures/`: the original 4 TSV files, unchanged.

This is a path/organization change, not a weakening of the tests. Existing test
names, assertions and skip behavior are preserved. In particular, a legacy browser
suite's existing `SKIP` exit must not be described as a successful browser run.

## Commands

Run commands from the repository root:

```bash
npm test
npm run test:courses
npm run test:learners
npm run test:advertising
npm run test:contract
python3 -B tests/unit/test-repository-layout.py
npx playwright test --config=playwright.config.mjs
```

Playwright's `@playwright/test` dependency and browser are installed separately
by `.github/workflows/playwright.yml`. They are not added to the package manifest
by this cleanup. Python browser suites also require their existing Playwright
runtime and the local server expected in each suite; they are not all selected
by the Node Playwright config.

## Safety and side effects

The master `python3 tools/build-all.py check` strips/reapplies generated HTML
layers and may update diagnostics. Some integration tests write reports or run
regeneration. Run those in an isolated filesystem copy when the source working
tree must remain unchanged. Never copy regenerated output back blindly.

Use the documented offline fixture mode when production Google endpoints are
unavailable:

```bash
EKGURU_TEST_FIXTURE_DIR=tests/fixtures python3 tests/integration/test-data-sources.py
node tests/integration/test-sheet-fetch.mjs
```

Fixture success is not live endpoint verification. Never change assertions or
turn network/browser failures into passes just to complete a migration.

## Compatibility

Selected `tools/test-*` paths remain as thin launchers because protected public
assets, Apps Script sources and content provenance cite those commands. Canonical
CI/package/master-build commands use the new paths. The complete mapping and
launcher flags live in `docs/architecture/cleanup-path-map.json`.

On future moves, check `import.meta.url`, `createRequire`, `__dirname`, Python
`__file__`/`sys.path`, sibling imports, subprocess commands, fixture paths,
package scripts, both workflow pipelines and Playwright configuration together.
