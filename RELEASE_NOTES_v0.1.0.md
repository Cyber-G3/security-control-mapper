# Security Control Mapper v0.1.0

Initial public release of the deterministic security finding-to-control mapping engine.

## Included
- deterministic finding-to-control mapping
- versioned mapping dataset
- ISO/IEC 27001, NIS2, ENS and SOC 2 supporting references
- mapping confidence semantics
- batch CSV/JSON mapping
- Security Evidence Collector findings ingestion
- Evidence Pack coverage ingestion
- Coverage Engine and Evidence Gap Engine
- assurance reporting
- versioned Expected Evidence Catalogue
- deterministic required_evidence() lookup
- mapping provenance and effective-date metadata

## Quality gates
- Ruff
- strict Mypy
- pytest with >=80% coverage threshold
- Bandit
- pip-audit
- end-to-end mapper smoke workflow

## Release scope
This release intentionally excludes new frameworks, cloud collectors, SaaS integrations and major mapping families. Those belong to post-v0.1 development.
