# Telegram PDF Module — Manifest

This bundle captures the Telegram/PDF code that was newly written and
integrated into EkGuru. It is a migration aid, not a runtime dependency
— after merging into EkGuru the application does not read from this
directory.

## Directories

```
migration/telegram-pdf-module/
├── README.md
├── MANIFEST.md
└── files/
    ├── server/
    │   ├── telegram/{url-parser.js,client.js,resolver.js}
    │   ├── pdf/{stream.js,metadata.js,api.js}
    │   ├── google-sheets/{pdf-sheets.js,config-reader.js}
    │   └── server.js
    ├── apps-script/
    │   └── Code.gs.append
    ├── scripts/
    │   └── telegram-login.js
    ├── courses/
    │   └── pdfs/index.html
    ├── admin-pdfs.html
    ├── tools/
    │   └── test-pdf-gateway.mjs
    ├── docs/
    │   ├── telegram-pdf-architecture.md
    │   ├── google-sheet-pdf-admin.md
    │   ├── telegram-auth-setup.md
    │   ├── security.md
    │   └── deployment.md
    ├── package.json.patch
    └── .gitignore.patch
```

## Checksum of intent

- Single repository runtime (EkGuru).
- No runtime dependency on EkguruTelegram.
- Google Sheet is the metadata source.
- MTProto streaming with Range and file-reference-expiry retry.
- Public responses never contain Telegram URLs.
- Admin enters only a `t.me/...` URL; the system derives publicId and serves on `/pdf/<publicId>`.
