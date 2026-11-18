## What and why
<!-- What changed, and why. One concern per PR. -->

## Type
- [ ] Content or data (`data/`, generator source)
- [ ] Generator or tool
- [ ] Runtime (`js/`, `css/`)
- [ ] Docs or structure
- [ ] Integration (`apps-script/`, `server/`): note whether the owner must redeploy

## Checks
- [ ] Ran the regeneration sequence (`docs/runbooks/regenerate-and-gate.md`)
- [ ] `python3 tools/build-all.py check` exits 0
- [ ] Changed the generator or source, not just its output
- [ ] New pages are noindex, or the owner approval is recorded in `docs/decisions/`
- [ ] No personal data in the diff (emails, phones, private Drive links, secrets)
- [ ] No unverifiable claims added ("verified", "native", counts)

## Owner action needed after merge
<!-- Apps Script redeploy, feed.url, Search Console, etc. Write "none" if none. -->

## CI
- [ ] `checks` green
- [ ] `journeys` green
