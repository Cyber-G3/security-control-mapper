from __future__ import annotations

from collections import defaultdict

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


def _effective_confidence(framework: str, configured: MappingConfidence) -> MappingConfidence:
    if configured is not MappingConfidence.CONTEXTUAL:
        return configured
    if framework in {"ISO/IEC 27001:2022", "SOC 2"}:
        return MappingConfidence.SUPPORTING
    return MappingConfidence.CONTEXTUAL


def calculate_coverage(observations: list[TechnicalObservation]) -> list[CoverageResult]:
    version, records = _load_dataset()
    observed = {item.check_id: item for item in observations}
    buckets: dict[tuple[str, str], dict[str, object]] = defaultdict(
        lambda: {
            "title": "",
            "passes": [],
            "fails": [],
            "unknowns": [],
            "evidence": set(),
            "confidences": [],
        }
    )

    for record in records:
        matched = [observed[cid] for cid in record.source_check_ids if cid in observed]
        if not matched:
            continue
        for reference in record.references:
            key = (reference.framework, reference.reference)
            bucket = buckets[key]
            bucket["title"] = reference.title
            confidence = _effective_confidence(reference.framework, reference.confidence)
            bucket["confidences"].append(confidence)  # type: ignore[union-attr]
            for observation in matched:
                if observation.status is ObservationStatus.PASS:
                    bucket["passes"].append(observation.check_id)  # type: ignore[union-attr]
                elif observation.status is ObservationStatus.FAIL:
                    bucket["fails"].append(observation.check_id)  # type: ignore[union-attr]
                    bucket["evidence"].update(record.evidence_needed)  # type: ignore[union-attr]
                elif observation.status in {ObservationStatus.UNKNOWN, ObservationStatus.ERROR}:
                    bucket["unknowns"].append(observation.check_id)  # type: ignore[union-attr]
                    bucket["evidence"].update(record.evidence_needed)  # type: ignore[union-attr]

    results: list[CoverageResult] = []
    for (framework, reference), bucket in buckets.items():
        passes = sorted(set(bucket["passes"]))  # type: ignore[arg-type]
        fails = sorted(set(bucket["fails"]))  # type: ignore[arg-type]
        unknowns = sorted(set(bucket["unknowns"]))  # type: ignore[arg-type]
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
        confidences = bucket["confidences"]  # type: ignore[assignment]
        confidence = max(confidences, key=lambda item: _CONFIDENCE_RANK[item])
        results.append(
            CoverageResult(
                framework=framework,
                reference=reference,
                title=str(bucket["title"]),
                status=status,
                confidence=confidence,
                supporting_checks=passes,
                failing_checks=fails,
                unknown_checks=unknowns,
                evidence_needed=sorted(bucket["evidence"]),  # type: ignore[arg-type]
                mapping_version=version,
            )
        )
    return sorted(results, key=lambda item: (item.framework, item.reference))
