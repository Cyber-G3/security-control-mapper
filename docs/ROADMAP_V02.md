# Security Control Mapper — v0.2 Roadmap

## Product direction

Evolve the project from a technical finding mapper into an explainable, local-first Security Assurance, Risk & Control Explorer.

The project must keep three concepts separate:

1. **Technical evidence** — what was actually observed.
2. **Risk context** — how important the observation is for a specific asset/business context.
3. **Control relevance / coverage** — which framework references the observation can support.

A score or mapping must never be presented as a certification, legal applicability decision, or compliance determination.

## P0 — Finding Catalog

Target an extensible catalog rather than a fixed list. Initial domains:

- Repository Security
- Identity & Access Management
- Privileged Access
- Secrets Management
- Vulnerability Management
- Patch Management
- Endpoint Security
- Network Security
- Cloud Security
- CI/CD Security
- Software Supply Chain
- Logging & Monitoring
- Cryptography
- Backup & Recovery
- Incident Response
- Business Continuity / Disaster Recovery
- Third-Party Risk
- Governance
- Data Protection
- AI Security / AI Governance

Each finding should support stable ID, title, description, category, source type, default severity, affected asset, remediation guidance, evidence requirements, and framework mappings.

## P0 — Framework Packs

Framework data must be independently versioned and provenance-aware.

Initial packs:

- ISO/IEC 27001:2022
- NIS2 supporting references
- ENS
- SOC 2 Trust Services Criteria
- BSI IT-Grundschutz
- BSI C5
- Austria Security Framework Bund

Candidate later packs:

- NIST CSF 2.0
- CIS Controls v8.1
- DORA
- PCI DSS 4.x
- ISO/IEC 42001

Do not label cross-framework relationships as equivalence unless an authoritative source explicitly establishes that relationship.

## P0 — Risk Context Engine

Keep the deterministic risk engine explainable. Inputs can include:

- technical severity
- asset criticality
- service criticality
- Internet exposure
- active exploitation
- data sensitivity
- compensating controls
- sector profile

Outputs:

- 0–100 contextual score
- LOW / MEDIUM / HIGH / CRITICAL priority
- reason codes
- remediation urgency

## P1 — Sector Profiles

Initial profiles:

- General
- SaaS / Technology
- Cloud Provider
- Financial Services
- Healthcare / Life Sciences
- Public Sector
- Critical Infrastructure
- Manufacturing / Industrial
- Professional Services

Sector profiles may tune risk context, evidence expectations and dashboard defaults. They must not automatically determine legal applicability.

## P1 — Evidence Quality

Evidence status should go beyond present/missing:

- PRESENT
- MISSING
- STALE
- INCOMPLETE
- UNVERIFIED

Quality dimensions:

- provenance
- collection timestamp
- age/freshness
- integrity verification
- owner
- source system
- completeness

## P1 — Remediation Engine

For every actionable gap, expose:

- finding/control reference
- contextual priority
- recommended remediation
- evidence expected after remediation
- suggested owner role
- estimated effort band
- target urgency
- compensating-control notes

Recommendations are guidance, not automated approval or compliance conclusions.

## P1 — Dashboard

Views:

### Executive
- overall risk distribution
- critical/high findings
- evidence coverage
- framework coverage
- top remediation priorities
- risk by asset/sector
- trend vs previous assessment

### Assurance / Audit
- control coverage
- evidence quality
- missing/stale evidence
- mapping confidence
- provenance
- framework filters

### Technical
- finding
- source/resource
- severity
- contextual risk
- reason codes
- remediation
- supporting evidence

Filters:

- framework
- region/country
- sector
- finding/category
- control family
- control type
- mapping confidence
- severity
- contextual priority
- asset criticality
- Internet exposure
- coverage status
- evidence quality
- source

## P2 — What-if Analysis

Allow users to select remediation candidates and estimate the deterministic effect on:

- open findings
- contextual risk distribution
- control coverage
- evidence gaps

The simulator must state that projections depend on the selected assumptions and do not prove remediation effectiveness.

## P2 — Historical Snapshots

Compare assessments over time:

- new findings
- resolved findings
- reopened findings
- risk movement
- evidence freshness
- coverage movement
- remediation throughput

## P2 — Custom Controls

Allow organizations to load an internal control library without modifying built-in framework packs. Preserve source/provenance and distinguish custom controls visually and in exports.

## P2 — Interoperability

Inputs/outputs should support, where semantically appropriate:

- Evidence Pack
- JSON
- CSV
- SARIF
- CycloneDX

Integrate with `security-evidence-collector` and `vulnerability-risk-prioritizer` through documented schemas rather than repository-specific assumptions.

## P3 — Local API

Expose the deterministic engines through a local API for automation and integration. Authentication, rate limiting and deployment hardening become requirements before recommending network-exposed operation.

## Non-goals

- automated certification decisions
- automated legal applicability decisions
- opaque AI-generated compliance scores
- claiming framework equivalence without authoritative provenance
- replacing professional audit judgement

## Proposed product flow

```text
COLLECT
Evidence / Findings
    ↓
NORMALIZE
Stable finding taxonomy
    ↓
PRIORITIZE
Contextual risk engine
    ↓
MAP
Versioned framework packs
    ↓
ASSESS
Coverage + evidence quality
    ↓
REMEDIATE
Prioritized action plan
    ↓
REPORT
Technical / Assurance / Executive dashboards
```
