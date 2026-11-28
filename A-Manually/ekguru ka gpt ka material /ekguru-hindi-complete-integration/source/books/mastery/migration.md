# Book 05 migration guide — safe staging, not a verified repository-wide map

Keep `/learn/hindi/` as the only Hindi hub. Book 05 follows Book 04. The target is `/learn/hindi/mastery/` with phases 01–04, chapters 01–40, lessons 01–02 and worksheets. Do not replace an existing root or child page silently. The installer refuses different-file collisions.

| Existing resource family | Proposed destination | Integration action |
|---|---|---|
| Existing literature and cultural guides | Phase 1 historical context; Phase 3 reading | Audit sources and depth; retain public URLs and link relevant guides |
| Grammar, idioms and language topics | Phase 2, chapters 11–20 | Reuse useful explanations, remove duplicates only after equivalence review |
| Advanced reading passages and practice | Phase 3, chapters 21–30 | Classify by difficulty and source; preserve independent tool state |
| Professional Hindi and office modules | Phase 4, chapters 33–34 or adult pathway | Reuse suitable content without equating school-inspired progression to adult proficiency |
| Writing, listening, speaking and translation labs | Phase 4 and final task | Keep original routes and connect relevant tasks |
| Existing A1–C2 courses | Independent proficiency resources | Do not equate CEFR levels with school grades |
| Old printables | Supplemental chapter materials | Preserve useful worksheets, canonical URLs, and print behavior |

Inspect the current Arena branch, inventory actual source ownership, URLs, inbound links, canonical/robots settings and state keys before migration. The above is not proof of repository-wide migration. Integrate with the existing Hindi V1 catalogue; connect Book 04 final link to the new verified route. Keep all new URLs noindex until owner approval. Reuse identical assets, consolidate shared reader JS/CSS, and retain independently authored textbook content. Do not publish internal tools or archives. Run the full repo regression, local and hosted browser journey, accessibility review, native-speaker editorial review and publishing checks. Preserve unrelated languages, tutor booking and existing serverless/static architecture. No unverified production deployment.
