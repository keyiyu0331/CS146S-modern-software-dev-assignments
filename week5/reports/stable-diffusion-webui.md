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