// Print the next (or current) Mercury retrograde from the dataset.
// Node 18+, no dependencies. Run from anywhere:
//
//   node examples/javascript/next-mercury-retrograde.mjs
//   node examples/javascript/next-mercury-retrograde.mjs 2031-06-01   # as of another date
//
// Data: Cazimi retrograde ephemeris (JPL DE421), CC BY 4.0,
// https://doi.org/10.5281/zenodo.24011806 and https://cazimi.live

import { readFile } from "node:fs/promises";

const DATA = new URL("../../data/mercury-1900-2050.json", import.meta.url);

// Times look like "2027-02-09T17:36Z": UTC, to the minute. Date.parse reads them as is.
const parse = (t) => new Date(t);

const now = process.argv[2] ? new Date(process.argv[2] + "T00:00Z") : new Date();
const { mercury: cycles } = JSON.parse(await readFile(DATA, "utf8"));

// The first cycle whose station direct is still ahead: current or next.
const cycle = cycles.find((c) => parse(c.direct) > now);
if (!cycle) {
  console.log("No Mercury retrograde after that date in this file (it ends in 2050).");
  process.exit(0);
}

const state = parse(cycle.retro) <= now ? "now retrograde" : "next retrograde";
console.log(`Mercury ${state}, in ${cycle.sign}`);
console.log(`  pre-shadow begins   ${cycle.pre}`);
console.log(`  station retrograde  ${cycle.retro}  ${cycle.retroDegree}`);
console.log(`  cazimi (Sun)        ${cycle.cazimi}  ${cycle.cazimiDegree}`);
console.log(`  station direct      ${cycle.direct}  ${cycle.directDegree}`);
console.log(`  post-shadow ends    ${cycle.post}`);
console.log("Source: Cazimi retrograde ephemeris, https://cazimi.live");
