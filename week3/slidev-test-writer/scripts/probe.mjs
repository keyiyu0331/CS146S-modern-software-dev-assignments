// Print what a Slidev function actually returns for a list of inputs.
// Imports the TypeScript source through tsx, so no build is needed and the
// result always reflects the current source (packages/*/dist can be stale).
//
// Usage, from the Slidev repo root:
//   pnpm exec tsx <skill-dir>/scripts/probe.mjs <source.ts> <exportName> '<JSON list of argument lists>'
// Example:
//   pnpm exec tsx <skill-dir>/scripts/probe.mjs packages/parser/src/utils.ts parseRangeString '[[5, "0"], [5, "-3"]]'

import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import { inspect } from 'node:util'

const [file, name, casesJson] = process.argv.slice(2)
if (!file || !name || !casesJson) {
  console.error('usage: probe.mjs <source.ts> <exportName> \'<JSON list of argument lists>\'')
  process.exit(2)
}

let cases
try {
  cases = JSON.parse(casesJson)
}
catch (e) {
  console.error(`cases must be JSON, e.g. '[[5, "1-3"], [5, ""]]': ${e.message}`)
  process.exit(2)
}
if (!Array.isArray(cases) || !cases.every(Array.isArray)) {
  console.error('cases must be a list of argument lists, e.g. \'[["16/9"], [""]]\'')
  process.exit(2)
}

const mod = await import(pathToFileURL(resolve(process.cwd(), file)).href)
const fn = mod[name]
if (typeof fn !== 'function') {
  console.error(`"${name}" is not an exported function of ${file}. Exports: ${Object.keys(mod).join(', ')}`)
  process.exit(2)
}

const show = v => inspect(v, { depth: 4, breakLength: Infinity })
for (const args of cases) {
  const call = `${name}(${args.map(show).join(', ')})`
  try {
    console.log(`${call} => ${show(await fn(...args))}`)
  }
  catch (e) {
    console.log(`${call} => THROWS ${e.message}`)
  }
}
