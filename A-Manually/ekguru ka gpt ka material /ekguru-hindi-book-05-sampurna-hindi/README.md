# EkGuru Hindi — Book 05: संपूर्ण हिंदी
Independent Class 10–12-inspired Hindi Mastery draft; not an accredited school qualification, official board syllabus or native-speaker-reviewed textbook. Entry: Book 04 or equivalent grammar, reading and writing competencies. The final task is a self-assessment, not a certificate.

## Actual contents
4 phases, 40 chapters, 80 authored lessons, 400 vocabulary occurrences (including revision), 241 short reading examples, 20 original extended passages and 60 comprehension questions, 59 topic-specific quiz labs, 22 visual analysis models, 10 final multiple-choice exercises, 80 writing workspaces, 40 printable worksheets and 165 generated HTML pages. 151 SVG assets: 141 shared from earlier books and 10 new contextual illustrations. Every lesson includes a contextual illustration or illustrated reading. Abstract vocabulary uses explanations and models rather than inaccurate pictorial definitions. The literature history lessons introduce authors and traditions; they are not a complete anthology. All practice passages are original. The references below are study directions, not claims of full scholarly review.

## Preview
Extract. Run `python3 -m http.server 8000 --directory site`. Open `http://localhost:8000/learn/hindi/mastery/`. `preview-lesson.html` is an embedded Chapter 23 Lesson 2 sample; internal links are disabled there, but the full site contains navigable routes. Audio uses a device Hindi speech-synthesis voice if available, not recordings. Drafts are saved on explicit request in browser storage. The word counter uses whitespace tokens. Freehand practice is not verified stroke-order instruction.

## Safe integration
Target `/learn/hindi/mastery/`. Run `python3 install.py /path/to/EkGuru` (dry run); if safe, rerun with `--apply`. If the current branch already has a mastery root, use `--keep-existing-root` at both steps and merge the root through its owning generator. The installer adds missing/identical files, refuses different-file collisions and never deletes old pages. It updates the existing Hindi V1 registry status to `existing` when available and installing the new root. Verify integrated content before advertising availability. Keep every new page noindex pending the existing indexing approval. Connect Book 04 → Book 05; Book 05 ends with a portfolio, final practice and independent further study, not a claim of certified fluency.

Keep the ZIP, source, tests, installer and standalone previews in private development directories. Reuse the existing static build pipeline, shared reader and site shell, theme, consent, editorial disclosures, accessibility and publisher contract. Consolidate identical assets and reader engines. Do not create a backend, another Academy root, paid API or payment service. See migration.md.

## Rebuild
`python3 source/build_art.py` regenerates the 10 new scenes and scene map. `python3 source/build.py` generates the static book from curriculum.txt, passages.txt, labs.json and visual-models.json. `python3 source/preview.py` generates the sample preview. Authored lab-data.txt and models.txt are source references; synchronize their JSON files when editing. Earlier illustrations are bundled for reuse.

## Educational references and editorial limitations
- IGNOU/eGyanKosh Hindi literature history: https://www.egyankosh.ac.in/handle/123456789/54489
- Dr. B. R. Ambedkar University Delhi, Hindi Sahitya ka Itihas (Ritikal tak): https://aud.delhi.gov.in/hindi-sahitya-ka-itihas-ritikal-tak
- IGNOU Hindi literature curriculum: https://egyankosh.ac.in/handle/123456789/66322
- Meter introduction: https://maanasa.org/chhand (secondary interactive reference; independently verify complete prosodic rules before review).
The periodization is an introduction, not a claim that literary periods have universally agreed boundaries. Meter diagrams show quantitative patterns, not automatic metrical validation. The original readings are not excerpts attributed to historical poets. Educator review of history, language, prosody, examples, pronunciation and accessibility remains required.

## Validation
`python3 tests/test_book.py` passed 11 tests; `python3 tests/test_install.py` passed 2 fixtures; `node --check site/js/hindi-mastery-reader.js` passed; `python3 tests/browser_test.py` passed 27 page/viewport combinations and embedded-DOM interaction tests (visual meter model, correct/incorrect feedback, writing canvas/undo, word counter, save feedback, progress completion, English toggle, dark theme, reading answers, final assessment, print CSS, no-JS reading, missing Hindi voice handling). Static local link and fragment checks passed. Hosted navigation, draft persistence across reloads, full repository build, actual print pagination, screen reader review, live performance and native recordings have not been verified. No GitHub edits or production deployment.
