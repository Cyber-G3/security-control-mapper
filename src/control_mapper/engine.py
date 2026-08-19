from __future__ import annotations

import json
from importlib.resources import files

from control_mapper.models import MappingRecord, MappingResult


def _load_dataset() -> tuple[str, list[MappingRecord]]:
    path = files("control_mapper").joinpath("data/mappings-v0.1.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    version = str(payload["mapping_version"])
    records = [MappingRecord.model_validate(item) for item in payload["records"]]
    return version, records


def list_finding_types() -> list[str]:
    _, records = _load_dataset()
    return sorted(record.finding_type for record in records)


def map_finding(finding_type: str) -> MappingResult:
    normalized = finding_type.strip().lower()
    version, records = _load_dataset()
    for record in records:
        if record.finding_type == normalized:
            return MappingResult(
                finding_type=record.finding_type,
                title=record.title,
                description=record.description,
                evidence_needed=record.evidence_needed,
                references=record.references,
                mapping_version=version,
            )
    raise KeyError(f"Unknown finding type: {finding_type}")
