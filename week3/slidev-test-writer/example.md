# Worked example: `packages/parser/src/utils.ts`

A real run of this skill's workflow. Use it as a reference for borderline classification calls.

## 1. Find existing tests

```
$ git grep -n "parseRangeString" -- '*.test.ts'
test/utils.test.ts:17:    expect(parseRangeString(5)).toEqual([1, 2, 3, 4, 5])
...
```

The colocated `packages/parser/src/utils.test.ts` exists but tests `isPathInsideRoots` from `fs.ts`. The real tests are in `test/utils.test.ts`, one `it` per function.

## 2. Rules vs. coverage

`parseRangeString(total, rangeStr)` turns `"1,3-5"` into slide numbers.

| Rule | Tested before? |
|---|---|
| missing / `all` / `*` → every slide | yes |
| `none` → `[]` | **no** |
| split on `,` or `;` | yes |
| `a-b` range; `a-` runs to the last slide | yes |
| dedupe, drop numbers > total, sort | **no** |

`parseAspectRatio(str)`: number or numeric string passes through; otherwise split on `:` `/` `x` `|` and return w/h; throw on NaN or h = 0. Untested: the `|` separator and empty input.

## 3. Probe (total = 5)

| Call | Result |
|---|---|
| `parseRangeString(5, 'none')` | `[]` |
| `parseRangeString(5, '')` | `[1,2,3,4,5]` |
| `parseRangeString(5, '3,1,1,2')` | `[1,2,3]` |
| `parseRangeString(5, '1,99')` | `[1]` |
| `parseRangeString(5, '3-99')` | `[3,4,5]` |
| `parseRangeString(5, 'abc')` / `'1\|3'` / `'5-3'` | `[]` |
| `parseRangeString(5, '0')` | `[0]` |
| `parseRangeString(5, '-3')` | `[0,1,2,3]` |
| `parseAspectRatio('4\|3')` | `1.333…` |
| `parseAspectRatio('')` / `'   '` | `0` |
| `parseAspectRatio('0/9')` | `0` |
| `parseAspectRatio('-16/9')` | `-1.777…` |

## 4. Classify

- **Correct → tested:** `none`, `''`, dedupe + sort, `1,99`, `3-99`, `4|3`.
- **Arguable → questions:** garbage, an unknown separator, and reversed ranges all silently return `[]` (should they throw?). `0/9` and `-16/9` are accepted (should a zero or negative ratio be rejected?).
- **Suspected bugs → reported:**
  - `'0'` → `[0]` and `'-3'` → `[0,1,2,3]`. Slides start at 1. Root cause: the final filter drops `i > total` but never `i < 1` (`utils.ts:30`). `'-3'` most likely *means* `[1,2,3]`, mirroring `'6-'`.
  - `parseAspectRatio('')` → `0`, but `'hello'` throws. Root cause: `+''` is `0`, so the numeric-string early return (`utils.ts:39`) fires before validation.

Note the reasoning for the bugs: each one contradicts something else *in the same function* (the `> total` filter, the `'6-'` form, the `'hello'` throw). That kind of internal inconsistency is the strongest signal.

## 5. Tests added (appended to the existing `it` blocks)

```ts
// it('page-range')
expect(parseRangeString(5, 'none')).toEqual([])
expect(parseRangeString(5, '')).toEqual([1, 2, 3, 4, 5])
expect(parseRangeString(5, '3,1,1,2')).toEqual([1, 2, 3])
expect(parseRangeString(5, '1,99')).toEqual([1])
expect(parseRangeString(5, '3-99')).toEqual([3, 4, 5])
// it('aspect-ratio')
expect(parseAspectRatio('4|3')).toEqual(4 / 3)
```

## 6. Verify

```
$ pnpm exec vitest run test/utils.test.ts   → 1 file, 8 tests passed
$ pnpm exec eslint test/utils.test.ts       → clean
$ git status --short                        → M test/utils.test.ts
```

An earlier full-suite run had rewritten an inline snapshot in `packages/slidev/node/syntax/integration.test.ts`. It was reverted with `git checkout --` before reporting.
