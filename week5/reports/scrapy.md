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