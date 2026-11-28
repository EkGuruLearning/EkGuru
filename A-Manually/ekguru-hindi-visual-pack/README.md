# EkGuru Hindi — original visual starter pack

This package contains **49 original hand-authored SVG illustrations** for the 13 current vowel/chart-form cards and the 36 consonant/conjunct cards in the four existing Foundation chapters. Includes a schematic animated क/ख airflow comparison, a printable preview, a JSON image manifest, a guarded installer, and fixture tests. The illustrations are simple textbook vectors, not photographs. No external image hosting, API or font file is needed.

## Preview
Unzip and open `preview.html` in a browser. Hindi speech uses the device's Hindi speech-synthesis voice if available; it is synthetic, not native-speaker audio. Print using the browser.

## Install in the actual Arena checkout
From the repository checkout, after extracting this package outside the repo:

```
python3 /path/to/ekguru-hindi-visual-pack/install.py .
python3 /path/to/ekguru-hindi-visual-pack/install.py . --apply
python3 tools/build-hindi-foundation.py --check
```

The first command is read-only. The installer matches the generator and four existing pages, compiles the modified generator and verifies all 49 exact character/word pairs before writing. It fails closed if the working branch has incompatible paths or layout. In that case, adapt the current generator to the provided manifest rather than reverting Arena work. Copy `images/hindi-textbook/` into the existing `images/` directory and use `illustrations.json` as the mapping. Keep the manifest's visual review status honest. Run the branch's normal full build, regression, publishing and browser tests; review any generated differences before committing. Don't copy the preview or installer into public deployment. The installer adds a manifest under `data/learning/`, 49 SVGs under `images/hindi-textbook/`, patches the Foundation builder, its CSS, and four generated pages. Re-running on the same compatible checkout is idempotent.

## Validation and limitations
- All 49 SVGs parsed and rendered locally; a contact sheet was visually inspected.
- Two local fixture tests passed (coverage/idempotence and fail-closed behavior). Source patch anchors and current keyword coverage were checked against GitHub main at d8f572a63694dd03c9256bec04214114c7f9183c.
- No full checkout, real repository build, browser interaction test, or editorial review was executed. GitHub branch creation returned 403, so nothing was pushed.
- This is an asset and integration starter pack, not the full Hindi curriculum. Additional letters, matras, Barakhadi, verified handwriting stroke paths, five distinct academic textbooks and an independent adult pathway still need implementation and review. Do not confuse the airflow animation with handwriting instruction.
- Some current Foundation example words depict concepts rather than a literal object (knowledge, greeting); illustrations are symbolic. Rare letters retain existing source wording; separate linguistic review is needed. No third-party artwork copied or hotlinked.
