from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class MappingConfidence(StrEnum):
    DIRECT = "DIRECT"
    SUPPORTING = "SUPPORTING"
    CONTEXTUAL = "CONTEXTUAL"


class CoverageStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    GAP = "GAP"
    UNKNOWN = "UNKNOWN"


class ObservationStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    ERROR = "ERROR"


class FrameworkReference(BaseModel):
    framework: str
    reference: str
    title: str
    relevance: str
    confidence: MappingConfidence = MappingConfidence.CONTEXTUAL


class MappingRecord(BaseModel):
    finding_type: str
    source_check_ids: list[str] = Field(default_factory=list)
    title: str
    description: str
    evidence_needed: list[str] = Field(default_factory=list)
    references: list[FrameworkReference] = Field(default_factory=list)


class MappingSource(BaseModel):
    framework: str
    source: str
    relationship: str


class MappingResult(BaseModel):
    finding_type: str
    title: str
    description: str
    evidence_needed: list[str]
    references: list[FrameworkReference]
    mapping_version: str
    mapping_effective_date: str | None = None
    mapping_metadata_version: str | None = None
    mapping_sources: list[MappingSource] = Field(default_factory=list)
    source_check_id: str | None = None
    source_finding_id: str | None = None
    source_severity: str | None = None
    disclaimer: str = (
        "Control references indicate potential relevance only and do not establish "
        "compliance, certification, legal applicability, or framework equivalence."
    )


class TechnicalObservation(BaseModel):
    check_id: str
    status: ObservationStatus
    reason: str | None = None


class CoverageResult(BaseModel):
    framework: str
    reference: str
    title: str
    status: CoverageStatus
    confidence: MappingConfidence
    supporting_checks: list[str] = Field(default_factory=list)
    failing_checks: list[str] = Field(default_factory=list)
    unknown_checks: list[str] = Field(default_factory=list)
    evidence_needed: list[str] = Field(default_factory=list)
    mapping_version: str
    disclaimer: str = (
        "Coverage is an evidence-support indicator derived from mapped technical observations. "
        "It is not a compliance conclusion or statement that a control is fully implemented."
    )
