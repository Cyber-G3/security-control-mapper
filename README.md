# SpectraSec Security Control Mapper

Open-source, deterministic mapping engine that relates technical security findings and evidence to control references across multiple frameworks.

> Development status: **Alpha / v0.1-dev**

## Goal

Translate technical observations into structured control references without claiming regulatory compliance or certification.

```text
Security Evidence Collector
          ↓
   Evidence Pack checks
          ↓
Security Control Mapper
          ↓
ISO 27001 / NIS2 / ENS / SOC 2
          ↓
SUPPORTED / PARTIAL / GAP / UNKNOWN
          ↓
Evidence gaps
```

## Current scope

The mapping dataset now covers branch protection, required PR reviews, required status checks, CODEOWNERS, secret scanning, push protection, Dependabot configuration/security updates, Actions policy, Actions SHA pinning, default workflow token permissions, archived repositories and repository security policy.

Mappings are versioned and classify their relationship as `DIRECT`, `SUPPORTING`, or `CONTEXTUAL`. Framework references indicate supporting relevance only; they do not establish legal applicability, conformity, certification, or framework equivalence.

## CLI

```bash
control-map list-findings
control-map map branch-protection-disabled
control-map map secret-scanning-disabled --json
```

Batch mapping:

```bash
control-map map-file findings.csv
control-map map-file findings.json --output mapped-controls.json
```

## Security Evidence Collector integration

Map explicit findings:

```bash
control-map map-collector ./evidence-pack-UUID/findings/findings.json
```

Or evaluate the **complete Evidence Pack**, including PASS, FAIL and UNKNOWN normalized checks:

```bash
control-map coverage-pack ./evidence-pack-UUID
control-map coverage-pack ./evidence-pack-UUID --json
```

The Evidence Pack integration reads `normalized/github/*.json`, which is the deterministic check format produced by `security-evidence-collector`.

## Coverage semantics

- `SUPPORTED`: mapped observations are PASS.
- `PARTIAL`: mixed PASS/FAIL or PASS/UNKNOWN signals exist for the same reference.
- `GAP`: mapped observations contain FAIL without supporting PASS evidence.
- `UNKNOWN`: relevant observations cannot be verified because the source returned UNKNOWN/ERROR.

These are evidence-support indicators, **not compliance statuses**.

For GAP, PARTIAL and UNKNOWN states, the engine returns the evidence still needed to investigate or substantiate the control context.

## Frameworks

Current framework coverage:

- ISO/IEC 27001:2022 / Annex A references
- NIS2 supporting references
- ENS supporting references
- SOC 2 Trust Services Criteria supporting references

ENS mappings are contextual and depend on system category, security dimensions and organizational scope.

## Design principles

- deterministic mappings
- versioned datasets
- source provenance preserved
- PASS/FAIL/UNKNOWN-aware coverage analysis
- explicit evidence requirements
- mapping confidence separated from compliance conclusions
- no LLM dependency at runtime
- machine-readable JSON/CSV output

## Roadmap

- v0.1: core mapping, batch input, Evidence Collector interoperability and coverage engine
- v0.2: richer cross-framework coverage reporting and mapping validation
- v0.3: management reports and mapping-version diff
- v0.4: interactive GitHub Pages explorer

## License

Apache-2.0.
