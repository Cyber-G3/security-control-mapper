from __future__ import annotations

import json
from importlib.resources import files

from control_mapper.models import MappingRecord, MappingResult, MappingSource


def _load_dataset() -> tuple[str, list[MappingRecord], dict[str, object]]:
    data_dir = files("control_mapper").joinpath("data")
    mapping_path = data_dir.joinpath("mappings-v0.1.json")
    metadata_path = data_dir.joinpath("mapping-metadata-v0.1.json")

    payload = json.loads(mapping_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    version = str(payload["mapping_version"])
    if str(metadata.get("mapping_version")) != version:
        raise ValueError("Mapping dataset and provenance metadata versions do not match")
    records = [MappingRecord.model_validate(item) for item in payload["records"]]
    return version, records, metadata


def list_finding_types() -> list[str]:
    _, records, _ = _load_dataset()
    return sorted(record.finding_type for record in records)


def _to_result(
    record: MappingRecord,
    version: str,
    metadata: dict[str, object],
    *,
    source_check_id: str | None = None,
    source_finding_id: str | None = None,
    source_severity: str | None = None,
) -> MappingResult:
    raw_sources = metadata.get("sources", [])
    if not isinstance(raw_sources, list):
        raise ValueError("Mapping provenance sources must be a list")
    mapping_sources = [MappingSource.model_validate(item) for item in raw_sources]
    return MappingResult(
        finding_type=record.finding_type,
        title=record.title,
        description=record.description,
        evidence_needed=record.evidence_needed,
        references=record.references,
        mapping_version=version,
        mapping_effective_date=str(metadata.get("effective_date")) if metadata.get("effective_date") else None,
        mapping_metadata_version=(
            str(metadata.get("metadata_version")) if metadata.get("metadata_version") else None
        ),
        mapping_sources=mapping_sources,
        source_check_id=source_check_id,
        source_finding_id=source_finding_id,
        source_severity=source_severity,
    )


def map_finding(finding_type: str) -> MappingResult:
    normalized = finding_type.strip().lower()
    version, records, metadata = _load_dataset()
    for record in records:
        if record.finding_type == normalized:
            return _to_result(record, version, metadata)
    raise KeyError(f"Unknown finding type: {finding_type}")


def map_check_id(
    check_id: str,
    *,
    finding_id: str | None = None,
    severity: str | None = None,
) -> MappingResult:
    normalized = check_id.strip().lower()
    version, records, metadata = _load_dataset()
    for record in records:
        if normalized in {item.lower() for item in record.source_check_ids}:
            return _to_result(
                record,
                version,
                metadata,
                source_check_id=check_id,
                source_finding_id=finding_id,
                source_severity=severity,
            )
    raise KeyError(f"Unknown source check ID: {check_id}")
