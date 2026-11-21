// news-image-20261120 entry (Node 22, standard library only).
// The image is entry.png beside this file: a dense newspaper front page
// summing up the world news of Friday 20 November 2026
// (Kyiv barrage into Poland, U.S.–China–Russia joint declaration,
// ICJ genocide ruling on Myanmar). The program copies it to the output dir.
//
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

// The program runs twice and both runs must write the same bytes,
// so this is a plain copy: no timestamps, no randomness, no network.
// (entry.png itself is drawn by draw_frontpage.py, Python + PIL.)
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
copyFileSync(source, join(outDir, 'entry.png'));
