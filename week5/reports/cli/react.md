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
