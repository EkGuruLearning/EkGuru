# Integrated Hindi architecture

```mermaid
graph TD
 A[Learn] --> B[Hindi hub existing generator]
 B --> C[Five academic textbooks]
 B --> D[Adult path: five stages]
 B --> E[Study Studio]
 C --> F[Book manifests]
 D --> F
 F --> G[Unified resource and card index]
 G --> E
 C --> H[Shared navigation]
 D --> H
 H --> E
 I[Existing local completion keys] --> E
 E --> J[Studio-specific local review and bookmarks]
 E --> K[JSON backup of Studio state only]
```

The six existing textbook generators are preserved as separate content owners. The build stages their output and checks collisions before combining. Studio only reads actual published-to-package routes. Lesson and progress identifiers remain stable. No new server database is required. For a future book or language, extend the explicit book registry in `source/build_studio.py` and provide the corresponding generated manifest, art and routes. The current registry is Hindi-specific; a language-neutral registry is a future improvement.
