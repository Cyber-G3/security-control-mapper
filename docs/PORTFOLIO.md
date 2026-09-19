# Portfolio Case — Security Control Mapper

## Problem
Technical findings and evidence do not automatically explain which governance or control requirements they support. Naive cross-framework mappings can also overstate equivalence.

## Assurance architecture
```text
Technical observation
       ↓
Normalized finding/evidence
       ↓
Versioned mapping relationship
       ↓
DIRECT / SUPPORTING / CONTEXTUAL
       ↓
Framework reference
       ↓
SUPPORTED / PARTIAL / GAP / UNKNOWN
       ↓
Additional evidence needed
```

## What this demonstrates
- Deterministic cross-framework mapping
- Versioned mapping datasets
- Explicit mapping semantics
- PASS/FAIL/UNKNOWN-aware coverage
- Interoperability with Security Evidence Collector
- Separation of evidence support from compliance conclusions

## Platform role
This project is best treated as an assurance-engine component rather than a standalone compliance product:

Security Evidence Collector → Security Control Mapper → Audit Evidence Readiness / Assurance Workbench.
