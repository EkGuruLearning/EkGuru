# Known generator cycles and ordering traps

`ARCHITECTURE.md` §6 promised this file. It lists the places where one tool
undoes another's output, so nobody rediscovers them by breaking 300 pages.
Phase 2 of the migration should make the ordering explicit; until then, follow
[`../runbooks/regenerate-and-gate.md`](../runbooks/regenerate-and-gate.md).

| Trap | What goes wrong | Rule |
|---|---|---|
| `build-lang-topics.py` run on decorated pages | Drops the ultra head and `data-ad-class` on about 314 Indian-language topic pages (found 2 Nov 2026) | Never run it without `apply-ultra.py --strip` first and `apply-ultra.py` after |
| Any page generator run on decorated pages | Same loss, wider | Generate only in the stripped state |
| Interrupted regeneration | Leaves 2,000+ pages stripped in the working tree | Re-run the whole sequence; never commit the partial state |
| `build-full-page-inventory.py` before `apply-ultra.py` | Inventory records stripped pages, gate then disagrees | Inventory runs after re-decoration |
| `update-editorial-metadata.py` skipped | Editorial dates and fingerprints stale, gate fails | Run it after the inventories |
| Page count changes | `tools/test-reading-layer.mjs` carries a hard-coded count | Update it in the same PR |

Add a row here whenever a new cycle is found.
