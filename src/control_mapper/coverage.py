from __future__ import annotations

from dataclasses import dataclass, field

from control_mapper.engine import _load_dataset
from control_mapper.models import (
    CoverageResult,
    CoverageStatus,
    MappingConfidence,
    ObservationStatus,
    TechnicalObservation,
)

_CONFIDENCE_RANK = {
    MappingConfidence.CONTEXTUAL: 1,
    MappingConfidence.SUPPORTING: 2,
    MappingConfidence.DIRECT: 3,
}


@dataclass
class _CoverageBucket:
    title: str = ""
    passes: set[str] = field(default_factory=set)
    fails: set[str] = field(default_factory=set)
    unknowns: set[str] = field(default_factory=set)
    evidence: set[str] = field(default_factory=set)
    confidences: list[MappingConfidence] = field(default_factory=list)


def _effective_confidence(framework: str, configured: MappingConfidence) -> MappingConfidence:
    if configured is not MappingConfidence.CONTEXTUAL:
        return configured
    if framework in {"ISO/IEC 27001:2022", "SOC 2"}:
        return MappingConfidence.SUPPORTING
    return MappingConfidence.CONTEXTUAL


def calculate_coverage(observations: list[TechnicalObservation]) -> list[CoverageResult]:
    version, records, _metadata = _load_dataset()
    observed = {
        item.check_id: item
        for item in observations
        if item.status is not ObservationStatus.NOT_APPLICABLE
    }
    buckets: dict[tuple[str, str], _CoverageBucket] = {}

    for record in records:
        matched = [observed[cid] for cid in record.source_check_ids if cid in observed]
        if not matched:
            continue
        for reference in record.references:
            key = (reference.framework, reference.reference)
            bucket = buckets.setdefault(key, _CoverageBucket())
            bucket.title = reference.title
            bucket.confidences.append(
                _effective_confidence(reference.framework, reference.confidence)
            )
            for observation in matched:
                if observation.status is ObservationStatus.PASS:
                    bucket.passes.add(observation.check_id)
                elif observation.status is ObservationStatus.FAIL:
                    bucket.fails.add(observation.check_id)
                    bucket.evidence.update(record.evidence_needed)
                elif observation.status in {ObservationStatus.UNKNOWN, ObservationStatus.ERROR}:
                    bucket.unknowns.add(observation.check_id)
                    bucket.evidence.update(record.evidence_needed)

    results: list[CoverageResult] = []
    for (framework, reference), bucket in buckets.items():
        passes = sorted(bucket.passes)
        fails = sorted(bucket.fails)
        unknowns = sorted(bucket.unknowns)
        if fails and passes:
            status = CoverageStatus.PARTIAL
        elif fails:
            status = CoverageStatus.GAP
        elif unknowns and passes:
            status = CoverageStatus.PARTIAL
        elif unknowns:
            status = CoverageStatus.UNKNOWN
        else:
            status = CoverageStatus.SUPPORTED
        confidence = max(bucket.confidences, key=_CONFIDENCE_RANK.__getitem__)
        results.append(
            CoverageResult(
                framework=framework,
                reference=reference,
                title=bucket.title,
                status=status,
                confidence=confidence,
                supporting_checks=passes,
                failing_checks=fails,
                unknown_checks=unknowns,
                evidence_needed=sorted(bucket.evidence),
                mapping_version=version,
            )
        )
    return sorted(results, key=lambda item: (item.framework, item.reference))
