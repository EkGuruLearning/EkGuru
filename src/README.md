# src/

Reserved for hand-edited source (migration phase 3). Today it holds only
`runtime/voice.js`, which `tools/build-runtime.mjs` and `js/voice.js` reference.

Target: `src/content/` (course JSON, tutor and review rows), `src/site/`
(templates and shell), `src/runtime/` (browser JS), `src/styles/` (CSS source).
Until phase 3, keep using `data/`, `js/` and `css/`. Do not start moving files
here ad hoc; the move is its own PR, with the gate green.
