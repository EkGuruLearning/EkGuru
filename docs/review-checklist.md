# Native/editorial review checklist

**Current state: no native-speaker approval has been recorded.** Registry rows, passing software checks and legacy
"complete/production" labels are not approval evidence. Existing indexing is frozen by the owner; the strict language gate
must keep failing while indexed failures exist. New drafts are noindex. Do not manufacture a reviewer, a permission, a
certificate or a review date.

## Review the exact version

1. Run the language gate for the language and save its `content_digest` — the normalized teaching input **without** the review
   field, not a menu/CSS hash.
2. Check sources. A generic homepage does not substantiate a speaker number or an official-language claim. Each number needs a
   precise record, a year and a URL. No source, no number.
3. Confirm the exact language/variety (ISO 639-3, BCP-47), endonym, script and direction. Keep ambiguous facts unresolved.
4. Independently check target text, romanisation, register, gender/number, dialect, punctuation and every answer key.
   IPA only where known; never invented to fill a field.
5. T1 needs eleven named rungs (A1, A1+, A2, A2+, B1, B1+, B2, B2+, C1, C1+, C2), 3–5 units per rung and 3–5 lessons per unit.
   A1 vocabulary relabelled C2 is not an advanced course, and legacy A3/B3/C3–C5 labels are not substitutes for the half-steps.
6. For each lesson: useful explanation, specific examples, vocabulary, grammar, dialogue, varied practice, quiz explanations and a
   worksheet with key. Check distractors and every accepted answer.
7. For each level: a sourced culture note, an original reading, a listening script, ten idioms/expressions with literal and
   actual meanings, learner-specific mistakes and one practical task. Record what is missing, not a guessed pass.
8. T2: a genuine script lesson, 300 words, 50 phrases, 10 dialogues, 5 grammar notes, 3 practice sets. T3: sourced facts, a
   script sample, 20 phrases and a guide with at least 400 unique words.
9. Originality: a similarity score is a signal, not proof of authorship. Do not copy textbook or reference passages.
10. Audio: test synthetic speech with a correctly tagged installed voice; the existence of a browser API is not approval of
    pronunciation. Review licensed human recordings and their credits separately. A missing voice must disable/skip playback honestly.
11. Test keyboard, language tags, RTL, zoom, contrast, reduced motion and visible romanisation.
12. Record corrections and unresolved questions. The public correction form is a suggestion queue, not an approval endpoint.

## Evidence and privacy

The owner privately verifies the reviewer's competence, identity, scope and checklist. Keep correspondence and non-consenting names
outside this public repository. A public approved record uses an opaque `reviewer_id`, the exact digest, the reviewed date,
`owner_verified: true` and `consent_to_publish`. Include `name` only if consent is true.

Changing teaching input invalidates a digest-bound review. After a real review, rerun the gate. **Passing the gate does not itself
authorize a publication or indexing change**: the owner freeze stays binding until separately lifted.

## Workflow

Draft → source and automatic checks → private competent native review → owner verification and permission → strict release
checks → owner-authorized publication. Reports may be generated for failing drafts; only `--enforce-publication` is a
publication acceptance gate.
