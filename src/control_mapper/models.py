from __future__ import annotations

from pydantic import BaseModel, Field


class FrameworkReference(BaseModel):
    framework: str
    reference: str
    title: str
    relevance: str


class MappingRecord(BaseModel):
    finding_type: str
    title: str
    description: str
    evidence_needed: list[str] = Field(default_factory=list)
    references: list[FrameworkReference] = Field(default_factory=list)


class MappingResult(BaseModel):
    finding_type: str
    title: str
    description: str
    evidence_needed: list[str]
    references: list[FrameworkReference]
    mapping_version: str
    disclaimer: str = (
        "Control references indicate potential relevance only and do not establish "
        "compliance, certification, legal applicability, or framework equivalence."
    )
