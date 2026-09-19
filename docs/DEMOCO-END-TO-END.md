# DemoCo — Control Mapping Scenario

> Fictional portfolio scenario.

## Input
The Evidence Collector reports:

- branch protection: PASS
- required PR reviews: PASS
- secret scanning: UNKNOWN
- CODEOWNERS: FAIL

## Mapping
The mapper evaluates versioned relationships between those observations and internal/security framework references.

## Expected behaviour
- PASS observations may provide supporting evidence.
- FAIL observations identify evidence-backed gaps.
- UNKNOWN observations remain unresolved.
- Mixed observations can produce PARTIAL support.
- No result is labelled "ISO 27001 compliant" or "NIS2 compliant".

## Assurance hand-off
The output identifies:
- what evidence exists;
- which references it supports;
- what failed;
- what remains unknown;
- what additional evidence should be requested.

## Portfolio lesson
Cross-framework mapping is implemented as explainable evidence relationships, not as automatic equivalence.
