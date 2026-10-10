---
name: slidev-test-writer
description: Writes vitest tests for functions in the Slidev repo (slidevjs/slidev). Finds existing tests, identifies untested behaviors and edge cases, probes what the code actually does, adds tests only for behavior that is clearly correct, and reports suspected bugs instead of writing tests that lock them in. Use when the user asks to write, add, or improve tests in Slidev, e.g. "write tests for this function", "add tests for parseRangeString", "cover the edge cases", "is this function tested?", or "increase test coverage for the parser".
---

# Slidev Test Writer

Add tests that pin down Slidev's *intended* behavior, and surface suspected bugs rather than encoding them as "expected". Run every command from the Slidev repo root.

## Workflow

1. **Find the existing tests first.** They are often not next to the source file, and a colocated `*.test.ts` may test a different file entirely.
   ```
   git grep -n "<functionName>" -- '*.test.ts'
   ```
   No hits? Decide where the new tests go using [conventions.md](conventions.md#where-tests-live).

2. **List the rules, then the gaps.** Read the function and write its rules in plain language: each branch, keyword, separator, and filter. Mark which rules the existing tests already cover. Gaps are the uncovered rules plus edge cases: empty or missing input, boundaries (0, 1, max, max+1), duplicates, ordering, reversed ranges, malformed input, unexpected separators.

3. **Probe before you assert.** Never write an expected value from reading the code alone. Run it:
   ```
   pnpm exec tsx ${CLAUDE_SKILL_DIR}/scripts/probe.mjs <source.ts> <exportName> '<JSON list of argument lists>'
   ```

4. **Classify every probed result before writing any test.**

   | Bucket | How to recognize it | Action |
   |---|---|---|
   | Correct | Matches the docstring, the function's other rules, and what a Slidev user would want | Write a test |
   | Arguable | Defensible but unspecified, e.g. garbage input silently returns `[]` | No test. List as an open question |
   | Suspected bug | Contradicts the docstring, the function's own other branches, or the domain (e.g. slide `0` when slides start at 1) | No test. Report it with a root cause |

   When torn between correct and arguable, choose arguable. A missing test costs little; a test that locks in the wrong choice misleads every future contributor.

5. **Write the tests in the file's existing style.** If the file groups many `expect`s in one `it` per function, append there. Don't add new `describe` blocks, helpers, or fixtures for a handful of cases. Expected values must be independent literals (`[1, 2, 3]`, `4 / 3`), never recomputed with the code's own logic.

6. **Verify.**
   ```
   pnpm exec vitest run <test-file>
   pnpm exec eslint <test-file>
   git status --short
   ```
   Every new test must pass. A failure means the probe and the test disagree: re-probe and reclassify, never just edit the expected value to match. `git status` must list only the test files you meant to change. Revert anything else (`git checkout -- <file>`), such as snapshots a run rewrote.

## Never

- Assert output you classified as a bug or as arguable.
- Edit source code to make a test pass. Fixing is a separate decision for the user.
- Run one file with `pnpm test <file>`. It runs the whole suite (see [conventions.md](conventions.md#running-tests)).
- Update snapshots (`-u`) or commit, unless the user asks.

## Report

End with these four sections, in this order:

1. **Tests added**: the file, and each case with the behavior it covers.
2. **Suspected bugs**: input → actual vs. expected, plus a one-line root cause citing `file:line`. Offer to record each as an `it.fails` test.
3. **Open questions**: the arguable cases, phrased as decisions for a maintainer.
4. **Verification**: the commands you ran and their results.

For a complete worked run on `parseRangeString` and `parseAspectRatio`, see [example.md](example.md).
