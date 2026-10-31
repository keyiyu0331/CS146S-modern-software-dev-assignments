# Week 4 Write-up

**Repo chosen** and link to your fork:
> [iamkun/dayjs](https://github.com/iamkun/dayjs). Fork: https://github.com/keyiyu0331/dayjs. The file is committed on the fork's `dev` branch, which is the repo's default branch.

**File you wrote** (`AGENTS.md` or `CLAUDE.md`):
> `CLAUDE.md`, at the root of the fork and copied to `week4/CLAUDE.md`. I chose it over `AGENTS.md` because Part III runs Claude Code, which loads `CLAUDE.md` automatically.


## Part I: Exploration

| | Finding |
|---|---|
| Build / run | `npm ci`, then `NODE_OPTIONS=--openssl-legacy-provider npm run build` (rollup UMD builds of the core, every plugin and every locale, followed by a size-limit check). Without the flag, the `size` step crashes on Node ≥17 with `ERR_OSSL_EVP_UNSUPPORTED`. The release workflow sets the same flag. `npm run babel` builds `esm/`. It's a library, so there is nothing to "run". |
| Test | `TZ=UTC npm test` runs the full suite as CI does: 8 timezone-pinned Jest runs, then a full run with a **100% line-coverage threshold**. For a single file: `npx jest test/plugin/isToday.test.js --coverage=false`. |
| Lint / format | `npm run lint` (ESLint 4, airbnb-base, no semicolons, no trailing commas). It's also a git pre-commit hook through the `pre-commit` package. `npm run prettier` only formats `docs/**/*.md`. |
| Key directories and entry points | `src/index.js` (the `Dayjs` class and `dayjs()` factory), `src/utils.js`, `src/constant.js`. `src/plugin/<name>/index.js` holds 36 plugins and `src/locale/<code>.js` 143 locales. `types/` holds the hand-written `.d.ts` files. `test/` mirrors `src/`. `build/` holds the rollup scripts. |
| Unstated conventions | Plugins are `(o, c, d) => {}` and patch `c.prototype`, saving the old method and falling through to `oldX.bind(this)(...)`. Internal state uses `$` fields (`$d`, `$y`, `$M`, `$L`, `$u`, `$x`, `$offset`). Methods never mutate `this`. Units are normalized with `this.$utils().p()`. Tests are flat `it()` blocks wrapped in `MockDate` and assert parity with `moment`. Locales import the bare `'dayjs'`, which `test/__mocks__/dayjs.js` maps to `src` under Jest. Line 1 of every locale must be `// Name [code]`. Every plugin needs a `types/plugin/<name>.d.ts`, which a test enforces. Commits use Conventional Commits because semantic-release reads them. |
| Off-limits (generated, vendored) | Build output at the repo root (`plugin/`, `locale/`, `esm/`, `dayjs.min.js`, `index.d.ts`, `locale.json`) is gitignored, but it shares names with `src/plugin` and `types/index.d.ts`. `CHANGELOG.md` is written by semantic-release. `patches/` is patch-package for the release bot. `docs/` is stale, because the real docs moved to day.js.org. Pushing to `master` publishes to npm; PRs target `dev`. |

**How you figured it out**: what you asked the agent, what you had to read yourself:
> I had Claude Code clone the repo and read `package.json`, `build/*.js`, the three workflows, `.eslintrc.json`, `.releaserc`, `.gitignore`, and a sample of plugins, locales and tests. Reading wasn't enough: actually running every command is what turned up most of what ended up in the file.
> - **Plain `npm test` failed on a clean checkout.** 6 tests failed in `timezone`, `dayOfYear` and `localizedFormat`. The script's last `jest` run isn't pinned to a timezone, so it used my laptop's `America/Los_Angeles`. CI runs on UTC, and `TZ=UTC npm test` passed all 794 tests.
> - **`npm run build` failed** in its `size` step until I copied `NODE_OPTIONS=--openssl-legacy-provider` from `release.yml`.
> - **`npm install` rewrote 1,300 lines of `package-lock.json`.** `npm ci` doesn't.
> - **Two tests enforce structure that nothing documents.** `declarations.test.js` fails if a plugin has no `.d.ts`. `locale/keys.test.js` checks the line-1 comment, which `build/index.js` also parses with a regex into `locale.json`. I only found both by reading the test files themselves.


## Part II: The File

**Anything you deliberately left out**, and why:
> - **The API itself** (`format` tokens, `add`/`subtract`, and so on). It's documented at day.js.org, and a model can read `src/index.js` when it needs to.
> - **Installation and browser/CDN usage.** That's a README concern, and it's for users of the library, not contributors.
> - **The Sauce Labs / Karma browser tests** (`npm run test:sauce`). They need credentials and CI doesn't run them, so an agent can't use them.
> - **Generic rules** like "write tests" or "keep functions small". The only testing guidance in the file is repo-specific: the 100% line threshold, the Moment parity idiom and `MockDate`.
> - **A per-plugin catalog.** `ls src/plugin` gives you that for free, and it would just go stale.

**The hardest call** on what to include:
> The `$`-field glossary (`$d $y $M $D $W $H $m $s $ms $L $u $x $offset`). It's the closest thing in the file to information an agent could rediscover by reading `init()` in `src/index.js`. But every plugin touches these fields, the names are cryptic (`$W` is the weekday, `$D` the date), and getting them wrong silently breaks immutability or UTC handling. I kept it to one line. I cut the bigger section I'd considered on how `parseDate` handles each input type, because that's only relevant to a few tasks.


## Part III: Trying It Out

Both tasks ran as fresh headless `claude -p` sessions started in the fork's root, so `CLAUDE.md` was the only context they had.

| # | Task | Did the agent use your commands and conventions? |
|---|---|---|
| 1 | "Run the test suite and tell me whether it passes." | **Yes.** Its first test command was `TZ=UTC npm test`, and it said it was running the suite "the way CI does". It reported 794/794 tests passing and the 100% line threshold met, which matches what I got. **But** it piped the output through `\| tail -60`, which throws away the exit code. To confirm the 8 earlier timezone runs had passed, it had to reason from the `&&` chain in `package.json`. It also spent a sentence explaining that the Handlebars warnings were harmless. |
| 2 | "Add a small plugin called isWeekend … make sure lint and tests pass. Don't commit." | **Yes, on structure and style.** It looked at `isToday` as a template, created exactly the three files the guardrail lists (`src/plugin/isWeekend/index.js`, `types/plugin/isWeekend.d.ts` with the `declare module` augmentation, and `test/plugin/isWeekend.test.js`), and used the `(o, c)` / `c.prototype` / `function` pattern, `MockDate` hooks and flat `it()` blocks with no semicolons. It didn't touch the root `plugin/` build output. It didn't add a Moment comparison because Moment has no `isWeekend`, which was the right call. It ran `npm run lint` and `TZ=UTC npm test`, both piped through `tail` again. I re-ran both myself: lint exits 0, tests exit 0, 796/796 pass, and the new plugin has 100% coverage. It never used the single-file `npx jest` command, which was fine for a change this small. |

**One thing you'd change** about the file after watching it get used:
> **Make the full-suite command report its result in a way the agent can't lose.** Both runs did `TZ=UTC npm test 2>&1 | tail -N`. That hides the exit status of 9 chained runs and roughly 750 lines of output, so a failure in an early timezone run would only show up as a missing summary line. I added this to the Commands section: the output is ~750 lines, the Handlebars warnings are noise, and you should run `TZ=UTC npm test > /tmp/dayjs-test.log 2>&1; echo $?` and then grep for `^(FAIL|Tests:)`. A second change I'd consider is moving the guardrail about root `plugin/` vs `src/plugin/` closer to the Layout section. The agent never went near the build output, but that's partly because I deleted the build artifacts before the run.


## Submission
1. `Command (⌘) + F` for `TODO`. No results means you're done.
2. Push all changes to your remote repository and submit via Gradescope.
