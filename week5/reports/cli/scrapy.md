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
