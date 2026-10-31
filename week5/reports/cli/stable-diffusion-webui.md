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
