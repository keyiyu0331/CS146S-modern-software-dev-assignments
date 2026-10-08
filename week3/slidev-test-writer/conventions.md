# Slidev test conventions

Read this when you're unsure where a test belongs, a command behaves unexpectedly, or `git status` shows files you didn't touch.

## Where tests live

- `vitest.config.ts` defines two kinds of test projects: `packages/*` (colocated tests) and `test` (top-level suite).
- Most tests are in the top-level `test/` directory, named by area: `test/utils.test.ts`, `test/parser.test.ts`, and so on. They import source by relative path, e.g. `import { parseRangeString } from '../packages/parser/src'`.
- Some packages also have colocated tests. **A colocated file's name does not tell you what it tests.** `packages/parser/src/utils.test.ts` tests `isPathInsideRoots` from `fs.ts`, while `packages/parser/src/utils.ts` is tested in `test/utils.test.ts`. Always grep.

Deciding where a new test goes:

1. The function already has tests → add to that file.
2. No tests, but other functions from the same source file are tested → add to that file.
3. Neither → the `test/<area>.test.ts` file whose name matches the area. Ask the user before creating a new test file.

`test/fixtures/markdown/*.md` is globbed by `test/parser.test.ts`: every file there becomes a snapshot test. Adding a fixture changes snapshots, so don't add one for a unit-level case.

## Running tests

- `package.json` defines `"test": "vitest test"`. That `test` is already a file filter, so `pnpm test --run test/utils.test.ts` still runs all ~34 files. To run one file:
  ```
  pnpm exec vitest run test/utils.test.ts
  ```
- One test by name: `pnpm exec vitest run <file> -t "<test name>"`.
- Whole suite, if you touched shared fixtures or helpers: `pnpm exec vitest run`.

## Snapshots

- The suite uses file snapshots (`test/__snapshots__/`) and inline snapshots. A run can leave a snapshot changed in a file you never edited. This was observed with the PlantUML `code="…"` string in `packages/slidev/node/syntax/integration.test.ts` after a full-suite run.
- It isn't your change, so revert it: `git checkout -- <file>`. Never pass `-u` / `--update` unless the user asked to update snapshots.

## Recording a suspected bug with `it.fails`

Only when the user agrees. The test asserts the *correct* behavior and passes while the bug exists. Once someone fixes the bug, it fails, which reminds them to remove `.fails`.

```ts
it.fails('page-range excludes slide 0', () => {
  expect(parseRangeString(5, '0')).toEqual([])
})
```

## Style

ESLint uses `@antfu/eslint-config`: single quotes, no semicolons, 2-space indent. `pnpm exec eslint --fix <file>` fixes formatting.

## Probing

`scripts/probe.mjs` imports TypeScript source through `tsx`, so it needs no build. Don't probe `packages/*/dist`: it reflects the last build and can be stale relative to `src`.
