// Entry for make.fun news-image-20261124: "Sum up 24 November's world
// news in one image".
//
// The front page itself is pre-drawn by render.py in this repository and
// stored as entry.png (1024x1024, well under the 1 MiB cap). This program
// does nothing but copy that fixed file into the grader's output folder,
// which makes every run produce byte-identical output. Before copying it
// sanity-checks the file: it must be a whole PNG, inside the size caps.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const OUT = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const SRC = new URL("./entry.png", import.meta.url);
const LIMIT = 1048576; // 1 MiB
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const data = readFileSync(SRC);

if (!data.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error("entry.png does not start with the PNG signature");
}
if (data.length > LIMIT) {
  throw new Error(`entry.png is ${data.length} bytes, over the 1 MiB cap`);
}

// Width and height live in the IHDR chunk: after the 8-byte signature, a
// 4-byte length and the 4-byte "IHDR" tag, the next 8 bytes are width
// then height, both big-endian.
const w = data.readUInt32BE(16);
const h = data.readUInt32BE(20);
if (w > 1024 || h > 1024) {
  throw new Error(`entry.png is ${w}x${h}, over the 1024x1024 cap`);
}

mkdirSync(OUT, { recursive: true });
const dest = join(OUT, "entry.png");
copyFileSync(SRC, dest);
console.log(`copied ${data.length} bytes (${w}x${h}) to ${dest}`);
