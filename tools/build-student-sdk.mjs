import { build } from 'esbuild';
import fs from 'node:fs';
const check = process.argv.includes('--check');
const result = await build({entryPoints:['src/student/firebase-sdk.js'], bundle:true, format:'esm', platform:'browser', target:['es2020'], minify:true, legalComments:'none', write:false, banner:{js:'/*! Firebase JS SDK 12.6.0 (Apache-2.0); bundled by tools/build-student-sdk.mjs */'}});
const output = Buffer.from(result.outputFiles[0].contents);
const target='js/student/firebase-sdk.js';
if(check){if(!fs.existsSync(target)||!fs.readFileSync(target).equals(output)){console.error('STALE '+target);process.exit(1)}console.log('Firebase browser bundle current');}
else {fs.mkdirSync('js/student',{recursive:true});fs.writeFileSync(target,output);console.log('Built '+target+' ('+output.length+' bytes)');}
