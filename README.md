# SpectraSec Security Control Mapper

Open-source, deterministic mapping engine that relates technical security findings and evidence to control references across multiple frameworks.

> Development status: **Alpha / v0.1-dev**

## Goal

Translate technical findings into structured control references without claiming regulatory compliance or certification.

```text
Finding / Evidence
      ↓
Normalized finding type
      ↓
Versioned mapping dataset
      ↓
ISO 27001 / NIS2 / ENS / SOC 2 references
      ↓
Coverage context + evidence needs
```

## Initial scope

The first version focuses on common software and repository security findings such as branch protection disabled, required pull-request reviews disabled, required status checks disabled, secret scanning disabled, dependency scanning unavailable, security policy missing, CODEOWNERS missing, and workflow permissions too broad.

## CLI

```bash
control-map list-findings
control-map map branch-protection-disabled
control-map map secret-scanning-disabled --json
```

## Design principles

- deterministic mappings
- versioned datasets
- framework references separated from compliance conclusions
- explicit evidence requirements
- no LLM dependency at runtime
- machine-readable JSON output

## Frameworks

Initial framework coverage:

- ISO/IEC 27001:2022 / Annex A references
- NIS2 supporting references
- ENS supporting references
- SOC 2 Trust Services Criteria supporting references

Mappings indicate potential relevance only. They are not legal determinations or statements of equivalence.

## Roadmap

- v0.1: core mapping engine, CLI, versioned mappings and tests
- v0.2: batch input and CSV/JSON exports
- v0.3: integration format for Security Evidence Collector findings
- v0.4: interactive GitHub Pages explorer

## License

Apache-2.0.
