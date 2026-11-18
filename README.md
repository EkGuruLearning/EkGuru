# EkGuru

Free, self-paced language learning with an emphasis on Hindi and the Indian
languages, plus a small directory of independent tutors. Live at
<https://ekguru.shop>.

This repository **is** the website: a static site of about 2,700 pages served
from the repository root by GitHub Pages, plus the tools that generate and
check it, a small payments server, and the Google Apps Script sources that
connect it to a Google Sheet.

## Start here

| If you want to… | Read |
|---|---|
| Understand how the repo is organised | [`docs/architecture/REPO-STRUCTURE.md`](docs/architecture/REPO-STRUCTURE.md) |
| See the system design and migration plan | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| Make a change safely | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Regenerate pages and pass the gate | [`docs/runbooks/regenerate-and-gate.md`](docs/runbooks/regenerate-and-gate.md) |
| Add a page, level, language or tutor | [`docs/runbooks/add-page-or-language.md`](docs/runbooks/add-page-or-language.md) |
| Know what is broken and who fixes it | [`docs/ROADMAP-FIXES.md`](docs/ROADMAP-FIXES.md) |
| Find every document | [`docs/README.md`](docs/README.md) |

## Quick start

```bash
npm install                              # jsdom for the browser-QA tests
python3 tools/build-all.py check         # the master gate; exit 0 = green
npm start                                # payments server (needs local config)
```

## The three rules

1. **A root folder is a public URL.** Do not move or rename `hindi/`,
   `learn/`, `languages/` and the rest. See the structure doc.
2. **Edit the source, not the generated page.** Pages come from `tools/`
   generators and `data/courses/`. Then run the regeneration sequence.
3. **The gate decides.** `python3 tools/build-all.py check` must exit 0 and CI
   (`checks`, `journeys`) must be green before a merge. New pages are noindex
   unless the owner approves them in writing.

## Layout at a glance

```
ekguru/
├── (root pages, sitemaps, CNAME)   published site files
├── hindi/ learn/ languages/ …      published URL folders (generated)
├── data/                           course JSON, schemas, quality reports
├── js/  css/  images/  src/        browser runtime and assets
├── tools/                          generators, audits and tests
├── tests/                          fixtures (unit tests move here in phase 1)
├── server/                         payments API (Node)
├── apps-script/                    Google Apps Script sources (owner deploys)
├── docs/                           architecture, runbooks, decisions, audits
├── reports/  research/             generated reports and research notes
└── .github/workflows/              CI
```

## Privacy

This repository is public. Never commit applicant or tutor emails, phone
numbers, private Drive links, or deploy secrets. Personal data lives in the
Google Sheet.
