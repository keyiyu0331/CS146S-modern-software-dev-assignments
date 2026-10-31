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