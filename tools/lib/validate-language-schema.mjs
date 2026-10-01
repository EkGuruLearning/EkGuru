#!/usr/bin/env node
/* Ajv (JSON Schema 2020-12) validation for the registry rows and the tiered content. Prints compact JSON to stdout.
   Usage: node tools/lib/validate-language-schema.mjs <input.json>   input: { registry:[rows], t1:{code:[{rung,file}]}, t2:{code:file|normalized}, t3:{code:file} } */
import { readFileSync } from 'node:fs';
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
const read = (f) => JSON.parse(readFileSync(f, 'utf8'));
const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);
const schemas = { registry: ajv.compile(read('data/schemas/registry.schema.json')), t1: ajv.compile(read('data/schemas/course-t1.schema.json')), t2: ajv.compile(read('data/schemas/starter-t2.schema.json')), t3: ajv.compile(read('data/schemas/reference-t3.schema.json')) };
const input = read(process.argv[2]);
const summarize = (validate) => [...new Set((validate.errors || []).map((e) => `${e.keyword}:${(e.instancePath || '').replace(/\/\d+/g, '/*') || '/'}${e.params && e.params.missingProperty ? '.' + e.params.missingProperty : ''}`))].sort();
const out = { registry: {}, t1: {}, t2: {}, t3: {} };
for (const row of input.registry || []) { const ok = schemas.registry(row); if (!ok) out.registry[row.code] = summarize(schemas.registry); }
for (const [code, levels] of Object.entries(input.t1 || {})) { out.t1[code] = {}; for (const { rung, file } of levels) { const ok = schemas.t1(read(file)); if (!ok) out.t1[code][rung] = summarize(schemas.t1); } }
for (const [code, obj] of Object.entries(input.t2 || {})) { const ok = schemas.t2(obj); if (!ok) out.t2[code] = summarize(schemas.t2); }
for (const [code, file] of Object.entries(input.t3 || {})) { const ok = schemas.t3(read(file)); if (!ok) out.t3[code] = summarize(schemas.t3); }
process.stdout.write(JSON.stringify(out));
