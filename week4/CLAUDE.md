# Day.js

Immutable, Moment.js-compatible date library. The core (`src/index.js`) must stay under a **2.99 KB gzipped** size limit, so new features go in plugins, not the core. Plain ES6 JavaScript compiled with Babel; there is no TypeScript source, only hand-written `.d.ts` files.

## Layout

- `src/index.js` holds the `Dayjs` class and the `dayjs()` factory. `src/utils.js` (exposed to plugins as `this.$utils()`) and `src/constant.js` hold unit names and regexes.
- `src/plugin/<name>/index.js` is always one directory per plugin with an `index.js`. Signature: `export default (option, DayjsClass, dayjsFactory) => {}`, usually written `(o, c, d)`.
- `src/locale/<code>.js` holds 140+ locales. Each one `import dayjs from 'dayjs'`s (a bare specifier, not a relative path), calls `dayjs.locale(locale, null, true)`, and `export default locale`.
- `types/index.d.ts`, `types/plugin/<name>.d.ts`, `types/locale/` hold the typings, maintained by hand.
- `test/*.test.js` covers the core, `test/plugin/<name>.test.js` the plugins, and `test/locale/<code>.test.js` the locales. `test/__mocks__/dayjs.js` maps `'dayjs'` to `src`, which is how locale imports resolve under Jest.
- `build/` holds the rollup scripts. `docs/` is stale translated READMEs: the real docs live at day.js.org in another repo, so don't update them for API changes.

## Commands

Use Node LTS and `npm ci`. Don't use `npm install`, because it rewrites `package-lock.json`.

- Lint (CI runs this, and it's also a git pre-commit hook): `npm run lint`
- One test file: `npx jest test/plugin/isToday.test.js --coverage=false`
- Full suite, as CI runs it: `TZ=UTC npm test`
  - Without `TZ=UTC`, the final run uses your machine's timezone, and ~6 DST/`dayOfYear`/`localizedFormat` tests fail outside UTC. That is not a regression.
  - `npm test -- <file>` does **not** narrow the run, because the script chains 8 timezone runs before the final `jest`. Use `npx jest <file>`.
  - It enforces **100% line coverage** over `src/**`, so new branches need tests or the run fails.
  - The output is ~750 lines: 9 runs, a coverage table, and harmless "Handlebars: Access has been denied" warnings. Judge it by the exit code, not by piping through `tail`: `TZ=UTC npm test > /tmp/dayjs-test.log 2>&1; echo $?`, then `grep -E '^(FAIL|Tests:)' /tmp/dayjs-test.log`.
- Build: `NODE_OPTIONS=--openssl-legacy-provider npm run build`. Without the flag, the `size` step crashes on Node ≥17 with `ERR_OSSL_EVP_UNSUPPORTED`. ESM build: `npm run babel`.

## Conventions

- Style is airbnb-base with **no semicolons**, **no trailing commas**, 2-space indent, and no file extensions in imports.
- Internal state uses `$`-prefixed fields: `$d` (native Date), `$y $M $D $W $H $m $s $ms`, `$L` (locale name), `$u` (UTC flag), `$x` (plugin extras), `$offset`. Methods never mutate `this`. They return a new instance (`this.clone()`, `Utils.w(date, this)`).
- Plugins extend `c.prototype`. To override a method, save the old one and fall through: `const oldAdd = proto.add; proto.add = function (n, u) { … return oldAdd.bind(this)(n, u) }`. Use `function`, not arrows, so `this` binds.
- Normalize units with `this.$utils().p(units)` and compare against the constants in `src/constant.js` (`M`, `D`, `Q`, …).
- Tests: plain top-level `it(...)` (rarely `describe`). Import from `'../../src'` and `'../../src/plugin/<name>'`, then `dayjs.extend(...)`. Wrap in `MockDate.set(new Date())` / `MockDate.reset()` in `beforeEach`/`afterEach`. Assert parity with Moment where it exists: `expect(dayjs(x).foo().format()).toBe(moment(x).foo().format())`.
- Commits use Conventional Commits: `fix(plugin): …`, `feat: …`, `chore: …`. semantic-release derives versions from them.

## Guardrails

- **Adding a plugin requires 3 files**: `src/plugin/<name>/index.js`, `types/plugin/<name>.d.ts` (`declare const plugin: PluginFunc; export = plugin`, plus a `declare module 'dayjs' { interface Dayjs { … } }` augmentation for any new methods; `test/plugin/declarations.test.js` fails if the file is missing), and `test/plugin/<name>.test.js`.
- **Adding a locale**: line 1 must be exactly `// English Name [code]`. The build parses it into `locale.json`, and `test/locale/keys.test.js` fails without it. `name` must equal the filename and be lowercase.
- **Never edit build output.** `plugin/`, `locale/`, `esm/`, `dayjs.min.js`, `index.d.ts` and `locale.json` at the **repo root** are gitignored artifacts copied from `src/` and `types/`. Edit `src/plugin/...` and `types/...` instead.
- Don't edit `CHANGELOG.md` (semantic-release writes it) or `patches/` (patch-package for the release bot).
- PRs target `dev`. `master` is release-only, and pushing to it publishes to npm.
- Pinned dev deps are old on purpose (Jest 22, ESLint 4, `moment@2.29.2`, which tests compare against). Don't upgrade them as a side effect.
