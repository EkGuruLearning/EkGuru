# Review records

No approved review records have been supplied. See `docs/review-checklist.md`.

This directory is PUBLIC (GitHub and Pages). Never commit a non-consenting name, a private email or correspondence.
Keep verification evidence in the owner's private queue, outside the deployed checkout.

A future real approval is a file `data/reviews/<code>.json` such as
`{ "review": { "status": "reviewed", "reviewer_id": "opaque-id-of-8-to-64-characters", "consent_to_publish": false, "content_digest": "exact SHA-256 from the language gate", "reviewed_on": "actual ISO date", "owner_verified": true } }`.
`name` is required only with explicit publication consent; otherwise it is prohibited. This illustration is not an approval,
a valid digest or a real reviewer.

A review is bound to the exact normalized course input (excluding the review field). A code change, a registry count or an
old "production" label is not a native review. Never invent a record or set `owner_verified` without the owner's evidence.
