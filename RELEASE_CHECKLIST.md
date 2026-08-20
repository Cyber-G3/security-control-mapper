# v0.1.0 Release Checklist

## Functional scope

- [x] Deterministic finding-to-control mapping
- [x] Versioned mapping dataset
- [x] ISO/IEC 27001, NIS2, ENS and SOC 2 supporting references
- [x] Mapping confidence semantics
- [x] Batch CSV/JSON mapping
- [x] Security Evidence Collector findings ingestion
- [x] Evidence Pack coverage ingestion
- [x] Coverage Engine
- [x] Evidence Gap Engine
- [x] Assurance reporting
- [x] Versioned Expected Evidence Catalogue
- [x] Deterministic `required_evidence()` lookup
- [x] Mapping provenance and effective-date metadata

## Quality gates

- [x] Ruff configured
- [x] Strict Mypy configured
- [x] pytest configured
- [x] Coverage threshold >=80%
- [x] Bandit configured
- [x] pip-audit configured
- [x] End-to-end smoke workflow configured
- [x] 44 tests passed and 80.43% coverage on release-candidate branch
- [x] CI green on current release-candidate head
- [x] Mapper CLI + coverage smoke workflow green on the pull-request release candidate

## Documentation and governance

- [x] README
- [x] README marks `v0.1.0 Release Candidate`
- [x] SECURITY.md
- [x] LICENSE file
- [x] Release checklist
- [x] GitHub Pages workflow configured
- [x] Public demo files committed
- [x] Bundled repository ZIP removed from release branch
- [ ] GitHub Pages live verification on final release state
- [ ] Public demo smoke check

## Release

- [x] Package version set to 0.1.0
- [x] Release-candidate CI and smoke workflows green
- [ ] Re-run CI/smoke after merge to `main`
- [ ] Tag v0.1.0
- [ ] GitHub Release v0.1.0

## Scope freeze

Do not add new frameworks, cloud collectors, SaaS integrations, or major mapping families before v0.1.0 is published. New capabilities belong to the post-v0.1 roadmap.
