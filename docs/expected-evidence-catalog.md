# Expected Evidence Catalogue v1

The Expected Evidence Catalogue turns a framework/control reference into a deterministic list of evidence types that may support assessment and investigation.

It is intentionally separate from compliance determination.

```text
Framework reference
        ↓
Expected evidence catalogue
        ↓
Evidence types / records expected
        ↓
Evidence Collector / platform evidence
        ↓
Downstream assurance with human review
```

## Public API

```python
from control_mapper.expected_evidence import required_evidence

record = required_evidence("NIS2", "Article 21(2)(d)")
```

The returned record includes:

- `framework`
- `reference`
- `title`
- `source`
- `relationship`
- `catalog_version`
- `effective_date`
- `expected_evidence[]`

Each evidence item includes a normalized `evidence_type`, a human-readable title and a `required` flag used by downstream workflows.

## Boundary

The catalogue states what evidence may reasonably be expected to support a control or requirement context. It does not determine legal applicability, regulatory conformity, certification status or whether supplied evidence is sufficient.

Those decisions belong to downstream assurance workflows and authorized human reviewers.

## Versioning

The initial dataset is `src/control_mapper/data/expected-evidence-v1.json` with `catalog_version=1.0`.

Future changes that alter semantics or identifiers should increment the catalogue version. Consumers should persist both catalogue version and framework/reference identifiers when storing results.
