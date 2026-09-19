/* =========================================================
   EkGuru — TOOL REGISTRY  (single source of truth · v100)
   ---------------------------------------------------------
   One record per public toolbox tool. The admin Learn Ops
   "Tool control centre" reads this file and joins it with the
   real-browser test results in reports/tool-functional-qa.json
   (fetched at runtime, same origin). Nothing here claims a test
   passed — `status` only records the last known state; the QA
   JSON is the authority on whether the tool actually works.

   owner   — who is responsible for this tool's content.
   deps    — runtime dependencies (empty = static, no JS deps).
   fallback— what the tool degrades to if its dependency fails.
   ========================================================= */
window.EKGURU_TOOL_REGISTRY = [
  {
    slug: "hindi-alphabet", name: "Hindi alphabet explorer",
    path: "/toolbox/hindi-alphabet/", category: "reading",
    version: "v3", owner: "EkGuru admin",
    deps: [], fallback: "None needed — static letter grid.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-numbers", name: "Hindi numbers converter",
    path: "/toolbox/hindi-numbers/", category: "vocabulary",
    version: "v2", owner: "EkGuru admin",
    deps: [], fallback: "None needed — pure JS conversion.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-phrasebook", name: "Hindi phrasebook",
    path: "/toolbox/hindi-phrasebook/", category: "speaking",
    version: "v4", owner: "EkGuru admin",
    deps: [], fallback: "None needed — static phrase list.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-flashcards", name: "Hindi flashcards",
    path: "/toolbox/hindi-flashcards/", category: "vocabulary",
    version: "v3", owner: "EkGuru admin",
    deps: ["speechSynthesis (optional play)"] ,
    fallback: "Cards still flip/advance without audio.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-quiz", name: "Hindi quiz",
    path: "/toolbox/hindi-quiz/", category: "practice",
    version: "v2", owner: "EkGuru admin",
    deps: [], fallback: "None needed.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-level-test", name: "Hindi level test",
    path: "/toolbox/hindi-level-test/", category: "placement",
    version: "v2", owner: "EkGuru admin",
    deps: [], fallback: "None needed.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-typing", name: "Hindi typing tutor",
    path: "/toolbox/hindi-typing/", category: "writing",
    version: "v2", owner: "EkGuru admin",
    deps: [], fallback: "None needed.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-verbs", name: "Hindi verb explorer",
    path: "/toolbox/hindi-verbs/", category: "grammar",
    version: "v4", owner: "EkGuru admin",
    deps: [], fallback: "None needed — static verb table + search.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-vocabulary", name: "Hindi vocabulary tool",
    path: "/toolbox/hindi-vocabulary/", category: "vocabulary",
    version: "v3", owner: "EkGuru admin",
    deps: [], fallback: "None needed — static word list + search.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-date-time", name: "Hindi date & time tool",
    path: "/toolbox/hindi-date-time/", category: "everyday",
    version: "v2", owner: "EkGuru admin",
    deps: [], fallback: "None needed — pure JS.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-pronunciation", name: "Hindi pronunciation guide",
    path: "/toolbox/hindi-pronunciation/", category: "pronunciation",
    version: "v2", owner: "EkGuru admin",
    deps: ["speechSynthesis (playback)"],
    fallback: "Letters still shown if audio unavailable.",
    last_tested: "2026-09-11"
  },
  {
    slug: "hindi-time-planner", name: "Hindi time planner",
    path: "/toolbox/hindi-time-planner/", category: "everyday",
    version: "v2", owner: "EkGuru admin",
    deps: [], fallback: "None needed.",
    last_tested: "2026-09-11"
  }
];
