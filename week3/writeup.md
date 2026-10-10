# Week 3 Write-up

**Skill name**, and the repo you targeted:
> `slidev-test-writer` (in `week3/slidev-test-writer/`), targeting [slidevjs/slidev](https://github.com/slidevjs/slidev). It's installed in my local clone by symlinking it into `.claude/skills/`.


## Part I: The Workflow

**What the workflow is**, and why it's worth encoding:
> Given a function in Slidev, the workflow finds its existing tests, lists the function's rules and which ones are already covered, probes what the code actually returns for untested edge cases, and writes tests only for behavior that is clearly correct. Suspected bugs and unclear cases go into a report instead of into tests. It applies to every function in the repo and to every PR that touches one, and it goes wrong the same ways each time: tests land in the wrong file, expected values are guessed from reading the code, and whatever the code currently returns gets asserted as correct. That makes it a checklist I would otherwise have to re-explain on every run.


**The decision point** in it (what the agent has to judge, not just execute):
> When a probed result is surprising, the agent has to decide whether it is **correct** (write a test), **arguable** (don't test it, ask the maintainer), or a **suspected bug** (don't test it, report a root cause). For example, `parseRangeString(5, '0')` returns `[0]`, but slides start at 1. A naive test writer would assert `[0]` and lock the bug in. The strongest bug signal turned out to be internal inconsistency: the function drops numbers above `total` but never below 1, and `parseAspectRatio('hello')` throws while `parseAspectRatio('')` silently returns `0`. A secondary decision is where the test goes, because the obvious location is often wrong.

**What you learned running it manually** that you would not have guessed:
> - **Colocated test files can be misleading.** `packages/parser/src/utils.test.ts` sits next to `utils.ts` but tests `fs.ts`. The real tests for `utils.ts` are in `test/utils.test.ts`, and only grepping for the function name found them.
> - **`pnpm test --run <file>` runs the whole suite.** The `test` script is already `vitest test`, so the extra argument doesn't narrow it. Running one file needs `pnpm exec vitest run <file>`.
> - **A test run can modify files you never touched.** A full-suite run rewrote an inline PlantUML snapshot in `integration.test.ts`, so checking `git status` and reverting has to be part of the workflow.
> - **Reading the code wasn't enough to predict its output.** I didn't expect `'-3'` to return `[0, 1, 2, 3]` or an empty aspect ratio to return `0`. Probing first is what exposed both bugs.
> - **The built `dist/` can be stale.** My first probe imported the built package, so the skill's probe script imports the TypeScript source through `tsx` instead.
> - **Following the file's style has a cost.** Appending `expect`s to the existing `it` blocks matches the file, but the test count stays the same, and one failing assertion hides the ones after it in that block.


## Part II: The Skill

**Your description**, verbatim:
```
Writes vitest tests for functions in the Slidev repo (slidevjs/slidev). Finds existing tests, identifies untested behaviors and edge cases, probes what the code actually does, adds tests only for behavior that is clearly correct, and reports suspected bugs instead of writing tests that lock them in. Use when the user asks to write, add, or improve tests in Slidev, e.g. "write tests for this function", "add tests for parseRangeString", "cover the edge cases", "is this function tested?", or "increase test coverage for the parser".
```

**Why it's worded that way** (what a user would type to trigger it):
> The first sentence says **what** you get and the second says **when** to use it. My early drafts each had only one of the two. "Slidev" and "vitest" scope the skill, because without them it would fire on "write tests" in any repo and then run Slidev's `pnpm` commands there. The trigger phrases cover the different ways people ask: direct ("write tests for this function"), with a real function name ("add tests for parseRangeString"), and coverage-style ("cover the edge cases", "is this function tested?"). "Reports suspected bugs instead of writing tests that lock them in" names the skill's main risk and keeps it separate from bug-fix requests. The near-miss test ("fix the bug in parseRangeString…") confirmed that it doesn't fire on those.

**Judgment encoded in the body** (what it says to do when things are ambiguous, and what not to do):
> - **Classify before writing:** correct → test, arguable → open question, suspected bug → report with root cause and `file:line`. **When torn between correct and arguable, choose arguable**, since a missing test costs little and a wrong one misleads future contributors.
> - **Probe before asserting.** Expected values must be independent literals, never values recomputed with the code's own logic.
> - **If a new test fails, re-probe and reclassify.** Never edit the expected value just to make it pass.
> - **Grep for existing tests before choosing a file**, and ask before creating a new test file. Match the file's existing structure (append to existing `it` blocks; no new helpers or `describe` blocks for a few cases).
> - **Never:** assert buggy or arguable output, edit source code to make a test pass, use `pnpm test <file>`, update snapshots, or commit without being asked. After running, `git status` must show only the intended test files; revert anything else.
> - **A fixed four-part report:** tests added, suspected bugs (offering `it.fails`), open questions, verification.

**Supporting files**, if any, and why they aren't inline:

| File | Contents | Why it's separate |
|---|---|---|
| `conventions.md` | Where Slidev tests live (the misleading colocated `utils.test.ts`, top-level `test/`, fixture globbing), why `pnpm test <file>` doesn't narrow, snapshot churn, `it.fails` syntax, ESLint style | Repo details the agent only needs when it's unsure where a test goes or a command behaves oddly. The body keeps the one-line rule and links here for the explanation |
| `example.md` | The full manual run on `parseRangeString` / `parseAspectRatio`: rules vs. coverage, probe table, classification with root causes, tests added, verification | A reference for borderline classifications. It shows the judgment applied, but it's too long to load on every run |
| `scripts/probe.mjs` | Runs any exported function on a JSON list of inputs via `tsx` and prints each result or thrown error | Code the agent executes, not reads, so it costs no context. It makes "probe before asserting" a single exact command |


## Part III: Testing

**Triggering:**

| Prompt | Should fire? | Did it? |
|---|---|---|
| "write tests for parseTimeString" | Yes | Yes |
| "resolveFonts in packages/parser/src/config.ts doesn't have any tests yet, can you add some?" | Yes | Yes |
| "I'm worried the time string parser breaks on weird inputs like empty strings or negative numbers.Can you check what's covered and fill in the gaps?" | Yes | Yes |
| "Fix the bug in parseRangeString where '0' returns [0]. Change the source so slide 0 is filtered out." | No (near-miss) | No |

**End-to-end run** on your repo, and the result:
```
 ▐▛███▛█   Claude Code v2.1.295
▝▜██████▀  Opus 5.5 · Claude Enterprise
 ▝▝   ▝▝   ~/Documents/slidev


❯ write tests for parseTimeString                                               

⏺ Skill(slidev-test-writer)
  ⎿  Successfully loaded skill

  Ran 4 shell commands (ctrl+o to expand)

⏺ Probing done — classifying results now, then adding the clearly-correct cases
  to the existing test file.

⏺ Bash(cd /Users/aristotle_co/Documents/slidev; python3 - <<'EOF'
      p='packages/parser/src/timesplit/timestring.test.ts'…)
  ⎿   Test Files  1 passed (1)
           Tests  2 passed (2)
        Start at  14:14:05
     … +5 lines (ctrl+o to expand)
  ⎿  Updated packages/parser/src/timesplit/timestring.test.ts (+23 -0)
      14      expect(parseTimeString('1h4s')).toEqual({ seconds: 3604, re
          lative: false })
      15      expect(parseTimeString('1:1:1')).toEqual({ seconds: 3661, r
          elative: false })
      16      expect(parseTimeString('0.5years')).toEqual({ seconds: 1577
          8476, relative: false })
      17 +    expect(parseTimeString(90)).toEqual({ seconds: 90, relative
         +: false })                                                     
      18 +    expect(parseTimeString('90')).toEqual({ seconds: 90, relati
         +ve: false })                                                   
      19 +    expect(parseTimeString('1.5')).toEqual({ seconds: 1.5, rela
         +tive: false })                                                 
      20 +    expect(parseTimeString('+90')).toEqual({ seconds: 90, relat
         +ive: true })                                                   
      21 +    expect(parseTimeString('+1:30')).toEqual({ seconds: 90, rel
         +ative: true })                                                 
      22 +    expect(parseTimeString('1:2:3.5')).toEqual({ seconds: 3723.
         +5, relative: false })                                          
      23 +    expect(parseTimeString('1h 30m')).toEqual({ seconds: 5400, 
         +relative: false })                                             
      24 +    expect(parseTimeString('  1h  ')).toEqual({ seconds: 3600, 
         +relative: false })                                             
      25 +    expect(parseTimeString('1H')).toEqual({ seconds: 3600, rela
         +tive: false })                                                 
      26 +    expect(parseTimeString('1sec')).toEqual({ seconds: 1, relat
         +ive: false })                                                  
      27 +    expect(parseTimeString('2hr')).toEqual({ seconds: 7200, rel
         +ative: false })                                                
      28 +    expect(parseTimeString('2hrs')).toEqual({ seconds: 7200, re
         +lative: false })                                               
      29 +    expect(parseTimeString('1hour')).toEqual({ seconds: 3600, r
         +elative: false })                                              
      30 +    expect(parseTimeString('2hours')).toEqual({ seconds: 7200, 
         +relative: false })                                             
      31 +    expect(parseTimeString('1day')).toEqual({ seconds: 86400, r
         +elative: false })                                              
      32 +    expect(parseTimeString('2days')).toEqual({ seconds: 172800,
         + relative: false })                                            
      33 +    expect(parseTimeString('1week')).toEqual({ seconds: 604800,
         + relative: false })                                            
      34 +    expect(parseTimeString('1month')).toEqual({ seconds: 262974
         +6, relative: false })                                          
      35 +    expect(parseTimeString('1year')).toEqual({ seconds: 3155695
         +2, relative: false })                                          
      36    })
      37  
      38    it('should throw an error for invalid timestamp', () => {
     ...
      44      expect(() => parseTimeString('30,5')).toThrow('Invalid time
          stamp format')
      45      expect(() => parseTimeString('1 30')).toThrow('Invalid time
          stamp format')
      46      expect(() => parseTimeString('1.2.3')).toThrow('Invalid tim
          estamp format')
      47 +    expect(() => parseTimeString('1:2:3:4')).toThrow('Invalid t
         +imestamp format')                                              
      48 +    expect(() => parseTimeString('1.2.3s')).toThrow('Invalid ti
         +mestamp value: 1.2.3')                                         
      49 +    expect(() => parseTimeString('1h30')).toThrow('Unknown time
         +stamp remaining: 30')                                          
      50 +    expect(() => parseTimeString('++10s')).toThrow('Unknown tim
         +estamp remaining: +')                                          
      51    })
      52  })

⏺ I added 23 assertions to the existing tests for parseTimeString, and they
  pass. I also found two likely bugs, which I didn't write tests for.

  Tests added

  They go in packages/parser/src/timesplit/timestring.test.ts, inside its two
  existing it blocks.

  Valid input:
  - Plain numbers: a number 90, the strings '90' and '1.5', and the relative
    form '+90'.
  - Relative colon form: '+1:30' gives 90 seconds with relative: true.
  - Decimal seconds in h:m:s: '1:2:3.5' gives 3723.5.
  - Spacing and case: a space between pairs ('1h 30m'), surrounding spaces ('  
    1h  '), and uppercase units ('1H').
  - Unit aliases with no tests yet: sec, hr, hrs, hour, hours, day, days, week,
    month, year.

  Errors:
  - '1:2:3:4': too many colon parts.
  - '1.2.3s': "Invalid timestamp value".
  - '1h30': a trailing number with no unit.
  - '++10s': a doubled +.

  Suspected bugs (no tests written)

  1. The colon form accepts values that aren't plain numbers. '1:Infinity' gives
     Infinity seconds and '1:1e1' gives 70. I'd expect both to throw "Invalid
     timestamp format". The cause is that the parts go through .map(Number) and
     are only checked for NaN (timestring.ts:35, timestring.ts:54). An Infinity
     would end up in the timer and timesplits, the same way NaN used to.
  2. Negative values are accepted inconsistently. '1:-30' gives 30, so a minus
     sign inside a part quietly subtracts. '-10' gives -10 and the number -5
     passes through unchanged. Meanwhile '-10s' throws. The plain-number and
     colon branches never check the sign (timestring.ts:57, timestring.ts:60). A
     negative duration or timesplit doesn't make sense.

  I can record either of these as an it.fails test if you'd like.

  Open questions

  - Should '' and '+' throw? Right now they give 0 seconds.
  - Should empty colon parts be allowed? '1:' gives 60 and ':30' gives 30.
  - Should parts over 60 be allowed, like '1:90' giving 150?
  - Should '5M' mean 5 minutes, since units are case-insensitive? Some people
    might read M as months.
  - Should these currently rejected forms be accepted:
    - '10 s', with a space between the number and its unit ('3mins 5secs'
      already allows spaces between pairs)
    - '1d' as short for a day, given that h and m are accepted
    - '1e3' as a plain number

  Verification

  - pnpm exec vitest run packages/parser/src/timesplit/timestring.test.ts: 2/2
    tests passed.
  - pnpm exec eslint on the file: no problems.
  - git status --short: shows the test file and test/utils.test.ts. The second
    one already had your uncommitted changes before I started, and I didn't
    touch it.

✻ Cooked for 1m 3s · done 2:14 PM
```


## Submission
1. `Command (⌘) + F` for `TODO`. No results means you're done.
2. Confirm the skill directory itself is committed under `week3/`.
3. Push all changes to your remote repository and submit via Gradescope.
