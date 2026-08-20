from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field


CATALOG_PATH = Path(__file__).with_name("data") / "expected-evidence-v1.json"


class ExpectedEvidenceItem(BaseModel):
    evidence_type: str
    title: str
    required: bool = True


class ExpectedEvidenceRecord(BaseModel):
    framework: str
    reference: str
    title: str
    source: str
    relationship: str
    expected_evidence: list[ExpectedEvidenceItem] = Field(default_factory=list)
    catalog_version: str
    effective_date: str


def load_expected_evidence_catalog(path: Path = CATALOG_PATH) -> list[ExpectedEvidenceRecord]:
    """Load the versioned expected-evidence catalog."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    version = str(payload["catalog_version"])
    effective_date = str(payload["effective_date"])
    return [
        ExpectedEvidenceRecord(
            **record,
            catalog_version=version,
            effective_date=effective_date,
        )
        for record in payload.get("records", [])
    ]


def required_evidence(framework: str, reference: str) -> ExpectedEvidenceRecord | None:
    """Return expected evidence for one exact framework reference."""
    framework_key = framework.casefold().strip()
    reference_key = reference.casefold().strip()
    for record in load_expected_evidence_catalog():
        if (
            record.framework.casefold().strip() == framework_key
            and record.reference.casefold().strip() == reference_key
        ):
            return record
    return None


def expected_evidence_for_references(
    references: list[tuple[str, str]],
) -> list[ExpectedEvidenceRecord]:
    """Resolve expected evidence for multiple framework references without duplicates."""
    results: list[ExpectedEvidenceRecord] = []
    seen: set[tuple[str, str]] = set()
    for framework, reference in references:
        key = (framework.casefold().strip(), reference.casefold().strip())
        if key in seen:
            continue
        seen.add(key)
        record = required_evidence(framework, reference)
        if record is not None:
            results.append(record)
    return results
