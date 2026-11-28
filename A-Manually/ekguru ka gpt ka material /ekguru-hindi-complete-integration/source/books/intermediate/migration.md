# Integration and migration checkpoint — Book 03

This is a proposed map, not a verified repository-wide content migration. Existing routes must remain reachable, with original indexing and canonical behavior. Inspect current branch before making changes; the last known repository inventory contains `/learn/hindi/intermediate/` with legacy content. Do not discard the current branch's changes or overwrite the root using the standalone generator.

| Existing material / collection | Proposed Book 03 destination | Action |
|---|---|---|
| /learn/hindi/intermediate/ | Book 03 landing page | Merge useful material, preserve existing URL and old anchors; change the owning generator only after audit |
| /hindi/grammar/, /hindi/verbs/, /hindi/sentence-structure/ | Phases 01–02 | Crosslink existing material and classify depth; retain indexed URLs |
| /learn/hindi-sentence-structure/, /learn/hindi-verbs-present-past-future/ | Chapters 8–11, 17–20 | Link as supplementary revision; compare overlapping text before any migration |
| /learn/common-hindi-mistakes/ | Chapter 19 | Retain guide and integrate useful correction examples after review |
| /hindi/reading/, /hindi/writing/, /hindi/listening/ | Phases 03–04 | Integrate appropriate skills references |
| /learn/practice/grammar/, /learn/practice/verbs/, /learn/practice/sentence-builder/ | Phase 02 | Link existing working practice as supplementary labs |
| /learn/practice/reading/, /learn/practice/speaking/, /learn/practice/listening/ | Phases 03–04 | Retain existing exercises |
| /materials/ | Worksheets | Retain all existing resources; do not remove old worksheets just because new ones exist |
| /languages/hi/level/ | Existing proficiency resources | Keep CEFR-style labels separate from age/academic stages; do not claim official equivalence |
| /learn/hindi/beginner/, /learn/hindi/advanced/ | Previous and next book | Update progression after actual integration |

Use an exact collision preflight. The generated pages default to noindex. Do not change old routes' canonical tags or robots by copying over existing landing pages. Register Book 03 with correct stage status only after integration. The standalone package retains its own progress key `ekguru:intermediate:done:v1`; preserve existing storage and map IDs explicitly. Do not reset users' data. Run the complete existing build and publisher validation, all link/fragment checks, browser navigation, real storage persistence, accessibility, speech and performance checks. Remove only independently verified obsolete presentation markup via its owning generator. No production deploy based on this package alone.
