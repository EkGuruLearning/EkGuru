# Hindi textbook: architecture and migration checkpoint

Snapshot: working branch `arena/28510265-ekguru`, HEAD `d8f572a63694dd03c9256bec04214114c7f9183c`, 2026-11-28. The uncommitted prior Academy work is part of this branch. The inventory snapshots are `resource-inventory.json` and `resource-inbound-links.json`; `python3 tools/audit-hindi-textbook.py` refreshes both. The scan covers all public HTML for inbound anchors and candidate selection additionally considers Hindi language tags inside main content. It is **not** a complete editorial audit: dynamic links, CSS imports, generic unreferenced assets, externally hosted material and non-HTML content require further investigation. Metadata fields marked unassigned/not assessed are not claims of pedagogical quality. Identity route mapping is deliberate: preserve each existing URL until the owner approves a specific change.

The site deploys the static `_site` artifact via `.github/workflows/pages.yml` and `tools/build-public-dist.py`; no server redirect rule is configured here. Do not assume a permanent HTTP redirect. No production deploy or merge is authorized by this document.

## 1. System context
```mermaid
flowchart LR
  Learner -->|HTML, CSS, JS| Pages[Static EkGuru Pages]
  Pages -->|optional| Voice[Device Hindi speech]
  Pages -->|device only| Local[Browser learning stores]
  Learner -->|optional| Tutors[Existing independent tutor pages]
  Editors -->|content and review| Repo[Repository]
  Repo --> Build[Existing build and quality gates]
  Build --> Pages
```
## 2. DFD level 0
```mermaid
flowchart LR
 Learner -->|select, read, practise| Hindi[Hindi learning system]
 Hindi -->|independent academic or adult lessons, feedback, print| Learner
 Hindi <--> |progress| Local[(Browser local storage)]
 Editors -->|reviewed content| Hindi
```
## 3. DFD level 1
```mermaid
flowchart LR
 Manifest[(Curriculum registry: academic and adult paths)] --> Contents[Foundation chapter contents]
 Manifest -. planned .-> Books[Distinct textbook content by pathway]
 Sources[(Existing Hindi pages)] --> Hub[Hindi home and contents]
 Sources --> Reader[Existing lesson reader]
 Contents --> Reader
 Reader --> Audio[Shared voice adapter]
 Reader --> Progress[Existing journal]
 Reader --> Print[Browser print]
```
## 4. DFD level 2: publication
```mermaid
flowchart LR
 Source[Pathway-specific content and shared media sources] --> Validate[Build-time validation]
 Validate -->|valid| Render[Static HTML and index generators]
 Render --> Gates[Shell, indexing contract, tests]
 Gates --> Public[Public artifact builder]
 Public -->|owner-approved release only| Pages[GitHub Pages]
 Validate -->|failure| Editor[Correction]
```
## 5. Logical ERD
```mermaid
erDiagram
 LANGUAGE ||--o{ LEARNING_PATH : offers
 LEARNING_PATH ||--o{ TEXTBOOK : contains
 TEXTBOOK ||--o{ PHASE : owns
 PHASE ||--o{ CHAPTER : contains
 CHAPTER ||--o{ LESSON : contains
 LESSON }o--o{ VOCABULARY : references
 LESSON ||--o{ ACTIVITY : has
 LESSON ||--o{ RESOURCE : links
 RESOURCE ||--o| AUDIO : may_be
 RESOURCE ||--o| WORKSHEET : may_be
 LESSON ||--o{ LEGACY_ROUTE : preserves
 LESSON ||--o| EDITORIAL_STATUS : has
 LESSON ||--o{ LEARNER_PROGRESS : "local on device"
 CHARACTER ||--o{ STROKE : "only if reviewed"
```
The diagram is a target logical model. Not all entities have implemented schema or reviewed records.

## 6. UML component diagram
```mermaid
flowchart TD
 Hub[build-hindi-hub.py] --> Existing[Existing public pages]
 Directory[build-hindi-academy.py] --> Registry[academy_registry.py]
 Reader[build-hindi-textbook-reader.py] --> Registry
 Registry --> Manifest[curriculum.json: existing lessons, planned books, character coverage]
 Reader --> FoundationPages[18 existing Foundation pages]
 Foundation[build-hindi-foundation.py] --> Primer[hindi-foundation-content.py]
 Foundation --> VisualManifest[Illustration manifest: 49 draft vectors]
 VisualManifest --> VisualAssets[Locally hosted SVG illustrations]
 Voice[voice.js] --> Browser[Browser speech]
 Progress[hindi-progress.js and retention.js] --> Store[(localStorage)]
```
## 7. UML package diagram
```mermaid
flowchart LR
 Tools[tools and tools/lib] --> Data[Curriculum and media manifests]
 Data --> Academic[Academic textbook content]
 Data --> Adult[Independent adult content]
 Tools --> Public[learn/hindi]
 Public --> Shared[css and js]
 Tests[tests] --> Tools
 Docs[docs/architecture/hindi] -. private .-> Public
```
## 8. Learning activity
```mermaid
flowchart TD
 A[Choose a pathway and level by proficiency] --> B[Open an existing lesson]
 B --> C[Read and listen]
 C --> D[Practise and self-check]
 D --> E{Continue?}
 E -->|yes| F[Next lesson]
 E -->|later| G[Optional local journal]
```
## 9. Chapter navigation state
```mermaid
stateDiagram-v2
 [*] --> Contents
 Contents --> Lesson: open anchor
 Lesson --> Lesson: previous or next
 Lesson --> Contents: back to contents
 Lesson --> [*]: leave freely
```
Navigation never requires assessment completion.

## 10. Learner interaction sequence
```mermaid
sequenceDiagram
 Learner->>StaticPage: Open lesson
 StaticPage-->>Learner: HTML reading and links
 Learner->>Voice: Optional listen
 Voice-->>Learner: Hindi device voice or unavailable message
 Learner->>Journal: Optional mark complete
 Journal->>LocalStorage: Save on device
```
## 11. Content publishing sequence
```mermaid
sequenceDiagram
 Editor->>Manifest: Assign resource to a specific pathway and textbook
 Editor->>Generator: Build
 Generator->>Validator: Check identifiers and routes
 Validator-->>Generator: Validation result
 Generator->>PublicPages: Update owned regions
 Editor->>Tests: Run checks and request review
```
## 12. Repository dependency graph
```mermaid
flowchart LR
 HubSource[tools/build-hindi-hub.py] --> Hub[/learn/hindi/]
 RegistrySource[data/hindi-academy/curriculum.json] --> ReaderBuilder[build-hindi-textbook-reader.py]
 Pictures[data/learning/hindi-textbook-illustrations.json] --> FoundationBuilder
 ReaderBuilder --> Foundation[/learn/hindi/foundation/]
 FoundationSource[tools/hindi-foundation-content.py] --> FoundationBuilder[build-hindi-foundation.py]
 FoundationBuilder --> Foundation
 Shell[build-shell.js] --> Hub
 Ultra[apply-ultra.py] --> Hub
 PublicBuilder[build-public-dist.py] --> Site[_site]
```
## 13. URL hierarchy
```mermaid
flowchart TD
 Home[/] --> Learn[/learn/]
 Learn --> Hindi[/learn/hindi/]
 Hindi --> Kids[/learn/hindi/kids/]
 Hindi --> Beginner[/learn/hindi/beginner/]
 Hindi --> Intermediate[/learn/hindi/intermediate/]
 Hindi --> Advanced[/learn/hindi/advanced/]
 Hindi --> Mastery[/learn/hindi/mastery/ planned]
 Hindi --> Older[/learn/hindi/older-adults/ planned]
 Older -. planned .-> AF[Adult Foundation]
 AF -. planned .-> AB[Adult Beginner]
 AB -. planned .-> AI[Adult Intermediate]
 AI -. planned .-> AA[Adult Advanced]
 AA -. planned .-> AM[Adult Mastery]
 Beginner --> Foundation[/learn/hindi/foundation/]
 Foundation --> Vowels[/learn/hindi/foundation/swar/]
 Hindi -. compatibility retained .-> Academy[/learn/hindi/academy/]
```
Kids, mastery, older-adults and all proposed phase routes are planned, not published. The existing beginner, intermediate and advanced pages are earlier material, not completed books. The current manifest references 18 existing Foundation lessons in the beginner book’s first planned phase; the generated navigation links to the existing URLs, not the planned phase URLs. No textbook is complete.

## 14. Existing-to-target migration map
```mermaid
flowchart LR
 Existing[Existing Foundation, level, topic, practice and material URLs] -->|KEEP; classify with editorial review| Hindi[/learn/hindi/]
 Existing -. preliminary 18 lessons .-> Academic[Academic beginner foundation]
 Existing -. adult mapping unreviewed .-> Adult[Adult pathway]
 Previous[Previous Academy URLs] -->|KEEP compatibility; no server redirect assumed| Hindi
 Unknown[Unassessed Hindi resources] --> Review[Human mapping and quality review]
 Review --> Existing
```
## 15. Editorial lifecycle
```mermaid
stateDiagram-v2
 [*] --> ExistingOrDraft
 ExistingOrDraft --> TechnicalChecks
 TechnicalChecks --> HumanReview: checks pass
 HumanReview --> Correction: issues found
 Correction --> TechnicalChecks
 HumanReview --> OwnerDecision: approved and documented
 OwnerDecision --> Published: indexing approved
```

## Guardrails and open decisions

- Old routes and canonical relationships remain untouched until an explicit reviewed migration; the inventory defaults to KEEP rather than inventing MOVE/MERGE decisions.
- No high-quality stroke data has been verified. The current canvas is a printed-model trace and self-check, not a stroke-order animation or recognition.
- Reuse existing foundation, graded levels, daily course, topic lessons, worksheets and voice controls; collection links are not evidence of complete new dedicated courses.
- The legacy local journal and shared retention stores are not rewritten or migrated merely to create new navigation.
- New standalone route files remain noindex pending owner and editorial approval in accordance with the existing indexing contract. Shared resources are not silently duplicated.


## 16. Curriculum progression and prerequisite matrix (planned)

```mermaid
flowchart LR
  K[Academic: Kids] --> B[Beginner] --> I[Intermediate] --> A[Advanced] --> M[Mastery]
  AF[Adult: Foundation] --> AB[Beginner] --> AI[Intermediate] --> AA[Advanced] --> AM[Mastery]
  M -. future assessment .-> H[Hindi Hero]
  AM -. future assessment .-> H
```

`data/hindi-academy/curriculum.json` contains each stage's immediate prerequisite, proposed entry/exit competencies, vocabulary and grammar scope, reading/writing/speaking/listening targets, and four phases. It records the 100 requested academic topics and 100 preliminary adult topics as **planned labels, not authored chapters or assessments**. Academic age/class guidance is an independent design analogy, not a board qualification, a prerequisite or an age restriction; learners may start by proficiency. The adult pathway requires independently authored mature content, not copies of the academic lessons. Placement and assessment criteria, individual learning objectives, precise vocabulary targets, differentiated content, phase pages and a complete dependency map remain to be developed and reviewed. No Hindi Hero credential exists yet.

The shared software component renders owned textbook content; it is not a single shared textbook. The 18 existing Foundation pages are preliminarily mapped only to academic Beginner, while the adult pathway is unfilled. Shared visual and vocabulary identifiers can be reused, but existing lesson IDs cannot be counted as chapters of multiple textbooks.
