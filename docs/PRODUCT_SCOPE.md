# Security Control Mapper — Product Scope

## Product direction

Evolve the project from a GitHub finding mapper into a deterministic Security Control & Risk Explorer that can ingest technical findings from multiple sources, enrich them with business context, prioritize them, and map them to supporting framework references without claiming compliance.

## Core model

```text
Technical Finding
    -> Source / Asset / Sector context
    -> Severity + exploitability + exposure + asset criticality
    -> Deterministic risk priority
    -> Framework mappings
    -> Coverage / evidence gaps
    -> Dashboard / prioritized action plan
```

Risk and compliance remain separate dimensions. A high-risk finding is not automatically a compliance gap, and a mapped framework reference is not proof of conformity.

## Finding catalog

The catalog is extensible rather than hard-coded to a fixed number of findings.

Initial domains:

- Repository governance
- Identity and access
- Secrets and credentials
- CI/CD and software supply chain
- Dependency and vulnerability management
- Configuration and hardening
- Logging and monitoring
- Encryption and key management
- Backup / recovery / resilience
- Incident readiness
- Endpoint / server posture
- Cloud posture
- Third-party / supplier controls
- AI / model governance (future pack)

Each finding should carry a normalized ID, source check ID(s), title, description, technical severity, category, control type, evidence requirements, and framework mappings.

## Framework packs

Current:

- ISO/IEC 27001:2022
- NIS2
- ENS
- SOC 2 Trust Services Criteria

Planned DACH packs:

- BSI IT-Grundschutz
- BSI C5
- Austria Security Framework Bund 2.0

Framework packs must be versioned and sourced. They express relevance/supporting relationships only unless the underlying source explicitly establishes an equivalence.

## Context filters

The web app should support independent filters for:

- Framework
- Country / region
- Sector
- Finding category
- Control family
- Control type
- Mapping confidence
- Technical severity
- Risk priority
- Asset criticality
- Internet exposure
- Evidence coverage status
- Source system

## Sector profiles

Sector profiles adjust prioritization and recommended evidence, not legal applicability by themselves.

Initial profiles:

- General / cross-sector
- SaaS / technology
- Cloud service provider
- Financial services
- Healthcare / life sciences
- Public administration
- Critical infrastructure
- Manufacturing / industrial
- Professional services

## Risk prioritization

Risk scoring must remain deterministic and explainable. Recommended inputs:

- Finding severity
- Asset criticality
- Internet exposure
- Exploitability / active exploitation when available
- Data sensitivity
- Business service criticality
- Compensating controls
- Evidence confidence

Output:

- CRITICAL / HIGH / MEDIUM / LOW
- Numeric score for sorting only
- Reason codes explaining the score
- Recommended remediation urgency

Do not present the score as a regulatory or audit conclusion.

## Dashboard

The management dashboard should show:

- Total findings
- Critical / high findings
- Risk distribution
- Findings by technical domain
- Framework coverage
- SUPPORTED / PARTIAL / GAP / UNKNOWN
- Evidence gaps
- Top remediation priorities
- Findings by sector/profile
- Findings by source
- Mapping confidence distribution
- Trend data when historical snapshots become available

## Interoperability

The mapper should accept normalized observations from:

1. Security Evidence Collector
2. Vulnerability Risk Prioritizer
3. CSV / JSON imports
4. Future source adapters

A normalized observation contract should prevent the core engine from depending on a specific scanner or cloud platform.

## Product boundary

The tool supports security assurance, prioritization, evidence organization, and control analysis. It does not determine certification, legal applicability, audit opinion, or regulatory compliance.
