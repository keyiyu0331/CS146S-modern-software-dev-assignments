# Week 5 Write-up

**Repos chosen**, and how they differ:

| Repo | Language | Size | Age / activity | Backing | Audited commit |
|---|---|---|---|---|---|
| [facebook/react](https://github.com/facebook/react) | JavaScript/Flow, TypeScript, Rust | Huge: 73 MB shallow clone, monorepo with 7 applications | Since 2013; active (last commit 2026-10-30) | Corporate (Meta) | `16453bcd12becf76340caa793d185cec1b80ebef` |
| [scrapy/scrapy](https://github.com/scrapy/scrapy) | Python | Large: 9.5 MB, 1 application | Since 2008; active (last commit 2026-10-30) | Open-source community, with Zyte (the company behind Scrapy) employing core maintainers | `51c10b14fca6d272587a5c23cf3ae8effdff16cd` |
| [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) | Python, JavaScript | Medium: 6.3 MB, 1 application | Since 2022; **inactive** (last commit 2024-07-27) | Single maintainer | `82a973c04367123ae98bd9abdf80d9eda9b910e2` |

My first choice was yt-dlp. I replaced it with scrapy because yt-dlp's `.NO_AI/README.md` tells agents to refuse to work with the repo, and Droid stopped the audit there.


## Part I: Report Results

**Categories.** The tables below use the 9 categories from Factory's detailed report, not the 8 pillars in the Agent Readiness blog post. The report has no separate Code Quality pillar: complexity, duplication, large-file and modularization checks are part of Style & Validation. It also adds Task Discovery (issue and PR hygiene) and Product & Experimentation. All three reports put every criterion in the same category, so the tables can be compared directly.

**Scoring.** Each criterion is pass/fail. react is scored per application (n/7), and a partial score like 4/7 counts as failed but contributes 4/7 to the category pass rate. Skipped (N/A) criteria are left out.

### Summary

| Repo | Maturity level | Blocking the next level | Pillar scores |
|---|---|---|---|
| react | **Level 3/5**, 52% (30 passed, 42 failed, 12 skipped) | Of the example Level 4 criteria Factory names, react fails **Flaky Test Detection** (4/7) and passes Fast CI Feedback and Deployment Frequency. Its Level 3 examples are also weak: Integration Tests 4/7, Distributed Tracing 0/7, Metrics 4/7. | Per-category pass rates in the table below |
| scrapy | **Level 4/5**, 61% (40 passed, 26 failed, 18 skipped) | Factory doesn't publish specific Level 5 criteria ("self-improving systems"), so nothing can be named. scrapy reached Level 4 while failing two of the three example Level 4 criteria: **Fast CI Feedback** (29.5-minute average) and **Deployment Frequency**. | Per-category pass rates in the table below |
| stable-diffusion-webui | **Level 3/5**, 42% (30 passed, 42 failed, 12 skipped) | Of the example Level 4 criteria, it fails **Deployment Frequency** (last release Feb 2025) and **Flaky Test Detection**, and passes Fast CI Feedback. Level 3 example: Distributed Tracing fails. | Per-category pass rates in the table below |

*Where the blocking column comes from:* neither the CLI output nor the downloaded report says which level a criterion belongs to, and Factory hasn't published the full mapping. The column uses the example criteria Factory gives for each level in its [Agent Readiness overview](https://docs.factory.com/docs/agent-readiness/overview). Level 2: AGENTS.md, devcontainer, pre-commit hooks, branch protection. Level 3: integration tests, secret scanning, distributed tracing, metrics. Level 4: fast CI feedback, deployment frequency, flaky test detection. So the column is a partial list, not the complete set of blocking criteria. Factory's two descriptions of the 80% gate also disagree. The [blog post](https://factory.com/news/agent-readiness) requires 80% of the current level plus all earlier levels. The docs require 80% of the previous level.

| Category (pass rate) | react | scrapy | stable-diffusion-webui |
|---|---|---|---|
| Style & Validation | 55% | 58% | 25% |
| Build System | 90% | 62% | 50% |
| Testing | 46% | 80% | 50% |
| Documentation | 71% | 71% | 25% |
| Development Environment | 50% | 0% | 50% |
| Debugging & Observability | 21% | 60% | 45% |
| Security | 14% | 67% | 44% |
| Task Discovery | 50% | 50% | 75% |
| Product & Experimentation | 0% | 0% | 0% |

### Failed criteria by pillar

Criteria scoring below full marks. react's partial scores are shown as n/7.

| Category | react | scrapy | stable-diffusion-webui |
|---|---|---|---|
| Style & Validation | Naming Consistency (0/7); Cyclomatic Complexity (0/7); Large File Detection; Duplicate Code Detection (0/7); Code Modularization Enforcement (1/7); Pre-commit Hooks (3/7) | Cyclomatic Complexity; Large File Detection; Duplicate Code Detection; Code Modularization Enforcement; Technical Debt Tracking | Type Checker; Pre-commit Hooks; Strict Typing; Naming Consistency; Cyclomatic Complexity; Large File Detection; Duplicate Code Detection; Code Modularization Enforcement; Technical Debt Tracking |
| Build System | Unused Dependencies Detection (0/7); Heavy Dependency Detection (2/7) | Automated PR Review Generation; Fast CI Feedback (29.5 min avg); Deployment Frequency; Feature Flag Infrastructure; Unused Dependencies Detection | Dependencies Pinned; Automated PR Review Generation; Deployment Frequency; Release Notes Automation; Unused Dependencies Detection; Release Automation; Dead Feature Flag Detection |
| Testing | Unit Tests Runnable (0/7, `chalk` missing); Test Coverage Thresholds (0/7); Unit Tests Exist (3/7); Integration Tests Exist (4/7); Test Performance Tracking (4/7); Flaky Test Detection (4/7); Test Isolation (4/7); Interactive QA Exists (4/7); Interactive QA Runnable (4/7); Test File Naming Conventions (5/7) | Unit Tests Runnable (Twisted missing); Flaky Test Detection | Test Performance Tracking; Flaky Test Detection; Test Coverage Thresholds; Test File Naming Conventions; Test Isolation |
| Documentation | AGENTS.md File (CLAUDE.md not accepted); AGENTS.md Freshness Validation | Skills Configuration; AGENTS.md Freshness Validation | AGENTS.md File; Skills Configuration; Documentation Freshness; API Schema Docs; Service Architecture Documented; AGENTS.md Freshness Validation |
| Development Environment | Dev Container | Dev Container; Environment Template | Dev Container |
| Debugging & Observability | Distributed Tracing (0/7); Error Tracking Contextualized (0/7); Runbooks Documented; Health Checks (0/7); Circuit Breakers (0/7); Alerting Configured (1/7); Deployment Observability (1/7); Structured Logging (3/7); Code Quality Metrics Dashboard (3/7); Metrics Collection (4/7); Profiling Instrumentation (4/7) | Error Tracking Contextualized; Alerting Configured; Runbooks Documented; Deployment Observability | Distributed Tracing; Error Tracking Contextualized; Alerting Configured; Runbooks Documented; Deployment Observability; Circuit Breakers |
| Security | CODEOWNERS File; Dependency Update Automation (Dependabot disabled); Gitignore Comprehensive (`.env`); DAST Scanning (0/7); Sensitive Data Log Scrubbing (0/7); Minimum Dependency Release Age | CODEOWNERS File; Gitignore Comprehensive (`.env`) | Dependency Update Automation; Gitignore Comprehensive (`.env`); DAST Scanning; Secrets Management; Minimum Dependency Release Age |
| Task Discovery | Issue Labeling System (no priority labels); Backlog Health (13/50 issues qualify) | Issue Labeling System (no priority labels); PR Templates | Issue Labeling System (no priority labels) |
| Product & Experimentation | Product Analytics Instrumentation (0/7); Error to Insight Pipeline (0/7) | Product Analytics Instrumentation; Error to Insight Pipeline | Product Analytics Instrumentation; Error to Insight Pipeline |

### The report's top remediation suggestions

| Repo | Suggestions (each CLI report's 3 action items. The downloaded report has none.) |
|---|---|
| react | 1. Add a root `AGENTS.md` with setup, bounded test commands and per-application QA steps, and check its commands in CI. 2. Add real tests and complete smoke-test paths for healthcheck, MCP and React Analyzer, and enforce coverage thresholds. 3. Turn on dependency-update PRs, add secret/security scanning, and fix the repo-wide `.env` exclusions. |
| scrapy | 1. Add a reproducible dev environment, plus CI smoke checks for test collection, CLI usage and `AGENTS.md` commands. 2. Turn on file-size, complexity, duplication, technical-debt-marker and unused-dependency checks. 3. Add secret-file ignores, secret scanning, CODEOWNERS and a complete PR template. |
| stable-diffusion-webui | 1. Add an `AGENTS.md` covering setup, checks and CPU/API QA, and check its commands in CI. 2. Add static typing, pre-commit checks, complexity limits and a blocking coverage threshold. 3. Commit reproducible dependency lockfiles, exclude secret files, and set up dependency updates and secret scanning. |

### Raw output

For each repo: the detailed report downloaded from app.factory.ai (`reports/<repo>.md`) and the original CLI output, which includes the action items (`reports/cli/<repo>.md`).

<details>
<summary>react: detailed report</summary>

```markdown
# Agent Readiness Report: react

**Level:** 3/5  
**Overall Score:** 52%  
**Generated:** 2026-10-31 00:45:07 UTC  
**Commit:** `16453bc`  
**Branch:** main  

## Summary

| Metric | Value |
|--------|-------|
| Total Criteria | 84 |
| Passed | 30 |
| Failed | 42 |
| Skipped | 12 |

## Pass Rate by Category

| Category | Pass Rate |
|----------|-----------|
| Style & Validation | 55% |
| Build System | 90% |
| Testing | 46% |
| Documentation | 71% |
| Development Environment | 50% |
| Debugging & Observability | 21% |
| Security | 14% |
| Task Discovery | 50% |
| Product & Experimentation | 0% |

## Style & Validation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Naming Consistency | 0/7 | 🔴 Failed | No explicit naming enforcement found for the applications. Root camelcase, id-match, and react/jsx-pascal-case rules are disabled; compiler/playground configuration has no replacement naming conven... |
| Cyclomatic Complexity | 0/7 | 🔴 Failed | Root ESLint explicitly disables complexity. No active complexity threshold or alternate analyzer was found for any application. |
| Large File Detection | 0/1 | 🔴 Failed | No file-size hook, max-lines rule, CI size threshold for individual files, or Git LFS configuration found. Bundle-size reporting does not enforce source-file size. |
| Duplicate Code Detection | 0/7 | 🔴 Failed | No jscpd, CPD, Sonar, or other duplicate-code detector configured for any application. |
| Code Modularization Enforcement | 1/7 | 🔴 Failed | Runtime Rollup tooling enforces renderer host-config forks and rejects forbidden fbjs imports. No comparable application-boundary enforcement found for the other six targets. |
| Pre-commit Hooks | 3/7 | 🔴 Failed | scripts/git/pre-commit is an opt-in checked-in ESLint hook for staged .js files, covering runtime and both DevTools targets. It does not cover the TypeScript application sources; no TS-capable hook... |
| Linter Configuration | 7/7 | 🟢 Passed | Root ESLint covers runtime/DevTools JavaScript. Compiler ESLint covers its TypeScript packages; playground has next/core-web-vitals configuration. |
| Type Checker | 7/7 | 🟢 Passed | Runtime and both DevTools targets use Flow-checked shared code. Playground and all three compiler tools have TypeScript configurations; CI runs Flow and compiler validation workflows. |
| Code Formatter | 7/7 | 🟢 Passed | Root Prettier configuration and scripts cover JavaScript/TypeScript/TSX across all seven applications, including compiler sources. CI runs prettier-check. |
| Strict Typing | 7/7 | 🟢 Passed | Root ESLint-plugin/compiler TypeScript uses @tsconfig/strictest, DevTools shared modules use @flow strict-local, playground enables strict:true, and the three compiler tools extend @tsconfig/strict... |
| Dead Code Detection | 7/7 | 🟢 Passed | Root ESLint enables no-unused-vars and no-unreachable. Compiler ESLint enables TypeScript unused-variable checks; playground inherits ESLint analysis. These provide dead-code detection across all s... |
| Technical Debt Tracking | 1/1 | 🟢 Passed | Compiler CLAUDE.md documents error.todo and error.bug fixture categories for unsupported features and known bugs. Rust-port plans track remaining work; GitHub also has a Compiler: todo label. |
| N+1 Query Detection | N/A | Skipped | None of the seven applications uses a database or ORM requiring N+1 query detection. |

## Build System

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Unused Dependencies Detection | 0/7 | 🔴 Failed | No depcheck, knip, cargo-udeps, or equivalent unused-dependency check found. Unused-variable linting does not inspect package dependencies. |
| Heavy Dependency Detection | 2/7 | 🔴 Failed | Runtime sizebot compares built/gzipped bundle sizes and comments on PRs. Browser-extension builds emit webpack-stats artifacts. No bundle-size analysis found for standalone DevTools, playground, or... |
| Build Command Documentation | 1/1 | 🟢 Passed | fixtures/dom/README.md documents yarn build from the repository root. DevTools READMEs document yarn build-for-devtools; compiler/docs/DEVELOPMENT_GUIDE.md documents building its runner. |
| Dependencies Pinned | 1/1 | 🟢 Passed | Tracked root, compiler, and playground yarn.lock files pin resolved dependencies; compiler/Cargo.lock pins Rust dependencies. CI installs use --frozen-lockfile. |
| VCS CLI Tools | 1/1 | 🟢 Passed | gh is installed and gh auth status succeeded. Read-only repository, PR, issue, release, and workflow queries succeeded. |
| Automated PR Review Generation | 1/1 | 🟢 Passed | The sizebot workflow generates bundle-size analysis comments, not just status checks. github-actions comments with comparisons were observed on PRs 38071 and 38070. |
| Agentic Development | 1/1 | 🟢 Passed | Checked-in .claude/settings.json has a SessionStart instruction hook, approved agent commands, and populated workflow skills. Compiler CLAUDE.md directs agent verification and plan updates. |
| Fast CI Feedback | 1/1 | 🟢 Passed | For 20 merged PRs, selected the primary runtime or compiler workflow and fetched all its jobs to avoid the 100-check rollup limit. Earliest job start to latest completion averaged 4.11 minutes; all... |
| Build Performance Tracking | 1/1 | 🟢 Passed | CI records per-bundle shard timings, compares mean and p95 timing changes, caches build weights, and balances 50 build workers. A completed workflow confirmed timed build steps and cache restoration. |
| Deployment Frequency | 1/1 | 🟢 Passed | Queried releases and both runtime/compiler publishing workflows. The latest 30 runs include 28 successful runtime and 30 successful compiler releases; successful scheduled publishes occurred each w... |
| Single Command Setup | 1/1 | 🟢 Passed | Compiler development guide provides yarn, yarn snap:build, then yarn snap --watch. Playground README provides yarn followed by yarn dev; scripts build/watch local compiler dependencies. |
| Feature Flag Infrastructure | 1/1 | 🟢 Passed | packages/shared/ReactFeatureFlags.js and per-target forks implement feature flags. DevTools also has target-specific flags, and CI runs yarn flags. |
| Release Notes Automation | 1/1 | 🟢 Passed | Root generate-changelog script collects package commits and PR metadata and renders changelog entries. scripts/devtools/prepare-release.js also supports release preparation. |
| Monorepo Tooling | 1/1 | 🟢 Passed | Root and compiler package.json files define Yarn workspaces; compiler/Cargo.toml defines a Rust workspace. CI discovers and tests compiler workspaces. |
| Version Drift Detection | 1/1 | 🟢 Passed | CI runs check-release-dependencies.js, comparing sibling package dependency/peer ranges against actual release versions. Rust version workflow checks that publishable crate versions match. |
| Release Automation | 1/1 | 🟢 Passed | runtime_release_from_ci.yml automates package publishing; compiler prerelease workflows publish on weekday schedules. Rust crates also have a publishing workflow. |
| Dead Feature Flag Detection | 1/1 | 🟢 Passed | scripts/flags/flags.js implements --cleanup, classifying flags enabled or disabled across all variants and identifying shipped experiments awaiting rollout/cleanup. |
| Progressive Rollout | N/A | Skipped | Not an infrastructure repository. Canary/experimental package channels exist, but percentage- or ring-based infrastructure rollout is not applicable. |
| Rollback Automation | N/A | Skipped | Not an infrastructure repository. No deployed-service rollback requirement is applied to library, developer-tool, or playground publishing. |

## Testing

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Unit Tests Runnable | 0/7 | 🔴 Failed | Ran cd /Users/aristotle_co/Documents/readiness/react && yarn test --listTests --maxWorkers=2 with a 40-second Execute timeout. Exit 1: Cannot find module 'chalk'. Node is available; no tests ran, n... |
| Test Coverage Thresholds | 0/7 | 🔴 Failed | Coverage input configuration exists, but no minimum coverage threshold, blocking coverage service, or equivalent gate is configured for any application. |
| Unit Tests Exist | 3/7 | 🔴 Failed | Runtime has extensive __tests__ suites. Both DevTools applications use tested react-devtools-shared code; the extension also has ignoreList-test.js. Playground has e2e-only tests; the three compile... |
| Integration Tests Exist | 4/7 | 🔴 Failed | Runtime has Flight/browser integration tests. Shared DevTools UI has Playwright end-to-end coverage used by both DevTools targets. Playground has __tests__/e2e/page.spec.ts. No integration suites f... |
| Test Performance Tracking | 4/7 | 🔴 Failed | Runtime CI retains Flight Playwright reports and DevTools traces/results; playground CI retains test artifacts and uses timing-aware reporters. These cover runtime, both shared-code DevTools target... |
| Flaky Test Detection | 4/7 | 🔴 Failed | Flight Playwright config retries CI tests twice, DevTools Playwright config retries three times, and playground retries five times with traces. These cover runtime, both DevTools targets, and playg... |
| Test Isolation | 4/7 | 🔴 Failed | Runtime/DevTools CI shards Jest tests. Flight and playground Playwright suites configure parallel execution and isolated browser contexts. No isolation configuration found for the three compiler to... |
| Interactive QA Exists | 4/7 | 🔴 Failed | Root compiler guide documents install/build/compile-output steps; DevTools guides cover dependency builds, desktop or extension launch, and inspection via the test shell. Playground README plus Pla... |
| Interactive QA Runnable | 4/7 | 🔴 Failed | Documentation fallback only, not an executed QA pass: dependencies/build outputs are absent, and this read-only audit did not install or build applications. Complete dependency, launch, no-auth, an... |
| Test File Naming Conventions | 5/7 | 🔴 Failed | Runtime and shared DevTools Jest configs define explicit testRegex patterns. Playground scopes Playwright to its e2e directory; React Analyzer config names dist/test/**/*.test.js. Healthcheck and M... |

## Documentation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| AGENTS.md File | 0/1 | 🔴 Failed | No AGENTS.md exists at the repository root. CLAUDE.md and .claude instructions are useful but do not satisfy this exact-file criterion. |
| AGENTS.md Freshness Validation | 0/1 | 🔴 Failed | No root AGENTS.md exists, so its prerequisite fails. No automation validating an AGENTS.md was found. |
| README File | 1/1 | 🟢 Passed | Root README.md explains React, installation routes, usage with JSX, documentation, and contribution guidance. |
| Automated Documentation Generation | 1/1 | 🟢 Passed | compiler package.json configures eslint-docs using scripts/build-eslint-docs.js. The root generate-changelog command also generates documentation from commits and PR metadata. |
| Skills Configuration | 1/1 | 🟢 Passed | .claude/skills/verify/SKILL.md and other skills have YAML name/description frontmatter and substantive workflow instructions. Compiler-specific skills also exist. |
| Documentation Freshness | 1/1 | 🟢 Passed | The prescribed 180-day history query lists README.md and CONTRIBUTING.md at HEAD dated 2026-10-30. This is a shallow checkout, so the evidence reflects only available snapshot history. |
| Service Architecture Documented | 1/1 | 🟢 Passed | packages/react-devtools/OVERVIEW.md describes frontend/backend responsibilities, bridge communication, operations messages, and inspection requests. Compiler documentation also covers architecture ... |
| API Schema Docs | N/A | Skipped | Recursive schema search found no OpenAPI/Swagger/GraphQL files. Targets are libraries, developer tools, a stdio MCP server, and a frontend playground, not HTTP API services requiring those schemas. |

## Development Environment

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Dev Container | 0/1 | 🔴 Failed | No .devcontainer/devcontainer.json or equivalent checked-in devcontainer configuration found. |
| Environment Template | 1/1 | 🟢 Passed | packages/react-devtools/README.md documents HOST, PORT, TLS paths, and client connection environment variables with defaults and examples. |
| Local Services Setup | N/A | Skipped | No database, cache, or comparable external local-service dependency was identified. DevTools local backend/frontend launch steps are documented; MCP uses remote public documentation search. |
| Database Schema | N/A | Skipped | No application database or ORM schema requirement identified. |
| Devcontainer Runnable | N/A | Skipped | The devcontainer CLI is not installed. No devcontainer was launched; absence of configuration is scored separately. |

## Debugging & Observability

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Distributed Tracing | 0/7 | 🔴 Failed | No cross-service trace/request-ID propagation found. React profiling, bridge element IDs, and local logging session IDs do not establish distributed request tracing. |
| Error Tracking Contextualized | 0/7 | 🔴 Failed | No Sentry/Bugsnag/Rollbar or equivalent configured error-tracking service with source maps, breadcrumbs, and user context found. Local component-stack logging alone does not satisfy this criterion. |
| Runbooks Documented | 0/1 | 🔴 Failed | Release and development guides exist, but no incident-response runbook, playbook directory, or external runbook pointer was found. |
| Health Checks | 0/7 | 🔴 Failed | The deployed playground has no health/readiness endpoint or probe. Other targets are libraries, desktop/browser extensions, or stdio/CLI tools where service probes are not applicable; denominator r... |
| Circuit Breakers | 0/7 | 🔴 Failed | MCP calls remote Algolia/documentation services but has no explicitly configured circuit breaker or exponential-backoff policy. Other applications do not require external-service resilience; denomi... |
| Alerting Configured | 1/7 | 🔴 Failed | Runtime release workflow has an always-evaluated Discord notification job for publishing failure/cancellation. No comparable failure-alert configuration found for the other six applications. |
| Deployment Observability | 1/7 | 🔴 Failed | Runtime release workflow sends release-start/failure Discord notifications linking the workflow attempt. No deploy-impact dashboard pointers or deployment notification configuration found for the o... |
| Structured Logging | 3/7 | 🔴 Failed | Runtime has ReactFiberErrorLogger.js; both DevTools targets share dedicated Logger.js and storeErrorLogger.js modules. No dedicated logging module or logging-library dependency found for playground... |
| Code Quality Metrics Dashboard | 3/7 | 🔴 Failed | scripts/jest/config.base.js configures coverage inputs for runtime and shared DevTools JavaScript, meeting the criterion's coverage-configuration evidence path. No equivalent metrics configuration ... |
| Metrics Collection | 4/7 | 🔴 Failed | Runtime Profiler timers and DevTools profiling stores collect render/commit performance metrics. MCP runtimePerf.ts captures React Profiler and web-vitals measurements. No comparable instrumentatio... |
| Profiling Instrumentation | 4/7 | 🔴 Failed | Runtime ReactProfilerTimer and profiling builds, both DevTools Profiler surfaces/flame graphs, and MCP Puppeteer/React Profiler measurements provide profiling. No comparable configured profiler fou... |

## Security

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| CODEOWNERS File | 0/1 | 🔴 Failed | No root or .github/CODEOWNERS file found. MAINTAINERS is not a CODEOWNERS assignment file. |
| Dependency Update Automation | 0/1 | 🔴 Failed | .github/dependabot.yml covers fixtures only, sets open-pull-requests-limit: 0, and ignores all dependencies. No active replacement updater was found. |
| Gitignore Comprehensive | 0/1 | 🔴 Failed | Root .gitignore excludes dependencies, builds, and IDE files, but does not exclude .env files. Its .DS_STORE entry does not match normal .DS_Store casing; playground-local env ignores do not cover ... |
| DAST Scanning | 0/7 | 🔴 Failed | No ZAP, Burp, Nuclei, StackHawk, or equivalent dynamic security scan is configured against the deployed playground. The remaining library/developer-tool targets are not web-service DAST targets. |
| Sensitive Data Log Scrubbing | 0/7 | 🔴 Failed | No logging redaction, PII masking, or scrubbing policy found for any application. DevTools sanitize helpers normalize serialized values rather than redact sensitive log content. |
| Minimum Dependency Release Age | 0/1 | 🔴 Failed | No minimumReleaseAge, stabilityDays, explicit waiting-period policy, or CI dependency-release-date gate found. |
| Secrets Management | 1/1 | 🟢 Passed | GitHub Actions use secrets.GITHUB_TOKEN, secrets.NPM_TOKEN, and Discord webhook secrets. Publishing also uses trusted-publishing permissions rather than embedding deployment credentials. |
| Branch Protection | N/A | Skipped | Authenticated GitHub repository query returned permissions.admin=false. Per criterion, branch protection/ruleset inspection is skipped without admin access. |
| Secret Scanning | N/A | Skipped | No checked-in secret-scanning hook or workflow found. GitHub admin permission is absent, so native secret-scanning status cannot be verified and is skipped. |
| Automated Security Review Generation | N/A | Skipped | No checked-in security-assessment/report generator or security bot evidence found. Native code-scanning inspection is skipped because GitHub admin access is absent. |
| PII Handling | N/A | Skipped | These are libraries and developer utilities, not identified end-user personal-data processing services. No PII-processing requirement was established; source anonymization is not treated as proof o... |
| Privacy Compliance | N/A | Skipped | Public library/developer-tool targets have no identified enabled end-user data collection. DevTools public/default feature configurations disable event logging; privacy-compliance infrastructure is... |

## Task Discovery

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Issue Labeling System | 0/1 | 🔴 Failed | Live labels include Type and Component categories, but no priority/severity hierarchy was found among the repository labels. The required priority/type/area combination is incomplete. |
| Backlog Health | 0/1 | 🔴 Failed | Of the latest 50 open issues, only 13 (26%) have both a title over 10 characters and at least one label, below the required >70%. None in that sample were inactive for over 365 days. |
| Issue Templates | 1/1 | 🟢 Passed | .github/ISSUE_TEMPLATE contains structured runtime, compiler, and DevTools bug-report templates. |
| PR Templates | 1/1 | 🟢 Passed | .github/PULL_REQUEST_TEMPLATE.md requires a Summary and How did you test this change section, with motivation, context, and contribution-check instructions. |

## Product & Experimentation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Product Analytics Instrumentation | 0/7 | 🔴 Failed | No enabled product-analytics integration found for public application targets. DevTools has optional custom event-logger infrastructure, but public/default feature flags set enableLogger=false. |
| Error to Insight Pipeline | 0/7 | 🔴 Failed | No configured error-tracking-to-GitHub issue integration, Sentry issue linking, or automated error-to-issue workflow found. |

---

*Generated by Factory Agent Readiness*
```

</details>

<details>
<summary>react: CLI output</summary>

```markdown
# Level
**Level 3, 52.38%**

84 criteria: 72 scored, 12 skipped. Report saved successfully.

Repository: https://github.com/facebook/react

Languages: JavaScript/Flow, TypeScript, and Rust. Evaluated local `main` at `16453bcd12becf76340caa793d185cec1b80ebef`. No source or configuration changes made during the audit.

# Applications
1. `.` - React runtime, renderers, and shared compiler libraries.
2. `packages/react-devtools` - Standalone Electron debugger.
3. `packages/react-devtools-extensions` - Browser debugging extensions.
4. `compiler/apps/playground` - Deployed compiler playground.
5. `compiler/packages/react-compiler-healthcheck` - Compiler readiness CLI.
6. `compiler/packages/react-mcp-server` - Experimental MCP server.
7. `compiler/packages/react-forgive` - React Analyzer VS Code extension.

# Criteria
Repository scores use denominator 1; application scores use 7. `null` means skipped.

**Style & Validation**
- Linter configuration: 7/7 - ESLint configurations cover all applications.
- Type checking: 7/7 - Flow and TypeScript configurations present.
- Formatter: 7/7 - Prettier covers application sources.
- Pre-commit hooks: 3/7 - Opt-in JavaScript hook lacks TypeScript coverage.
- Strict typing: 7/7 - Strict TypeScript settings and strict-local Flow modules.
- Naming consistency: 0/7 - Naming rules disabled or absent.
- Cyclomatic complexity: 0/7 - No active complexity thresholds.
- Large-file detection: 0/1 - No individual-file size enforcement.
- Dead-code detection: 7/7 - Unused-variable and unreachable-code checks.
- Duplicate-code detection: 0/7 - No configured detector.
- Code modularization: 1/7 - Runtime build enforces renderer boundaries.
- Technical-debt tracking: 1/1 - Compiler fixtures categorize known limitations and bugs.
- N+1 detection: null/7 - No database/ORM applications.
- Unused-dependency detection: 0/7 - No dependency-usage analyzer.

**Build System**
- Build commands documented: 1/1 - Runtime, compiler, and DevTools commands documented.
- Dependencies pinned: 1/1 - Committed Yarn and Cargo lockfiles.
- VCS CLI access: 1/1 - GitHub CLI authenticated.
- Automated PR review: 1/1 - Sizebot posts bundle-size analysis comments.
- Agentic development: 1/1 - Agent hooks, skills, and workflows configured.
- Fast CI feedback: 1/1 - Twenty primary workflows averaged 4.11 minutes.
- Build-performance tracking: 1/1 - Recorded timings drive balanced build shards.
- Deployment frequency: 1/1 - Successful weekday prerelease publishing verified.
- Single-command setup: 1/1 - Short development setup sequences documented.
- Feature flags: 1/1 - Runtime and DevTools flag infrastructure.
- Release-notes automation: 1/1 - Changelog-generation scripts configured.
- Progressive rollout: null/1 - Not an infrastructure repository.
- Rollback automation: null/1 - Infrastructure rollback criterion not applicable.
- Monorepo tooling: 1/1 - Yarn and Cargo workspaces.
- Version-drift detection: 1/1 - Release dependency and crate-version validation.
- Release automation: 1/1 - Automated package-publishing workflows.
- Dead-feature-flag detection: 1/1 - Cleanup command identifies flag lifecycle states.
- Heavy-dependency detection: 2/7 - Runtime sizebot and extension webpack reports.

**Testing**
- Unit tests exist: 3/7 - Runtime and shared DevTools coverage.
- Integration tests exist: 4/7 - Runtime, DevTools, and playground coverage.
- Unit tests runnable: 0/7 - Bounded discovery failed because `chalk` is missing.
- Test-performance tracking: 4/7 - CI retains browser reports and artifacts.
- Flaky-test detection: 4/7 - Browser-test retries and traces configured.
- Coverage thresholds: 0/7 - No enforced minimum coverage.
- Test-naming conventions: 5/7 - Configured test patterns or directories.
- Test isolation: 4/7 - Sharding and isolated browser contexts.
- Interactive QA documented: 4/7 - Three smaller compiler tools lack complete paths.
- Interactive QA runnable: 4/7 - Documentation fallback only; applications were not launched.

No tests executed. Discovery used `yarn test --listTests --maxWorkers=2`, with a 40-second command timeout. It exited 1 because `chalk` was unavailable.

**Documentation**
- Root AGENTS.md: 0/1 - Missing; CLAUDE.md does not satisfy this criterion.
- Root README: 1/1 - Installation and usage guidance present.
- Automated documentation: 1/1 - ESLint documentation and changelog generators.
- Skills: 1/1 - Valid, populated SKILL.md files.
- Documentation freshness: 1/1 - Recent documentation appears in available shallow history.
- Architecture documentation: 1/1 - DevTools communication and compiler architecture documented.
- AGENTS.md validation: 0/1 - File and validation automation absent.
- API schemas: null/7 - No applicable HTTP API service identified.
- Runbooks: 0/1 - No incident-response runbook pointers.
- Issue templates: 1/1 - Structured bug-report templates.
- Issue-labeling system: 0/1 - Type/area labels exist, but priority hierarchy is missing.
- Backlog health: 0/1 - Only 13/50 sampled issues met title-and-label requirements.
- PR templates: 1/1 - Summary, context, and testing sections.

**Dev Environment**
- Devcontainer: 0/1 - No configuration found.
- Environment template/documentation: 1/1 - DevTools environment variables documented.
- Local services setup: null/1 - No external local-service dependencies identified.
- Database schema: null/7 - No application databases identified.
- Devcontainer runnable: null/1 - CLI unavailable.

**Debugging & Observability**
- Structured logging: 3/7 - Runtime and shared DevTools logger modules.
- Distributed tracing: 0/7 - No cross-service request-ID propagation.
- Metrics collection: 4/7 - Runtime, DevTools, and MCP performance measurements.
- Code-quality metrics: 3/7 - Runtime/shared DevTools coverage configuration.
- Contextualized error tracking: 0/7 - No qualifying error-tracking service configuration.
- Alerting: 1/7 - Runtime release failures notify Discord.
- Deployment observability: 1/7 - Runtime release notifications link workflow attempts.
- Health checks: 0/7 - Deployed playground lacks a health probe.
- Circuit breakers: 0/7 - MCP external calls lack explicit resilience configuration.
- Profiling: 4/7 - Runtime, DevTools, and MCP profiling.
- Log scrubbing: 0/7 - No sensitive-log redaction mechanism.
- Product analytics: 0/7 - Public DevTools event logging is disabled.
- Error-to-insight pipeline: 0/7 - No automated error-to-issue integration.

**Security**
- Branch protection: null/1 - Admin access unavailable; not verified.
- Secret scanning: null/1 - No local scanner; native settings require admin access.
- CODEOWNERS: 0/1 - Missing.
- Automated security review: null/1 - No local evidence; native checks inaccessible.
- Dependency updates: 0/1 - Dependabot disables update PRs and ignores all dependencies.
- Comprehensive gitignore: 0/1 - Repository-wide environment-file exclusions missing.
- Privacy compliance: null/1 - No enabled end-user collection identified.
- Secrets management: 1/1 - Actions secrets and trusted publishing configured.
- Minimum dependency release age: 0/1 - No waiting-period policy.
- DAST: 0/7 - No dynamic security scanning for playground.
- PII handling: null/7 - No applicable personal-data service identified.

# Action Items
- Add root `AGENTS.md` with setup, bounded tests, and per-application QA steps; validate its commands in CI.
- Add real tests and complete smoke-test paths for healthcheck, MCP, and React Analyzer; enforce coverage thresholds.
- Enable dependency-update PRs, add secret/security scanning, and fix repository-wide `.env` exclusions.

---
View the full report: https://app.factory.ai/analytics/readiness/https%3A%2F%2Fgithub.com%2Ffacebook%2Freact
```

</details>

<details>
<summary>scrapy: detailed report</summary>

```markdown
# Agent Readiness Report: scrapy

**Level:** 4/5  
**Overall Score:** 61%  
**Generated:** 2026-10-31 00:49:31 UTC  
**Commit:** `51c10b1`  
**Branch:** master  

## Summary

| Metric | Value |
|--------|-------|
| Total Criteria | 84 |
| Passed | 40 |
| Failed | 26 |
| Skipped | 18 |

## Pass Rate by Category

| Category | Pass Rate |
|----------|-----------|
| Style & Validation | 58% |
| Build System | 62% |
| Testing | 80% |
| Documentation | 71% |
| Development Environment | 0% |
| Debugging & Observability | 60% |
| Security | 67% |
| Task Discovery | 50% |
| Product & Experimentation | 0% |

## Style & Validation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Cyclomatic Complexity | 0/1 | 🔴 Failed | No explicit cyclomatic/cognitive complexity threshold, Radon, Xenon, or equivalent monitoring is configured. Ruff does not enable C901. |
| Large File Detection | 0/1 | 🔴 Failed | No file-size hook, CI size gate, or LFS rule. Pylint explicitly disables too-many-lines. |
| Duplicate Code Detection | 0/1 | 🔴 Failed | Pylint explicitly disables duplicate-code, and no alternate copy-paste/duplication detector is configured. |
| Code Modularization Enforcement | 0/1 | 🔴 Failed | No import-linter contracts or architecture/layer boundary tests are configured. Ruff's reactor-specific import restrictions do not define application module boundaries. |
| Technical Debt Tracking | 0/1 | 🔴 Failed | Pylint fixme is disabled. No TODO/FIXME scanner, required issue linkage, or explicit technical-debt tracking process was found. |
| Linter Configuration | 1/1 | 🟢 Passed | pyproject.toml configures Ruff and Pylint; pre-commit and CI run these analyzers. |
| Type Checker | 1/1 | 🟢 Passed | pyproject.toml configures mypy, and tox/CI run mypy against scrapy and tests plus separate typing tests. |
| Code Formatter | 1/1 | 🟢 Passed | Pre-commit configures ruff-format and blacken-docs; the contributing guide documents Ruff formatting. |
| Pre-commit Hooks | 1/1 | 🟢 Passed | .pre-commit-config.yaml defines quality hooks, and docs/contributing.rst explicitly documents pre-commit install. |
| Strict Typing | 1/1 | 🟢 Passed | [tool.mypy] sets strict = true. Tests and selected third-party/interface modules have explicit, scoped relaxations. |
| Naming Consistency | 1/1 | 🟢 Passed | AGENTS.md explicitly requires underscore prefixes for private APIs and specifies other naming/documentation conventions. |
| Dead Code Detection | 1/1 | 🟢 Passed | Ruff enables Pyflakes F rules, including unused imports and unused local variables, through pre-commit and CI. |
| N+1 Query Detection | N/A | Skipped | No application-owned ORM/database query layer; Scrapy is a crawling framework. |

## Build System

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Automated PR Review Generation | 0/1 | 🔴 Failed | Ten recent PRs show human reviews and Codecov/CodSpeed reports, but no automated code-review comments or configured code-review generator. |
| Fast CI Feedback | 0/1 | 🔴 Failed | For 19 of the latest 20 merged PRs with completed primary CI checks, earliest-start to latest-completion averaged 29.48 minutes, including reruns, above the 10-minute limit. |
| Deployment Frequency | 0/1 | 🔴 Failed | Checked 30 releases and 30 Publish workflow runs. Actual releases/publishes occur weeks apart, not multiple times per week; latest release was 2026-09-10. |
| Feature Flag Infrastructure | 0/1 | 🔴 Failed | No feature-flag platform or rollout-targeting system is configured. Ordinary Scrapy component settings are not release feature flags. |
| Unused Dependencies Detection | 0/1 | 🔴 Failed | No deptry, pip-extra-reqs, or other unused-dependency analysis hook or CI task was found. |
| Build Command Documentation | 1/1 | 🟢 Passed | README.rst documents pip install scrapy and links the contributing guide, whose local copy documents pip install -e .; tox.ini defines package build checks. |
| Dependencies Pinned | 1/1 | 🟢 Passed | docs/requirements.txt is a committed uv-compiled requirements file with exact pins, including runtime dependencies. Static-check and minimum-version tox environments also pin dependencies. |
| VCS CLI Tools | 1/1 | 🟢 Passed | gh auth status exited 0 and confirmed authenticated GitHub access. Repository permissions allow reading but not administration. |
| Agentic Development | 1/1 | 🟢 Passed | Recent PRs #8433 and #8431 contain maintainers' explicitly identified AI review feedback followed by contributor fixes, providing direct evidence of AI-assisted development. |
| Build Performance Tracking | 1/1 | 🟢 Passed | CI configures uv caching with dependency-file keys, parallel jobs, and static-check gates to avoid unnecessary test matrices. GitHub run 41115731186 exposes per-step build/check timing. |
| Single Command Setup | 1/1 | 🟢 Passed | README links the contributing guide; docs/contributing.rst documents pip install -e . and pip install tox. Installation and CLI documentation provide a short setup-to-use path. |
| Release Notes Automation | 1/1 | 🟢 Passed | publish.yml builds Sphinx documentation, extracts release notes with extras/github-release-notes.py, and creates the GitHub release automatically. |
| Release Automation | 1/1 | 🟢 Passed | Version-tag pushes trigger package builds, PyPI trusted publishing, GitHub releases, and related documentation updates in publish.yml. |
| Progressive Rollout | N/A | Skipped | Not an infrastructure repository or hosted service; Scrapy is a Python framework and CLI distributed through PyPI. |
| Rollback Automation | N/A | Skipped | Not an infrastructure repository; service deployment rollback is outside this library/package's lifecycle. |
| Monorepo Tooling | N/A | Skipped | Single application and one root Python build package; no monorepo orchestration is needed. |
| Heavy Dependency Detection | N/A | Skipped | Non-bundled Python framework/CLI; frontend bundle-size analysis is not applicable. |
| Version Drift Detection | N/A | Skipped | One build package/module. Documentation and test environments do not constitute independently built sibling modules. |
| Dead Feature Flag Detection | N/A | Skipped | Skipped because feature_flag_infrastructure does not pass; there is no release feature-flag system to inspect. |

## Testing

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Unit Tests Runnable | 0/1 | 🔴 Failed | Ran python -m pytest --collect-only tests/test_request_dict.py with a 60-second Execute timeout and cache/bytecode writes disabled. Exit 4: conftest.py cannot import twisted. No tests were collecte... |
| Flaky Test Detection | 0/1 | 🔴 Failed | pytest-rerunfailures is listed as a dependency, but no rerun flags, flaky markers, quarantine policy, or flaky-test analytics configuration was found. Recent duplicate checks were from the PR guard... |
| Unit Tests Exist | 1/1 | 🟢 Passed | A bounded root test-file scan found 172 tests/test_*.py modules; tests/test_request_dict.py contains concrete request serialization unit tests. |
| Integration Tests Exist | 1/1 | 🟢 Passed | tests/test_crawl.py runs actual crawlers against MockServer fixtures; subprocess, downloader, proxy, and feed-export integration tests also exist. |
| Test Performance Tracking | 1/1 | 🟢 Passed | tox pytest commands include --durations=10 and JUnit XML. CI uploads test results to Codecov; separate CodSpeed workflows track performance benchmarks. |
| Test Coverage Thresholds | 1/1 | 🟢 Passed | codecov.yml sets the project coverage target to 100%. CI uploads coverage and recent PRs expose the codecov/project status check and coverage reports. |
| Test File Naming Conventions | 1/1 | 🟢 Passed | pytest explicitly sets python_files to test_*.py and test_*/__init__.py; contribution documentation describes matching test-module names. |
| Test Isolation | 1/1 | 🟢 Passed | pytest-xdist is a test dependency, and CI sets PYTEST_ADDOPTS to -n logical. Fixtures also provide isolated mock-server and monkeypatch state. |
| Interactive QA Exists | 1/1 | 🟢 Passed | Installation and contributor docs cover dependency setup; CLI docs give settings --get BOT_NAME with expected output, and the tutorial covers a full crawl. These paths need no login. |
| Interactive QA Runnable | 1/1 | 🟢 Passed | Documentation fallback: python -m scrapy settings --get BOT_NAME was attempted but exited 1 because w3lib is absent. Runtime success is not claimed; complete install and CLI interaction instruction... |

## Documentation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Skills Configuration | 0/1 | 🔴 Failed | No repository-local SKILL.md or valid skill directory was found. Documentation links an external agent plugin, but no skill is installed in this repository. |
| AGENTS.md Freshness Validation | 0/1 | 🔴 Failed | No automation validates AGENTS.md commands or references. Sybil documentation tests only collect *.rst, and the Sphinx link checker covers documentation rather than AGENTS.md. |
| AGENTS.md File | 1/1 | 🟢 Passed | Root AGENTS.md is 4,909 bytes and documents test/lint commands, dependency compatibility checks, coding rules, documentation conventions, and the PR workflow. |
| README File | 1/1 | 🟢 Passed | Root README.rst provides the project purpose, supported Python version, installation command, and links to usage and contribution documentation. |
| Automated Documentation Generation | 1/1 | 🟢 Passed | Sphinx, autodoc-related extensions, tox documentation environments, Read the Docs configuration, and publishing workflows generate documentation. |
| Documentation Freshness | 1/1 | 🟢 Passed | The required local git-history query reports AGENTS.md and CONTRIBUTING.md in commit 51c10b1 dated 2026-10-30, within 180 days. Available local history contains one commit. |
| Service Architecture Documented | 1/1 | 🟢 Passed | docs/topics/architecture.rst documents components and request/item flow and embeds scrapy_architecture_02.png. |
| API Schema Docs | N/A | Skipped | Library/CLI with no application-owned HTTP API; no OpenAPI or GraphQL schema is required. |

## Development Environment

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Dev Container | 0/1 | 🔴 Failed | No .devcontainer/devcontainer.json or equivalent development-container configuration exists. |
| Environment Template | 0/1 | 🔴 Failed | No .env.example template exists, and README.rst/AGENTS.md do not document environment variables. Variable documentation exists only deeper in the narrative docs. |
| Local Services Setup | N/A | Skipped | Core framework development requires no provisioned database or service stack; integration tests supply their own mock servers. Optional storage backends are not mandatory local dependencies. |
| Database Schema | N/A | Skipped | No application-owned database schema. Optional downstream storage/pipeline integrations do not define a database for this package. |
| Devcontainer Runnable | N/A | Skipped | The devcontainer CLI is not installed; no devcontainer configuration exists either. |

## Debugging & Observability

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Error Tracking Contextualized | 0/1 | 🔴 Failed | No configured Sentry, Bugsnag, Rollbar, or equivalent external error tracking with breadcrumbs and contextualized reports was found. |
| Alerting Configured | 0/1 | 🔴 Failed | Memory-warning signals and optional email hooks exist, but default warning/limit thresholds are zero and notification recipients are empty. No configured alert destinations or operational alert rul... |
| Runbooks Documented | 0/1 | 🔴 Failed | Troubleshooting, performance, and deployment guides exist, but no dedicated incident-response runbook/playbook or explicit runbook reference was found. |
| Deployment Observability | 0/1 | 🔴 Failed | Deployment docs describe optional hosting providers, but no repository-specific deployment-impact dashboard, monitoring URL, or deployment-notification integration is configured. |
| Structured Logging | 1/1 | 🟢 Passed | Dedicated scrapy/utils/log.py, scrapy/logformatter.py, and scrapy/_logging configure logging and structured contextual fields, satisfying the dedicated-logger-module criterion. |
| Distributed Tracing | 1/1 | 🟢 Passed | Requests have unique id and parent_id attributes. Request copies and scraper callback outputs propagate parent IDs, allowing request lineage to be followed through the crawl. |
| Metrics Collection | 1/1 | 🟢 Passed | StatsCollector, CoreStats, downloader statistics, memory usage, event-loop lag, and periodic logging provide built-in performance instrumentation. |
| Code Quality Metrics Dashboard | 1/1 | 🟢 Passed | Coverage is configured and uploaded to Codecov, whose readable reports appear in recent merged PR comments; project coverage has a 100% target. |
| Circuit Breakers | 1/1 | 🟢 Passed | RetryMiddleware implements a bounded resilience policy for outbound requests: automatic retries for transient exceptions and HTTP 408/429/5xx responses, with retry counters and a two-retry default.... |
| Profiling Instrumentation | 1/1 | 🟢 Passed | MemoryDebugger and trackref provide development memory profiling; resource-usage documentation explains their use and points to py-spy. CodSpeed adds configured CPU/walltime benchmarks. |
| Health Checks | N/A | Skipped | A Python framework/CLI, not a deployed service requiring liveness/readiness endpoints. |

## Security

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| CODEOWNERS File | 0/1 | 🔴 Failed | No CODEOWNERS file exists at the root or under .github. |
| Gitignore Comprehensive | 0/1 | 🔴 Failed | .gitignore covers Python caches, virtualenvs, build artifacts, IDE directories, and OS files, but does not ignore .env or .env.* secret files. |
| Dependency Update Automation | 1/1 | 🟢 Passed | Dependabot is configured, and recent Dependabot PRs #8384, #8258, and #8103 confirm activity. A separate workflow upgrades CI dependency pins. |
| Secrets Management | 1/1 | 🟢 Passed | Workflows use GitHub Actions secrets for Read the Docs and the CI-pins GitHub App, and PyPI publishing uses OIDC trusted publishing instead of hardcoded credentials. |
| Sensitive Data Log Scrubbing | 1/1 | 🟢 Passed | Default UriUserInfoMiddleware removes credentials from request URLs before downstream processing; scrapy.utils.url.strip_url also explicitly strips credentials. This is limited URL credential sanit... |
| Minimum Dependency Release Age | 1/1 | 🟢 Passed | Dependabot has cooldown.default-days: 7. extras/upgrade-ci-pins.py also enforces a seven-day cutoff before adopting GitHub Actions releases. |
| Branch Protection | N/A | Skipped | Authenticated GitHub permissions report admin=false and maintain=false. Skipped rather than inferring protection settings without the required administrative access. |
| Secret Scanning | N/A | Skipped | No committed-secret scanning hook or workflow was found, and GitHub admin access is unavailable. Native secret-scanning status cannot be verified. |
| Automated Security Review Generation | N/A | Skipped | Ruff security rules and zizmor lint are configured, but no explicit generated security-assessment integration was found. Admin-only code-scanning APIs were not queried without admin access. |
| DAST Scanning | N/A | Skipped | Not deployed as a web service; dynamic security scans against a hosted application are not applicable. |
| PII Handling | N/A | Skipped | Generic developer library with no application-specific personal-data collection model; downstream spiders determine what data they process. |
| Privacy Compliance | N/A | Skipped | Scrapy is a library/framework rather than an end-user data-collection service; application-specific consent and privacy policies belong to downstream projects. |

## Task Discovery

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Issue Labeling System | 0/1 | 🔴 Failed | GitHub labels cover types and areas such as bug, enhancement, CI, HTTP/2, and typing, but no consistent priority/severity label taxonomy exists. |
| PR Templates | 0/1 | 🔴 Failed | The PR template contains an issue-resolution placeholder and a contribution/pre-commit checkbox, but lacks description, testing, and relevant-context sections. |
| Issue Templates | 1/1 | 🟢 Passed | .github/ISSUE_TEMPLATE contains structured bug, feature-request, and question templates; bug reports request reproduction steps, versions, and context. |
| Backlog Health | 1/1 | 🟢 Passed | Of 50 sampled open issues, 39 (78%) have titles over 10 characters and at least one label. Only 19 (38%) are over a year old without a comment in the last year. |

## Product & Experimentation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Product Analytics Instrumentation | 0/1 | 🔴 Failed | No Mixpanel, Amplitude, PostHog, Heap, GA4, or equivalent product-usage instrumentation is configured in the framework. |
| Error to Insight Pipeline | 0/1 | 🔴 Failed | No error-tracker-to-issue integration, Sentry project configuration, or automated incident/error issue creation workflow was found. |

---

*Generated by Factory Agent Readiness*
```

</details>

<details>
<summary>scrapy: CLI output</summary>

```markdown
# Level
**Level 4, 60.61%**

40 passed, 26 failed, 18 skipped across 84 criteria. Report saved successfully. No source or configuration changed.

# Applications
1. `.` - Scrapy’s Python web crawling and scraping framework and CLI.

# Criteria
Skipped criteria use `null/1` and do not affect the score.

**Style & Validation**
- Linter configuration: 1/1 - Ruff and Pylint configured.
- Type checking: 1/1 - Mypy runs in CI.
- Formatter: 1/1 - Ruff formatting and blacken-docs configured.
- Pre-commit hooks: 1/1 - Hooks and installation instructions provided.
- Strict typing: 1/1 - Mypy strict mode enabled.
- Naming consistency: 1/1 - AGENTS.md defines naming conventions.
- Cyclomatic complexity: 0/1 - No explicit complexity threshold configured.
- Large-file detection: 0/1 - No size gate; Pylint’s line-count check disabled.
- Dead-code detection: 1/1 - Ruff detects unused imports and variables.
- Duplicate-code detection: 0/1 - Pylint duplication detection explicitly disabled.
- Code modularization: 0/1 - No architectural boundary enforcement.
- Technical-debt tracking: 0/1 - No marker scanner or explicit tracking process; `fixme` disabled.

**Build System**
- Build command documented: 1/1 - Installation and editable setup documented.
- Dependencies pinned: 1/1 - Compiled documentation requirements and selected tox environments use exact pins.
- VCS CLI tools: 1/1 - GitHub CLI authenticated.
- Automated PR review: 0/1 - No automated code-review generator verified.
- Agentic development: 1/1 - Recent PRs show explicit AI feedback followed by fixes.
- Fast CI feedback: 0/1 - Completed primary CI checks averaged 29.48 minutes across 19 PRs.
- Build-performance tracking: 1/1 - Dependency caching, parallelism, staged checks, and step timings available.
- Deployment frequency: 0/1 - Releases occur weeks apart, not multiple times weekly.
- Feature-flag infrastructure: 0/1 - No release feature-flag system.
- Release-notes automation: 1/1 - Publishing generates GitHub release notes.
- Progressive rollout: null/1 - Not an infrastructure repository.
- Rollback automation: null/1 - Package repository, not deployed infrastructure.
- Monorepo tooling: null/1 - One application.
- Heavy-dependency detection: null/1 - Non-bundled Python package.
- Unused-dependency detection: 0/1 - No deptry or equivalent.
- Version-drift detection: null/1 - One build package.
- Release automation: 1/1 - Tags trigger automated PyPI publishing and GitHub releases.
- Dead-feature-flag detection: null/1 - No feature-flag infrastructure.
- Minimum release age: 1/1 - Explicit seven-day dependency-update cooldown.

**Testing**
- N+1 detection: null/1 - No application-owned database query layer.
- Unit tests exist: 1/1 - Extensive `tests/test_*.py` coverage.
- Integration tests exist: 1/1 - Crawlers exercise mock servers and subprocesses.
- Unit tests runnable: 0/1 - Bounded collection exited 4 because Twisted is missing; no tests executed.
- Test-performance tracking: 1/1 - Duration output, uploaded test results, and CodSpeed benchmarks.
- Flaky-test detection: 0/1 - Retry dependency exists, but no configured retry/quarantine management found.
- Coverage thresholds: 1/1 - Codecov project target is 100%.
- Test naming: 1/1 - Explicit pytest filename patterns.
- Test isolation: 1/1 - CI uses pytest-xdist parallel execution.
- Interactive QA documented: 1/1 - Dependency installation and meaningful CLI/crawl interactions documented.
- Interactive QA runnable: 1/1 - Documentation fallback applied. CLI attempt failed because w3lib is missing; execution success is not claimed.

**Documentation**
- AGENTS.md: 1/1 - Substantial agent-specific workflow instructions.
- README: 1/1 - README.rst provides installation and usage links.
- Automated documentation: 1/1 - Sphinx generation and publishing configured.
- Skills: 0/1 - No repository-local skill; external plugin link only.
- Documentation freshness: 1/1 - Available local history places key documentation within 180 days.
- API schema documentation: null/1 - Library/CLI without an application-owned HTTP API.
- Architecture documentation: 1/1 - Component diagram and data-flow guide.
- AGENTS.md validation: 0/1 - No automation checks its accuracy.
- Runbooks: 0/1 - No explicit incident-response runbook or reference.
- Issue templates: 1/1 - Structured bug and feature templates.
- Issue labeling: 0/1 - Type/area labels exist, but no priority taxonomy.
- Backlog health: 1/1 - 78% of sampled issues meet clarity/label requirements; stale proportion remains below 50%.
- PR templates: 0/1 - Missing description, testing, and context sections.

**Dev Environment**
- Single-command setup: 1/1 - Short documented editable-install and tooling sequence.
- Devcontainer: 0/1 - No configuration.
- Environment template: 0/1 - No template or environment-variable documentation in README/AGENTS.md.
- Local services: null/1 - No mandatory provisioned service stack.
- Database schema: null/1 - No application-owned database.
- Devcontainer runnable: null/1 - Devcontainer CLI unavailable.

**Debugging & Observability**
- Structured logging: 1/1 - Dedicated logging modules and contextual fields.
- Distributed tracing: 1/1 - Request IDs and parent IDs propagate crawl lineage.
- Metrics collection: 1/1 - Crawl statistics, memory, downloader, and event-loop instrumentation.
- Code-quality metrics: 1/1 - Codecov configuration and readable PR reports.
- Contextualized error tracking: 0/1 - No configured external error tracker.
- Alerting: 0/1 - Optional hooks exist, but thresholds and recipients are unconfigured.
- Deployment observability: 0/1 - No repository-specific deployment-impact dashboard or notifications.
- Health checks: null/1 - Not a deployed service.
- Circuit breakers: 1/1 - Bounded outbound retry resilience satisfies the criterion; no actual circuit breaker claimed.
- Profiling: 1/1 - MemoryDebugger, trackref, and CPU/walltime benchmarks.
- Product analytics: 0/1 - No product-usage instrumentation.
- Error-to-insight pipeline: 0/1 - No error-to-issue automation.

**Security**
- Branch protection: null/1 - Required administrative access unavailable.
- Secret scanning: null/1 - No local scanner found; native settings unverified without admin access.
- CODEOWNERS: 0/1 - Missing.
- Automated security review: null/1 - Security lint exists, but assessment generation and native scanning remain unverified.
- Dependency-update automation: 1/1 - Active Dependabot PRs and CI-pin updates.
- Comprehensive gitignore: 0/1 - `.env` secret files are not ignored.
- DAST: null/1 - Not a hosted web service.
- PII handling: null/1 - Generic library; downstream spiders determine data collection.
- Privacy compliance: null/1 - No application-owned end-user collection service.
- Secrets management: 1/1 - Actions secrets and PyPI OIDC publishing.
- Log scrubbing: 1/1 - Limited URL-credential sanitization exists; not universal log redaction.

# Action Items
- Add a reproducible development environment and CI smoke checks for test collection, CLI usage, and AGENTS.md commands.
- Enable file-size, complexity, duplication, technical-debt marker, and unused-dependency checks.
- Add secret-file ignores, secret scanning, CODEOWNERS, and a complete PR template.

---
View the full report: https://app.factory.ai/analytics/readiness/https%3A%2F%2Fgithub.com%2Fscrapy%2Fscrapy
```

</details>

<details>
<summary>stable-diffusion-webui: detailed report</summary>

```markdown
# Agent Readiness Report: stable-diffusion-webui

**Level:** 3/5  
**Overall Score:** 42%  
**Generated:** 2026-10-31 00:39:48 UTC  
**Commit:** `82a973c`  
**Branch:** master  

## Summary

| Metric | Value |
|--------|-------|
| Total Criteria | 84 |
| Passed | 30 |
| Failed | 42 |
| Skipped | 12 |

## Pass Rate by Category

| Category | Pass Rate |
|----------|-----------|
| Style & Validation | 25% |
| Build System | 50% |
| Testing | 50% |
| Documentation | 25% |
| Development Environment | 50% |
| Debugging & Observability | 45% |
| Security | 44% |
| Task Discovery | 75% |
| Product & Experimentation | 0% |

## Style & Validation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Type Checker | 0/1 | 🔴 Failed | No mypy, Pyright, TypeScript configuration, or static type-checking CI step exists. |
| Pre-commit Hooks | 0/1 | 🔴 Failed | No checked-in pre-commit, Husky, Lefthook, or custom quality-check Git hooks were found; checks run in CI only. |
| Strict Typing | 0/1 | 🔴 Failed | Python/JavaScript support distinct stricter typing setups, but no strict mypy, Pyright, or TypeScript configuration exists. |
| Naming Consistency | 0/1 | 🔴 Failed | No active naming-convention rules or local documented naming policy were found. Pylint disables every message category. |
| Cyclomatic Complexity | 0/1 | 🔴 Failed | pyproject.toml explicitly ignores Ruff C901, and no alternative configured complexity analyzer or threshold was found. |
| Large File Detection | 0/1 | 🔴 Failed | No size-checking hooks, CI file limits, Git LFS attributes, or active max-lines rules exist. .pylintrc disables all message categories. |
| Duplicate Code Detection | 0/1 | 🔴 Failed | No configured copy-paste/duplicate-code detector or CI duplication check was found. |
| Code Modularization Enforcement | 0/1 | 🔴 Failed | The substantial modules/extensions application has no import-linter configuration, architectural tests, or other enforced module boundaries. |
| Technical Debt Tracking | 0/1 | 🔴 Failed | No debt scanner, enforced issue-linked TODO policy, or configured technical-debt platform was found in repository configuration or workflows. |
| Linter Configuration | 1/1 | 🟢 Passed | Ruff is configured in pyproject.toml and ESLint in .eslintrc.js; the Linter workflow runs both. |
| Code Formatter | 1/1 | 🟢 Passed | npm run fix invokes eslint --fix. ESLint enforces fixable indentation, spacing, braces, semicolons, and newline formatting rules. |
| Dead Code Detection | 1/1 | 🟢 Passed | Ruff keeps its default Pyflakes F checks, including unused imports and unused locals, and CI runs Ruff across the root application. |
| N+1 Query Detection | N/A | Skipped | Not applicable: no application ORM or relational query layer exists. diskcache provides internal local key-value caching, not domain queries. |

## Build System

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Dependencies Pinned | 0/1 | 🔴 Failed | requirements_versions.txt pins most runtime packages, but test requirements use ~=, ESLint uses ^8.40.0, and package-lock.json is ignored rather than committed. |
| Automated PR Review Generation | 0/1 | 🔴 Failed | Previously skipped; authenticated inspection of the latest 10 PRs found no reviews or automated review comments. Local workflows only lint, test, and warn about branch targets. |
| Deployment Frequency | 0/1 | 🔴 Failed | Previously skipped; authenticated release/run inspection found the latest release on 2025-02-09 and no deploy workflows among 50 recent runs. Multiple automated deployments per week are not evidenced. |
| Release Notes Automation | 0/1 | 🔴 Failed | CHANGELOG.md is present, but no changelog generator, release-note automation, or release workflow is configured. |
| Unused Dependencies Detection | 0/1 | 🔴 Failed | No deptry, pip-extra-reqs, depcheck, knip, or equivalent unused-dependency check is configured. |
| Release Automation | 0/1 | 🔴 Failed | The three checked-in workflows perform linting, testing, and branch-target warnings. No automated release, artifact publication, or deployment pipeline exists. |
| Dead Feature Flag Detection | 0/1 | 🔴 Failed | Custom feature flags exist, but no stale-flag scanner, usage/age reporting, or documented flag cleanup lifecycle was found. |
| Build Command Documentation | 1/1 | 🟢 Passed | README Installation and Running documents webui-user.bat and webui.sh, which bootstrap dependencies and launch this Python application. |
| VCS CLI Tools | 1/1 | 🟢 Passed | Previously 0; now gh is installed and gh auth status succeeds. This is an evaluation-environment change, not a source change. |
| Agentic Development | 1/1 | 🟢 Passed | Previously 0; newly available authenticated PR evidence shows Copilot-authored/coauthored commits in PRs #17486, #17487, and #17488. Local shallow history remains one unchanged commit; this is newl... |
| Fast CI Feedback | 1/1 | 🟢 Passed | Previously skipped; 5 of the latest 20 merged PRs retain usable check timestamps. Mean earliest-check-start to latest-check-completion is 4.67 minutes, below 10; 15 PRs lack usable timestamps. |
| Build Performance Tracking | 1/1 | 🟢 Passed | run_tests.yaml caches pip dependencies and models. on_pull_request.yaml explicitly avoids downloading an approximately 4 GB dependency cache to keep lint feedback fast. |
| Single Command Setup | 1/1 | 🟢 Passed | README documents prerequisites and cloning, then one launch command, webui.sh or webui-user.bat, that prepares the environment and starts the application. |
| Feature Flag Infrastructure | 1/1 | 🟢 Passed | modules/options.py persists custom UI/API options. The Hypertile extension defines default-off U-Net/VAE flags and gates its implementation with them. |
| Progressive Rollout | N/A | Skipped | Not applicable: this is a locally operated application, not an infrastructure repository with staged deployments. |
| Rollback Automation | N/A | Skipped | Not applicable: no infrastructure/deployment lifecycle is defined by this application repository. |
| Monorepo Tooling | N/A | Skipped | Not applicable: one root application; built-in extensions are dependent plugins, not independently deployable packages. |
| Heavy Dependency Detection | N/A | Skipped | Not applicable: browser JavaScript is served directly; package.json contains lint tooling, not a JavaScript bundling pipeline. |
| Version Drift Detection | N/A | Skipped | Not applicable: only one build package/module; there are no sibling build modules whose dependency versions require comparison. |

## Testing

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Test Performance Tracking | 0/1 | 🔴 Failed | CI creates test/results.xml but does not retain or analyze that JUnit report, and no duration reporting or test-performance analytics is configured. Retained coverage reports measure coverage. |
| Flaky Test Detection | 0/1 | 🔴 Failed | Previously skipped; the latest 10 PRs have no duplicate check names. No retry, quarantine, randomization, or flaky-test analytics configuration was found locally. |
| Test Coverage Thresholds | 0/1 | 🔴 Failed | CI collects and uploads coverage, but no minimum coverage percentage or blocking coverage gate is configured. |
| Test File Naming Conventions | 0/1 | 🔴 Failed | Tests follow test_*.py informally. pytest configuration only sets base_url; no explicit naming/discovery patterns or local documented test naming policy exists. |
| Test Isolation | 0/1 | 🔴 Failed | No configured xdist, randomization, process sharding, or isolated service/database fixtures exist. API tests share one server. |
| Unit Tests Exist | 1/1 | 🟢 Passed | test/test_torch_utils.py parametrizes a unit test of modules.torch_utils.get_param. |
| Integration Tests Exist | 1/1 | 🟢 Passed | test/test_txt2img.py, test_img2img.py, test_extras.py, and test_utils.py exercise HTTP API endpoints against a running server. |
| Unit Tests Runnable | 1/1 | 🟢 Passed | Previously 0; python -m pytest --collect-only test/test_torch_utils.py exited 0 and collected 2 tests in 2.93s. No tests executed. Bytecode/cache writes were disabled. Missing pytest-base-url cause... |
| Interactive QA Exists | 1/1 | 🟢 Passed | The CI harness specifies Python 3.10.6, test/runtime dependency setup, CPU empty-model server launch, readiness waiting, and HTTP interactions asserting 200. Launcher/API code confirms default no-a... |
| Interactive QA Runnable | 1/1 | 🟢 Passed | Documentation fallback, not runtime-verified: the CI CPU/empty-model harness covers dependencies, no-auth access, startup, and successful API interactions. Preflight found only unsupported Python 3... |

## Documentation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| AGENTS.md File | 0/1 | 🔴 Failed | No root AGENTS.md exists. |
| Skills Configuration | 0/1 | 🔴 Failed | No repository SKILL.md files or skill directories were found. Session-provided skills are not repository configuration. |
| Documentation Freshness | 0/1 | 🔴 Failed | The required git log --since="180 days ago" query found no README.md, AGENTS.md, or CONTRIBUTING.md changes. Available history is shallow. |
| API Schema Docs | 0/1 | 🔴 Failed | Recursive schema-pattern searches found no OpenAPI/Swagger JSON/YAML or GraphQL schema files. Runtime-generated FastAPI documentation does not meet this file-based criterion. |
| Service Architecture Documented | 0/1 | 🔴 Failed | No architecture/sequence diagrams or explicit service-dependency documentation were found. README credits and the UI screenshot do not document service flow. |
| AGENTS.md Freshness Validation | 0/1 | 🔴 Failed | AGENTS.md is absent, and there is no automation validating agent instructions or their commands. |
| README File | 1/1 | 🟢 Passed | Root README.md explains the Gradio image-generation application, features, dependencies, installation, and launch commands. |
| Automated Documentation Generation | 1/1 | 🟢 Passed | webui.py configures FastAPI /docs and /redoc endpoints. API routes and response models support runtime-generated OpenAPI documentation. |

## Development Environment

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Dev Container | 0/1 | 🔴 Failed | No .devcontainer/devcontainer.json or equivalent development-container configuration exists. |
| Environment Template | 1/1 | 🟢 Passed | README documents the python_cmd override and points to webui-user.sh, a commented template for launch, Python, dependency, and repository environment settings. |
| Local Services Setup | N/A | Skipped | Not applicable: default operation uses local model files and diskcache, not an external database, cache, or other required service. |
| Database Schema | N/A | Skipped | Not applicable: no application/domain database schema exists; diskcache manages its internal local key-value store. |
| Devcontainer Runnable | N/A | Skipped | Skipped: the devcontainer CLI is not installed; no devcontainer configuration exists either. |

## Debugging & Observability

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Distributed Tracing | 0/1 | 🔴 Failed | No correlated request/trace ID propagation or distributed tracing is configured. Generation task IDs and X-Process-Time support progress/timing rather than tracing. |
| Error Tracking Contextualized | 0/1 | 🔴 Failed | No contextualized Sentry/Bugsnag/Rollbar-style error tracker is configured. Local traceback collection does not qualify. |
| Alerting Configured | 0/1 | 🔴 Failed | No operational alert rules, PagerDuty/OpsGenie integration, or comparable automated alerting mechanism was found. |
| Runbooks Documented | 0/1 | 🔴 Failed | No incident-response runbook/playbook directory or explicit external runbook pointer was found. Generic support/wiki links and user debugging guidance do not establish an incident runbook. |
| Deployment Observability | 0/1 | 🔴 Failed | No deployment-impact dashboard pointers, deployment annotations, or deploy-notification integrations were found. |
| Circuit Breakers | 0/1 | 🔴 Failed | The API can retrieve external image URLs with requests.get(timeout=30), but no external-call circuit breaker or exponential-backoff policy exists. |
| Structured Logging | 1/1 | 🟢 Passed | modules/logging_config.py is a dedicated logger module with configurable levels, timestamp/name formatting, and console/Rich handlers. |
| Metrics Collection | 1/1 | 🟢 Passed | modules/memmon.py measures GPU memory and peaks; modules/call_queue.py measures request duration and displays performance statistics. |
| Code Quality Metrics Dashboard | 1/1 | 🟢 Passed | run_tests.yaml collects pytest-cov coverage, combines server/test data, prints a report, and retains HTML coverage as a CI artifact. |
| Health Checks | 1/1 | 🟢 Passed | modules/ui.py registers GET /internal/ping, a lightweight application liveness endpoint. |
| Profiling Instrumentation | 1/1 | 🟢 Passed | modules/profiling.py configures torch.profiler CPU/CUDA activities, memory/stack options, and Chrome trace export; processing.py invokes the profiler. |

## Security

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Dependency Update Automation | 0/1 | 🔴 Failed | No Dependabot, Renovate, or equivalent dependency-update automation is configured in the checkout. |
| Gitignore Comprehensive | 0/1 | 🔴 Failed | .gitignore covers models, outputs, venv, node_modules, IDE files, and .DS_Store, but does not exclude .env or .env.* secret files. |
| DAST Scanning | 0/1 | 🔴 Failed | No ZAP, Burp, Nuclei, StackHawk, or equivalent security-focused test job targets the running web application. API tests check functionality. |
| Secrets Management | 0/1 | 🔴 Failed | No secrets-manager integration, encrypted secret configuration, Actions secrets references, or ignored .env plus example-template pattern was found. |
| Minimum Dependency Release Age | 0/1 | 🔴 Failed | No explicit minimum dependency-release age, stability delay, or documented waiting-period policy is configured. |
| CODEOWNERS File | 1/1 | 🟢 Passed | Root CODEOWNERS assigns all paths to @AUTOMATIC1111. |
| PII Handling | 1/1 | 🟢 Passed | The bug-report form tells users to review sysinfo for unwanted personal information before sharing. sysinfo also hides auth arguments and allowlists environment data. |
| Privacy Compliance | 1/1 | 🟢 Passed | The launcher disables Gradio analytics by default; UI blocks explicitly disable analytics. sysinfo limits environment reporting and hides supplied UI/API authentication arguments. |
| Sensitive Data Log Scrubbing | 1/1 | 🟢 Passed | modules/sysinfo.py replaces supplied UI/API auth argument values with <hidden> and limits reported environment keys. This is diagnostic scrubbing, not universal log redaction. |
| Branch Protection | N/A | Skipped | Skipped: authenticated repository metadata reports permissions.admin=false, so branch protection/ruleset enforcement cannot be administratively verified. |
| Secret Scanning | N/A | Skipped | Skipped: no checked-in secret-scanner configuration/workflow was found, and authenticated access lacks admin permission for the native secret-scanning check. |
| Automated Security Review Generation | N/A | Skipped | Skipped: no local report-generating security automation was found, and authenticated access lacks admin permission for the native code-scanning check. |

## Task Discovery

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Issue Labeling System | 0/1 | 🔴 Failed | Local issue forms and live labels provide type and some area/platform labels, but the inspected taxonomy lacks a consistent priority labeling scheme. |
| Issue Templates | 1/1 | 🟢 Passed | .github/ISSUE_TEMPLATE contains structured bug-report and feature-request forms with required information. |
| Backlog Health | 1/1 | 🟢 Passed | Previously skipped; 42/50 sampled open issues (84%) have titles longer than 10 characters and at least one label. None of these 50 issues is older than 365 days. |
| PR Templates | 1/1 | 🟢 Passed | .github/pull_request_template.md requests description, issue context, screenshots, self-review, style compliance, and test confirmation. |

## Product & Experimentation

| Criterion | Score | Status | Rationale |
|-----------|-------|--------|-----------|
| Product Analytics Instrumentation | 0/1 | 🔴 Failed | No product analytics SDK is instrumented; Gradio analytics is intentionally disabled. |
| Error to Insight Pipeline | 0/1 | 🔴 Failed | No error-tracker issue integration, error-to-issue workflow, or alert-driven issue creation is configured. |

---

*Generated by Factory Agent Readiness*
```

</details>

<details>
<summary>stable-diffusion-webui: CLI output</summary>

```markdown
# Level
**Level 3: 41.67%**. Report saved.

30 passed, 42 failed, and 12 skipped across all 84 criteria.

Audited commit: `82a973c`. Primary languages: Python and JavaScript. Source and configuration remain unchanged.

# Applications
1. `.` - Stable Diffusion image-generation application with a Gradio browser UI and optional FastAPI API.

# Criteria
`null/1` means skipped and excluded from scoring.

**Style & Validation**
- Linter configuration: 1/1 - Ruff and ESLint run in CI.
- Type checking: 0/1 - No static type-checking configuration.
- Formatter: 1/1 - ESLint autofix enforces JavaScript formatting.
- Pre-commit hooks: 0/1 - No checked-in quality hooks.
- Strict typing: 0/1 - No strict type-checker configuration.
- Naming consistency: 0/1 - No enforced naming rules or local policy.
- Cyclomatic complexity: 0/1 - Ruff’s complexity check is explicitly ignored.
- Large-file detection: 0/1 - No size limits, hooks, or LFS configuration.
- Dead-code detection: 1/1 - Ruff detects unused imports and locals.
- Duplicate-code detection: 0/1 - No duplication detector configured.
- Code modularization: 0/1 - No enforced architectural boundaries.
- Technical-debt tracking: 0/1 - No debt scanner or enforced tracking policy.
- Unused-dependency detection: 0/1 - No dependency-usage checker.

**Build System**
- Build command documentation: 1/1 - README documents bootstrap and launch commands.
- Pinned dependencies: 0/1 - Development dependencies remain ranged; npm lockfile is ignored.
- Fast CI feedback: 1/1 - Five measurable merged PRs averaged 4.67 minutes.
- Build-performance tracking: 1/1 - Deliberate caching and lint-cache optimizations exist.
- Deployment frequency: 0/1 - Latest release was February 2025; no deployment workflows found.
- Single-command setup: 1/1 - Launch scripts prepare dependencies and start the application.
- Feature-flag infrastructure: 1/1 - Persisted options gate default-off Hypertile features.
- Release-note automation: 0/1 - Changelog exists without automated generation.
- Progressive rollout: null/1 - Not an infrastructure repository.
- Rollback automation: null/1 - No infrastructure deployment lifecycle.
- Monorepo tooling: null/1 - Single application.
- Heavy-dependency detection: null/1 - No JavaScript bundling pipeline.
- Version-drift detection: null/1 - Single build package.
- Release automation: 0/1 - No release or publishing pipeline.
- Dead-feature-flag detection: 0/1 - No stale-flag detection or cleanup lifecycle.
- Minimum release age: 0/1 - No dependency-adoption waiting period.

**Testing**
- Unit tests present: 1/1 - Parametrized `torch_utils` tests exist.
- Integration tests present: 1/1 - Tests exercise running HTTP APIs.
- Unit tests runnable: 1/1 - Bounded collection exited zero and found two tests; none executed.
- Test-performance tracking: 0/1 - JUnit output is neither retained nor analyzed.
- Flaky-test detection: 0/1 - No retry/quarantine configuration or duplicate sampled checks.
- Coverage thresholds: 0/1 - Coverage is collected without a minimum gate.
- Test naming conventions: 0/1 - No explicit discovery patterns or documented naming policy.
- Test isolation: 0/1 - API tests share a server without configured isolation.
- Interactive QA documented: 1/1 - CI specifies dependencies, CPU startup, readiness, and API interactions.
- Interactive QA runnable: 1/1 - Documentation fallback qualifies. Unsupported Python and missing dependencies prevented launch; not runtime-verified.

**Documentation**
- AGENTS.md: 0/1 - Missing at repository root.
- README: 1/1 - Includes purpose, setup, and usage.
- Automated documentation generation: 1/1 - FastAPI generates runtime API documentation.
- Documentation freshness: 0/1 - Required history query found no recent key-document changes.
- API schema files: 0/1 - No committed OpenAPI, Swagger, or GraphQL schema.
- Service-flow documentation: 0/1 - No architecture diagrams or explicit dependency-flow documentation.
- AGENTS.md validation: 0/1 - Neither instructions nor validation exist.
- Runbooks: 0/1 - No explicit incident-response runbook pointers.
- Issue templates: 1/1 - Structured bug and feature forms exist.
- Issue labeling system: 0/1 - Type/area labels exist, but consistent priority labels are missing.
- Backlog health: 1/1 - 42/50 sampled issues have descriptive titles and labels; none exceed one year.
- PR templates: 1/1 - Requests descriptions, context, self-review, and testing confirmation.

**Dev Environment**
- VCS CLI tools: 1/1 - GitHub CLI is installed and authenticated.
- Automated PR review: 0/1 - No automated review content found across ten sampled PRs.
- Agentic development: 1/1 - Remote PR commits show Copilot authorship and coauthorship.
- Skills: 0/1 - No repository-defined skills.
- Devcontainer: 0/1 - No configuration exists.
- Environment template: 1/1 - README and `webui-user.sh` document configuration variables.
- Local services setup: null/1 - Default operation requires no external services.
- Database schema: null/1 - No application database; diskcache manages internal storage.
- Devcontainer runnable: null/1 - Devcontainer CLI is unavailable.

**Debugging & Observability**
- Structured logging: 1/1 - Dedicated configurable logging module exists.
- Distributed tracing: 0/1 - No correlated request/trace propagation.
- Metrics collection: 1/1 - GPU memory and request-duration measurements exist.
- Code-quality metrics: 1/1 - CI retains combined coverage reports.
- Contextualized error tracking: 0/1 - No configured contextual error-tracking service.
- Alerting: 0/1 - No operational alerting integration.
- Deployment observability: 0/1 - No deployment-impact dashboards or notifications.
- Health checks: 1/1 - `/internal/ping` provides application liveness.
- Circuit breakers: 0/1 - External image retrieval lacks circuit breaking or exponential backoff.
- Profiling instrumentation: 1/1 - Torch profiling exports Chrome traces.
- Product analytics: 0/1 - No instrumentation; Gradio analytics is disabled.
- Error-to-insight pipeline: 0/1 - No automated error-to-issue integration.
- N+1 detection: null/1 - No application ORM or relational-query layer.

**Security**
- Branch protection: null/1 - Account lacks administrative access.
- Secret scanning: null/1 - No local scanner; native settings require admin access.
- CODEOWNERS: 1/1 - Root ownership assignment covers all paths.
- Automated security review: null/1 - No local reporting automation; native checks require admin access.
- Dependency-update automation: 0/1 - No Dependabot or Renovate configuration.
- Comprehensive gitignore: 0/1 - Missing `.env` and `.env.*` exclusions.
- DAST scanning: 0/1 - No dynamic security-testing workflow.
- PII handling: 1/1 - Reporting instructions address personal information; diagnostics hide auth arguments.
- Privacy compliance: 1/1 - Analytics defaults and diagnostic minimization provide privacy-by-design measures.
- Secrets management: 0/1 - No qualifying secure secret-management pattern.
- Log scrubbing: 1/1 - Diagnostic reports hide supplied authentication arguments; not universal redaction.

# Action Items
- Add `AGENTS.md` covering setup, checks, and CPU/API QA. Validate its commands in CI.
- Add static typing, pre-commit checks, complexity limits, and a blocking coverage threshold.
- Commit reproducible dependency locks, exclude secret files, and configure dependency updates plus secret scanning.

# Changes Since Last Report
Changes reflect newly available environment tools and remote evidence, not source edits.

- VCS CLI tools: 0/1 → 1/1 - Authenticated GitHub CLI is available.
- Automated PR review: skipped → 0/1 - No review automation found in sampled PRs.
- Agentic development: 0/1 → 1/1 - Remote Copilot contribution evidence found.
- Fast CI feedback: skipped → 1/1 - Measured average is 4.67 minutes.
- Deployment frequency: skipped → 0/1 - Release/run evidence does not meet frequency requirements.
- Backlog health: skipped → 1/1 - Sample meets title, label, and age requirements.
- Unit tests runnable: 0/1 → 1/1 - Pytest successfully collected two tests.
- Flaky-test detection: skipped → 0/1 - No qualifying detection evidence found.

---
View the full report: https://app.factory.ai/analytics/readiness/https%3A%2F%2Fgithub.com%2Fautomatic1111%2Fstable-diffusion-webui
```

</details>


## Part II: Analysis

**Which pillars failed most**, and were failures consistent across all three or specific to one?
> By pass rate, **Product & Experimentation** failed most: 0% in all three repos, but it has only 2 criteria (product analytics and an error-to-issue pipeline). Both assume a hosted product whose maintainers own the runtime. react and scrapy are libraries that run in other people's code, and stable-diffusion-webui deliberately disables analytics, which earns it a Privacy Compliance pass for the same choice. The failure is consistent but says little about these repos.
>
> The more meaningful consistent failure is **Development Environment** (average 33%). Dev Container fails in all three repos, and the cost shows up in the same reports: "Unit Tests Runnable" failed for react and scrapy because the auditing agent couldn't install dependencies (`chalk`, Twisted).
>
> Two criteria fail everywhere regardless of repo: Gitignore Comprehensive (`.env` not ignored) in Security, and the code-quality checks (complexity, large-file, duplicate-code, modularization) in Style & Validation. Beyond those, **Security** is weak mainly in react (14%: no CODEOWNERS, Dependabot disabled, no DAST on its playground). The basic **Style & Validation** checks fail mainly in stable-diffusion-webui (25%: no type checker, strict typing or pre-commit hooks). **Debugging & Observability** (average 42%) is mixed: error tracking, alerting, runbooks and deployment observability fail everywhere, and react is lowest at 21%.
>
> | Category | react | scrapy | stable-diffusion-webui | Average |
> |---|---|---|---|---|
> | Product & Experimentation | 0% | 0% | 0% | 0% |
> | Development Environment | 50% | 0% | 50% | 33% |
> | Debugging & Observability | 21% | 60% | 45% | 42% |
> | Security | 14% | 67% | 44% | 42% |
> | Style & Validation | 55% | 58% | 25% | 46% |

**What explains the pattern?** Which suspects your data supports, and which it cannot distinguish:
> **Agent-era timing does not explain the gap.** stable-diffusion-webui's last commit (July 2024) came before AGENTS.md and skills existed, but removing the four agent-specific criteria barely changes its score (41.7% → 42.6%). Its gap is general engineering hygiene: no type checker, no pre-commit hooks, unpinned dependencies, no release automation. **Inactivity is a better candidate**, because several of its failures need ongoing maintenance to keep passing (Deployment Frequency, Documentation Freshness, Dependency Update Automation). It is also the only single-maintainer repo, though, so my sample cannot separate "one maintainer" from "no longer maintained."
>
> **Language:** the two Python repos differ by 19 points, so language does not explain the difference between them. With one non-Python repo, I can't test language more broadly.
>
> **Size:** the largest repo (react) is not the lowest scorer, so size does not predict the overall score. It does affect react through per-application scoring: 17 of its 42 failures are partial (e.g. 4/7), where some of its seven applications pass and the criterion still fails. Size costs react mostly through how the framework counts a monorepo.
>
> **Backing shapes which categories score well, not the overall rank.** react's Build System score (90%) rests on infrastructure that needs dedicated staff: bundle-size bots on PRs, 50 balanced build shards, automated weekday releases. That fits corporate backing, but react is also the only fully corporate repo, so backing and size can't be separated. react's low Security score (14%) is partly a visibility issue: 5 of 12 security criteria were skipped, 3 for lack of admin access, and some failures are deliberate configuration choices (Dependabot set to open no PRs). scrapy's 67% rests on only 6 scored criteria, mostly dependency hygiene.

**Cheapest high-leverage fix**, per repo:

| Repo | The one change | Why this one, over the report's top suggestion |
|---|---|---|
| react | Expand the root agent file into a map of all 7 applications (path, build and test commands, run `yarn` before tests), as `AGENTS.md`, with `CLAUDE.md` pointing to it | This is the report's own #1, but trimmed to the cheap core. The current 13-line `CLAUDE.md` only separates React from the Compiler, so for any question about DevTools, the playground or the MCP server, an agent has to explore the 7-app monorepo first. Checking the file's commands in CI, the rest of the suggestion, costs more and helps agents less than the map itself. |
| scrapy | Add one explicit line to the existing `AGENTS.md`: "Never run `pytest` directly; tox creates the environment that installs Twisted." | AGENTS.md already says to use `tox -e py`, yet the auditing agent ran pytest and failed on missing Twisted. The gap is an unstated warning, not a missing environment. One line fixes the observed failure. The report's reproducible dev environment plus CI smoke checks would take far more work. |
| stable-diffusion-webui | Declare the required Python version (3.10) in a machine-readable file (`.python-version` / `requires-python`), so the existing pinned environment can be reproduced, before upgrading anything | The audit couldn't start the app because the Python version wasn't supported. The README requires 3.10.6, but only in prose. Runtime dependencies are already pinned in `requirements_versions.txt`. The report's #1, an `AGENTS.md`, would describe an environment the agent still can't build. Upgrading all dependencies is the eventual goal, but after two years without maintenance it's a risky project, not a cheap fix. |

**Where the framework falls short:**
> **A category weighted beyond its relevance: Product & Experimentation.** It failed in all three repos (0%), yet neither of its criteria fits what I scored. Product analytics assumes a hosted product the maintainers can instrument. react and scrapy are libraries that run inside other people's applications, where usage tracking would be a privacy liability. stable-diffusion-webui shows the contradiction most clearly: it deliberately disables Gradio analytics, which earns a pass on Privacy Compliance and a fail on Product Analytics for the same choice. The error-to-insight pipeline has the same problem, since library errors surface in users' apps and reach maintainers as GitHub issues. Nothing in this category affects whether an agent can build, test or change these repos, so it lowers all three scores without describing a real gap. The criteria should be skipped for libraries, the way Health Checks and DAST already are.
>
> **Criteria that don't fit the repo's shape.**
> - *Per-application scoring* treats a monorepo as seven repos that must all pass. 17 of react's 42 failures are partial (e.g. Integration Tests 4/7), where the core runtime passes but smaller tools like the experimental MCP server don't. So react's score partly reflects how many apps it has, not how ready it is.
> - *AGENTS.md* is an exact-filename check. react has a `CLAUDE.md`, a nested `compiler/CLAUDE.md`, and populated skills, yet gets no credit, while any `AGENTS.md`, however thin, would pass. The criterion rewards the filename, not whether an agent gets useful guidance.
>
> **Something it misses: whether maintainers want agents at all.** My first choice, yt-dlp, has a `.NO_AI/README.md` instructing agents to refuse to interact with the repo, and Droid stopped the audit there. The framework has no criterion for this, so a repo could score well and still be off-limits. scrapy, also a community-run Python project, takes the opposite position and has a detailed `AGENTS.md` written for agents. The framework scores whether a repo is equipped for agents, but whether an agent should work there at all depends on the maintainers' policy, which it never checks.
>
> **Scope:** these points come from three scored repos and one that refused the audit, all open-source and most of them libraries. They show where the framework misfits this kind of repo. I can't say how often these issues arise in hosted services or private corporate codebases, where product analytics and per-service scoring may fit well.


## Submission
1. `Command (⌘) + F` for `TODO`. No results means you're done.
2. Push all changes to your remote repository and submit via Gradescope.
